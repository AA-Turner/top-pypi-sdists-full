# arpakit

import logging
import os
from typing import Optional

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def init_log_file(*, log_filepath: str):
    directory = os.path.dirname(log_filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(log_filepath):
        with open(log_filepath, mode="w") as file:
            file.write("")


_normal_logging_was_setup: bool = False


def setup_normal_logging(log_filepath: Optional[str] = None):
    global _normal_logging_was_setup
    if _normal_logging_was_setup is True:
        return

    if log_filepath:
        init_log_file(log_filepath=log_filepath)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter(
        "%(asctime)s %(msecs)03d | %(levelname)s | %(filename)s | %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%d.%m.%Y %I:%M:%S %p"
    )
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    if log_filepath:
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.WARNING)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%d.%m.%Y %I:%M:%S%p"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    _normal_logging_was_setup = True

    logger.info("normal logging was setup")


def __example():
    pass


if __name__ == '__main__':
    __example()
