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

    # Process image
    img_bytes = decodebytes(img_dict['img'].encode('ascii'))
    c = 3  # Channels
    m = img_dict['h_img']  # Image height
    n = img_dict['w_img']  # Image width
    output_img = np.reshape(np.frombuffer(img_bytes, dtype='uint8'), (m,n,c))
    output_img = output_img[::-1].copy()   # Rotate 180 degrees

    # Process bounding box
    ball_vector = np.asarray(img_dict["ball_locate"])
    if img_dict["ball_sighted"]==1 and np.sum(np.abs(ball_vector)) != 0 :
        BALL_RAD = 0.042
        FOV = 58
        r_ball = ball_vector[0]
        theta_ball = ball_vector[1]
        phi_ball = ball_vector[2]

        # Image plane properties
        resolution = max(m,n)
        w_implane = r_ball*np.tan(np.deg2rad(FOV//2))*2
        BALL_RAD_implane = int((BALL_RAD/w_implane*resolution))

        # Localization
        m_delta_implane = phi_ball/(FOV/2)
        n_delta_implane = theta_ball/(FOV/2)
        m_coord = -int(m_delta_implane*(resolution/2))+(m//2)
        n_coord = -int(n_delta_implane*(resolution/2))+(n//2)

        cv2.circle(output_img, (n_coord, m_coord), BALL_RAD_implane,  (255, 0, 0), 1)

    # store result
    output = Image.fromarray(output_img)
    output.save(name[:-5] + ".jpeg")
