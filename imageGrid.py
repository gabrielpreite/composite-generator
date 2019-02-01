import cv2
import numpy as np

def genGrid(img, CELLSIZE):
    ROWS = img.shape[0] / CELLSIZE
    COLUMNS = img.shape[1] / CELLSIZE

    grid = np.zeros((ROWS, COLUMNS))

    for i in range(ROWS):
        for j in range(COLUMNS):
            maxval = 0
            for x in range(CELLSIZE):
                for y in range(CELLSIZE):
                    maxval = max(maxval, img[i*CELLSIZE+x][j*CELLSIZE+y])
            if maxval > 0:
                grid[i][j] = 255
            
    #for i in range(ROWS):
        #print grid[i]

    #for i in range(ROWS-1):
        #for j in range(COLUMNS-1):
            #if grid[i][j] == 1:
                #for x in range(-1, 2):
                    #for y in range(-1, 2):
                        #grid[i+x][j+y] = -1 if grid[i+x][j+y] == 0 else grid[i+x][j+y]
    #for i in range(ROWS):
        #print grid[i]
    return grid