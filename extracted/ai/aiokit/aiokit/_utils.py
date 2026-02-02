import asyncio
import inspect
import sys
import types
from functools import singledispatch, wraps
from typing import Any, Callable, Generator

PY35 = sys.version_info >= (3, 5)


def _is_awaitable(co: Generator[Any, None, Any]) -> bool:
    if PY35:
        return inspect.isawaitable(co)
    else:
        return isinstance(co, types.GeneratorType) or isinstance(co, asyncio.Future)


@singledispatch
def sync(co: Any):
    raise TypeError("Called with unsupported argument: {}".format(co))


@sync.register(asyncio.Future)
@sync.register(types.GeneratorType)
def sync_co(co: Generator[Any, None, Any]) -> Any:
    if not _is_awaitable(co):
        raise TypeError("Called with unsupported argument: {}".format(co))
    return asyncio.get_event_loop().run_until_complete(co)


@sync.register(types.FunctionType)
@sync.register(types.MethodType)
def sync_fu(f: Callable[..., Any]) -> Callable[..., Any]:
    if not asyncio.iscoroutinefunction(f):
        raise TypeError("Called with unsupported argument: {}".format(f))

    @wraps(f)
    def run(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return run


async def wait_first(*futures):
    tasks = [
        asyncio.create_task(f) if not isinstance(f, asyncio.Task) else f
        for f in futures
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    result = done.pop()
    if result.exception() and pending:
        return wait_first(*pending)
    gather = asyncio.gather(*pending)
    gather.cancel()
    try:
        await gather
    except asyncio.CancelledError:
        pass
    return result.result()
