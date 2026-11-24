"""A decorator in its own module: a wrapper's ``__globals__`` must not be the tool's own module."""

from __future__ import annotations

import functools
from typing import Any


def passthrough(func: Any) -> Any:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        return await func(*args, **kwargs)

    return wrapper
