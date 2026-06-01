"""
OTel setup for LiveKit Agents — registers Aigie exporter with LiveKit's
native OpenTelemetry support via set_tracer_provider().

Usage:
    import aigie
    from aigie.integrations.livekit_agents.otel_setup import setup_livekit_otel

    client = aigie.init(url, token)
    setup_livekit_otel(client)

    # LiveKit now auto-exports all spans to Aigie
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def setup_livekit_otel(
    aigie_client: Any,
    service_name: str = "livekit-voice-agent",
    batch_size: int = 256,
    export_timeout_ms: int = 5000,
) -> Any:
    """
    Set up OpenTelemetry with Aigie exporter for LiveKit Agents.

    Creates a TracerProvider, registers the LiveKitAigieSpanExporter,
    and calls LiveKit's set_tracer_provider() so all LiveKit spans
    are automatically captured.

    Args:
        aigie_client: Initialized Aigie client
        service_name: OTel service name
        batch_size: Max spans per export batch
        export_timeout_ms: Export timeout in milliseconds

    Returns:
        TracerProvider instance (for cleanup)
    """
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        logger.warning(
            "[AIGIE-OTel] opentelemetry-sdk not installed. "
            "Install with: pip install aigie[livekit-otel]"
        )
        return None

    from .otel_exporter import LiveKitAigieSpanExporter

    # Create resource
    resource = Resource.create({"service.name": service_name})

    # Check if a provider already exists (user may have Datadog, etc.)
    existing_provider = trace.get_tracer_provider()
    provider = None

    if isinstance(existing_provider, TracerProvider):
        # Add our exporter to existing provider
        provider = existing_provider
        logger.info("[AIGIE-OTel] Adding Aigie exporter to existing TracerProvider")
    else:
        # Create new provider
        provider = TracerProvider(resource=resource)
        logger.info("[AIGIE-OTel] Created new TracerProvider")

    # Create and register exporter
    exporter = LiveKitAigieSpanExporter(aigie_client)
    processor = BatchSpanProcessor(
        exporter,
        max_queue_size=batch_size * 4,
        max_export_batch_size=batch_size,
        export_timeout_millis=export_timeout_ms,
    )
    provider.add_span_processor(processor)

    # Set as LiveKit's tracer provider
    try:
        from livekit.agents.telemetry import set_tracer_provider

        set_tracer_provider(provider)
        logger.info("[AIGIE-OTel] Registered with LiveKit via set_tracer_provider()")
    except ImportError:
        # Fallback: set as global OTel provider
        trace.set_tracer_provider(provider)
        logger.info(
            "[AIGIE-OTel] Set as global OTel TracerProvider (LiveKit telemetry module not found)"
        )

    return provider
