import asyncio
import contextvars
import functools
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

PROCESS_POOL = ProcessPoolExecutor()


async def to_process(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """Asynchronously run a function in a separate process.

    The underlying ProcessPoolExecutor sets a maximum number of worker processes
    based on the number of cores.

    See: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor
    """
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(PROCESS_POOL, func_call)
