from __future__ import annotations

import asyncio
import contextlib
import functools
import queue
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, AsyncIterable, AsyncIterator, Callable, Coroutine, Generic, Iterable, TypeVar, overload

from typing_extensions import ParamSpec

from chalk.utils.tracing import safe_activate_trace_context, safe_current_trace_context

T = TypeVar("T")
P = ParamSpec("P")
K = TypeVar("K")


@contextlib.asynccontextmanager
async def async_null_context(obj: T) -> AsyncIterator[T]:
    yield obj


async def async_enumerate(iterable: AsyncIterator[T] | AsyncIterable[T]):
    i = 0
    async for x in iterable:
        yield i, x
        i += 1


_RUNNING_TASKS: set[asyncio.Task[Any]] = set()


def run_coroutine_fn_threadsafe(
    loop: asyncio.AbstractEventLoop,
    coro_fn: Callable[P, Coroutine[Any, Any, T]],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Future[T]:
    """Similar to asyncio.run_coroutine_threadsafe(), but it constructs the coroutine inside the main event loop thread.
    This helps eliminate errors related to constructing coroutines that will never be awaited if the event loop is closed before
    the coroutine could be executed"""
    ans: Future[T] = Future()

    current_trace_context = safe_current_trace_context()

    def _run_on_event_loop_thread():
        if ans.set_running_or_notify_cancel():

            @functools.wraps(coro_fn)
            async def wrapped_with_context(*args: P.args, **kwargs: P.kwargs):
                try:
                    safe_activate_trace_context(current_trace_context)
                    res = await coro_fn(*args, **kwargs)
                except BaseException as exc:
                    ans.set_exception(exc)
                else:
                    ans.set_result(res)

            t = asyncio.create_task(wrapped_with_context(*args, **kwargs))
            _RUNNING_TASKS.add(t)
            t.add_done_callback(_RUNNING_TASKS.remove)
        else:
            ans.set_exception(RuntimeError("Future was cancelled"))

    loop.call_soon_threadsafe(_run_on_event_loop_thread)
    return ans


def _put_on_queue(
    loop: asyncio.AbstractEventLoop,
    q: asyncio.Queue[T | ellipsis],
    finished_event: threading.Event,
    x: T | ellipsis,
):
    if finished_event.is_set():
        return
    run_coroutine_fn_threadsafe(loop, q.put, x).result()


def _yield_to_queue(
    loop: asyncio.AbstractEventLoop,
    q: asyncio.Queue[T | ellipsis],
    finished_event: threading.Event,
    it: Iterable[T],
):
    try:
        for x in it:
            _put_on_queue(loop, q, finished_event, x)
    finally:
        _put_on_queue(loop, q, finished_event, ...)


class to_async_iterable(Generic[T]):
    """Runs a blocking iterator in an executor, and yields batches asynchronously as they become available.

    This function-like class runs the generator in a separate thread, and uses a queue to share results between the background thread
    and the event loop. This approach ensures that the generator context is spun with the correct parent
    """

    @overload
    def __init__(
        self,
        iterable: Iterable[T],
        executor: ThreadPoolExecutor | None = None,
        loop: None = None,
    ):
        ...

    @overload
    def __init__(
        self,
        iterable: Iterable[T],
        executor: ThreadPoolExecutor,
        loop: asyncio.AbstractEventLoop,
    ):
        ...

    def __init__(
        self,
        iterable: Iterable[T],
        executor: ThreadPoolExecutor | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ):
        super().__init__()
        self._q: asyncio.Queue[T | ellipsis] = asyncio.Queue(maxsize=2)
        self._finished_event = threading.Event()
        if isinstance(iterable, (list, tuple, set, frozenset)):
            # For simple containers we can iterate directly; no need to use a queue / task
            self._task = None
            self._loop = None
            self._iterator = iter(iterable)
        else:
            self._iterator = None
            if loop is None:
                self._loop = asyncio.get_running_loop()
                self._task = self._loop.run_in_executor(
                    executor,
                    _yield_to_queue,
                    self._loop,
                    self._q,
                    self._finished_event,
                    iterable,
                )
            else:
                assert executor is not None, "If the loop is provided, an executor must also be provided"
                self._loop = loop
                self._task = executor.submit(
                    _yield_to_queue,
                    self._loop,
                    self._q,
                    self._finished_event,
                    iterable,
                )

    def __aiter__(self):
        return self

    async def __anext__(self) -> T:
        if self._iterator is not None:
            element = next(self._iterator, ...)
            if element is ...:
                raise StopAsyncIteration
            else:
                return element
        assert self._task is not None
        try:
            item = await self._q.get()
        except asyncio.CancelledError:
            # If the task is cancelled, we still need to add something to the queue so the .get() call above doesn't hang
            # When the worker task finishes, it will either a) be before any code below runs, which is fine
            # because it is idempotent, or b) be after the the finished event is set, in which case we won't attempt to
            # append anything
            self._finished_event.set()
            try:
                self._q.put_nowait(...)
            except queue.Full:
                pass
            raise
        if item is ...:
            await asyncio.wrap_future(self._task, loop=self._loop)
            raise StopAsyncIteration
        return item

    def __del__(self):
        # If there was an exception, then the queue might still have an element in it
        # We'll first set the finished_event, and then we'll drain the queue. This will allow the
        # _yield_to_queue to successfully put another element in it, if _safe_put is blocked on q.put(...)
        # Because the finished_event is already set, it will not attempt to add yet another element, which would
        # block forever, because we aren't draining the queue any more
        # If there was no exception, then the queue should already be empty, and the task complete
        self._finished_event.set()
        try:
            if self._loop is not None:
                self._loop.call_soon_threadsafe(self._wrapped_get, self._q)
        except RuntimeError:
            pass

    @staticmethod
    def _wrapped_get(q: asyncio.Queue[T | ellipsis]):
        # Staticmethod so this doesn't hold a reference to self
        try:
            q.get_nowait()
        except asyncio.QueueEmpty:
            pass
