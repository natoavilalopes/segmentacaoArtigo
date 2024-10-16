Repositório de arquivos relacionados ao artigo Assistance for Navigation of Autonomous Vehicles on Rural Roads using Instance Segmentation, submetido ao [WVC 2024](https://wvc2024.ufv.br/). 

Links relevantes:

Base de imagens rotuladas (Roboflow):  
[Roboflow](https://universe.roboflow.com/visao/segmentacaoartigo)

Aplicação em funcionamento (Colab):  
[segmentation.ipynb](https://drive.google.com/file/d/1YawDZ0nHZAdeMwvynjYwxzdAlTJUzYA1)

Processo de treinamento (Colab):  
[segmentation_train.ipynb](https://drive.google.com/file/d/1fyGCk_hMf-kYg62ASMaOle7XChxBypXY/view?usp=sharing)

Implementação da máscara (Colab):  
[segmentation_masc](https://drive.google.com/file/d/1geuenAERbRxV3mJRK5N0UJElBtjgY2wP/view?usp=sharing)

Drive com todo material (Google Drive):  
[Drive](https://drive.google.com/drive/folders/111J7AjpR_V6OwRjB4cvlGyN7BakrBLgs)

O diagrama de blocos em [Method.png](https://github.com/natoavilalopes/segmentationArticle/blob/main/Method.png) fornece uma representação visual das etapas principais envolvidas no método proposto de navegação autônoma. O processo começa com a coleta de dados, onde imagens e vídeos são capturados usando uma câmera monocular instalada em um veículo. Posteriormente, a geração do conjunto de dados envolve o processamento dos dados capturados para criar um conjunto de dados rotulado que é usado para treinar o modelo de segmentação. O modelo de segmentação baseado em YOLOv8 é então treinado neste conjunto de dados. Uma vez treinado, o modelo é aplicado para realizar a segmentação de instância em imagens em tempo real. Os resultados da segmentação são utilizados para criar uma máscara que diferencia áreas navegáveis (estradas) de áreas não navegáveis (vegetação, obstáculos). Uma representação de grade de ocupação do ambiente é então gerada com base na segmentação. Finalmente, a grade de ocupação, juntamente com outras informações relevantes, é usada para planejamento de navegação e tomada de decisão. As setas no diagrama indicam o fluxo de dados e informações entre os vários estágios de processamento.

O arquivo [labels.png](https://github.com/natoavilalopes/segmentationArticle/blob/main/labels.png) mostra a quantidade de objetos rotulados por classe no dataset durante o treinamento, juntamente com as técnicas de aumento de dados.

- - - - - - - - - - - - - - - - -   


Repository of files related to the article Assistance for Navigation of Autonomous Vehicles on Rural Roads using Instance Segmentation, submitted to [WVC 2024](https://wvc2024.ufv.br/).

Relevant links:

Labeled image database (Roboflow):  
[Roboflow](https://universe.roboflow.com/visao/segmentacaoartigo)

Working application (Colab):  
[segmentation.ipynb](https://drive.google.com/file/d/1YawDZ0nHZAdeMwvynjYwxzdAlTJUzYA1)

Training process (Colab):  
[segmentation_train.ipynb](https://drive.google.com/file/d/1fyGCk_hMf-kYg62ASMaOle7XChxBypXY/view?usp=sharing)

Mask implementation (Colab):  
[segmentation_masc](https://drive.google.com/file/d/1geuenAERbRxV3mJRK5N0UJElBtjgY2wP/view?usp=sharing)

Drive with all material (Google Drive):  
[Drive](https://drive.google.com/drive/folders/111J7AjpR_V6OwRjB4cvlGyN7BakrBLgs)

The block diagram in [Method.png](https://github.com/natoavilalopes/segmentationArticle/blob/main/Method.png) provides a visual representation of the key steps involved in the proposed autonomous navigation method. The process begins with data collection, where images and videos are captured using a monocular camera mounted on a vehicle. Subsequently, dataset generation involves processing the captured data to create a labeled dataset that is used to train the segmentation model. The YOLOv8-based segmentation model is then trained on this dataset. Once trained, the model is applied to perform instance segmentation on real-time images. The segmentation results are utilized to create a mask that differentiates navigable areas (roads) from non-navigable areas (vegetation, obstacles). An occupancy grid representation of the environment is then generated based on the segmentation. Finally, the occupancy grid, along with other relevant information, is used for navigation planning and decision-making. The arrows in the diagram indicate the flow of data and information between the various processing stages.

File [labels.png](https://github.com/natoavilalopes/segmentationArticle/blob/main/labels.png) shows the number of objects labeled by class in the dataset during training, along with the data augmentation techniques.
