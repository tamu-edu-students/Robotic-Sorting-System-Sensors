import numpy as np
import cv2 

#settup webcam
cap = cv2.VideoCapture(0)


#while loop create a live video from webcam
while(True):
    ret, frame = cap.read()
    cv2.imshow("Frame",frame)
    frame= cv2.resize(frame, (0,0), fx=0.5,fy=0.5)

    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break                            #press 'q' on the keyboard to exit the video

cap.release()
cv2.destroyAllWindows()