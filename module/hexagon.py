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
def grid_rectangle(draw, width, height, interval, gap) :
    '''
    interval * (n) + gap * (n-1) < width < interval * (n+1) + gap * (n)
    side = width - (interval * n + gap * (n-1))
    '''
    n_width = int(floor((width - interval) / (interval + gap)))
    n_height = int(floor((height - interval) / (interval + gap)))

    side_width = 0.5 * (width - (interval * n_width + gap * (n_width-1)))
    side_height = 0.5 * (height - (interval * n_height + gap * (n_height-1)))

    box_number = n_width * n_heigth
    box_info = np.zeros((box_number, 4))
    start_vertex = [side_width, 
    for index in range(box_number) :
        box_info[index, :] = []


save = 0 

os.chdir(smpl_dir)
smpl = Image.open('pink_panther.jpg')
smpl_width, smpl_height = smpl.size

image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
draw = ImageDraw.Draw(image)
print(smpl_width, smpl_height)

#draw.rectangle([0, smpl_width, 0, smpl_height], fill = None, outline = 'gray', width = 1)


if save == 1 :
    dlt.savepng(image, plot_dir, 'canvas.png')
#    dlt.savepng(smpl, plot_dir, 'pink_panther.png')
