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

#categories = [
#    {
#    "id": 1,
#    "name": "ball",
#    "supercategory": "none"
#    },
#    {
#    "id": 2,
#    "name": "nao",
#    "supercategory": "none"
#    },
#    ]

categories = [
    {"supercategory": "person","id": 1,"name": "person"},  #1
    {"supercategory": "vehicle","id": 2,"name": "bicycle"},  #2
    {"supercategory": "vehicle","id": 3,"name": "car"},  #3
    {"supercategory": "vehicle","id": 4,"name": "motorcycle"},  #4
    {"supercategory": "vehicle","id": 5,"name": "airplane"},  #5
    {"supercategory": "vehicle","id": 6,"name": "bus"},  #6
    {"supercategory": "vehicle","id": 7,"name": "train"},  #7
    {"supercategory": "vehicle","id": 8,"name": "truck"},  #8
    {"supercategory": "vehicle","id": 9,"name": "boat"},  #9
    {"supercategory": "outdoor","id": 10,"name": "traffic light"},  #10
    {"supercategory": "outdoor","id": 11,"name": "fire hydrant"},  #11
    {"supercategory": "outdoor","id": 13,"name": "stop sign"},  #12
    {"supercategory": "outdoor","id": 14,"name": "parking meter"},  #13
    {"supercategory": "outdoor","id": 15,"name": "bench"},  #14
    {"supercategory": "animal","id": 16,"name": "bird"},  #15
    {"supercategory": "animal","id": 17,"name": "cat"},  #16
    {"supercategory": "animal","id": 18,"name": "dog"},  #17
    {"supercategory": "animal","id": 19,"name": "horse"},  #18
    {"supercategory": "animal","id": 20,"name": "sheep"},  #19
    {"supercategory": "animal","id": 21,"name": "cow"},  #20
    {"supercategory": "animal","id": 22,"name": "elephant"},  #21
    {"supercategory": "animal","id": 23,"name": "bear"},  #22
    {"supercategory": "animal","id": 24,"name": "zebra"},  #23
    {"supercategory": "animal","id": 25,"name": "giraffe"},  #24
    {"supercategory": "accessory","id": 27,"name": "backpack"},  #25
    {"supercategory": "accessory","id": 28,"name": "umbrella"},  #26
    {"supercategory": "accessory","id": 31,"name": "handbag"},  #27
    {"supercategory": "accessory","id": 32,"name": "tie"},  #28
    {"supercategory": "accessory","id": 33,"name": "suitcase"},  #29
    {"supercategory": "sports","id": 34,"name": "frisbee"},  #30
    {"supercategory": "sports","id": 35,"name": "skis"},  #31
    {"supercategory": "sports","id": 36,"name": "snowboard"},  #32
    {"supercategory": "sports","id": 37,"name": "sports ball"},  #33
    {"supercategory": "sports","id": 38,"name": "kite"},  #34
    {"supercategory": "sports","id": 39,"name": "baseball bat"},  #35
    {"supercategory": "sports","id": 40,"name": "baseball glove"},  #36
    {"supercategory": "sports","id": 41,"name": "skateboard"},  #37
    {"supercategory": "sports","id": 42,"name": "surfboard"},  #38
    {"supercategory": "sports","id": 43,"name": "tennis racket"},  #39
    {"supercategory": "kitchen","id": 44,"name": "bottle"},  #40
    {"supercategory": "kitchen","id": 46,"name": "wine glass"},  #41
    {"supercategory": "kitchen","id": 47,"name": "cup"},  #42
    {"supercategory": "kitchen","id": 48,"name": "fork"},  #43
    {"supercategory": "kitchen","id": 49,"name": "knife"},  #44
    {"supercategory": "kitchen","id": 50,"name": "spoon"},  #45
    {"supercategory": "kitchen","id": 51,"name": "bowl"},  #46
    {"supercategory": "food","id": 52,"name": "banana"},  #47
    {"supercategory": "food","id": 53,"name": "apple"},  #48
    {"supercategory": "food","id": 54,"name": "sandwich"},  #49
    {"supercategory": "food","id": 55,"name": "orange"},  #50
    {"supercategory": "food","id": 56,"name": "broccoli"},  #51
    {"supercategory": "food","id": 57,"name": "carrot"},  #52
    {"supercategory": "food","id": 58,"name": "hot dog"},  #53
    {"supercategory": "food","id": 59,"name": "pizza"},  #54
    {"supercategory": "food","id": 60,"name": "donut"},  #55
    {"supercategory": "food","id": 61,"name": "cake"},  #56
    {"supercategory": "furniture","id": 62,"name": "chair"},  #57
    {"supercategory": "furniture","id": 63,"name": "couch"},  #58
    {"supercategory": "furniture","id": 64,"name": "potted plant"},  #59
    {"supercategory": "furniture","id": 65,"name": "bed"},  #60
    {"supercategory": "furniture","id": 67,"name": "dining table"},  #61
    {"supercategory": "furniture","id": 70,"name": "toilet"},  #62
    {"supercategory": "electronic","id": 72,"name": "tv"},  #63
    {"supercategory": "electronic","id": 73,"name": "laptop"},  #64
    {"supercategory": "electronic","id": 74,"name": "mouse"},  #65
    {"supercategory": "electronic","id": 75,"name": "remote"},  #66
    {"supercategory": "electronic","id": 76,"name": "keyboard"},  #67
    {"supercategory": "electronic","id": 77,"name": "cell phone"},  #68
    {"supercategory": "appliance","id": 78,"name": "microwave"},  #69
    {"supercategory": "appliance","id": 79,"name": "oven"},  #70
    {"supercategory": "appliance","id": 80,"name": "toaster"},  #71
    {"supercategory": "appliance","id": 81,"name": "sink"},  #72
    {"supercategory": "appliance","id": 82,"name": "refrigerator"},  #73
    {"supercategory": "indoor","id": 84,"name": "book"},  #74
    {"supercategory": "indoor","id": 85,"name": "clock"},  #75
    {"supercategory": "indoor","id": 86,"name": "vase"},  #76
    {"supercategory": "indoor","id": 87,"name": "scissors"},  #77
    {"supercategory": "indoor","id": 88,"name": "teddy bear"},  #78
    {"supercategory": "indoor","id": 89,"name": "hair drier"},  #79
    {"supercategory": "indoor","id": 90,"name": "toothbrush"},  #80
]

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
            "category_id": 37, #1,
            "ignore": 0,
            "segmentation": [],
            "image_id": img_id,
            "id": anno_id
        })
        anno_id = anno_id + 1

    img_name = name[3+len(set):-5] + ".jpeg"
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
