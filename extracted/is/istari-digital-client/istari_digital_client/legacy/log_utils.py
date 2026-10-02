import functools
import logging
import inspect
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def log_method(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator that logs method calls, arguments, return values, and exceptions.
    Usage: @log_method (no parentheses)
    """
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        method_name = func.__qualname__

        try:
            bound = inspect.signature(func).bind(*args, **kwargs)
            bound.apply_defaults()
            args_to_log = {k: v for k, v in bound.arguments.items() if k != "self"}

            logger.debug(
                "Calling method: %s with arguments: %s",
                method_name,
                args_to_log,
                stacklevel=2,
            )

            result = func(*args, **kwargs)

            logger.debug(
                "Returned from method: %s with result: %r",
                method_name,
                result,
                stacklevel=2,
            )
            return result

        except Exception as exc_info:
            logger.exception(
                "Exception %s in method %s : %s",
                type(exc_info).__name__,
                method_name,
                exc_info,
                stacklevel=2,
            )
            raise

    return wrapper
