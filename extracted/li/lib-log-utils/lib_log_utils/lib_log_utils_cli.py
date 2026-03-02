# STDLIB
import logging
import os
import sys
from typing import Optional

# EXT
import click

# OWN
import cli_exit_tools

# PROJ
try:
    from . import __init__conf__
    from . import lib_log_utils
    from . import log_levels
    from .log_config import log_settings
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    # imports for doctest
    import __init__conf__  # type: ignore  # pragma: no cover
    import lib_log_utils  # type: ignore  # pragma: no cover
    import log_levels  # type: ignore  # pragma: no cover
    from log_config import log_settings  # type: ignore  # pragma: no cover

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

logger = logging.getLogger()


def cli_info() -> None:
    """
    >>> cli_info()
    Info for ...

    """
    __init__conf__.print_info()


def do_log(
    message: str,
    level_str: str = "info",
    extended: Optional[bool] = None,
    banner: bool = False,
    width: Optional[int] = None,
    wrap: Optional[bool] = None,
    silent: Optional[str] = None,
    quiet: Optional[bool] = None,
    force: bool = False,
    colortest: bool = False,
) -> None:

    """
    >>> do_log('test', banner=False)
    >>> do_log('test', banner=True)
    >>> do_log('test', silent='True')
    >>> do_log('test', silent='False')

    """
    if silent is not None:
        # this is intentionally, we accept every value, only "true" is handled !
        if silent.lower().startswith("true"):
            quiet = True
        else:
            quiet = False

    level = log_levels.get_log_level_from_str(level_str)
    set_logger_level_from_env()
    set_extended_from_env(extended, force)
    set_width_from_env(width, force)
    set_wrap_from_env(wrap, force)
    set_quiet_from_env(quiet, force)

    logger.level = log_settings.new_logger_level
    lib_log_utils.setup_handler(logger)

    if colortest:
        lib_log_utils.colortest()
    else:
        lib_log_utils.log_level(message=message, level=level, banner=banner)


def set_logger_level_from_env() -> None:
    """
    >>> # Setup
    >>> log_level_default = log_settings.new_logger_level

    >>> # no env Set
    >>> set_logger_level_from_env()
    >>> assert log_settings.new_logger_level == log_level_default

    >>> # env Set spam
    >>> os.environ['LOG_UTIL_LEVEL']='spam'
    >>> set_logger_level_from_env()
    >>> assert log_settings.new_logger_level == 5

    >>> # env Set unknown
    >>> os.environ['LOG_UTIL_LEVEL']='unknown'
    >>> set_logger_level_from_env()
    Traceback (most recent call last):
        ...
    ValueError: the environment setting "LOG_UTIL_LEVEL" has to be from ...

    >>> # Teardown
    >>> del os.environ['LOG_UTIL_LEVEL']
    >>> log_settings.new_logger_level = log_level_default

    """

    if "LOG_UTIL_LEVEL" in os.environ:
        try:
            log_settings.new_logger_level = log_levels.get_log_level_from_str(os.environ["LOG_UTIL_LEVEL"])
        except ValueError:
            raise ValueError('the environment setting "LOG_UTIL_LEVEL" has to be from 0-50 or one of the predefined logging levels')


