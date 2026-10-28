"""Progress events emitted by the transfer engine."""

from __future__ import annotations

import logging
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, replace
from enum import Enum
from threading import RLock
from time import monotonic
from traceback import walk_tb
from types import MethodType

logger = logging.getLogger("istari_digital_client.transfer")


class EventKind(str, Enum):
    """What a :class:`TransferEvent` reports; a ``str`` so ``event.kind == "part_done"`` also works."""

    HASH_PROGRESS = "hash_progress"
    PART_DONE = "part_done"
    RETRY = "retry"
    REPRESIGN = "represign"
    COMPLETE = "complete"
    ABORT = "abort"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class TransferEvent:
    """One progress notification.

    Transfer ``bytes_done`` is cumulative and nondecreasing across retries and fallback
    for one object. HASH_PROGRESS has its own, independent hashing counter.
    ``bytes_total`` is ``None`` only when the size is not yet known. ``part_number``,
    ``attempt`` and ``latency`` (seconds) are set for the events they apply to.
    COMPLETE means transfer success, not successful revision registration; ABORT
    reports multipart cleanup, not user cancellation. Callbacks run on transfer
    threads and should return promptly.
    """

    kind: EventKind
    bytes_done: int
    bytes_total: int | None
    part_number: int | None = None
    attempt: int | None = None
    latency: float | None = None


ProgressCallback = Callable[[TransferEvent], None]


class _CallbackLogCache:
    """Bound direct-callback warnings without retaining callbacks or their owners."""

    def __init__(
        self,
        capacity: int = 128,
        window: float = 60.0,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        """Keep at most ``capacity`` identities for ``window`` seconds each."""
        self._capacity: int = capacity
        self._window: float = window
        self._clock: Callable[[], float] = clock
        self._entries: OrderedDict[tuple[int, ...], float] = OrderedDict()
        self._lock: RLock = RLock()

    def should_log(self, progress: ProgressCallback) -> bool:
        """Atomically claim a warning slot, expiring and evicting old identities."""
        if isinstance(progress, MethodType):
            key: tuple[int, ...] = (id(progress.__self__), id(progress.__func__))
        else:
            key = (id(progress),)
        with self._lock:
            now = self._clock()
            while self._entries:
                _, expires = next(iter(self._entries.items()))
                if expires > now:
                    break
                _ = self._entries.popitem(last=False)
            if key in self._entries:
                return False
            if len(self._entries) >= self._capacity:
                _ = self._entries.popitem(last=False)
            self._entries[key] = now + self._window
            return True


_callback_logs = _CallbackLogCache()


def _log_callback_failure(error: Exception) -> None:
    """Log locations and type only, never exception text, chains or source lines."""
    locations = [
        f'  File "{frame.f_code.co_filename}", line {line}, in {frame.f_code.co_name}'
        for frame, line in walk_tb(error.__traceback__)
    ]
    diagnostic = "\n".join(
        ["Traceback (stack locations only):", *locations, type(error).__name__]
    )
    logger.warning("progress callback raised; ignoring\n%s", diagnostic)


def _is_forwarder(progress: ProgressCallback) -> bool:
    """Recognize internal dispatch, including freshly bound provisional methods."""
    return isinstance(progress, EventForwarder) or (
        isinstance(progress, MethodType)
        and isinstance(progress.__self__, EventForwarder)
    )


class EventForwarder:
    """Serialize one object's events across attempts and optional owner postchecks.

    Use ``provisional`` for lower layers when the caller still needs to verify the
    result, then send COMPLETE through this instance only after those checks pass.
    Separate content objects (including revision properties) need separate instances.
    """

    def __init__(
        self, progress: ProgressCallback | None, total: int | None = None
    ) -> None:
        """Keep the expected total and a transfer-only high-water count."""
        self._progress: ProgressCallback | None = progress
        self._total: int | None = total
        self._done: int = 0
        self._terminal: EventKind | None = None
        self._callback_failed: bool = False
        self._lock: RLock = RLock()

    def _deliver(self, event: TransferEvent) -> None:
        """Deliver under the operation lock, logging only its first consumer failure."""
        if self._progress is None:
            return
        if _is_forwarder(self._progress):
            self._progress(event)
            return
        try:
            self._progress(event)
        except Exception as error:  # noqa: BLE001 - user callbacks must not fail transfers
            if not self._callback_failed:
                self._callback_failed = True
                _log_callback_failure(error)

    def provisional(self, event: TransferEvent) -> None:
        """Forward lower-layer events except success awaiting owner postchecks."""
        if event.kind != EventKind.COMPLETE:
            self(event)

    def __call__(self, event: TransferEvent) -> None:
        """Normalize and deliver under one lock, swallowing consumer exceptions."""
        with self._lock:
            if event.kind == EventKind.HASH_PROGRESS:
                self._deliver(event)
                return
            if self._terminal is not None and event.kind != EventKind.ABORT:
                return
            if event.bytes_total is not None:
                if self._total is not None and event.bytes_total != self._total:
                    raise ValueError("transfer size differs from expected object size")
                if event.bytes_total < self._done:
                    raise ValueError("transfer size is smaller than reported progress")
                self._total = event.bytes_total
            done = max(self._done, event.bytes_done, 0)
            if self._total is not None:
                done = min(done, self._total)
            self._done = done
            if event.kind in (EventKind.COMPLETE, EventKind.CANCELLED):
                self._terminal = event.kind
            self._deliver(replace(event, bytes_done=done, bytes_total=self._total))


def emit(progress: ProgressCallback | None, event: TransferEvent) -> None:
    """Deliver on this thread; bound user warnings but propagate internal validation."""
    if progress is None:
        return
    if _is_forwarder(progress):
        progress(event)
        return
    try:
        progress(event)
    except Exception as error:  # noqa: BLE001 - user callbacks must not fail transfers
        if _callback_logs.should_log(progress):
            _log_callback_failure(error)
