#!/usr/bin/env python3
"""Add key-value pair to json file"""

import json
import sys
import os
import glob
import uuid
import numpy as np

img_list = glob.glob(os.path.join('./',"*.json"))
prefix = str(uuid.uuid4().fields[-1])[:5]

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)
        
    ball_vector = np.asarray(img_dict["ball_locate"])
    img_dict["type"]="drill"
    img_dict["occluded"]=False

    with open("./processed/" + name[2:], 'w') as out_file:
        json.dump(img_dict, out_file)