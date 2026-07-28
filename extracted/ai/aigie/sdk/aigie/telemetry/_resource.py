from __future__ import annotations

import os
import uuid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.telemetry._config import TelemetryConfig

# Generated once per process (traces/metrics/logs each get their own
# Resource.create() call, but must carry the same value so the platform can
# correlate them to one running instance).
_INSTANCE_ID = str(uuid.uuid4())


def _regenerate_instance_id() -> None:
    global _INSTANCE_ID
    _INSTANCE_ID = str(uuid.uuid4())


# A forked child otherwise inherits the parent's _INSTANCE_ID (e.g. gunicorn/uvicorn
# preload workers), making every worker look like the same connection to the platform.
# register_at_fork is POSIX-only.
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_regenerate_instance_id)


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
            "service.instance.id": _INSTANCE_ID,
        }
    )
