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

ex_16 = os.path.join(tilesets_dir, 'tilesets_extended_16x16')
ex_32 = os.path.join(tilesets_dir, 'tilesets_extended_32x32')
ex_64 = os.path.join(tilesets_dir, 'tilesets_extended_64x64')
ex_96 = os.path.join(tilesets_dir, 'tilesets_extended_96x96')
ex_800 = os.path.join(tilesets_dir, 'tilesets_extended_800x800')

test_dir = os.path.join(tilesets_dir, 'test')


sys.path.append(module_dir)
import discordlib_pyplot as dlt
import image_module as im

'''
info
each tile is 32 * 32,
in the tilesets assume that each tile is 16 * 16

tile_set_1 : 128 * 40 : (16, 5)
tile_set_2 : 128 * 48 : (16, 6)
tile_set_4 : 128 * 48 : (16, 6)
tile_set_6 : 128 * 40 : (16, 5)
tile_set_7 : 128 * 48 : (16, 6)
tile_set_8 : 128 * 48 : (16, 6)
tile_set_9 : 128 * 48 : (16, 6)
tile_set_0A : 128 * 48 : (16, 6)
tile_set_0B : 128 * 48 : (16, 6)
tile_set_0C : 128 * 48 : (16, 6)
tile_set_0D : 128 * 40 : (16, 5)
tile_set_0E : 128 * 48 : (16, 6)
tile_set_10 : 128 * 40 : (16, 5)
tile_set_11 : 128 * 40 : (16, 5)
tile_set_12 : 128 * 16 : (16, ?)

'''


# make list of tilesets to add
name_list = ['0A', '01', '09', '10', '11']
tileset_list = []
for item in name_list :
    tileset_list.append(f'Pokemon_RBY_Tile_Set_{item}.png')
    print(f'adding... Pokemon_RBY_Tile_Set_{item}.png')


tileset_list = os.listdir(org_tilesets_dir)


#print(16 * (25 + 54))
# load tilesets and print tileset size info
for tileset in os.listdir(org_tilesets_dir) :
    if '.png' in tileset :
        os.chdir(org_tilesets_dir)

        tiles, tiles_draw, tiles_width, tiles_height, h, s, v = im.load_img(tileset)
        print(f'{tileset[12 : -4]} : ({tiles_width}, {tiles_height})')

# add grid to tilesets (crop lines)

    
for tileset in os.listdir(org_tilesets_dir) :
    if tileset in tileset_list :
        interval = 8
        multi = 10
        gap = 0

        n_interval = interval * multi
        os.chdir(org_tilesets_dir)
        tiles, tiles_draw, tiles_width, tiles_height, h, s, v = im.load_img_resize(tileset, multi)

        image, draw = im.get_draw(tiles_width, tiles_height, None)

        box_info, side_width, side_height = im.grid_rectangle(tiles_draw, tiles_width, tiles_height, n_interval, gap, 'red')
        
        if int(box_info.shape[0] != (tiles_width / (interval * multi)) * (tiles_height / (interval * multi))) :
                print('wrong slice\n' * 30)
        else :
            print(box_info.shape[0], (tiles_width / (interval * multi)),  (tiles_height / (interval * multi)))
                

        #dlt.savepng(tiles, grid_tilesets_dir,  f'{tileset[12 : -4]}_grid.png')

# crop tilesets


