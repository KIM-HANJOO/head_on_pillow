from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import imodule as imd
import numpy as np
import random

size = [pow(10, 4), pow(10, 4)]
square = [200, 20, 800, 1000] # left x, left y, right x, right y
name = 'temp.png'
grid_color = 'black'

########################################################################

def pos(string, percentage) :
	
	if string == 'width' :
		#length = globals()['width_size']
		length = pow(10, 4)
	elif string == 'height' :
		#length = globals()['height_size']
		length = pow(10, 4)
	else :
		print('wrong string argument, {}'.format(string))
	
	return percentage * (1/1000) * length
		
def width(percentage) :
	exact_pos = pos('width', percentage)
	return exact_pos

def height(percentage) :
	exact_pos = pos('height', percentage)
	return exact_pos
	
########################################################################



# (width, height) 크기의 빈 이미지와
# 그 이미지 위에 도형을 그릴 수 있는 툴


global width_size
global height_size

width_size = size[0]
height_size = size[1]

print('width = {}, height = {}'.format(width_size, height_size))

image = Image.new(mode = 'P', size = (width_size, height_size), color = 'white')
draw = ImageDraw.Draw(image)
draw.rectangle([width(square[0]), width(square[1]), width(square[2]), width(square[3])], fill = None, outline = 'gray', width = 1)
imd.grid(draw, square, 20, grid_color)
box = imd.working_area(square, 100, 270, 500, 500, 40, 230, 1)
for i in range(box.shape[0]) :
	random_size = random.random()
	
	xx0 = box[i].tolist()[0]
	xx1 = box[i].tolist()[2]
	
	y0 = box[i].tolist()[1]
	y1 = box[i].tolist()[3]

	yy0 = ((y1 + y0) / 2) - (y1 - y0) * random_size / 2
	yy1 = ((y1 + y0) / 2) + (y1 - y0) * random_size / 2

	box_temp = [xx0, yy0, xx1, yy1]
	draw.rounded_rectangle(box_temp, fill = (139,0,0), outline = (139,0,0), width = 3, radius = 5)
#draw.ellipse([width(400), height(400), width(600), height(600)], fill = 'black', outline = 'black', width = 2)

box_num = len(box) #box_num == bar_count
wave = imd.Waveform()

print(box_num) # 648


plt.imshow(image)

image.save('{}'.format(name))
print('image saved as {}'.format(name))
