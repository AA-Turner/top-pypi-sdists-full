# STDLIB
import logging
import sys
import traceback
from typing import Any, Optional

# OWN
import lib_parameter

# PROJ
try:
    from . import lib_log_utils
    from . import log_handlers
except ImportError:  # pragma: no cover
    import lib_log_utils  # type: ignore  # pragma: no cover
    import log_handlers  # type: ignore  # pragma: no cover


def log_exception_traceback(
    s_error: str, log_level: int = logging.ERROR, log_level_exec_info: Optional[int] = None, log_level_traceback: Optional[int] = None
) -> str:
    """

    >>> # test with exc_info = None
    >>> assert log_exception_traceback('test') == 'test'

    >>> # test with exc_info
    >>> try:
    ...     raise FileNotFoundError('test')
    ... except Exception:       # noqa
    ...     assert log_exception_traceback('test') == 'test'


    >>> # test with subprocess to get stdout, stderr
    >>> import subprocess
    >>> try:
    ...     discard=subprocess.run('unknown_command', shell=True, check=True)
    ... except subprocess.CalledProcessError:
    ...     assert log_exception_traceback('test') == 'test'


    """

    log_level_exec_info = int(lib_parameter.get_default_if_none(log_level_exec_info, log_level))
    log_level_traceback = int(lib_parameter.get_default_if_none(log_level_traceback, log_level_exec_info))

    if s_error and log_level != logging.NOTSET:
        lib_log_utils.log_level(message=s_error, level=log_level)

    if log_level_exec_info != logging.NOTSET:
        exc_info = sys.exc_info()[1]
        exc_info_type = type(exc_info).__name__
        exc_info_msg = exc_info_type + ": " + str(exc_info)
        lib_log_utils.log_level(message=exc_info_msg, level=log_level_exec_info)
        log_stdout(exc_info, log_level_exec_info)
        log_stderr(exc_info, log_level_exec_info)

    if log_level_traceback != logging.NOTSET:
        s_traceback = traceback.format_exc().rstrip("\n")
        lib_log_utils.log_level(message=s_traceback, level=log_level_traceback)

    log_handlers.logger_flush_all_handlers()
    return s_error  # to use it as input for re-raising


def print_exception_traceback(s_error: str) -> str:
    """

    >>> # test with exc_info = None
    >>> assert print_exception_traceback('test') == 'test'

    >>> # test with exc_info
    >>> try:
    ...     raise FileNotFoundError('test')
    ... except Exception:       # noqa
    ...     assert print_exception_traceback('test') == 'test'

    >>> # test with subprocess to get stdout, stderr
    >>> import subprocess
    >>> try:
    ...     discard=subprocess.run('unknown_command', shell=True, check=True)
    ... except subprocess.CalledProcessError:
    ...     assert print_exception_traceback('test') == 'test'

    """

    exc_info = sys.exc_info()[1]
    if exc_info is not None:
        encoding = sys.getdefaultencoding()
        exc_info_msg = get_exc_info_msg()
        print(exc_info_msg.encode(encoding), file=sys.stderr)
        print_stdout(exc_info)
        print_stderr(exc_info)
        print(traceback.format_exc().rstrip("\n").encode(encoding), file=sys.stderr)
    return s_error  # to use it as input for re-raising


def get_exc_info_msg(s_error: str = '') -> str:
    """

    >>> # test with exc_info = None
    >>> assert get_exc_info_msg('test') == 'test: '

    >>> # test with exc_info
    >>> try:
    ...     raise FileNotFoundError('test')
    ... except Exception:       # noqa
    ...     assert get_exc_info_msg('test') == 'test: FileNotFoundError: test'

    >>> # test with subprocess to get stdout, stderr
    >>> import subprocess
    >>> try:
    ...     discard=subprocess.run('unknown_command', shell=True, check=True)
    ... except subprocess.CalledProcessError:
    ...     ignore = get_exc_info_msg('test')

    """
    if s_error:
        exc_info_msg = f'{s_error}: '
    else:
        exc_info_msg = ''

    exc_info = sys.exc_info()[1]
    if exc_info is not None:
        exc_info_type = type(exc_info).__name__
        exc_info_msg += exc_info_type + ": " + str(exc_info)
    return exc_info_msg


