from utils.fileutils import delete_files
import utils.multprocutils as multprocutils, logging
from utils.noiseutils import stacking
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
                    filename=f"logs/{time.asctime()}.log")

def run():
    logging.info("Program start")
    delete_files(['noises', 'meshes', 'fnoises', 'tiles'])
    multprocutils.gen_tiles()
    multprocutils.gen_noises()
    stacking()
    for _ in range(4):
        delete_files(['noises'])
        multprocutils.gen_noises()
        stacking()
    multprocutils.gen_meshes()
    logging.info("Program exit")


if __name__ == "__main__":
    begin = time.time()
    run()
    end = time.time()
    logging.info(f"Time in seconds: {end-begin}s")