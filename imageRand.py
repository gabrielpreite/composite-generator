import cv2
import random
import numpy as np
import configparser
from imageGrid import genGrid

#carica da config.ini
config = configparser.ConfigParser()
config.read("config.ini")

CELLSIZE = config["SETTINGS"]["CELLSIZE"]
MOD = config["SETTINGS"]["MOD"]
THR = config["sETTINGS"]["THR"]

def randomize(img1, img2):
    #Numero di colonne e righe
    cols = img1.shape[0]
    rows = img1.shape[1]

    degree = 0
    #Rapporto dimensioni
    scale = 1
    
    dst1 = img1
    dst2 = img2

    if(MOD == 0): #rotazione random
        degree = random.randint(0, 360)

        #Genera matrice per la rotazione 2d e ruota le immagini
        M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,scale)
        dst1 = cv2.warpAffine(img1,M,(cols,rows))
        dst2 = cv2.warpAffine(img2,M,(cols,rows))

        dst1, dst2 = cut(dst1, dst2)

    elif(MOD == 1): #rotazione orizzontale
        dst1, dst2 = cut(img1, img2)
        if np.size(dst1, 0) > np.size(dst1, 1):
            degree = random.randint(0, 11)+85
        else:
            degree = random.randint(0, 11)+355
        
        M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,scale)
        dst1 = cv2.warpAffine(img1,M,(cols,rows))
        dst2 = cv2.warpAffine(img2,M,(cols,rows))

        dst1, dst2 = cut(dst1, dst2)

    #Aggiunge ad una lista le matrici e le restituisce
    grid = genGrid(dst1)

    #normalizza dst1, dst2
    for i in range(np.size(dst1, 0)):
        for j in range(np.size(dst1, 1)):
            dst1[i][j] = 255 if dst1[i][j] > THR else 0
            dst2[i][j] = 255 if dst2[i][j] > THR else 0

    mats = [dst1, dst2, grid]
    return mats

def cut(img1, img2):
    cols = img1.shape[0]
    rows = img1.shape[1]

    #taglia zone nere
    startx = starty = endx = endy = 0
    flag = False
    for i in range(cols):
        for j in range(rows):
            if img1[i][j] == 255:
                starty = i
                flag = True
                break
        if flag:
            break
    
    flag = False
    for i in range(cols):
        for j in range(rows):
            if img1[j][i] == 255:
                startx = i
                flag = True
                break
        if flag:
            break

    flag = False
    for i in range(cols-1, -1, -1):
        for j in range(rows-1, -1, -1):
            if img1[i][j] == 255:
                endy = i
                flag = True
                break
        if flag:
            break

    flag = False
    for i in range(cols-1, -1, -1):
        for j in range(rows-1, -1, -1):
            if img1[j][i] == 255:
                endx = i
                flag = True
                break
        if flag:
            break

    endx += CELLSIZE - (endx%CELLSIZE)
    endy += CELLSIZE - (endy%CELLSIZE)

    res1 = img1[starty:endy, startx:endx]
    res2 = img2[starty:endy, startx:endx]

    return res1, res2