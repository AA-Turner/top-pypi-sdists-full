from logging import Formatter, Logger, StreamHandler, getLogger
from sys import stderr


def get_logger() -> Logger:
    logger = getLogger("galileo_core")
    handler = StreamHandler(stderr)
    handler.setFormatter(Formatter("%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s"))
    if logger.handlers:
        logger.handlers.clear()
    logger.addHandler(handler)
    return logger


logger = get_logger()
