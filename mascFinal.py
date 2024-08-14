import rclpy
import cv2
import time
import random
import argparse
from rclpy.node import Node
from rclpy.time import Time
from rclpy.executors import SingleThreadedExecutor
from vision_msgs.msg import Detection2DArray
from sensor_msgs.msg import Image
from std_msgs.msg import Header
from cv_bridge import CvBridge
from nav_msgs.msg import OccupancyGrid
from ultralytics import YOLO
import numpy as np

path = "/home/renato/nato/deteccaoWS/src/deteccao/deteccao/"
timestr = time.strftime("%Y%m%d_%H%M%S")

def load_classes():
    rede = "dnn_model/dataSegmentation.yaml"
    with open(path + rede, 'r') as config_file:
        config_data = config_file.read()

    class_names_start = config_data.find("names: [") + len("names: [")
    class_names_end = config_data.find("]", class_names_start)
    class_names_str = config_data[class_names_start:class_names_end]
    class_names = [name.strip().strip("'") for name in class_names_str.split(",")]

    return class_names

def class_colors(names):
    return {name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for name in names}

class segmentationPub(Node):
    def __init__(self, show, raw, infer):
        super().__init__('image_segmentation')

        self.raw = raw
        self.infer = infer
        self.show = show
        
        # - - - subscription

        self.subscription = self.create_subscription(Image, 'video_frames', self.listener_callback, 10)

        # - - - publisher

        if raw:
            self.raw_publisher = self.create_publisher(Image, 'image_raw', 10)

        if infer:
            self.infer_publisher = self.create_publisher(Image, 'image_bb', 10)

        self.occupancy_grid_publisher = self.create_publisher(OccupancyGrid, 'occupancy_grid', 10)

        # - - - model

        self.model = YOLO(path + "dnn_model/bestSegmentation.pt")
        self.classes = load_classes()
        self.color = class_colors(self.classes)

        self.br = CvBridge()

    def listener_callback(self, data):
        self.get_logger().info('Receiving video frame')
        frame = self.br.imgmsg_to_cv2(data)

        size = (data.width, data.height)
        min_y = int(data.height * 0.25)  # Ignora a parte superior (1/4 da imagem)
        mask_height = data.height - min_y

        try:
            results = self.model(frame)
            result = results[0]

            segmentation_contours_idx = []
            for seg in result.masks.xyn:
                seg[:, 0] *= size[0]
                seg[:, 1] *= size[1]
                segment = np.array(seg, dtype=np.int32)
                segmentation_contours_idx.append(segment)

            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            yoloClasses = np.array(result.boxes.cls.cpu(), dtype="int")
            scores = np.array(result.boxes.conf.cpu())

            grid = OccupancyGrid()
            header = Header()
            header.stamp = self.get_clock().now().to_msg()
            header.frame_id = 'mapa'
            grid.header = header

            grid.info.resolution = 0.1
            grid.info.width = mask_height * 3  # Ajustado para ter 3 vezes a altura
            grid.info.height = data.width  # Após rotação, a altura se torna a largura original
            grid.info.origin.position.x = 0.0
            grid.info.origin.position.y = 0.0
            grid.info.origin.position.z = 0.0
            grid.info.origin.orientation.w = 1.0

            # Cria uma máscara de ocupação considerando apenas os 3/4 mais altos da imagem
            mask = np.zeros((mask_height, data.width), dtype=np.uint8)

            for bbox, class_id, seg, score in zip(bboxes, yoloClasses, segmentation_contours_idx, scores):
                className = self.classes[class_id]

                if className == "vegetation":
                    seg = seg[seg[:, 1] >= min_y]  # Considera apenas a área de interesse
                    seg[:, 1] -= min_y  # Ajusta a posição vertical para a máscara reduzida
                    cv2.fillPoly(mask, [seg], 255)  # Preenche o polígono da classe "vegetation"

                #if className in mostraPoly:
                    cv2.polylines(frame, [seg], True, self.color[className], 3)

            # Estica a máscara verticalmente para ter o triplo da altura
            mask_stretched = np.zeros((mask_height * 3, data.width), dtype=np.uint8)
            for y in range(mask_height):
                mask_stretched[3*y:3*(y+1), :] = mask[y, :]

            # Faz o flip horizontal na máscara esticada
            mask_stretched_flipped = cv2.flip(mask_stretched, 1)  # 1 indica flip horizontal

            # Rotaciona a máscara de ocupação em 90 graus
            mask_rotated = np.rot90(mask_stretched_flipped, k=-1)  # k=-1 para rotação no sentido horário

            # Define o deslocamento necessário
            offset_x = 0.0
            offset_y = 60.0

            # Aplica o deslocamento no mapa
            grid.info.origin.position.x = -offset_x
            grid.info.origin.position.y = -offset_y

            # Define o grid de ocupação
            data_grid = []
            for y in range(mask_rotated.shape[0]):
                for x in range(mask_rotated.shape[1]):
                    if mask_rotated[y, x] == 255:
                        data_grid.append(100)  # Dentro do polígono (pintado)
                    else:
                        data_grid.append(-1)  # Fora do polígono (não pintado)

            # Verifica se o tamanho dos dados corresponde ao tamanho esperado
            if len(data_grid) != grid.info.width * grid.info.height:
                raise ValueError(f"Tamanho dos dados não corresponde: width={grid.info.width}, height={grid.info.height}")

            grid.data = data_grid
            self.occupancy_grid_publisher.publish(grid)

            if self.show:
                frame = cv2.resize(frame, None, fx=0.6, fy=0.6)
                cv2.imshow("Image", frame)
                cv2.waitKey(1) & 0xff

            if self.infer:
                self.infer_publisher.publish(self.br.cv2_to_imgmsg(frame))

        except Exception as e:
            print(f"Erro: {e}")

def main(args=None):
    print("ok")
    rclpy.init(args=args)

    parser = argparse.ArgumentParser()
    parser.add_argument('--show', type=int, default=0, help='Set to 1 to display images')
    parser.add_argument('--raw', type=int, default=0, help='Set to 1 to enable raw image publishing')
    parser.add_argument('--infer', type=int, default=1, help='Set to 1 to enable inferenced image publishing')
    
    args = parser.parse_args()

    image_publisher = segmentationPub(args.show, args.raw, args.infer)
    try:
        while rclpy.ok():
            rclpy.spin_once(image_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        image_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
