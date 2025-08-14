from importlib import metadata
from io import StringIO

from loguru import logger


# Configure loguru with version formatter by default for S3 operations
def _configure_s3_logger():
    """Configure loguru with version formatter for S3 operations"""
    # Remove existing sinks
    logger.remove()

    # Add sink with version formatter
    version = metadata.version("gable")
    logger.add(
        lambda msg: print(msg, end=""),  # Print to stdout
        format=f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> <blue>[v{version}]</blue> - {{message}}",
        level="DEBUG",
    )


# Configure the logger when this module is imported
_configure_s3_logger()


def setup_logging(
    level: str = "TRACE", filepath: str = "application.log", rotation: str = "1 week"
):
    logger.remove()
    version = metadata.version("gable")
    logger.add(
        filepath,
        rotation=rotation,
        level=level,
        backtrace=True,
        diagnose=True,
        format=f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> <blue>[v{version}]</blue> - {{message}}",
    )
    print(
        f"Logging configured to level {level}, outputting to {filepath}, with rotation {rotation}."
    )


def log_trace(message: str, *args):
    """
    A wrapper function to log trace messages. This simplifies the usage of logging trace messages
    throughout the application with a standardized format.

    Args:
        message (str): The message template to log.
        *args: Arguments which are merged into the message template.
    """
    logger.trace(message, *args)


def log_error(message: str, *args):
    """
    A wrapper function to log error messages. This standardizes error logging throughout the application.

    Args:
        message (str): The message template for the error.
        *args: Arguments which are merged into the message template, typically context or error details.
    """
    logger.error(message, *args)


def log_debug(message: str, *args):
    """
    A wrapper function to log debug messages. This standardizes debug logging throughout the application.

    Args:
        message (str): The message template for the debug message.
        *args: Arguments which are merged into the message template, typically context or debug details.
    """
    logger.debug(message, *args)


log_stream = StringIO()


def setup_test_logging():
    logger.remove()
    version = metadata.version("gable")
    logger.add(
        log_stream,
        format=f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> <blue>[v{version}]</blue> - {{message}}",
        level="TRACE",
    )
    return log_stream


def get_log_output():
    """
    Retrieve the log output captured in the StringIO buffer.
    """
    return log_stream.getvalue()


def clear_log_output():
    """
    Clear the log output captured in the StringIO buffer.
    """
    log_stream.seek(0)
    log_stream.truncate()
