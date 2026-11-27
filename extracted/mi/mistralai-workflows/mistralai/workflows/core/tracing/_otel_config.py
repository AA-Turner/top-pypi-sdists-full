import atexit
import logging
import os
import threading
from collections.abc import Mapping
from typing import Any, Tuple

import temporalio.activity
import temporalio.workflow
from mistralai.extra.observability import (
    DEFAULT_REDACTED_VALUE,
    DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS,
    AttributeRedactionPolicy,
    RedactingSpanExporter,
    RedactionPolicy,
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
from structlog.typing import EventDict

from mistralai.workflows._version import __version__
from mistralai.workflows.core._events.event_utils import try_get_lineage_workflow_exec_id
from mistralai.workflows.core._logger import get_logger
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
from mistralai.workflows.core.tracing.workflow_context import (
    WorkflowContextSpanProcessor,
    current_context_info,
)

logger = get_logger(__name__)

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

# Redaction policies only redact attribute mappings, so log body text goes through them under this key.
_LOG_BODY_ATTRIBUTE = "log.body"

# OTLP HTTP exporters wait out their 10 s timeout on an endpoint that does not answer, once per pending batch.
# This caps the wait on spans at process exit.
_TRACES_SHUTDOWN_TIMEOUT_SECONDS = 3.0


class _StructlogAwareLoggingHandler(LoggingHandler):
    """Log handler that redacts exported attributes and keeps structlog's private extras out of them.

    structlog's ``ProcessorFormatter.wrap_for_formatter`` attaches ``_logger`` (a structlog logger
    object) and ``_name`` to every LogRecord via ``extra``; its formatter reads them, so they must
    stay on the record. The OTel base class exports every non-reserved record attribute, and a
    logger object is not a valid OTel attribute value, so without this filter every exported log
    warns "Invalid type ... for attribute value" from ``opentelemetry.attributes``.

    ``redaction`` (``OTEL_REDACTION``) applies to the attributes here; the body is redacted by the
    ``_LogBodyRedactor`` in the formatter ``config_otel`` attaches. ``_get_attributes`` is stable
    across the supported OTel SDK range, unlike the log processor and exporter interfaces.

    Unlike stdlib handlers, the OTel base ``emit`` does not catch errors, so a record its formatter
    cannot render (a cyclic value, a ``repr()`` that raises) would fail the log call itself, and
    with it the user's activity. ``emit`` drops such records through ``handleError`` instead.

    The handler does not lock: ``createLock`` installs a lock whose acquire and release do nothing,
    so the stdlib ``handle`` runs unchanged. A stdlib handler serializes every record behind one
    lock, so a slow record (redaction of a large value) blocks every other thread that logs.
    Temporal interrupts a workflow thread blocked for 2s by injecting an exception into it; if that
    thread was waiting on the lock, the exception can fire just after the lock is acquired and leak
    it, freezing all logging in the process. Nothing here needs the lock: formatting and redaction
    work on per-record data, and the OTel logger provider and batch processor are thread-safe on
    their own.
    """

    def __init__(
        self, *, logger_provider: LoggerProvider, redaction: OtelRedactionMode = OtelRedactionMode.NONE
    ) -> None:
        super().__init__(logger_provider=logger_provider)
        self._redaction_policy = _build_redaction_policy(redaction)

    def createLock(self) -> None:
        self.lock = _NonLockingLock()  # type: ignore[assignment]

    def emit(self, record: logging.LogRecord) -> None:
        try:
            super().emit(record)
        except Exception:
            self.handleError(record)

    def _get_attributes(self, record: logging.LogRecord) -> dict[str, Any]:  # type: ignore[override]
        # Instance method + super() so a future OTel base change (e.g. staticmethod -> instance
        # method) keeps working; the ignore covers the current staticmethod declaration upstream.
        attributes = super()._get_attributes(record)
        attributes = {key: value for key, value in (attributes or {}).items() if not key.startswith("_")}
        if self._redaction_policy is None:
            return attributes
        return self._redaction_policy.redact_attributes(attributes)


class _NonLockingLock:
    """Stands in for ``logging.Handler.lock`` so the handler never serializes or blocks callers."""

    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        return True

    def release(self) -> None:
        pass

    def __enter__(self) -> bool:
        return True

    def __exit__(self, *exc_info: object) -> None:
        pass

    def _at_fork_reinit(self) -> None:
        pass


class _LogBodyRedactor:
    """structlog processor that redacts the event dict just before it is rendered as the exported body.

    Redacting the dict rather than the rendered JSON text keeps the body valid JSON: scrubbing the
    text would also match unquoted numbers (a 13-digit epoch-ms timestamp looks like a card number).
    ``default`` scrubs string values, nested ones included, and leaves keys and numbers as they are,
    like span attributes. ``strict`` replaces the whole body.
    """

    def __init__(self, redaction: OtelRedactionMode) -> None:
        self._strict = redaction is OtelRedactionMode.STRICT
        self._policy = _build_redaction_policy(redaction)

    def __call__(self, logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
        if self._policy is None:
            return event_dict
        if self._strict:
            return {"event": DEFAULT_REDACTED_VALUE}
        return {key: self._redact(value) for key, value in event_dict.items()}

    def _redact(self, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float)):
            return value
        if isinstance(value, str):
            assert self._policy is not None
            return self._policy.redact_attributes({_LOG_BODY_ATTRIBUTE: value})[_LOG_BODY_ATTRIBUTE]
        if isinstance(value, dict):
            return {key: self._redact(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._redact(item) for item in value]
        # JSONRenderer would serialize any other object through __structlog__() or repr() after this
        # processor runs, unscrubbed; do the same conversion here so its text is redacted too.
        try:
            converted = value.__structlog__()
        except AttributeError:
            converted = repr(value)
        if converted is not None and not isinstance(converted, (str, bool, int, float, dict, list, tuple)):
            converted = repr(converted)
        return self._redact(converted)


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

        context_info = current_context_info()
        if context_info is None:
            _set_ids_from_temporal_extra(record)
            return True

        record.workflowExecutionID = context_info.workflow_id
        record.workflowRunID = (
            context_info.workflow_run_id if isinstance(context_info, temporalio.activity.Info) else context_info.run_id
        )
        record.workflowName = context_info.workflow_type
        if isinstance(context_info, temporalio.activity.Info):
            record.temporalActivityID = context_info.activity_id
        return True


def _set_ids_from_temporal_extra(record: logging.LogRecord) -> None:
    """Tag records temporalio logs outside the workflow/activity context, from the details it attaches.

    temporalio logs workflow task failures ("Failed activation on workflow ...") after the workflow
    event loop has stopped, so the context lookup finds nothing, but the record carries a
    `temporal_workflow` (or `temporal_activity`) extra with the ids.
    """
    activity_details = getattr(record, "temporal_activity", None)
    if isinstance(activity_details, Mapping):
        _set_if_str(record, "workflowExecutionID", activity_details.get("workflow_id"))
        _set_if_str(record, "workflowRunID", activity_details.get("workflow_run_id"))
        _set_if_str(record, "workflowName", activity_details.get("workflow_type"))
        _set_if_str(record, "temporalActivityID", activity_details.get("activity_id"))
        return

    workflow_details = getattr(record, "temporal_workflow", None)
    if isinstance(workflow_details, Mapping):
        _set_if_str(record, "workflowExecutionID", workflow_details.get("workflow_id"))
        _set_if_str(record, "workflowRunID", workflow_details.get("run_id"))
        _set_if_str(record, "workflowName", workflow_details.get("workflow_type"))


def _set_if_str(record: logging.LogRecord, attribute: str, value: object) -> None:
    if isinstance(value, str):
        setattr(record, attribute, value)


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


def _shutdown_traces(provider: TracerProvider) -> None:
    # TracerProvider.shutdown takes no timeout. Run it in a daemon thread and stop waiting at the deadline.
    shutdown = threading.Thread(target=provider.shutdown, name="otel-trace-shutdown", daemon=True)
    shutdown.start()
    shutdown.join(_TRACES_SHUTDOWN_TIMEOUT_SECONDS)
    if shutdown.is_alive():
        logger.warning(
            "OpenTelemetry traces not exported before exit; pending spans dropped",
            timeout_s=_TRACES_SHUTDOWN_TIMEOUT_SECONDS,
        )


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
        # Replaced by the bounded shutdown registered below.
        shutdown_on_exit=False,
    )
    # Shut down at exit, not when the worker stops: the provider is global, and the process may keep emitting spans.
    atexit.register(_shutdown_traces, tracer_provider)
    # Attached unconditionally (and before the exporter processor) so every span started in a
    # workflow or activity context carries the wf.* workflow attributes even when export is off:
    # spans still exist for context propagation and log correlation.
    tracer_provider.add_span_processor(WorkflowContextSpanProcessor())
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
        otel_handler = _StructlogAwareLoggingHandler(logger_provider=logger_provider, redaction=redaction)
        otel_handler.setFormatter(
            build_json_log_formatter(
                _LogBodyRedactor(redaction),
                redact_credentials=redaction is not OtelRedactionMode.NONE,
            )
        )
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
    tracer_provider.add_span_processor(WorkflowContextSpanProcessor())
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


def _build_redaction_policy(redaction: OtelRedactionMode) -> RedactionPolicy | None:
    """Policy applied to spans and log records before export, or None when redaction is off."""
    if redaction is OtelRedactionMode.NONE:
        return None
    if redaction is OtelRedactionMode.DEFAULT:
        return default_redaction_policy()
    # mistralai's strict defaults miss `wf.result` (activity and workflow outputs).
    return AttributeRedactionPolicy(sensitive_fragments=DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS | {"result"})


def _apply_span_redaction(exporter: SpanExporter, redaction: OtelRedactionMode) -> SpanExporter:
    """Wrap a span exporter so spans are redacted client-side before export."""
    policy = _build_redaction_policy(redaction)
    if policy is None:
        return exporter
    return RedactingSpanExporter(exporter, policy)
