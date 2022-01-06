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
src_dir = os.path.join(main_dir, 'sources')

sys.path.append(module_dir)
import discordlib_pyplot as dlt

'''
copy the import parts
'''


def read_excel(excel) : 
    df = pd.read_excel(excel)
    if 'Unnamed: 0' in df.columns :
        df.drop('Unnamed: 0', axis = 1, inplace = True)

    return df

def load_img(file_name) :
    pil_image = Image.open(file_name)
    pil_width, pil_height = pil_image.size
    pil_draw = ImageDraw.Draw(pil_image)
    opencv_image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    opencv_hsv = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(opencv_hsv)
    h = h.transpose()
    s = s.transpose()
    v = v.transpose()

    return pil_image, pil_draw, pil_width, pil_height, h, s, v

def load_img_greyscale(file_name) :
    pil_image = Image.open(file_name)
    pil_image = pil_image.convert('L')

    pil_width, pil_height = pil_image.size
    pil_draw = ImageDraw.Draw(pil_image)

    pil_hsv = pil_image.convert('HSV')
    h, s, v = pil_hsv.split()
    h = np.array(h).transpose()
    s = np.array(s).transpose()
    v = np.array(v).transpose()


    print(pil_image.size)
    print(v.shape)

    return pil_image, pil_draw, pil_width, pil_height, h, s, v

def rgb2hsv_pil(image) :
    return image.convert('HSV')


def load_img_resize(file_name, multiplier) :
    pil_image = Image.open(file_name)
    pil_width, pil_height = pil_image.size
    new_width = pil_width * multiplier
    new_height = pil_height * multiplier

    pil_image = pil_image.resize((new_width, new_height), Image.BILINEAR)
    pil_draw = ImageDraw.Draw(pil_image)

    pil_hsv = pil_image.convert('HSV')
    h, s, v = pil_hsv.split()
    h = np.array(h).transpose()
    s = np.array(s).transpose()
    v = np.array(v).transpose()

#    opencv_image = cv2.imread(file_name, cv2.IMREAD_COLOR)
#    opencv_image = cv2.resize(opencv_image, dsize = (new_width, new_height))
#
#    opencv_hsv = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2HSV)
#    h, s, v = cv2.split(opencv_hsv)
#    h = h.transpose()
#    s = s.transpose()
#    v = v.transpose()
#
    return pil_image, pil_draw, new_width, new_height, h, s, v


def get_draw(width, height, colour) :
    image = Image.new('RGBA', size = (width, height), color = colour)
    draw = ImageDraw.Draw(image)

    return image, draw



def grid_rectangle(draw, width, height, interval, gap, grid_colour) :
    '''
    interval * (n) + gap * (n-1) < width < interval * (n+1) + gap * (n)
    side = width - (interval * n + gap * (n-1))
    '''

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
        draw.rectangle(now_draw_list, fill = None, outline = grid_colour, width = 1)

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

        hsv_value.append(255 - (tmp_array.sum().sum() / (tmp_array.shape[0] * tmp_array.shape[1])))

    return hsv_value



def internal_division(a, b, m, n) :
    return (a * n + b * m) / (m + n)

def convert_to_greyscale(image) :
    return image.convert('L') # L : greyscale, '1' : binary, 'RGB', 'RGBA', 'CMYK'

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
        

def get_area(hsv_value, target_value, t_range) :
    width = hsv_value.shape[0]
    height = hsv_value.shape[1]
    colour = None

    temp_image = Image.new(mode = 'RGBA', size = (width, height), color = colour)
    temp_draw = ImageDraw.Draw(temp_image)
    area = np.zeros((width, height))

    for x in range(width) :
        for y in range(height) :
            if hsv_value[x, y] == target_value :
                check = 1
                
                for x_add in range(t_range) :
                    for y_add in range(t_range) :
                        if x + x_add < width :
                            if hsv_value[x + x_add, y] != target_value :
                                check = 0
                                break
                        if y + y_add < height :
                            if hsv_value[x, y + y_add] != target_value :
                                check = 0
                                break

                if check == 1 :
                    area[x : x + x_add, y : y + y_add] = 1
                    
                    temp_draw.rectangle((x, y, x + x_add, y + y_add), outline = 'red', width = 1)
            print(f'({x}, {y}) is done', end = '\r')

    return temp_image, area   

                            
