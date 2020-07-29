import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread(r'img2.jpeg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
print(img.shape)
# img = cv2.resize(img,(720,640))


# # Detecting Characters

# Himg,Wimg,_ = img.shape
# boxes = pytesseract.image_to_boxes(img)  #fetching co-ordinates of each alphabate

# for b in boxes.splitlines():
#     b = b.split()   #create a list
#     x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])

#     #create a rectangular box
#     # cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)  #Normally we use this
#     cv2.rectangle(img,(x,Himg-y),(w,Himg-h),(0,0,255),1)  #but for this we are going to use it
#     # cv2.putText(img,b[0],(x,Himg-y+25),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),1)




# Detecting Words

Himg,Wimg,_ = img.shape
boxes = pytesseract.image_to_data(img)  #fetching co-ordinates of each word here it have 12 columns

for x,b in enumerate(boxes.splitlines()):
    if x!= 0:
        b = b.split()
        print(b)
        if len(b) == 12:
            x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img,(x,y),(w+x,h+y),(255,51,51),int(0.5))  
            # cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),1)



cv2.imshow("Result",img)
cv2.waitKey(0)