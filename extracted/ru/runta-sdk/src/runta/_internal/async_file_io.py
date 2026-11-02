"""Bounded client-owned file operations with cancellation-safe draining."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import os
from typing import Any, Callable, Iterator


def file_io_worker_count(value: int | None) -> int:
    if value is not None:
        if type(value) is not int or value <= 0:
            raise ValueError("file_io_workers must be a positive integer or None")
        return value
    count = None
    process_count = getattr(os, "process_cpu_count", None)
    if process_count is not None:
        try:
            count = process_count()
        except (OSError, NotImplementedError):
            pass
    if count is None:
        try:
            count = len(os.sched_getaffinity(0))
        except (AttributeError, OSError, NotImplementedError):
            count = os.cpu_count()
    return min(32, (count or 1) + 4)


async def finish_worker(future: asyncio.Future) -> Any:
    """Drain despite repeated cancellation, then propagate the first cancellation."""
    cancelled = None
    while not future.done():
        try:
            await asyncio.shield(future)
        except asyncio.CancelledError as exc:
            cancelled = cancelled or exc
        except BaseException:
            break
    if cancelled is not None:
        # Retrieve any exception, so cancelled callers leave no orphan errors.
        if not future.cancelled():
            future.exception()
        raise cancelled
    return future.result()


class _AsyncFileIO:
    def __init__(self, workers: int | None, bind_loop: Callable[[], Any]) -> None:
        self.workers = file_io_worker_count(workers)
        self._bind_loop = bind_loop
        self._executor: ThreadPoolExecutor | None = None
        self._slots: asyncio.Semaphore | None = None
        self._leases = 0
        self._closed = False

    @contextmanager
    def lease(self) -> Iterator[_AsyncFileIO]:
        if self._closed:
            raise RuntimeError("AsyncRunta is closed")
        self._bind_loop()
        self._leases += 1
        try:
            yield self
        finally:
            self._leases -= 1
            self._shutdown_if_unused()

    async def run(self, operation: Callable[..., Any], *args: Any) -> Any:
        if not self._leases:
            raise RuntimeError("File I/O requires an active download lease")
        if self._slots is None:
            self._slots = asyncio.Semaphore(self.workers)
        async with self._slots:
            if self._executor is None:
                self._executor = ThreadPoolExecutor(
                    max_workers=self.workers, thread_name_prefix="runta-file-io"
                )
            future = asyncio.wrap_future(self._executor.submit(operation, *args))
            # Keep the permit until the underlying operation really completes.
            return await finish_worker(future)

    def close(self) -> None:
        self._closed = True
        self._shutdown_if_unused()

    def _shutdown_if_unused(self) -> None:
        if self._closed and not self._leases and self._executor is not None:
            # All lease operations have drained; no blocking join on the loop.
            self._executor.shutdown(wait=False)
