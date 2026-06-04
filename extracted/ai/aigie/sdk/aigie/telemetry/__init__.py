from __future__ import annotations

import logging
import threading
from typing import Any

from aigie.telemetry._config import TelemetryConfig
from aigie.telemetry._judge_instruments import judge_logger, judge_tracer
from aigie.telemetry._noop import _NoOpProvider
from aigie.telemetry._safe import _metric_add, _metric_record, safe_span

__all__ = [
    "TelemetryConfig",
    "initialize",
    "get_provider",
    "get_tracer",
    "get_meter",
    "get_logger",
    "flush",
    "shutdown",
    "shutdown_sync",
    "judge_tracer",
    "judge_logger",
    "safe_span",
    "_metric_add",
    "_metric_record",
]

_log = logging.getLogger(__name__)
_PROVIDER: Any = _NoOpProvider()
_INITIALIZED = False
_LOCK = threading.Lock()


def initialize(config: TelemetryConfig) -> None:
    """Initialize the SDK telemetry provider. Idempotent — second call is a no-op with warning."""
    global _PROVIDER, _INITIALIZED
    with _LOCK:
        if _INITIALIZED or not isinstance(_PROVIDER, _NoOpProvider):
            _log.warning(
                "aigie telemetry already initialized; ignoring duplicate initialize() call"
            )
            return
        if not config.enabled:
            return
        if not config.endpoint:
            # Without a base URL the OTLP exporters would be built with
            # scheme-less endpoints like "/v1/metrics" and fail loudly on
            # every export interval. Stay no-op instead.
            from aigie.diagnostics import C004, format_diagnostic

            _log.warning(format_diagnostic(C004))
            _INITIALIZED = True
            return
        from aigie.telemetry._provider import SdkTelemetryProvider

        _PROVIDER = SdkTelemetryProvider(config)
        _INITIALIZED = True


def get_provider() -> Any:
    return _PROVIDER


def get_tracer(name: str, version: str | None = None) -> Any:
    return _PROVIDER.tracer(name, version)


def get_meter(name: str, version: str | None = None) -> Any:
    return _PROVIDER.meter(name, version)


def get_logger(name: str, version: str | None = None) -> Any:
    return _PROVIDER.logger(name, version)


async def flush(timeout_ms: int = 30_000) -> bool:
    return bool(await _PROVIDER.flush(timeout_ms))


async def shutdown(timeout_ms: int = 30_000) -> None:
    await _PROVIDER.shutdown(timeout_ms)


def shutdown_sync(timeout_ms: int = 30_000) -> None:
    _PROVIDER.shutdown_sync(timeout_ms)
