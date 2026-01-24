from __future__ import annotations

import contextlib
import os
import threading
import time
import types
from typing import TYPE_CHECKING, Any, Callable, Mapping, Union, cast

from chalk.utils._ddtrace_version import can_use_datadog_statsd, can_use_ddtrace
from chalk.utils._otel_version import can_use_otel_trace
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger

if TYPE_CHECKING:
    import ddtrace.context
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

    def safe_current_trace_context() -> ddtrace.context.Context | otel_trace.SpanContext | None:  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        return otel_trace.get_current_span().get_span_context()

    @contextlib.contextmanager
    def safe_activate_trace_context(  # pyright: ignore[reportRedeclaration]
        ctx: ddtrace.context.Context
        | ddtrace.Span
        | otel_trace.SpanContext
        | None,  # pyright: ignore[reportPrivateImportUsage]
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

elif can_use_ddtrace:
    import ddtrace
    from ddtrace.propagation.http import HTTPPropagator

    _logger.debug("ddtrace installed and available, using it to trace")

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        if not ddtrace.tracer.enabled:
            yield
            return
        if attributes is None:
            attributes = {}
        attributes = dict(attributes)
        attributes["thread_id"] = str(threading.get_native_id())
        with ddtrace.tracer.trace(name=span_id) as span:
            if hasattr(span, "_ignore_exception"):
                span._ignore_exception(GeneratorExit)  # pyright: ignore [reportPrivateUsage, reportArgumentType]
                from chalk.sql._internal.sql_source import UnsupportedEfficientExecutionError

                span._ignore_exception(  # pyright: ignore [reportPrivateUsage]
                    UnsupportedEfficientExecutionError  # pyright: ignore [reportArgumentType]
                )
            if attributes:
                span.set_tags(cast(Any, attributes))
            yield

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        span = ddtrace.tracer.current_span()
        if span:
            span.set_metrics(cast(Any, metrics))

    def safe_add_tags(tags: Mapping[str, str]):  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        span = ddtrace.tracer.current_span()
        if span:
            span.set_tags(cast(Any, tags))

    def safe_current_trace_context() -> ddtrace.context.Context | otel_trace.SpanContext | None:  # pyright: ignore[reportRedeclaration]
        configure_tracing("chalkpy")
        return ddtrace.tracer.current_trace_context()

    @contextlib.contextmanager
    def safe_activate_trace_context(  # pyright: ignore[reportRedeclaration]
        ctx: ddtrace.context.Context
        | ddtrace.Span
        | otel_trace.SpanContext
        | None,  # pyright: ignore[reportPrivateImportUsage]
    ):
        configure_tracing("chalkpy")
        if isinstance(ctx, ddtrace.context.Context) or isinstance(ctx, ddtrace.Span):
            ddtrace.tracer.context_provider.activate(ctx)
        yield

    def add_trace_headers(  # pyright: ignore[reportRedeclaration]
        input_headers: None | dict[str, str]
    ) -> dict[str, str]:
        configure_tracing("chalkpy")
        headers: dict[str, str] = dict(input_headers if input_headers is not None else {})
        span = ddtrace.tracer.current_span()
        if span:
            span.context.sampling_priority = 2
            span.set_tags({ddtrace.constants.SAMPLING_PRIORITY_KEY: 2})  # Ensure that sampling is enabled
            HTTPPropagator.inject(span.context, headers)
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

    def safe_current_trace_context() -> ddtrace.context.Context | otel_trace.SpanContext | None:  # pyright: ignore[reportRedeclaration]
        return

    @contextlib.contextmanager
    def safe_activate_trace_context(  # pyright: ignore[reportRedeclaration]
        ctx: ddtrace.context.Context
        | ddtrace.Span
        | otel_trace.Context
        | otel_trace.SpanContext
        | None,  # pyright: ignore[reportPrivateImportUsage]
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

        elif can_use_ddtrace:
            import ddtrace
            from ddtrace.filters import FilterRequestsOnUrl

            if ddtrace.config.service is None:
                ddtrace.config.service = default_service_name
            # Re-configuring the global tracer to capture any setting changes from environs from a .dotenv file
            # which might be loaded after the first ddtrace import

            ddtrace.tracer.configure(
                enabled=None if "DD_TRACE_ENABLED" not in os.environ else env_var_bool("DD_TRACE_ENABLED"),
                hostname=os.getenv("DD_AGENT_HOST") or os.getenv("DD_TRACE_AGENT_URL"),
                uds_path=os.getenv("DD_TRACE_AGENT_URL"),
                dogstatsd_url=os.getenv("DD_DOGSTATSD_URL"),
                api_version=os.getenv("DD_TRACE_API_VERSION"),
                compute_stats_enabled=env_var_bool("DD_TRACE_COMPUTE_STATS"),
                iast_enabled=None if "DD_IAST_ENABLED" not in os.environ else env_var_bool("DD_IAST_ENABLED"),
                # exclude healthcheck url from apm trace collection
                settings={
                    "FILTERS": [
                        FilterRequestsOnUrl(
                            [
                                r"^http://.*/healthcheck$",
                                r"^http://.*/ready$",
                                r"^http://[^/]*/$",  # exclude "/"
                            ]
                        )
                    ]
                },
            )
            if ddtrace.tracer.enabled:
                ddtrace.patch(
                    asyncio=True,
                    databricks=False,
                    fastapi=True,
                    futures=True,
                    httplib=True,
                    httpx=True,
                    psycopg=True,
                    redis=True,
                    requests=True,
                    sqlalchemy=False,
                    urllib3=True,
                )

            _logger.info(
                f"Configuring DDtrace tracing: enabled={ddtrace.tracer.enabled}, service={ddtrace.config.service}, env={ddtrace.config.env}, trace_agent_url: {ddtrace.config._trace_agent_url}, effective trace agent: {ddtrace.tracer._agent_url}"  # pyright: ignore [reportAttributeAccessIssue, reportPrivateUsage]
            )
        else:
            _logger.warning("neither opentelemetry nor ddtrace are installed")

    _TRACING_CONFIGURED.do_once(do_configure_tracing)
