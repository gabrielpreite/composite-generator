import cv2
import random
import numpy as np
from imageGrid import genGrid

def randomize(img1, img2, CELLSIZE, MODE, THR):
    #Numero di colonne e righe
    cols = img1.shape[0]
    rows = img1.shape[1]

    degree = 0
    #Rapporto dimensioni
    scale = 1
    
    dst1 = img1
    dst2 = img2

    if(MODE == 0): #rotazione random
        degree = random.randint(0, 360)

        #Genera matrice per la rotazione 2d e ruota le immagini
        M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,scale)
        dst1 = cv2.warpAffine(img1,M,(cols,rows))
        dst2 = cv2.warpAffine(img2,M,(cols,rows))

        dst1, dst2 = cut(dst1, dst2, CELLSIZE)

    elif(MODE == 1): #rotazione orizzontale
        dst1, dst2 = cut(img1, img2, CELLSIZE)
        if np.size(dst1, 0) > np.size(dst1, 1):
            degree = random.randint(0, 11)+85
        else:
            degree = random.randint(0, 11)+355
        
        M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,scale)
        dst1 = cv2.warpAffine(img1,M,(cols,rows))
        dst2 = cv2.warpAffine(img2,M,(cols,rows))

        dst1, dst2 = cut(dst1, dst2, CELLSIZE)

    #Genera un valore casuale multiplo di 10 per ridimensionare le immagini
    #size = random.randint(-10,10) * 10
    #dst1 = cv2.resize(dst1,((cols+size),(rows+size)))
    #dst2 = cv2.resize(dst2,((cols+size),(rows+size)))

    #Aggiunge ad una lista le matrici e le restituisce
    grid = genGrid(dst1, CELLSIZE)

    #normalizza dst1, dst2
    for i in range(np.size(dst1, 0)):
        for j in range(np.size(dst1, 1)):
            dst1[i][j] = 255 if dst1[i][j] > THR else 0
            dst2[i][j] = 255 if dst2[i][j] > THR else 0

    mats = [dst1, dst2, grid]
    return mats

def cut(img1, img2, CELLSIZE):
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
            #img1[i][j] = 50
        if flag:
            break
    
    flag = False
    for i in range(cols):
        for j in range(rows):
            if img1[j][i] == 255:
                startx = i
                flag = True
                break
            #img1[j][i] = 100
        if flag:
            break

    flag = False
    for i in range(cols-1, -1, -1):
        for j in range(rows-1, -1, -1):
            if img1[i][j] == 255:
                endy = i
                flag = True
                break
            #img1[i][j] = 150
        if flag:
            break

    flag = False
    for i in range(cols-1, -1, -1):
        for j in range(rows-1, -1, -1):
            if img1[j][i] == 255:
                endx = i
                flag = True
                break
            #img1[j][i] = 200
        if flag:
            break

    endx += CELLSIZE - (endx%CELLSIZE)
    endy += CELLSIZE - (endy%CELLSIZE)

    res1 = img1[starty:endy, startx:endx]
    res2 = img2[starty:endy, startx:endx]

    """print "startx: ",startx
    print "starty: ",starty
    print "endx: ",endx
    print "endy: ",endy
    cv2.imshow("res", res2)
    cv2.imshow("img", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

    return res1, res2

#Inizio test funzionamento
#img1 = cv2.imread("9615a.png",cv2.IMREAD_COLOR)
#img2 = cv2.imread("9615b.png",cv2.IMREAD_COLOR)

#lista = generate_mat(img1,img2)
#dst1 = cv2.imwrite("9615a_rotate.png",lista[0])
#dst2 = cv2.imwrite("9615b_rotate.png",lista[1])
#Fine del test

#test ang40x20
#img1 = cv2.imread("Resized/Mask/ANG40x20.png", cv2.IMREAD_COLOR)
#img2 = img1
#img1, img2 = randomize(img1, img2)
#cv2.imshow("img", img1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()