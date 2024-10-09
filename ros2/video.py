import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImagePublisher(Node):

    def __init__(self, video_path):
        super().__init__('image_publisher')
        self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
        self.br = CvBridge()

        # Caminho do vídeo .avi
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            self.get_logger().error('Error opening video file')
            rclpy.shutdown()

    def publish_video(self):
        while rclpy.ok():
            ret, frame = self.cap.read()
            if ret:
                img_msg = self.br.cv2_to_imgmsg(frame)
                self.publisher_.publish(img_msg)
                self.get_logger().info('Publishing video frame')
                rclpy.spin_once(self, timeout_sec=0.1)
            else:
                self.get_logger().info('End of video file reached')
                break
        self.cap.release()

def main(args=None):
    rclpy.init(args=args)
    video_path = '/home/renato/nato/deteccaoWS/src/deteccao/deteccao/videos/estradaEscuro00.mp4'
    image_publisher = ImagePublisher(video_path)
    image_publisher.publish_video()
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
