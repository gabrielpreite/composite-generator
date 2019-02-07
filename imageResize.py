import cv2
import numpy as np
import os
import configparser

# carica da config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# processa mask
src1 = config["SETTINGS"]["DIR_OMASK"]
dst1 = config["SETTINGS"]["DIR_MASK"]
list1 = os.listdir(src1)
if ".directory" in list1:
    list1.remove(".directory")

for elem in list1:
    print "mask - ",elem
    img = cv2.cvtColor(cv2.imread(src1+elem), cv2.COLOR_BGR2GRAY)
    result = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    for i in range(np.size(result, 0)):
        for j in range(np.size(result, 1)):
            result[i][j] = 0 if result[i][j] == 0 else 255
    cv2.imwrite(dst1+elem, result)

src2 = config["SETTINGS"]["DIR_OPROF"]
dst2 = config["SETTINGS"]["DIR_PROF"]
list2 = os.listdir(src2)
if ".directory" in list2:
    list2.remove(".directory")

# processa profili

for elem in list2:
    print "prof - ",elem
    img = cv2.cvtColor(cv2.imread(src2+elem), cv2.COLOR_BGR2GRAY)
    result = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    for i in range(np.size(result, 0)):
        for j in range(np.size(result, 1)):
            result[i][j] = 0 if result[i][j] == 0 else 255
    cv2.imwrite(dst2+elem, result)

if os.path.exists("Resized/Mask/.directory"):
    os.remove("Resized/Mask/.directory")
if os.path.exists("Resized/Profile/.directory"):
    os.remove("Resized/Profile/.directory")
