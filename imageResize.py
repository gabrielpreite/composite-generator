import cv2
import numpy as np
import os

src1 = "Original/Mask/"
dst1 = "Resized/Mask/"
list1 = os.listdir(src1)

for elem in list1:
    img = cv2.cvtColor(cv2.imread(src1+elem), cv2.COLOR_BGR2GRAY)
    result = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    for i in range(np.size(result, 0)):
        for j in range(np.size(result, 1)):
            result[i][j] = 0 if result[i][j] == 0 else 255
    cv2.imwrite(dst1+elem, result)

src2 = "Original/Profile/"
dst2 = "Resized/Profile/"
list2 = os.listdir(src2)

for elem in list2:
    img = cv2.cvtColor(cv2.imread(src2+elem), cv2.COLOR_BGR2GRAY)
    result = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    for i in range(np.size(result, 0)):
        for j in range(np.size(result, 1)):
            result[i][j] = 0 if result[i][j] == 0 else 255
    cv2.imwrite(dst2+elem, result)
