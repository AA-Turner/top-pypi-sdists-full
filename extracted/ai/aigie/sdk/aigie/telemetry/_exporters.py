from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.telemetry._config import TelemetryConfig


def _auth_headers(config: TelemetryConfig) -> dict[str, str]:
    """Return Authorization header dict if an API key is configured, else empty."""
    if config.api_key:
        return {"Authorization": f"Bearer {config.api_key}"}
    return {}


def make_span_exporter(config: TelemetryConfig) -> Any:
    """Create an OTLP/HTTP span exporter, or return None if package not installed."""
    try:
        from opentelemetry.exporter.otlp.proto.http import Compression
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    except ImportError:
        return None

    return OTLPSpanExporter(
        endpoint=f"{config.endpoint}/v1/traces",
        headers=_auth_headers(config),
        timeout=config.export_timeout_ms // 1000,
        compression=Compression.Gzip,
    )


def make_metric_exporter(config: TelemetryConfig) -> Any:
    """Create an OTLP/HTTP metric exporter, or return None if package not installed."""
    try:
        from opentelemetry.exporter.otlp.proto.http import Compression
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    except ImportError:
        return None

    return OTLPMetricExporter(
        endpoint=f"{config.endpoint}/v1/metrics",
        headers=_auth_headers(config),
        timeout=config.export_timeout_ms // 1000,
        compression=Compression.Gzip,
    )


def make_log_exporter(config: TelemetryConfig) -> Any:
    """Create an OTLP/HTTP log exporter, or return None if package not installed."""
    return _try_make_log_exporter(config)


def _try_make_log_exporter(config: TelemetryConfig) -> Any:
    try:
        from opentelemetry.exporter.otlp.proto.http import Compression

        exporter_cls = _get_log_exporter_cls()
        if exporter_cls is None:
            return None
        return exporter_cls(
            endpoint=f"{config.endpoint}/v1/logs",
            headers=_auth_headers(config),
            timeout=config.export_timeout_ms // 1000,
            compression=Compression.Gzip,
        )
    except Exception:
        return None


def _get_log_exporter_cls() -> Any:
    """Try multiple import paths for the log exporter (varies by OTel version)."""
    try:
        from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

        return OTLPLogExporter
    except ImportError:
        pass
    try:
        from opentelemetry.exporter.otlp.proto.http.log_exporter import (
            OTLPLogExporter,  # type: ignore[no-redef]
        )

        return OTLPLogExporter
    except ImportError:
        return None
