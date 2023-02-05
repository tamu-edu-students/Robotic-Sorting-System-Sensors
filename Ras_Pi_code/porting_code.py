import numpy as np
import cv2
import math

#read image and display it
img = cv2.imread("Cropped_Image.jpg")
#cv2.imshow("first",img)


#crop the black square
crop_blk = img[0:140, 0:140]
#cv2.imshow("crop it", crop_blk)
gray_squ = cv2.cvtColor(crop_blk, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray it", gray_squ)
ret,thresh1 = cv2.threshold(gray_squ,110,255,cv2.THRESH_BINARY)
cv2.imshow("Binary", thresh1)

#modying the image to remove the black square
pix_val = img[140, 140]
b = pix_val[0]
g = pix_val[1]
r = pix_val[2]
#print(img[0,0,2])
#print(b, g, r)
i=0
while i < 140:
    j = 0
    while j < 140:
        img[i,j,0] = b
        img[i,j,1] = g
        img[i,j,2] = r
        j = j+1
    i = i+1
#cv2.imshow('modify img', img)

#how much pixel is in an inch
contours,hierarchy = cv2.findContours(thresh1, 1, 2)
cnt = contours[0]
area = cv2.contourArea(cnt)
print("area: ",area)
pix_p_inch = math.sqrt(area)
print("pixels per inch is ", pix_p_inch)


#BGR to HSV
hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#Determining if the pixel belong to white background or the object
low = np.array([0,42,0])
#high = np.array([220,255,255])
high = np.array([179,255,255])
mask = cv2.inRange(hsv_frame, low, high)
cv2.imshow("mask",mask)


#determing the boundaries of the object
r= len(mask)
c= len(mask[0])
#print("number of row is ", r)
#print("number of column is ", c)


foundTop = False
foundBottom = False
foundLeft = False
foundRight = False

#top bound
i = 0
top = None
while(foundTop == 0) and (i< r):
    arr = mask[i]
    is_all_zero = np.all(arr == 0)
    if is_all_zero:
        foundTop = False
        i = i+1
    else:
        foundTop = True
        top = i
#print("top value is ", top)
        
#bottom bound
i = r - 1
bottom = None
while(foundBottom == 0) and (i >= 0):
    arr = mask[i]
    is_all_zero = np.all(arr == 0)
    if is_all_zero:
        foundBottom = False
        i = i - 1
    else:
        foundBottom = True
        bottom = i
#print("bottom value is ", bottom)

#left bound
i = 0
left = None
while (foundLeft == 0) and (i < c):
    arr = mask[:,i]
    is_all_zero = np.all(arr == 0)
    if is_all_zero:
        foundLeft = False
        i = i + 1
    else:
        foundLeft = True
        left = i
        
#print("Left index is ", left)
        
#right bound
        #does () differ from this (())
i = c - 1
right = None
while (foundRight == 0) and (i >= 0):
    arr = mask[:, i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundLeft = False
        i = i - 1
    else:
        foundRight = True
        right = i
#print("Right value is ", right)
        
crop_img = img[top:bottom, left:right]
crop_hsv_frame = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
#cv2.imshow("cropped", crop_img)
#cv2.imshow("cropped hsv", crop_hsv_frame)
crop_mask = mask[top:bottom, left:right]
#cv2.imshow("cropped mask", crop_mask)
#boxxing in the object
cv2.rectangle(img,(left,top),(right, bottom),(10,255,10),3)
cv2.imshow("square_img", img)

########### implendmet colors percentage 
num_red = 0
num_orange = 0
num_yellow = 0
num_green = 0
num_blue = 0
num_violet = 0

collect_hue = np.array([])
i = 0
j = 0
while i < (bottom - top):
    j = 0
    while j < (right - left):
        if crop_mask[i,j] == 255:
            pixel = crop_hsv_frame[i,j]
            hue_value = pixel[0]
            collect_hue = np.append(collect_hue, hue_value)
            ### update 2/5
            if hue_value < 5:
                num_red = num_red + 1
            elif hue_value < 22:
                num_orange = num_orange + 1
            elif hue_value < 33:
                num_yellow = num_yellow + 1
            elif hue_value < 78:
                num_green = num_green + 1
            elif hue_value < 131:
                num_blue = num_blue + 1
            elif hue_value < 167:
                num_violet = num_violet + 1
            else:
                num_red = num_red + 1
            ### 2/5
        j = j + 1
    i = i + 1
obj_pixel = collect_hue.size
col_mean = np.mean(collect_hue)
col_median = np.median(collect_hue)
print("the number of pixels within the object: ", obj_pixel)
print("mean of the collected hue is ", col_mean)
print("median of the collected hue is ", col_median)
#print("how long")

#deteriming the hue of the object
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
print("Object hue is ",color)

##### 2/5
###########calculating the hue composion of the object
totalpix = num_red + num_orange + num_yellow + num_green + num_blue + num_violet
print("total pixel of the obj is ", totalpix)
print("red percent: " ,100*num_red/totalpix)
print("orange percent: " ,100*num_orange/totalpix)
print("yellow percent: " ,100*num_yellow/totalpix)
print("green percent: " ,100*num_green/totalpix)
print("blue percent: " ,100*num_blue/totalpix)
print("violet percent: " ,100*num_violet/totalpix)
##### 2/5

height = (bottom - top)/pix_p_inch
print("height in inches: ", height)
width = (right - left)/pix_p_inch
print("width in inches: ", width)







cv2.waitKey(0)
cv2.destroyAllWindows()
