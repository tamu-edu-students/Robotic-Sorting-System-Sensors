from asyncio.windows_events import NULL
from pickletools import int4
import cv2
import numpy as np
import math


img = cv2.imread('banana_blk_sq.PNG')
#consider the square inch on the top left conner
#extact it and edit the img to remove it

#from blk_sq_test.py
##################################################################
cv2.imshow('first', img)

#use to measure this
crop_blk = img[0:140, 0:140]
cv2.imshow('crop+_black', crop_blk)
#contevt to grayscale and reduce noise
gray_squ = cv2.cvtColor(crop_blk, cv2.COLOR_BGR2GRAY)
gray_squ = cv2.fastNlMeansDenoising(gray_squ,None,10,7,21)
cv2.imshow('gray squ', gray_squ)

#threshold it to get a black square and white background
ret,thresh1 = cv2.threshold(gray_squ,110,255,cv2.THRESH_BINARY)
cv2.imshow("Binary", thresh1)



#modying the img to remove the black square
#print('pix val', img[140,140])
pix_val = img[140,140]
b = pix_val[0]
g = pix_val[1]
r = pix_val[2]
#print(b,g,r)


i=0
while i < 140:
    j = 0
    while j < 140:
        img[i,j,0] = b
        img[i,j,1] = g
        img[i,j,2] = r
        j = j + 1
    i = i + 1
cv2.imshow('modify img', img)


#how much pixel is in an inch?
contours,hierarchy = cv2.findContours(thresh1, 1, 2)
cnt = contours[0]
M = cv2.moments(cnt)
#print( M )
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt,True)
print("area: ",area)

pix_p_inch = math.sqrt(area)
print("pixels per inch is", pix_p_inch)
##################################################################

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow('img', img)



cv2.imshow('Gray image', gray)
#red mask takes the red color as true
#low_red_l = np.array([0, 130, 84])
#high_red_l = np.array([5, 255,255])
#red_mask_l = cv2.inRange(hsv_frame, low_red_l, high_red_l)
#cv2.imshow("red mask",red_mask_l)

#cancel the white background, all colors not white background, thresholding, detect the object
low = np.array([0, 42, 0])
high = np.array([179,255,255])
mask = cv2.inRange(hsv_frame, low, high)
cv2.imshow("mask",mask)


#crop the object from the image
#print(mask)
#top
#bottom
#left
#right
r = len(mask)
c = len(mask[0])
#print("number of rows ",r)
#print("number of column ",c)
#val = mask[0][0]
#print(val) # print out '0' for black
#val = mask[200][200]
#print(val) # print out '255' for white

foundTop = False
foundBottom = False
foundLeft = False
foundRight = False

#arr = mask[200]
#is_all_zero = np.all((arr == 0))
#if is_all_zero:
#    print('Array contains only 0')
#else:
#    print('Array has non-zero items too')




i = 0                                 #find top
top = NULL
while (foundTop == 0) and (i < r):
    arr = mask[i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundTop = False
        i = i + 1
    else:
        foundTop = True
        top = i
        #print("Top index is ", top)
i = r - 1                           #find bottom
bottom = NULL
while (foundBottom == 0) and (i >= 0):
    arr = mask[i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundBottom = False
        i = i - 1
    else:
        foundBottom = True
        bottom = i
        print("Bottom index is ", bottom)

                                       #find left
i = 0
left = NULL
while (foundLeft == 0) and (i < c):
    arr = mask[:,i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundLeft = False
        i = i + 1
    else:
        foundLeft = True
        left = i
        print("Left index is ", left)

                                       #find right
i = c - 1
right = NULL
while (foundRight == 0) and (i >= 0):
    arr = mask[:,i]
    is_all_zero = np.all((arr == 0))
    if is_all_zero:
        foundLeft = False
        i = i - 1
    else:
        foundRight = True
        right = i
        print("Right index is ", right)

                                       #crop the img
crop_img = img[top:bottom, left:right]

crop_hsv_frame = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
cv2.imshow("cropped",crop_img)

#cv2.imshow("cropped hsv img",crop_hsv_frame)
crop_mask = mask[top:bottom, left:right]
cv2.imshow("cropped mask",crop_mask)
cv2.rectangle(img,(left,top),(right,bottom),(10,255,10),3)      #add a rectangle around the object
cv2.imshow("square_img",img)




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
"""
print(crop_mask[100, 200])
print(crop_hsv_frame[100, 200])
print(crop_img[100, 200])
pixel = crop_hsv_frame[100, 200]
hue_value = pixel[0]
collect_hue = np.append(collect_hue, hue_value)
print("the collect hue is ", int(collect_hue))
"""


#find the size of the object
height = (bottom - top)
print("height by pixels: ", height)
width = (right - left)
print("width by pixels: ", width)
height = (bottom - top)/pix_p_inch
print("height by inch: ", height)
width = (right - left)/pix_p_inch
print("width by inch: ", width)


#try to find the scarring/ damage
crop_gray = gray[top:bottom, left:right]

#with thresholding
ret,thresh = cv2.threshold(crop_gray,150,255,cv2.THRESH_BINARY)
#thresh = cv2.adaptiveThreshold(crop_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
cv2.imshow("cropped gray",crop_gray)
cv2.imshow("cropped thresh",thresh)

#with canny edge detection
edges = cv2.Canny(crop_img, 100, 70,3)
cv2.imshow("Canny edge", edges)

cv2.waitKey(0) 
cv2.destroyAllWindows()
