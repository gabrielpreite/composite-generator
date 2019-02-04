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


def ListDir(Path, OUT_NAME):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(Path) if f.endswith(".png") and f != OUT_NAME]
    return onlyfiles

def CreateCategories(FromDir, OUT_NAME):
    CATEGORIES=[]
    profiles=dict()
    profile_list = ListDir(FromDir, OUT_NAME)
    profile_list.sort()
    for i in range(0, len(profile_list)): 
        prefix, suffix = profile_list[i].split('.') 
        category_info = {'id': i, 'name': prefix,  'supercategory': 'shape'}
        CATEGORIES.append(category_info)
        profiles[prefix] = i
    #print profiles
    return CATEGORIES, profiles


#from numpy import np

def get_red_to_binary(image_name):
    imcol = cv2.imread(image_name)
    R = imcol.copy()
    R[:, :, 0] = R[:,:,2]
    R[:, :, 1] = R[:,:,2]
    # Set threshold and maxValue
    thresh = 200
    maxValue = 255 
    # Basic threshold example
    th, dst = cv2.threshold(R[:,:,2], thresh, maxValue, cv2.THRESH_BINARY);
    binary=np.asarray(dst)
    cv2.imshow('image',dst)
  
    cv2.waitKey(0)
    
   # bw = Image.fromarray(R,'L')
    #bw = gray.point(lambda x: 0 if x < 200 else 255, '1')
    #cv2.imwrite("./"+folderNew+"/"+image_name, dst)
    #print "Write"+"./" + folderNew + "/" + image_name
    return binary



def filter_for_png(root, files):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    #print files
    files = [f for f in files if re.match(file_types, f)]

    return files

def filter_for_png(root, files):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]

    return files

def filter_for_annotations(root, files, image_filename):
    file_types = ['*.png']
    #print image_filename
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension + '.*'
    #print file_name_prefix
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]

    return files

"""def FindAnnotationFiles(folderOld):
    for root, _, files in os.walk(folderOld):
        image_files = filter_for_png(root, files)
    return image_files"""

#def profiles2Coco(CatDir, WorkingDir):
def profiles2Coco(WorkingDir, OUT_NAME):
    IMAGE_DIR = WorkingDir
    #print IMAGE_DIR
    ANNOTATION_DIR = WorkingDir
    #print ANNOTATION_DIR
    CATEGORIES, profiles=CreateCategories(WorkingDir, OUT_NAME)
    INFO = {
        "description": WorkingDir,
        "url": "...",
        "version": "1.0",
        "year": 2018,
        "contributor": "Pier",
        "date_created": datetime.datetime.utcnow().isoformat(' ')
     }

    LICENSES = [
    {
        "id": 2112,
        "name": "DFV Srl Surano",
        "url": "..."
    }
    ]


    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories":CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    segmentation_id = 1
    i = 1

    # filter for jpeg images
    for root, _, files in os.walk(IMAGE_DIR):
        files.remove("composite.png")
        image_files = filter_for_png(root, files)
        #print "x"
        print "image_files: ", image_files
        # go through each image
        for image_filename in image_files:
            image = Image.open(image_filename)
            image_info = pycococreatortools.create_image_info(
                image_id, os.path.basename(image_filename), image.size)
            coco_output["images"].append(image_info)
            #print "y"
            # filter for associated png annotations
            for root, _, files in os.walk(ANNOTATION_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:
                    #prefix = annotation_filename.split('.')
                    #name, seq = prefix.split('_')
                    fileNameAnnotated=os.path.splitext(os.path.basename(annotation_filename))[0]
                    filen, name, seq = fileNameAnnotated.split('_') 
                    class_id=profiles[name]
                    #print(str(i) + " " + name)
                    
                    

                    category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                    # binary_mask=get_red_to_binary(annotation_filename) 
                    binary_mask = np.asarray(Image.open(annotation_filename)
                                                .convert('1')).astype(np.uint8)

                    annotation_info = pycococreatortools.create_annotation_info(
                        segmentation_id, image_id, category_info, binary_mask,
                        image.size, tolerance=2)

                    if annotation_info is None:
                        print "asd"
                    print "annotation: \n", annotation_info

                    if annotation_info is not None:
                        coco_output["annotations"].append(annotation_info)

                    segmentation_id = segmentation_id + 1

            image_id = image_id + 1
            i += 1

    with open(WorkingDir+"dataset.json", "w") as output_json_file:
        json.dump(coco_output, output_json_file)

    #print coco_output

"""def profiles2CocoRealData(CatDir, WorkingDir):
    IMAGE_DIR=WorkingDir+"/train/dataset_train/" 
    print IMAGE_DIR
    ANNOTATION_DIR=WorkingDir+"/train/annotations_train/" 
    print ANNOTATION_DIR
    CATEGORIES, profiles=CreateCategories(CatDir, )
    INFO = {
        "description": WorkingDir,
        "url": "...",
        "version": "1.0",
        "year": 2018,
        "contributor": "Pier",
        "date_created": datetime.datetime.utcnow().isoformat(' ')
     }

    LICENSES = [
    {
        "id": 2112,
        "name": "DFV Srl Surano",
        "url": "..."
    }
    ]


    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories":CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    segmentation_id = 1
    i = 1

    # filter for jpeg images
    for root, _, files in os.walk(IMAGE_DIR):
        image_files = filter_for_jpeg(root, files)

        # go through each image
        for image_filename in image_files:
            image = Image.open(image_filename)
            image_info = pycococreatortools.create_image_info(
                image_id, os.path.basename(image_filename), image.size)
            coco_output["images"].append(image_info)

            # filter for associated png annotations
            for root, _, files in os.walk(ANNOTATION_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:
                    #prefix = annotation_filename.split('.')
                    #name, seq = prefix.split('_')
                    fileNameAnnotated=os.path.splitext(os.path.basename(annotation_filename))[0]
                    filen, name, seq = fileNameAnnotated.split('_') 
                    class_id=profiles[name]
                    print(str(i) + " " + name)
                   
                 

                    category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                    binary_mask=get_red_to_binary(annotation_filename) 
                   # binary_mask = np.asarray(Image.open(annotation_filename)
                   #                          .convert('1')).astype(np.uint8)

                    annotation_info = pycococreatortools.create_annotation_info(
                        segmentation_id, image_id, category_info, binary_mask,
                        image.size, tolerance=2)

                    if annotation_info is not None:
                        coco_output["annotations"].append(annotation_info)

                    segmentation_id = segmentation_id + 1

            image_id = image_id + 1
            i += 1

    with open('{}/dataset_train.json'.format(WorkingDir), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)

    print coco_output"""



def main():
    pass
    #Categories for COCOSTYLE
    #WorkingDir="./repository/large/55/800/Group_0" 
    #print WorkingDir
    #CATEGORIES, profiles=CreateCategories(WorkingDir)
    #print CATEGORIES
    #print profiles
    #cv2.waitKey(0)
    #profiles2Coco(WorkingDir)
    

if __name__ == "__main__":
    main()




