# canonmap/utils/logger.py

import logging

from rich.logging import RichHandler

def configure_logging(level: str = "INFO") -> None:
    """
    Call once, very early in your program.
    The force=True parameter makes sure basicConfig replaces existing handlers.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(show_time=False, markup=True)],
        force=True,
    )


def configure_logging_decorator(level: str = "INFO"):
    """
    Decorator version of configure_logging.
    Usage: @configure_logging_decorator("INFO")
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            configure_logging(level)
            return func(*args, **kwargs)
        return wrapper
    return decorator