from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.telemetry._config import TelemetryConfig


def build_sdk_resource(config: TelemetryConfig) -> Any:
    """Return an OTel Resource for the SDK, or None if opentelemetry is not installed."""
    try:
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.semconv.resource import ResourceAttributes
    except ImportError:
        return None

    return Resource.create(
        {
            ResourceAttributes.SERVICE_NAME: config.service_name,
            ResourceAttributes.SERVICE_VERSION: config.service_version,
            ResourceAttributes.TELEMETRY_SDK_NAME: "aigie-python-sdk",
            ResourceAttributes.TELEMETRY_SDK_VERSION: config.service_version,
            ResourceAttributes.TELEMETRY_SDK_LANGUAGE: "python",
            "aigie.sdk.version": config.service_version,
            "aigie.sdk.language": "python",
        }
    )
