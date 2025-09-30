#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File name: posteritas.py
# Author: Ma 3443
# Date created: 2025-04-27
# Version = "1.0"
# License =  "CC0 1.0"
# =============================================================================
""" This script script loads images from a folder, corrects their orientation 
using EXIF data, and creates either a near-square grid poster (mode1) 
or a full-coverage mosaic poster (mode2) or both."""
# =============================================================================

# Imports
import os
import random
from math import ceil, sqrt
from typing import List, Tuple, Union
from PIL import Image, ExifTags

# Constants
POSTER_SIZE = (3508, 2480) #A3 size @300dpi
VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')


# ---------------------------------------------------------------------------
# Functions
def correct_image_orientation(img: Image.Image) -> Image.Image:
    """
    Correct the orientation of the image using EXIF data.

    Args:
        img (Image.Image): The input image.

    Returns:
        Image.Image: The image with corrected orientation.
    """
    try:
        orientation_tag = next(
            (tag for tag, value in ExifTags.TAGS.items() if value == 'Orientation'),
            None
        )
        exif = img._getexif()
        if exif is not None and orientation_tag is not None:
            orientation = exif.get(orientation_tag)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except Exception as e:
        print(f"Error correcting orientation: {e}")
    return img


def load_images(image_folder: str) -> List[Image.Image]:
    """
    Load images from a folder and apply orientation correction.

    Args:
        image_folder (str): Path to the folder containing images.

    Returns:
        List[Image.Image]: A list of PIL Image objects.
    """
    images: List[Image.Image] = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(VALID_EXTENSIONS):
            path = os.path.join(image_folder, filename)
            try:
                with Image.open(path) as img:
                    corrected_img = correct_image_orientation(img)
                    images.append(corrected_img.copy())
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    if not images:
        print("No images loaded!")
    return images


