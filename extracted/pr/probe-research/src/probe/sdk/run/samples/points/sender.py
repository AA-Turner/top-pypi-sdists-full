"""A training worker's per-sample metrics, sent as its own producer (`<adapter>-train-<rank>`) from a background
thread: joining the run (`attach_producer`, a network call) and every send happen there, so an optimizer update never
waits on the network. Fails open: a worker that cannot join trains unrecorded."""

from __future__ import annotations

import atexit
import collections
import logging
import threading
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from probe.foundation.compat.compat import StrEnum

logger = logging.getLogger(__name__)

#: Updates held while the join is in flight; past it the newest are dropped (counted), training never waits.
MAX_QUEUED_UPDATES = 1024
#: How long the process's exit waits for what is queued.
EXIT_FLUSH_SECONDS = 30.0


class _Item(StrEnum):
    """What a queued item sends."""

    UPDATE = "update"
    PLAN = "plan"


def _attach(producer: str) -> Any:
    from ..producer import attach_producer

    return attach_producer(producer, should_sample_hardware=False, should_capture_logs=False)


class PointsSender:
    """One worker process's sender. ``start(producer)`` begins joining (once); ``send`` queues an update's rows and
    records and ``send_plan`` a training declaration, both returning at once; ``flush`` waits for the queue (a test,
    or the process's exit); ``close`` flushes, stops the thread and lets go of everything it held (a trainer that
    finished in a long-lived process, a notebook)."""

    def __init__(self, framework: str, *, attach: Callable[[str], Any] = _attach) -> None:
        self.framework = framework
        self.run: Any = None
        self.is_disabled = False
        self.dropped_updates = 0
        self._attach = attach
        self._queue: collections.deque = collections.deque()
        self._condition = threading.Condition()
        self._is_sending = False
        self._is_closed = False
        self._has_warned_drop = False
        self._thread: threading.Thread | None = None

    def start(self, producer: str) -> None:
        with self._condition:
            if self._thread is not None or self.is_disabled or self._is_closed:
                return
            self._thread = threading.Thread(target=self._run, args=(producer,), name=f"probe-{producer}", daemon=True)
            atexit.register(self.flush, EXIT_FLUSH_SECONDS)  # under the lock, never after a close; a job shorter
            thread = self._thread  # than its join still waits for it (moved after the join's own release in `_run`)
        thread.start()

    def send(self, step: int, update: int | None, rows: Sequence[Mapping[str, Any]],
             records: Sequence[Mapping[str, Any]]) -> None:  # fmt: skip
        with self._condition:
            if self.is_disabled or self._is_closed:
                return
            if len(self._queue) >= MAX_QUEUED_UPDATES:
                self.dropped_updates += 1
                if not self._has_warned_drop:
                    self._has_warned_drop = True
                    logger.warning("Probe's %s sender is %d updates behind (the run is not joined yet, or sends are "
                                   "slow): newer updates are dropped and read missing", self.framework,
                                   MAX_QUEUED_UPDATES)  # fmt: skip
                return
            self._queue.append((_Item.UPDATE, (step, update, list(rows), list(records))))
            self._condition.notify_all()

    def send_plan(self, training: Mapping[str, Any]) -> None:
        """Queue this producer's training declaration (`run.samples.plan(training=...)`), in order with its updates."""
        with self._condition:
            if self.is_disabled or self._is_closed:
                return
            self._queue.append((_Item.PLAN, dict(training)))
            self._condition.notify_all()

    def flush(self, timeout: float) -> Any:
        """Wait until everything queued is sent (or the join failed, or the sender closed or never started); returns
        the run, None when not joined. On the sender's own thread it never waits (it is the one sending)."""
        if threading.current_thread() is self._thread:
            return self.run
        with self._condition:
            self._condition.wait_for(lambda: self.is_disabled or self._is_closed or self._thread is None
                                     or (self.run is not None and not self._queue and not self._is_sending),
                                     timeout)  # fmt: skip
            return self.run

    def close(self, timeout: float = EXIT_FLUSH_SECONDS) -> None:
        """Flush, then stop the thread, release this producer's lease (as its exit would) and drop what it held (the
        attach function and the run), so a trainer that finished is freed in a long-lived process; later sends are
        ignored. Safe to call twice, before the join finished, or from the sender's own thread."""
        self.flush(timeout)
        with self._condition:
            self._is_closed = True
            self._queue.clear()
            self._condition.notify_all()
            atexit.unregister(self.flush)  # under the lock: a join finishing now sees `_is_closed` and never re-adds it
            run, thread = self.run, self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=1.0)
        if run is not None:
            from ..producer import release_producer

            release_producer(run)
        self._attach, self.run = None, None

    # -- the background thread ---------------------------------------------------------------------------
    def _run(self, producer: str) -> None:
        try:
            run = self._attach(producer)
        except Exception as exc:  # noqa: BLE001 -- fail open: the worker trains unrecorded
            logger.warning("Probe could not join the run from this %s worker; its per-sample training metrics are "
                           "not recorded and %s continues: %s", self.framework, self.framework, exc)  # fmt: skip
            with self._condition:
                self.is_disabled = True
                self._queue.clear()
                self._condition.notify_all()
            return
        with self._condition:
            is_closed = self._is_closed
            if not is_closed:
                atexit.unregister(self.flush)  # again after the join's own release, so it runs first (LIFO)
                atexit.register(self.flush, EXIT_FLUSH_SECONDS)
                self.run = run
                self._condition.notify_all()
        if is_closed:  # closed while joining: no exit hook again, and the lease goes now (outside the lock)
            from ..producer import release_producer

            release_producer(run)
            return
        while True:
            with self._condition:
                self._condition.wait_for(lambda: bool(self._queue) or self._is_closed)
                if self._is_closed:
                    return
                kind, item = self._queue.popleft()
                self._is_sending = True
            try:
                if kind is _Item.PLAN:
                    run.samples.plan(training=item)
                else:
                    self._send_now(run, *item)
            except Exception as exc:  # noqa: BLE001 -- one item lost, never the thread
                what = "its training declaration" if kind is _Item.PLAN else "an update's per-sample training metrics"
                logger.warning("Probe could not send %s: %s", what, exc)
            finally:
                with self._condition:
                    self._is_sending = False
                    self._condition.notify_all()

    @staticmethod
    def _send_now(run: Any, step: int, update: int | None, rows: list, records: list) -> None:
        if rows:
            run.samples.log_metrics_many(rows)
        for record in records:
            run.samples.log_update(step, update, **record)
