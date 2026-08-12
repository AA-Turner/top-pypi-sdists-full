from __future__ import annotations

import contextlib
import secrets
import threading
import time
import types
from typing import TYPE_CHECKING, Callable, Mapping, TypeAlias, Union

from chalk.utils._datadog_version import get_datadog_statsd
from chalk.utils._otel_version import can_use_otel_trace
from chalk.utils.log_with_context import get_logger

if TYPE_CHECKING:
    from opentelemetry import trace as otel_trace

    TraceContext: TypeAlias = otel_trace.SpanContext
else:
    TraceContext = object


class Once:
    """Execute a function exactly once and block all callers until the function returns

    Same as golang's `sync.Once <https://pkg.go.dev/sync#Once>`_
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._done = False
        super().__init__()

    def do_once(self, func: Callable[[], None]) -> bool:
        """Execute ``func`` if it hasn't been executed or return.

        Will block until ``func`` has been called by one thread.

        Returns:
            Whether or not ``func`` was executed in this call
        """

        # fast path, try to avoid locking
        if self._done:
            return False

        with self._lock:
            if not self._done:
                func()
                self._done = True
                return True
        return False


_TRACING_CONFIGURED = Once()
_logger = get_logger(__name__)

if can_use_otel_trace:
    import os as _os

    from opentelemetry import context as otel_context
    from opentelemetry import trace as otel_trace
    from opentelemetry.propagate import inject as otel_inject

    _logger.debug("OTEL trace packages installed, otel tracing is available")

    # Skip span allocation when no exporter is configured.
    _TRACING_ENABLED: bool = _os.environ.get("OTEL_TRACES_SAMPLER") != "always_off" and any(
        _os.environ.get(var)
        for var in (
            "OTEL_EXPORTER_OTLP_ENDPOINT",
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
        )
    )

    class _NoOpSpan:
        """Duck-typed no-op Span. Yielded by `safe_trace` when tracing is disabled."""

        __slots__ = ()

        def set_attribute(self, *args: object, **kwargs: object) -> "_NoOpSpan":
            return self

        def set_attributes(self, *args: object, **kwargs: object) -> "_NoOpSpan":
            return self

        def set_status(self, *args: object, **kwargs: object) -> "_NoOpSpan":
            return self

        def add_event(self, *args: object, **kwargs: object) -> "_NoOpSpan":
            return self

        def record_exception(self, *args: object, **kwargs: object) -> "_NoOpSpan":
            return self

        def update_name(self, *args: object, **kwargs: object) -> "_NoOpSpan":
            return self

        def end(self, *args: object, **kwargs: object) -> None:
            return None

        def is_recording(self) -> bool:
            return False

        def get_span_context(self):  # noqa: ANN201 — match Span API
            return otel_trace.INVALID_SPAN_CONTEXT

        def __enter__(self) -> "_NoOpSpan":
            return self

        def __exit__(self, *exc_info: object) -> None:
            return None

    _NOOP_SPAN: _NoOpSpan = _NoOpSpan()

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):  # pyright: ignore[reportRedeclaration]
        if not _TRACING_ENABLED:
            yield _NOOP_SPAN
            return
        configure_tracing("chalkpy")
        if attributes is None:
            attributes = {}
        attributes = dict(attributes)
        attributes["thread_id"] = str(threading.get_native_id())
        with otel_trace.get_tracer("chalk").start_as_current_span(span_id) as span:
            span.set_attributes(attributes)
            yield span

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):  # pyright: ignore[reportRedeclaration]
        if not _TRACING_ENABLED:
            return
        configure_tracing("chalkpy")
        current_span = otel_trace.get_current_span()
        current_span.set_attributes(dict(metrics))

    def safe_add_tags(tags: Mapping[str, str]):
        if not _TRACING_ENABLED:
            return
        configure_tracing("chalkpy")
        current_span = otel_trace.get_current_span()
        current_span.set_attributes(dict(tags))

    def safe_current_trace_context() -> otel_trace.SpanContext | None:  # pyright: ignore[reportRedeclaration]
        if not _TRACING_ENABLED:
            return None
        configure_tracing("chalkpy")
        return otel_trace.get_current_span().get_span_context()

    def current_trace_context() -> TraceContext | None:  # pyright: ignore[reportRedeclaration]
        span_context = otel_trace.get_current_span().get_span_context()
        if not span_context.is_valid:
            return None
        return span_context

    def current_or_new_trace_context() -> TraceContext:  # pyright: ignore[reportRedeclaration]
        trace_context = current_trace_context()
        if trace_context is not None:
            return trace_context
        trace_id = 0
        while trace_id == 0:
            trace_id = secrets.randbits(128)
        span_id = 0
        while span_id == 0:
            span_id = secrets.randbits(64)
        return otel_trace.SpanContext(
            trace_id=trace_id,
            span_id=span_id,
            is_remote=False,
            trace_flags=otel_trace.TraceFlags(otel_trace.TraceFlags.SAMPLED),
            trace_state=otel_trace.TraceState(),
        )

    def inject_trace_context(  # pyright: ignore[reportRedeclaration]
        carrier: None | Mapping[str, Union[str, bytes]],
        trace_context: TraceContext | None = None,
    ) -> dict[str, Union[str, bytes]]:
        output = dict(carrier if carrier is not None else {})
        if trace_context is None:
            trace_context = current_trace_context()
        if trace_context is None:
            return output
        if not trace_context.is_valid:
            return output
        context = otel_trace.set_span_in_context(otel_trace.NonRecordingSpan(trace_context))
        otel_inject(output, context=context)
        return output

    @contextlib.contextmanager
    def safe_activate_trace_context(  # pyright: ignore[reportRedeclaration]
        ctx: otel_trace.SpanContext | None,  # pyright: ignore[reportPrivateImportUsage]
    ):
        configure_tracing("chalkpy")
        if isinstance(ctx, otel_trace.SpanContext):
            new_span = otel_trace.NonRecordingSpan(ctx)
            new_context = otel_trace.set_span_in_context(new_span)
            token = otel_context.attach(new_context)
            yield
            otel_context.detach(token)
        else:
            yield

else:
    _logger.debug("no trace packages found, tracing will not work")

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):  # pyright: ignore[reportRedeclaration]
        yield

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):  # pyright: ignore[reportRedeclaration]
        pass

    def safe_add_tags(tags: Mapping[str, str]):  # pyright: ignore[reportRedeclaration]
        pass

    def safe_current_trace_context() -> None:  # pyright: ignore[reportRedeclaration]
        return

    def current_trace_context() -> None:  # pyright: ignore[reportRedeclaration]
        return None

    def current_or_new_trace_context() -> None:  # pyright: ignore[reportRedeclaration]
        return None

    def inject_trace_context(  # pyright: ignore[reportRedeclaration]
        carrier: None | Mapping[str, Union[str, bytes]],
        trace_context: TraceContext | None = None,
    ) -> dict[str, Union[str, bytes]]:
        return dict(carrier if carrier is not None else {})

    @contextlib.contextmanager
    def safe_activate_trace_context(  # pyright: ignore[reportRedeclaration]
        ctx: None,
    ):
        yield


def safe_set_gauge(gauge: str, value: int | float, tags: list[str] | None = None):
    """Set a Datadog gauge when StatsD is available; otherwise do nothing."""
    statsd = get_datadog_statsd()
    if statsd is not None:
        statsd.gauge(gauge, value, tags=tags)


def safe_incr(counter: str, value: int | float, tags: list[str] | None = None):
    """Increment a Datadog counter when StatsD is available; otherwise do nothing."""
    statsd = get_datadog_statsd()
    if statsd is not None:
        statsd.increment(counter, value, tags)


def safe_distribution(counter: str, value: int | float, tags: list[str] | None = None):
    """Record a Datadog distribution when StatsD is available; otherwise do nothing."""
    statsd = get_datadog_statsd()
    if statsd is not None:
        statsd.distribution(counter, value, tags)


class PerfTimer:
    def __init__(self):
        super().__init__()
        self._start = None
        self._end = None

    def __enter__(self):
        """Start a new timer as a context manager"""
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_typ: type[BaseException] | None, exc: BaseException | None, tb: types.TracebackType | None):
        """Stop the context manager timer"""
        self._end = time.perf_counter()

    @property
    def duration_seconds(self):
        assert self._start is not None
        end = time.perf_counter() if self._end is None else self._end
        return end - self._start

    @property
    def duration_ms(self):
        return self.duration_seconds * 1_000


def configure_tracing(default_service_name: str):
    def do_configure_tracing():
        from chalk.utils.log_with_context import get_logger

        _logger = get_logger(__name__)

        if can_use_otel_trace:
            from opentelemetry import trace as otel_trace
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider

            provider = TracerProvider(
                resource=Resource.create(
                    {
                        "service.name": default_service_name,
                    }
                ),
            )
            otel_trace.set_tracer_provider(provider)

        else:
            _logger.warning("opentelemetry is not installed, tracing will not work")

    _TRACING_CONFIGURED.do_once(do_configure_tracing)
