import logging
import os
import threading
from typing import Any, Tuple

import structlog
import temporalio.activity
import temporalio.workflow
from mistralai.extra.observability import (
    AttributeRedactionPolicy,
    RedactingSpanExporter,
    default_redaction_policy,
)
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    MetricReader,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.metrics.view import View
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)
from opentelemetry.sdk.trace.id_generator import IdGenerator, RandomIdGenerator
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio

from mistralai.workflows._version import __version__
from mistralai.workflows.core._events.event_utils import try_get_lineage_workflow_exec_id
from mistralai.workflows.core.auth import TokenProvider
from mistralai.workflows.core.config.config import OtelRedactionMode
from mistralai.workflows.core.logging import build_json_log_formatter
from mistralai.workflows.core.tracing.exporters import (
    OtelExportOptions,
    _DropOtelExportDiagnosticsFilter,
    build_otlp_log_exporter,
    build_otlp_metric_exporter,
    build_otlp_span_exporter,
)

logger = structlog.getLogger(__name__)

# Worker telemetry uses a fixed service name so downstream consumers (e.g. Abraxas
# filtering execution logs by ServiceName) can rely on it. It is intentionally
# decoupled from the user-configurable app_name and must not be overridable.
WORKER_SERVICE_NAME = "mistral-workflows-worker"
WORKFLOWS_TELEMETRY_DISTRO_NAME = "mistralai-workflows"
TELEMETRY_DISTRO_NAME_ATTRIBUTE = "telemetry.distro.name"
TELEMETRY_DISTRO_VERSION_ATTRIBUTE = "telemetry.distro.version"

# These attribute keys smuggle the desired trace/span ids from the workflow sandbox to the host side.
# Temporal's sandbox forbids direct OTel calls, so _maybe_emit_workflow_root_span() (sandbox) stashes
# the ids as span attributes, and _completed_workflow_span() (host) pops them before the real span is
# created, so they never appear in exported telemetry.
FORCE_TRACE_ID_ATTRIBUTE = "__mistral_force_trace_id"
FORCE_SPAN_ID_ATTRIBUTE = "__mistral_force_span_id"


class _StructlogAwareLoggingHandler(LoggingHandler):
    """Log handler that keeps structlog's private record extras out of exported log attributes.

    structlog's ``ProcessorFormatter.wrap_for_formatter`` attaches ``_logger`` (a structlog logger
    object) and ``_name`` to every LogRecord via ``extra``; its formatter reads them, so they must
    stay on the record. The OTel base class exports every non-reserved record attribute, and a
    logger object is not a valid OTel attribute value, so without this filter every exported log
    warns "Invalid type ... for attribute value" from ``opentelemetry.attributes``.
    """

    def _get_attributes(self, record: logging.LogRecord) -> dict[str, Any]:  # type: ignore[override]
        # Instance method + super() so a future OTel base change (e.g. staticmethod -> instance
        # method) keeps working; the ignore covers the current staticmethod declaration upstream.
        attributes = super()._get_attributes(record)
        return {key: value for key, value in (attributes or {}).items() if not key.startswith("_")}


class _ForcedIdGenerator(IdGenerator):
    """Override OTel's random id generation for one span at a time.

    OTel's API does not support creating a span with a caller-specified id: TracerProvider always
    calls id_generator.generate_span_id() internally, and there is no parameter to bypass that. The
    only extension point is the IdGenerator itself, so we override it to return a specific value once,
    then revert to random.

    This lets us create the root span with the exact span_id that all other workflow spans already
    reference as their parent, turning a phantom parent into a real, visible span.

    Thread-local because this is a singleton shared across all workflows on the worker.
    """

    def __init__(self) -> None:
        self._random = RandomIdGenerator()
        self._local = threading.local()

    def prime(self, trace_id: int | None, span_id: int | None) -> None:
        self._local.trace_id = trace_id
        self._local.span_id = span_id

    def clear(self) -> None:
        self._local.trace_id = None
        self._local.span_id = None

    def generate_span_id(self) -> int:
        span_id = getattr(self._local, "span_id", None)
        if span_id is not None:
            self._local.span_id = None
            return int(span_id)
        return self._random.generate_span_id()

    def generate_trace_id(self) -> int:
        trace_id = getattr(self._local, "trace_id", None)
        if trace_id is not None:
            self._local.trace_id = None
            return int(trace_id)
        return self._random.generate_trace_id()


# Shared instance installed on the worker TracerProvider so the tracing interceptor can prime it.
WORKFLOW_ROOT_ID_GENERATOR = _ForcedIdGenerator()


def _create_resource(
    service_name: str, service_version: str, component: str | None = None, include_worker_id: bool = True
) -> Resource:
    attributes: dict[str, str | int] = {
        "service.name": service_name,
        "service.version": service_version,
        TELEMETRY_DISTRO_NAME_ATTRIBUTE: WORKFLOWS_TELEMETRY_DISTRO_NAME,
        TELEMETRY_DISTRO_VERSION_ATTRIBUTE: __version__,
    }
    if component is not None:
        # worker_id (the PID) churns on every restart. It's useful on traces but a cardinality anti-pattern
        # as a metric label, so the runtime-metrics MeterProvider omits it (matches the old core global_tags).
        if include_worker_id:
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


