import json
import argparse
import unicodedata
import cv2
import numpy as np

if __name__=='__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument('--json_file', required=True, help="Path to the JSON dataset file to visualize")
    args = ap.parse_args()
    
    #cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
    
    with open(args.json_file, 'r') as f:    
        obj = json.loads(f.read())
    
    images, annotations = obj["images"], obj["annotations"]
    classes = obj["categories"][0]
    #print "class ",len(classes)
    #print "img ",len(images)
    #print "anno ",len(annotations)
    #print classes
    for img in images:
        anns = [ann for ann in annotations if ann["image_id"]==img["id"]]
        image_cv2 = cv2.imread(img["file_name"])
        
        #print img
        #print ann
        #print ann['bbox']
               
       
        for ann in anns:
            s = [int(x) for x in ann['bbox']]
            print s
           
            # pts = [pnt for pnt in ann['segmentation']]
            for pnt in ann['segmentation']:
                a = np.array(pnt, np.int32)
                at = a.reshape((-1,1,2))
                #print at
                cv2.polylines(image_cv2,at,False,(255,0,255),4)
          
            cv2.rectangle(image_cv2, (s[0], s[1]), (s[0]+s[2], s[1]+s[3]), (0,255,255), 8)
            #cv2.imshow('hey', image_cv2)
            #cv2.waitKey()
            ProfileClass = classes[ann['category_id']]
            # ProfileClass = classes[ann['category_id']]
            print ProfileClass['name']
            #ProfileClass = unicodedata.normalize('NFKD',Profile).encode('ascii','ignore')
            cv2.putText(image_cv2, ProfileClass['name'], (s[0], s[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            #cv2.putText(image_cv2, ProfileClass['name'], (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 5)

        cv2.imshow('frame', image_cv2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
