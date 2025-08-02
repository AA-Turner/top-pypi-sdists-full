import logging

from project.core.util import setup_logging

_logger = logging.getLogger(__name__)


def __command():
    setup_logging()
    _logger.info("logging is good")


if __name__ == '__main__':
    __command()
