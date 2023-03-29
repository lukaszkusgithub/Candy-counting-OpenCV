# **Candy counting**

With technological advances in the area of vision sensors, the need for solutions to automate processes using vision feedback has increased. In addition, scientific developments in image processing algorithms make it possible to extract information such as object quantity, size, location, and orientation from images. One of the applications using image processing is the automatic control of the number of objects on a production line along with the distinction of their class, for example, for sorting them in a further step.


## Description

The algorithm detects and counts the colored candies found in the images. For simplicity, there are only 4 colors of candies in the dataset:
- red
- yellow
- green
- purple

All images were captured "from above," but from different heights and angles. In addition, the images differ in the level of lighting and, of course, the amount of candy.

Below is a sample image from the dataset and the correct detection result for it:

```bash
{
  ...,
  "37.jpg": {
    "red": 2,
    "yellow": 2,
    "green": 2,
    "purple": 2
  },
  ...
}
```

<p align="center">
  <img width="750" height="500" src="./data/37.jpg">
</p>

## Project structure

```bash
.
├── data
│   ├── 00.jpg
│   ├── 01.jpg
│   └── 02.jpg
├── readme_files
├── detect.py
├── README.md
└── requirements.txt
```

The directory [`data`](./data) contains examples, based on which the candy counting algorithm is to be prepared in the file [`detect.py`](./detect.py). The `main` function in the `detect.py` file should remain unchanged. 

### Libraries

Interpreter testujący projekty będzie miał zainstalowane biblioteki w wersjach:
```bash
pip install numpy==1.24.1 opencv-python-headless==4.5.5.64 tqdm==4.64.1 click==8.1.3
```

### Run program

Script `detect.py` takes 2 input parameters:
- `data_path` - path to the folder with data (photos)
- `output_file_path` - path to the file with the results

```bash
$ python3 detect.py --help

Options:
  -p, --data_path TEXT         Path to data directory
  -o, --output_file_path TEXT  Path to output file
  --help                       Show this message and exit.
```

In the Linux console, the script can be called from the project directory as follows:

```bash
python3 detect.py -p ./data -o ./results.json
```
