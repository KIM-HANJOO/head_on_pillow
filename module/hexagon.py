from PIL import Image, ImageDraw
import os
import sys
from pathlib import Path
import cv2
import math
import pandas as pd

import matplotlib.pyplot as plt
#import imodule as imd
import numpy as np
import random


module_dir = os.getcwd()
tmp_path = Path(module_dir)
main_dir = tmp_path.parent.absolute()
smpl_dir = os.path.join(main_dir, 'sample')
plot_dir = os.path.join(main_dir, 'image')

sys.path.append(module_dir)
import discordlib_pyplot as dlt

'''
info
'''
def grid_rectangle(draw, width, height, interval, gap, grid) :
    '''
    interval * (n) + gap * (n-1) < width < interval * (n+1) + gap * (n)
    side = width - (interval * n + gap * (n-1))
    '''
    if grid == 0 :
        colour = 'white'
    else :
        colour = 'grey'

    n_width = int(math.floor((width + gap) / (interval + gap)))
    n_height = int(math.floor((height + gap) / (interval + gap)))

    side_width = 0.5 * (width - (interval * n_width + gap * (n_width-1)))
    side_height = 0.5 * (height - (interval * n_height + gap * (n_height-1)))

    box_number = n_width * n_height
    box_info = np.zeros((box_number, 4))

    start_vertex = [side_width, side_height]
    print(f'n_width = {n_width}, n_height = {n_height}')
    
    for index in range(box_number) :
        now_x = int(index % n_width)
        now_y = int(index // n_width)
        
        # box_info 0, 1 are (x, y) for the left-top vertex
        box_info[index, 0] = start_vertex[0] + interval * now_x + gap * now_x
        box_info[index, 1] = start_vertex[1] + interval * now_y + gap * now_y
        
        # box info 2, 3 are (x, y) for the right-bottom vertex
        box_info[index, 2] = start_vertex[0] + interval * (now_x + 1) + gap * (now_x + 1)
        box_info[index, 3] = start_vertex[1] + interval * (now_y + 1) + gap * (now_y + 1)

    for index in range(box_number) :
        now_draw_list = box_info[index, :].tolist()
        draw.rectangle(now_draw_list, fill = None, outline = colour, width = 1)

    return box_info, side_width, side_height


def h_of_box(x_smpl, box_info) :
    x_smpl = x_smpl.transpose()
    hsv_value = []
    for index in range(box_info.shape[0]) :

        left_x = int(box_info[index, 0])
        right_x = int(box_info[index, 2])
        left_y = int(box_info[index, 1])
        right_y = int(box_info[index, 3])

        tmp_array = x_smpl[left_x : right_x, left_y : right_y]

#        image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
#        draw2 = ImageDraw.Draw(image)
#        draw2.rectangle((left_x, left_y, right_x, right_y), fill = 'black', outline = 'black', width = 1)
#        dlt.savepng(image, plot_dir, f'canvas_{index}.png')

        hsv_value.append((tmp_array.sum().sum() / (tmp_array.shape[0] * tmp_array.shape[1])))


    return hsv_value


def s_of_box(x_smpl, box_info) :
    x_smpl = x_smpl.transpose()
    hsv_value = []
    for index in range(box_info.shape[0]) :

        left_x = int(box_info[index, 0])
        right_x = int(box_info[index, 2])
        left_y = int(box_info[index, 1])
        right_y = int(box_info[index, 3])

        tmp_array = x_smpl[left_x : right_x, left_y : right_y]

#        image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
#        draw2 = ImageDraw.Draw(image)
#        draw2.rectangle((left_x, left_y, right_x, right_y), fill = 'black', outline = 'black', width = 1)
#        dlt.savepng(image, plot_dir, f'canvas_{index}.png')

        hsv_value.append((tmp_array.sum().sum() / (tmp_array.shape[0] * tmp_array.shape[1])))


    return hsv_value


def v_of_box(x_smpl, box_info) :
    x_smpl = x_smpl.transpose()
    hsv_value = []
    for index in range(box_info.shape[0]) :

        left_x = int(box_info[index, 0])
        right_x = int(box_info[index, 2])
        left_y = int(box_info[index, 1])
        right_y = int(box_info[index, 3])

        tmp_array = x_smpl[left_x : right_x, left_y : right_y]

#        image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
#        draw2 = ImageDraw.Draw(image)
#        draw2.rectangle((left_x, left_y, right_x, right_y), fill = 'black', outline = 'black', width = 1)
#        dlt.savepng(image, plot_dir, f'canvas_{index}.png')

        hsv_value.append(255 - (tmp_array.sum().sum() / (tmp_array.shape[0] * tmp_array.shape[1])))


    return hsv_value



def internal_division(a, b, m, n) :
    return (a * n + b * m) / (m + n)



def hsv_to_circle(draw, interval, hsv_value, box_info) :
    min_radius = 0 #interval / 4
    max_radius = interval / 2
    
    radius_value = []

    # change hsv to radius
    hsv_rev = [x for x in hsv_value if x != 0]

    min_hsv = min(hsv_rev)
    max_hsv = max(hsv_rev)
    ave_hsv = sum(hsv_rev) / len(hsv_rev)

    # floor some values
    for i in range(len(hsv_value)) :
        if float(hsv_value[i]) <= 0.5 * ave_hsv :
            hsv_value[i] = 0


    for hsv in hsv_value :
        if hsv == 0 :
            radius_value.append(0)
        else :
            ratio = (hsv - min_hsv) / (max_hsv - min_hsv)
            if ratio < 0 :
                radius_value.append(0)
            else :
                radius_value.append(internal_division(min_radius, max_radius, ratio, 1 - ratio))


    for index in range(box_info.shape[0]) :
        left_x = box_info[index, 0]
        right_x = box_info[index, 2]
        left_y = box_info[index, 1]
        right_y = box_info[index, 3]

        midpoint = [0.5 * (left_x + right_x), 0.5 * (left_y + right_y)]
        radius = radius_value[index]
        
        ellipse_points = [midpoint[0] - radius, midpoint[1] - radius, \
                          midpoint[0] + radius, midpoint[1] + radius]
        if radius != 0 :
            draw.ellipse(ellipse_points, fill = 'black', outline = 'black')
        
        



for interval in [70, 100, 150, 300, 500, 800, 1000] :
    save = 1 
    #interval = 200 
    gap = 0
    mult = 10

# load image

    os.chdir(smpl_dir)
    image_name = 'face.jpg'
#image_name = 'pink_panther.jpg'
    smpl = Image.open(image_name)
    smpl_width, smpl_height = smpl.size
    smpl = smpl.resize((smpl_width * mult, smpl_height * mult))

    src = cv2.imread(image_name, cv2.IMREAD_COLOR)
    src = cv2.resize(src, dsize = (smpl_width * mult, smpl_height * mult), interpolation = cv2.INTER_LINEAR)

    smpl_width = smpl_width * mult
    smpl_height = smpl_height * mult


    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h_smpl, s_smpl, v_smpl = cv2.split(hsv)
    v_smpl = np.array(v_smpl)


# ready to draw
    image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
    draw1 = ImageDraw.Draw(smpl)
    draw2 = ImageDraw.Draw(image)
    for i in range(2) :
        draw = globals()[f'draw{i+1}']
        if i == 0 :
            grid = 1
        else :
            grid = 0

# make grid (box)
        box_info, side_width, side_height = grid_rectangle(draw, smpl_width, smpl_height, interval, gap, grid)

# hsv_info for all boxes
        hsv_value = []
        h_value = h_of_box(h_smpl, box_info)
        s_value = s_of_box(s_smpl, box_info)
        v_value = v_of_box(v_smpl, box_info)
#    print('h_value =\n', h_value)
#    print('s_value =\n', s_value)
#    print('v_value =\n', v_value)

        for i in range(len(h_value)) :
            hsv_value.append(0 * h_value[i] + 0 * s_value[i] + v_value[i])
        hsv_temp = [x for x in hsv_value if x != 0]
        print(sum(hsv_temp) / len(hsv_temp))

# change hsv_info to R of circle
        hsv_to_circle(draw, interval, hsv_value, box_info) 

# print session
#    print(v_smpl)
#    print(v_smpl.shape)
#    print(box_info)


    if save == 1 :
        dlt.savepng(smpl, plot_dir, 'canvas.png')
        dlt.savepng(image, plot_dir, f'canvas_{interval}.png')
        pass
