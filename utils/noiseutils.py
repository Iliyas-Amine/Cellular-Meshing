from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from scipy.ndimage import gaussian_filter
from utils.fileutils import fetch_imgs, _load_noise_map
import numpy as np, random, logging
from os import urandom

def _conv_tilemap(matrix):
    logging.info("Starting conversion...")
    noise_map = np.zeros((64, 64))
    above = 1 # if np.count_nonzero(matrix == 1) < np.count_nonzero(matrix == 0) else 0
    below = 0 # if above == 1 else 1

    logging.info("Creating adequate noise matrix...")
    for x in range(64):
        for y in range(64):
            if matrix[x, y] == above: 
                noise_map[x, y] = random.uniform(0.25, 1)  
            elif matrix[x, y] == below: 
                noise_map[x, y] = random.uniform(-1, -0.25) 
    logging.debug(f"Noise Matrix: {noise_map}")

    logging.info("Smoothing the noise matrix")
    smoothed_noise_map = gaussian_filter(noise_map, sigma=2)

    logging.debug(f"Smooth Noise Matrix: {smoothed_noise_map}")

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


def _join_tiles(grid_size):
    contrast_factor = 1.1
    noise_grid = Image.new('RGB', (grid_size*64, grid_size*64))
    tiles = fetch_imgs('tiles')

    random.shuffle(tiles)
    for i in range(grid_size):
        for j in range(grid_size):
            noise_grid.paste(tiles[i*grid_size + j], (j * 64, i * 64))

    noise_grid = noise_grid.filter(ImageFilter.GaussianBlur(radius=16))
    enhancer = ImageEnhance.Contrast(noise_grid)
    noise_grid = enhancer.enhance(contrast_factor)
    noise_grid = noise_grid.filter(ImageFilter.UnsharpMask(radius=32, percent=100))
    noise_grid = noise_grid.resize((512, 512), Image.LANCZOS)
    noise_grid.save(f'noises/noise_g{grid_size}_{urandom(4).hex()}.png')


def stacking():
    noise_sum = np.zeros((512, 512))
    noise_maps = []
    layers = fetch_imgs('noises')
    for img in layers:
        noise_maps.append(_load_noise_map(img))
        
    pattern = [0.4, 0.3, 0.15, 0.1, 0.05]
    for index, percentile in enumerate(pattern):
        noise_sum = noise_sum + noise_maps[index] * percentile
    noise_map = Image.new('L', (512, 512))
    draw = ImageDraw.Draw(noise_map)
    for x in range(0, 512):
        for y in range(0, 512):
            z_value = int(np.clip(noise_sum[x, y], 0, 255))
            draw.rectangle([(x, y), (x, y)], fill=z_value)
    noise_map.save(f"fnoises/noise_f_{urandom(4).hex()}.png")