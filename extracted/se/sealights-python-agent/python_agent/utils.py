import functools
import hashlib
import logging
import os
import random
import string
import sys
import threading
import time
from enum import Enum
from threading import _DummyThread

from python_agent import bootstrap

log = logging.getLogger(__name__)


def create_md5():
    """
    Create MD5 hash object with proper configuration.

    MD5 is used for non-security purposes (method signatures, file identifiers).
    usedforsecurity=False allows MD5 in environments with FIPS-enabled OpenSSL
    (common in RHEL, government systems, etc). The parameter has been available
    since Python 3.9, below the agent's 3.10+ support floor, so no version guard
    is needed.
    """
    return hashlib.md5(usedforsecurity=False)


def retries(logger, tries=3, quiet=True):
    def inner(f):
        @functools.wraps(f)
        def inner_args(*args, **kwargs):
            for i in range(tries):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        "failed try #%s running function %s. args: %s exception: %s"
                        % (str(i + 1), f.__name__, str(args), str(e)),
                        exc_info=True,
                    )
                    time.sleep(2 * i)
            if quiet:
                return
            raise

        return inner_args

    return inner


def exception_handler(log, quiet=True, message=None):
    def f_exception_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.exception(
                    "%s. Error: %s. Args: %s. Kwargs: %s"
                    % (message, str(e), args, kwargs)
                )
                if not quiet:
                    raise

        return wrapper

    return f_exception_handler


def get_top_relative_path(filepath, workspacepath=None):
    start = workspacepath or os.getcwd()
    start = os.path.abspath(start)
    return os.path.relpath(filepath, start)


def get_python_path():
    python_path = os.environ.get("PYTHONPATH")
    if python_path:
        python_paths = python_path.split(os.pathsep)
        # we're filtering out the agent's boostrap path in case we're running with the run command
        # the agent injects a python path we want to ignore
        bootstrap_path = bootstrap.__name__.replace(".", os.sep)
        python_paths = [path for path in python_paths if bootstrap_path not in path]
        python_path = python_paths[0] if python_paths else None
    return python_path


def to_str_obj(obj):
    return "\n".join("%s=%s" % (key, value) for key, value in obj.__dict__.items())


def to_str_obj_one_line(obj):
    line_format = "(%s)"
    arg_format = "%s=%s"
    return line_format % (
        ",".join(arg_format % (key, value) for key, value in obj.__dict__.items())
    )


def to_str_list(title, obj_list):
    """
    Creates a string representation of a given list  as a title and zero-based numbered entries:
    <title> :
    [0] <entry>
    ...
    [n=len-1] <entry>

    If a list entry has implemented method __str__ , it is called.
    Otherwise the default object reference is printed

    :param title:
    :param obj_list:
    :return:
    """
    to_str = title

    if len(obj_list) == 0:
        to_str += ": empty"
    else:
        line_format = "\t[%d]:\t%s"
        to_str += ":\n" + "\n".join(
            line_format % (index, e) for index, e in enumerate(obj_list)
        )

    return to_str


def to_str_dict(title, obj_dict):
    """
    Creates a string representation of a given dictionary as a title and zero-based numbered entries:
    <title> :
    [0] <key> -> <value>
    ...
    [n=len-1] <key> -> <value>

    If a dictionary key/value has implemented method __str__ , it is called.
    Otherwise the default object reference is printed

    :param title:
    :param obj_dict:
    :return:
    """
    to_str = title

    if len(obj_dict) == 0:
        to_str += ": empty"
    else:
        line_format = "\t[%d]:\t%s->%s"
        to_str += ":\n" + "\n".join(
            line_format % (index, key, obj_dict[key])
            for index, key in enumerate(obj_dict.keys())
        )

    return to_str


def trace(f, trace_function):
    @functools.wraps(f)
    def inner_trace(*args, **kwargs):
        value = f(*args, **kwargs)
        if isinstance(value, _DummyThread):
            sys.settrace(trace_function)
            threading.settrace(trace_function)
        return value

    return inner_trace


def generate_random_build_name():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )


class disableable:
    """
    This decorator skips method execution if config_data.isDisabled is true.
    This means that the agent failed to be configured correctly.
    This decorator should only be used inside a class as it assumes that the first arg is 'self'
    Args:
        config_data_name: the name of the config data member to check isDisabled against
        fail_silently: if True exits with exit code = 1 (unsuccessful)
    Returns: the wrapped function
    """

    def __init__(self, config_data_name="config_data", fail_silently=False):
        self.config_data_name = config_data_name
        self.fail_silently = fail_silently

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            instance = args[0] if args and len(args) > 0 else object()
            config_data = getattr(instance, self.config_data_name)
            if config_data and not config_data.isDisabled:
                return function(*args, **kwargs)
            # if config_data doesn't exist, the developer used the decorator wrong, do not run the function
            elif self.fail_silently:
                return
            sys.exit(1)

        return wrapper


class CommandType(Enum):
    TEST = "test"
    CONFIG = "config"
    SCAN = "scan"
    START = "start"
    RUN = "run"
    INIT = "init"
    OTHER = "other"
