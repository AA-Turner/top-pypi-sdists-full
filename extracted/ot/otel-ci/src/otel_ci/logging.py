import logging

logger = logging.getLogger("otel-cli")


def configure_logging(verbosity_level: int) -> None:
    if verbosity_level == 0:
        logging.basicConfig(level=logging.WARNING)
    elif verbosity_level == 1:
        logging.basicConfig(level=logging.INFO)
    elif verbosity_level >= 2:
        logging.basicConfig(level=logging.DEBUG)
