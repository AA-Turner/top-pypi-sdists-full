import logging
import os
import threading
import time
from dataclasses import dataclass
from typing import Any, Sequence, Tuple

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
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler, ReadableLogRecord
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, LogRecordExportResult
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.instrument import Counter, Histogram
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    ConsoleMetricExporter,
    MetricExportResult,
    MetricReader,
    MetricsData,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.metrics.view import View
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.sdk.trace.id_generator import IdGenerator, RandomIdGenerator
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio

from mistralai.workflows._version import __version__
from mistralai.workflows.core._events.event_utils import try_get_lineage_workflow_exec_id
from mistralai.workflows.core.auth import TokenProvider
from mistralai.workflows.core.config.config import OtelRedactionMode
from mistralai.workflows.core.logging import build_json_log_formatter, extract_error_context

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


class _DropOtelExportDiagnosticsFilter(logging.Filter):
    """Keep OTLP export diagnostics out of the OTel log-export pipeline.

    Our export-failure warnings and the OTel SDK's own exporter error logs would otherwise be bridged
    back into the log exporter; if the log endpoint is the broken one, each failed export emits a log
    that gets queued for export and fails again. These records still reach stdout via structlog.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name != __name__ and not record.name.startswith("opentelemetry.")


_EXPORT_WARN_INTERVAL_SECONDS = 30.0

_OTLP_404_HINT = (
    "the telemetry endpoint does not seem to exist (not found). If you configured a custom OTEL "
    "endpoint, check that it is correct; if you are using the default endpoint, your organization may "
    "not have access to telemetry export"
)


class _ThrottledExportWarner:
    """Capture the last export HTTP status and emit a throttled warning on failure (404 gets a hint).

    The SDK collapses failures into a bare FAILURE, so we intercept ``_export`` for the status. First
    failure logs immediately, then at most once per interval per signal (reporting suppressed count).
    """

    _last_export_status: int | None = None
    _last_export_warn: float | None = None
    _suppressed_export_warns: int = 0

    def _export(self, serialized_data: bytes, timeout_sec: float | None = None) -> Any:
        resp = super()._export(serialized_data, timeout_sec)  # type: ignore[misc]
        self._last_export_status = getattr(resp, "status_code", None)
        return resp

    def _warn_export_failure(self, signal: str, endpoint: str | None, exc: Exception | None = None) -> None:
        now = time.monotonic()
        if self._last_export_warn is not None and now - self._last_export_warn < _EXPORT_WARN_INTERVAL_SECONDS:
            self._suppressed_export_warns += 1
            return
        status_code = self._last_export_status
        extra: dict[str, Any] = dict(extract_error_context(exc)) if exc is not None else {}
        if status_code is not None:
            extra["status_code"] = status_code
        if self._suppressed_export_warns:
            extra["suppressed_failures"] = self._suppressed_export_warns
        message = f"Failed to export OpenTelemetry {signal}"
        if status_code == 404:
            message = f"{message}: {_OTLP_404_HINT}"
        logger.warning(message, endpoint=endpoint, **extra)
        self._last_export_warn = now
        self._suppressed_export_warns = 0


class _LoggingOTLPSpanExporter(_ThrottledExportWarner, OTLPSpanExporter):
    """OTLP span exporter that warns via structlog when export fails.

    The upstream exporter swallows export failures (e.g. an invalid endpoint returning 404) and only
    emits a raw stdlib log, so we surface a throttled structured warning instead of failing silently.
    """

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        self._last_export_status = None
        try:
            result = super().export(spans)
        except Exception as exc:
            self._warn_export_failure("traces", self._endpoint, exc)
            return SpanExportResult.FAILURE
        if result is SpanExportResult.FAILURE:
            self._warn_export_failure("traces", self._endpoint)
        return result


class _LoggingOTLPMetricExporter(_ThrottledExportWarner, OTLPMetricExporter):
    """OTLP metric exporter that warns via structlog when export fails."""

    def export(
        self, metrics_data: MetricsData, timeout_millis: float | None = 10_000, **kwargs: Any
    ) -> MetricExportResult:
        self._last_export_status = None
        try:
            result = super().export(metrics_data, timeout_millis, **kwargs)
        except Exception as exc:
            self._warn_export_failure("metrics", self._endpoint, exc)
            return MetricExportResult.FAILURE
        if result is MetricExportResult.FAILURE:
            self._warn_export_failure("metrics", self._endpoint)
        return result


class _LoggingOTLPLogExporter(_ThrottledExportWarner, OTLPLogExporter):
    """OTLP log exporter that warns via structlog when export fails.

    The warning is emitted on the internal structlog logger only (not routed through the OTel logging
    handler) so a broken log endpoint cannot feed its own failures back into the export pipeline.
    """

    def export(self, batch: Sequence[ReadableLogRecord]) -> LogRecordExportResult:
        self._last_export_status = None
        try:
            result = super().export(batch)
        except Exception as exc:
            self._warn_export_failure("logs", self._endpoint, exc)
            return LogRecordExportResult.FAILURE
        if result is LogRecordExportResult.FAILURE:
            self._warn_export_failure("logs", self._endpoint)
        return result


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


def _resolve_endpoint(options: OtelExportOptions, export_path: str) -> str:
    assert options.endpoint is not None
    return options.endpoint.removesuffix("/") + "/" + export_path


def _attach_dynamic_auth(exporter: Any, provider: TokenProvider) -> None:
    """Set ``session.auth`` so the OTLP exporter recomputes its bearer per export (picks up rotation).

    Exporters otherwise freeze ``headers`` at construction; if ``_session`` is missing we skip dynamic
    auth (export goes unauthenticated rather than crashing). A token read failure is logged (throttled,
    since this runs on every export) and the export goes out unauthenticated until the token recovers.
    """
    session = getattr(exporter, "_session", None)
    if session is None:
        logger.warning(
            "OTLP exporter exposes no _session; skipping dynamic telemetry auth "
            "(export may be unauthenticated). The exporter library layout may have changed."
        )
        return

    last_error_log = 0.0
    error_log_interval_seconds = 60.0

    def _inject(request: Any) -> Any:
        nonlocal last_error_log
        try:
            token = provider.get_token()
        except Exception as exc:
            token = None
            now = time.monotonic()
            if now - last_error_log >= error_log_interval_seconds:
                last_error_log = now
                logger.warning(
                    "Failed to read token for OTLP telemetry auth; "
                    "exporting unauthenticated until the token is readable again",
                    **extract_error_context(exc),
                )
        if token:
            request.headers["Authorization"] = f"Bearer {token}"
        return request

    session.auth = _inject


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
    if not (metric_config.enabled and metric_config.endpoint):
        return None
    endpoint = _resolve_endpoint(metric_config, DEFAULT_METRICS_EXPORT_PATH)
    preferred_temporality: dict[type, AggregationTemporality] = {
        Histogram: AggregationTemporality.CUMULATIVE,
        Counter: AggregationTemporality.CUMULATIVE,
    }
    exporter = _LoggingOTLPMetricExporter(endpoint=endpoint, preferred_temporality=preferred_temporality)
    if metric_config.use_api_key and token_provider is not None:
        _attach_dynamic_auth(exporter, token_provider)
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
    if trace_config.enabled and trace_config.endpoint:
        traces_endpoint = _resolve_endpoint(trace_config, DEFAULT_TRACES_EXPORT_PATH)
        raw_span_exporter = _LoggingOTLPSpanExporter(endpoint=traces_endpoint)
        if trace_config.use_api_key and token_provider is not None:
            _attach_dynamic_auth(raw_span_exporter, token_provider)
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
    if log_config.enabled and log_config.endpoint:
        resolved_logs_endpoint = _resolve_endpoint(log_config, DEFAULT_LOGS_EXPORT_PATH)
        log_exporter = _LoggingOTLPLogExporter(endpoint=resolved_logs_endpoint)
        if log_config.use_api_key and token_provider is not None:
            _attach_dynamic_auth(log_exporter, token_provider)
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        set_logger_provider(logger_provider)

        # Bridge Python's standard logging module to OTel log SDK. The JSON
        # formatter forces exported log bodies to JSON regardless of the console
        # log format chosen by the user.
        otel_handler = LoggingHandler(logger_provider=logger_provider)
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
