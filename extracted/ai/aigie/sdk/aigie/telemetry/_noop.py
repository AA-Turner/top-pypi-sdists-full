from __future__ import annotations

import contextlib
from collections.abc import Generator
from typing import Any


class _NoOpSpan:
    """No-op span — all methods are silent."""

    def set_attribute(self, key: str, value: Any) -> _NoOpSpan:
        return self

    def set_status(self, *args: Any, **kwargs: Any) -> _NoOpSpan:
        return self

    def add_event(self, *args: Any, **kwargs: Any) -> _NoOpSpan:
        return self

    def record_exception(self, *args: Any, **kwargs: Any) -> _NoOpSpan:
        return self

    def end(self, *args: Any, **kwargs: Any) -> None:
        pass


class _NoOpTracer:
    """No-op tracer — returns context managers that yield _NoOpSpan."""

    @contextlib.contextmanager
    def start_as_current_span(self, name: str, **kwargs: Any) -> Generator[_NoOpSpan, None, None]:
        yield _NoOpSpan()

    @contextlib.contextmanager
    def start_span(self, name: str, **kwargs: Any) -> Generator[_NoOpSpan, None, None]:
        yield _NoOpSpan()


class _NoOpCounter:
    def add(self, amount: float, attributes: Any = None, **kwargs: Any) -> None:
        pass


class _NoOpHistogram:
    def record(self, amount: float, attributes: Any = None, **kwargs: Any) -> None:
        pass


class _NoOpUpDownCounter:
    def add(self, amount: float, attributes: Any = None, **kwargs: Any) -> None:
        pass


class _NoOpMeter:
    def create_counter(self, name: str, **kwargs: Any) -> _NoOpCounter:
        return _NoOpCounter()

    def create_histogram(self, name: str, **kwargs: Any) -> _NoOpHistogram:
        return _NoOpHistogram()

    def create_up_down_counter(self, name: str, **kwargs: Any) -> _NoOpUpDownCounter:
        return _NoOpUpDownCounter()

    def create_observable_gauge(self, name: str, **kwargs: Any) -> _NoOpObservableGauge:
        return _NoOpObservableGauge()


class _NoOpObservableGauge:
    pass


class _NoOpLogger:
    def emit(self, record: Any) -> None:
        pass


class _NoOpProvider:
    """Returned when telemetry is disabled or opentelemetry-sdk is not installed."""

    is_initialized: bool = False

    def tracer(self, name: str, version: str | None = None) -> _NoOpTracer:
        return _NoOpTracer()

    def meter(self, name: str, version: str | None = None) -> _NoOpMeter:
        return _NoOpMeter()

    def logger(self, name: str, version: str | None = None) -> _NoOpLogger:
        return _NoOpLogger()

    async def flush(self, timeout_ms: int = 30_000) -> bool:
        return True

    async def shutdown(self, timeout_ms: int = 30_000) -> None:
        pass

    def shutdown_sync(self, timeout_ms: int = 30_000) -> None:
        pass
