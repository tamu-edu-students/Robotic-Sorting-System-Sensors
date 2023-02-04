import cv2
import numpy as np

img= cv2.imread('lemontest.jpg')
print(img.shape)
cv2.imshow("orighinal", img)

#cropping an image
cropped_img = img[225:500,335:550]

#display cropped img
cv2.imshow("cropped", cropped_img)

# Save the cropped image
cv2.imwrite("Cropped_Image.jpg", cropped_img)

#may need to scale the image as camera height increase

up_points = 2*cropped_img.shape[1],2*cropped_img.shape[0]

resized_up = cv2.resize(cropped_img, up_points, interpolation= cv2.INTER_LINEAR)
cv2.imshow("cropped+resize", resized_up)

# Save the resize image
cv2.imwrite("Cropped_Image.jpg", resized_up)


cv2.waitKey(0)
cv2.destroyAllWindows()