def print_stdout(exc_info: Any) -> None:
    """
    >>> class ExcInfo(object):
    ...    pass

    >>> exc_info = ExcInfo()

    >>> # test no stdout attribute
    >>> print_stdout(exc_info)

    >>> # test stdout=None
    >>> exc_info.stdout=None
    >>> print_stdout(exc_info)

    >>> # test stdout
    >>> exc_info.stdout=b'test'
    >>> print_stdout(exc_info)

    """
    if hasattr(exc_info, "stdout"):
        if exc_info.stdout is not None:
            assert isinstance(exc_info.stdout, bytes)
            print(b"STDOUT: " + exc_info.stdout, file=sys.stderr)


def print_stderr(exc_info: Any) -> None:
    """
    >>> class ExcInfo(object):
    ...    pass

    >>> exc_info = ExcInfo()

    >>> # test no stdout attribute
    >>> print_stderr(exc_info)

    >>> # test stdout=None
    >>> exc_info.stderr=None
    >>> print_stderr(exc_info)

    >>> # test stdout
    >>> exc_info.stderr=b'test'
    >>> print_stderr(exc_info)

    """
    if hasattr(exc_info, "stderr"):
        if exc_info.stderr is not None:
            assert isinstance(exc_info.stderr, bytes)
            print(b"STDERR: " + exc_info.stderr, file=sys.stderr)


def log_stdout(exc_info: Any, log_level_exec_info: int) -> None:
    """
    >>> class ExcInfo(object):
    ...    pass

    >>> exc_info = ExcInfo()

    >>> # test no stdout attribute
    >>> log_stdout(exc_info, logging.ERROR)

    >>> # test stdout=None
    >>> exc_info.stdout=None
    >>> log_stdout(exc_info, logging.ERROR)

    >>> # test stdout
    >>> exc_info.stdout=b'test'
    >>> log_stdout(exc_info, logging.ERROR)

    """
    encoding = sys.getdefaultencoding()
    if hasattr(exc_info, "stdout"):
        if exc_info.stdout is not None:
            assert isinstance(exc_info.stdout, bytes)
            lib_log_utils.log_level(message="STDOUT: " + exc_info.stdout.decode(encoding), level=log_level_exec_info)


def log_stderr(exc_info: Any, log_level_exec_info: int) -> None:
    """
    >>> class ExcInfo(object):
    ...    pass

    >>> exc_info = ExcInfo()

    >>> # test no stdout attribute
    >>> log_stderr(exc_info, logging.ERROR)

    >>> # test stdout=None
    >>> exc_info.stderr=None
    >>> log_stderr(exc_info, logging.ERROR)

    >>> # test stdout
    >>> exc_info.stderr=b'test'
    >>> log_stderr(exc_info, logging.ERROR)

    """
    encoding = sys.getdefaultencoding()
    if hasattr(exc_info, "stderr"):
        if exc_info.stderr is not None:
            assert isinstance(exc_info.stderr, bytes)
            lib_log_utils.log_level(message="STDERR: " + exc_info.stderr.decode(encoding), level=log_level_exec_info)


def test_log_util():  # type: ignore
    """
    # >>> import lib_doctest_pycharm
    # >>> lib_doctest_pycharm.setup_doctest_logger_for_pycharm(log_level=logging.DEBUG)
    # >>> test_log_util() # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Error
    ZeroDivisionError: division by zero
    Traceback Information :
    Traceback (most recent call last):
    ...
    ZeroDivisionError: division by zero

    """
    try:
        xxx = 1 / 0
        return xxx
    except ZeroDivisionError:
        log_exception_traceback("Error", log_level=logging.WARNING, log_level_exec_info=logging.INFO, log_level_traceback=logging.INFO)
