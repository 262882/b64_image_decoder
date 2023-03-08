#!/usr/bin/env python3
"""Decode base64 encoded images"""

import json
import os
import glob
import numpy as np
from datetime import date
from decode import decode
from PIL import Image

output_prefix = "coco"

set_options = ["train", "validation", "test"]
range_options = ["all", "near", "far"]
type_options = [["game", "drill"], "game", "drill"]
occlusion_options = [["exclude", "include"], "exclude", "include"]
set = set_options[0]
range = range_options[1]
type = type_options[0]
occlusion = occlusion_options[1]

output_dir = "./" + output_prefix+ "_" + set + "_" + range + "_" + type + "_" + occlusion + "/"
try:
    os.makedirs(output_dir)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./'+ set + "/", "*.json"))
print(img_list)

info = {
    "description": "RoboCup Ball detection Dataset: " + type,
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
    "id": 0,
    "name": "Ball",
    "supercategory": "none"
    }]

images = []
img_id = 1
annotations = []
anno_id = 1


for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)

    if img_dict["occluded"] in occlusion:
        continue
    else:
        pass

    if img_dict["type"] in type:
        continue
    else:
        pass

    output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])

    if img_dict["ball_sighted"]==1:

        ball_vector = np.asarray(img_dict["ball_locate"])

        NEAR_THRES = 16  # height in pixels
        BALL_RAD = 0.042
        FOV = 58
        r_ball = ball_vector[0]
        theta_ball = ball_vector[1]
        phi_ball = ball_vector[2]
        m, n = output_img.shape[:2]

        # Image plane properties
        resolution = max(m,n)
        w_implane = r_ball*np.tan(np.deg2rad(FOV//2))*2
        BALL_RAD_implane = int((BALL_RAD/w_implane*resolution))

        # Localization
        m_delta_implane = phi_ball/(FOV/2)
        n_delta_implane = theta_ball/(FOV/2)
        m_coord = -int(m_delta_implane*(resolution/2))+(m//2)
        n_coord = -int(n_delta_implane*(resolution/2))+(n//2)

        bb_coords = [n_coord - BALL_RAD_implane, m_coord - BALL_RAD_implane, 
                    n_coord + BALL_RAD_implane, m_coord + BALL_RAD_implane]

        if range == "near":
            if 2*BALL_RAD_implane <= NEAR_THRES:
                continue
            else:
                pass

        elif range == "far":
            if 2*BALL_RAD_implane > NEAR_THRES:
                continue
            else:
                pass
        
        else:
            continue

        annotations.append({
            "area": (2*BALL_RAD_implane)**2,
            "iscrowd": 0,
            "bbox": bb_coords,
            "category_id": 0,
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
