import unicodedata
import datetime
import cv2
import os
import fnmatch
import glob
from natsort import natsorted
import re
from PIL import Image
import json
import numpy as np
from pycococreatortools import pycococreatortools

def getCategories(DIR_MASK):
    catList = []
    id = 0
    for image in os.listdir(DIR_MASK):
        #print image
        catList.append(
            {
                "supercategory" : "shape",
                "id" : id,
                "name" : image.split(".")[0]
            }
        )
        id += 1
    #print catList
    return catList


def genCoco(DIR, COCO_NAME, OUT_NAME, JSON_NAME, DIR_MASK):
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

    catList = getCategories(DIR_MASK)
    coco_output["categories"].append(catList)

    compositeId = 0
    annotationId = 0

    for subDir in subdirList:
        imageList = []
        imageList = os.listdir(DIR+subDir)

        composite = OUT_NAME.split(".")[0]+"_"+subDir+"."+OUT_NAME.split(".")[1]
        i = Image.open(DIR+subDir+"/"+composite)
        coco_output["images"].append( #adds composite
                pycococreatortools.create_image_info(
                    compositeId,
                    os.path.basename(composite),
                    i.size
                )
            )

        imageList.remove(composite)
        imageList.remove(JSON_NAME.split(".")[0]+"_"+subDir+"."+JSON_NAME.split(".")[1])

        #print imageList
        for image in imageList:
            img = Image.open(DIR+subDir+"/"+image)

            category_info = {
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