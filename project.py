from asyncio.windows_events import NULL
from pickletools import int4
import cv2
import numpy as np


img = cv2.imread('yellow_banana_1.PNG')

hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow('img', img)

#red mask takes the red color as true
low_red_l = np.array([0, 130, 84])
high_red_l = np.array([5, 255,255])
red_mask_l = cv2.inRange(hsv_frame, low_red_l, high_red_l)
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
print("number of rows ",r)
print("number of column ",c)
val = mask[0][0]
print(val) # print out '0' for black
val = mask[200][200]
print(val) # print out '255' for white

foundTop = False
foundBottom = False
foundLeft = False
foundRight = False

arr = mask[200]
is_all_zero = np.all((arr == 0))
if is_all_zero:
    print('Array contains only 0')
else:
    print('Array has non-zero items too')


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
        print("Top index is ", top)

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
crop_img = img[top:bottom, left:right]
crop_hsv_frame = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
cv2.imshow("cropped",crop_img)
#cv2.imshow("cropped hsv img",crop_hsv_frame)
crop_mask = mask[top:bottom, left:right]
cv2.imshow("cropped mask",crop_mask)
cv2.rectangle(img,(left,top),(right,bottom),(10,255,10),3)
cv2.imshow("square_img",img)
#find the color of the object

collect_hue = np.array([])
print(collect_hue.size)

i = 0
j = 0
count = 0
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
print(crop_mask.size)
print(collect_hue.size)
print(collect_hue[50])
print(collect_hue[100])
print(collect_hue[1050])
print(np.mean(collect_hue))
print(np.median(collect_hue))
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


cv2.waitKey(0) 