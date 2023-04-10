#!/usr/bin/env python3
"""Decode base64 encoded images"""

import json
import os
import glob
import numpy as np
from datetime import date
from decode import decode, translate_coords
from PIL import Image

def iterable_list(in_list):
    if isinstance(in_list, list):
        return in_list
    else:
        return [in_list]

set_options = ["train", "validation", "test"]  # Only choose one
size_options = ["s", "m", "l"]  # One or all
occlusion_options = [False, True]  # Either or both
type_options = ["match", "drill"]  # Either or both

set = set_options[0]
size = size_options[2]  # Large == close
occlusion = occlusion_options[0]
type = type_options[:]

output_dir = ("./cutout/")

try:
    os.makedirs(output_dir)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./'+ set + "/", "*.json"))

images = []
neg_annotations = []
pos_annotations = []
SMALL_THRES = 32  # height in pixels
LARGE_THRES = 96 
cutout_dim = 0

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)

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

    if img_dict["ball_sighted"]==1:

        ball_vector = np.asarray(img_dict["ball_locate"])
        m_coord, n_coord, BALL_RAD_implane = translate_coords(output_img, ball_vector)

        if size == "s":
            if 2*BALL_RAD_implane <= SMALL_THRES:
                cutout_dim = 16
                pass
            else:
                print("Skipped for size")
                continue

        elif size == "m":
            if 2*BALL_RAD_implane > SMALL_THRES and 2*BALL_RAD_implane < LARGE_THRES:
                cutout_dim = 32
                pass
            else:
                print("Skipped for size")
                continue

        elif size == "l":
            if 2*BALL_RAD_implane > LARGE_THRES:
                cutout_dim = 64
                pass
            else:
                print("Skipped for size")
                continue
        
        else:
            pass

        img_name = name[3+len(set):-5] + ".jpeg"
   
        # store result
        cutout = output_img[int(m_coord-BALL_RAD_implane):int(m_coord+BALL_RAD_implane+1),
                           int(n_coord-BALL_RAD_implane):int(n_coord+BALL_RAD_implane+1)]
        output = Image.fromarray(cutout)
        output = output.resize((cutout_dim, cutout_dim))
        output.save(output_dir + img_name)
