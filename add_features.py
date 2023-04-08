#!/usr/bin/env python3
"""Add key-value pair to json file"""

import json
import sys
import os
import glob
import uuid
import numpy as np

output_dir1 = "processed"
try:
    os.makedirs(output_dir1)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./',"*.json"))
prefix = str(uuid.uuid4().fields[-1])[:5]

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)
        
    img_dict["type"]="match" # ["drill", "match"]

    with open("./processed/" + name[2:], 'w') as out_file:
        json.dump(img_dict, out_file)