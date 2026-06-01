from typing import (
    Literal,
    Tuple,
)

import structlog
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider

try:
    from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor

    _HAS_AIOHTTP_INSTRUMENTATION = True
except ImportError:
    _HAS_AIOHTTP_INSTRUMENTATION = False

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.tracing._otel_config import config_otel, config_otel_local

logger = structlog.getLogger(__name__)


def init_tracing(component: Literal["api", "worker"]) -> Tuple[MeterProvider | None, TracerProvider | None]:
    """
    Initialize OpenTelemetry tracing for either the API or worker component.

    Args:
        component: Either "api" or "worker"

    Returns:
        A tuple of (meter_provider, tracer_provider), both of which may be None if tracing is not enabled
    """
    if not config.common.otel_enabled:
        logger.debug("OpenTelemetry tracing is disabled")
        return None, None

    service_name = f"{config.common.app_name}-{component}"

    if config.common.otel_local:
        logger.info(
            "Initializing local OpenTelemetry tracing",
            service=service_name,
            sample_rate=config.common.otel_sample_rate,
        )
        meter_provider, tracer_provider = config_otel_local(
            service_name=service_name,
            service_version=config.common.app_version,
            sample_rate=config.common.otel_sample_rate,
            tail_sampling=config.common.otel_tail_sampling,
        )
    else:
        if config.common.otel_endpoint:
            logger.warning(
                "otel_endpoint is deprecated, use otel_traces_endpoint and otel_metrics_endpoint instead",
            )
            traces_endpoint = config.common.otel_endpoint
            metrics_endpoint: str = config.common.otel_endpoint
            api_key: str | None = None
        else:
            assert config.worker.agent.mistral_client_server_url is not None  # guaranteed by WorkerConfig validator
            traces_endpoint = (
                config.common.otel_traces_endpoint
                or f"{config.worker.agent.mistral_client_server_url.rstrip('/')}/telemetry"
            )
            metrics_endpoint = config.common.otel_metrics_endpoint
            # Explicit endpoint: authentication is at the user's charge via conventional OTLP environment
            # variables (e.g. OTEL_EXPORTER_OTLP_HEADERS)
            api_key = (
                config.worker.agent.mistral_client_api_key.get_secret_value()
                if config.worker.agent.mistral_client_api_key and not config.common.otel_traces_endpoint
                else None
            )

        logger.info(
            "Initializing OpenTelemetry tracing",
            traces_endpoint=traces_endpoint,
            metrics_endpoint=metrics_endpoint,
            service=service_name,
            sample_rate=config.common.otel_sample_rate,
        )
        meter_provider, tracer_provider = config_otel(
            endpoint=traces_endpoint,
            metrics_endpoint=metrics_endpoint,
            service_name=service_name,
            service_version=config.common.app_version,
            sample_rate=config.common.otel_sample_rate,
            export_otlp_interval_ms=config.common.otel_export_interval_ms,
            tail_sampling=config.common.otel_tail_sampling,
            component=component,
            api_key=api_key,
        )

    # Instrument common libraries
    AsyncioInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)
    HTTPXClientInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)

    # Only instrument aiohttp if it's available (GCS storage dependency)
    if _HAS_AIOHTTP_INSTRUMENTATION:
        AioHttpClientInstrumentor().instrument(meter_provider=meter_provider, tracer_provider=tracer_provider)

    return meter_provider, tracer_provider
