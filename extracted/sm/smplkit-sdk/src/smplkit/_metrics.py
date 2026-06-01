"""Internal SDK telemetry engine.

Accumulates usage metrics in memory and periodically flushes them to the
app service via ``POST /api/v1/metrics/bulk``.  This module is entirely
private — nothing here is exported or documented for customers.
"""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class _Counter:
    """Mutable accumulator for a single metric series."""

    value: int = 0
    unit: str | None = None
    window_start: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class _MetricsReporter:
    """Synchronous metrics reporter.

    Accumulates counters/gauges in memory under a lock and flushes them
    to ``/api/v1/metrics/bulk`` on a periodic daemon timer.  All failures
    are swallowed — telemetry never throws, blocks, or degrades the
    customer's application.
    """

    def __init__(
        self,
        *,
        http_client: Any,
        environment: str,
        service: str,
        flush_interval: float = 60.0,
    ) -> None:
        self._http_client = http_client
        self._environment = environment
        self._service = service
        self._flush_interval = flush_interval

        self._counters: dict[tuple[str, frozenset[tuple[str, str]]], _Counter] = {}
        self._gauges: dict[tuple[str, frozenset[tuple[str, str]]], _Counter] = {}
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None
        self._closed = False

    # ------------------------------------------------------------------
    # Public recording API
    # ------------------------------------------------------------------

    def record(
        self,
        name: str,
        value: int = 1,
        unit: str | None = None,
        dimensions: dict[str, str] | None = None,
    ) -> None:
        """Increment a counter metric."""
        key = self._make_key(name, dimensions)
        with self._lock:
            if key not in self._counters:
                self._counters[key] = _Counter(unit=unit)
            counter = self._counters[key]
            counter.value += value
            if counter.unit is None and unit is not None:
                counter.unit = unit
            self._maybe_start_timer()

    def record_gauge(
        self,
        name: str,
        value: int,
        unit: str | None = None,
        dimensions: dict[str, str] | None = None,
    ) -> None:
        """Set a gauge metric (replaces rather than accumulates)."""
        key = self._make_key(name, dimensions)
        with self._lock:
            if key not in self._gauges:
                self._gauges[key] = _Counter(unit=unit)
            gauge = self._gauges[key]
            gauge.value = value
            if gauge.unit is None and unit is not None:
                gauge.unit = unit
            self._maybe_start_timer()

    # ------------------------------------------------------------------
    # Flush / close
    # ------------------------------------------------------------------

    def flush(self) -> None:
        """Synchronously flush accumulated metrics."""
        self._flush()

    def close(self) -> None:
        """Cancel the timer and flush one final time.  Idempotent."""
        if self._closed:
            return
        self._closed = True
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        self._flush()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _make_key(self, name: str, dimensions: dict[str, str] | None) -> tuple[str, frozenset[tuple[str, str]]]:
        merged: dict[str, str] = {
            "environment": self._environment,
            "service": self._service,
        }
        if dimensions:
            merged.update(dimensions)
        return (name, frozenset(merged.items()))

    def _maybe_start_timer(self) -> None:
        """Start the periodic flush timer if not already running.

        Must be called while ``self._lock`` is held.
        """
        if self._timer is None and not self._closed:
            self._start_timer()

    def _start_timer(self) -> None:
        self._timer = threading.Timer(self._flush_interval, self._tick)
        self._timer.daemon = True
        self._timer.start()

    def _tick(self) -> None:
        self._flush()
        with self._lock:
            self._timer = None
            if not self._closed:
                self._start_timer()

    def _flush(self) -> None:
        with self._lock:
            counters = self._counters
            gauges = self._gauges
            self._counters = {}
            self._gauges = {}

        if not counters and not gauges:
            return

        payload = self._build_payload(counters, gauges)
        try:
            httpx_client = self._http_client.get_httpx_client()
            httpx_client.post(
                "/api/v1/metrics/bulk",
                content=json.dumps(payload),
                headers={"Content-Type": "application/vnd.api+json"},
            )
        except Exception:
            logger.warning("Metrics flush failed", exc_info=True)

    def _build_payload(
        self,
        counters: dict[tuple[str, frozenset[tuple[str, str]]], _Counter],
        gauges: dict[tuple[str, frozenset[tuple[str, str]]], _Counter],
    ) -> dict[str, Any]:
        data: list[dict[str, Any]] = []
        for (name, dims_frozen), counter in counters.items():
            data.append(self._entry(name, counter, dims_frozen))
        for (name, dims_frozen), gauge in gauges.items():
            data.append(self._entry(name, gauge, dims_frozen))
        return {"data": data}

    def _entry(
        self,
        name: str,
        counter: _Counter,
        dims_frozen: frozenset[tuple[str, str]],
    ) -> dict[str, Any]:
        return {
            "type": "metric",
            "attributes": {
                "name": name,
                "value": counter.value,
                "unit": counter.unit,
                "period_seconds": int(self._flush_interval),
                "dimensions": dict(dims_frozen),
                "recorded_at": counter.window_start.isoformat(),
            },
        }


