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
        FOV = 120
        r_ball = ball_vector[0]
        theta_ball = ball_vector[1]
        phi_ball = ball_vector[2]

        # 2D implane through ball centre
        r_implane_theta = r_ball*np.cos(np.deg2rad(theta_ball)) 
        r_implane_phi = r_ball*np.cos(np.deg2rad(phi_ball))
        r_implane = np.sqrt(r_implane_theta**2 + r_implane_phi**2)
        print(name, r_implane)

        w_implane = r_implane*np.tan(np.deg2rad(FOV//2))*2
        resolution = max(m,n)
        BALL_RAD_implane = int((BALL_RAD/w_implane*resolution))

        #implane_width_theta = r_implane_theta*np.tan(np.deg2rad(FOV//2))
        #implane_width_phi = r_implane_phi*np.tan(np.deg2rad(FOV//2))
        #implane_rad = int((BALL_RAD/implane_width)*(n//2))

        m_delta_implane = r_ball*np.sin(np.deg2rad(theta_ball))
        n_delta_implane = r_ball*np.sin(np.deg2rad(phi_ball))
        m_coord = -int(n_delta_implane/(w_implane/2)*(resolution/2))+(m//2)
        n_coord = -int(m_delta_implane/(w_implane/2)*(resolution/2))+(n//2)

        cv2.circle(output_img, (n_coord, m_coord), BALL_RAD_implane,  (255, 0, 0), 1)

    # store result
    output = Image.fromarray(output_img)
    output.save(name[:-5] + ".jpeg")