def cover_image(img: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """
    Resize the image in 'cover' mode: scale and crop so that the image fills the target dimensions.

    Args:
        img (Image.Image): The input image.
        target_width (int): Target width.
        target_height (int): Target height.

    Returns:
        Image.Image: The resized and cropped image.
    """
    scale = max(target_width / img.width, target_height / img.height)
    new_width = int(img.width * scale)
    new_height = int(img.height * scale)
    resized = img.resize((new_width, new_height), Image.LANCZOS)
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    return resized.crop((left, top, left + target_width, top + target_height))


def create_poster_mode1(images: List[Image.Image], output_file: str, poster_size: Tuple[int, int] = POSTER_SIZE) -> None:
    """
    Create a near-square grid poster.
    Landscape images fill a grid cell, and portrait images are paired together in a cell.

    Args:
        images (List[Image.Image]): List of images to include.
        output_file (str): Path to save the created poster.
        poster_size (Tuple[int, int], optional): Dimensions of the poster. Defaults to POSTER_SIZE.
    """
    poster_width, poster_height = poster_size
    num_images = len(images)
    if num_images == 0:
        print("No images found for Mode 1.")
        return

    # Calculate grid dimensions approximating a square
    cols = int(num_images**0.5)
    rows = ceil(num_images / cols)
    cell_width = poster_width // cols
    cell_height = poster_height // rows

    print(
        f"Grid: {cols} cols x {rows} rows. Cell size: {cell_width}x{cell_height}")

    poster = Image.new('RGB', poster_size, (0, 0, 0))
    portrait_images = [img for img in images if img.width < img.height]
    portrait_index = 0
    index = 0

    for row in range(rows):
        for col in range(cols):
            if index >= num_images:
                break
            x = col * cell_width
            y = row * cell_height
            img = images[index]
            # For landscape and square images
            if img.width >= img.height:
                poster.paste(img.resize(
                    (cell_width, cell_height), Image.LANCZOS), (x, y))
            else:
                # For portrait images, fill half the cell; try pairing if available.
                half_width = cell_width // 2
                poster.paste(img.resize(
                    (half_width, cell_height), Image.LANCZOS), (x, y))
                if portrait_index + 1 < len(portrait_images):
                    second_img = portrait_images[portrait_index + 1].resize(
                        (half_width, cell_height), Image.LANCZOS)
                    poster.paste(second_img, (x + half_width, y))
                    portrait_index += 2
                else:
                    portrait_index += 1
            index += 1

    poster.save(output_file)
    print(f"Mode 1 poster created and saved as {output_file}")


def create_poster_mode2(images: List[Image.Image], output_file: str, poster_size: Tuple[int, int] = POSTER_SIZE) -> None:
    """
    Create a full-coverage mosaic poster.
    Portrait images are paired, and non-portrait images fill a cell
    with the 'cover' mode ensuring full poster coverage.

    Args:
        images (List[Image.Image]): List of images to include.
        output_file (str): Path to save the mosaic.
        poster_size (Tuple[int, int], optional): Dimensions of the poster. Defaults to POSTER_SIZE.
    """
    poster_width, poster_height = poster_size
    portrait_images = [img for img in images if img.height > img.width]
    non_portrait_images = [img for img in images if img.height <= img.width]

    # Pair portrait images
    paired_portraits: List[Union[Tuple[Image.Image,
                                       Image.Image], Image.Image]] = []
    i = 0
    while i < len(portrait_images):
        if i + 1 < len(portrait_images):
            paired_portraits.append(
                (portrait_images[i], portrait_images[i + 1]))
            i += 2
        else:
            paired_portraits.append(portrait_images[i])
            i += 1

    tiles: List[Union[Tuple[Image.Image, Image.Image], Image.Image]
                ] = paired_portraits + non_portrait_images
    random.shuffle(tiles)
    n = len(tiles)

    cols = ceil(sqrt(n))
    rows = ceil(n / cols)
    cell_width = poster_width // cols
    cell_height = poster_height // rows

    print(
        f"Grid: {cols} cols x {rows} rows. Cell size: {cell_width}x{cell_height}")

    poster = Image.new('RGB', poster_size, (0, 0, 0))
    tile_index = 0

    for row in range(rows):
        for col in range(cols):
            # Calculate cell coordinates
            x = col * cell_width
            y = row * cell_height
            if x + cell_width > poster_width or y + cell_height > poster_height:
                continue
            tile = tiles[tile_index % n]
            tile_index += 1

            if isinstance(tile, tuple):
                # For paired portraits, split cell vertically
                half_width = cell_width // 2
                left_img = cover_image(tile[0], half_width, cell_height)
                poster.paste(left_img, (x, y))
                right_img = cover_image(
                    tile[1], cell_width - half_width, cell_height)
                poster.paste(right_img, (x + half_width, y))
            else:
                poster.paste(cover_image(
                    tile, cell_width, cell_height), (x, y))

    poster.save(output_file)
    print(f"Mode 2 poster created and saved as {output_file}")


# ---------------------------------------------------------------------------
# Main Code
def main(image_folder: str,
         output_file_mode1: str,
         output_file_mode2: str,
         mode: str = 'mode1') -> None:
    """
    Load images and create posters based on the selected mode.

    Parameters:
        image_folder (str): Folder containing images.
        output_file_mode1 (str): Output file path for mode1 poster.
        output_file_mode2 (str): Output file path for mode2 mosaic.
        mode (str, optional): 'mode1', 'mode2', or 'both'. Defaults to 'mode1'.
    """
    images = load_images(image_folder)
    if not images:
        print("No images to process. Exiting...")
        return

    if mode == 'mode1':
        create_poster_mode1(images, output_file_mode1)
    elif mode == 'mode2':
        create_poster_mode2(images, output_file_mode2)
    elif mode == 'both':
        print("Creating Mode 1 poster...")
        create_poster_mode1(images, output_file_mode1)
        print("Creating Mode 2 poster...")
        create_poster_mode2(images, output_file_mode2)
    else:
        print("Invalid mode selected. Choose 'mode1', 'mode2', or 'both'.")


if __name__ == '__main__':
    # Configuration: Set your image folder and output file paths here.
    IMAGE_FOLDER = 'poster_source_images_folder_path' 
    OUTPUT_FILE_MODE1 = 'mode1.jpg'
    OUTPUT_FILE_MODE2 = 'mode2.jpg'
    MODE = 'mode2'  # Options: 'mode1', 'mode2', 'both'

    main(IMAGE_FOLDER, OUTPUT_FILE_MODE1, OUTPUT_FILE_MODE2, MODE)
