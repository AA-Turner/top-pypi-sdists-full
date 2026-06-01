"""OutcomeReport dataclass, StreamSink protocol, and OutcomeReporter with bounded queue."""

from __future__ import annotations

import collections
import enum
import logging
import os
import threading
from dataclasses import dataclass
from typing import Protocol

import aigie.telemetry as _telemetry
from aigie.autonomous.metrics import kytte_outcome_queue_dropped_total

logger = logging.getLogger(__name__)

tracer = _telemetry.get_tracer("aigie.autonomous")


class Status(enum.IntEnum):
    """Outcome status — values match the proto enum (ADR 0001 §5)."""

    APPLIED = 1
    FAILED = 2
    REVERTED = 3
    EXPIRED = 4


@dataclass(frozen=True, slots=True)
class OutcomeReport:
    """Immutable record of a remediation directive's outcome."""

    directive_id: str
    rule_id: str  # empty for novel-case judge directives
    remediation_plan_id: str
    plan_step_index: int  # -1 if not applicable
    status: Status
    next_span_ok: bool
    observed_at_unix_ms: int  # int for test simplicity; codec.py converts to proto Timestamp
    rule_cache_version: str
    reason: str  # free-form, used for FAILED/EXPIRED diagnostics
    # Span context: identifies the LLM span the outcome attaches to on the
    # dashboard. The proto OutcomeReport (v1) does not carry these fields,
    # so codec.py serialises them via a structured prefix in `reason`.
    # Defaults to "" for backward compatibility with tests and pre-existing
    # construction sites that do not have access to a span context.
    trace_id: str = ""
    span_id: str = ""
    # RemediationFlow linkage carried back from the directive that produced
    # this outcome. Empty / -1 when the directive was not flow-derived.
    flow_id: str = ""
    step_index: int = -1


class StreamSink(Protocol):
    """Fire-and-forget transport used by OutcomeReporter."""

    def send_outcome(self, outcome: OutcomeReport) -> None:
        """Send an outcome report; raises if transport is unavailable."""
        ...

    def is_connected(self) -> bool:
        """Return True when the underlying transport is usable."""
        ...


_DEFAULT_QUEUE_MAX = 10_000


class OutcomeReporter:
    """Buffers OutcomeReports in a bounded deque and drains them on reconnect."""

    def __init__(self, sink: StreamSink, max_queue: int | None = None) -> None:
        if max_queue is None:
            max_queue = int(os.environ.get("AIGIE_OUTCOME_QUEUE_MAX", _DEFAULT_QUEUE_MAX))
        self._sink = sink
        self._queue: collections.deque[OutcomeReport] = collections.deque(maxlen=max_queue)
        self._lock = threading.Lock()

    def report(self, outcome: OutcomeReport) -> None:
        """Enqueue an outcome; increment drop counter if the queue is at capacity."""
        with tracer.start_as_current_span("outcome.report") as span:
            span.set_attribute("directive_id", outcome.directive_id)
            span.set_attribute("rule_id", outcome.rule_id)
            span.set_attribute("status", outcome.status.name)
            span.set_attribute("reason", outcome.reason)
            self._report_inner(outcome, span)

    def _report_inner(self, outcome: OutcomeReport, span: object) -> None:
        with self._lock:
            at_capacity = len(self._queue) == self._queue.maxlen
            self._queue.append(outcome)
            size = len(self._queue)
        span.set_attribute("queue_depth", size)  # type: ignore[union-attr]
        if at_capacity:
            kytte_outcome_queue_dropped_total.inc()
        logger.debug(
            "Outcome REPORT: directive=%s rule=%s status=%s reason=%s queue=%d",
            outcome.directive_id,
            outcome.rule_id,
            outcome.status,
            outcome.reason,
            size,
        )
        if self._sink.is_connected():
            self._try_drain()

    def _try_drain(self) -> None:
        """Drain the queue while connected; restore head on send failure."""
        while self._queue and self._sink.is_connected():
            item = self._queue.popleft()
            try:
                self._sink.send_outcome(item)
            except Exception:
                self._queue.appendleft(item)
                break

    def on_connected(self) -> None:
        """Call after reconnect; schedules a background drain so the caller is not blocked."""
        t = threading.Thread(target=self._try_drain, daemon=True, name="aigie-outcome-drain")
        t.start()

    def stop(self, timeout: float = 5.0) -> None:
        """Best-effort drain with a timeout; returns regardless of remaining queue."""
        import time

        deadline = time.monotonic() + timeout
        while self._queue and self._sink.is_connected():
            if time.monotonic() >= deadline:
                break
            self._try_drain()

    def queue_size(self) -> int:
        """Return the current number of buffered outcomes."""
        return len(self._queue)
