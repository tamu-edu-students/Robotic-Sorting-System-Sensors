
import cv2
import numpy as np

####Asssuming that the conveyor belt is clean 
####Assuming that the converyor belt won't reflect light
##### who am i kidding, this converyor belt is prob gonna be noisy

#image_bgr = cv2.imread('background1crop.PNG')
#image_bgr = cv2.imread('one_inch.PNG')
image_bgr = cv2.imread('one_inch_bright.PNG')

gray_squ = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
gray_squ = cv2.fastNlMeansDenoising(gray_squ,None,10,7,21)
cv2.imshow('gray squ', gray_squ)

#ret,thresh1 = cv2.threshold(gray_squ,110,255,cv2.THRESH_BINARY)
ret,thresh1 = cv2.threshold(gray_squ,140,255,cv2.THRESH_BINARY)
cv2.imshow("Binary", thresh1)
result1 = cv2.bitwise_and(image_bgr,image_bgr,mask=thresh1)
cv2.imshow("result1", result1)
###########################################################################
#^---------this would filter black background

# using histogram equalization to remove noise
"""
equ = cv2.equalizeHist(gray_squ)
res = np.hstack((gray_squ,equ)) #stacking images side-by-side
cv2.imshow("applying histogram equalization", res)
ret,thresh2 = cv2.threshold(res,140,255,cv2.THRESH_BINARY)
cv2.imshow("Binary thresh2", thresh2)  """ #### the result ampily the noise, so yeah don't use this



##### using Morphological Transformations to try to remove the noise from lighting
kernel = np.ones((15,15),np.uint8)
opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
cv2.imshow("opening MT Binary thresh1", opening)   #### this work for one_inch.PNG, but not for one_inch_bright.PNG



"""
##### using Adaptive Thresholding to try to remove the noise from lighting
th2 = cv2.adaptiveThreshold(gray_squ,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(gray_squ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
apadtive = np.hstack((th2,th3)) #stacking images side-by-side
cv2.imshow("ADAPTIVE_THRESH_MEAN and ADAPTIVE_THRESH_GAUSSIAN_C", apadtive)     #### this won't work for one_inch.PNG
"""


"""
# Otsu's thresholding
ret2,th4 = cv2.threshold(gray_squ,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("Otsu", th4)                 #### this won't work for one_inch.PNG
"""


# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(gray_squ,(5,5),0)
ret3,th4 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("Otsu after Gaussian filtering", th4)   #### this work for one_inch.PNG, but not for one_inch_bright.PNG




"""
#second itiation of gray to threshold
gray_squ2 = cv2.cvtColor(result1, cv2.COLOR_BGR2GRAY)
gray_squ2 = cv2.fastNlMeansDenoising(gray_squ2,None,10,7,21)
cv2.imshow('gray squ2', gray_squ2)
ret,thresh2 = cv2.threshold(gray_squ2,140,255,cv2.THRESH_BINARY)
cv2.imshow("second itiation of gray to threshold ", thresh2)  #### it did remove some noise but not all  for one_inch.PNG
"""



"""
##from the project.py
hsv_frame = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
low = np.array([0, 42, 0])
high = np.array([179,255,255])
mask = cv2.inRange(hsv_frame, low, high)
#mask = cv2.inRange(gray, low, high)
cv2.imshow("mask",mask)
result2 = cv2.bitwise_and(image_bgr,image_bgr,mask=mask)
cv2.imshow("result2", result2)"""
###########################################################################
#^---------this would filter white background

cv2.waitKey(0) 
cv2.destroyAllWindows() 