# make dataframe, log for v values
#cols = ['tilename']
#for i in range(1, 65) :
#    cols.append(str(i))
#hsv_df = pd.DataFrame(columns = cols)
#df_num = 0 
#
## write in dataframe
#for number, tileset in enumerate(os.listdir(org_tilesets_dir)) :
#    if tileset in tileset_list :
##    if ('.png' in tileset) & ('12' not in tileset) :
#        interval = 8
#        gap = 0
#
#        os.chdir(org_tilesets_dir)
#        tiles, tiles_draw, tiles_width, tiles_height, h, s, v = im.load_img(tileset)
#
#        box_info, side_width, side_height = im.grid_rectangle(tiles_draw, tiles_width, tiles_height, interval, gap, None)
#
#        for tile_num in range(box_info.shape[0]) :
#            tile_name = f'{tileset[12 : -4]}_{tile_num}.png'
#            crop_range = box_info[tile_num, :].tolist()
#
#            crop_tile_org = tiles.crop(tuple(crop_range))
#            
#            crop_tile_org = crop_tile_org.convert('RGBA')
#            crop_background = Image.new('RGBA', crop_tile_org.size, 'white')
#            crop_background.paste(crop_tile_org, mask = crop_tile_org)
#            #crop_background.paste(crop_tile_org, (0, 0))
#            crop_tile = crop_background.convert('RGB')
#            print(crop_tile.size)
#
#            crop_hsv = crop_tile.convert('HSV')
#            h, s, v = crop_hsv.split()
#            v = np.array(v).transpose()
#            ave = v.sum() / (v.shape[0] * v.shape[1]) 
#            #if (ave < 200) & (ave > 60) :
#            print(v.shape)
#            if ave < 1000 :
#
#                os.chdir(os.path.join(tilesets_dir, 'tilesets_split'))
#                crop_tile.save(tile_name)
#                hsv_df.loc[df_num, 'tilename'] = tile_name #                hsv_df.loc[df_num, '1' : '64'] = v.reshape(1, 64)[0].tolist() #                df_num += 1 #            else :
#                os.chdir(os.path.join(tilesets_dir, 'tilesets_excepts'))
#                crop_tile.save(f'!_{tile_name}')
#                pass
#                #print('white/black tile')
#            #dlt.savepng(crop_tile, os.path.join(tilesets_dir, 'tilesets_split'), f'{tileset[12 : -4]}_{tile_num}.png')
#            if number == 1 :
#                dlt.savepng(crop_tile, test_dir, 'test.png')
#
#
#os.chdir(tilesets_dir)
#hsv_df.to_excel('tilesets_v_info.xlsx')
#
#for number, tile_name in enumerate(os.listdir(split_tilesets_dir)) :
#    for mult in [2, 4, 12, 100] :
#        # load 16x16 sixed tile image
#        os.chdir(split_tilesets_dir)
#        tile = Image.open(tile_name)
#
#        # make canvas with extended size
#        tile_ex = Image.new('RGBA', size = (mult * tile.size[0], mult * tile.size[1]), color = 'white')
#        draw_ex = ImageDraw.Draw(tile_ex)
#
#        # get rgb by array type
#        tile_rgb = tile.convert('RGB')
#        print('tile_rgb size is ', tile_rgb.size)
#        print('tile size is', tile.size)
#        #print(tile_rgb)
#        #tile_rgb = np.array(tile_rgb)
#        #print(tile_rgb.shape)
#
#        # make extended_rgb_array
#        ex_size = (mult * tile.size[0], mult * tile.size[1])
#        #ex_rgb_array = np.zeros(ex_size)
#
#        # add rgb values to extended_rgb_array
#        for x in range(tile.size[0]) :
#            for y in range(tile.size[1]) :
#                r, g, b = tile_rgb.getpixel((x, y))
#                temp_paste = Image.new('RGBA', (mult, mult), color = (r, g, b))
#                tile_ex.paste(temp_paste, (mult * x, mult * y))
#                print(f'x = {x}, = {y}')
#                print(f'r, g, b value is found, {r, g, b}')
#                print(f'made {(mult, mult)} size of temp_paste')
#                print(f'pasted on to {(mult * x, mult * y)}, where size is {ex_size}')
#                print('#####################')
#
#
#        os.chdir(locals()[f'ex_{ex_size[0]}'])
#        tile_ex.save(f'{tile_name[ : -4]}_{ex_size[0]}x{ex_size[1]}.png')
#        print(f'{tile_name[ : -4]}_{ex_size[0]}x{ex_size[1]}.png saved')
#
#        if (number > 80) & (number < 100) :
#            if mult == 100 :
#                dlt.savepng(tile_ex, test_dir, f'{tile_name[ : -4]}_{ex_size[0]}x{ex_size[1]}.png')
#
#
#
