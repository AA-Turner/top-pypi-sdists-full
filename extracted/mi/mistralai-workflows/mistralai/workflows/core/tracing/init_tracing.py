from typing import (
    Literal,
    Tuple,
)

import structlog
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider

try:
    from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor

    _HAS_AIOHTTP_INSTRUMENTATION = True
except ImportError:
    _HAS_AIOHTTP_INSTRUMENTATION = False

from mistralai.workflows.core.auth import TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.runtime_metrics import build_temporal_metric_views
from mistralai.workflows.core.tracing._otel_config import (
    WORKER_SERVICE_NAME,
    OtelExportOptions,
    build_runtime_metrics_meter_provider,
    config_otel,
    config_otel_local,
)

logger = structlog.getLogger(__name__)


def _build_export_options(
    endpoint_override: str | None,
    default_endpoint: str | None,
    enabled: bool,
) -> OtelExportOptions:
    # Authenticate with the Mistral API key only when falling back to the default endpoint.
    # Explicitly configured endpoints handle auth themselves via the conventional OTLP
    # environment variables (e.g. OTEL_EXPORTER_OTLP_HEADERS).
    return OtelExportOptions(
        endpoint=endpoint_override or default_endpoint,
        enabled=enabled,
        use_api_key=not endpoint_override,
    )


def _signal_log_field(export_config: OtelExportOptions, endpoint_override: str | None) -> dict[str, object]:
    # A per-signal override (or the deprecated otel_endpoint) means a custom destination;
    # otherwise the signal exports to Mistral's hosted /telemetry endpoint.
    mode = "custom" if endpoint_override else "mistral"
    return {"mode": mode, "endpoint": export_config.endpoint, "enabled": export_config.enabled}


def init_tracing(
    component: Literal["api", "worker"],
    *,
    deployment_name: str | None = None,
    worker_name: str | None = None,
) -> Tuple[MeterProvider | None, TracerProvider | None, LoggerProvider | None, MeterProvider | None]:
    """
    Initialize OpenTelemetry tracing for either the API or worker component.

    Args:
        component: Either "api" or "worker"
        deployment_name: Worker deployment name, attached as a `deploymentName` log attribute
        worker_name: Worker name, attached as a `workerName` log attribute

    Returns:
        (meter_provider, tracer_provider, logger_provider, runtime_metrics_meter_provider), all may be None.
        The last is the worker-only provider for re-emitted Temporal runtime metrics (no ``worker_id``);
        None for non-worker components.
        TODO: Remove once Temporal handles SA for metrics (then the Rust-core exporter can push directly).
    """
    if not config.common.otel_enabled:
        logger.debug("OpenTelemetry tracing is disabled")
        return None, None, None, None

    service_name = WORKER_SERVICE_NAME if component == "worker" else f"{config.common.app_name}-{component}"

    if config.common.otel_local:
        logger.info(
            "Initializing local OpenTelemetry tracing",
            service=service_name,
            sample_rate=config.common.otel_sample_rate,
        )
        # Local mode ships traces + metrics to console exporters (no log export) and ignores the per-signal toggles.
        logger.info(
            "Telemetry enabled",
            service=service_name,
            traces={"mode": "local", "endpoint": None, "enabled": True},
            metrics={"mode": "local", "endpoint": None, "enabled": True},
            logs={"mode": "local", "endpoint": None, "enabled": False},
        )
        meter_provider, tracer_provider, logger_provider = config_otel_local(
            service_name=service_name,
            service_version=config.common.app_version,
            sample_rate=config.common.otel_sample_rate,
            redaction=config.common.otel_redaction,
            metric_views=build_temporal_metric_views() if component == "worker" else None,
        )
        # Local/console dev: the pump reuses this provider (worker_id churn is a prod-mimir concern only).
        runtime_metrics_meter_provider = meter_provider if component == "worker" else None
    else:
        common = config.common
        if common.otel_endpoint:
            logger.warning(
                "otel_endpoint is deprecated, use otel_traces_endpoint and otel_metrics_endpoint instead",
            )
            token_provider: TokenProvider | None = None
            # The deprecated single endpoint applies to every signal and never carries auth.
            trace_endpoint: str | None = common.otel_endpoint
            metric_endpoint: str | None = common.otel_endpoint
            log_endpoint: str | None = common.otel_endpoint
            default_endpoint: str | None = None
        else:
            assert config.worker.agent.mistral_client_server_url is not None  # guaranteed by WorkerConfig validator
            default_endpoint = f"{config.worker.agent.mistral_client_server_url.rstrip('/')}/telemetry"
            token_provider = get_token_provider(config.worker.agent.mistral_client_api_key)
            trace_endpoint = common.otel_traces_endpoint
            metric_endpoint = common.otel_metrics_endpoint
            log_endpoint = common.otel_logs_endpoint

        trace_config = _build_export_options(
            trace_endpoint, default_endpoint, common.mistral_workflows_otel_traces_export
        )
        metric_config = _build_export_options(
            metric_endpoint, default_endpoint, common.mistral_workflows_otel_metrics_export
        )
        log_config = _build_export_options(log_endpoint, default_endpoint, common.mistral_workflows_otel_logs_export)

        logger.info(
            "Telemetry enabled",
            service=service_name,
            traces=_signal_log_field(trace_config, trace_endpoint),
            metrics=_signal_log_field(metric_config, metric_endpoint),
            logs=_signal_log_field(log_config, log_endpoint),
        )

        meter_provider, tracer_provider, logger_provider = config_otel(
            service_name=service_name,
            service_version=config.common.app_version,
            sample_rate=config.common.otel_sample_rate,
            export_otlp_interval_ms=config.common.otel_export_interval_ms,
            component=component,
            token_provider=token_provider,
            trace_config=trace_config,
            metric_config=metric_config,
            log_config=log_config,
            deployment_name=deployment_name,
            worker_name=worker_name,
            redaction=config.common.otel_redaction,
        )
        # Temporal runtime metrics re-emit through a dedicated provider whose Resource omits worker_id, so
        # temporal_* keep the old core label set (no per-restart PID churn). Worker-only.
        # TODO: Remove once Temporal handles SA for metrics (Rust-core exporter can then push directly).
        runtime_metrics_meter_provider = (
            build_runtime_metrics_meter_provider(
                service_name,
                config.common.app_version,
                token_provider=token_provider,
                metric_config=metric_config,
                export_otlp_interval_ms=config.common.otel_export_interval_ms,
                views=build_temporal_metric_views(),
            )
            if component == "worker"
            else None
        )

    # Instrument common libraries.
    # AsyncioInstrumentor is deliberately not enabled: it wraps every coroutine passed to
    # asyncio.create_task/gather/wait/to_thread, and that bookkeeping breaks against Temporal's
    # separate deterministic workflow event loop ("Cannot enter into task X while another task Y is
    # being executed"), which can leave a workflow task hung until its start-to-close timeout.
    HTTPXClientInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)

    # Only instrument aiohttp if it's available (GCS storage dependency)
    if _HAS_AIOHTTP_INSTRUMENTATION:
        AioHttpClientInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)

    return meter_provider, tracer_provider, logger_provider, runtime_metrics_meter_provider
