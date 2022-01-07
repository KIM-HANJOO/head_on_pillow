import time
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
tilesets_dir = os.path.join(main_dir, 'pokemon_red_tilesets')
org_tilesets_dir = os.path.join(tilesets_dir, 'tilesets_org')
split_tilesets_dir = os.path.join(tilesets_dir, 'tilesets_split')
grid_tilesets_dir = os.path.join(tilesets_dir, 'tilesets_grid')
big_tilesets_dir = os.path.join(tilesets_dir, 'tilesets_extended_800x800')
dir_64x64 = os.path.join(tilesets_dir, 'tilesets_extended_64x64')
dir_96x96 = os.path.join(tilesets_dir, 'tilesets_extended_96x96')



sys.path.append(module_dir)
import discordlib_pyplot as dlt
import directory_change as dich
import image_module as im
import random

'''
info
each tile is 32 * 32,
in the tilesets assume that each tile is 16 * 16
'''
interval = 96 
gap = 0
resize_param = 1
set_tiledir = big_tilesets_dir

if interval in [8, 16, 64, 96] :
    tiledir = globals()[f'dir_{interval}x{interval}']

else : 
    tiledir = big_tilesets_dir

img_name = 'mona_lisa.jpg'
greyscaled_multiplier = resize_param #0.3
greyscaled_name = f'{img_name[ : -4]}_greyscaled.jpg'
greyscaled_name = 'scull.jpg'

# load image, save greyscaled
os.chdir(smpl_dir)
smpl_org = Image.open(img_name)
smpl_org = smpl_org.convert('L')
smpl_width_org, smpl_height_org = smpl_org.size
nwidth = round(smpl_width_org * greyscaled_multiplier)
nheight = round(smpl_height_org * greyscaled_multiplier)
smpl_org = smpl_org.resize((nwidth, nheight), Image.BICUBIC)
smpl_org.save(greyscaled_name)


# load greyscaled img
smpl, smpl_draw, smpl_width, smpl_height, h_smpl, s_smpl, v_smpl = im.load_img(greyscaled_name)
smpl_info, side_width, side_height = im.grid_rectangle(smpl_draw, smpl_width, smpl_height, interval, gap, None)#'red')

# white new canvas
canvas, canvas_draw = im.get_draw(smpl_width, smpl_height, 'White')
box_info, box_width, box_height = im.grid_rectangle(canvas_draw, smpl_width, smpl_height, interval, gap, None)#'red')



# -------------------------------------------------------------------------
# logic
# -------------------------------------------------------------------------

print('logic')
os.chdir(tilesets_dir)
v_info = im.read_excel('tilesets_v_info.xlsx')
v_info['sum'] = None
print('tilesets excel loaded')

total = smpl_info.shape[0]
# for the comparing sequence, having (255 - v_value) is not needed
for c in range(2) :
    if c == 0 :
        cho = 1
    else :
        cho = 3

    for index in range(smpl_info.shape[0]) :
        # smpl_info : grid info of smpl image
        if index > 540 :
            start = time.time()
            left_x = int(smpl_info[index, 0])
            right_x = int(smpl_info[index, 2])
            left_y = int(smpl_info[index, 1])
            right_y = int(smpl_info[index, 3])

            h_array = v_smpl[left_x : right_x, left_y : right_y]
            # v_info : v values for all tilesets
            # v_info_small : small version of v_info 

            # v_smpl : v values for all pixels in smpl image
            # h_array : v values only of the chosen grid(intervals x intervals)
            # h_rs_array : reshaped version of h_array
            # h_rs_small : small version (3x3) of h_rs_array (using 'ncols')

            h_rs_array = h_array.reshape(1, h_array.shape[0] * h_array.shape[1])

            ncols_add = ['tilename', 'sum']
            ncols_int = [1, 5, 8, 33, 37, 39, 56, 60, 63]
            ncols = ['1', '5', '8', '33', '37', '39', '56', '60', '63']
            ncols_all = ncols_add + ncols

            h_small_cols = []
            for integ in ncols_int :
                h_small_cols.append(round(pow(interval, 2) * (integ / 64)))

            v_info_small = v_info.copy()[ncols_all]
            h_rs_small = h_rs_array.copy()[0, h_small_cols]

            t2 = time.time()
            for boxes in range(v_info_small.shape[0]) :
                v_info_small.loc[boxes, '1' : '63'] = (v_info_small.loc[boxes, '1' : '63'] - h_rs_small[0].tolist()) ** 2
                v_info_small.loc[boxes, 'sum'] = sum(v_info_small.loc[boxes, '1' : '63'])
            t4 = time.time()

            v_info_small = v_info_small.sort_values(by = ['sum'])
            v_info_small.reset_index(drop = True, inplace = True)
            choice = random.randrange(0, cho)
            choice = 0

            os.chdir(tiledir)
            tile = Image.open(v_info_small.loc[choice, 'tilename'])
            tile.show()
            tile = tile.convert('RGBA')
            os.chdir(os.path.join(plot_dir, 'test'))
            tile.save(f'{index}.png')

            tile = tile.resize((interval, interval), Image.BILINEAR)
            canvas.paste(tile, (left_x, left_y))
            smpl.paste(tile, (left_x, left_y))
            print(f"{v_info_small.loc[choice, 'tilename']}")
            v_info_small = None
            if index == 850 :
                break
            t8 = time.time()
            remaining_time = round(((total - index) * (t8 - start)) / 60, 1)
            print(f'{index} done, {round(index / total * 100, 2)}%, {round(t8 - start, 2)}sec, {remaining_time}min remaining')
            
    print(smpl.size)



    os.chdir(plot_dir)
    smpl.save(f'test_lisa_{cho}.jpg')
    canvas.save(f'temp_lisa_{cho}.png')
    dlt.savepng(smpl, plot_dir,f'test_lisa_{cho}.jpg')
    dlt.savepng(canvas, plot_dir, f'temp_lisa_{cho}.png')
