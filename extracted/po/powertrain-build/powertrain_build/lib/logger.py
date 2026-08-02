# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for logging."""
import os
import sys
import logging

LEVEL_NOTSET = 'NOTSET'
LEVEL_DEBUG = 'DEBUG'
LEVEL_INFO = 'INFO'
LEVEL_WARNING = 'WARNING'
LEVEL_ERROR = 'ERROR'
LEVEL_CRITICAL = 'CRITICAL'

LEVELS = {
    LEVEL_NOTSET: logging.NOTSET,
    LEVEL_DEBUG: logging.DEBUG,
    LEVEL_INFO: logging.INFO,
    LEVEL_WARNING: logging.WARNING,
    LEVEL_ERROR: logging.ERROR,
    LEVEL_CRITICAL: logging.CRITICAL
}


def parse_log_level(log_level_name):
    """Convert textual log_level_name to numerical ones defined in logging module."""
    level = log_level_name.upper()
    if level not in LEVELS:
        print(f'Log level "{log_level_name}" invalid, valid list: {", ".join(LEVELS.keys())}', file=sys.stderr)
        level = LEVEL_DEBUG
    return LEVELS[level]


def create_logger(name, handler=None, log_format=None):
    """Create a logger.

    If the handler already have a log format, it will be replaced.

    Args:
        name (str): Name of the logger
        handler (obj): Handler for the logger. Default used if not supplied.
        log_format (str): Format for the handler. Default used if not supplied.'
    Returns:
        logger (obj): A logger with a handler and log format
    """
    new_logger = logging.getLogger(name)
    new_logger.setLevel(parse_log_level(os.getenv('LOG_LEVEL', LEVEL_INFO)))
    if handler is None:
        handler = logging.StreamHandler(sys.stdout)
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handler.setFormatter(logging.Formatter(log_format))
    new_logger.addHandler(handler)
    return new_logger
