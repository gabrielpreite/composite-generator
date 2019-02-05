import numpy as np
import cv2
import sys
import os
import json
import random
import configparser
import shutil
from imageRand import randomize
from coco import genCoco

#python generator.py <nome directory> <numero immagini>

#carica da config.ini
config = configparser.ConfigParser()
config.read("config.ini")

CELLSIZE = int(config["SETTINGS"]["CELLSIZE"])
OUT_SIZE = [int(config["SETTINGS"]["OUT_SIZEY"]), int(config["SETTINGS"]["OUT_SIZEX"])]
OUT_NAME = config["SETTINGS"]["OUT_NAME"]
MOD = int(config["SETTINGS"]["MOD"])
N = int(config["SETTINGS"]["N"])
DIR_MASK = config["SETTINGS"]["DIR_MASK"]
DIR_PROF = config["SETTINGS"]["DIR_PROF"]
DIR_OUT = config["SETTINGS"]["DIR_OUT"]
DISTR = int(config["SETTINGS"]["DISTR"])
THR = int(config["SETTINGS"]["THR"])
JSON_NAME = config["SETTINGS"]["JSON_NAME"]
COCO_NAME = config["SETTINGS"]["COCO_NAME"]

FGRID_SIZE = [OUT_SIZE[0] / CELLSIZE, OUT_SIZE[1] / CELLSIZE]
NAME = sys.argv[1]
NUMBER = int(sys.argv[2])

#cancella la directory di output se esiste gia
if os.path.exists(DIR_OUT+NAME):
    shutil.rmtree(DIR_OUT+NAME)

#crea directory di output
if not os.path.exists(DIR_OUT+NAME):
    os.makedirs(DIR_OUT+NAME)

for image_num in range(NUMBER):

    #grid per il controllo delle collisioni
    fullgrid = np.zeros((FGRID_SIZE[0], FGRID_SIZE[1]))
    #immagine finale
    composite = np.zeros((OUT_SIZE[0], OUT_SIZE[1]))

    #crea directory di output per l'immagine corrente
    if not os.path.exists(DIR_OUT+NAME+"/"+str(image_num).zfill(6)):
        os.makedirs(DIR_OUT+NAME+"/"+str(image_num).zfill(6))

    jsonList = []

    #legge i profili/mask in input
    lista = os.listdir(DIR_MASK)
    count = {}
    for name in lista:
        count[name] = 0

    for n in range(N):
        #seleziona un profilo random
        path = lista[random.randint(0, len(lista)-1)]

        mask = cv2.cvtColor(cv2.imread(DIR_MASK+path), cv2.COLOR_BGR2GRAY)
        profile = cv2.cvtColor(cv2.imread(DIR_PROF+path), cv2.COLOR_BGR2GRAY)
        mask, profile, grid = randomize(mask, profile)

        IMG_SIZE = [np.size(mask, 0), np.size(mask, 1)]
        GRID_SIZE = [np.size(grid, 0), np.size(grid, 1)]

        x = y = i = j = 0

        if(DISTR == 0): #distribuzione centrata
            found = False
            turn = 0
            maxturns = 1
            direc = 0
            #movimento a spirale partendo dal centro
            mask = [[-1, 0], [0, 1], [1, 0], [0, -1]]
            x = FGRID_SIZE[0]/2
            y = FGRID_SIZE[1]/2
            while(x > 0 and x < FGRID_SIZE[0] - GRID_SIZE[0] and y > 0 and y < FGRID_SIZE[1] - GRID_SIZE[1]):
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
            #y = random.randint(0, FGRID_SIZE[1] - GRID_SIZE[1])
            for x in range(FGRID_SIZE[0] - GRID_SIZE[0]-1, 0, -1):
                #print "check y:", y
                for y in range(FGRID_SIZE[1] - GRID_SIZE[1]):
                    #print "check x: ", x
                    valid = True
                    for i in range(GRID_SIZE[0]):
                        for j in range(GRID_SIZE[1]): #se un bordo si sovrappone ad una figura
                            if grid[i][j] == 255 and fullgrid[x+i][y+j] == 255: #collisione
                                valid = False
                                break
                        if valid is False:
                            break
                    if valid:
                        break
                if valid:
                    break
            if valid is False: #raggiunto il limite dell'immagine
                break
            #y = y if y == FGRID_SIZE[1] - GRID_SIZE[1] -1 else y-1 #ultima posizione valida

        #aggiorna json
        jsonList.append({"category" : path.split(".")[0],
                        "confidence" : str(1.0),
                        "bbox" : [str(float(y)*CELLSIZE), str(float(x)*CELLSIZE), str(float(IMG_SIZE[1])), str(float(IMG_SIZE[0]))]})

        #aggiorna fullgrid
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                fullgrid[x+i][y+j] = fullgrid[x+i][y+j] if grid[i][j] == 0 else grid[i][j]

        #aggiorna composite
        for i in range(IMG_SIZE[0]):
            for j in range(IMG_SIZE[1]):
                composite[x*CELLSIZE + i][y*CELLSIZE + j] = composite[x*CELLSIZE + i][y*CELLSIZE + j] if profile[i][j] == 0 else profile[i][j]

        #crea immagine con layer singolo e la salva
        tmp = np.zeros((OUT_SIZE[0], OUT_SIZE[1]))
        for i in range(IMG_SIZE[0]):
            for j in range(IMG_SIZE[1]):
                tmp[x*CELLSIZE + i][y*CELLSIZE + j] = tmp[x*CELLSIZE + i][y*CELLSIZE + j] if mask[i][j] == 0 else mask[i][j]
        count[path] += 1
        cv2.imwrite(DIR_OUT+NAME+"/"+str(image_num).zfill(6)+"/"+path.split(".")[0]+"_"+str(count[path]).zfill(6)+".png", tmp)

        print "#",n

    # (debug)
    #for i in range(FGRID_SIZE[0]):
        #for j in range(FGRID_SIZE[1]):
            #fullgrid[i][j] = 255 if fullgrid[i][j] == 1 else 0
    #cv2.imwrite("Output/"+NAME+"/fullgrid.png", fullgrid)
    
    cv2.imwrite(DIR_OUT+NAME+"/"+str(image_num).zfill(6)+"/"+OUT_NAME.split(".")[0]+"_"+str(image_num).zfill(6)+"."+OUT_NAME.split(".")[1], composite)

    # dump del json
    with open(DIR_OUT+NAME+"/"+str(image_num).zfill(6)+"/"+JSON_NAME.split(".")[0]+"_"+str(image_num).zfill(6)+"."+JSON_NAME.split(".")[1], "w") as out:
        json.dump(jsonList, out)

genCoco(DIR_OUT+NAME+"/")
