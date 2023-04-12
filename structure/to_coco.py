#!/usr/bin/env python3
"""Decode base64 encoded images"""

import json
import os
import glob
import numpy as np
from datetime import date
from PIL import Image
import sys
sys.path.append(os.path.join(sys.path[0], '../processing/'))
from decode import decode, translate_coords

def iterable_list(in_list):
    if isinstance(in_list, list):
        return in_list
    else:
        return [in_list]

output_prefix = "coco"

set_options = ["train", "validation", "test"]  # Only choose one
size_options = ["s", "m", "l"]  # One or all
sighted_options = [0, 1]  # Either or both
occlusion_options = [False, True]  # Either or both
type_options = ["match", "drill"]  # Either or both

set = set_options[0]
size = size_options[1]  # Large == close
sighted = sighted_options[:]
occlusion = occlusion_options[0]
type = type_options[:]

output_dir = (
    "./" + output_prefix 
    + "_" + set 
    + "_" + "".join(size) 
    + "_" + "".join(str(val) for val in iterable_list(sighted))
    + "_" + "".join(str(val) for val in iterable_list(occlusion))
    + "_" + "".join(type)  + "/")

try:
    os.makedirs(output_dir)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./'+ set + "/", "*.json"))

info = {
    "description": "RoboCup Ball detection Dataset: " + set,
    "url": "https://gitlab.com/robocup-sim",
    "version": "1.0",
    "year": str(date.today())[:4],
    "contributor": "M Nagy",
    "date_created": str(date.today())
    }

licenses = [{
    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
    "id": 1,
    "name": "Attribution-NonCommercial-ShareAlike License"
    }]

categories = [{
    "id": 1,
    "name": "Ball",
    "supercategory": "none"
    }]

images = []
img_id = 1
annotations = []
anno_id = 1
SMALL_THRES = 32  # height in pixels
LARGE_THRES = 96 

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)

    if img_dict["ball_sighted"] in iterable_list(sighted):
        pass
    else:
        print("Skipped for sighted")
        continue

    if img_dict["occluded"] in iterable_list(occlusion):
        pass
    else:
        print("Skipped for occlusion")
        continue

    if img_dict["type"] in iterable_list(type):
        pass
    else:
        print("Skipped for type")
        continue

    output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])
    m, n = output_img.shape[:2]

    if img_dict["ball_sighted"] ==1:

        ball_vector = np.asarray(img_dict["ball_locate"])
        m_coord, n_coord, BALL_RAD_implane = translate_coords(output_img, ball_vector)

        bb_coords = [n_coord - BALL_RAD_implane, m_coord - BALL_RAD_implane,  # Top left coords 
                    2*BALL_RAD_implane, 2*BALL_RAD_implane]                   # Width and height

        if size == "s":
            if 2*BALL_RAD_implane <= SMALL_THRES:
                pass
            else:
                print("Skipped for size")
                continue

        elif size == "m":
            if 2*BALL_RAD_implane > SMALL_THRES and 2*BALL_RAD_implane < LARGE_THRES:
                pass
            else:
                print("Skipped for size")
                continue

        elif size == "l":
            if 2*BALL_RAD_implane > LARGE_THRES:
                pass
            else:
                print("Skipped for size")
                continue
        
        else:
            pass

        annotations.append({
            "area": (2*BALL_RAD_implane)**2,
            "iscrowd": 0,
            "bbox": bb_coords,
            "category_id": 1,
            "ignore": 0,
            "segmentation": [],
            "image_id": img_id,
            "id": anno_id
        })
        anno_id = anno_id + 1

    img_name = name[2+len(set):-5] + ".jpeg"
    images.append({
        "file_name": img_name,
        "height": m,
        "width": n,
        "id": img_id
        })
    
    img_id = img_id + 1
   
    # store result
    output = Image.fromarray(output_img)
    output.save(output_dir + img_name)

dataset = {
    "info": info,
    "licenses": licenses,
    "categories": categories,
    "images": images,
    "annotations": annotations
    }

with open("./" + output_dir + "annot.json", 'w') as out_file:
            json.dump(dataset, out_file, indent=4)
