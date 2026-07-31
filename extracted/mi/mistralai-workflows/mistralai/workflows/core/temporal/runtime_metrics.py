"""Temporal Rust-core runtime metrics via a MetricBuffer drained in-process.

The Rust-core OTLP exporter bakes its auth header once and can't refresh it, so it goes stale under a
rotating SA token. Instead the worker attaches a ``MetricBuffer`` (no auth) and ``pump_runtime_metrics``
re-emits through the Python OTel pipeline, which rotates its bearer per export. Only the worker runs the
pump, so only it gets a buffer — an undrained buffer fills and drops updates.

TODO: Remove once Temporal handles SA for metrics (then the Rust-core exporter can push directly and this
whole buffer/pump bridge, plus the dedicated worker_id-free MeterProvider, can go away).
"""

import asyncio
import math
import time
from typing import NamedTuple

import structlog
from opentelemetry.metrics import Counter, Histogram, Meter, _Gauge
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View
from temporalio.runtime import (
    BUFFERED_METRIC_KIND_COUNTER,
    BUFFERED_METRIC_KIND_GAUGE,
    BUFFERED_METRIC_KIND_HISTOGRAM,
    BufferedMetricUpdate,
    MetricBuffer,
    MetricBufferDurationFormat,
    OpenTelemetryConfig,
    Runtime,
    TelemetryConfig,
)

from mistralai.workflows._version import __version__
from mistralai.workflows.core.auth import TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.tracing._otel_config import (
    TELEMETRY_DISTRO_NAME_ATTRIBUTE,
    TELEMETRY_DISTRO_VERSION_ATTRIBUTE,
    WORKER_SERVICE_NAME,
    WORKFLOWS_TELEMETRY_DISTRO_NAME,
)
from mistralai.workflows.exceptions import WorkflowError

logger = structlog.get_logger(__name__)

TEMPORAL_RUNTIME_METRIC_GLOBAL_TAGS = {
    "service.name": WORKER_SERVICE_NAME,
    "component.type": "worker",
    TELEMETRY_DISTRO_NAME_ATTRIBUTE: WORKFLOWS_TELEMETRY_DISTRO_NAME,
    TELEMETRY_DISTRO_VERSION_ATTRIBUTE: __version__,
}

# Core prefixes its runtime metrics with ``temporal_``; we normalize idempotently.
_METRIC_PREFIX = "temporal_"

