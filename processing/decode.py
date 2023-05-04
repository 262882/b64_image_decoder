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

def spherical2cartesian(R_, theta, phi):
    x_ = R_ * np.cos(np.radians(phi)) * np.cos(np.radians(theta))
    y_ = R_ * np.cos(np.radians(phi)) * np.sin(np.radians(theta))
    z_ = R_ * np.sin(np.radians(phi))
    return x_, y_, z_

def cartesian2spherical(x_, y_, z_):
    R_ = np.linalg.norm([x_, y_, z_])
    theta = np.rad2deg(np.arctan2(y_,x_))
    phi = np.rad2deg(np.arcsin(z_/R_))
    return R_, theta, phi

def ballSpherical2bb(R_, theta, phi, im_shape, BALL_RAD = 0.042, FOV = 58):

    # Image plane properties
    m,n = im_shape[:2]
    resolution = max(m, n)
    w_implane = R_*np.radians(FOV//2)*2
    BALL_RAD_implane = (BALL_RAD/w_implane*resolution)

    # Position on arc
    m_delta_arc = np.sin(np.radians(phi))/np.sin(np.radians(FOV/2))
    n_delta_arc = np.sin(np.radians(theta))/np.sin(np.radians(FOV/2))
    delta_ang = np.rad2deg(np.arctan2(m_delta_arc, n_delta_arc))

    # Position on plane
    spher_ang = np.rad2deg(np.arccos(np.cos(np.radians(phi))*np.cos(np.radians(theta))))
    rd = np.tan(np.radians(spher_ang))/np.tan(np.radians(FOV/2))
    m_delta_plane = rd*np.sin(np.radians(delta_ang))
    n_delta_plane = rd*np.cos(np.radians(delta_ang))

    m_coord = (m/2)-1-(m_delta_plane)*(resolution/2)
    n_coord = (n/2)-1-(n_delta_plane)*(resolution/2)

    return m_coord, n_coord, BALL_RAD_implane

def ballbb2Spherical(m_coord, n_coord, BALL_RAD_implane, im_shape, BALL_RAD = 0.042, FOV = 58):

    # Image plane properties
    m, n = im_shape[:2]
    resolution = max(m, n)
    w_implane = BALL_RAD*resolution/BALL_RAD_implane
    R_ = w_implane/(np.radians(FOV//2)*2)

    # Position on plane
    m_delta_plane = ((m/2)-1-m_coord)/(resolution/2)
    n_delta_plane = ((n/2)-1-n_coord)/(resolution/2)
    rd = np.linalg.norm([m_delta_plane, n_delta_plane])  # How must be scaled?
    delta_ang = np.rad2deg(np.arctan2(m_delta_plane, n_delta_plane))

    # Position on arc    
    spher_ang = np.rad2deg(np.arctan(rd*np.tan(np.radians(FOV/2))))
    phi = spher_ang*np.sin(np.radians(delta_ang))
    theta = spher_ang*np.cos(np.radians(delta_ang))

    return R_, theta, phi

def transform_camsph2bb(image, ball_vector):
    BALL_RAD = 0.042
    FOV = 58
    r_ball = ball_vector[0]
    theta_ball = ball_vector[1]
    phi_ball = ball_vector[2]
    m, n = image.shape[:2]

    # Coord transform local to camera
    NAO_HEAD = 0.065  # Camera offset
    x, y, z = spherical2cartesian(r_ball, theta_ball, phi_ball)
    x, y = y, x - NAO_HEAD
    r_ball_cam, theta_ball_cam, phi_ball_cam = cartesian2spherical(y, x, z)

    return ballSpherical2bb(r_ball_cam, theta_ball_cam, phi_ball_cam, image.shape[:2])

def add_bb_frmcamsph(image, ball_vector, color = (255, 0, 0)):
    m_coord, n_coord, BALL_RAD_implane = transform_camsph2bb(image, ball_vector)
    cv2.rectangle(image, (ceil(n_coord - BALL_RAD_implane), ceil(m_coord - BALL_RAD_implane)), 
                              (floor(n_coord + BALL_RAD_implane), floor(m_coord + BALL_RAD_implane)), color, 1)
    
def add_bb_frmsph(image, ball_vector, color = (255, 0, 0)):
    m_coord, n_coord, BALL_RAD_implane = ballSpherical2bb(ball_vector[0], ball_vector[1], ball_vector[2], image.shape[:2])
    cv2.rectangle(image, (ceil(n_coord - BALL_RAD_implane), ceil(m_coord - BALL_RAD_implane)), 
                              (floor(n_coord + BALL_RAD_implane), floor(m_coord + BALL_RAD_implane)), color, 1)
    
def add_bb_frmbb(image, boxes, color = (255, 0, 0)):
    m_coord, n_coord, BALL_RAD_implane = boxes
    cv2.rectangle(image, (ceil(n_coord - BALL_RAD_implane), ceil(m_coord - BALL_RAD_implane)), 
                              (floor(n_coord + BALL_RAD_implane), floor(m_coord + BALL_RAD_implane)), color, 1)
    
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
            add_bb_frmcamsph(output_img, ball_vector, add_cam_offset = True)

        # store result
        output = Image.fromarray(output_img)
        output.save("./" + output_dir + "/" + name[:-5] + ".jpeg")
