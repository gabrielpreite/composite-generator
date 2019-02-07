import cv2
import numpy as np
import os

lista = os.listdir("Profile/")

"""for elem in lista:
    print elem
    img = cv2.cvtColor(cv2.imread("Profile/"+elem), cv2.COLOR_BGR2GRAY)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = 255 if img[i][j] > 200 else 0
    cv2.imwrite("Profile/"+elem, img)"""

for elem in lista:
    if elem == "SL1102.png":
        print elem
        img = cv2.cvtColor(cv2.imread("Profile/"+elem), cv2.COLOR_BGR2GRAY)

        # Copy the thresholded image.
        im_floodfill = img.copy()
        
        # Mask used to flood filling.
        # Notice the size needs to be 2 pixels than the image.
        h, w = img.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        
        # Floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0,0), 127);

        flood2 = cv2.bitwise_not(im_floodfill)

        """cv2.imshow("1", img)
        cv2.imshow("2", flood2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                img[i][j] = 255 if img[i][j] == 255 or flood2[i][j] == 255 else 0
        cv2.imwrite("Mask/"+elem, img)