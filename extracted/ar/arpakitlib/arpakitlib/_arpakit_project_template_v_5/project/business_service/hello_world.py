import logging

from project.core.util import setup_logging

_logger = logging.getLogger(__name__)


def hello_world() -> str:
    _logger.info("hello world")
    return "Hello world"


if __name__ == "__main__":
    setup_logging()
    hello_world()
