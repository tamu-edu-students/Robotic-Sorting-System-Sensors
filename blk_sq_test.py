from asyncio.windows_events import NULL
from pickletools import int4
import cv2
import numpy as np
import math

#create 2 img, the blck square for measure, and obj img w/o black square
img = cv2.imread('banana_blk_sq.PNG')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('img', img)
#cv2.imshow('gray o img', gray)

crop_blk = img[0:140, 0:140]
gray_squ = cv2.cvtColor(crop_blk, cv2.COLOR_BGR2GRAY)
gray_squ = cv2.fastNlMeansDenoising(gray_squ,None,10,7,21)
cv2.imshow('gray squ', gray_squ)

ret,thresh1 = cv2.threshold(gray_squ,110,255,cv2.THRESH_BINARY)
cv2.imshow("Binary", thresh1)
"""""
gray_squ = cv2.cvtColor(crop_blk, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray squ', gray_squ)
thresh = cv2.adaptiveThreshold(gray_squ, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
cv2.imshow("Binary", thresh)
elem = cv2.getStructuringElement(cv2.MORPH_CROSS, [3,3])
erosion_dst = cv2.dilate(thresh, elem)
cv2.imshow("dilate", erosion_dst)
dil_dst =  cv2.erode(erosion_dst, elem)
cv2.imshow("open", dil_dst)
dil_dst = cv2.dilate(dil_dst, elem)
dil_dst =  cv2.erode(dil_dst, elem)
cv2.imshow("open1", dil_dst)
dil_dst = cv2.dilate(dil_dst, elem)
dil_dst =  cv2.erode(dil_dst, elem)
cv2.imshow("open2", dil_dst)
dil_dst = cv2.dilate(dil_dst, elem)
dil_dst =  cv2.erode(dil_dst, elem)
cv2.imshow("open3", dil_dst)



#noisy
#thresholding
#dst = cv2.fastNlMeansDenoisingColored(crop_blk,None,10,10,7,21)
hsv_crop_blk = cv2.cvtColor(crop_blk, cv2.COLOR_BGR2HSV)
low = np.array([0, 27, 0])
high = np.array([179,255,255])
squ = cv2.inRange(hsv_crop_blk, low, high)
cv2.imshow("mask",squ)
#closing
elem = cv2.getStructuringElement(cv2.MORPH_CROSS, [3,3])
squ = cv2.dilate(squ, elem)
squ = cv2.erode(squ, elem)

cv2.imshow("closing",squ)
squ = cv2.dilate(squ, elem)
squ = cv2.erode(squ, elem)

cv2.imshow("closing1",squ)
squ = cv2.dilate(squ, elem)
squ = cv2.erode(squ, elem)

cv2.imshow("closing2",squ)
"""
cv2.imshow('crop+_black', crop_blk)
#print('pix val', img[140,140])

#removing the black square from img
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

#gray = cv2.cvtColor(crop_blk, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray img', gray)
#how much pixel is in an inch?
""""
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
cv2.imshow("Binary", thresh)

_, contours, hierarchy = cv2.findContours(squ, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    area = cv2.contourArea(c)
    perimeter = cv2.arcLength(c, True)
    print("AREA: {}, perimeter: {}", format(area, perimeter))


ret,thresh = cv2.threshold(crop_blk,127,255,0)"""
contours,hierarchy = cv2.findContours(thresh1, 1, 2)
cnt = contours[0]
M = cv2.moments(cnt)
#print( M )
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt,True)
print("area: ",area)
print(perimeter)

#x,y,w,h = cv2.boundingRect(cnt)
#cv2.rectangle(thresh1,(x,y),(x+w,y+h),(0,255,0),2)
#I trust area give a better measurement
pix_p_inch = math.sqrt(area)
print("pixels per inch is", pix_p_inch)

#boundaing the square

cv2.imshow("squaring",thresh1)



cv2.waitKey(0) 
cv2.destroyAllWindows()
