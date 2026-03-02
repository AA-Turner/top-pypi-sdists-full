# STDLIB
from typing import Optional, Union

import logging
import logging.handlers
import sys
import textwrap
from typing import Dict

# EXT
import humanfriendly.cli  # type: ignore  # noqa

# OWN
import lib_parameter

# PROJ
# imports for local pytest
try:
    from .log_config import log_settings
    from . import log_handlers
    from . import log_levels
    from . import log_traceback
except ImportError:  # pragma: no cover
    from log_config import log_settings  # type: ignore # pragma: no cover
    import log_handlers  # type: ignore # pragma: no cover
    import log_levels  # type: ignore # pragma: no cover
    import log_traceback  # type: ignore # pragma: no cover


# Custom Types
FieldAndLevelStyles = Dict[str, Dict[str, Union[str, bool]]]


def banner_spam(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner SPAM

    >>> banner_spam('spam')

    """
    log_level(message=message, level=log_levels.SPAM, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_debug(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner DEBUG

    >>> banner_debug('debug')

    """
    log_level(message=message, level=logging.DEBUG, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_verbose(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner VERBOSE

    >>> banner_verbose('verbose')

    """
    log_level(message=message, level=log_levels.VERBOSE, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_info(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner INFO

    >>> banner_info('info')

    """
    log_level(message=message, level=logging.INFO, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_notice(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner NOTICE

    >>> banner_notice('notice')

    """
    log_level(message=message, level=log_levels.NOTICE, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_success(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner SUCCESS

    >>> banner_success('success')

    """
    log_level(message=message, level=log_levels.SUCCESS, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_warning(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner WARNING

    >>> banner_warning('warning')

    """
    log_level(message=message, level=logging.WARNING, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_error(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner ERROR

    >>> banner_error('error')

    """
    log_level(message=message, level=logging.ERROR, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def banner_critical(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = True,
) -> None:
    """
    logs a banner CRITICAL

    >>> banner_critical('critical')

    """
    log_level(message=message, level=logging.CRITICAL, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_spam(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs SPAM

    >>> log_spam('spam')

    """
    log_level(message=message, level=log_levels.SPAM, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_debug(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs DEBUG

    >>> log_debug('debug')

    """
    log_level(message=message, level=logging.DEBUG, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_verbose(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs VERBOSE

    >>> log_verbose('verbose')

    """
    log_level(message=message, level=log_levels.VERBOSE, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_info(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs INFO

    >>> log_info('info')

    """
    log_level(message=message, level=logging.INFO, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_notice(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs NOTICE

    >>> log_notice('notice')

    """
    log_level(message=message, level=log_levels.NOTICE, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_success(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs SUCCESS

    >>> log_success('success')

    """
    log_level(message=message, level=log_levels.SUCCESS, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_warning(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs WARNING

    >>> log_warning('warning')

    """
    log_level(message=message, level=logging.WARNING, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_error(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs ERROR

    >>> log_error('error')

    """
    log_level(message=message, level=logging.ERROR, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_critical(
    message: str,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs CRITICAL

    >>> log_critical('critical')

    """

    log_level(message=message, level=logging.CRITICAL, width=width, wrap=wrap, logger=logger, quiet=quiet, banner=banner)


def log_level(
    message: str,
    level: Optional[int] = None,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    logger: Optional[logging.Logger] = None,
    quiet: Optional[bool] = None,
    banner: bool = False,
) -> None:
    """
    logs a message

    if there is no logger passed, the root logger will be used.

    >>> logger = logging.getLogger()
    >>> log_level('test')
    >>> log_level('test', quiet=True)
    >>> log_level('test', logger=logger)
    >>> log_level('test', logging.SUCCESS, wrap=True)  # noqa
    >>> log_level('test', logging.ERROR, wrap=True)
    >>> log_level('test', logging.ERROR, wrap=False)
    >>> log_level('test', logging.ERROR, wrap=True, banner = True)
    >>> log_level('test', logging.ERROR, wrap=False, banner = True)
    >>> log_level('this is\\none nice piece of ham\\none nice piece of spam\\none more piece of wonderful spam', \
                   logging.ERROR, width=10, wrap=True)
    >>> log_level('this is\\none nice piece of ham\\none nice piece of spam\\none more piece of wonderful spam', \
                   logging.ERROR, width=10, wrap=False)
    >>> log_level('this is\\none nice piece of ham\\none nice piece of spam\\none more piece of wonderful spam', \
                   logging.ERROR, width=10, wrap=True, banner = True)
    >>> log_level('this is\\none nice piece of ham\\none nice piece of spam\\none more piece of wonderful spam', \
                   logging.ERROR, width=10, wrap=False, banner = True)
    """

    quiet = bool(lib_parameter.get_default_if_none(quiet, default=log_settings.quiet))

    if quiet:
        return

    message = str(message)

    level = int(lib_parameter.get_default_if_none(level, default=log_settings.new_logger_level))
    width = int(lib_parameter.get_default_if_none(width, default=log_settings.width))
    wrap = bool(lib_parameter.get_default_if_none(wrap, default=log_settings.wrap))

    if logger is None:
        logger = logging.getLogger()

    l_message = message.split("\n")

    if banner:
        sep_line = "*" * width
        logger.log(level=level, msg=sep_line)  # 140 characters is about the width in travis log screen
        for line in l_message:
            if wrap:
                l_wrapped_lines = textwrap.wrap(line, width=width - 2, tabsize=4, replace_whitespace=False, initial_indent="* ", subsequent_indent="* ")
                for wrapped_line in l_wrapped_lines:
                    msg_line = wrapped_line + (width - len(wrapped_line) - 1) * " " + "*"
                    logger.log(level=level, msg=msg_line)
            else:
                line = "* " + line.rstrip()
                if len(line) < width - 1:
                    line = line + (width - len(line) - 1) * " " + "*"
                logger.log(level=level, msg=line)
        logger.log(level=level, msg=sep_line)
        log_handlers.logger_flush_all_handlers(logger)
    else:
        for line in l_message:
            if wrap:
                l_wrapped_lines = textwrap.wrap(line, width=width, tabsize=4, replace_whitespace=False)
                for msg_line in l_wrapped_lines:
                    logger.log(level=level, msg=msg_line)
            else:
                msg_line = line.rstrip()
                logger.log(level=level, msg=msg_line)
                log_handlers.logger_flush_all_handlers(logger)


def colortest(quiet: bool = False) -> None:
    """test banner colors

    >>> # Setup
    >>> log_settings.use_colored_stream_handler=True
    >>> log_settings.new_logger_level = 0
    >>> log_settings.stream_handler_log_level = 0
    >>> log_settings.stream = sys.stdout
    >>> setup_handler()
    >>> colortest()
    <BLANKLINE>
        ...test ...
    >>> colortest(quiet=True)
    >>> # TearDown
    >>> log_settings.stream = sys.stderr
    >>> setup_handler(remove_existing_stream_handlers=True)

    """
    if not quiet:
        log_spam("test level spam")
        log_debug("test level debug")
        log_verbose("test level verbose")
        log_info("test level info")
        log_notice("test level notice")
        log_success("test level success")
        log_warning("test level warning")
        log_error("test level error")
        log_critical("test level critical")
        humanfriendly.cli.demonstrate_ansi_formatting()


def setup_handler(logger: logging.Logger = logging.getLogger(), remove_existing_stream_handlers: bool = False) -> None:
    """

    >>> # Setup
    >>> save_use_use_colored_stream_handler = log_settings.use_colored_stream_handler

    >>> # Test colored
    >>> log_settings.use_colored_stream_handler = True
    >>> setup_handler()
    >>> assert log_handlers.exists_handler_with_name('stream_handler_color')

    >>> # Test non colored
    >>> log_settings.use_colored_stream_handler = False
    >>> setup_handler()
    >>> assert log_handlers.exists_handler_with_name('stream_handler')

    >>> # Teardown
    >>> log_settings.use_colored_stream_handler = save_use_use_colored_stream_handler

    """
    if log_settings.use_colored_stream_handler:
        log_handlers.set_stream_handler_color(
            logger=logger,
            level=log_settings.stream_handler_log_level,
            fmt=log_settings.fmt,
            datefmt=log_settings.datefmt,
            field_styles=log_settings.field_styles,
            level_styles=log_settings.level_styles,
            stream=log_settings.stream,
            remove_existing_stream_handlers=remove_existing_stream_handlers,
        )
    else:
        log_handlers.set_stream_handler(
            logger=logger,
            level=log_settings.stream_handler_log_level,
            fmt=log_settings.fmt,
            datefmt=log_settings.datefmt,
            stream=log_settings.stream,
            remove_existing_stream_handlers=remove_existing_stream_handlers,
        )
