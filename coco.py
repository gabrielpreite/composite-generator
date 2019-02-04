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

def getCategories(imageList):
    catList = []
    found = {}
    id = 0
    for image in imageList:
        #print image
        if image.split("_")[0] not in found:
            catList.append(
                {
                    "supercategory" : "shape",
                    "id" : id,
                    "name" : image.split("_")[0]
                }
            )
            id += 1
            found[image.split("_")[0]] = True
    #print catList
    return catList


def genCoco(DIR, COCO_NAME, OUT_NAME, JSON_NAME):
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

    imageList = []
    imageList = os.listdir(DIR)

    imageList.remove(OUT_NAME)
    imageList.remove(JSON_NAME)

    catList = getCategories(imageList)
    #print catList
    coco_output["categories"].append(catList)

    #print imageList
    imageId = 0
    annotationId = 0
    for image in imageList:
        img = Image.open(DIR+image)

        coco_output["images"].append( #images
            pycococreatortools.create_image_info(
                imageId,
                os.path.basename(image),
                img.size
            )
        )

        category_info = {
            "id": next((cat for cat in catList if cat["name"] == image.split("_")[0]), None)["id"],
            "is_crowd": 0
        }

        binary_mask = np.asarray(img.convert("1")).astype(np.uint8)

        annotation_info = pycococreatortools.create_annotation_info(
            annotationId, imageId, category_info, binary_mask, img.size, tolerance = 2
        )

        coco_output["annotations"].append(annotation_info)

        imageId += 1
        annotationId += 1

    with open(DIR+COCO_NAME, "w") as out:
        json.dump(coco_output, out)