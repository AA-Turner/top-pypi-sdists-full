import asyncio
import logging

from arpakitlib.ar_logging_util import init_log_file
from project.core.settings import get_cached_settings

_logging_was_setup: bool = False


def setup_logging():
    global _logging_was_setup
    if _logging_was_setup:
        return

    if get_cached_settings().log_filepath:
        init_log_file(log_filepath=get_cached_settings().log_filepath)

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

    if get_cached_settings().log_filepath:
        file_handler = logging.FileHandler(get_cached_settings().log_filepath)
        file_handler.setLevel(logging.WARNING)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%d.%m.%Y %I:%M:%S%p"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    _logging_was_setup = True

    logger.info("normal logging was setup")


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
