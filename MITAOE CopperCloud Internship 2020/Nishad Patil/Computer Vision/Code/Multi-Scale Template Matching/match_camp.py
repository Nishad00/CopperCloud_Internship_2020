import numpy as np
import imutils
import os
import time
import cv2



def edge_detection(image):
	orig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 75, 200)
	return edged


def contour_detection(edged):
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	return cnts
	

def loop_and_filter(image,cnts,a):
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if len(approx) == 4:
			if (( approx[0][0][0] - approx[1][0][0] ) + ( approx[2][0][0] - approx[3][0][0] ) + ( approx[0][0][1] - approx[3][0][1] ) + ( approx[1][0][1] - approx[2][0][1] )) < a and (( approx[0][0][0] - approx[1][0][0] ) + ( approx[2][0][0] - approx[3][0][0] ) + ( approx[0][0][1] - approx[3][0][1] ) + ( approx[1][0][1] - approx[2][0][1] )) > -a:
				cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)	
				ca = max(c, key = cv2.contourArea)
				return cv2.minAreaRect(c)



def distance_to_camera(knownWidth, focalLength, perWidth):
	return (knownWidth * focalLength) / perWidth



def distance(marker,image):
	inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
	cv2.putText(image, "%.2fI" % (inches),(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)
				





img = cv2.imread(r'notebook_template.jpeg')
# img = cv2.imread(r'template.PNG')
template = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]






# cap = cv2.VideoCapture(r"Video.mp4")
cap = cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)





KNOWN_DISTANCE = 12.0
KNOWN_WIDTH = 1.5
marker = None


# Image Template Capture

Timg = cv2.imread(r'distance.PNG')
Tedge = edge_detection(Timg)
Tcnts = contour_detection(Tedge)
marker = loop_and_filter(Timg,Tcnts,5)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH




while True:
    sucess, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None
    cannyimg = cv2.Canny(gray, 50, 200)

    for scale in np.linspace(0.1, 1.0, 10)[::-1]:
        resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])
    
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
       
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
            
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)


    edged = edge_detection(image)
    cnts = contour_detection(edged)
    marker = loop_and_filter(image,cnts,50)
    
    if marker != None:
        distance(marker,image)
        
       
    if found is None:
        continue



    (maxVal, maxLoc, r) = found

    if float(maxVal) > 15000000.0:

        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        c = cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)

    cv2.imshow("Video",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break