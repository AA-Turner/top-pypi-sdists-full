from __future__ import annotations

import contextlib
import os
import threading
import time
import types
from typing import TYPE_CHECKING, Any, Mapping, Union, cast

from chalk.utils.environment_parsing import env_var_bool

if TYPE_CHECKING:
    import ddtrace.context

try:
    import ddtrace
    from datadog.dogstatsd.base import statsd

    def safe_set_gauge(gauge: str, value: int | float):
        statsd.gauge(gauge, value)

    def safe_incr(counter: str, value: int | float, tags: list[str] | None = None):
        statsd.increment(counter, value, tags)

    def safe_distribution(counter: str, value: int | float, tags: list[str] | None = None):
        statsd.distribution(counter, value, tags)

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):
        if not ddtrace.tracer.enabled:
            yield
            return
        if (current_ctx := ddtrace.tracer.current_trace_context()) is None:
            yield
            return
        if (priority := current_ctx.sampling_priority) is not None and priority <= 0:
            # If a priority is negative, then it won't be sampled
            # See https://github.com/DataDog/dd-trace-py/blob/09edef713bf9f0ab30f554bf7765d7a7c2ed6f30/ddtrace/constants.py#L74
            # Not sure what a priority=None means
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

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):
        span = ddtrace.tracer.current_span()
        if span:
            span.set_metrics(cast(Any, metrics))

    def safe_add_tags(tags: Mapping[str, str]):
        span = ddtrace.tracer.current_span()
        if span:
            span.set_tags(cast(Any, tags))

    def safe_current_trace_context():  # pyright: ignore[reportRedeclaration]
        return ddtrace.tracer.current_trace_context()

    def safe_activate_trace_context(
        ctx: ddtrace.context.Context | ddtrace.Span | None,  # pyright: ignore[reportPrivateImportUsage]
    ) -> None:
        ddtrace.tracer.context_provider.activate(ctx)

except ImportError:

    def safe_set_gauge(gauge: str, value: int | float):
        pass

    def safe_incr(counter: str, value: int | float, tags: list[str] | None = None):
        pass

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):
        yield

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):
        pass

    def safe_add_tags(tags: Mapping[str, str]):
        pass

    def safe_current_trace_context():
        return

    def safe_activate_trace_context(
        ctx: ddtrace.context.Context | ddtrace.Span | None,  # pyright: ignore[reportPrivateImportUsage]
    ) -> None:
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
    from chalk.utils.log_with_context import get_logger

    _logger = get_logger(__name__)

    try:
        import ddtrace
        from ddtrace.filters import FilterRequestsOnUrl
    except ImportError:
        _logger.warning("ddtrace is not installed")
        return

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
