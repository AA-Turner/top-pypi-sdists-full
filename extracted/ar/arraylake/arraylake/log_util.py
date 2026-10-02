import logging
import sys

import structlog

from arraylake import config as config_obj


def get_logger(logger_name):
    """Convenience function to obtain a logger with appropriate settings.
    Logging can be set to DEBUG or INFO using config value / env var:
    ARRAYLAKE_LOG_LEVEL, or config option 'log_level'.

    This function does a little work to return a structlog logger that is
    compatible with direct/cli instantiation and consumption as a library in
    our service.

    If ARRAYLAKE_LOG_LEVEL is unset we return a struclog logger that
    will comply to outside configuration (i.e. server logger configuration).
    Else, we configure a basic logger set to log at ARRAYLAKE_LOG_LEVEL
    and output contents to the console.
    """

    logger = logging.getLogger(logger_name)
    log_level = config_obj.config.get("log_level", "").upper()
    if log_level in ("DEBUG", "INFO"):
        logger.setLevel(getattr(logging, log_level))
        handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(handler)
    return structlog.wrap_logger(logger)
