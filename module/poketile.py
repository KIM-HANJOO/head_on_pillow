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
grid_tilesets_Dir = os.path.join(tilesets_dir, 'tilesets_grid')

sys.path.append(module_dir)
import discordlib_pyplot as dlt
import image_module as im
import random

'''
info
each tile is 32 * 32,
in the tilesets assume that each tile is 16 * 16
'''
interval = 8
gap = 0

img_name = 'mona_lisa.jpg'
greyscaled_multiplier = 0.3
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
        if index > 540 :
            start = time.time()
            left_x = int(smpl_info[index, 0])
            right_x = int(smpl_info[index, 2])
            left_y = int(smpl_info[index, 1])
            right_y = int(smpl_info[index, 3])

            h_array = v_smpl[left_x : right_x, left_y : right_y]
            
            ncols = ['tilename', 'sum', '1', '5', '8', '33', '37', '39', '56', '60', '63']
            print(v_info.columns)

            v_df = v_info.copy()[ncols]
            print(v_df.columns)

            t2 = time.time()
            for boxes in range(v_df.shape[0]) :
                t3 = time.time()
                v_df.loc[boxes, '1' : '63'] = (v_df.loc[boxes, '1' : '63'] - h_array.reshape(1, 256)[0].tolist()) ** 2
                t4 = time.time()
                v_df.loc[boxes, '1' : '256'] = np.absolute(v_df.loc[boxes, '1' : '256'] - h_array.reshape(1, 256)[0].tolist())
                t5 = time.time()
                v_df.loc[boxes, 'sum'] = sum(v_df.loc[boxes, '1' : '256'])
                t6 = time.time()
                print(f'{boxes} to {v_df.shape[0]}', end = '\r')
                print(100 * (t4 - t3))
                print(100 * (t5 - t4))
                print('#####################')
            t7 = time.time()
            v_df = v_df.sort_values(by = ['sum'])
            v_df.reset_index(drop = True, inplace = True)
            choice = random.randrange(0, cho)
            #choice = 0

            os.chdir(split_tilesets_dir)
            tile = Image.open(v_df.loc[choice, 'tilename'])
            tile.show()
            tile = tile.convert('RGBA')
            os.chdir(os.path.join(plot_dir, 'test'))
            tile.save(f'{index}.png')

            canvas.paste(tile, (left_x, left_y))
            smpl.paste(tile, (left_x, left_y))
            print(f"{v_df.loc[choice, 'tilename']}")
            print(f'{index} done, {index / total * 100}%')
            v_df = None
            if index == 550 :
                break
            t8 = time.time()
            print(100 * ( t8 - t7))
            print('33333333333333333333333333333333')
            
    print(smpl.size)



    os.chdir(plot_dir)
    smpl.save(f'test_lisa_{cho}.jpg')
    canvas.save(f'temp_lisa_{cho}.png')
