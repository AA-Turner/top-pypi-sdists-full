import logging


class Logging:

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("debug.log"),
                logging.StreamHandler()
            ]
        )

    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        logging.info(msg)