def _build_otlp_metric_reader(
    metric_config: OtelExportOptions, token_provider: TokenProvider | None, export_otlp_interval_ms: int
) -> MetricReader | None:
    """Build an OTLP metric reader (CUMULATIVE, dynamic per-export auth) or None when metrics are disabled."""
    exporter = build_otlp_metric_exporter(metric_config, token_provider)
    if exporter is None:
        return None
    return PeriodicExportingMetricReader(exporter, export_interval_millis=export_otlp_interval_ms)


def build_runtime_metrics_meter_provider(
    service_name: str,
    service_version: str,
    *,
    token_provider: TokenProvider | None,
    metric_config: OtelExportOptions | None,
    export_otlp_interval_ms: int,
    views: list[View],
) -> MeterProvider | None:
    """Dedicated MeterProvider for re-emitted Temporal runtime metrics (the worker's pump).

    Its Resource omits ``worker_id`` (unlike the app-telemetry provider) so ``temporal_*`` series keep the
    same label set as the old Rust-core exporter. Returns None when metrics export is disabled.
    """
    reader = _build_otlp_metric_reader(metric_config or OtelExportOptions(), token_provider, export_otlp_interval_ms)
    if reader is None:
        return None
    resource = _create_resource(service_name, service_version, component="worker", include_worker_id=False)
    return MeterProvider(resource=resource, metric_readers=[reader], views=tuple(views))


def _silence_raw_otlp_exporter_logs() -> None:
    # Mute the OTLP exporters' own retry/failure logs; our throttled _Logging*Exporter warning replaces them.
    logging.getLogger("opentelemetry.exporter.otlp").setLevel(logging.CRITICAL)


def config_otel(
    component: str,
    service_name: str,
    service_version: str = "0.0.0",
    sample_rate: float = 1.0,
    export_otlp_interval_ms: int = 30000,
    token_provider: TokenProvider | None = None,
    trace_config: OtelExportOptions | None = None,
    metric_config: OtelExportOptions | None = None,
    log_config: OtelExportOptions | None = None,
    deployment_name: str | None = None,
    worker_name: str | None = None,
    redaction: OtelRedactionMode = OtelRedactionMode.DEFAULT,
    metric_views: list[View] | None = None,
) -> Tuple[MeterProvider, TracerProvider, LoggerProvider | None]:
    """
    Configure OpenTelemetry with OTLP exporters.
    """
    trace_config = trace_config or OtelExportOptions()
    metric_config = metric_config or OtelExportOptions()
    log_config = log_config or OtelExportOptions()

    _silence_raw_otlp_exporter_logs()

    resource = _create_resource(service_name=service_name, service_version=service_version, component=component)

    tracer_provider = TracerProvider(
        resource=resource,
        sampler=ParentBasedTraceIdRatio(sample_rate),
        id_generator=WORKFLOW_ROOT_ID_GENERATOR,
    )
    # Spans are still created for context propagation and log trace injection; only the
    # OTLP export is gated so traces can be disabled independently of the OTEL_ENABLED master switch.
    raw_span_exporter = build_otlp_span_exporter(trace_config, token_provider)
    if raw_span_exporter is not None:
        span_exporter = _apply_span_redaction(raw_span_exporter, redaction)
        tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Configure metrics with CUMULATIVE temporality for Prometheus compatibility
    metric_readers: list[MetricReader] = []
    reader = _build_otlp_metric_reader(metric_config, token_provider, export_otlp_interval_ms)
    if reader is not None:
        metric_readers.append(reader)
    meter_provider = MeterProvider(resource=resource, metric_readers=metric_readers, views=tuple(metric_views or ()))
    metrics.set_meter_provider(meter_provider)

    # Configure log export via OTLP when enabled and an endpoint is provided
    logger_provider: LoggerProvider | None = None
    log_exporter = build_otlp_log_exporter(log_config, token_provider)
    if log_exporter is not None:
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        set_logger_provider(logger_provider)

        # Bridge Python's standard logging module to OTel log SDK. The JSON
        # formatter forces exported log bodies to JSON regardless of the console
        # log format chosen by the user.
        otel_handler = _StructlogAwareLoggingHandler(logger_provider=logger_provider)
        otel_handler.setFormatter(build_json_log_formatter())
        otel_handler.addFilter(_DropOtelExportDiagnosticsFilter())
        otel_handler.addFilter(_WorkflowRunFilter(deployment_name=deployment_name, worker_name=worker_name))
        logging.getLogger().addHandler(otel_handler)

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
    redaction: OtelRedactionMode = OtelRedactionMode.DEFAULT,
    metric_views: list[View] | None = None,
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
    )

    resource = _create_resource(service_name=service_name, service_version=service_version)

    tracer_provider = TracerProvider(
        resource=resource,
        sampler=ParentBasedTraceIdRatio(sample_rate),
        id_generator=WORKFLOW_ROOT_ID_GENERATOR,
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(_apply_span_redaction(ConsoleSpanExporter(), redaction)))
    trace.set_tracer_provider(tracer_provider)

    metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader], views=tuple(metric_views or ()))
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


def _apply_span_redaction(exporter: SpanExporter, redaction: OtelRedactionMode) -> SpanExporter:
    """Wrap a span exporter so spans are redacted client-side before export."""
    if redaction is OtelRedactionMode.NONE:
        return exporter
    policy = AttributeRedactionPolicy() if redaction is OtelRedactionMode.STRICT else default_redaction_policy()
    return RedactingSpanExporter(exporter, policy)
