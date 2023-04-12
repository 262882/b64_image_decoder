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
from decode import decode

if __name__ == "__main__":

    output_dir = "video_out"
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    img_list = []
    if len(sys.argv)==1:
        album = True
    else:
        album = False

    if not album:
        img_list.append(sys.argv[1])

    elif album:
        img_num = []
        img_list = glob.glob(os.path.join('./', "*.json"))

        for name in img_list:
            img_num.append(name[name.rfind('-')+1:-5])
            img_order = np.argsort(np.array(img_num).astype(np.int))

    FPS = 25 # Capture rate
    duration = len(img_list)//FPS # seconds
    video = cv2.VideoWriter(output_dir +'/video_out.avi', cv2.VideoWriter_fourcc(*'MP42'),
                        float(FPS), (480, 480))
    
    for frame in range(FPS*duration):
        print("Process frame: " + str(frame))

        with open(img_list[img_order[frame]], 'r') as input_file:
            img_dict = json.load(input_file)

        output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])
        video.write(output_img[:,:,::-1])

video.release()
print("Complete")