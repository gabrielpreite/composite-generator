import numpy as np
import cv2
import sys
import os
import random
import configparser
import shutil
from imageGrid import genGrid
from imageRand import randomize

#python generator.py <nome directory>

#carica da config.ini
config = configparser.ConfigParser()
config.read("config.ini")

CELLSIZE = int(config["SETTINGS"]["CELLSIZE"])
OUT_SIZE = [int(config["SETTINGS"]["OUT_SIZEY"]), int(config["SETTINGS"]["OUT_SIZEX"])]
OUT_NAME = config["SETTINGS"]["OUT_NAME"]
MODE =  int(config["SETTINGS"]["MODE"])
N = int(config["SETTINGS"]["N"])
DIR_MASK = config["SETTINGS"]["DIR_MASK"]
DIR_PROF = config["SETTINGS"]["DIR_PROF"]
DIR_OUT = config["SETTINGS"]["DIR_OUT"]
DISTR = int(config["SETTINGS"]["DISTR"])
THR = int(config["SETTINGS"]["THR"])

FGRID_SIZE = [OUT_SIZE[0] / CELLSIZE, OUT_SIZE[1] / CELLSIZE]
NAME = sys.argv[1]

#cancella la directory di output se esiste gia
if os.path.exists(DIR_OUT+NAME):
    shutil.rmtree(DIR_OUT+NAME)

fullgrid = np.zeros((FGRID_SIZE[0], FGRID_SIZE[1]))
composite = np.zeros((OUT_SIZE[0], OUT_SIZE[1]))

#crea directory di output
if not os.path.exists(DIR_OUT+NAME):
    os.makedirs(DIR_OUT+NAME)

lista = os.listdir(DIR_MASK)
count = {}
for name in lista:
    count[name] = 0

for n in range(N):
    #seleziona un profilo random
    path = lista[random.randint(0, len(lista))-1]

    mask = cv2.cvtColor(cv2.imread(DIR_MASK+path), cv2.COLOR_BGR2GRAY)
    profile = cv2.cvtColor(cv2.imread(DIR_PROF+path), cv2.COLOR_BGR2GRAY)

    mask, profile, grid = randomize(mask, profile, CELLSIZE, MODE, THR)

    IMG_SIZE = [np.size(mask, 0), np.size(mask, 1)]
    GRID_SIZE = [np.size(grid, 0), np.size(grid, 1)]

    x = y = i = j = 0

    if(DISTR == 0): #distribuzione accentrata
        found = False
        turn = 0
        maxturns = 1
        direc = 0
        mask = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        x = FGRID_SIZE[0]/2
        y = FGRID_SIZE[1]/2
        while(x > 0 and x < FGRID_SIZE[0] - GRID_SIZE[0] and y > 0 and y < FGRID_SIZE[1] - GRID_SIZE[1]):
            #print "x: ",x
            #print "y: ",y
            #print ""
            #controlla collisioni
            invalid = False
            for i in range(GRID_SIZE[0]):
                for j in range(GRID_SIZE[1]): #se un bordo si sovrappone ad una figura
                    if grid[i][j] == 255 and fullgrid[x+i][y+j] == 255:
                        invalid = True
                        break
                if invalid:
                    break
            if invalid is False:
                found = True
                break
            if turn == maxturns:
                maxturns += 1
                turn = 0
                direc = (direc+1) % 4

            x += mask[direc][0]
            y += mask[direc][1]
            turn += 1
        
        #raggiunto il limite dell'immagine
        if found == False:
            break

    elif(DISTR == 1): #distribuzione margine inferiore
        valid = True
        y = random.randint(0, FGRID_SIZE[1] - GRID_SIZE[1])
        for x in range(FGRID_SIZE[0] - GRID_SIZE[0]):
            for i in range(GRID_SIZE[0]):
                for j in range(GRID_SIZE[1]): #se un bordo si sovrappone ad una figura
                    if grid[i][j] == 255 and fullgrid[x+i][y+j] == 255: #collisione
                        valid = False
                        break
                if valid is False:
                    break
            if valid is False:
                break
        if valid is False and y == 0: #raggiunto il limite dell'immagine
            break
        y = y if y == FGRID_SIZE[1] - GRID_SIZE[1] -1 else y-1 #ultima posizione valida
    #aggiorna fullgrid
    for i in range(GRID_SIZE[0]):
        for j in range(GRID_SIZE[1]):
            fullgrid[x+i][y+j] = fullgrid[x+i][y+j] if grid[i][j] == 0 else grid[i][j]

    #aggiorna composite
    for i in range(IMG_SIZE[0]):
        for j in range(IMG_SIZE[1]):
            composite[x*CELLSIZE + i][y*CELLSIZE + j] = composite[x*CELLSIZE + i][y*CELLSIZE + j] if profile[i][j] == 0 else profile[i][j]

    #crea immagine con layer singolo
    tmp = np.zeros((OUT_SIZE[0], OUT_SIZE[1]))
    for i in range(IMG_SIZE[0]):
        for j in range(IMG_SIZE[1]):
            tmp[x*CELLSIZE + i][y*CELLSIZE + j] = tmp[x*CELLSIZE + i][y*CELLSIZE + j] if profile[i][j] == 0 else profile[i][j]
    count[path] += 1
    cv2.imwrite(DIR_OUT+NAME+"/"+path.split(".")[0]+"_"+str(count[path]).zfill(6)+".png", tmp)

    print "#",n

#for i in range(FGRID_SIZE[0]):
    #for j in range(FGRID_SIZE[1]):
        #fullgrid[i][j] = 255 if fullgrid[i][j] == 1 else 0
#cv2.imwrite("Output/"+NAME+"/fullgrid.png", fullgrid)

cv2.imwrite(DIR_OUT+NAME+"/"+OUT_NAME, composite)
