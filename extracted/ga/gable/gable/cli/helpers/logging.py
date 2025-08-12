import sys
import time
from importlib import metadata
from typing import Literal

import click
from loguru import logger

# Used to track what the current log level is so it can be accessed in plugin code
# We need to track separately as there's no way to access the level from the loguru
# public API https://github.com/Delgan/loguru/issues/774#issuecomment-1373652135
CURRENT_LOG_LEVEL: Literal["INFO", "DEBUG", "TRACE"] = "INFO"


def get_winston_log_level() -> Literal["info", "verbose", "debug"]:
    """Maps loguru log levels to their equivalent Winston levels"""
    if CURRENT_LOG_LEVEL == "INFO":
        return "info"
    elif CURRENT_LOG_LEVEL == "DEBUG":
        return "verbose"
    return "debug"


def configure_default_click_logging():
    """Configure default logger for the CLI, which uses click.echo() to print INFO+ messages to the console."""

    def default_formatter(record):
        """Function that returns the default loguru formatter for the CLI. The only reason we need this is to prevent
        the logger from appending a newline to the end of the message, as click.echo() will do for us...
        """
        return "{message}"

    # Remove the default loguru sink
    logger.remove()
    global CURRENT_LOG_LEVEL
    CURRENT_LOG_LEVEL = "INFO"
    # Add a new sink for click.echo() to use
    logger.add(
        click_echo_sink,
        format=default_formatter,
        level="INFO",
        backtrace=False,
        diagnose=False,
    )


def configure_debug_logger(ctx, param, value):
    """Configure debug logging by adding an additional loguru sink that prints DEBUG+ messages to stderr."""

    def debug_formatter(record):
        """Function that returns a loguru formatter for debug logging. If the record contains a 'context' key in the
        'extra' dictionary, it will be used to format the message. The context can be set with either the logger.bind()
        or logger.contextualize() functions."""
        version = metadata.version("gable")
        if "extra" in record and "context" in record["extra"]:
            return f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> <light-cyan>({{extra[context]}})</light-cyan> <blue>[v{version}]</blue> - {{message}}\n"
        return f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> <blue>[v{version}]</blue> - {{message}}\n"

    if value:
        # Add the new sink with level set to DEBUG
        global CURRENT_LOG_LEVEL
        CURRENT_LOG_LEVEL = "DEBUG"
        logger.add(
            sys.stderr,
            level="DEBUG",
            format=debug_formatter,
        )
    return value


def configure_trace_logger(ctx, param, value):
    """Configure trace logging by adding an additional loguru sink that prints that prints TRACE+ messages to stderr,
    along with more detailed log messages.
    """

    def trace_formatter(record):
        """Function that returns a loguru formatter for trace logging. If the record contains a 'context' key in the
        'extra' dictionary, it will be used to format the message. The context can be set with either the logger.bind()
        or logger.contextualize() functions."""
        # Trim the .py from the file name
        record["file"].name = record["file"].name.replace(".py", "")
        version = metadata.version("gable")
        if "extra" in record and "context" in record["extra"]:
            return f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> | <fg 255,161,94>{{file.name}}.{{function}}</fg 255,161,94> <light-cyan>({{extra[context]}})</light-cyan> <blue>[v{version}]</blue> - {{message}}\n"
        return f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> | <fg 255,161,94>{{file.name}}.{{function}}</fg 255,161,94> <blue>[v{version}]</blue> - {{message}}\n"

    if value:
        # Add the new sink with level set to DEBUG
        global CURRENT_LOG_LEVEL
        CURRENT_LOG_LEVEL = "TRACE"
        logger.add(
            sys.stderr,
            level="TRACE",
            format=trace_formatter,
        )
    return value


def click_echo_sink(message):
    """Define a loguru sink for click.echo() to use - this will be the default sync, and is equivalent
    to just calling click.echo() directly. This sink will be replaced if the --debug flag is passed to the CLI
    """
    # Be very safe here so we don't throw an error when logging
    is_error = False
    try:
        record = message if isinstance(message, dict) else message.record
        is_error = record["level"].name == "ERROR"
    except:
        pass
    click.echo(message, err=is_error)


def log_execution_time(func):
    """Decorator that logs the execution time of a function."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logger.debug(f"{func.__name__} executed in {duration:.2f} seconds")
        return result

    return wrapper
