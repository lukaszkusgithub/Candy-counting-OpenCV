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


def detect(img_path: str) -> Dict[str, int]:

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    #TODO: Implement detection method.
    
    red = 0
    yellow = 0
    green = 0
    purple = 0

    return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}


@click.command()
@click.option('-p', '--data_path', help='Path to data directory', type=click.Path(exists=True, file_okay=False, path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path), required=True)
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
