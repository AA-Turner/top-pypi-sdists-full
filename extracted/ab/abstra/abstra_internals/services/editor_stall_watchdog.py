"""Whole-process scheduling stall detector for the web editor.

A daemon thread sleeps a fixed interval and measures how late it actually
wakes up. When the process cannot schedule any Python thread (GIL held by
native code, or the container CPU-throttled), the wake-up is delayed by
roughly the stall duration — the same starvation that makes /_healthcheck
time out for the kubelet liveness probe and for the frontend watcher that
sends users back to the console. A stall can only be reported after it
ends: while it lasts, this thread is starved too.

Stalls at or above `threshold_seconds` are batched and emitted as a single
`editor.stall` lifecycle event per episode: consecutive stalls accumulate
(keeping every individual duration) and the batch is flushed on the first
on-time wake-up after a stall (the episode ended), when the batch window
expires while stalls keep coming (bounds volume to one event per window on
a pathologically stalling pod), or on stop() (graceful shutdown mid-burst).
No data is dropped — only grouped.

Opening an episode also emits an `editor.stall_started` marker so a live
observer (kubectl logs -f, Kibana) sees the trouble at the first recovery
instead of only at the episode summary. The marker is a duplicate of the
episode's first stall by design: measurement queries must count only
`editor.stall` events.
"""

import threading
import time
from typing import Any, Callable, Dict, List, Optional

from abstra_internals.environment import (
    EDITOR_STALL_WATCHDOG_BATCH_WINDOW_SECONDS,
    EDITOR_STALL_WATCHDOG_INTERVAL_SECONDS,
    EDITOR_STALL_WATCHDOG_THRESHOLD_SECONDS,
)
from abstra_internals.logger import AbstraLogger

Emit = Callable[[str, Dict[str, Any]], None]

# AbstraLogger.lifecycle relies on os.write atomicity up to PIPE_BUF (4096
# bytes); capping the reported durations keeps the line safely below that
# even with an env-configured giant window. stallCount/stallTotalSeconds
# stay exact regardless of truncation.
MAX_REPORTED_STALLS = 100


class EditorStallWatchdog:
    def __init__(
        self,
        *,
        interval_seconds: Optional[float] = None,
        threshold_seconds: Optional[float] = None,
        batch_window_seconds: Optional[float] = None,
        monotonic: Callable[[], float] = time.monotonic,
        emit: Optional[Emit] = None,
    ):
        self._interval = (
            interval_seconds
            if interval_seconds is not None
            else EDITOR_STALL_WATCHDOG_INTERVAL_SECONDS
        )
        self._threshold = (
            threshold_seconds
            if threshold_seconds is not None
            else EDITOR_STALL_WATCHDOG_THRESHOLD_SECONDS
        )
        self._batch_window = (
            batch_window_seconds
            if batch_window_seconds is not None
            else EDITOR_STALL_WATCHDOG_BATCH_WINDOW_SECONDS
        )
        self._monotonic = monotonic
        self._emit: Emit = emit or AbstraLogger.lifecycle

        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._last_wake = 0.0
        # Guards the batch state: ticks run on the watchdog thread, but
        # stop() flushes from the shutdown thread.
        self._batch_lock = threading.Lock()
        self._batch_started_at: Optional[float] = None
        self._batch_stalls: List[float] = []

    def _run(self) -> None:
        self._last_wake = self._monotonic()
        # Event.wait returns True as soon as stop() is called, so shutdown
        # is near-instant; a timeout (False) is a normal tick.
        while not self._stop_event.wait(self._interval):
            self._tick(self._monotonic())
            # Re-stamp after the tick so time spent emitting (os.write can
            # block on log backpressure) is not measured as a process stall
            # on the next wake-up.
            self._last_wake = self._monotonic()

    def _tick(self, now: float) -> None:
        delay = now - self._last_wake - self._interval
        self._last_wake = now
        with self._batch_lock:
            if delay >= self._threshold:
                if self._batch_started_at is None:
                    self._batch_started_at = now - delay
                    self._emit_started(delay)
                self._batch_stalls.append(delay)
                if now - self._batch_started_at >= self._batch_window:
                    self._flush(now)
            elif self._batch_stalls:
                # First on-time wake-up after a burst: the episode ended.
                self._flush(now)

    def _emit_started(self, first_stall_seconds: float) -> None:
        try:
            self._emit(
                "[Editor] Stall episode started",
                {
                    "stage": "editor.stall_started",
                    "stallSeconds": round(first_stall_seconds, 3),
                    "thresholdSeconds": self._threshold,
                },
            )
        except Exception:
            # The watchdog must never die on a reporting failure.
            pass

    def _flush(self, now: float) -> None:
        """Emit and reset the pending batch. Callers hold _batch_lock."""
        stalls = self._batch_stalls
        started_at = self._batch_started_at
        self._batch_stalls = []
        self._batch_started_at = None
        if not stalls or started_at is None:
            return

        attrs: Dict[str, Any] = {
            "stage": "editor.stall",
            "stallCount": len(stalls),
            "stallTotalSeconds": round(sum(stalls), 3),
            "stallMaxSeconds": round(max(stalls), 3),
            "stallsSeconds": [round(s, 3) for s in stalls[:MAX_REPORTED_STALLS]],
            "episodeSeconds": round(now - started_at, 3),
            "thresholdSeconds": self._threshold,
        }
        try:
            self._emit("[Editor] Process stall detected", attrs)
        except Exception:
            # The watchdog must never die on a reporting failure; the
            # batch was already reset, so a broken emitter cannot loop.
            pass

    def start(self) -> None:
        if self._thread is not None:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="EditorStallWatchdog",
            daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        self._stop_event.set()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=timeout)
            self._thread = None
        # Don't lose an in-progress burst on SIGTERM (scale-down or
        # liveness kill); SIGKILL/OOM is unrecoverable by nature. But never
        # hang the shutdown on it either: if the watchdog thread is wedged
        # inside emit holding the lock, skip the final flush.
        if self._batch_lock.acquire(timeout=1.0):
            try:
                self._flush(self._monotonic())
            finally:
                self._batch_lock.release()
