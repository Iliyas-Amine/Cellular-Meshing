import utils.multprocutils as multprocutils, logging
from utils.noiseutils import stacking
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
                    filename=f"logs/{time.asctime()}.log")

def run():
    t0 = time.time()
    logging.info("Program start")
    tiles = multprocutils.gen_tiles()
    t1 = time.time()
    logging.info(f"Time in seconds: Tile Generation in {t1-t0}s")
    noises = multprocutils.gen_noises(tiles)
    fnoises = list()
    fnoises.append(stacking(noises))
    t2 = time.time()
    logging.info(f"Time in seconds: One Noise Map Generation in {t2-t1}s")
    multprocutils.gen_meshes(fnoises)
    t3 = time.time()
    logging.info(f"Time in seconds: VTK Mesh Generation in {t3-t2}s")
    logging.info(f"Time in seconds: Full Program in {t3-t0}s")
    logging.info("Program exit")


if __name__ == "__main__":
    run()