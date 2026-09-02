"""Best-effort OpenTelemetry tracing for the CLI / AI Watch.

Design constraints:
- Must stay importable inside the ``aiwatch`` PyInstaller bundle, so this module
  imports only stdlib + structlog at top level. All OpenTelemetry imports are
  deferred into functions and guarded, so a missing/!bundled OTEL degrades to a
  no-op rather than crashing a scan.
- Telemetry is never allowed to slow or break a scan: every public function
  swallows its own errors and returns quietly.

Spans are exported via OTLP/HTTP to the backend's authenticated trace-ingest
route (``/api/v1/telemetry/traces``), which forwards them to the collector and
on to Tempo. The CLI also injects a W3C ``traceparent`` into its backend
requests so a scan and its backend ingest form one connected trace.
"""

from __future__ import annotations

import contextlib
import os
import threading
from collections.abc import Iterator
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

_TRACER_NAME = "runlayer.cli"
_TRACES_PATH = "/api/v1/telemetry/traces"

_lock = threading.Lock()
_initialized = False
_enabled = False
_provider: Any = None
_tracer: Any = None


def _telemetry_disabled() -> bool:
    val = os.getenv("RUNLAYER_TELEMETRY_DISABLED") or os.getenv(
        "RUNLAYER_DISABLE_TELEMETRY"
    )
    return str(val).strip().lower() in {"1", "true", "yes", "on"}


def init_cli_tracing(
    *,
    host: str | None,
    api_key: str | None,
    collector_version: str | None = None,
    service_name: str = "runlayer-cli",
) -> None:
    """Initialize CLI tracing. Idempotent and best-effort (no-op on any failure).

    Disabled when telemetry is opted out, when host/api_key are missing (offline
    / unauthenticated), or when OpenTelemetry is not available.
    """
    global _initialized, _enabled, _provider, _tracer

    with _lock:
        if _initialized:
            return
        _initialized = True

        if _telemetry_disabled() or not host or not api_key:
            return

        try:
            # Deferred heavy optional imports: keep the aiwatch bundle import-safe
            # and avoid paying OTEL import cost on every CLI invocation.
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )
            from opentelemetry.sdk.resources import SERVICE_NAME, Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            resource_attrs: dict[str, str] = {SERVICE_NAME: service_name}
            if collector_version:
                resource_attrs["service.version"] = collector_version

            endpoint = f"{host.rstrip('/')}{_TRACES_PATH}"
            # Short export timeout: it bounds the exporter's internal retry
            # backoff (5xx retries sleep 1s/2s/4s... up to the timeout), so a
            # backend that rejects traces can't hang CLI exit for ~7s.
            exporter = OTLPSpanExporter(
                endpoint=endpoint,
                headers={"x-runlayer-api-key": api_key},
                timeout=2,
            )
            provider = TracerProvider(resource=Resource.create(resource_attrs))
            provider.add_span_processor(BatchSpanProcessor(exporter))

            _provider = provider
            _tracer = provider.get_tracer(_TRACER_NAME)
            _enabled = True
        except Exception as e:
            logger.debug("cli_tracing_init_skipped", error=str(e))


@contextlib.contextmanager
def command_span(name: str, **attributes: Any) -> Iterator[None]:
    """Start a span around a unit of work. No-op when tracing is disabled."""
    if not _enabled or _tracer is None:
        yield
        return

    try:
        # Best-effort usage telemetry: don't let normal control-flow exits
        # (e.g. typer.Exit on no-results / dry-run) get recorded as span errors.
        span_cm = _tracer.start_as_current_span(
            name, record_exception=False, set_status_on_exception=False
        )
    except Exception:
        yield
        return

    with span_cm as span:
        for key, value in attributes.items():
            if value is not None:
                with contextlib.suppress(Exception):
                    span.set_attribute(key, value)
        yield


def inject_trace_context(headers: dict[str, str]) -> None:
    """Inject the current W3C trace context into outbound request headers.

    Mutates ``headers`` in place. No-op when tracing is disabled.
    """
    if not _enabled:
        return
    try:
        from opentelemetry.propagate import inject

        inject(headers)
    except Exception:
        pass


def shutdown_cli_tracing() -> None:
    """Flush and shut down the exporter. Best-effort, bounded."""
    global _initialized, _enabled, _provider, _tracer

    with _lock:
        provider = _provider
        if provider is None:
            _initialized = False
            return
        try:
            # Bounded flush so process exit is not blocked on a slow backend.
            provider.force_flush(timeout_millis=2000)
            provider.shutdown()
        except Exception as e:
            logger.debug("cli_tracing_shutdown_skipped", error=str(e))
        finally:
            _enabled = False
            _initialized = False
            _provider = None
            _tracer = None
