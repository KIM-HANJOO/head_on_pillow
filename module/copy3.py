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

'''
info
each tile is 32 * 32,
in the tilesets assume that each tile is 16 * 16
