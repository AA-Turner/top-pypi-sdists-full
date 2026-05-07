from __future__ import annotations

import contextlib
import threading
import time
import types
from typing import TYPE_CHECKING, Callable, Mapping, Union

from chalk.utils._datadog_version import can_use_datadog_statsd
from chalk.utils._otel_version import can_use_otel_trace
from chalk.utils.log_with_context import get_logger

if TYPE_CHECKING:
    from opentelemetry import trace as otel_trace


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
    from opentelemetry import context as otel_context
    from opentelemetry import trace as otel_trace
    from opentelemetry.propagate import inject as otel_inject

    _logger.debug("OTEL trace packages installed, otel tracing is available")

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        if attributes is None:
            attributes = {}
        attributes = dict(attributes)
        attributes["thread_id"] = str(threading.get_native_id())
        with otel_trace.get_tracer("chalk").start_as_current_span(span_id) as span:
            span.set_attributes(attributes)
            yield span

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        current_span = otel_trace.get_current_span()
        current_span.set_attributes(dict(metrics))

    def safe_add_tags(tags: Mapping[str, str]):
        configure_tracing("chalkpy")
        current_span = otel_trace.get_current_span()
        current_span.set_attributes(dict(tags))

    def safe_current_trace_context() -> otel_trace.SpanContext | None:  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        return otel_trace.get_current_span().get_span_context()

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

    def add_trace_headers(  # pyright: ignore[reportRedeclaration]
        input_headers: None | dict[str, str]
    ) -> dict[str, str]:
        configure_tracing("chalkpy")
        current_span_ctx = otel_trace.get_current_span().get_span_context()
        new_span_ctx = otel_trace.SpanContext(
            trace_id=current_span_ctx.trace_id,
            span_id=current_span_ctx.span_id,
            is_remote=current_span_ctx.is_remote,
            trace_flags=otel_trace.TraceFlags(otel_trace.TraceFlags.SAMPLED),
            trace_state=current_span_ctx.trace_state,
        )
        ctx = otel_trace.set_span_in_context(otel_trace.NonRecordingSpan(new_span_ctx))
        headers: dict[str, str] = dict(input_headers if input_headers is not None else {})
        otel_inject(headers, context=ctx)
        return headers

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

    @contextlib.contextmanager
    def safe_activate_trace_context(  # pyright: ignore[reportRedeclaration]
        ctx: None,
    ):
        yield

    def add_trace_headers(headers: None | dict[str, str]) -> dict[str, str]:  # pyright: ignore[reportRedeclaration]
        if headers is None:
            return {}
        return headers


if can_use_datadog_statsd:
    from datadog.dogstatsd.base import statsd

    def safe_set_gauge(gauge: str, value: int | float, tags: list[str] | None = None):
        statsd.gauge(gauge, value, tags=tags)

    def safe_incr(counter: str, value: int | float, tags: list[str] | None = None):
        statsd.increment(counter, value, tags)

    def safe_distribution(counter: str, value: int | float, tags: list[str] | None = None):
        statsd.distribution(counter, value, tags)

else:

    def safe_set_gauge(gauge: str, value: int | float, tags: list[str] | None = None):
        pass

    def safe_incr(counter: str, value: int | float, tags: list[str] | None = None):
        pass

    def safe_distribution(counter: str, value: int | float, tags: list[str] | None = None):
        pass


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
