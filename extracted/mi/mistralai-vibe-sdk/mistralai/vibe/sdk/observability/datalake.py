"""Datalake telemetry event helpers.

The helper emits structured event payloads to the datalake. When
``DATALAKE_OTEL_EXPORTER_OTLP_ENDPOINT`` is set and the optional OpenTelemetry
packages are installed, events are sent through the OTLP log exporter configured
by the ``DATALAKE_*`` environment variables. Otherwise events are written through
the ``vibe_sdk.telemetry.datalake`` structlog logger with ``track=True`` for
host logging pipelines to ingest when configured.
"""

import asyncio
import ipaddress
import logging
import os
import uuid
from collections.abc import Awaitable, Mapping, Sequence
from dataclasses import dataclass
from importlib import import_module
from typing import Any, Literal, cast
from urllib.parse import urlparse

import structlog

from mistralai.vibe.sdk.observability.context import attributes_from_context
from mistralai.vibe.sdk.observability.conversion import str_to_bool

logger = structlog.get_logger("vibe_sdk.telemetry.datalake")

ERROR_EVENT = "telemetry.emit_failed"
AUTO_CONTEXT_PROPERTY_KEYS = (
    "session_id",
    "conversation_id",
)
LOGGER_NAME = "vibe_sdk.tracking.otel"
OTEL_EXPORTER_OTLP_PROTOCOLS = {"grpc", "http"}
_logger_provider: Any | None = None
_config: "DatalakeTelemetryConfig | None" = None
_otel_logger: "logging.Logger | None" = None


@dataclass(frozen=True)
class DatalakeTelemetryConfig:
    """Telemetry export settings for hosts that configure the SDK explicitly.

    Most applications can use ``from_env()`` to load ``DATALAKE_*`` settings.
    Instantiate this class directly when tests or embedded hosts need to pass
    telemetry settings without mutating process environment variables.
    """

    otel_exporter_otlp_endpoint: str = ""
    otel_exporter_otlp_protocol: Literal["grpc", "http"] = "grpc"
    otel_log_level: str = "INFO"
    console_tee: bool = False

    @classmethod
    def from_env(cls) -> "DatalakeTelemetryConfig":
        protocol = os.getenv("DATALAKE_OTEL_EXPORTER_OTLP_PROTOCOL", "grpc").lower()
        if protocol not in OTEL_EXPORTER_OTLP_PROTOCOLS:
            raise ValueError(f"Invalid OTLP protocol: {protocol}")
        typed_protocol = cast(Literal["grpc", "http"], protocol)

        return cls(
            otel_exporter_otlp_endpoint=os.getenv("DATALAKE_OTEL_EXPORTER_OTLP_ENDPOINT", ""),
            otel_exporter_otlp_protocol=typed_protocol,
            otel_log_level=os.getenv("DATALAKE_OTEL_LOG_LEVEL", "INFO"),
            console_tee=str_to_bool(os.getenv("DATALAKE_CONSOLE_TEE", "")),
        )

    @property
    def otel_enabled(self) -> bool:
        return bool(self.otel_exporter_otlp_endpoint)


def configure(config: DatalakeTelemetryConfig | None = None) -> None:
    """Initialize telemetry export before emitting SDK events.

    Host applications usually do not need to call this directly because emitters
    lazily load ``DATALAKE_*`` settings. Call it at startup when a host or test
    wants to provide an explicit ``DatalakeTelemetryConfig`` instead.
    """
    global _config, _otel_logger

    if is_configured():
        return

    next_config = config if config is not None else DatalakeTelemetryConfig.from_env()
    next_otel_logger = None
    if next_config.otel_enabled:
        next_otel_logger = _build_otel_logger(next_config)

    _config = next_config
    _otel_logger = next_otel_logger


def get_config() -> DatalakeTelemetryConfig:
    if not is_configured():
        configure()
    config = _config
    if config is None:
        raise RuntimeError("Telemetry configuration was not initialized")
    return config


def get_logger() -> logging.Logger:
    if not is_configured():
        get_config()
    otel_logger = _otel_logger
    if otel_logger is None:
        raise RuntimeError("OpenTelemetry logging is not configured")
    return otel_logger


def flush(timeout_millis: int = 30_000) -> bool:
    if _logger_provider is None:
        return True

    force_flush = getattr(_logger_provider, "force_flush", None)
    if force_flush is None:
        return True

    result = force_flush(timeout_millis=timeout_millis)
    if result is None:
        return True
    return bool(result)


def shutdown(timeout_millis: int = 30_000) -> None:
    global _logger_provider, _config, _otel_logger

    if _logger_provider is not None:
        flush(timeout_millis=timeout_millis)
        _logger_provider.shutdown()
        _logger_provider = None

    if _otel_logger is not None:
        for handler in _otel_logger.handlers[:]:
            _otel_logger.removeHandler(handler)
        _otel_logger = None

    _config = None


def is_configured() -> bool:
    return _config is not None


def is_otel_enabled() -> bool:
    get_config()
    return _otel_logger is not None


def _build_otel_logger(config: DatalakeTelemetryConfig) -> logging.Logger | None:
    """Create the named Python logger and attach the OTEL handler."""
    try:
        handler = _build_otel_handler(config)
    except ImportError:
        return None

    otel_logger = logging.getLogger(LOGGER_NAME)
    otel_logger.addHandler(handler)
    otel_logger.setLevel(config.otel_log_level)
    otel_logger.propagate = False
    return otel_logger


