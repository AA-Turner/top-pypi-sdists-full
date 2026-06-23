import logging
import os
from dataclasses import dataclass
from typing import Tuple

import structlog
import temporalio.activity
import temporalio.workflow
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    DEFAULT_LOGS_EXPORT_PATH,
    OTLPLogExporter,
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    DEFAULT_METRICS_EXPORT_PATH,
    OTLPMetricExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    DEFAULT_TRACES_EXPORT_PATH,
    OTLPSpanExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.instrument import Counter, Histogram
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    ConsoleMetricExporter,
    MetricReader,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio

from mistralai.workflows._version import __version__
from mistralai.workflows.core._events.event_utils import try_get_lineage_workflow_exec_id
from mistralai.workflows.core.logging import build_json_log_formatter

logger = structlog.getLogger(__name__)

WORKFLOWS_TELEMETRY_DISTRO_NAME = "mistralai-workflows"
TELEMETRY_DISTRO_NAME_ATTRIBUTE = "telemetry.distro.name"
TELEMETRY_DISTRO_VERSION_ATTRIBUTE = "telemetry.distro.version"


@dataclass(frozen=True)
class OtelExportOptions:
    """Per-export-type options for an OTLP exporter (traces, metrics, or logs).

    endpoint: OTLP base endpoint; export is skipped when unset.
    enabled: whether to export this telemetry type at all.
    use_api_key: whether to authenticate the exporter with the Mistral API key.
    """

    endpoint: str | None = None
    enabled: bool = True
    use_api_key: bool = True


def _resolve_endpoint_and_headers(
    options: OtelExportOptions, export_path: str, api_key: str | None
) -> Tuple[str, dict[str, str] | None]:
    assert options.endpoint is not None
    endpoint = options.endpoint.removesuffix("/") + "/" + export_path
    headers = {"Authorization": f"Bearer {api_key}"} if options.use_api_key and api_key else None
    return endpoint, headers


def _create_resource(service_name: str, service_version: str, component: str | None = None) -> Resource:
    attributes: dict[str, str | int] = {
        "service.name": service_name,
        "service.version": service_version,
        TELEMETRY_DISTRO_NAME_ATTRIBUTE: WORKFLOWS_TELEMETRY_DISTRO_NAME,
        TELEMETRY_DISTRO_VERSION_ATTRIBUTE: __version__,
    }
    if component is not None:
        attributes["worker_id"] = os.getpid()
        attributes["component.type"] = component
    return Resource.create(attributes)


class _WorkflowRunFilter(logging.Filter):
    """Filter that enriches log records with deployment/worker and workflow/activity context."""

    def __init__(self, deployment_name: str | None = None, worker_name: str | None = None) -> None:
        super().__init__()
        self._deployment_name = deployment_name
        self._worker_name = worker_name

    def filter(self, record: logging.LogRecord) -> bool:
        # Process-level constants: attached to every record (including non-workflow logs).
        if self._deployment_name is not None:
            record.deploymentName = self._deployment_name
        if self._worker_name is not None:
            record.workerName = self._worker_name

        root_id, parent_id = try_get_lineage_workflow_exec_id()
        if root_id is not None:
            record.rootWorkflowExecutionID = root_id
        if parent_id is not None:
            record.parentWorkflowExecutionID = parent_id

        try:
            workflow_info = temporalio.workflow.info()
            record.workflowExecutionID = workflow_info.workflow_id
            record.workflowRunID = workflow_info.run_id
            record.workflowName = workflow_info.workflow_type
            return True
        except Exception:
            pass

        try:
            activity_info = temporalio.activity.info()
            record.workflowExecutionID = activity_info.workflow_id
            record.workflowRunID = activity_info.workflow_run_id
            record.temporalActivityID = activity_info.activity_id
            record.workflowName = activity_info.workflow_type
        except Exception:
            pass
        return True