def set_width_from_env(width: Optional[int] = None, force: bool = False) -> None:
    # env settings have precedence, unless force=True - if nothing is passed, the default value will be used
    """
    >>> # Setup
    >>> default_banner_width = log_settings.width

    >>> # No env Setting, width=None
    >>> set_width_from_env()
    >>> assert log_settings.width == default_banner_width

    >>> # No env Setting, width = default + 1
    >>> set_width_from_env(default_banner_width + 1)
    >>> assert log_settings.width == default_banner_width + 1

    >>> # Env Setting = default + 2, width=None
    >>> os.environ['LOG_UTIL_WIDTH'] = str(default_banner_width + 2)
    >>> set_width_from_env()
    >>> assert log_settings.width == default_banner_width + 2

    >>> # Env Setting = default + 3, width=default (env has precedence)
    >>> os.environ['LOG_UTIL_WIDTH'] = str(default_banner_width + 3)
    >>> set_width_from_env(default_banner_width)
    >>> assert log_settings.width == default_banner_width + 3

    >>> # Env Setting = default + 3, width=default + 4, force = True (parameter has precedence)
    >>> set_width_from_env(default_banner_width + 4, True)
    >>> assert log_settings.width == default_banner_width + 4

    >>> # provoke Error wrong type
    >>> os.environ['LOG_UTIL_WIDTH'] = 'abc'
    >>> set_width_from_env()
    Traceback (most recent call last):
        ...
    ValueError: invalid environment setting for "LOG_UTIL_WIDTH", must be numerical and >= 10

    >>> # provoke Error too small
    >>> os.environ['LOG_UTIL_WIDTH'] = '9'
    >>> set_width_from_env()
    Traceback (most recent call last):
        ...
    ValueError: invalid environment setting for "LOG_UTIL_WIDTH", must be numerical and >= 10

    >>> # Teardown
    >>> log_settings.width = default_banner_width
    >>> del os.environ['LOG_UTIL_WIDTH']

    """

    if "LOG_UTIL_WIDTH" in os.environ:
        if width is not None and force:
            log_settings.width = width
        else:
            s_error = 'invalid environment setting for "LOG_UTIL_WIDTH", must be numerical and >= 10'
            try:
                width = int(os.environ["LOG_UTIL_WIDTH"])
            except ValueError:
                raise ValueError(s_error)
            if width < 10:
                raise ValueError(s_error)
            log_settings.width = width
    else:
        if width is not None:
            log_settings.width = width


def set_extended_from_env(extended: Optional[bool] = None, force: bool = False) -> None:
    # env settings have precedence, unless force=True - if nothing is passed, the default value will be used
    """
    >>> # Setup
    >>> default_fmt = log_settings.fmt

    >>> # No env Setting, extended=None
    >>> set_extended_from_env()
    >>> assert log_settings.fmt == default_fmt

    >>> # No env Setting, extended = True
    >>> set_extended_from_env(True)
    >>> assert log_settings.fmt == log_settings.fmt_extended_cli

    >>> # No env Setting, extended = False
    >>> set_extended_from_env(False)
    >>> assert log_settings.fmt == log_settings.fmt_plain

    >>> # Env Setting = plain, extended=None
    >>> os.environ['LOG_UTIL_FMT'] = 'plain'
    >>> set_extended_from_env()
    >>> assert log_settings.fmt == log_settings.fmt_plain

    >>> # Env Setting = extended, extended=None
    >>> os.environ['LOG_UTIL_FMT'] = 'extended'
    >>> set_extended_from_env()
    >>> assert log_settings.fmt == log_settings.fmt_extended_cli

    >>> # Env Setting = extended, extended=False, Force = False
    >>> os.environ['LOG_UTIL_FMT'] = 'extended'
    >>> set_extended_from_env(extended=False, force=False)
    >>> assert log_settings.fmt == log_settings.fmt_extended_cli

    >>> # Env Setting = extended, extended=False, Force = True
    >>> os.environ['LOG_UTIL_FMT'] = 'extended'
    >>> set_extended_from_env(extended=False, force=True)
    >>> assert log_settings.fmt == log_settings.fmt_plain

    >>> # Env Setting = extended, extended=True, Force = True
    >>> os.environ['LOG_UTIL_FMT'] = 'plain'
    >>> set_extended_from_env(extended=True, force=True)
    >>> assert log_settings.fmt == log_settings.fmt_extended_cli

    >>> # custom format string
    >>> os.environ['LOG_UTIL_FMT'] = 'some_custom_format'
    >>> set_extended_from_env()
    >>> assert log_settings.fmt == 'some_custom_format'

    >>> # Teardown
    >>> log_settings.fmt = default_fmt
    >>> del os.environ['LOG_UTIL_FMT']

    """

    def set_fmt(_ext: Optional[bool]) -> None:
        if extended is True:
            log_settings.fmt = log_settings.fmt_extended_cli
        elif extended is False:
            log_settings.fmt = log_settings.fmt_plain

    if "LOG_UTIL_FMT" in os.environ:
        if extended is not None and force:
            set_fmt(extended)
        else:
            if os.environ["LOG_UTIL_FMT"].lower().startswith("plain"):
                log_settings.fmt = log_settings.fmt_plain
            elif os.environ["LOG_UTIL_FMT"].lower().startswith("extended"):
                log_settings.fmt = log_settings.fmt_extended_cli
            else:
                log_settings.fmt = os.environ["LOG_UTIL_FMT"]

    else:
        set_fmt(extended)


