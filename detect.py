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


# RESIZE IMAGE
def resize_image(original_image):
	width = 720
	height = int(original_image.shape[0] * width / original_image.shape[1])
	dim = (width, height)
	return cv2.resize(original_image, dim, interpolation=cv2.INTER_AREA)


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
