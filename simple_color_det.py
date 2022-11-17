import numpy as np
import cv2 

#I am still going to have to make some improvement, but here is the simple color detection using HSV format
#I might have better result if I clean my webcam

#settup webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


#while loop create a live video from webcam
while(True):
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)     #convert BGR to HSV format
    height, width, ret = frame.shape

    cx = int(width/2)
    cy = int(height/2)
    
    #pick pixel value
    #pixel_center = frame[cy, cx]    #pixel_center is in bgr format

    pixel_center = hsv_frame[cy, cx]    #in hsv format 
    hue_value = pixel_center[0]         

    color = "undefine"
    if hue_value < 5:
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 78:
        color = "GREEN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 167:
        color = "VIOLET"
    else:
        color = "RED"

    print(pixel_center)                   #print out the value of the center pixel
    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
    cv2.putText(frame, color, (10, 50), 0, 1, (b,g,r), 2)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)     #point out the center pixel

    cv2.imshow("Frame",frame)
    frame= cv2.resize(frame, (0,0), fx=0.5,fy=0.5)

    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):       #press 'q' on the keyboard to exit the video
        break


cap.release()
cv2.destroyAllWindows()
