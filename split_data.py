#!/usr/bin/env python3
"""Decode base64 encoded images"""

import json
import sys
import os
import glob
import uuid
import numpy as np

img_list = glob.glob(os.path.join('./',"*.json"))
sort_order = np.arange(len(img_list))
np.random.shuffle(sort_order)

train_split = 0.6
valid_split = 0.2
test_split = 1-train_split-valid_split

train_idx = int(train_split*len(img_list))
test_idx = int(test_split*len(img_list))

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)
    
    if count in sort_order[:train_idx-1]:
        with open("./train/" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)

    elif count in sort_order[-test_idx:]:
        with open("./test/" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)

    else:
        with open("./validation/" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)