def set_wrap_from_env(wrap_text: Optional[bool] = None, force: bool = False) -> None:
    # env settings have precedence, unless force=True - if nothing is passed, the default value will be used
    """
    >>> # Setup
    >>> default_wrap_text = log_settings.wrap

    >>> # No env Setting, wrap=None
    >>> set_wrap_from_env()
    >>> assert log_settings.wrap == default_wrap_text

    >>> # No env Setting, wrap = not default_wrap_text
    >>> set_wrap_from_env(not default_wrap_text)
    >>> assert log_settings.wrap != default_wrap_text

    >>> # Env Setting = not default_wrap_text, wrap=None
    >>> os.environ['LOG_UTIL_WRAP'] = str(not default_wrap_text)
    >>> set_wrap_from_env()
    >>> assert log_settings.wrap != default_wrap_text

    >>> # Env Setting = not default_wrap_text, wrap=default_wrap_text (env has precedence)
    >>> os.environ['LOG_UTIL_WRAP'] = str(not default_wrap_text)
    >>> set_wrap_from_env(default_wrap_text)
    >>> assert log_settings.wrap != default_wrap_text

    >>> # Env Setting = default_wrap_text, wrap=default_wrap_text (env has precedence)
    >>> os.environ['LOG_UTIL_WRAP'] = str(default_wrap_text)
    >>> set_wrap_from_env(default_wrap_text)
    >>> assert log_settings.wrap == default_wrap_text

    >>> # Env Setting = not default_wrap_text, wrap=default_wrap_text (parameter has precedence)
    >>> set_wrap_from_env(default_wrap_text, True)
    >>> assert log_settings.wrap == default_wrap_text

    >>> # provoke Error
    >>> os.environ['LOG_UTIL_WRAP'] = 'something'
    >>> set_wrap_from_env()
    Traceback (most recent call last):
        ...
    ValueError: invalid environment setting for "LOG_UTIL_WRAP", must be "True" or "False"

    >>> # Teardown
    >>> log_settings.wrap = default_wrap_text
    >>> del os.environ['LOG_UTIL_WRAP']

    """
    if "LOG_UTIL_WRAP" in os.environ:
        if wrap_text is not None and force:
            log_settings.wrap = wrap_text
        else:
            if os.environ["LOG_UTIL_WRAP"].lower().startswith("false"):
                log_settings.wrap = False
            elif os.environ["LOG_UTIL_WRAP"].lower().startswith("true"):
                log_settings.wrap = True
            else:
                raise ValueError('invalid environment setting for "LOG_UTIL_WRAP", must be "True" or "False"')
    else:
        if wrap_text is not None:
            log_settings.wrap = wrap_text


