# import the necessary packages
import numpy as np
import imutils
import os
import time
import cv2


# load the image image, convert it to grayscale, and detect edges
img = cv2.imread(r'template.PNG')
template = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]


path = r'Images'
image_files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        image_files.append(os.path.join(r, file))


for imagePath in image_files:

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None

    cannyimg = cv2.Canny(gray, 50, 200)

    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
    	# resize the image according to the scale, and keep track
    	# of the ratio of the resizing
    	resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
    	r = gray.shape[1] / float(resized.shape[1])
    	# if the resized image is smaller than the template, then break
    	# from the loop
    	if resized.shape[0] < tH or resized.shape[1] < tW:
    		break


    	# detect edges in the resized, grayscale image and apply template
    	# matching to find the template in the image
    	edged = cv2.Canny(resized, 50, 200)
    	result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
    	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    	# if we have found a new maximum correlation value, then update
    	# the bookkeeping variable
    	if found is None or maxVal > found[0]:
    		found = (maxVal, maxLoc, r)


    # unpack the bookkeeping variable and compute the (x, y) coordinates
    # of the bounding box based on the resized ratio
    if found is None:
        continue
    print(imagePath,image.shape)
    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))


    # draw a bounding box around the detected result and display the image
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)


    cv2.imshow("Template", img)
    # cv2.imshow("Template_Gray_Canny", template)
    # cv2.imshow("Image_gray_Canny", cannyimg)

    (H, W) = image.shape[:2]

    if H > 1000 or W > 1000:
        newimage = cv2.resize(image,(720,640))
    else:
        newimage = image

    
    cv2.imshow("Image", newimage)
    cv2.waitKey(3000)

    