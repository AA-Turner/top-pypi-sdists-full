# STDLIB
import logging
import logging.handlers
import getpass
import os
import platform
import sys
from types import TracebackType
from typing import Any, Dict, Optional, Tuple, Union, TextIO, Type

LogHandler = Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]]

# OWN
import lib_parameter
import lib_platform
import lib_programname

# EXT
import coloredlogs  # type: ignore

# Custom Types
FieldAndLevelStyles = Dict[str, Dict[str, Union[str, bool]]]


# default_fmt_string = '[{username}@%(hostname)s][%(asctime)s][%(levelname)-8s]: %(message)s'
# we dont use the built in %(programname)s because it does not work in doctest
default_fmt = "[{username}@{hostname_short}][{program_name}@%(process)d][%(asctime)s][%(levelname)-8s]: %(message)s"
default_date_fmt = "%Y-%m-%d %H:%M:%S"


class HostnameFilter(logging.Filter):
    """
    adds a filter for short hostname

    >>> record = logging.makeLogRecord(dict())
    >>> hostname_filter = HostnameFilter()
    >>> discard = hostname_filter.filter(record)
    >>> assert record.hostname == platform.node()   # noqa

    """

    hostname = platform.node()

    def filter(self, record: Any) -> bool:
        record.hostname = HostnameFilter.hostname
        return True


def set_file_handler(
    filename: str,
    logger: logging.Logger = logging.getLogger(),
    name: str = "file_handler",
    level: int = logging.INFO,
    fmt: str = default_fmt,
    datefmt: str = default_date_fmt,
    remove_existing_file_handlers: bool = False,
    mode: str = "a",
    encoding: str = "utf-8",
    delay: bool = True,
) -> logging.Handler:
    """
    name: the name of the file handler. if name = '', name = filename

    mode: 'a': Opens a file for appending new information to it. The pointer is placed at the end of the file.
               A new file is created if one with the same name doesn't exist.
          'w': Opens in write-only mode. The pointer is placed at the beginning of the file and this will overwrite
               any existing file with the same name. It will create a new file if one with the same name doesn't exist.
    delay: If delay is true, then file opening is deferred until the first call to emit(). By default, the file grows indefinitely.
    """

    if remove_existing_file_handlers:
        remove_handler_by_type(logger, logging.FileHandler)

    file_handler = logging.FileHandler(filename=filename, mode=mode, encoding=encoding, delay=delay)  # type: logging.Handler
    file_handler = _add_handler(file_handler, logger=logger, name=name, level=level, fmt=fmt, datefmt=datefmt)
    return file_handler


def set_stream_handler(
    logger: logging.Logger = logging.getLogger(),
    stream: TextIO = sys.stderr,
    name: str = "stream_handler",
    level: int = logging.INFO,
    fmt: str = default_fmt,
    datefmt: str = default_date_fmt,
    remove_existing_stream_handlers: bool = False,
) -> logging.Handler:

    """
    Sets a Stream Handler. A Handler with the same name will be replaced (with a warning)


    >>> logger = logging.getLogger('test_add_streamhandler')
    >>> set_stream_handler(logger, remove_existing_stream_handlers=True)
    <StreamHandler ...
    >>> set_stream_handler(logger, name='test', remove_existing_stream_handlers=False)
    <StreamHandler ...
    >>> assert len(logger.handlers) == 2

    """

    if remove_existing_stream_handlers:
        try:
            remove_handler_by_type(logger=logger, handler_type=logging.StreamHandler)
            remove_handler_by_name(name)
        except ValueError:  # pragma: no cover
            pass  # pragma: no cover

    stream_handler: logging.Handler = logging.StreamHandler(stream=stream)
    stream_handler = _add_handler(stream_handler, logger=logger, name=name, level=level, fmt=fmt, datefmt=datefmt)
    return stream_handler


