from concurrent.futures import ProcessPoolExecutor, wait
from utils.noiseutils import _conv_tilemap, _join_tiles
from utils.fileutils import fetch_imgs
from utils.meshutils import _gen_mesh
from utils.tilegen import _gen_pop
import logging


def _gen_tile():
    logging.info("Generating a single tile...")
    matrix = _gen_pop()
    logging.debug(f"Matrix: {matrix}")
    _conv_tilemap(matrix)
    logging.info("Generated tile")


def gen_tiles():
    n = 64
    logging.info("Generating {n} tiles...")
    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(_gen_tile) for _ in range(n)]
        wait(futures)
    logging.info("All {n} tiles generated")


def gen_noises():
    logging.info("Generating noise maps...")
    argl = [2, 4, 8, 8, 8]
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(_join_tiles, gs) for gs in argl]
        wait(futures)
    logging.info("All 5 noise maps generated")


def gen_meshes():
    logging.info("Generating VTK meshes...")
    imgs = fetch_imgs('fnoises')
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(_gen_mesh, img) for img in imgs]
        wait(futures)
    logging.info(f"All {len(imgs)} VTK meshes generated")