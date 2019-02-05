import numpy as np
import configparser

#carica da config.ini
config = configparser.ConfigParser()
config.read("config.ini")

CELLSIZE = config["SETTINGS"]["CELLSIZE"]

def genGrid(img):
    ROWS = img.shape[0] / CELLSIZE
    COLUMNS = img.shape[1] / CELLSIZE

    grid = np.zeros((ROWS, COLUMNS))
    # genera una grid (w/CELLSIZE, h/CELLSIZE)
    for i in range(ROWS):
        for j in range(COLUMNS):
            maxval = 0
            for x in range(CELLSIZE):
                for y in range(CELLSIZE):
                    maxval = max(maxval, img[i*CELLSIZE+x][j*CELLSIZE+y])
            if maxval > 0:
                grid[i][j] = 255
    return grid