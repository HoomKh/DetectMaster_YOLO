from ultralytics import YOLO
import cv2

model = YOLO('../YOLO_Weights/yolov8l.pt')
result = model("images/4.jpg", show=True)
cv2.waitKey(0)
