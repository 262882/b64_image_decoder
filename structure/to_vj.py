#!/usr/bin/env python3
"""Decode base64 encoded images"""

import json
import os
import glob
import numpy as np
from datetime import date
from PIL import Image
import sys
import cv2
sys.path.append(os.path.join(sys.path[0], '../processing/'))
from decode import decode, transform_camsph2bb

def iterable_list(in_list):
    if isinstance(in_list, list):
        return in_list
    else:
        return [in_list]

output_prefix = "vj"

set_options = ["train", "validation", "test"]  # Only choose one
size_options = ["s", "m", "l"]  # One or all
occlusion_options = [False, True]  # Either or both
type_options = ["match", "drill"]  # Either or both
edge_detect = [False, True]  # Either 

set = set_options[0]
size = size_options[1]  # Large == close
occlusion = occlusion_options[0]
type = type_options[:]
edge = edge_detect[1]

output_dir = (
    "./" + output_prefix 
    + "_" + set 
    + "_" + "".join(size) 
    + "_" + "".join(str(val) for val in iterable_list(occlusion))
    + "_" + "".join(type)
    + "_" + str(edge) + "/")

neg_dir = output_dir+"neg/"
pos_dir = output_dir+"pos/"

try:
    os.makedirs(output_dir)
except FileExistsError:
    pass

try:
    os.makedirs(neg_dir)
except FileExistsError:
    pass

try:
    os.makedirs(pos_dir)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./'+ set + "/", "*.json"))

images = []
neg_annotations = []
pos_annotations = []
SMALL_THRES = 32  # height in pixels
LARGE_THRES = 96 

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

    # process images
    if (edge):
        ddepth = cv2.CV_16S
        kernel_size = 3
        grey_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
        edge_img = cv2.Laplacian(grey_img, ddepth, ksize=kernel_size)
        final = np.array((edge_img>100)*255, dtype='uint8')

    else:
        final = output_img

    if img_dict["ball_sighted"]==1:

        ball_vector = np.asarray(img_dict["ball_locate"])
        m_coord, n_coord, BALL_RAD_implane = transform_camsph2bb(output_img, ball_vector)

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

        img_name = name[3+len(set):-5] + ".jpeg"
        pos_annotations.append(
            img_name + "  " +
            str(1) + "  " +
            str(int(n_coord-BALL_RAD_implane)) + " " + str(int(m_coord-BALL_RAD_implane)) + " " +
            str(int(2*BALL_RAD_implane)) + " " + str(int(2*BALL_RAD_implane))
            )

        # store result
        output = Image.fromarray(final)
        output.save(pos_dir + img_name)

    elif img_dict["ball_sighted"]==0:

        img_name = name[3+len(set):-5] + ".jpeg"
        neg_annotations.append(neg_dir + img_name)
   
        # store result
        output = Image.fromarray(final)
        output.save(neg_dir + img_name)

with open("./" + pos_dir + "info.dat", 'w') as out_file:
    for row in pos_annotations:
        out_file.write(row + '\n')

with open("./" + neg_dir + "bg.txt", 'w') as out_file:
    for row in neg_annotations:
        out_file.write(row + '\n')
