import cv2
import numpy as np
import math


#this py file will sense color and size of the fruit with integrating with the conveyor

#determining if the pixel belong to the object or the black conveyor belt background
#image_bgr = cv2.imread('background1crop.PNG')
image_bgr = cv2.imread('one_inch2.PNG')
cv2.imshow("first", image_bgr)

gray_squ = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
gray_squ = cv2.fastNlMeansDenoising(gray_squ,None,10,7,21)
kernel = np.ones((5,5),np.uint8)
ret,thresh1 = cv2.threshold(gray_squ,140,255,cv2.THRESH_BINARY)
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
cv2.imshow("Binary", thresh1)

result1 = cv2.bitwise_and(image_bgr,image_bgr,mask=thresh1)  ##the object with the converyor belt background

r = len(thresh1)
c = len(thresh1[0])

foundTop = False
foundBottom = False
foundLeft = False
foundRight = False



i = 0                                 #find top
top = None
while (foundTop == 0) and (i < r):
    arr = thresh1[i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundTop = False
        i = i + 1
    else:
        foundTop = True
        top = i
        #print("Top index is ", top)
i = r - 1                           #find bottom
bottom = None
while (foundBottom == 0) and (i >= 0):
    arr = thresh1[i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundBottom = False
        i = i - 1
    else:
        foundBottom = True
        bottom = i
        #print("Bottom index is ", bottom)

                                       #find left
i = 0
left = None
while (foundLeft == 0) and (i < c):
    arr = thresh1[:,i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundLeft = False
        i = i + 1
    else:
        foundLeft = True
        left = i
        #print("Left index is ", left)

                                       #find right
i = c - 1
right = None
while (foundRight == 0) and (i >= 0):
    arr = thresh1[:,i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundLeft = False
        i = i - 1
    else:
        foundRight = True
        right = i
        #print("Right index is ", right)

                                       #crop the img
crop_img = image_bgr[top:bottom, left:right]

crop_hsv_frame = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
cv2.imshow("cropped",crop_img)


crop_mask = thresh1[top:bottom, left:right]
cv2.imshow("cropped mask",crop_mask)
cv2.rectangle(image_bgr,(left,top),(right,bottom),(10,255,10),3)      #add a rectangle around the object
cv2.imshow("square_img",image_bgr)

#find the color of the object for the cropped img

collect_hue = np.array([])
#print(collect_hue.size)

i = 0
j = 0
#count = 0
while i < (bottom - top):
    j = 0
    while j < (right - left):
        #count = count + 1
        
        if crop_mask[i,j] == 255:
            pixel = crop_hsv_frame[i, j]
            hue_value = pixel[0] 
            collect_hue = np.append(collect_hue, hue_value)
        
        j = j + 1
        
    i = i + 1
#print(crop_mask.size)
#print(collect_hue.size)
#print(collect_hue[50])
#print(collect_hue[100])
#print(collect_hue[1050])
obj_pixel = collect_hue.size
col_mean = np.mean(collect_hue)
col_median = np.median(collect_hue)
print(col_mean)
print(col_median)

color = "undefine"
if col_median < 5:
    color = "RED"
elif col_median < 22:
    color = "ORANGE"
elif col_median < 33:
    color = "YELLOW"
elif col_median < 78:
    color = "GREEN"
elif col_median < 131:
    color = "BLUE"
elif col_median < 167:
    color = "VIOLET"
else:
    color = "RED"

print(color)


pix_p_inch = 171.35                      ###### NOTE: change this when you find the acutual pixel per inch

#find the size of the object
height = (bottom - top)
print("height by pixels: ", height)
width = (right - left)
print("width by pixels: ", width)
height = (bottom - top)/pix_p_inch
print("height by inch: ", height)
width = (right - left)/pix_p_inch
print("width by inch: ", width)


cv2.waitKey(0) 
cv2.destroyAllWindows() 