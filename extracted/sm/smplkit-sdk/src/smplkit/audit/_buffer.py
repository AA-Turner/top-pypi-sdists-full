"""Bounded in-memory buffer + worker thread for fire-and-forget audit emits.

ADR-047 §2.6. The buffer caps at ``MAX_BUFFER_SIZE`` to bound memory
consumption under sustained back-pressure. When full, the oldest queued
event is dropped to make room — recent events are more useful for
debugging than ancient ones, and the loss is acknowledged as part of the
async-emit trade-off.

Retry strategy: exponential backoff with jitter on transient failures
(connection errors, 5xx, 429). Permanent failures (4xx other than 429)
are logged and dropped. The retry budget per item is finite so a single
event can't block the queue indefinitely.

The buffer is HTTP-library-agnostic: ``post_fn`` returns either an
``int`` HTTP status code (when the generated client got a response)
or an ``Exception`` (transport failures, unexpected statuses, etc.).
"""

from __future__ import annotations

import logging
import random
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable

logger = logging.getLogger("smplkit.audit")

MAX_BUFFER_SIZE = 1000
PERIODIC_FLUSH_INTERVAL = 5.0  # seconds
HIGH_WATERMARK = 50  # flush eagerly once this many items are queued
MAX_ATTEMPTS_PER_ITEM = 5
INITIAL_BACKOFF = 0.25  # seconds
MAX_BACKOFF = 8.0  # seconds


@dataclass
class _PendingEvent:
    # Typed EventResponse from the generated client. We carry the
    # already-built model rather than a dict so a spec change that
    # drops a field shows up as a build/type error in the wrapper
    # construction site rather than as silently-emitted stale bytes
    # on the wire (the failure mode that shipped 3.2.21).
    body: Any
    idempotency_key: str | None
    attempts: int = 0
    next_retry_at: float = 0.0  # monotonic clock
    last_error: str | None = field(default=None)


class AuditEventBuffer:
    """Thread-safe bounded queue + flush worker for audit POSTs.

    The buffer owns a single daemon worker thread that wakes up on the
    periodic timer or when an enqueue tips the depth past the watermark.
    """

    def __init__(
        self,
        *,
        post_fn: Callable[[_PendingEvent], "int | Exception"],
        max_size: int = MAX_BUFFER_SIZE,
        flush_interval: float = PERIODIC_FLUSH_INTERVAL,
        watermark: int = HIGH_WATERMARK,
    ) -> None:
        self._post_fn = post_fn
        self._max_size = max_size
        self._flush_interval = flush_interval
        self._watermark = watermark
        self._queue: deque[_PendingEvent] = deque()
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._closed = False
        self._dropped_count = 0
        # ``_in_flight`` is the count of items the worker has popped from
        # the queue but not yet finished POSTing. flush() must wait on
        # both queue empty AND in_flight == 0 — otherwise it can return
        # while a just-popped item is still mid-roundtrip and an
        # immediately following list() call would miss the event.
        self._in_flight = 0
        self._worker = threading.Thread(target=self._run, name="smplkit-audit-flush", daemon=True)
        self._worker.start()

    # ------------------------------------------------------------------ public

    def enqueue(self, body: Any, idempotency_key: str | None = None) -> None:
        """Add an event to the buffer. May drop the oldest item if full."""
        with self._lock:
            if self._closed:
                return
            if len(self._queue) >= self._max_size:
                self._queue.popleft()
                self._dropped_count += 1
                logger.warning(
                    "audit buffer full (size=%d); dropped oldest event (total dropped=%d)",
                    self._max_size,
                    self._dropped_count,
                )
            self._queue.append(_PendingEvent(body=body, idempotency_key=idempotency_key))
            depth = len(self._queue)
        if depth >= self._watermark:
            self._wake.set()

    def flush(self, timeout: float | None = 5.0) -> None:
        """Drain the buffer synchronously. Used on shutdown.

        Returns when the buffer is idle (queue empty AND no in-flight
        POST) OR ``timeout`` elapses. The worker thread continues
        processing in parallel; the caller's flush is a cooperative
        drain rather than a takeover.
        """
        deadline = time.monotonic() + timeout if timeout is not None else None
        while True:
            with self._lock:
                if not self._queue and self._in_flight == 0:
                    return
            if deadline is not None and time.monotonic() >= deadline:
                logger.warning("audit buffer flush timed out (timeout=%.2fs)", timeout)
                return
            self._wake.set()
            time.sleep(0.05)

    def close(self, timeout: float | None = 5.0) -> None:
        """Mark closed, drain, then stop the worker thread."""
        self.flush(timeout=timeout)
        with self._lock:
            self._closed = True
        self._wake.set()
        self._worker.join(timeout=timeout)

    # ----------------------------------------------------------------- internals

    def _run(self) -> None:
        while True:
            with self._lock:
                if self._closed and not self._queue:
                    return

            self._drain_once()
            self._wake.wait(timeout=self._flush_interval)
            self._wake.clear()

    def _drain_once(self) -> None:
        """Send everything that's currently due. Re-queue retry items."""
        now = time.monotonic()
        retries: list[_PendingEvent] = []
        while True:
            with self._lock:
                if not self._queue:
                    break
                item = self._queue[0]
                if item.next_retry_at > now:
                    break
                self._queue.popleft()
                self._in_flight += 1

            try:
                outcome = self._post_fn(item)
            except Exception as exc:
                # Defensive — _post_fn shouldn't raise, but mark transient.
                outcome = exc

            handled = self._handle_outcome(item, outcome)
            with self._lock:
                self._in_flight -= 1
            if handled is not None:
                retries.append(handled)

        if retries:
            with self._lock:
                # Put retries back at the FRONT so they keep their slot in the
                # original ordering (oldest first); the worker re-checks
                # next_retry_at on the next pass.
                for item in reversed(retries):
                    self._queue.appendleft(item)

    def _handle_outcome(self, item: _PendingEvent, outcome: "int | Exception") -> _PendingEvent | None:
        """Decide whether an item is done, retried, or dropped."""
        # Success.
        if isinstance(outcome, int) and 200 <= outcome < 300:
            return None

        # Permanent failure — 4xx other than 429.
        if isinstance(outcome, int) and 400 <= outcome < 500 and outcome != 429:
            logger.warning("audit POST permanent failure: status=%d", outcome)
            return None

        # Transient failure — retry with exponential backoff.
        item.attempts += 1
        if isinstance(outcome, int):
            item.last_error = f"status={outcome}"
        else:
            item.last_error = repr(outcome)

        if item.attempts >= MAX_ATTEMPTS_PER_ITEM:
            logger.warning(
                "audit POST gave up after %d attempts (last_error=%s)",
                item.attempts,
                item.last_error,
            )
            return None

        backoff = min(MAX_BACKOFF, INITIAL_BACKOFF * (2 ** (item.attempts - 1)))
        jitter = random.uniform(0.0, backoff * 0.25)
        item.next_retry_at = time.monotonic() + backoff + jitter
        return item
