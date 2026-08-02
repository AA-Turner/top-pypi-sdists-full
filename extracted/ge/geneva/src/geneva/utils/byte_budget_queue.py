# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import queue
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class _ByteBudgetedQueueItem(Generic[T]):
    """An item whose byte reservation is released explicitly by the consumer."""

    item: T
    size_bytes: int
    _queue: ByteBudgetedQueue[T] = field(repr=False, compare=False)
    _released: bool = field(default=False, init=False, repr=False)

    def release(self) -> None:
        """Release this item's byte reservation.

        The release is intentionally separate from ``get`` so the queue budget
        covers both queued items and items currently held by the consumer.
        """
        with self._queue._condition:
            if self._released:
                return
            self._released = True
            self._queue._release_locked(self.size_bytes)


class ByteBudgetedQueue(Generic[T]):
    """FIFO queue with byte-aware producer backpressure.

    ``put(item, size_bytes)`` reserves ``size_bytes`` against the queue's byte
    budget. ``get()`` returns a leased item but does not release the reservation:
    callers must invoke ``lease.release()`` after the item has been fully
    consumed and any references that should count against the budget have been
    dropped. Until then, the budget covers both queued items and consumer-held
    leases.

    The budget is a backpressure threshold, not a hard admission limit. A
    producer may enqueue the item that crosses the threshold so the consumer can
    observe it and flush promptly; subsequent metered puts block until consumers
    release enough leased bytes.

    Example
    -------
        >>> q = ByteBudgetedQueue[str](max_bytes=1024)
        >>> q.put("batch-1", 900)
        >>> lease = q.get()
        >>> lease.item
        'batch-1'
        >>> q.outstanding_bytes
        900
        >>> lease.release()
        >>> q.outstanding_bytes
        0
    """

    def __init__(self, max_bytes: int) -> None:
        self._max_bytes = max(0, int(max_bytes))
        self._budget_enabled = self._max_bytes > 0
        self._condition = threading.Condition()
        self._items: deque[_ByteBudgetedQueueItem[T]] = deque()
        self._outstanding_bytes = 0

    @property
    def outstanding_bytes(self) -> int:
        """Return metered bytes currently queued or leased by consumers."""
        with self._condition:
            return self._outstanding_bytes

    def put(
        self,
        item: T,
        size_bytes: int,
        *,
        block: bool = True,
        timeout: float | None = None,
    ) -> None:
        """Put a metered item into the queue.

        Raises ``queue.Full`` if the byte budget is exceeded and the call is
        non-blocking or times out.
        """
        size_bytes = max(0, int(size_bytes))
        with self._condition:
            if not block and not self._can_accept_locked(size_bytes):
                raise queue.Full
            if timeout is not None and timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")

            endtime = None if timeout is None else time.perf_counter() + timeout
            while not self._can_accept_locked(size_bytes):
                if not block:
                    raise queue.Full
                if endtime is None:
                    self._condition.wait()
                    continue
                remaining = endtime - time.perf_counter()
                if remaining <= 0:
                    raise queue.Full
                self._condition.wait(remaining)

            self._put_locked(item, size_bytes, metered=True)

    def put_unmetered(self, item: T) -> None:
        """Put an item that does not consume byte budget."""
        with self._condition:
            self._put_locked(item, 0, metered=False)

    def get(
        self,
        block: bool = True,
        timeout: float | None = None,
    ) -> _ByteBudgetedQueueItem[T]:
        """Remove and return the next leased item.

        Raises ``queue.Empty`` with the same timeout semantics as
        ``queue.Queue.get``.
        """
        with self._condition:
            if timeout is not None and timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            if not block and not self._items:
                raise queue.Empty

            endtime = None if timeout is None else time.perf_counter() + timeout
            while not self._items:
                if not block:
                    raise queue.Empty
                if endtime is None:
                    self._condition.wait()
                    continue
                remaining = endtime - time.perf_counter()
                if remaining <= 0:
                    raise queue.Empty
                self._condition.wait(remaining)

            return self._items.popleft()

    def _can_accept_locked(self, size_bytes: int) -> bool:
        return (
            not self._budget_enabled
            or size_bytes <= 0
            or self._outstanding_bytes <= self._max_bytes
        )

    def _put_locked(self, item: T, size_bytes: int, *, metered: bool) -> None:
        lease = _ByteBudgetedQueueItem(item, size_bytes, self)
        self._items.append(lease)
        if metered and self._budget_enabled:
            self._outstanding_bytes += size_bytes
        self._condition.notify()

    def _release_locked(self, size_bytes: int) -> None:
        if self._budget_enabled and size_bytes > 0:
            self._outstanding_bytes -= size_bytes
            if self._outstanding_bytes < 0:
                raise RuntimeError(
                    "byte budget queue released more bytes than reserved"
                )
        self._condition.notify_all()
