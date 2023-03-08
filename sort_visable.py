#!/usr/bin/env python3
"""Decode base64 encoded images"""

import json
import sys
import os
import glob
import uuid
import numpy as np

output_dir1 = "vis_true"
try:
    os.makedirs(output_dir1)
except FileExistsError:
    pass

output_dir2 = "vis_false"
try:
    os.makedirs(output_dir2)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./',"*.json"))
prefix = str(uuid.uuid4().fields[-1])[:5]

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)
        
    ball_vector = np.asarray(img_dict["ball_locate"])
    if img_dict["ball_sighted"]==1 and np.sum(np.abs(ball_vector)) != 0 :
        with open("./"+ output_dir1 + "/" + prefix + "_" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)

    elif img_dict["ball_sighted"]==0 and np.sum(np.abs(ball_vector)) == 0 :
        with open("./"+ output_dir2 + "/" + prefix + "_" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)