# Per-instrument histogram buckets (le, ms) captured from the live series to match core's; re-capture if
# core's histogram config changes. (Python owns bucketing on the buffer path.)
TEMPORAL_HISTOGRAM_BOUNDARIES: dict[str, list[float]] = {
    "temporal_workflow_endtoend_latency": [
        100.0,
        500.0,
        1000.0,
        1500.0,
        2000.0,
        5000.0,
        10000.0,
        30000.0,
        60000.0,
        120000.0,
        300000.0,
        600000.0,
        1800000.0,
        3600000.0,
        30600000.0,
        86400000.0,
    ],
    "temporal_activity_execution_latency": [50.0, 100.0, 500.0, 1000.0, 5000.0, 10000.0, 60000.0],
    "temporal_activity_succeed_endtoend_latency": [50.0, 100.0, 500.0, 1000.0, 2500.0, 10000.0],
    "temporal_activity_schedule_to_start_latency": [100.0, 500.0, 1000.0, 5000.0, 10000.0, 100000.0, 1000000.0],
    "temporal_local_activity_execution_latency": [50.0, 100.0, 500.0, 1000.0, 5000.0, 10000.0, 60000.0],
    "temporal_local_activity_succeed_endtoend_latency": [50.0, 100.0, 500.0, 1000.0, 2500.0, 10000.0],
    "temporal_long_request_latency": [50.0, 100.0, 500.0, 1000.0, 2500.0, 10000.0],
    "temporal_request_latency": [50.0, 100.0, 500.0, 1000.0, 2500.0, 10000.0],
    "temporal_workflow_task_execution_latency": [1.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
    "temporal_workflow_task_replay_latency": [1.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
    "temporal_workflow_task_schedule_to_start_latency": [100.0, 500.0, 1000.0, 5000.0, 10000.0, 100000.0, 1000000.0],
}

_Instrument = Counter | _Gauge | Histogram


class RuntimeBundle(NamedTuple):
    runtime: Runtime
    metric_buffer: MetricBuffer | None


def _runtime_global_tags() -> dict[str, str]:
    return {**TEMPORAL_RUNTIME_METRIC_GLOBAL_TAGS, "service.version": config.common.app_version}


def build_runtime() -> RuntimeBundle:
    """Build the worker's Temporal Runtime with a MetricBuffer for the pump to drain.

    Only the worker calls this — it runs ``pump_runtime_metrics``, which is why it can use a buffer (needed
    for rotating credentials). Pump-less callers use ``build_client_runtime`` instead.
    """
    if not (config.common.otel_enabled and config.common.mistral_workflows_otel_metrics_export):
        return RuntimeBundle(Runtime(telemetry=TelemetryConfig()), None)

    buffer = MetricBuffer(
        config.common.temporal_runtime_metrics_buffer_size,
        MetricBufferDurationFormat.MILLISECONDS,
    )
    runtime = Runtime(
        telemetry=TelemetryConfig(metrics=buffer, global_tags=_runtime_global_tags(), attach_service_name=False)
    )
    return RuntimeBundle(runtime, buffer)


class _MetricsAuth(NamedTuple):
    disable: bool
    headers: dict[str, str] | None


def _resolve_metrics_auth(provider: TokenProvider | None) -> _MetricsAuth:
    # Static credential (reuse == inf) bakes a durable bearer; rotating/unreadable can't, so disable.
    if provider is None:
        return _MetricsAuth(disable=False, headers=None)
    try:
        token, reuse = provider.get_token_with_max_age()
    except WorkflowError:
        return _MetricsAuth(disable=True, headers=None)
    if not math.isinf(reuse):
        return _MetricsAuth(disable=True, headers=None)
    return _MetricsAuth(disable=False, headers={"Authorization": f"Bearer {token}"})


def _build_otlp_runtime(metrics_base: str, *, headers: dict[str, str] | None) -> Runtime:
    return Runtime(
        telemetry=TelemetryConfig(
            metrics=OpenTelemetryConfig(url=f"{metrics_base}/v1/metrics", http=True, headers=headers),
            global_tags=_runtime_global_tags(),
            attach_service_name=False,
        )
    )


def build_client_runtime() -> Runtime:
    """Build a Runtime for pump-less callers (API/webhook clients).

    They can't drain a buffer, so they use the Rust-core OTLP exporter directly — it self-exports, needing
    no drainer. That works for a static credential or an explicitly configured endpoint. A rotating or
    unreadable credential can't bake a durable auth header, so runtime metrics are disabled for that caller.
    """
    if not (config.common.otel_enabled and config.common.mistral_workflows_otel_metrics_export):
        return Runtime(telemetry=TelemetryConfig())

    explicit_endpoint = config.common.otel_endpoint or config.common.otel_metrics_endpoint
    if explicit_endpoint:
        return _build_otlp_runtime(explicit_endpoint, headers=None)

    auth = _resolve_metrics_auth(get_token_provider(config.worker.agent.mistral_client_api_key))
    if auth.disable:
        return Runtime(telemetry=TelemetryConfig())
    assert config.worker.agent.mistral_client_server_url is not None  # guaranteed by WorkerConfig validator
    metrics_base = f"{config.worker.agent.mistral_client_server_url.rstrip('/')}/telemetry"
    return _build_otlp_runtime(metrics_base, headers=auth.headers)


def build_temporal_metric_views() -> list[View]:
    """One histogram View per instrument, pinning its bucket boundaries (matched by name)."""
    return [
        View(instrument_name=name, aggregation=ExplicitBucketHistogramAggregation(boundaries=boundaries))
        for name, boundaries in TEMPORAL_HISTOGRAM_BOUNDARIES.items()
    ]


def _normalize_name(name: str) -> str:
    return name if name.startswith(_METRIC_PREFIX) else _METRIC_PREFIX + name


def _get_instrument(
    meter: Meter, cache: dict[tuple[str, int], _Instrument], update: BufferedMetricUpdate
) -> _Instrument:
    metric = update.metric
    name = _normalize_name(metric.name)
    key = (name, metric.kind)
    instrument = cache.get(key)
    if instrument is None:
        if metric.kind == BUFFERED_METRIC_KIND_COUNTER:
            instrument = meter.create_counter(name, unit=metric.unit or "", description=metric.description or "")
        elif metric.kind == BUFFERED_METRIC_KIND_GAUGE:
            instrument = meter.create_gauge(name, unit=metric.unit or "", description=metric.description or "")
        elif metric.kind == BUFFERED_METRIC_KIND_HISTOGRAM:
            if name not in TEMPORAL_HISTOGRAM_BOUNDARIES:
                # No pinned View -> Python default buckets, which won't match core's.
                logger.warning("temporal runtime histogram has no pinned bucket boundaries", metric=name)
            instrument = meter.create_histogram(name, unit=metric.unit or "", description=metric.description or "")
        else:
            raise ValueError(f"unknown buffered metric kind {metric.kind!r} for {name}")
        cache[key] = instrument
    return instrument


def _dispatch(instrument: _Instrument, update: BufferedMetricUpdate) -> None:
    attributes = dict(update.attributes)
    if isinstance(instrument, Counter):
        instrument.add(update.value, attributes)  # buffered counter values are deltas
    elif isinstance(instrument, _Gauge):
        instrument.set(update.value, attributes)
    else:
        instrument.record(update.value, attributes)


# A drained batch this close to the buffer size means core may be dropping updates (it drops silently when full).
_BUFFER_NEAR_CAPACITY_RATIO = 0.8
_BUFFER_WARN_INTERVAL_SECONDS = 60.0


def _drain(meter: Meter, cache: dict[tuple[str, int], _Instrument], buffer: MetricBuffer) -> int:
    count = 0
    for update in buffer.retrieve_updates():
        count += 1
        try:
            _dispatch(_get_instrument(meter, cache, update), update)
        except Exception as exc:
            logger.warning(
                "failed to re-emit a buffered temporal runtime metric; skipping",
                metric=update.metric.name,
                **extract_error_context(exc),
                exc_info=exc,
            )
    return count


async def pump_runtime_metrics(
    buffer: MetricBuffer,
    meter: Meter,
    *,
    interval_s: float,
    meter_provider: MeterProvider,
    buffer_size: int,
) -> None:
    """Drain the buffer on an interval and re-emit through the Python meter; final drain + flush on cancel.
    Warns (throttled) when a drained batch nears ``buffer_size`` — the only signal core may be dropping."""
    cache: dict[tuple[str, int], _Instrument] = {}
    near_capacity = max(1, int(buffer_size * _BUFFER_NEAR_CAPACITY_RATIO))
    last_capacity_warn = 0.0
    try:
        while True:
            # Runtime metrics are non-critical: a buffer/drain error must never abort the worker's TaskGroup.
            try:
                drained = _drain(meter, cache, buffer)
            except Exception as exc:
                drained = 0
                logger.warning(
                    "failed to drain temporal runtime metrics; continuing",
                    **extract_error_context(exc),
                    exc_info=exc,
                )
            now = time.monotonic()
            if drained >= near_capacity and now - last_capacity_warn >= _BUFFER_WARN_INTERVAL_SECONDS:
                last_capacity_warn = now
                logger.warning(
                    "temporal runtime metrics buffer near capacity; core may be dropping updates",
                    drained=drained,
                    buffer_size=buffer_size,
                )
            await asyncio.sleep(interval_s)
    except asyncio.CancelledError:
        # Best-effort final drain + flush; never let it mask the CancelledError the worker awaits.
        try:
            _drain(meter, cache, buffer)
            meter_provider.force_flush()
        except Exception as exc:
            logger.warning(
                "failed final drain/flush of temporal runtime metrics on shutdown",
                **extract_error_context(exc),
                exc_info=exc,
            )
        raise
