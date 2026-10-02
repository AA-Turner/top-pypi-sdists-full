"""Functionality to support standard logging."""

import logging


def debug_on():
    """Turn debugging logging on."""
    logging_on(logging.DEBUG)


_is_logging_on = False


def logging_on(level=logging.WARNING):
    """Turn logging on."""
    global _is_logging_on

    if not _is_logging_on:
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("[%(levelname)s: %(asctime)s :"
                                               " %(name)s] %(message)s",
                                               "%Y-%m-%d %H:%M:%S"))
        console.setLevel(level)
        logging.getLogger("").addHandler(console)
        _is_logging_on = True

    log = logging.getLogger("")
    log.setLevel(level)
    for h in log.handlers:
        h.setLevel(level)


class NullHandler(logging.Handler):
    """Empty handler."""

    def emit(self, record):
        """Record a message."""


def logging_off():
    """Turn logging off."""
    logging.getLogger("").handlers = [NullHandler()]


def get_logger(name):
    """Return logger with null handle."""
    log = logging.getLogger(name)
    if not log.handlers:
        log.addHandler(NullHandler())
    return log
