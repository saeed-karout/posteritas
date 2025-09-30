# Tilestry story

**Posterity, thou art mine!**

![Banner Image](/img/Bureij.jpg "Byzantine-era mosaic floor discovered under an olive orchard.")
*Early Byzantine mosaic unearthed in [Bureij](https://en.wikipedia.org/wiki/Bureij_mosaic) (Source M.A./AFP).*

### Genesis

> This is just another week-end side project for a draft I was working on. I tinkered with a script that creates a poster image by arranging pictures located in a specified folder into a tiled layout. A good opportunity to tackle the challenge of resizing images to fit a computed grid.

## Table of contents

<details>
<summary>Contents - click to expand</summary>

- [Tilestry story](#tilestry-story)
    - [Genesis](#genesis)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [main functions overview](#main-functions-overview)
    - [correct\_image\_orientation function](#correct_image_orientation-function)
    - [create\_poster functions](#create_poster-functions)
  - [Further learning](#further-learning)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)
  - [Limitations](#limitations)

</details>

## Overview

This script reads images from a given directory, fixes their orientation if necessary, and then arranges them into a poster made to fit an A3 landscape canvas (3508x2480 pixels). Landscape images are resized to fill an allocated grid tile, while portrait images are paired to share a grid tile. The final poster is saved as a single JPEG.
We provide **two modes**:

- An unperfect one, *[serendipitous](https://en.wikipedia.org/wiki/B%C3%AAtise_de_Cambrai)*, that has his charm with its unfilled gaps.
- The second mode fills the gaps and works as it was originally intended.

![Demo Image](/img/poster.gif "graffiti mosaic.")
*Demo with pictures from a [graffiti dataset](https://huggingface.co/datasets/bghira/free-to-use-graffiti/tree/main)*

## Features

- **Automatic orientation correction:** Uses EXIF data to correct the image orientation.
- **Dynamic tiling:** Automatically calculates grid dimensions based on the number of images.
- **Handling portrait & landscape:** Resizes landscape images to fill a tile and pairs portrait images where applicable.
- **Full tile coverage:** Images are cropped so they don't show margins, when sizes do not fit the computed cell.
- **Output in A3 landscape format:** The poster is generated to fit an A3 size (landscape) at 300 DPI.

## Dependencies

- Python 3.x
- Pillow 9.5.0 (PIL fork)

## Installation

1. Ensure you have Python 3 installed.
2. Download the script's folder or clone its repository.
3. If you don't have it yet, install Pillow with pip:

   ```bash
    pip install pillow
    ```

## Usage

1. Place the images you want to include in your poster inside a folder (example: /poster).
2. Modify the `IMAGE_FOLDER` parameter in the script to point to your folder's path if necessary.
3. Choose a mode: `MODE = 'yourmodehere'  # Options: 'mode1', 'mode2', 'both'`
4. Optionally, change the `OUTPUT_FILE` parameter(s) to set the desired output filename(s).
5. Run the script from the command line:

   ```bash
    python posteritas.py
    ```

- Once processed, the poster will be saved as `modeX.jpg` (or your specified output file).

## main functions overview

### correct_image_orientation function

This function checks the EXIF metadata of an image and rotates it accordingly to correct the orientation.

### create_poster functions

The main functions, one for each mode, they:
    - Read images from the specified folder.
    - Correct their orientation.
    - Compute the grid layout based on the number of images.
    - *Mode2* function additionally leaves no pairing gaps between portrait pictures.
    - *Mode2* function additionally randomizes the picture order display.
    - Resize and arrange images into an A3-sized poster.
    - Save the final poster as a JPEG file.

>[!NOTE]
> The mode1 function **leaves gaps** by the end of the process because of a suboptimal pairing. It was left as is (because I actually liked it!) and corrected in the additional mode2.
> See the examples provide above to get a grasp of the differences.

## Further learning

Not necessarily 100% related to this project, but intriguing:

- About the bin packing problem: [link](https://github.com/secnot/rectpack)
- Another type of mosaic: [link](https://github.com/dvdtho/python-photo-mosaic)

## Troubleshooting

- Ensure that the provided `IMAGE_FOLDER` path exists and contains valid image files **(e.g., .png, .jpg, .jpeg, .gif, .bmp)**.
- Check that Pillow is correctly installed if you encounter import errors.

## License

The source code is provided under a Creative Commons CC0 license. See the [LICENSE](/LICENSE) file for details.
Feel free to modify and use the script per your needs.

## Limitations

- The script assumes a fixed A3 canvas size and a basic grid layout; more complex layouts or variable poster sizes require further modifications.
- Pairing of portrait images is basic.
