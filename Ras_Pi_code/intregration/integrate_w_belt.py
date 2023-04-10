import cv2
import numpy as np
import math



#this py file will sense color and size of the fruit with integrating with the conveyor

#determining if the pixel belong to the object or the black conveyor belt background
image_bgr = cv2.imread('Cropped_spottedlemon.jpg')
cv2.imshow("first", image_bgr)

####once you intergate with the converyor belt, you should try to intergate the camera code into this file

gray_squ = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
gray_squ = cv2.fastNlMeansDenoising(gray_squ,None,10,7,21)
ret,thresh1 = cv2.threshold(gray_squ,140,255,cv2.THRESH_BINARY)  ##may need to adjust this
kernel = np.ones((5,5),np.uint8)
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
cv2.imshow("Binary", thresh1)

####if there is bright, shiny spot on the conveyor belt, use this row of codes

result1 = cv2.bitwise_and(image_bgr, image_bgr, mask=thresh1)
hsv_frame = cv2.cvtColor(result1, cv2.COLOR_BGR2HSV)
low = np.array([0, 72, 0])
high = np.array([179, 255, 255])
mask = cv2.inRange(hsv_frame, low, high)
result1 = cv2.bitwise_and(image_bgr, image_bgr, mask=mask)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(150,150))
closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
result1 = cv2.bitwise_and(image_bgr, image_bgr, mask=closing)
#cv2.imshow("does it works", result1)
thresh1 = cv2.bitwise_and(thresh1, thresh1, mask=closing)
cv2.imshow("shiny", thresh1)
####if weird value uncoment some of this code to diagones the error/problem
#result1 = cv2.bitwise_and(image_bgr,image_bgr,mask=thresh1)  ##the object with the converyor belt background


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


pix_p_inch = 74.39758060582346                     ###### NOTE: change this when you find the acutual pixel per inch
#pix_p_inch = 42.81354925721529 


#find the size of the object
height_p = (bottom - top)
print("height by pixels: ", height_p)
width_p = (right - left)
print("width by pixels: ", width_p)
height = (bottom - top)/pix_p_inch
print("height by inch: ", height)
width = (right - left)/pix_p_inch
print("width by inch: ", width)



#####Note, the finished product may not need show images

###################################error message implemention
######
error_message = "check for noise(dust, uneven lighting), the position of the fruit are not on the edge of the frame, there is only one fruit current within the frame"
sensor_error = False
contours,hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
num_obj = len(contours)                          ###<------determines the number of fruits on the frame
print("number of stuff on the belt is:", num_obj)
##check if the fruit is on the left edge or top edge
if top < 1 or bottom < 1 or left < 1 or right < 1:
    sensor_error = True
    print("the sensor error is", sensor_error)
    print("The object need to be on the center of the frame")
    print(error_message)
##check if the fruit is on the right edge or bottom edge
elif top > r-3 or bottom > r-3 or left > c-3 or right > c-3:
    sensor_error = True
    print("the senosor error is", sensor_error)
    print("The object need to be on the center of the frame")
    print(error_message)
###check if the mulitple fruits or noise present, rememember this system is for lemon, lime, apples, but not big fruit, so if the width or height is more than
elif width > 4 or height > 4:  ## 4 inches, there is probalby some weird stuff on the frame, this may applies to the color/ ml
    sensor_error = True
    print(error_message)
elif num_obj == 0:
    sensor_error = True
    print("seem like there is no object on the frame")
elif num_obj > 1:
    sensor_error = True
    print(error_message)
else:
    print("seem like there is no error")
################################is there a var to update if there is a sensor error

######intergate with the json file"""

import json
with open("/home/lifeofpi/BLEProject/subsystem_connection.json", "r") as f:      # read the json file
    variables = json.load(f)

##ctypes
sort_num = variables["ctype"]
fruit_reading = variables["fruit"]
#print(sort_num)

largest = height_p

if height_p < width_p:
    largest = width_p

if sensor_error == True:
    print("settting fruit to -1 because of error")
    fruit_reading = 255
elif sort_num == 1 and sensor_error == False:
    print("sort by color")
    fruit_reading = col_median
elif sort_num == 2 and sensor_error == False:
    print("sort by size")
    fruit_reading = largest
else:
    print("machine learning!?")
    
variables["fruit"] = fruit_reading
with open("/home/lifeofpi/BLEProject/subsystem_connection.json", "w") as f:      # write back to the json file
    json.dump(variables, f)
    
#############################

cv2.waitKey(0) 
cv2.destroyAllWindows() 
