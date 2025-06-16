import asyncio
import typing as t
from collections import abc
from functools import partial, wraps

RET = t.TypeVar("RET")
P = t.ParamSpec("P")
SelfType = t.TypeVar("SelfType")


def sync_to_async(
    func: abc.Callable[t.Concatenate[SelfType, P], RET],
) -> abc.Callable[t.Concatenate[SelfType, P], abc.Awaitable[RET]]:
    """
    Utility decorator to convert a synchronous method into an asynchronous one.
    """

    @wraps(func)
    async def wrapper(self: SelfType, *args: P.args, **kwargs: P.kwargs) -> RET:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(func, self, *args, **kwargs))

    return wrapper
