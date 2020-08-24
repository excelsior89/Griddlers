from matplotlib import image
from itertools import groupby
import numpy as np

import sys

import SvgFuncs


	
def ImageUniqueColours(img_data):
	unique_colours = [tuple(colours) for colours in np.unique(img_data.reshape(-1, img_data.shape[2]), axis=0)]
	unique_colours.sort()
	return unique_colours
	
def NonogramVectorCount(vec):
	return [(k, sum(1 for i in g)) for k, g in groupby(vec)]
	
def NonogramRowCounts(img_data, unique_colours, background_index = -1):
	row_counts = [(0, 0)] * img_data.shape[0]
	for ir in range(img_data.shape[0]):
		if background_index >= 0:
			row_counts[ir] = [v for v in NonogramVectorCount([unique_colours.index(tuple(colours)) for colours in img_data[ir]]) if v[0] != background_index]
		else:
			row_counts[ir] = NonogramVectorCount([unique_colours.index(tuple(colours)) for colours in img_data[ir]])
		
	return row_counts
		
def NonogramColumnCounts(img_data, unique_colours, background_index = -1):
	col_counts = [(0, 0)] * img_data.shape[1]
	for ic in range(img_data.shape[1]):
		if background_index >= 0:
			col_counts[ic] = [v for v in NonogramVectorCount([unique_colours.index(tuple(colours)) for colours in img_data[:,ic].reshape(img_data.shape[0], img_data.shape[2])]) if v[0] != background_index]
		else:
			col_counts[ic] = NonogramVectorCount([unique_colours.index(tuple(colours)) for colours in img_data[:,ic].reshape(img_data.shape[0], img_data.shape[2])])
		
	return col_counts
	
	
# Padding colour must be a 3-tuple of 0-1 range rgb
def NonogramColumnCountsToPixels(nonogram_cols, unique_colours, padding_colour):
	max_nn_cols = max([len(x) for x in nonogram_cols])
	
	column_image_data = np.zeros([max_nn_cols, len(nonogram_cols), 3])
	
	column_text_array = [[None for i in range(len(nonogram_cols))] for i in range(max_nn_cols)]
	
	for ic, col in enumerate(nonogram_cols):
		padding_count = max_nn_cols - len(col)
		
		for ir in range(padding_count):
			column_image_data[ir, ic, :] = padding_colour
			
		for ir, rect_colour in enumerate(col):
			column_image_data[ir + padding_count, ic, :] = unique_colours[rect_colour[0]]
			
			column_text_array[ir + padding_count][ic] = str(rect_colour[1])
		
	return column_image_data, column_text_array
	
# Padding colour must be a 3-tuple of 0-1 range rgb
def NonogramRowCountsToPixels(nonogram_rows, unique_colours, padding_colour):
	max_nn_rows = max([len(x) for x in nonogram_rows])
	
	row_image_data = np.zeros([len(nonogram_rows), max_nn_rows, 3])
	
	row_text_array = [[None for i in range(max_nn_rows)] for i in range(len(nonogram_rows))]
	
	for ir, row in enumerate(nonogram_rows):
		padding_count = max_nn_rows - len(row)
		
		for ic in range(padding_count):
			row_image_data[ir, ic, :] = padding_colour
			
		for ic, rect_colour in enumerate(row):
			row_image_data[ir, ic + padding_count, :] = unique_colours[rect_colour[0]]
			
			row_text_array[ir][ic + padding_count] = str(rect_colour[1])
		
	return row_image_data, row_text_array
	
if __name__ == '__main__':
	# Image path, background colour as hex "#rrggbb" (in quotes), output path, [-s]
	# optional -s tag to generate "solution" griddler with middle data (original image) present
	# load image as pixel array
	img_data = image.imread(str(sys.argv[1]))
	
	background_colour = SvgFuncs.Hex2Rgb(str(sys.argv[2]))
	
	# Discard any alpha
	img_data = img_data[:,:,0:3]
	
	unique_colours = ImageUniqueColours(img_data)
	
	if background_colour not in unique_colours:
		unique_colours.append(background_colour)
		
	background_colour_index = unique_colours.index(background_colour)
	
	nonogram_cols = NonogramColumnCounts(img_data, unique_colours, background_colour_index)
	nonogram_rows = NonogramRowCounts(img_data, unique_colours, background_colour_index)
	
	nonogram_cols_image, nonogram_cols_text = NonogramColumnCountsToPixels(nonogram_cols, unique_colours, unique_colours[background_colour_index])
	nonogram_rows_image, nonogram_rows_text = NonogramRowCountsToPixels(nonogram_rows, unique_colours, unique_colours[background_colour_index])
	
	max_nn_cols = max([len(x) for x in nonogram_cols])
	max_nn_rows = max([len(x) for x in nonogram_rows])

	horizontal_max = max_nn_rows
	vertical_max = max_nn_cols
	nx = img_data.shape[1]
	ny = img_data.shape[0]
	spacing = 5

	with open(str(sys.argv[3]), 'w') as fp_svg:
		fp_svg.write(SvgFuncs.XmlHeader())
		fp_svg.write('\n')
		fp_svg.write(SvgFuncs.SvgA4Header())
		fp_svg.write('\n')
		
		if (len(sys.argv) > 4) and (str(sys.argv[4]) == '-s'):
			fp_svg.write(SvgFuncs.SvgPixelGrid((horizontal_max + 1) * spacing, (vertical_max + 1) * spacing, spacing, 'pxgrid', img_data))
			fp_svg.write('\n')
		
		fp_svg.write(SvgFuncs.SvgPixelGrid((horizontal_max + 1) * spacing, 0, spacing, 'pxcolclues', nonogram_cols_image))
		fp_svg.write('\n')
		
		fp_svg.write(SvgFuncs.SvgTextPixelGrid((horizontal_max + 1) * spacing, 0, spacing, 'textcolclues', nonogram_cols_text, nonogram_cols_image))
		fp_svg.write('\n')
		
		fp_svg.write(SvgFuncs.SvgPixelGrid(0, (vertical_max + 1) * spacing, spacing, 'pxrowclues', nonogram_rows_image))
		fp_svg.write('\n')
		
		fp_svg.write(SvgFuncs.SvgTextPixelGrid(0, (vertical_max + 1) * spacing, spacing, 'textrowclues', nonogram_rows_text, nonogram_rows_image))
		fp_svg.write('\n')
		
		fp_svg.write(SvgFuncs.SvgGrid((horizontal_max + 1) * spacing, 0, nx, vertical_max, spacing, 'vclues', 5, 0))
		fp_svg.write('\n')
		fp_svg.write(SvgFuncs.SvgGrid(0,(vertical_max + 1) * spacing, horizontal_max, ny, spacing, 'hclues', 0, 5))
		fp_svg.write('\n')
		fp_svg.write(SvgFuncs.SvgGrid((horizontal_max + 1) * spacing, (vertical_max + 1) * spacing, nx, ny, spacing, 'grid', 5, 5))
		fp_svg.write('\n')
		fp_svg.write('</svg>')


