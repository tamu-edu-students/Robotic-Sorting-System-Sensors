import cv2
import numpy as np
import math

#this py file will determine the pixel per inch with integrating with the conveyor
##given image that may of being cropped or resized

image_bgr = cv2.imread('one_inch2.PNG')
cv2.imshow("first", image_bgr)

gray_squ = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
gray_squ = cv2.fastNlMeansDenoising(gray_squ,None,10,7,21)
kernel = np.ones((5,5),np.uint8)
ret,thresh1 = cv2.threshold(gray_squ,140,255,cv2.THRESH_BINARY)
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
cv2.imshow("Binary", thresh1)

contours,hierarchy = cv2.findContours(thresh1, 1, 2)
cnt = contours[0]
M = cv2.moments(cnt)
#print( M )
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt,True)
print("area: ",area)

pix_p_inch = math.sqrt(area)
print("pixels per inch is", pix_p_inch)

cv2.waitKey(0) 
cv2.destroyAllWindows() 