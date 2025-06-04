import warnings, os
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('ultralytics/cfg/models/v11_exp/LGM_YOLO.yaml')
    # model.load('yolo11n.pt') # loading pretrain weights
    model.train(data='dataset/data.yaml',
                cache=False,
                imgsz=640,
                epochs=200,
                batch=8,
                close_mosaic=0,
                workers=4,
                optimizer='SGD', # using SGD
                project='runs/train',
                name='exp',
                )