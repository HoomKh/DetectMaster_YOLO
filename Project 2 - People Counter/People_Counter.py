import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

#For Videos
cap = cv2.VideoCapture("../Videos/people.mp4")

model = YOLO("../YOLO_Weights/yolov8n.pt")


classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

#Read mask img
mask = cv2.imread("mask.png")

#Tracking
tracker = Sort(max_age = 20, min_hits = 2, iou_threshold = 0.3)

#make point for line
limit_up = [103, 161, 296, 161]
limit_down = [527, 489, 735, 489]

#make total count
total_count_up = []
total_count_down = []

while True:
    success, img = cap.read()
    imgRegion = cv2.bitwise_and(img, mask)

    imgGraphics = cv2.imread("graphics.png", cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img, imgGraphics, (730, 260))

    results = model(imgRegion, stream=True)

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:

        #Bounding Box

            #use OpenCv
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            #use CvZone
            w, h = x2 - x1, y2 - y1


        #Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # print(conf)


        #ClassName
            cls = int(box.cls[0])
            currenClass = classNames[cls]

            if currenClass == "person" and conf > 0.25:
                # cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=0.6, thickness=1, offset = 3)
                # cvzone.cornerRect(img, (x1, y1, w, h), l=8)
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    resultsTrack = tracker.update(detections)

    #make line
    cv2.line(img, (limit_up[0], limit_up[1]), (limit_up[2], limit_up[3]), (0, 0, 255), 5)
    cv2.line(img, (limit_down[0], limit_down[1]), (limit_down[2], limit_down[3]), (0, 0, 255), 5)

    for result in resultsTrack:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(result)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt = 2, colorR = (255, 0, 0))
        cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)), scale = 2, thickness = 3,
                           offset = 10)

        #make center point of each car
        cx ,cy = x1 + w // 2 , y1 + h // 2
        cv2.circle(img, (cx, cy), 5,(0, 0, 255), cv2.FILLED)

        if limit_up[0] < cx < limit_up[2] and limit_up[1] - 15 < cy < limit_up[1] + 15:
            if total_count_up.count(id) == 0:
                total_count_up.append(id)
                cv2.line(img, (limit_up[0], limit_up[1]), (limit_up[2], limit_up[3]), (0, 255, 0), 5)

        if limit_down[0] < cx < limit_down[2] and limit_down[1] - 15 < cy < limit_down[1] + 15:
            if total_count_down.count(id) == 0:
                total_count_down.append(id)
                cv2.line(img, (limit_down[0], limit_down[1]), (limit_down[2], limit_down[3]), (0, 255, 0), 5)


    # # cvzone.putTextRect(img, f' Count: {len(totalCount)}', (50, 50))
    cv2.putText(img, str(len(total_count_up)), (929, 345), cv2.FONT_HERSHEY_PLAIN, 5, (139, 195, 75), 7)
    cv2.putText(img, str(len(total_count_down)), (1191, 345), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 230), 7)

    cv2.imshow('Image', img)
    # cv2.imshow('imageRegion', imgRegion)
    cv2.waitKey(1)