def _build_otel_handler(config: DatalakeTelemetryConfig) -> Any:
    """Build the OpenTelemetry provider, exporter, and log handler."""
    global _logger_provider

    sdk_logs = import_module("opentelemetry.sdk._logs")
    logger_provider = sdk_logs.LoggerProvider
    logging_handler = sdk_logs.LoggingHandler
    batch_log_record_processor = import_module(
        "opentelemetry.sdk._logs.export"
    ).BatchLogRecordProcessor
    resource = import_module("opentelemetry.sdk.resources").Resource

    if config.otel_exporter_otlp_protocol == "grpc":
        grpc_log_exporter = import_module(
            "opentelemetry.exporter.otlp.proto.grpc._log_exporter"
        ).OTLPLogExporter
        exporter = grpc_log_exporter(
            endpoint=config.otel_exporter_otlp_endpoint,
            insecure=_is_loopback_endpoint(config.otel_exporter_otlp_endpoint),
        )
    else:
        http_log_exporter = import_module(
            "opentelemetry.exporter.otlp.proto.http._log_exporter"
        ).OTLPLogExporter
        endpoint = config.otel_exporter_otlp_endpoint
        if not endpoint.startswith(("http://", "https://")):
            endpoint = "https://" + endpoint
        exporter = http_log_exporter(endpoint=endpoint.rstrip("/") + "/v1/logs")

    provider = logger_provider(resource=resource.create())
    try:
        provider.add_log_record_processor(batch_log_record_processor(exporter))
        handler = logging_handler(logger_provider=provider)
    except Exception:
        shutdown_provider = getattr(provider, "shutdown", None)
        if shutdown_provider is not None:
            shutdown_provider()
        raise

    _logger_provider = provider
    return handler


def _is_loopback_endpoint(endpoint: str) -> bool:
    host = _endpoint_host(endpoint)
    if host is None:
        return False
    normalized_host = host.rstrip(".").lower()
    if normalized_host == "localhost":
        return True
    try:
        return ipaddress.ip_address(normalized_host).is_loopback
    except ValueError:
        return False


def _endpoint_host(endpoint: str) -> str | None:
    value = endpoint.strip()
    if not value:
        return None
    parsed = urlparse(value if "://" in value else f"//{value}")
    return parsed.hostname


def _drop_none(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _drop_none(item) for key, item in value.items() if item is not None}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_drop_none(item) for item in value if item is not None]
    return value


def _build_extra(
    properties: dict[str, Any] | None,
    customer_uuid: str | uuid.UUID | None,
    correlation_id: str | None,
    workspace_uuid: str | uuid.UUID | None,
    user_uuid: str | uuid.UUID | None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Build the shared structured log payload."""
    event_properties = {
        **attributes_from_context(*AUTO_CONTEXT_PROPERTY_KEYS),
        **(properties or {}),
    }
    if customer_uuid is not None:
        event_properties["customer_id"] = str(customer_uuid)

    extra: dict[str, Any] = {"properties": event_properties, **kwargs}
    if customer_uuid is not None:
        extra["customer_uuid"] = str(customer_uuid)
    if correlation_id is not None:
        extra["correlation_id"] = correlation_id
    if workspace_uuid is not None:
        extra["workspace_uuid"] = str(workspace_uuid)
    if user_uuid is not None:
        extra["user_uuid"] = str(user_uuid)
    return cast(dict[str, Any], _drop_none(extra))


def track(
    event: str,
    *,
    properties: dict[str, Any] | None = None,
    correlation_id: str | None = None,
    customer_uuid: str | uuid.UUID | None = None,
    workspace_uuid: str | uuid.UUID | None = None,
    user_uuid: str | uuid.UUID | None = None,
    **kwargs: Any,
) -> None:
    try:
        extra = _build_extra(
            properties,
            customer_uuid,
            correlation_id,
            workspace_uuid,
            user_uuid,
            **kwargs,
        )
        _emit_to_configured_sink(event, extra, async_logger=False)
    except Exception:
        logger.warning(ERROR_EVENT, telemetry_event=event, exc_info=True)


async def atrack(
    event: str,
    *,
    properties: dict[str, Any] | None = None,
    correlation_id: str | None = None,
    customer_uuid: str | uuid.UUID | None = None,
    workspace_uuid: str | uuid.UUID | None = None,
    user_uuid: str | uuid.UUID | None = None,
    **kwargs: Any,
) -> None:
    try:
        extra = _build_extra(
            properties,
            customer_uuid,
            correlation_id,
            workspace_uuid,
            user_uuid,
            **kwargs,
        )

        pending_log = _emit_to_configured_sink(event, extra, async_logger=True)
        if pending_log is None:
            return

        try:
            await asyncio.shield(pending_log)
        except NotImplementedError:
            _emit_structlog_sync(event, extra, track=True if not is_otel_enabled() else None)
    except Exception:
        logger.warning(ERROR_EVENT, telemetry_event=event, exc_info=True)


def _emit_to_configured_sink(
    event: str,
    extra: dict[str, Any],
    *,
    async_logger: bool,
) -> Awaitable[Any] | None:
    if is_otel_enabled():
        config = get_config()
        get_logger().info(event, extra=extra)
        if not config.console_tee:
            return None
        if async_logger:
            return logger.ainfo(event, **extra)
        _emit_structlog_sync(event, extra, track=None)
        return None

    if async_logger:
        return logger.ainfo(event, track=True, **extra)
    _emit_structlog_sync(event, extra, track=True)
    return None


def _emit_structlog_sync(
    event: str,
    extra: dict[str, Any],
    *,
    track: bool | None,
) -> None:
    track_extra = {} if track is None else {"track": track}
    logger.info(event, **track_extra, **extra)