def set_stream_handler_color(
    logger: logging.Logger = logging.getLogger(),
    stream: TextIO = sys.stderr,
    name: str = "stream_handler_color",
    level: int = logging.INFO,
    fmt: str = default_fmt,
    datefmt: str = default_date_fmt,
    field_styles: Optional[FieldAndLevelStyles] = None,
    level_styles: Optional[FieldAndLevelStyles] = None,
    remove_existing_stream_handlers: bool = False,
) -> logging.Handler:
    """
    Sets a Colored Stream Handler. A Handler with the same name will be replaced (with a warning)
    if remove_existing_stream_handlers is set, otgerwise it will be reconfigured

    >>> logger=logging.getLogger()
    >>> handler = set_stream_handler_color(logger)
    >>> logger.debug("DEBUG")
    >>> logger.info("INFO")
    >>> logger.warning("WARNING")
    >>> logger.error("ERROR")
    >>> logger.critical("CRITICAL")

    """

    field_styles = lib_parameter.get_default_if_none(field_styles, coloredlogs.DEFAULT_FIELD_STYLES)  # type: ignore
    level_styles = lib_parameter.get_default_if_none(level_styles, coloredlogs.DEFAULT_LEVEL_STYLES)  # type: ignore

    if remove_existing_stream_handlers:
        try:
            remove_handler_by_type(logger=logger, handler_type=logging.StreamHandler)
            remove_handler_by_name(name)
        except ValueError:
            pass

    fmt = override_fmt_via_environment(fmt, "COLOREDLOGS_LOG_FORMAT")
    if hasattr(fmt, "format"):
        fmt = format_fmt(fmt)
    datefmt = override_fmt_via_environment(datefmt, "COLOREDLOGS_DATE_FORMAT")
    field_styles = override_style_via_environment(field_styles, "COLOREDLOGS_FIELD_STYLES")
    level_styles = override_style_via_environment(level_styles, "COLOREDLOGS_LEVEL_STYLES")

    # https://coloredlogs.readthedocs.io/en/latest/api.html
    coloredlogs.install(
        logger=logger, level=level, fmt=fmt, datefmt=datefmt, field_styles=field_styles, level_styles=level_styles, stream=stream, isatty=True
    )  # type: ignore
    logger.handlers[-1].name = name
    handler = logger.handlers[-1]
    return handler


def override_fmt_via_environment(original_value: Any, environment_variable: str) -> Any:
    if environment_variable in os.environ:
        return_value = os.environ[environment_variable]
    else:
        return_value = original_value
    return return_value


def override_style_via_environment(original_value: Any, environment_variable: str) -> Any:
    if environment_variable in os.environ:
        return_value = coloredlogs.parse_encoded_styles(os.environ[environment_variable])  # type: ignore
    else:
        return_value = original_value
    return return_value


def _add_handler(
    handler: logging.Handler,
    logger: logging.Logger = logging.getLogger(),
    name: str = "log_handler",
    level: int = logging.INFO,
    fmt: str = default_fmt,
    datefmt: str = default_date_fmt,
) -> logging.Handler:

    """
    >>> result = set_stream_handler()
    >>> result2 = set_stream_handler()

    """

    handler.addFilter(HostnameFilter())
    fmt = format_fmt(fmt)
    formatter = logging.Formatter(fmt, datefmt)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    handler.name = name
    logger.addHandler(handler)
    return handler


def format_fmt(fmt: str) -> str:
    fmt = fmt.format(
        username=getpass.getuser(),
        hostname_short=lib_platform.hostname_short,
        hostname=lib_platform.hostname,
        program_name=lib_programname.get_path_executed_script().stem,
    )
    return fmt


def get_handler_by_name(name: str) -> logging.Handler:
    """
    >>> import unittest
    >>> logger = set_stream_handler()
    >>> unittest.TestCase().assertIsNotNone(get_handler_by_name, ['console_handler'])
    >>> unittest.TestCase().assertRaises(ValueError, get_handler_by_name, ['unknown_handler'])

    """

    handlers = logging.getLogger().handlers
    for handler in handlers:
        if hasattr(handler, "name"):
            if handler.name == name:
                return handler
    raise ValueError(f'Logging Handler "{name}" not found')


