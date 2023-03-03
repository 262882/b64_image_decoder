#!/usr/bin/env python3
"""Decode base64 encoded images"""

from base64 import decodebytes
import json
import sys
import os
import glob
from PIL import Image
import numpy as np

album = False
img_list = []
if len(sys.argv)==1:
    album = True

if not album:
    img_list.append(sys.argv[1])

elif album:
    img_list = glob.glob(os.path.join('./',"*.json"))

for count, name in enumerate(img_list):
    print(count+1, "/", len(img_list), "Images processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)

    img_bytes = decodebytes(img_dict['img'].encode('ascii'))
    c = 3  # Channels
    m = img_dict['h_img']  # Image height
    n = img_dict['w_img']  # Image width

    output_img = np.zeros([m, n, c],dtype='uint8')
    for k in range(c):
        for j in range(m):
            for i in range(n):
                ind = 3*(i) + 3*j*n + k
                output_img[-j,-i,k]=img_bytes[ind]

    output = Image.fromarray(output_img)
    output.save(name[:-5] + ".jpeg")
