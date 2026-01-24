#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import logging

from pyspark import StorageLevel


def ensure_logger_has_handler(
    logger_name: str, log_level: int = logging.INFO, force_level: bool = False
):
    """
    Ensure a logger has a StreamHandler, add one if missing.
    Checks both the specific logger and root logger for existing handlers.

    Args:
        logger_name: Name of the logger to configure
        log_level: Log level to set on both logger and handler
        force_level: If True, always set the log level. If False, only set if logger level is NOTSET

    Returns:
        The configured logger
    """
    target_logger = logging.getLogger(logger_name)

    # Only set level if forced or if logger hasn't been configured yet
    if force_level or target_logger.level == logging.NOTSET:
        target_logger.setLevel(log_level)
    else:
        log_level = target_logger.level

    # Check if the logger already has a StreamHandler
    has_stream_handler = any(
        isinstance(h, logging.StreamHandler) for h in target_logger.handlers
    )

    # Check if root logger has handlers (from basicConfig or manual setup)
    root_logger = logging.getLogger()
    has_root_handlers = len(root_logger.handlers) > 0

    # Only add handler if:
    # 1. Logger doesn't have its own StreamHandler AND
    # 2. Root logger doesn't have handlers (to avoid duplication)
    if not has_stream_handler and not has_root_handlers:
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [Thread %(thread)d] - %(message)s"
        )
        handler.setFormatter(formatter)
        target_logger.addHandler(handler)

    return target_logger


# Initialize the main logger using the helper function
# force_level=False means it will respect any existing log level configuration
logger = ensure_logger_has_handler(
    "snowflake_connect_server", logging.INFO, force_level=False
)


def run_once_decorator(func):
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "has_run"):
            wrapper.has_run = True
            return func(*args, **kwargs)

    return wrapper


@run_once_decorator
def log_waring_once_storage_level(storage_level: StorageLevel):
    logger.warning(
        f"Ignored unsupported Spark storage level:\n{storage_level}"
        "Snowflake will always create materialized temp table from the dataframe "
        "when dataframe.cache or dataframe.persist is called.\n"
        "The behavior is similar with Spark's StorageLevel.DISK_ONLY."
    )
