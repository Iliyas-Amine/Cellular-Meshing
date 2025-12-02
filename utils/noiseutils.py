from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from scipy.ndimage import gaussian_filter, zoom
from utils.fileutils import fetch_imgs, _load_noise_map
import numpy as np, random, logging
from os import urandom
from utils.config import (GRID_SIZE, SIGMA, BLUR_RADIUS, UNSHARP_RADIUS, UNSHARP_PERCENT, SAVE, RESIZE, CONTRAST_FACTOR, PATTERN)

def _conv_tilemap(matrix):
    logging.info("Starting conversion...")

    noise_map = np.zeros((GRID_SIZE, GRID_SIZE))

    # TODO: Make a mask instead of an above and below and the loop
    above = 1 if np.count_nonzero(matrix == 1) < np.count_nonzero(matrix == 0) else 0
    below = 0 if above == 1 else 1

    logging.info("Creating adequate noise matrix...")
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if matrix[x, y] == above: 
                noise_map[x, y] = random.uniform(0.25, 1)  
            elif matrix[x, y] == below: 
                noise_map[x, y] = random.uniform(-1, -0.25) 

    logging.debug(f"Noise Matrix: {noise_map}")

    logging.info("Smoothing the noise matrix")

    smoothed_noise_map = gaussian_filter(noise_map, sigma=SIGMA)

    logging.debug(f"Smooth Noise Matrix: {smoothed_noise_map}")

    if SAVE:
        logging.info("Converting matrix to image")
        noise_image = Image.new('L', (64, 64))
        draw = ImageDraw.Draw(noise_image)
        for x in range(0, 64):
            for y in range(0, 64):
                z_value = smoothed_noise_map[x, y]
                color = int((z_value + 1) * 127.5)
                draw.rectangle([(x, y), (x, y)], fill=color)

        logging.info("Applying contrast...")
        contrast_factor = 1.4
        noise_image = ImageEnhance.Contrast(noise_image).enhance(contrast_factor)
        logging.info("Saving noise tile...")
        noise_image.save(f"tiles/tile_{urandom(8).hex()}.png")
    
    return smoothed_noise_map

def _bipolar_map(matrix):
    noise_map = np.zeros((64, 64))
    above = 0
    below = 1
    for x in range(64):
        for y in range(64):
            if matrix[x, y] == above: 
                noise_map[x, y] = 1
            elif matrix[x, y] == below: 
                noise_map[x, y] = -1
    noise_image = Image.new('L', (64, 64))
    draw = ImageDraw.Draw(noise_image)
    for x in range(0, 64):
        for y in range(0, 64):
            z_value = noise_map[x, y]
            color = int((z_value + 1) * 127.5)
            draw.rectangle([(x, y), (x, y)], fill=color)
    noise_image.save(f"tiles/tile_{urandom(8).hex()}.png")


def _join_tiles(multiplier, tiles):
    current_size = multiplier*GRID_SIZE

    noise_grid = np.zeros((current_size, current_size), dtype=np.float64)

    random.shuffle(tiles)
    for i in range(multiplier):
        for j in range(multiplier):
            tile_idx = i * multiplier + j
            if tile_idx < len(tiles):
                y_start, y_end = i * GRID_SIZE, (i + 1) * GRID_SIZE
                x_start, x_end = j * GRID_SIZE, (j + 1) * GRID_SIZE
                noise_grid[y_start:y_end, x_start:x_end] = tiles[tile_idx]

    noise_grid = gaussian_filter(noise_grid, sigma=BLUR_RADIUS)
    noise_grid = noise_grid * CONTRAST_FACTOR
    noise_grid = np.clip(noise_grid, -1.0, 1.0)

    blurred_mask = gaussian_filter(noise_grid, sigma=UNSHARP_RADIUS)
    mask = noise_grid - blurred_mask
    amount = UNSHARP_PERCENT / 100.0 if UNSHARP_PERCENT > 1 else UNSHARP_PERCENT
    noise_grid = noise_grid + (mask * amount)
    noise_grid = np.clip(noise_grid, -1.0, 1.0)

    zoom_ratio = RESIZE / current_size

    noise_grid = zoom(noise_grid, zoom_ratio, order=3)

    if SAVE:
        normalized_grid = ((noise_grid + 1) / 2.0) * 255.0
        img_data = normalized_grid.astype(np.uint8)
        
        img_obj = Image.fromarray(img_data, mode='L')
        
        filename = f'noises/noise_g{multiplier}_{urandom(4).hex()}.png'
        img_obj.save(filename)

    return noise_grid


def stacking(noises):
    noise_sum = np.zeros((RESIZE, RESIZE), dtype=np.float32)

    for grid, weight in zip(noises, PATTERN):
        noise_sum += grid * weight

    if SAVE:
        normalized = ((noise_sum + 1) / 2.0) * 255.0
        img_data = np.clip(normalized, 0, 255).astype(np.uint8)
        noise_map = Image.fromarray(img_data, mode='L')
        
        filename = f"fnoises/noise_f_{urandom(4).hex()}.png"
        noise_map.save(filename)

    return noise_sum * 255
