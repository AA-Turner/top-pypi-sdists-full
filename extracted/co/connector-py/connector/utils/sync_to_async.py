import asyncio
import typing as t
from collections import abc
from functools import wraps

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
        # to_thread, not run_in_executor: it copies the current contextvars into the
        # worker thread. The host binds request metadata (app_id, capability, trace)
        # as contextvars, and logging filters read them off the current context, so
        # anything logged from a bare executor thread arrives unattributed.
        return await asyncio.to_thread(func, self, *args, **kwargs)

    return wrapper
