#!/usr/bin/env python3
"""Decode base64 encoded images"""

from base64 import decodebytes
import json
import sys
import os
import glob
from PIL import Image
import numpy as np
import cv2

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

    # Process image
    img_bytes = decodebytes(img_dict['img'].encode('ascii'))
    c = 3  # Channels
    m = img_dict['h_img']  # Image height
    n = img_dict['w_img']  # Image width
    output_img = np.reshape(np.frombuffer(img_bytes, dtype='uint8'), (m,n,c))
    output_img = output_img[::-1].copy()   # Rotate 180 degrees

    # Process bounding box
    ball_vector = np.asarray(img_dict["ball_locate"])

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
