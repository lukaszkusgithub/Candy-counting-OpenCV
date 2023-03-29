import json
from pathlib import Path
from typing import Dict

import click
import cv2
import numpy as np
from tqdm import tqdm

# MASKS
green_low = np.array([32, 0, 0], np.uint8)
green_up = np.array([80, 255, 255], np.uint8)

yellow_low = np.array([15, 150, 100], np.uint8)
yellow_up = np.array([30, 255, 255], np.uint8)

purple_low = np.array([70, 8, 2], np.uint8)
purple_up = np.array([86, 255, 255], np.uint8)

red_low_dark = np.array([0, 100, 0], np.uint8)
red_up_dark = np.array([4, 255, 255], np.uint8)

red_low = np.array([75, 100, 0], np.uint8)
red_up = np.array([180, 255, 255], np.uint8)

remove_purple_low = np.array([0, 0, 0], np.uint8)
remove_purple_up = np.array([255, 205, 215], np.uint8)


# DETECT CIRCLES PARAMS
min_radius = 2
max_radius = 18
param_1 = 500
param_2 = 2.5
dp = 1
minDist = 30
range_size = 3


# CHANGE GAMMA
def gamma_trans(img, gamma):
	gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
	gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
	return cv2.LUT(img, gamma_table)


# CHANGE BRIGHTNESS
def increase_brightness(img, value=30):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)

	lim = 255 - value
	v[v > lim] = 255
	v[v <= lim] += value

	final_hsv = cv2.merge((h, s, v))
	img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return img


# GET ONLY MMS
def get_all_candy(img, green=False, yellow=False, purple=False,
                red=False):
	dark_image = increase_brightness(img, 250)
	dark_image = gamma_trans(dark_image, 0.1)
	dark_image = increase_brightness(dark_image, 0)
	dark_image = gamma_trans(dark_image, 5)
	dark_image_gray = cv2.cvtColor(dark_image, cv2.COLOR_BGR2GRAY)
	smooth = cv2.GaussianBlur(dark_image_gray, (121, 121), 0)
	division = cv2.divide(dark_image_gray, smooth, scale=255)

	if green or purple or yellow:
		_, th_dark = cv2.threshold(division, 250, 255, cv2.THRESH_BINARY_INV)
		dark_image = cv2.bitwise_and(img, img, mask=th_dark)

		if green or purple:
			dark_image = increase_brightness(dark_image, 150)
			dark_image = gamma_trans(dark_image, 0.3)
			dark_image = increase_brightness(dark_image, 0)
			dark_image = gamma_trans(dark_image, 5)

		return dark_image
	elif red:
		_, th_dark = cv2.threshold(division, 240, 255, cv2.THRESH_BINARY_INV)
		dark_image = cv2.bitwise_and(img, img, mask=th_dark)

		return dark_image


# GET COLOR MASK
def get_color_mask(all_mms, mask_low, mask_up):
	hsv_color = cv2.cvtColor(all_mms, cv2.COLOR_BGR2HSV)
	extract_color = cv2.inRange(hsv_color, mask_low,
	                            mask_up)

	median_blur = 7
	extract_color = cv2.medianBlur(extract_color, median_blur)
	kernel_erode = np.ones((3, 3), np.uint8)
	extract_color = cv2.erode(extract_color, kernel_erode, iterations=1)
	color_only = cv2.bitwise_and(all_mms, all_mms,
	                             mask=extract_color)
	return [color_only, extract_color]


# RESIZE IMAGE
def resize_image(original_image):
	width = 720
	height = int(original_image.shape[0] * width / original_image.shape[1])
	dim = (width, height)
	return cv2.resize(original_image, dim, interpolation=cv2.INTER_AREA)


# CHECK PIXELS COLORS
def check_color(color, up, low):
	if color[0][0][0] == color[0][0][1] == color[0][0][2] == 0:
		if not low[0] < color[0][0][0] < up[0]:
			if not low[1] < color[0][0][1] < up[1]:
				if not low[2] < color[0][0][2] < up[2]:
					return False
	return True


# GET PIXEL COLOR
def get_color(image, x, y):
	B = image[x, y][0]
	G = image[x, y][1]
	R = image[x, y][2]
	return cv2.cvtColor(np.uint8([[[B, G, R]]]), cv2.COLOR_BGR2HSV)


# DETECT CIRCLES
def detect_circles(mask, dp, minDist, param_1, param_2, min_radius,
                   max_radius, image, low_boundaries, up_boundaries,
                   range_size, img):
	result = 0
	try:
		minus_counter = 0
		circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp,
		                           minDist,
		                           param1=param_1, param2=param_2,
		                           minRadius=min_radius,
		                           maxRadius=max_radius)
		circles = np.uint16(np.around(circles))

		in_range = False

		for i in circles[0, :]:
			color_to_check = get_color(image, i[1], i[0])

			in_range = check_color(color_to_check, low_boundaries,
			                       up_boundaries)

			for z in range(-range_size, range_size):
				for k in range(-range_size, range_size):
					in_range = check_color(color_to_check, low_boundaries,
					            up_boundaries)
					color_to_check = get_color(image, i[1] + k, i[0] + z)
					if in_range:
						break
				if in_range:
					break

			if not in_range:
				minus_counter += 1

			if in_range:
				cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 1)
				cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 1)

		result = len(circles[0]) - minus_counter

	except:
		result = 0
	return result


def detect(img_path: str) -> Dict[str, int]:
	original_image = cv2.imread(img_path, cv2.IMREAD_COLOR)
	img = resize_image(original_image)

	# TODO: Implement detection method.

	red = 0
	yellow = 0
	green = 0
	purple = 0

	return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}


@click.command()
@click.option('-p', '--data_path', help='Path to data directory', type=click.Path(exists=True, file_okay=False,
                                                                                  path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path),
              required=True)
def main(data_path: Path, output_file_path: Path):
	img_list = data_path.glob('*.jpg')

	results = {}

	for img_path in tqdm(sorted(img_list)):
		fruits = detect(str(img_path))
		results[img_path.name] = fruits

	with open(output_file_path, 'w') as ofp:
		json.dump(results, ofp)


if __name__ == '__main__':
	main()
