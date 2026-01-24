import logging
from typing import Any

DEFAULT_TELEMETRY_METADATA: dict[str, Any] = {}


def set_telemetry_metadata(config: dict[str, Any]) -> None:
    DEFAULT_TELEMETRY_METADATA.update(config)


def get_telemetry_metadata() -> dict[str, Any]:
    return DEFAULT_TELEMETRY_METADATA


def debug_logs() -> None:
    """Test all the log levels in the root logger and a custom logger."""
    root_logger = logging.getLogger()

    root_logger.debug("This is a debug log")
    root_logger.info("This is an info log")
    root_logger.warning("This is a warning log")
    root_logger.error("This is an error log")
    root_logger.critical("This is a critical log")

    logger = logging.getLogger("test-logger")
    logger.debug("This is a debug log")
    logger.info("This is an info log")
    logger.warning("This is a warning log")
    logger.error("This is an error log")
    logger.critical("This is a critical log")

    try:
        msg = "Missing key"
        raise KeyError(msg)  # noqa: TRY301
    except KeyError as e:
        root_logger.exception(e)  # noqa:TRY401
        logger.exception(e)  # noqa:TRY401
