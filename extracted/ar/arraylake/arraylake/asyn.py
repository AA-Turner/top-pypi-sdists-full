# Portions of this module were adapted from fsspec.
# https://github.com/fsspec/filesystem_spec/blob/4eeba2ba2da6ec39ac98fa7e02af53b208446106/fsspec/asyn.py
# Fsspec is licensed under the BSD 3-Clause License with the following copyright notice:
#     BSD 3-Clause License

#     Copyright (c) 2018, Martin Durant
#     All rights reserved.

#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are met:

#     * Redistributions of source code must retain the above copyright notice, this
#       list of conditions and the following disclaimer.

#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.

#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.

#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import asyncio
import sys
import threading
from collections.abc import Awaitable, Callable, Coroutine, Iterable
from contextlib import contextmanager
from functools import cache
from typing import Any, TypeVar

from arraylake.config import config as config_obj
from arraylake.log_util import get_logger

logger = get_logger(__name__)

# dedicated IO thread
iothread: list[threading.Thread | None] = [None]

# global event loop to run on that thread
loop: list[asyncio.AbstractEventLoop | None] = [None]

# global lock placeholder
# threading.Lock is not usable as a proper type hint prior to 3.13, but
# works if you use quotes!
# https://github.com/python/cpython/issues/114315#issuecomment-1911141288
_lock: "threading.Lock | None" = None


T = TypeVar("T")

PageableFunction = Callable[..., Awaitable[tuple[Iterable[T], "PageableFunction"]]]


# NOTE: Properly type hinting this is impossible at the moment
# https://discuss.python.org/t/pre-pep-considerations-and-feedback-type-transformations-on-variadic-generics/50605
async def async_gather_tasks(*coroutines: Coroutine[Any, Any, T]) -> list[T]:
    """
    Run coroutines concurrently using TaskGroup, returning ordered results.

    Like asyncio.gather() but uses TaskGroup for better error handling
    and guaranteed task cleanup.

    Raises an ExecptionGroup if multiple requests failed, otherwise an unwrapped exception if only one failed.
    """
    try:
        async with asyncio.TaskGroup() as tg:
            tasks: list[asyncio.Task[T]] = [tg.create_task(coro) for coro in coroutines]

        return [task.result() for task in tasks]
    except BaseException as e:
        # TaskGroup wraps exceptions in ExceptionGroup, but we want to unwrap
        # single exceptions to maintain compatibility with asyncio.gather()
        if isinstance(e, BaseExceptionGroup) and len(e.exceptions) == 1:
            raise e.exceptions[0] from None
        raise


def get_lock() -> threading.Lock:
    """Allocate or return a threading lock.

    The lock is allocated on first use to allow setting one lock per forked process.
    """
    global _lock
    if _lock is None:
        _lock = threading.Lock()
    return _lock


async def _runner(event: threading.Event, coro: Coroutine, result: list[Any], timeout: int | None = None) -> None:
    timeout = timeout if timeout else None
    if timeout is not None:
        coro = asyncio.wait_for(coro, timeout=timeout)
    try:
        result[0] = await coro
    except Exception as ex:
        result[0] = ex
    finally:
        event.set()


