from __future__ import annotations

import os
from dataclasses import dataclass


def _default_endpoint() -> str:
    """Derive the OTel collection base URL from the Aigie server URL env vars."""
    explicit = os.getenv("AIGIE_INTERNAL_OTEL_ENDPOINT")
    if explicit:
        return explicit
    base = os.getenv("AIGIE_URL") or os.getenv("KYTTE_URL") or os.getenv("AIGIE_API_URL") or ""
    return (base.rstrip("/") + "/otel") if base else ""


def _default_api_key() -> str:
    """Read the SDK API key used to authenticate OTel exports.

    Priority mirrors the main AigieConfig.aigie_token resolution:
    KYTTE_TOKEN (legacy) → AIGIE_TOKEN → AIGIE_API_KEY (deprecated fallback).
    """
    return os.getenv("KYTTE_TOKEN") or os.getenv("AIGIE_TOKEN") or os.getenv("AIGIE_API_KEY") or ""


@dataclass(frozen=True)
class TelemetryConfig:
    """Configuration for SDK-internal OTel telemetry. Frozen — immutable after creation."""

    enabled: bool
    endpoint: str
    api_key: str
    service_name: str
    service_version: str
    traces_enabled: bool
    metrics_enabled: bool
    logs_enabled: bool
    batch_schedule_delay_ms: int
    batch_max_queue_size: int
    batch_max_export_size: int
    export_timeout_ms: int
    metrics_export_interval_ms: int

    @classmethod
    def from_env(cls, service_version: str = "") -> TelemetryConfig:
        """Build config from environment variables with sensible defaults."""
        if not service_version:
            try:
                from aigie import __version__

                service_version = __version__
            except Exception:
                service_version = "unknown"

        return cls(
            enabled=os.getenv("AIGIE_INTERNAL_OTEL_ENABLED", "true").lower() != "false",
            endpoint=_default_endpoint(),
            api_key=_default_api_key(),
            service_name=os.getenv("AIGIE_INTERNAL_OTEL_SERVICE_NAME", "kytte-sdk"),
            service_version=service_version,
            traces_enabled=os.getenv("AIGIE_INTERNAL_OTEL_TRACES", "true").lower() != "false",
            metrics_enabled=os.getenv("AIGIE_INTERNAL_OTEL_METRICS", "true").lower() != "false",
            logs_enabled=os.getenv("AIGIE_INTERNAL_OTEL_LOGS", "true").lower() != "false",
            batch_schedule_delay_ms=int(os.getenv("AIGIE_INTERNAL_OTEL_BATCH_DELAY_MS", "5000")),
            batch_max_queue_size=int(os.getenv("AIGIE_INTERNAL_OTEL_MAX_QUEUE", "512")),
            batch_max_export_size=int(os.getenv("AIGIE_INTERNAL_OTEL_MAX_EXPORT", "256")),
            export_timeout_ms=int(os.getenv("AIGIE_INTERNAL_OTEL_TIMEOUT_MS", "10000")),
            metrics_export_interval_ms=int(
                os.getenv("AIGIE_INTERNAL_OTEL_METRICS_INTERVAL_MS", "60000")
            ),
        )
