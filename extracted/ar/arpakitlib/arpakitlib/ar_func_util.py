import asyncio
import inspect
from typing import Callable

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def is_async_func(func: Callable) -> bool:
    if inspect.ismethod(func) or inspect.isfunction(func):
        return inspect.iscoroutinefunction(func)
    if isinstance(func, (staticmethod, classmethod)):
        return inspect.iscoroutinefunction(func.__func__)
    return False


def raise_if_not_async_func(func: Callable):
    if not is_async_func(func):
        raise TypeError(f"the provided callable '{func.__name__}' is not an async")


# ---


def is_coroutine(obj: object) -> bool:
    return asyncio.iscoroutine(obj)


# ---


def is_sync_func(func: Callable) -> bool:
    return callable(func) and not is_async_func(func=func)


def raise_if_not_sync_func(func: Callable):
    if not is_sync_func(func):
        raise TypeError(f"the provided callable '{func.__name__}' is not an sync")


#


def get_func_name(func: Callable) -> str:
    return func.__name__


def __example():
    pass


if __name__ == '__main__':
    __example()
