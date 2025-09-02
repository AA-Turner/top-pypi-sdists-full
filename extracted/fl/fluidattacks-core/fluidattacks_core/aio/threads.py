import asyncio
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


async def to_thread(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """Asynchronously run a function in a separate thread.

    The underlying ThreadPoolExecutor sets a maximum number of worker threads
    based on the number of cores.

    See: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
    """
    return await asyncio.to_thread(func, *args, **kwargs)
