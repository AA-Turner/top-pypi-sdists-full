"""Tracks utils."""

import functools
import threading
from collections.abc import Callable
from contextlib import suppress
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def fire_and_forget(func: Callable[P, T]) -> Callable[P, None]:  # noqa: UP047
    """Make a function fire-and-forget."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        def run() -> None:
            with suppress(Exception):
                func(*args, **kwargs)

        thread = threading.Thread(target=run)
        thread.start()

    return wrapper