def config_otel(
    component: str,
    service_name: str,
    service_version: str = "0.0.0",
    sample_rate: float = 1.0,
    export_otlp_interval_ms: int = 30000,
    tail_sampling: bool = False,
    api_key: str | None = None,
    trace_config: OtelExportOptions | None = None,
    metric_config: OtelExportOptions | None = None,
    log_config: OtelExportOptions | None = None,
    deployment_name: str | None = None,
    worker_name: str | None = None,
) -> Tuple[MeterProvider, TracerProvider, LoggerProvider | None]:
    """
    Configure OpenTelemetry with OTLP exporters.
    """
    trace_config = trace_config or OtelExportOptions()
    metric_config = metric_config or OtelExportOptions()
    log_config = log_config or OtelExportOptions()

    logger.info(
        "Initializing OpenTelemetry",
        sample_rate=sample_rate,
        service=service_name,
        version=service_version,
        tail_sampling=tail_sampling,
        traces_endpoint=trace_config.endpoint,
        metrics_endpoint=metric_config.endpoint,
    )

    resource = _create_resource(service_name=service_name, service_version=service_version, component=component)

    tracer_provider = TracerProvider(
        resource=resource,
        sampler=ParentBasedTraceIdRatio(sample_rate),
    )
    # Spans are still created for context propagation and log trace injection; only the
    # OTLP export is gated so traces can be disabled independently of the OTEL_ENABLED master switch.
    if trace_config.enabled and trace_config.endpoint:
        traces_endpoint, traces_headers = _resolve_endpoint_and_headers(
            trace_config, DEFAULT_TRACES_EXPORT_PATH, api_key
        )
        span_exporter = OTLPSpanExporter(endpoint=traces_endpoint, headers=traces_headers)
        tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Configure metrics with CUMULATIVE temporality for Prometheus compatibility
    metric_readers: list[MetricReader] = []
    if metric_config.enabled and metric_config.endpoint:
        resolved_metrics_endpoint, metrics_headers = _resolve_endpoint_and_headers(
            metric_config, DEFAULT_METRICS_EXPORT_PATH, api_key
        )
        preferred_temporality: dict[type, AggregationTemporality] = {
            Histogram: AggregationTemporality.CUMULATIVE,
            Counter: AggregationTemporality.CUMULATIVE,
        }
        metric_readers.append(
            PeriodicExportingMetricReader(
                OTLPMetricExporter(
                    endpoint=resolved_metrics_endpoint,
                    headers=metrics_headers,
                    preferred_temporality=preferred_temporality,
                ),
                export_interval_millis=export_otlp_interval_ms,
            )
        )
    meter_provider = MeterProvider(resource=resource, metric_readers=metric_readers)
    metrics.set_meter_provider(meter_provider)

    # Configure log export via OTLP when enabled and an endpoint is provided
    logger_provider: LoggerProvider | None = None
    if log_config.enabled and log_config.endpoint:
        resolved_logs_endpoint, logs_headers = _resolve_endpoint_and_headers(
            log_config, DEFAULT_LOGS_EXPORT_PATH, api_key
        )
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(OTLPLogExporter(endpoint=resolved_logs_endpoint, headers=logs_headers))
        )
        set_logger_provider(logger_provider)

        # Bridge Python's standard logging module to OTel log SDK. The JSON
        # formatter forces exported log bodies to JSON regardless of the console
        # log format chosen by the user.
        otel_handler = LoggingHandler(logger_provider=logger_provider)
        otel_handler.setFormatter(build_json_log_formatter())
        otel_handler.addFilter(_WorkflowRunFilter(deployment_name=deployment_name, worker_name=worker_name))
        logging.getLogger().addHandler(otel_handler)

        logger.info("OTLP log export configured", logs_endpoint=log_config.endpoint)

    logger.info(
        "OpenTelemetry configured",
        endpoint=trace_config.endpoint,
        service_name=service_name,
        sample_rate=sample_rate,
        logs_endpoint=log_config.endpoint,
    )

    return meter_provider, tracer_provider, logger_provider


def config_otel_local(
    service_name: str,
    service_version: str = "0.0.0",
    sample_rate: float = 1.0,
    tail_sampling: bool = False,
) -> Tuple[MeterProvider, TracerProvider, LoggerProvider | None]:
    """
    Configure OpenTelemetry for local development (console exporters).
    No log export in local mode - logs go to stdout only.
    """
    logger.info(
        "Initializing OpenTelemetry (locally)",
        sample_rate=sample_rate,
        service=service_name,
        version=service_version,
        tail_sampling=tail_sampling,
    )

    resource = _create_resource(service_name=service_name, service_version=service_version)

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

    return meter_provider, tracer_provider, None


def _get_calling_module_name() -> str:
    """Get the name of the calling module for tracer naming."""
    import inspect
    from typing import cast

    frame = inspect.currentframe()
    if frame and frame.f_back and frame.f_back.f_back:
        return cast(str, frame.f_back.f_back.f_globals.get("__name__", "unknown"))
    return "unknown"