def sync(func: Callable, *args, timeout: int | None = None, **kwargs) -> Any:
    """
    Make loop run coroutine until it returns. Runs in other thread (`iothread`)
    """
    sync_loop = get_loop()
    timeout = timeout or None  # convert 0 or 0.0 to None
    # If the loop is not running *yet*, it is OK to submit work and we will wait for it.
    # When an event loop is created, it is not yet running. It has to be explicitly run (e.g. run_forever or
    # run_until_complete. If the event loop is closed, however, it can never run anything again, so an error
    # is appropriate.
    if sync_loop.is_closed():
        raise RuntimeError("Loop is closed")
    # note: the following code was feature-flagged due to an observation that this check was overly aggressive
    # in blocking alternative event loops operating in the same runtime. we're maintaining the default state
    # because we don't fully understand why this code should exist, if it is indeed critical to our async approach
    # we should make it obvious to the next developer that ends up debugging here.
    disable_loop_check = config_obj.get("disable_async_loop_check", False)
    if not disable_loop_check:
        try:
            loop0 = asyncio.events.get_running_loop()
            if loop0 is sync_loop:
                # This is not just a sanity check. This is a guard against calling sync from an already sync'd async
                # function, which would could trigger the async equivalent of a black hole singularity--some sort of
                # deeply inconsistent race condition in which a thread is waiting for itself to finish.
                raise NotImplementedError("Calling sync() from within a running loop")
        except NotImplementedError:
            raise
        except RuntimeError:
            # this can be hit during shutdown
            pass
    coro = func(*args, **kwargs)
    result = [None]
    event = threading.Event()
    asyncio.run_coroutine_threadsafe(_runner(event, coro, result, timeout), sync_loop)
    while True:
        # this loop allows thread to get interrupted
        if event.wait(1):
            break
        if timeout is not None:
            timeout -= 1
            if timeout < 0:
                raise RuntimeError("Operation timed out")

    return_result = result[0]
    if isinstance(return_result, BaseException):
        # note: fsspec has special handling for asyncio.TimeoutError; here we just raise it
        raise return_result
    else:
        return return_result


@contextmanager
def loop_selector_policy():
    """
    A context manager that temporarily changes the event loop policy to a specific selector policy
    when running on Windows or when uvloop is available.
    """

    original_policy = asyncio.get_event_loop_policy()
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        else:
            try:
                import uvloop

                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            except ImportError:
                pass
        yield
    finally:
        asyncio.set_event_loop_policy(original_policy)


def get_loop() -> asyncio.AbstractEventLoop:
    """Create or return the default arraylake IO loop

    The loop will be running on a separate thread.
    """
    if loop[0] is None:
        with get_lock():
            # repeat the check just in case the loop got filled between the
            # previous two calls from another thread
            if loop[0] is None:
                with loop_selector_policy():
                    # mypy doesn't link this line
                    #  No overload variant of "__setitem__" of "list" matches argument types "int", "AbstractEventLoop"
                    loop[0] = asyncio.new_event_loop()
                # mypy can't tell that loop[0] is not None here
                th = threading.Thread(target=loop[0].run_forever, name="arraylake")  # type: ignore
                th.daemon = True
                th.start()
                iothread[0] = th
    # mypy can't tell that loop[0] is not None here
    # this can likely be removed after we drop support for Python 3.8
    if loop[0] is None:
        raise ValueError("failed to get loop")
    return loop[0]


@cache
def get_background_loop() -> asyncio.AbstractEventLoop:
    """Create a background event loop.

    The loop will be running on a separate thread.
    """

    def _start_background_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    new_loop = asyncio.new_event_loop()
    logger.debug("Starting background loop with ID %s", id(new_loop))
    loop_thread = threading.Thread(target=_start_background_loop, args=(new_loop,), daemon=True)
    loop_thread.start()

    return new_loop


def asyncio_run(coro: Coroutine[Any, Any, T], timeout=30) -> T:
    """
    Runs the coroutine in an event loop running on a background thread,
    and blocks the current thread until it returns a result.

    Taken from:
    https://stackoverflow.com/questions/52232177/runtimeerror-timeout-context-manager-should-be-used-inside-a-task/69514930#69514930

    Args:
        coro: A coroutine, typically an async method
        timeout: How many seconds we should wait for a result before raising an error
    """
    return asyncio.run_coroutine_threadsafe(coro, get_background_loop()).result(timeout=timeout)


async def close_async_context(context, message=""):
    """Close an async context and log a message."""
    # print("Closing async context for %s. %s", context, message)
    await context.__aexit__(None, None, None)
