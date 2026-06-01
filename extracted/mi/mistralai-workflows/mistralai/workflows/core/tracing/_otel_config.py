import os
from typing import Tuple

import structlog
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    DEFAULT_METRICS_EXPORT_PATH,
    OTLPMetricExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    DEFAULT_TRACES_EXPORT_PATH,
    OTLPSpanExporter,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.instrument import Counter, Histogram
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio

logger = structlog.getLogger(__name__)


def config_otel(
    endpoint: str,
    metrics_endpoint: str,
    component: str,
    service_name: str,
    service_version: str = "0.0.0",
    sample_rate: float = 1.0,
    export_otlp_interval_ms: int = 30000,
    tail_sampling: bool = False,
    api_key: str | None = None,
) -> Tuple[MeterProvider, TracerProvider]:
    """
    Configure OpenTelemetry with OTLP exporters.
    """
    logger.info(
        "Initializing OpenTelemetry",
        sample_rate=sample_rate,
        service=service_name,
        version=service_version,
        tail_sampling=tail_sampling,
        traces_endpoint=endpoint,
        metrics_endpoint=metrics_endpoint,
    )

    traces_endpoint = endpoint.removesuffix("/") + "/" + DEFAULT_TRACES_EXPORT_PATH
    resolved_metrics_endpoint = metrics_endpoint.removesuffix("/") + "/" + DEFAULT_METRICS_EXPORT_PATH

    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": service_version,
            "worker_id": os.getpid(),
            "component.type": component,
        }
    )

    tracer_provider = TracerProvider(
        resource=resource,
        sampler=ParentBasedTraceIdRatio(sample_rate),
    )
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    span_exporter = OTLPSpanExporter(endpoint=traces_endpoint, headers=headers)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Configure metrics with CUMULATIVE temporality for Prometheus compatibility
    preferred_temporality: dict[type, AggregationTemporality] = {
        Histogram: AggregationTemporality.CUMULATIVE,
        Counter: AggregationTemporality.CUMULATIVE,
    }
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=resolved_metrics_endpoint, preferred_temporality=preferred_temporality),
        export_interval_millis=export_otlp_interval_ms,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    logger.info(
        "OpenTelemetry configured",
        endpoint=endpoint,
        service_name=service_name,
        sample_rate=sample_rate,
    )

    return meter_provider, tracer_provider


def config_otel_local(
    service_name: str,
    service_version: str = "0.0.0",
    sample_rate: float = 1.0,
    tail_sampling: bool = False,
) -> Tuple[MeterProvider, TracerProvider]:
    """
    Configure OpenTelemetry for local development (console exporters).
    """
    logger.info(
        "Initializing OpenTelemetry (locally)",
        sample_rate=sample_rate,
        service=service_name,
        version=service_version,
        tail_sampling=tail_sampling,
    )

    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": service_version,
        }
    )

    tracer_provider = TracerProvider(
        resource=resource,
        sampler=ParentBasedTraceIdRatio(sample_rate),
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(tracer_provider)

    metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    logger.info("OpenTelemetry configured for local development", service_name=service_name)

    return meter_provider, tracer_provider


def _get_calling_module_name() -> str:
    """Get the name of the calling module for tracer naming."""
    import inspect
    from typing import cast

    frame = inspect.currentframe()
    if frame and frame.f_back and frame.f_back.f_back:
        return cast(str, frame.f_back.f_back.f_globals.get("__name__", "unknown"))
    return "unknown"
