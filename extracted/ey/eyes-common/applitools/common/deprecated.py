from __future__ import absolute_import, division, print_function

import warnings
from functools import wraps
from inspect import getcallargs
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Optional, Text


def module(name, recommendation=None):
    # type: (Text, Optional[Text]) -> None
    message = "Module {} is deprecated".format(name)
    if recommendation:
        message += ": " + recommendation
    warnings.warn(message, stacklevel=2, category=ImportWarning)


def argument(name, recommendation):
    # type: (Text, Text) -> Callable[[Callable], Callable]
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            call_args = getcallargs(func, *args, **kwargs)
            argval = call_args.get(name)
            if argval is not None:
                message = "Argument {} of {} is deprecated: {}".format(
                    name, func.__name__, recommendation
                )
                warnings.warn(message, stacklevel=2, category=DeprecationWarning)
            return func(*args, **kwargs)

        return wrapped

    return wrapper


def attribute(recommendation):
    # type: (Text) -> Callable[[Callable], Callable]
    def wrapper(attr):
        @wraps(attr)
        def wrapped(*args, **kwargs):
            msg = "Use of {} is deprecated: {}".format(attr.__name__, recommendation)
            warnings.warn(msg, stacklevel=2, category=DeprecationWarning)
            return attr(*args, **kwargs)

        return wrapped

    return wrapper


warnings.filterwarnings("default", module="applitools")
