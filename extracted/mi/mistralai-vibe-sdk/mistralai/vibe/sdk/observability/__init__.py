"""Observability helpers."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "DatalakeTelemetryConfig",
    "COMMON_CONTEXT_KEYS",
    "ObservabilityAttributes",
    "RequestMetadata",
    "SESSION_OBSERVABILITY_ATTRIBUTE_KEYS",
    "SPAN_CONTEXT_KEYS",
    "TelemetryCallType",
    "attributes_from_context",
    "atrack",
    "configure",
    "configure_logging",
    "configure_tracing",
    "flush",
    "get_config",
    "get_logger",
    "is_configured",
    "is_otel_enabled",
    "logger",
    "observability_context",
    "shutdown",
    "track",
    "upsert_in_context",
    "validate_observability_attributes",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.observability.context import (
        COMMON_CONTEXT_KEYS,
        SESSION_OBSERVABILITY_ATTRIBUTE_KEYS,
        SPAN_CONTEXT_KEYS,
        ObservabilityAttributes,
        attributes_from_context,
        observability_context,
        upsert_in_context,
        validate_observability_attributes,
    )
    from mistralai.vibe.sdk.observability.datalake import (
        DatalakeTelemetryConfig,
        atrack,
        configure,
        flush,
        get_config,
        get_logger,
        is_configured,
        is_otel_enabled,
        logger,
        shutdown,
        track,
    )
    from mistralai.vibe.sdk.observability.logging import configure_logging
    from mistralai.vibe.sdk.observability.otel import configure_tracing
    from mistralai.vibe.sdk.observability.request_metadata import (
        RequestMetadata,
        TelemetryCallType,
    )

_LAZY_EXPORTS = {
    "COMMON_CONTEXT_KEYS": "mistralai.vibe.sdk.observability.context",
    "SESSION_OBSERVABILITY_ATTRIBUTE_KEYS": "mistralai.vibe.sdk.observability.context",
    "SPAN_CONTEXT_KEYS": "mistralai.vibe.sdk.observability.context",
    "ObservabilityAttributes": "mistralai.vibe.sdk.observability.context",
    "attributes_from_context": "mistralai.vibe.sdk.observability.context",
    "observability_context": "mistralai.vibe.sdk.observability.context",
    "upsert_in_context": "mistralai.vibe.sdk.observability.context",
    "validate_observability_attributes": "mistralai.vibe.sdk.observability.context",
    "DatalakeTelemetryConfig": "mistralai.vibe.sdk.observability.datalake",
    "atrack": "mistralai.vibe.sdk.observability.datalake",
    "configure": "mistralai.vibe.sdk.observability.datalake",
    "flush": "mistralai.vibe.sdk.observability.datalake",
    "get_config": "mistralai.vibe.sdk.observability.datalake",
    "get_logger": "mistralai.vibe.sdk.observability.datalake",
    "is_configured": "mistralai.vibe.sdk.observability.datalake",
    "is_otel_enabled": "mistralai.vibe.sdk.observability.datalake",
    "logger": "mistralai.vibe.sdk.observability.datalake",
    "shutdown": "mistralai.vibe.sdk.observability.datalake",
    "track": "mistralai.vibe.sdk.observability.datalake",
    "configure_logging": "mistralai.vibe.sdk.observability.logging",
    "configure_tracing": "mistralai.vibe.sdk.observability.otel",
    "RequestMetadata": "mistralai.vibe.sdk.observability.request_metadata",
    "TelemetryCallType": "mistralai.vibe.sdk.observability.request_metadata",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
