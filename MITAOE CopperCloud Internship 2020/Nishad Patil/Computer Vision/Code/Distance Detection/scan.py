import numpy as np
import argparse
import cv2
import imutils


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
				
	

cap = cv2.VideoCapture(0)	
cap.set(3,1080)
cap.set(4,720)

KNOWN_DISTANCE = 12.0
KNOWN_WIDTH = 1.5
marker = None


# Image Template Capture

Timg = cv2.imread(r'distance.PNG')
# cv2.imshow('m',Timg)
Tedge = edge_detection(Timg)
Tcnts = contour_detection(Tedge)
marker = loop_and_filter(Timg,Tcnts,5)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH





while True:

	sucess, img = cap.read()
	edged = edge_detection(img)
	cnts = contour_detection(edged)
	image = img.copy()

	marker = loop_and_filter(image,cnts,50)

	if marker != None:
		distance(marker,image)

		
	cv2.imshow("Outline", image)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

