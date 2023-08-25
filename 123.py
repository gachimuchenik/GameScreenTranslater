import cv2
import numpy as np

sharpening_kernel = np.array([
    [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1]
], dtype=np.float32)

image = cv2.imread('cut.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_white = np.array([230, 230, 230])
upper_white = np.array([255, 255, 255])
mask = cv2.inRange(image, lower_white, upper_white)
result = cv2.bitwise_and(image, image, mask=mask)
result[np.where((result == [0, 0, 0]).all(axis=2))] = [0, 0, 0]
result = cv2.bitwise_not(result)
result = cv2.medianBlur(result, 3)
result = cv2.filter2D(result, -1, sharpening_kernel)
cv2.imwrite('test.png', result)


# cut = cv2.imread('cut.png')
# gray = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
# _, cut = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# cut = cv2.medianBlur(cut, 3)
# cut = cv2.filter2D(cut, -1, sharpening_kernel)
# cv2.imwrite('test.png', cut)