def set_quiet_from_env(quiet: Optional[bool] = None, force: bool = False) -> None:
    # env settings have precedence, unless force=True - if nothing is passed, the default value will be used
    # parameter -q is anything else then "True" (not case sensitive), or not set, it is considered as False.
    """
    >>> # Setup
    >>> default_quiet = log_settings.quiet

    >>> # No env Setting, log_console=None
    >>> set_quiet_from_env()
    >>> assert log_settings.quiet == default_quiet

    >>> # No env Setting, log_console = default_quiet
    >>> set_quiet_from_env(not default_quiet)
    >>> assert log_settings.quiet != default_quiet

    >>> # Env Setting = not default_quiet, log_console=None
    >>> os.environ['LOG_UTIL_QUIET'] = str(not default_quiet)
    >>> set_quiet_from_env()
    >>> assert log_settings.quiet != default_quiet

    >>> # Env Setting = not default_quiet, log_console=not default_quiet (env has precedence)
    >>> os.environ['LOG_UTIL_QUIET'] = str(not default_quiet)
    >>> set_quiet_from_env(default_quiet)
    >>> assert log_settings.quiet != default_quiet

    >>> # Env Setting = default_quiet, log_console=not default_quiet (env has precedence)
    >>> os.environ['LOG_UTIL_QUIET'] = str(default_quiet)
    >>> set_quiet_from_env(default_quiet)
    >>> assert log_settings.quiet == default_quiet

    >>> # Env Setting = not default_quiet, log_console=default_quiet (parameter has precedence)
    >>> set_quiet_from_env(default_quiet, True)
    >>> assert log_settings.quiet == default_quiet

    >>> # provoke Error
    >>> os.environ['LOG_UTIL_QUIET'] = 'something'
    >>> set_quiet_from_env()
    Traceback (most recent call last):
        ...
    ValueError: invalid environment setting for "LOG_UTIL_QUIET", must be "True" or "False"

    >>> # Teardown
    >>> log_settings.quiet = default_quiet
    >>> del os.environ['LOG_UTIL_QUIET']

    """

    if "LOG_UTIL_QUIET" in os.environ:
        if quiet is not None and force:
            log_settings.quiet = quiet
        else:
            if os.environ["LOG_UTIL_QUIET"].lower().startswith("false"):
                log_settings.quiet = False
            elif os.environ["LOG_UTIL_QUIET"].lower().startswith("true"):
                log_settings.quiet = True
            else:
                raise ValueError('invalid environment setting for "LOG_UTIL_QUIET", must be "True" or "False"')
    else:
        if quiet is not None:
            log_settings.quiet = quiet


@click.command(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(
    version=__init__conf__.version, prog_name=__init__conf__.shell_command, message=f"{__init__conf__.shell_command} version {__init__conf__.version}"
)
@click.option("-e", "--extended", is_flag=True, type=bool, default=None, help="extended log format")
@click.option("-p", "--plain", is_flag=True, type=bool, default=None, help="plain log format")
@click.option("-b", "--banner", is_flag=True, type=bool, default=False, help="log as banner")
@click.option("-w", "--width", type=int, default=None, help="wrap width, default=140")
@click.option("--wrap/--nowrap", type=bool, default=None, help="wrap text")
# if parameter -q is anything else then "True" (not case sensitive), or not set, it is considered as False.
# This makes it possible to silence messages elegantly in a shellscript
@click.option("-s", "--silent", type=str, default=None, help='disable logging if "True"')
@click.option("-q", "--quiet", is_flag=True, type=bool, default=None, help="disable logging as flag")
@click.option("-f", "--force", is_flag=True, type=bool, default=False, help="take precedence over environment settings")
@click.option("-l", "--level", type=str, default="info", help="log level as number or predefined Level")
@click.option("--program_info", is_flag=True, type=bool, default=False, help="get program info")
@click.option("-c", "--colortest", is_flag=True, type=bool, default=False, help="color test")
@click.option("--traceback/--no-traceback", is_flag=True, type=bool, default=None, help="return traceback information on cli")
@click.argument("message", required=False, default="")
def cli_main(
    message: str,
    level: str,
    extended: Optional[bool],
    plain: Optional[bool],
    banner: bool,
    width: Optional[int],
    wrap: Optional[bool],
    silent: Optional[str],
    quiet: Optional[bool],
    force: bool,
    program_info: bool,
    colortest: bool,
    traceback: Optional[bool] = None,
) -> None:
    """log a message"""
    if traceback is not None:
        cli_exit_tools.config.traceback = traceback
    if program_info:
        cli_info()
    else:
        if plain:
            extended = False
        do_log(
            message=message,
            level_str=level,
            extended=extended,
            banner=banner,
            width=width,
            wrap=wrap,
            silent=silent,
            quiet=quiet,
            force=force,
            colortest=colortest,
        )


# entry point if main
if __name__ == "__main__":
    try:
        cli_main()  # type: ignore
    except Exception as exc:
        cli_exit_tools.print_exception_message()
        sys.exit(cli_exit_tools.get_system_exit_code(exc))
    finally:
        cli_exit_tools.flush_streams()
