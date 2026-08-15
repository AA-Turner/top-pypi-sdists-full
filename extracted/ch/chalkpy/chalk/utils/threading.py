from __future__ import annotations

import asyncio
import contextvars
import functools
import os
import queue
import threading
import weakref
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Final, ParamSpec, TypeVar

DESIRED_CPU_PARALLELISM: int = int(os.getenv("OMP_NUM_THREADS", max(8, os.cpu_count() or 8)))
"""
The desired cpu parallelism. os.cpu_count() should never be used on k8s, as it returns the total
number of cores on the node rather than the requested cpu count from the pod manifest.
Rarely would os.cpu_count() return None, but falling back to 8 in that case.

We set a minimum bound of 8 for DESIRED_CPU_PARALLELISM because arrow can deadlock if initialized with too few threads.
"""


class MultiSemaphore:
    """Semaphore-like class that takes a value for both acquire and release"""

    def __init__(self, value: int = 1, /) -> None:
        super().__init__()
        self._value = value
        self.initial_value: Final = value
        self._cond = threading.Condition()

    def get_value(self):
        return self._value

    def acquire(self, val: int = 1, /, *, block: bool = True, timeout: float | None = None):
        if val <= 0:
            raise ValueError(f"Value ({val}) is not positive")
        if val > self.initial_value:
            raise ValueError(f"Value ({val}) is greater than the initial value ({self.initial_value})")
        if timeout is not None and timeout < 0:
            raise ValueError(f"Timeout ({timeout}) is negative, which is not supported")
        if not block:
            if timeout:
                raise ValueError("If `block` is False, then the timeout must not be specified (or be 0)")
            timeout = 0
        with self._cond:
            self._cond.wait_for(lambda: self._value - val >= 0, timeout)
            if self._value - val >= 0:
                self._value -= val
                return True
            return False

    def release(self, val: int):
        if val <= 0:
            raise ValueError(f"Value ({val}) is not positive")
        with self._cond:
            if self._value + val > self.initial_value:
                raise ValueError(f"Value ({val}) would put the semaphore above the initial value.")
            self._value += val
            # notify_all, not notify: "there is capacity now" does not mean "the first waiter
            # can use it". A single notification handed to a waiter that still wants more than
            # is available is consumed and lost, and the waiter that could have proceeded is
            # never woken -- which, since callers acquire without a timeout, strands it for good.
            self._cond.notify_all()


def shutdown_prefetch_workers(
    pending_work: queue.Queue[Any],
    prefetched: queue.Queue[Any],
    sem: MultiSemaphore | None,
    workers: dict[Any, Future[Any]],
) -> None:
    """Stop a pool of prefetch workers and give back every semaphore weight they still hold.

    The warehouse integrations prefetch query results with a fan-out of download workers
    bounded by a `MultiSemaphore`: a worker acquires a chunk's weight *before* downloading it,
    and that weight is only returned once the consumer pulls the chunk off `prefetched`. So a
    consumer that stops draining -- because it raised, or because its generator was closed --
    strands both the weight and the workers, which then block in `sem.acquire()` forever and
    never return their threads to `DEFAULT_IO_EXECUTOR`. That pool is process-wide, so the
    damage outlives the query: once it is empty, later queries' workers never start at all.

    Call this on *every* exit from a prefetch loop. A loop that finished normally has already
    emptied `workers`, which makes this a no-op.
    """
    # Stop handing out new work, so each worker exits once it finishes its current chunk.
    while True:
        try:
            pending_work.get_nowait()
        except queue.Empty:
            break
    # Drain what the workers have produced, or are still about to produce, releasing as we go.
    # The releases are what let a worker parked in `acquire` wake up and reach its exit, so
    # draining and releasing have to be interleaved rather than done one after the other.
    #
    # This terminates: every worker puts its id in a `finally`, and a worker can only be
    # blocked on weight that some other chunk is holding -- which this loop is handing back.
    while len(workers) > 0:
        item = prefetched.get()
        if isinstance(item, int):
            # A worker id, meaning that worker has exited. Deliberately not calling .result():
            # we may already be unwinding the consumer's exception, and the normal path checks
            # worker results itself.
            workers.pop(item, None)
            continue
        _, weight = item
        if sem is not None and weight > 0:
            sem.release(weight)


__all__ = ["ChalkThreadPoolExecutor"]

P = ParamSpec("P")
T = TypeVar("T")


class _ThreadlocalData(threading.local):
    parent_thread_pools: weakref.WeakSet[  # pyright: ignore[reportUninitializedInstanceVariable]
        ChalkThreadPoolExecutor
    ]


_threadlocal_data = _ThreadlocalData()


class ChalkThreadPoolExecutor(ThreadPoolExecutor):
    """Implementation of :class:`ThreadPoolExecutor` that adds trace context propagation,
    log context propagation, an asyncio hook, and thread pool checks."""

    def __init__(
        self,
        max_workers: int | None = None,
        thread_name_prefix: str = "",
        initializer: Callable[..., object] | None = None,
        initargs: tuple[Any, ...] = (),
    ) -> None:
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)

    if __debug__:

        def submit(  # pyright: ignore[reportRedeclaration]
            self, fn: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
        ) -> Future[T]:
            """Submit a new task to the thread pool."""
            if not hasattr(_threadlocal_data, "parent_thread_pools"):
                _threadlocal_data.parent_thread_pools = weakref.WeakSet()

            if self in _threadlocal_data.parent_thread_pools:
                raise RuntimeError(
                    (
                        "Attempted to submit a task to a thread pool from a thread spawned by the same thread pool. "
                        "This is a logic error which can lead to deadlocks."
                    )
                )
            # Copy the thread pool references and include `self` this time
            new_parent_thread_pools = weakref.WeakSet((*_threadlocal_data.parent_thread_pools, self))
            current_context = contextvars.copy_context()

            @functools.wraps(fn)
            def wrapped_fn(*args: P.args, **kwargs: P.kwargs):
                _threadlocal_data.parent_thread_pools = new_parent_thread_pools
                # Setting _merge=False to override the existing context,
                # in case if there is context left behind in the current thread from a previous
                # task
                return fn(*args, **kwargs)

            return super().submit(current_context.run, wrapped_fn, *args, **kwargs)

    else:
        # If not debug mode, skipping the reenetrency checking
        def submit(self, fn: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> Future[T]:
            """Submit a new task to the thread pool."""
            current_context = contextvars.copy_context()
            return super().submit(current_context.run, fn, *args, **kwargs)

    async def submit_async(self, fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return await asyncio.get_running_loop().run_in_executor(self, functools.partial(fn, *args, **kwargs))


DEFAULT_IO_EXECUTOR = ChalkThreadPoolExecutor(
    max_workers=int(os.getenv("CHALK_IO_EXECUTOR_MAX_WORKERS", "32")),
    thread_name_prefix="chalk-io-",
)
