import numpy as np
import imutils
import os
import time
import cv2


def pre_processing(img):
    if img is None:
        return 0 
    image = img.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(image, 50, 200)
    return image

def scalling_algo(frame):
    found = None
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = imutils.resize(frame, width = int(frame.shape[1] * scale))

        if resized.shape[0] < tH or resized.shape[1] < tW:
    		continue

        processed_video_frame = pre_processing(frame)

    	result = cv2.matchTemplate(processed_video_frame, processed_template_img, cv2.TM_CCOEFF)

        








img = cv2.imread(r'template.PNG')
processed_template_img = pre_processing(img)
(tH, tW) = processed_template_img.shape[:2]
# cv2.imshow("template_img",processed_template_img)
# cv2.waitKey(0)


cap = cv2.VideoCapture(r"Video.mp4")
while True:
    sucess, frame = cap.read()
    result = scalling_algo(frame)

    if result is True:
        print("\nMatched")
    else:
        print("\n Match Not Found")

    
    if frame is None:
        break

    # cv2.imshow("processed_video_frame",processed_video_frame)
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
