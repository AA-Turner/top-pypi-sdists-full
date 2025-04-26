import asyncio
import atexit
import functools
import os
import threading
from contextlib import contextmanager
from typing import Any, Awaitable, Callable, TypeVar

from flytekit.loggers import logger
from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")


@contextmanager
def _selector_policy():
    original_policy = asyncio.get_event_loop_policy()
    try:
        if os.name == "nt" and hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        yield
    finally:
        asyncio.set_event_loop_policy(original_policy)


class _TaskRunner:
    """A task runner that runs an asyncio event loop on a background thread."""

    def __init__(self) -> None:
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__runner_thread: threading.Thread | None = None
        self.__lock = threading.Lock()
        atexit.register(self._close)

    def _close(self) -> None:
        if self.__loop:
            self.__loop.stop()

    def _execute(self) -> None:
        loop = self.__loop
        assert loop is not None
        try:
            loop.run_forever()
        finally:
            loop.close()

    def run(self, coro: Any) -> Any:
        """Synchronously run a coroutine on a background thread."""
        name = f"{threading.current_thread().name} : loop-runner"
        with self.__lock:
            if self.__loop is None:
                with _selector_policy():
                    self.__loop = asyncio.new_event_loop()
                self.__runner_thread = threading.Thread(target=self._execute, daemon=True, name=name)
                self.__runner_thread.start()
        fut = asyncio.run_coroutine_threadsafe(coro, self.__loop)
        res = fut.result(None)

        return res


class _AsyncLoopManager:
    def __init__(self):
        self._runner_map: dict[str, _TaskRunner] = {}

    def run_sync(self, coro_func: Callable[..., Awaitable[T]], *args, **kwargs) -> T:
        """
        This should be called from synchronous functions to run an async function.
        """
        name = threading.current_thread().name + f"PID:{os.getpid()}"
        coro = coro_func(*args, **kwargs)
        if name not in self._runner_map:
            if len(self._runner_map) > 500:
                logger.warning(
                    "More than 500 event loop runners created!!! This could be a case of runaway recursion..."
                )
            self._runner_map[name] = _TaskRunner()
        return self._runner_map[name].run(coro)

    def synced(self, coro_func: Callable[P, Awaitable[T]]) -> Callable[P, T]:
        """Make loop run coroutine until it returns. Runs in other thread"""

        @functools.wraps(coro_func)
        def wrapped(*args: Any, **kwargs: Any) -> T:
            return self.run_sync(coro_func, *args, **kwargs)

        return wrapped


def exception_handler(loop: asyncio.AbstractEventLoop, context: dict) -> None:
    """Used by patch_exception_handler to patch BlockingIOError."""
    if (
        "exception" in context
        and type(context["exception"]).__name__ == "BlockingIOError"
        and str(context["exception"]).startswith("[Errno")
    ):
        return
    loop.default_exception_handler(context)


def patch_exception_handler(loop: asyncio.AbstractEventLoop) -> None:
    """Patch exception handler to ignore the `BlockingIOError: [Errno 11] ...` error.

    This is emitted by `aio.grpc` when multiple event loops are used in separate threads.
    This is an issue with grpc's cython implementation of `aio.Channel.__init__` where
    `socket.recv(1)` call only works on the first call. All subsequent calls result in
    an error, but this does not have any impact.

    For more info:
        - https://github.com/grpc/grpc/issues/25364
        - https://github.com/grpc/grpc/pull/36096
    """
    loop.set_exception_handler(exception_handler)


def _add_to_queue(queue, async_iter):
    assert hasattr(async_iter, "__aiter__")

    async def _aiter_to_queue(ait):
        async for i in async_iter:
            await queue.put(i)

    return _aiter_to_queue(async_iter)


async def merge(loop, *args):
    """Merge async generators into one stream."""
    queue = asyncio.Queue()
    iters = [_add_to_queue(queue, it) for it in args]
    futures = [asyncio.ensure_future(it, loop=loop) for it in iters]

    while True:
        if all(f.done() for f in futures) and queue.empty():
            return
        yield await queue.get()


loop_manager = _AsyncLoopManager()
run_sync = loop_manager.run_sync
