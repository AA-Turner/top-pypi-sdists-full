from typing import (
    Literal,
    Tuple,
)

import structlog
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider

try:
    from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor

    _HAS_AIOHTTP_INSTRUMENTATION = True
except ImportError:
    _HAS_AIOHTTP_INSTRUMENTATION = False

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.tracing._otel_config import OtelExportOptions, config_otel, config_otel_local

logger = structlog.getLogger(__name__)

# Worker telemetry uses a fixed service name so downstream consumers (e.g. Abraxas
# filtering execution logs by ServiceName) can rely on it. It is intentionally
# decoupled from the user-configurable app_name and must not be overridable.
WORKER_SERVICE_NAME = "mistral-workflows-worker"


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
) -> Tuple[MeterProvider | None, TracerProvider | None, LoggerProvider | None]:
    """
    Initialize OpenTelemetry tracing for either the API or worker component.

    Args:
        component: Either "api" or "worker"
        deployment_name: Worker deployment name, attached as a `deploymentName` log attribute
        worker_name: Worker name, attached as a `workerName` log attribute

    Returns:
        A tuple of (meter_provider, tracer_provider, logger_provider), all may be None
    """
    if not config.common.otel_enabled:
        logger.debug("OpenTelemetry tracing is disabled")
        return None, None, None

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
            tail_sampling=config.common.otel_tail_sampling,
        )
    else:
        common = config.common
        if common.otel_endpoint:
            logger.warning(
                "otel_endpoint is deprecated, use otel_traces_endpoint and otel_metrics_endpoint instead",
            )
            api_key: str | None = None
            # The deprecated single endpoint applies to every signal and never carries auth.
            trace_endpoint: str | None = common.otel_endpoint
            metric_endpoint: str | None = common.otel_endpoint
            log_endpoint: str | None = common.otel_endpoint
            default_endpoint: str | None = None
        else:
            assert config.worker.agent.mistral_client_server_url is not None  # guaranteed by WorkerConfig validator
            default_endpoint = f"{config.worker.agent.mistral_client_server_url.rstrip('/')}/telemetry"
            api_key = (
                config.worker.agent.mistral_client_api_key.get_secret_value()
                if config.worker.agent.mistral_client_api_key
                else None
            )
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
            tail_sampling=config.common.otel_tail_sampling,
            component=component,
            api_key=api_key,
            trace_config=trace_config,
            metric_config=metric_config,
            log_config=log_config,
            deployment_name=deployment_name,
            worker_name=worker_name,
        )

    # Instrument common libraries
    AsyncioInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)
    HTTPXClientInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)

    # Only instrument aiohttp if it's available (GCS storage dependency)
    if _HAS_AIOHTTP_INSTRUMENTATION:
        AioHttpClientInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)

    return meter_provider, tracer_provider, logger_provider
