from picamera2 import Picamera2, Preview
import cv2
import time
picam2 = Picamera2()
#picam2.start_and_capture_file("test.jpg")
#img = cv2.imread("/home/lifeofpi/ECEN_403/test.jpg")
preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
#cv2.imshow("test.jpg", img)
##large resoultion
picam2.configure(preview_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(6)
metadata = picam2.capture_file("lemontest.jpg")
#print(metadata)
img = cv2.imread("/home/lifeofpi/ECEN_403/lemontest.jpg")
cv2.imshow("lemontest.jpg", img)
#cv2.waitKey(0) <------this will mess up the program
#cv2.destroyAllWindows()
print("1")
picam2.close()
print("2")
#img = cv2.imread("/home/lifeofpi/ECEN_403/lemon.jpg")
#cv2.imshow("lemon.jpg", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()