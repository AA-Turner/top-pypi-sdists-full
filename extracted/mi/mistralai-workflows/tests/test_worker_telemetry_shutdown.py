import atexit
import threading
import time
from collections.abc import Callable, Sequence
from typing import Any

import pytest
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, LogRecordExporter, LogRecordExportResult
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    MetricExporter,
    MetricExportResult,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter, SpanExportResult

from mistralai.workflows.core import worker
from mistralai.workflows.core.tracing import _otel_config
from mistralai.workflows.core.tracing.exporters import OtelExportOptions


class _DelayedMetricExporter(MetricExporter):
    """Stands in for an OTLP exporter; a blocked export stands in for a telemetry endpoint that does not answer."""

    def __init__(self, *, blocked: bool = False) -> None:
        super().__init__(preferred_temporality={Counter: AggregationTemporality.CUMULATIVE})
        self.release = threading.Event()
        if not blocked:
            self.release.set()
        self.exports = 0
        self.exported_names: set[str] = set()

    def export(self, metrics_data: Any, timeout_millis: float = 10_000, **kwargs: Any) -> MetricExportResult:
        self.exports += 1
        for resource_metrics in metrics_data.resource_metrics:
            for scope_metrics in resource_metrics.scope_metrics:
                self.exported_names.update(metric.name for metric in scope_metrics.metrics)
        self.release.wait(5)
        return MetricExportResult.SUCCESS

    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        return True

    def shutdown(self, timeout_millis: float = 30_000, **kwargs: Any) -> None:
        return None


class _BlockedLogExporter(LogRecordExporter):
    """Stands in for an OTLP exporter on an endpoint that does not answer, until released."""

    def __init__(self) -> None:
        self.release = threading.Event()
        self.exports = 0

    def export(self, batch: Any) -> LogRecordExportResult:
        self.exports += 1
        self.release.wait(5)
        return LogRecordExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30_000) -> bool:
        return True

    def shutdown(self) -> None:
        return None


class _BlockedSpanExporter(SpanExporter):
    """Stands in for an OTLP exporter on an endpoint that does not answer, until released."""

    def __init__(self, *, blocked: bool) -> None:
        self.release = threading.Event()
        if not blocked:
            self.release.set()
        self.exports = 0

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        self.exports += 1
        self.release.wait(5)
        return SpanExportResult.SUCCESS


def _join_new_thread(name: str, before: set[threading.Thread]) -> None:
    """Join the shutdown thread a test left running, so it does not outlive the test."""
    for thread in set(threading.enumerate()) - before:
        if thread.name == name:
            thread.join(5)


class _RecordingLogger:
    def __init__(self) -> None:
        self.warnings: list[str] = []

    def warning(self, event: str, **_kwargs: object) -> None:
        self.warnings.append(event)


def _provider_with_one_metric(exporter: _DelayedMetricExporter) -> MeterProvider:
    provider = MeterProvider(
        metric_readers=[PeriodicExportingMetricReader(exporter, export_interval_millis=60_000)],
        shutdown_on_exit=False,
    )
    provider.get_meter("test").create_counter("temporal_workflow_completed_total").add(1)
    return provider


class TestRuntimeMetricsOnShutdown:
    def test_a_slow_exporter_does_not_hold_up_the_shutdown(self) -> None:
        exporter = _DelayedMetricExporter(blocked=True)
        provider = _provider_with_one_metric(exporter)
        before = set(threading.enumerate())

        started = time.monotonic()
        worker._flush_runtime_metrics(provider, shared=False, deadline=started + 0.2)
        elapsed = time.monotonic() - started
        exporter.release.set()
        for thread in set(threading.enumerate()) - before:
            thread.join(5)

        assert elapsed < 1.0
        assert exporter.exports == 1

    def test_the_shared_local_provider_is_exported_and_left_running(self) -> None:
        exporter = _DelayedMetricExporter()
        provider = _provider_with_one_metric(exporter)

        worker._flush_runtime_metrics(provider, shared=True, deadline=time.monotonic())
        flushed = set(exporter.exported_names)
        provider.get_meter("test").create_counter("temporal_workflow_failed_total").add(1)
        provider.force_flush()

        assert flushed == {"temporal_workflow_completed_total"}
        assert "temporal_workflow_failed_total" in exporter.exported_names


class TestLogsOnShutdown:
    def test_a_slow_exporter_does_not_hold_up_the_shutdown(self, monkeypatch: pytest.MonkeyPatch) -> None:
        recorder = _RecordingLogger()
        monkeypatch.setattr(worker, "logger", recorder)
        exporter = _BlockedLogExporter()
        provider = LoggerProvider(shutdown_on_exit=False)
        provider.add_log_record_processor(BatchLogRecordProcessor(exporter, schedule_delay_millis=60_000))
        provider.get_logger("test").emit(body="teardown")
        before = set(threading.enumerate())

        started = time.monotonic()
        worker._shutdown_logs(provider, deadline=started + 0.2)
        elapsed = time.monotonic() - started
        exporter.release.set()
        _join_new_thread("otel-log-shutdown", before)

        assert elapsed < 1.0
        assert exporter.exports == 1
        assert len(recorder.warnings) == 1


class TestTracesOnExit:
    @pytest.mark.parametrize(("blocked", "warnings"), [(True, 1), (False, 0)], ids=["slow", "fast"])
    def test_the_exit_waits_at_most_the_deadline_and_warns_when_spans_are_dropped(
        self, monkeypatch: pytest.MonkeyPatch, blocked: bool, warnings: int
    ) -> None:
        recorder = _RecordingLogger()
        monkeypatch.setattr(_otel_config, "logger", recorder)
        monkeypatch.setattr(_otel_config, "_TRACES_SHUTDOWN_TIMEOUT_SECONDS", 0.2)
        exporter = _BlockedSpanExporter(blocked=blocked)
        provider = TracerProvider(shutdown_on_exit=False)
        provider.add_span_processor(BatchSpanProcessor(exporter, schedule_delay_millis=60_000))
        with provider.get_tracer("test").start_as_current_span("teardown"):
            pass
        before = set(threading.enumerate())

        started = time.monotonic()
        _otel_config._shutdown_traces(provider)
        elapsed = time.monotonic() - started
        exporter.release.set()
        _join_new_thread("otel-trace-shutdown", before)

        assert elapsed < 1.0
        assert exporter.exports == 1
        assert len(recorder.warnings) == warnings

    def test_the_tracer_provider_is_shut_down_at_exit_by_the_bounded_shutdown_only(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        registered: list[tuple[Callable[..., object], tuple[object, ...]]] = []

        def _record(func: Callable[..., object], *args: object) -> Callable[..., object]:
            registered.append((func, args))
            return func

        monkeypatch.setattr(atexit, "register", _record)
        off = OtelExportOptions(enabled=False)

        _, tracer_provider, _ = _otel_config.config_otel(
            "worker", "test", trace_config=off, metric_config=off, log_config=off
        )

        assert (_otel_config._shutdown_traces, (tracer_provider,)) in registered
        assert (tracer_provider.shutdown, ()) not in registered
