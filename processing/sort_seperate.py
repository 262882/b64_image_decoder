#!/usr/bin/env python3
"""Seperate out files from json dataset"""

import json
import os
import glob
import numpy as np
import cv2
from decode import decode

output_dir = "seperate"
try:
    os.makedirs(output_dir)
except FileExistsError:
    pass

img_list = glob.glob(os.path.join('./',"*.json"))

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)

    output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])

    # Display and sort
    cv2.imshow('Frame', output_img)
    des = print("s - Seperate? q - Quit? - Otherwise any key)")
    key = cv2.waitKey()

    # Process file
    if key==ord('s'):
        print("Seperate")
        with open("./" + output_dir + "/" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)

    elif key==ord('q'):
        break

    else: 
        print("Pass")
