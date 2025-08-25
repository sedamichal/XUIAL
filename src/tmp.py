import cv2
import time


device_idx = 0

cap = cv2.VideoCapture(device_idx)

for i in range(10):
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"{i}.jpg", frame)
    time.sleep(2)
