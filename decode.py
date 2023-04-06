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
from math import floor, ceil, sqrt

def decode(encoded_image, m, n):
    img_bytes = decodebytes(encoded_image.encode('ascii'))
    c = 3  # Channels
    output_img = np.reshape(np.frombuffer(img_bytes, dtype='uint8'), (m,n,c))
    output_img = output_img[::-1].copy()   # Rotate 180 degrees
    return output_img

def add_bb(image, ball_vector):
    BALL_RAD = 0.042
    FOV = 58
    eff_FOV =  61  #2*np.arctan2(np.radians(np.tan(FOV/2)),sqrt(2))
    r_ball = ball_vector[0]
    theta_ball = ball_vector[1]
    phi_ball = ball_vector[2]
    m, n = image.shape[:2]

    # Coord transform local to camera
    NAO_HEAD = 0.065  # Camera offset

    # Spherical to cartesian
    x = r_ball*np.cos(np.radians(phi_ball))*np.sin(np.radians(theta_ball))
    y = r_ball*np.cos(np.radians(phi_ball))*np.cos(np.radians(theta_ball))-NAO_HEAD
    z = r_ball*np.sin(np.radians(phi_ball))

    # Cartesian to spherical
    r_ball_cam = np.linalg.norm([x,y,z])
    phi_ball_cam = np.rad2deg(np.arcsin(z/r_ball_cam))
    theta_ball_cam = np.rad2deg(np.arctan2(x,y))

    # Image plane properties
    resolution = max(m,n)
    w_implane = r_ball_cam*np.radians(FOV//2)*2
    BALL_RAD_implane = (BALL_RAD/w_implane*resolution)

    # Localization
    m_delta_implane = phi_ball_cam/(eff_FOV/2)
    n_delta_implane = theta_ball_cam/(eff_FOV/2)

    m_coord = (m/2)-1-(m_delta_implane*(resolution/2))
    n_coord = (n/2)-1-(n_delta_implane*(resolution/2))

    cv2.rectangle(image, (ceil(n_coord - BALL_RAD_implane), ceil(m_coord - BALL_RAD_implane)), 
                              (floor(n_coord + BALL_RAD_implane), floor(m_coord + BALL_RAD_implane)), (255, 0, 0), 2)

if __name__ == "__main__":

    output_dir = "decode"
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    include_bb = True
    img_list = []
    if len(sys.argv)==1:
        album = True
    else:
        album = False

    if not album:
        img_list.append(sys.argv[1])

    elif album:
        img_list = glob.glob(os.path.join('./', "*.json"))

    for count, name in enumerate(img_list):
        print(count+1, "/", len(img_list), "Images processed")

        with open(name, 'r') as input_file:
            img_dict = json.load(input_file)

        output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])

        if include_bb and (img_dict["ball_sighted"]==1 and np.linalg.norm(img_dict["ball_locate"])>0):
            ball_vector = np.asarray(img_dict["ball_locate"])
            add_bb(output_img, ball_vector)

        # store result
        output = Image.fromarray(output_img)
        output.save("./" + output_dir + "/" + name[:-5] + ".jpeg")
