import datetime
import os
import json
import numpy as np
import configparser
from PIL import Image
from pycococreatortools import pycococreatortools

#carica da config.ini
config = configparser.ConfigParser()
config.read("config.ini")
COCO_NAME = config["SETTINGS"]["COCO_NAME"]
OUT_NAME = config["SETTINGS"]["OUT_NAME"]
JSON_NAME = config["SETTINGS"]["JSON_NAME"]
DIR_MASK = config["SETTINGS"]["DIR_MASK"]

def getCategories():
    #crea lista di categorie
    catList = []
    catId = 0
    for image in os.listdir(DIR_MASK):
        #print image
        catList.append(
            {
                "supercategory" : "shape",
                "id" : catId,
                "name" : image.split(".")[0]
            }
        )
        catId += 1
    #print catList
    return catList


def genCoco(DIR):
    coco_output ={
        "info": {
            "description": DIR,
            "url": "...",
            "version": "1.0",
            "year": 2019,
            "contributor": "gp",
            "date_created": datetime.datetime.utcnow().isoformat(' ')
        },
        "licenses": [
            {
                "id": 2112,
                "name": "DFV Srl Surano",
                "url": "..."
            }
        ],
        "categories" : [],
        "images": [],
        "annotations": []
    }

    subdirList = []
    subdirList = os.listdir(DIR)

    catList = getCategories()
    coco_output["categories"].append(catList)

    compositeId = 0
    annotationId = 0

    for subDir in subdirList: #per ogni esecuzione
        composite = OUT_NAME.split(".")[0]+"_"+subDir+"."+OUT_NAME.split(".")[1]
        i = Image.open(DIR+subDir+"/"+composite)
        coco_output["images"].append( # aggiunge l'immagine composita 
                pycococreatortools.create_image_info(
                    compositeId,
                    os.path.basename(composite),
                    i.size
                )
            )
        
        #ottiene le immagini singole (composita esclusa)
        imageList = []
        imageList = os.listdir(DIR+subDir)
        imageList.remove(composite)
        imageList.remove(JSON_NAME.split(".")[0]+"_"+subDir+"."+JSON_NAME.split(".")[1])

        for image in imageList:
            img = Image.open(DIR+subDir+"/"+image)

            category_info = { # id categoria dell'immagine singola
                "id": next((cat for cat in catList if cat["name"] == image.split("_")[0]), None)["id"],
                "is_crowd": 0
            }

            binary_mask = np.asarray(img.convert("1")).astype(np.uint8)

            annotation_info = pycococreatortools.create_annotation_info(
                annotationId, compositeId, category_info, binary_mask, img.size, tolerance = 2
            )

            coco_output["annotations"].append(annotation_info)

            annotationId += 1
        
        compositeId += 1

    with open(DIR+COCO_NAME, "w") as out:
        json.dump(coco_output, out)