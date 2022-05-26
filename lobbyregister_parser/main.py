import logging
import os
from lr_extractor import LrExtractor

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)

def run():
    LrExtractor().extract_everything()


if __name__ == "__main__":
    run()
