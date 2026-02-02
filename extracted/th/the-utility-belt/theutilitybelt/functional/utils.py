from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def constant(val: T) -> Callable[..., T]:
    def fun(*_):
        return val

    fun.__name__ = f"constant_{val}"

    return fun


def identity(val: T) -> T:
    return val
