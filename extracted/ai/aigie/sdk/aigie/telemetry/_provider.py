from __future__ import annotations

import asyncio
import logging
import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.telemetry._config import TelemetryConfig

_log = logging.getLogger(__name__)


class SdkTelemetryProvider:
    """Isolated OTel provider for SDK-internal telemetry. Never sets global providers."""

    def __init__(self, config: TelemetryConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
        self._is_shutdown = False
        self._tracer_provider: Any = None
        self._meter_provider: Any = None
        self._logger_provider: Any = None
        self._initialize()

    def _initialize(self) -> None:
        if self._config.traces_enabled:
            self._tracer_provider = self._build_tracer_provider()
        if self._config.metrics_enabled:
            self._meter_provider = self._build_meter_provider()
        if self._config.logs_enabled:
            self._logger_provider = self._build_logger_provider()
        self._auto_instrument()

    def _build_tracer_provider(self) -> Any:
        try:
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            from aigie.telemetry._exporters import make_span_exporter
            from aigie.telemetry._resource import build_sdk_resource
        except ImportError:
            return None

        exporter = make_span_exporter(self._config)
        if exporter is None:
            return None
        resource = build_sdk_resource(self._config)
        provider = TracerProvider(resource=resource) if resource else TracerProvider()
        processor = BatchSpanProcessor(
            exporter,
            max_queue_size=self._config.batch_max_queue_size,
            schedule_delay_millis=self._config.batch_schedule_delay_ms,
            max_export_batch_size=self._config.batch_max_export_size,
            export_timeout_millis=self._config.export_timeout_ms,
        )
        provider.add_span_processor(processor)
        return provider

    def _build_meter_provider(self) -> Any:
        try:
            from opentelemetry.sdk.metrics import MeterProvider
            from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

            from aigie.telemetry._exporters import make_metric_exporter
            from aigie.telemetry._resource import build_sdk_resource
        except ImportError:
            return None

        exporter = make_metric_exporter(self._config)
        if exporter is None:
            return None
        resource = build_sdk_resource(self._config)
        reader = PeriodicExportingMetricReader(
            exporter=exporter,
            export_interval_millis=self._config.metrics_export_interval_ms,
            export_timeout_millis=self._config.export_timeout_ms,
        )
        kwargs: dict[str, Any] = {"metric_readers": [reader]}
        if resource:
            kwargs["resource"] = resource
        provider = MeterProvider(**kwargs)

        from aigie.telemetry._heartbeat import register_heartbeat_gauge

        register_heartbeat_gauge(provider)
        return provider

    def _build_logger_provider(self) -> Any:
        try:
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            from aigie.telemetry._exporters import make_log_exporter
            from aigie.telemetry._resource import build_sdk_resource
        except ImportError:
            return None

        exporter = make_log_exporter(self._config)
        if exporter is None:
            return None
        resource = build_sdk_resource(self._config)
        provider = LoggerProvider(resource=resource) if resource else LoggerProvider()
        provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        return provider

    def _auto_instrument(self) -> None:
        try:
            from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

            HTTPXClientInstrumentor().instrument()
        except Exception as exc:
            _log.debug("HTTPXClientInstrumentor not available: %s", exc)
        try:
            from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

            GrpcInstrumentorClient().instrument()
        except Exception as exc:
            _log.debug("GrpcInstrumentorClient not available: %s", exc)

    def _noop_tracer(self) -> Any:
        from aigie.telemetry._noop import _NoOpTracer

        return _NoOpTracer()

    def _noop_meter(self) -> Any:
        from aigie.telemetry._noop import _NoOpMeter

        return _NoOpMeter()

    def _noop_logger(self) -> Any:
        from aigie.telemetry._noop import _NoOpLogger

        return _NoOpLogger()

    def tracer(self, name: str, version: str | None = None) -> Any:
        if self._is_shutdown or self._tracer_provider is None:
            return self._noop_tracer()
        try:
            return self._tracer_provider.get_tracer(name, version)
        except Exception:
            return self._noop_tracer()

    def meter(self, name: str, version: str | None = None) -> Any:
        if self._is_shutdown or self._meter_provider is None:
            return self._noop_meter()
        try:
            return self._meter_provider.get_meter(name, version)
        except Exception:
            return self._noop_meter()

    def logger(self, name: str, version: str | None = None) -> Any:
        if self._is_shutdown or self._logger_provider is None:
            return self._noop_logger()
        try:
            return self._logger_provider.get_logger(name, version)
        except Exception:
            return self._noop_logger()

    async def flush(self, timeout_ms: int = 30_000) -> bool:
        success = True
        loop = asyncio.get_event_loop()
        for provider in (self._tracer_provider, self._meter_provider, self._logger_provider):
            if provider is None:
                continue
            try:
                await loop.run_in_executor(None, lambda p=provider: p.force_flush(timeout_ms))  # type: ignore[misc]
            except RuntimeError:
                # Thread pool already shut down (interpreter exit) — flush synchronously.
                try:
                    provider.force_flush(timeout_ms)
                except Exception as exc:
                    _log.warning("telemetry flush error: %s", exc)
                    success = False
            except Exception as exc:
                _log.warning("telemetry flush error: %s", exc)
                success = False
        return success

    async def shutdown(self, timeout_ms: int = 30_000) -> None:
        with self._lock:
            if self._is_shutdown:
                return
            self._is_shutdown = True
        await self.flush(timeout_ms)
        for provider in (self._tracer_provider, self._meter_provider, self._logger_provider):
            if provider is None:
                continue
            try:
                provider.shutdown()
            except Exception as exc:
                _log.warning("telemetry shutdown error: %s", exc)

    def shutdown_sync(self, timeout_ms: int = 30_000) -> None:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.shutdown(timeout_ms))
            else:
                loop.run_until_complete(self.shutdown(timeout_ms))
        except RuntimeError:
            asyncio.run(self.shutdown(timeout_ms))

    @property
    def is_initialized(self) -> bool:
        return not self._is_shutdown

    @property
    def config(self) -> TelemetryConfig:
        return self._config
