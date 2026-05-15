"""
Centralized logging configuration for matrice_common.

Applications should call configure_logging() once at startup so that
LOG_LEVEL controls verbosity (e.g. WARNING in production, DEBUG in dev).
"""

import logging
import os


def configure_logging() -> None:
    """
    Configure the root logger from the LOG_LEVEL environment variable.

    Call once at application startup. If the root logger already has
    handlers, this is a no-op to avoid duplicate configuration.

    Environment
    -----------
    LOG_LEVEL : str, optional
        One of DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is WARNING
        so that debug/info output is silent in production.
    """
    root = logging.getLogger()
    if root.handlers:
        return
    level_name = os.getenv("LOG_LEVEL", "WARNING").upper()
    level = getattr(logging, level_name, logging.WARNING)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
