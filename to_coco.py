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
type_options = ["all", "game", "drill"]
occlusion_options = ["all", "exclude", "include"]
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
annotations = []

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)

    #if occlusion:

    #if (img_dict["occlusion" = True])
    
    output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])

    # Process bounding box
    #ball_vector = np.asarray(img_dict["ball_locate"])
    #if img_dict["ball_sighted"]==1 and np.sum(np.abs(ball_vector)) != 0 :

    # store result
    output = Image.fromarray(output_img)
    output.save(output_dir + name[2+len(set):-5] + ".jpeg")

dataset = {
    "info": info,
    "licenses": licenses,
    "categories": categories,
    "images": images,
    "annotations": annotations
    }

with open("./" + output_dir + "annot.json", 'w') as out_file:
            json.dump(dataset, out_file, indent=4)
