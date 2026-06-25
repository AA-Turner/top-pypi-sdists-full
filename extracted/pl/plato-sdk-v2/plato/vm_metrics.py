"""VM system metrics instrumentation via OpenTelemetry.

Uses ``opentelemetry-instrumentation-system-metrics`` (backed by psutil) to
automatically collect CPU, memory, disk, and network metrics.  Exports to the
same OTLP endpoint used for traces so Chronos can store them alongside spans.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource

    _HAS_OTEL_METRICS = True
except ImportError:
    _HAS_OTEL_METRICS = False

_meter_provider: MeterProvider | None = None
_instrumentor: SystemMetricsInstrumentor | None = None


def instrument_system_metrics(
    otlp_endpoint: str,
    session_id: str,
    env_alias: str = "world",
    job_id: str = "",
    collect_interval_s: float = 10.0,
) -> None:
    """Start emitting system metrics via OTLP.

    Uses the standard OTel system-metrics instrumentor (psutil-based) so
    CPU, memory, network, and disk metrics are collected automatically.

    Safe to call multiple times; subsequent calls are no-ops.
    No-op if opentelemetry-instrumentation-system-metrics is not installed.
    """
    global _meter_provider, _instrumentor

    if not _HAS_OTEL_METRICS:
        logger.debug("opentelemetry-instrumentation-system-metrics not installed, skipping")
        return

    if _meter_provider is not None:
        return

    attrs: dict[str, str] = {
        "service.name": f"vm-metrics-{env_alias}",
        "plato.session.id": session_id,
        "env_alias": env_alias,
    }
    if job_id:
        attrs["plato.job.id"] = job_id
    resource = Resource.create(attrs)

    # Route the batch by header so chronos doesn't have to peek into the
    # OTLP payload to recover the session id (see useplato/plato#2962).
    #
    # Per-request timeout for the OTLP HTTP POST. The upstream default is 10s,
    # which we routinely hit under bursty chronos load (the backend returns
    # 502 or responds slower than 10s). The exporter only retries on
    # ConnectionError — a read timeout bubbles all the way up and is logged
    # as a noisy urllib3 traceback — so a too-short timeout both loses the
    # batch and spams logs. Bump the default to 30s (matching the trace
    # exporter in plato/otel.py), but defer to the OTel SDK's native env-var
    # resolution when OTEL_EXPORTER_OTLP_METRICS_TIMEOUT (signal-specific,
    # takes precedence per spec) or OTEL_EXPORTER_OTLP_TIMEOUT is set —
    # passing timeout= ourselves would shadow those env vars.
    metrics_endpoint = f"{otlp_endpoint.rstrip('/')}/v1/metrics"
    metrics_headers = {"X-Plato-Session-Id": session_id}
    if "OTEL_EXPORTER_OTLP_METRICS_TIMEOUT" in os.environ or "OTEL_EXPORTER_OTLP_TIMEOUT" in os.environ:
        exporter = OTLPMetricExporter(endpoint=metrics_endpoint, headers=metrics_headers)
    else:
        exporter = OTLPMetricExporter(
            endpoint=metrics_endpoint,
            headers=metrics_headers,
            timeout=30,
        )
    reader = PeriodicExportingMetricReader(
        exporter,
        export_interval_millis=int(collect_interval_s * 1000),
    )
    _meter_provider = MeterProvider(resource=resource, metric_readers=[reader])

    _instrumentor = SystemMetricsInstrumentor()
    _instrumentor.instrument(meter_provider=_meter_provider)


async def shutdown_metrics() -> None:
    """Flush and shut down the metrics pipeline."""
    global _meter_provider, _instrumentor

    if _instrumentor is not None:
        _instrumentor.uninstrument()
        _instrumentor = None

    if _meter_provider is not None:
        try:
            _meter_provider.force_flush(timeout_millis=10_000)
        except Exception:
            logger.debug("VM metrics force_flush failed", exc_info=True)
        _meter_provider.shutdown()
        _meter_provider = None
