import logging


def get_logger():
    logging.basicConfig(
        format="[%(threadName)s] %(asctime)s [%(levelname)s]  %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("SpotipyLogger")


logger = get_logger()
