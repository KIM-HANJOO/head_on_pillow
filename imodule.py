from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import imodule as imd
import numpy as np
import sys

from pydub import AudioSegment
from PIL import Image, ImageDraw


def working_area(square, width_, height_, horizontal_buffer, vertical_buffer, \
				width_interval, height_interval, visualize) :
	
	x0 = width(square[0])
	y0 = height(square[1])
	x1 = width(square[2])
	y1 = height(square[3])
	
	x0 += horizontal_buffer
	x1 += -1 * horizontal_buffer
	y0 += vertical_buffer
	y1 += -1 * vertical_buffer
	
	square = [x0, y0, x1, y1]
	
	if visualize == 1 :
		color = 'red'
	else :
		color = 'black'
		
	# adjust width_interval
	
	print('original width, width_interval = {}, {}'.format(width, width_interval))
	
	box_num_x = ((x1 - x0 + width_interval) / (width_ + width_interval)) // 1
	if box_num_x != 1 :
		width_interval = (x1 - x0 - box_num_x * width_) / (box_num_x - 1)
	else :
		print('error : box number(x) must be bigger than 1')
	
	box_num_y = ((y1 - y0 + height_interval) / (height_ + height_interval)) // 1
	if box_num_y != 1 :
		height_interval = (y1 - y0 - box_num_y * height_) / (box_num_y - 1)
	else :
		print('error : box number(y) must be bigger than 1')
	
	print('adjusted width, width_interval = {}, {}'.format(width, width_interval))
	
	# make workboxes
	box_left_x = [x0]
	box_left_y = [y0]
	
	x = x0
	y = y0
	
	while x + width_ < x1 :
		x += width_ + width_interval
		box_left_x.append(x)
		
	while y + height_ < y1 :
		y += height_ + height_interval
		box_left_y.append(y)
		
	print(x0, x1, min(box_left_x), max(box_left_x), width_, width_interval)
	print(y0, y1, min(box_left_y), max(box_left_y), height_, height_interval)
		
	box_xy = np.array([[0, 0, 0, 0]])

	for i in range(len(box_left_x)) :
		for j in range(len(box_left_y)) :
			xx0 = box_left_x[i]
			yy0 = box_left_y[j]
			xx1 = xx0 + width_
			yy1 = yy0 + height_
			
			box_xy = np.append(box_xy, [[xx0, yy0, xx1, yy1]], axis = 0)
	print(box_xy)
	print(width_, width_interval, height_, height_interval)
	box_xy = box_xy[1 :]
	
	return box_xy
	

def grid(draw, square, interval, color) :
	
	x0 = width(square[0])
	y0 = height(square[1])
	x1 = width(square[2])
	y1 = height(square[3])
	
	xvalues = [x0]
	yvalues = [y0]
	
	x = x0
	y = y0
	
	while x < x1 :
		x += width(interval)
		xvalues.append(x)
		
	while y < y1 :
		y += height(interval)
		yvalues.append(y)
	
	for x in xvalues :
		draw.line(((x, y0), (x, y1)), fill = color)
		
	for y in yvalues :
		draw.line(((x0, y), (x1, y)), fill = color)
		

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

class Waveform(object):
    bar_count = 648
    db_ceiling = 60

    def __init__(self, filename):
        self.filename = filename

        audio_file = AudioSegment.from_file(
            self.filename, self.filename.split('.')[-1])

        self.peaks = self._calculate_peaks(audio_file)

    def _calculate_peaks(self, audio_file):
        """ Returns a list of audio level peaks """
        chunk_length = len(audio_file) / self.bar_count

        loudness_of_chunks = [
            audio_file[i * chunk_length: (i + 1) * chunk_length].rms
            for i in range(self.bar_count)]

        max_rms = max(loudness_of_chunks) * 1.00

        return [int((loudness / max_rms) * self.db_ceiling)
                for loudness in loudness_of_chunks]

    def _get_bar_image(self, size, fill):
        """ Returns an image of a bar. """
        bar = Image.new('RGBA', size, fill)

        return bar

    def _generate_waveform_image(self):
        """ Returns the full waveform image """
        bar_width = 4
        px_between_bars = 1
        offset_left = 4
        offset_top = 4

        width = ((bar_width + px_between_bars) * self.bar_count) + (offset_left * 2)
        height = (self.db_ceiling + offset_top) * 2

        im = Image.new('RGBA', (width, height), '#ffffff00')
        for index, value in enumerate(self.peaks, start=0):
            column = index * (bar_width + px_between_bars) + offset_left
            upper_endpoint = (self.db_ceiling - value) + offset_top

            im.paste(self._get_bar_image((bar_width, value * 2), '#333533'),
                     (column, upper_endpoint))

    def save(self):
        """ Save the waveform as an image """
        png_filename = self.filename.replace(
            self.filename.split('.')[-1], 'png')
        with open(png_filename, 'wb') as imfile:
            self._generate_waveform_image().save(imfile, 'PNG')
        return png_filename