def remove_handler_by_name(name: str) -> None:
    handler = get_handler_by_name(name=name)
    logging.getLogger().removeHandler(handler)


def remove_all_handlers(logger: logging.Logger = logging.getLogger()) -> None:
    handlers = logger.handlers
    for handler in handlers:
        logger.removeHandler(handler)


def remove_handler_by_type(logger: logging.Logger, handler_type: LogHandler) -> None:
    """
    >>> logger = logging.getLogger()
    >>> logging.basicConfig()
    >>> remove_handler_by_type(logger, logging.StreamHandler)

    """

    handlers = logger.handlers
    for handler in handlers:
        # noinspection PyTypeChecker
        if isinstance(handler, handler_type):
            logger.removeHandler(handler)


def exists_handler_with_name(name: str) -> bool:
    """
    >>> discard = set_stream_handler()
    >>> assert exists_handler_with_name('stream_handler')
    >>> discard2 = set_stream_handler_color()
    >>> assert exists_handler_with_name('stream_handler_color')
    >>> assert not exists_handler_with_name('unknown_handler')

    """
    handlers = logging.getLogger().handlers
    for handler in handlers:
        if hasattr(handler, "name"):
            if handler.name == name:
                return True
    return False


def logger_flush_all_handlers(logger: logging.Logger = logging.getLogger()) -> None:
    """
    >>> logger_flush_all_handlers()

    """
    for handler in logger.handlers:
        if hasattr(handler, "flush"):
            try:
                handler.flush()
            except ValueError:
                # we have got ValueError: underlying buffer has been detached on github Actions Windows
                pass


class SaveLogHandlerFormatter(object):
    """ """

    """
    >>> # those tests dont run on pytest
    >>> import lib_doctest_pycharm
    >>> lib_doctest_pycharm.setup_doctest_logger_for_pycharm()
    >>> logger=logging.getLogger()
    >>> logger.info('test')
    test
    >>> handler = get_handler_by_name('doctest_console_handler')

    >>> log_handler_formatter_save = SaveLogHandlerFormatter(handler=handler)
    >>> set_log_handler_formatter_prefix(handler=handler, log_formatter_prefix='test4 prefix: ')
    >>> logger.info('test')
    test4 prefix: test
    >>> log_handler_formatter_save.restore()
    >>> log_handler_formatter_save.close()

    >>> with SaveLogHandlerFormatter(handler=handler):
    ...     set_log_handler_formatter_prefix(handler=handler, log_formatter_prefix='test5 prefix2: ')
    ...     logger.info('test2')
    test5 prefix2: test2

    >>> # teardown
    >>> remove_handler_by_name(name='doctest_console_handler')

    """

    def __init__(self, handler: logging.Handler):
        self._handler = handler
        self._formatter: Optional[logging.Formatter] = None
        self.save()

    def __enter__(self) -> "SaveLogHandlerFormatter":
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        self.restore()
        self.close()

    def close(self) -> None:
        del self._handler
        del self._formatter

    def save(self) -> None:
        self._formatter = self._handler.formatter

    def restore(self) -> None:
        self._handler.formatter = self._formatter


def set_log_handler_formatter_prefix(handler: logging.Handler, log_formatter_prefix: str) -> None:
    if handler.formatter:
        if handler.formatter._fmt:
            handler.formatter._fmt = log_formatter_prefix + handler.formatter._fmt
            handler.formatter._style._fmt = log_formatter_prefix + handler.formatter._style._fmt
        else:
            handler.formatter._fmt = log_formatter_prefix + "%(message)s"
            handler.formatter._style._fmt = log_formatter_prefix + "%(message)s"
    else:
        datefmt = default_date_fmt
        formatter = logging.Formatter(log_formatter_prefix + "%(message)s", datefmt)
        handler.setFormatter(formatter)
