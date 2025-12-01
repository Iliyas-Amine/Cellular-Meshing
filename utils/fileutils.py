from PIL import Image
import numpy as np, os, glob, logging

def delete_files(folders):
    logging.info("Deleting files...")
    countp = 0
    countv = 0
    for folder in folders:
        pattern1 = os.path.join(folder, '*.png')
        pattern2 = os.path.join(folder, '*.vtk')
        png_files = glob.glob(pattern1)
        vtk_files = glob.glob(pattern2)
        for file in png_files:
            try:
                os.remove(file)
                countp += 1
            except Exception:
                logging.exception(f"Error deleting {file}:")
        for file in vtk_files:
            try:
                os.remove(file)
                countv += 1
            except Exception:
                logging.exception(f"Error deleting {file}:")
    logging.info(f"Deletion done: Deleted {countp} png files and {countv} vtk files")

def fetch_imgs(file_dir):
    imgs = {}
    logging.info(f"Fetching {file_dir}")
    for filename in os.listdir(file_dir):
        if filename.endswith('.png'): 
            img_path = os.path.join(file_dir, filename)
            img = Image.open(img_path)
            imgs[filename] = img
    logging.info("Fetching done")
    myKeys = list(imgs.keys())
    myKeys.sort()
    imgs = {i: imgs[i] for i in myKeys}
    return list(imgs.values())

def _load_noise_map(img):
    logging.info("Loading noise from image...")
    img = img.convert('L')
    noise_map = np.flip(np.rot90(np.array(img)), axis=0)
    logging.info("Loading noise done")
    return noise_map