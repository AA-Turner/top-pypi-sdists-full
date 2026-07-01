"""
threatwire.core.event_bus
=========================
ThreatEventBus — pub/sub event router for threat alerts.

Features:
  - Synchronous and async handler registration
  - Alert deduplication with configurable cooldown windows
  - Severity-based routing (subscribe to HIGH+ only, etc.)
  - Structured JSON output compatible with ECS and MITRE ATT&CK field mapping
  - Rolling summary events for volumetric attacks (DDoS amplification)

Attack scenario addressed:
    DDoS amplification generates 50,000 UDP alerts/sec, flooding handlers and
    causing legitimate critical alerts to be dropped.
    ThreatEventBus deduplicates amplification into a single rolling summary,
    ensuring critical lateral-movement alerts route immediately.
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from collections import defaultdict
from collections.abc import Coroutine
from dataclasses import dataclass, field
from typing import Any, Callable, Union

from threatwire.core.models import AlertSeverity, ThreatAlert

logger = logging.getLogger(__name__)

HandlerFn = Union[
    Callable[[ThreatAlert], None],
    Callable[[ThreatAlert], Coroutine[Any, Any, None]],
]


# ---------------------------------------------------------------------------
# Subscription descriptor
# ---------------------------------------------------------------------------

@dataclass
class Subscription:
    handler: HandlerFn
    min_severity: AlertSeverity = AlertSeverity.INFO
    rule_ids: list[str] = field(default_factory=list)     # empty = all rules
    tactic_ids: list[str] = field(default_factory=list)   # empty = all tactics
    is_async: bool = False

    def matches(self, alert: ThreatAlert) -> bool:
        if alert.severity < self.min_severity:
            return False
        if self.rule_ids and alert.rule_id not in self.rule_ids:
            return False
        if self.tactic_ids and alert.tactic_id not in self.tactic_ids:
            return False
        return True


# ---------------------------------------------------------------------------
# Dedup state
# ---------------------------------------------------------------------------

@dataclass
class DedupEntry:
    first_seen: float
    last_seen: float
    count: int = 1
    suppressed: int = 0


# ---------------------------------------------------------------------------
# Rolling summary for volumetric events
# ---------------------------------------------------------------------------

@dataclass
class VolumeSummary:
    """Emitted periodically instead of flooding handlers with identical alerts."""
    dedup_key: str
    rule_id: str
    rule_name: str
    severity: AlertSeverity
    src_ip: str
    dst_ip: str
    total_events: int
    suppressed_events: int
    window_start: float
    window_end: float

    def to_dict(self) -> dict:
        return {
            "type": "volume_summary",
            "dedup_key": self.dedup_key,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "severity": self.severity.value,
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
            "total_events": self.total_events,
            "suppressed_events": self.suppressed_events,
            "window_start": self.window_start,
            "window_end": self.window_end,
        }


# ---------------------------------------------------------------------------
# ThreatEventBus
# ---------------------------------------------------------------------------

class ThreatEventBus:
    """
    Pub/sub event router for ThreatAlert objects.

    Usage::

        bus = ThreatEventBus(dedup_window=30)

        @bus.subscribe(severity="critical")
        async def on_critical(alert):
            await siem.ingest(alert.to_ecs())

        @bus.subscribe(severity="high", rule_ids=["TW-C2-001"])
        def on_c2(alert):
            slack.notify(f"C2 beacon: {alert.src_ip}")

        bus.start()

        # Publish alerts (thread-safe)
        bus.publish(alert)

        bus.stop()

    Or use as a context manager::

        with ThreatEventBus() as bus:
            bus.publish(alert)
    """

    def __init__(
        self,
        dedup_window: float = 30.0,
        volume_summary_interval: float = 60.0,
        volume_threshold: int = 100,       # alerts/window before summaries kick in
        max_queue_size: int = 10_000,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self.dedup_window = dedup_window
        self.volume_summary_interval = volume_summary_interval
        self.volume_threshold = volume_threshold
        self.max_queue_size = max_queue_size

        self._subscriptions: list[Subscription] = []
        self._dedup: dict[str, DedupEntry] = {}
        self._volume_state: dict[str, list[float]] = defaultdict(list)
        self._volume_summaries: dict[str, list[ThreatAlert]] = defaultdict(list)

        self._lock = threading.Lock()
        self._queue: list[ThreatAlert] = []
        self._running = False
        self._worker_thread: threading.Thread | None = None

        # Async event loop (for async handlers)
        self._loop = loop or asyncio.new_event_loop()

    # ------------------------------------------------------------------
    # Subscription API
    # ------------------------------------------------------------------

    def subscribe(
        self,
        severity: str | AlertSeverity = "info",
        rule_ids: list[str] | None = None,
        tactic_ids: list[str] | None = None,
    ) -> Callable[[HandlerFn], HandlerFn]:
        """
        Decorator to register an alert handler.

            @bus.subscribe(severity="high")
            def my_handler(alert): ...

            @bus.subscribe(severity="critical")
            async def async_handler(alert): ...
        """
        min_sev = AlertSeverity(severity) if isinstance(severity, str) else severity

        def decorator(fn: HandlerFn) -> HandlerFn:
            sub = Subscription(
                handler=fn,
                min_severity=min_sev,
                rule_ids=rule_ids or [],
                tactic_ids=tactic_ids or [],
                is_async=asyncio.iscoroutinefunction(fn),
            )
            self._subscriptions.append(sub)
            logger.debug("Registered handler %s (severity>=%s)", fn.__name__, min_sev.value)
            return fn

        return decorator

    def add_handler(
        self,
        handler: HandlerFn,
        severity: str | AlertSeverity = "info",
        rule_ids: list[str] | None = None,
        tactic_ids: list[str] | None = None,
    ) -> None:
        """Programmatic alternative to the @subscribe decorator."""
        min_sev = AlertSeverity(severity) if isinstance(severity, str) else severity
        sub = Subscription(
            handler=handler,
            min_severity=min_sev,
            rule_ids=rule_ids or [],
            tactic_ids=tactic_ids or [],
            is_async=asyncio.iscoroutinefunction(handler),
        )
        self._subscriptions.append(sub)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the background worker thread for dispatching alerts."""
        if self._running:
            return
        self._running = True
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name="threatwire-event-bus",
        )
        self._worker_thread.start()
        logger.info("ThreatEventBus started (%d subscriptions)", len(self._subscriptions))

    def stop(self, timeout: float = 5.0) -> None:
        """Stop the worker thread, flushing remaining queued alerts."""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=timeout)
        logger.info("ThreatEventBus stopped")

    def __enter__(self) -> ThreatEventBus:
        self.start()
        return self

    def __exit__(self, *_) -> None:
        self.stop()

    # ------------------------------------------------------------------
    # Publishing
    # ------------------------------------------------------------------

    def publish(self, alert: ThreatAlert) -> bool:
        """
        Enqueue an alert for dispatch.
        Thread-safe. Returns False if the queue is full (backpressure).
        Deduplication is applied before queueing.
        """
        with self._lock:
            if not self._should_dispatch(alert):
                return False
            if len(self._queue) >= self.max_queue_size:
                logger.warning(
                    "ThreatEventBus queue full (%d). Dropping alert %s.",
                    self.max_queue_size, alert.rule_id,
                )
                return False
            self._queue.append(alert)
        return True

    def publish_many(self, alerts: list[ThreatAlert]) -> int:
        """Publish multiple alerts. Returns count of successfully queued alerts."""
        return sum(1 for a in alerts if self.publish(a))

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    def _should_dispatch(self, alert: ThreatAlert) -> bool:
        """
        Apply deduplication logic.
        High-volume identical alerts are collapsed into rolling summaries.
        Critical-severity alerts always pass through.
        """
        now = alert.timestamp or time.time()
        key = alert.dedup_key or f"{alert.rule_id}:{alert.src_ip}:{alert.dst_ip}"

        entry = self._dedup.get(key)

        if entry is None:
            self._dedup[key] = DedupEntry(first_seen=now, last_seen=now)
            return True

        # Expired dedup window — reset and dispatch
        if now - entry.last_seen > self.dedup_window:
            self._dedup[key] = DedupEntry(first_seen=now, last_seen=now)
            return True

        entry.last_seen = now
        entry.count += 1

        # Track volume for summary generation
        self._volume_state[key].append(now)

        # Critical alerts always pass, even if deduped
        if alert.severity == AlertSeverity.CRITICAL:
            return True

        # Non-critical duplicates within window are suppressed
        entry.suppressed += 1
        self._volume_summaries[key].append(alert)

        # Periodically emit a volume summary instead
        window_alerts = self._volume_state[key]
        if len(window_alerts) >= self.volume_threshold:
            self._emit_volume_summary(key, alert, entry)
            self._volume_state[key] = []
            self._volume_summaries[key] = []

        return False

    def _emit_volume_summary(
        self, key: str, sample_alert: ThreatAlert, entry: DedupEntry
    ) -> None:
        summary = VolumeSummary(
            dedup_key=key,
            rule_id=sample_alert.rule_id,
            rule_name=sample_alert.rule_name,
            severity=sample_alert.severity,
            src_ip=sample_alert.src_ip,
            dst_ip=sample_alert.dst_ip,
            total_events=entry.count,
            suppressed_events=entry.suppressed,
            window_start=entry.first_seen,
            window_end=entry.last_seen,
        )
        logger.info("Volume summary: %s", summary.to_dict())
        # Notify summary-aware handlers
        for sub in self._subscriptions:
            if hasattr(sub.handler, "_accepts_summary"):
                self._call_handler(sub.handler, summary)  # type: ignore

    # ------------------------------------------------------------------
    # Worker loop
    # ------------------------------------------------------------------

    def _worker_loop(self) -> None:
        while self._running or self._queue:
            batch: list[ThreatAlert] = []
            with self._lock:
                if self._queue:
                    batch = self._queue.copy()
                    self._queue.clear()

            for alert in batch:
                self._dispatch(alert)

            if not batch:
                time.sleep(0.001)   # 1ms idle sleep

    def _dispatch(self, alert: ThreatAlert) -> None:
        for sub in self._subscriptions:
            if not sub.matches(alert):
                continue
            try:
                self._call_handler(sub.handler, alert)
            except Exception as exc:
                logger.error("Handler %s raised: %s", sub.handler.__name__, exc, exc_info=True)

    def _call_handler(self, handler: HandlerFn, payload: Any) -> None:
        if asyncio.iscoroutinefunction(handler):
            future = asyncio.run_coroutine_threadsafe(handler(payload), self._loop)
            future.result(timeout=10.0)
        else:
            handler(payload)  # type: ignore

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        with self._lock:
            return {
                "queue_depth": len(self._queue),
                "subscriptions": len(self._subscriptions),
                "dedup_entries": len(self._dedup),
                "running": self._running,
            }