class _AsyncMetricsReporter:
    """Async-aware metrics reporter.

    ``record()`` and ``record_gauge()`` remain synchronous (no I/O, just
    dict mutations under a ``threading.Lock``).  Periodic flushes run on a
    daemon ``threading.Timer`` using sync HTTP (same pattern as
    ``LoggingClient``).  The explicit ``flush()`` and ``close()`` methods
    are ``async`` and use the async HTTP client.
    """

    def __init__(
        self,
        *,
        http_client: Any,
        environment: str,
        service: str,
        flush_interval: float = 60.0,
    ) -> None:
        self._http_client = http_client
        self._environment = environment
        self._service = service
        self._flush_interval = flush_interval

        self._counters: dict[tuple[str, frozenset[tuple[str, str]]], _Counter] = {}
        self._gauges: dict[tuple[str, frozenset[tuple[str, str]]], _Counter] = {}
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None
        self._closed = False

    # ------------------------------------------------------------------
    # Public recording API (sync — no I/O)
    # ------------------------------------------------------------------

    def record(
        self,
        name: str,
        value: int = 1,
        unit: str | None = None,
        dimensions: dict[str, str] | None = None,
    ) -> None:
        """Increment a counter metric."""
        key = self._make_key(name, dimensions)
        with self._lock:
            if key not in self._counters:
                self._counters[key] = _Counter(unit=unit)
            counter = self._counters[key]
            counter.value += value
            if counter.unit is None and unit is not None:
                counter.unit = unit
            self._maybe_start_timer()

    def record_gauge(
        self,
        name: str,
        value: int,
        unit: str | None = None,
        dimensions: dict[str, str] | None = None,
    ) -> None:
        """Set a gauge metric (replaces rather than accumulates)."""
        key = self._make_key(name, dimensions)
        with self._lock:
            if key not in self._gauges:
                self._gauges[key] = _Counter(unit=unit)
            gauge = self._gauges[key]
            gauge.value = value
            if gauge.unit is None and unit is not None:
                gauge.unit = unit
            self._maybe_start_timer()

    # ------------------------------------------------------------------
    # Flush / close (async)
    # ------------------------------------------------------------------

    async def flush(self) -> None:
        """Flush accumulated metrics using the async HTTP client."""
        await self._flush_async()

    async def close(self) -> None:
        """Cancel the timer and flush one final time.  Idempotent."""
        if self._closed:
            return
        self._closed = True
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        await self._flush_async()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _make_key(self, name: str, dimensions: dict[str, str] | None) -> tuple[str, frozenset[tuple[str, str]]]:
        merged: dict[str, str] = {
            "environment": self._environment,
            "service": self._service,
        }
        if dimensions:
            merged.update(dimensions)
        return (name, frozenset(merged.items()))

    def _maybe_start_timer(self) -> None:
        if self._timer is None and not self._closed:
            self._start_timer()

    def _start_timer(self) -> None:
        self._timer = threading.Timer(self._flush_interval, self._tick)
        self._timer.daemon = True
        self._timer.start()

    def _tick(self) -> None:
        self._flush_sync()
        with self._lock:
            self._timer = None
            if not self._closed:
                self._start_timer()

    def _snapshot(
        self,
    ) -> tuple[
        dict[tuple[str, frozenset[tuple[str, str]]], _Counter],
        dict[tuple[str, frozenset[tuple[str, str]]], _Counter],
    ]:
        with self._lock:
            counters = self._counters
            gauges = self._gauges
            self._counters = {}
            self._gauges = {}
        return counters, gauges

    def _flush_sync(self) -> None:
        """Sync flush used by the daemon timer thread."""
        counters, gauges = self._snapshot()
        if not counters and not gauges:
            return
        payload = self._build_payload(counters, gauges)
        try:
            httpx_client = self._http_client.get_httpx_client()
            httpx_client.post(
                "/api/v1/metrics/bulk",
                content=json.dumps(payload),
                headers={"Content-Type": "application/vnd.api+json"},
            )
        except Exception:
            logger.warning("Metrics flush failed", exc_info=True)

    async def _flush_async(self) -> None:
        """Async flush used by explicit flush()/close()."""
        counters, gauges = self._snapshot()
        if not counters and not gauges:
            return
        payload = self._build_payload(counters, gauges)
        try:
            httpx_client = self._http_client.get_async_httpx_client()
            await httpx_client.post(
                "/api/v1/metrics/bulk",
                content=json.dumps(payload),
                headers={"Content-Type": "application/vnd.api+json"},
            )
        except Exception:
            logger.warning("Metrics flush failed", exc_info=True)

    def _build_payload(
        self,
        counters: dict[tuple[str, frozenset[tuple[str, str]]], _Counter],
        gauges: dict[tuple[str, frozenset[tuple[str, str]]], _Counter],
    ) -> dict[str, Any]:
        data: list[dict[str, Any]] = []
        for (name, dims_frozen), counter in counters.items():
            data.append(self._entry(name, counter, dims_frozen))
        for (name, dims_frozen), gauge in gauges.items():
            data.append(self._entry(name, gauge, dims_frozen))
        return {"data": data}

    def _entry(
        self,
        name: str,
        counter: _Counter,
        dims_frozen: frozenset[tuple[str, str]],
    ) -> dict[str, Any]:
        return {
            "type": "metric",
            "attributes": {
                "name": name,
                "value": counter.value,
                "unit": counter.unit,
                "period_seconds": int(self._flush_interval),
                "dimensions": dict(dims_frozen),
                "recorded_at": counter.window_start.isoformat(),
            },
        }
