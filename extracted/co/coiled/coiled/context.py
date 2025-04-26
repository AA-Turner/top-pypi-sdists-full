from __future__ import annotations

import asyncio
import functools
import random
import string
from contextlib import contextmanager, nullcontext
from contextvars import ContextVar
from datetime import datetime, timedelta, timezone
from logging import getLogger
from os import environ
from typing import Any, Awaitable, Callable, Dict, TypeVar, Union, cast
from urllib.parse import urlencode

import aiohttp

DDTRACE = environ.get("DD_TRACE_ENABLED", "true").lower() in ["true", "1"]
if DDTRACE:
    try:
        from ddtrace import tracer
        from ddtrace.propagation.http import HTTPPropagator
    except ImportError:
        DDTRACE = False

logger = getLogger(__name__)


def random_str(length: int = 8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Sessions last the entire duration of the python process
COILED_SESSION_ID = "coiled-session-" + random_str()
logger.debug(f"Coiled Session  ID : {COILED_SESSION_ID}")

# Operations are transient and more granular
# Note: we don't type the actual RHS value due to a bug in some versions of Python
# 3.7 and 3.8: https://bugs.python.org/issue38979
COILED_OP_CONTEXT: ContextVar[str] = ContextVar("coiled-operation-context", default="")
COILED_OP_NAME: ContextVar[str] = ContextVar("coiled-operation-name", default="")


TRACE_CONFIG = aiohttp.TraceConfig()


def get_datadog_trace_link(
    start: datetime | None = None,
    end: datetime | None = None,
    **filters: Dict[str, str],
):
    params = {
        "query": " ".join([f"@{k}:{v}" for k, v in filters.items()]),
        "paused": "true",
        "streamTraces": "false",
        "showAllSpans": "true",
    }
    if start:
        fuzzed = start - timedelta(minutes=1)
        params["start"] = str(int(fuzzed.timestamp() * 1000))
    if end:
        fuzzed = end + timedelta(minutes=1)
        params["end"] = str(int(fuzzed.timestamp() * 1000))
    return f"https://app.datadoghq.com/apm/traces?{urlencode(params)}"


@contextmanager
def operation_context(name: str):
    c_id = COILED_OP_CONTEXT.get()
    if c_id:
        # already in a coiled op context, don't create a new one
        yield c_id
    else:
        # create a new coiled context
        c_id = random_str()
        COILED_OP_CONTEXT.set(c_id)
        COILED_OP_NAME.set(name)

        logger.debug(f"Entering {name}-{c_id}")
        start = datetime.now(tz=timezone.utc)
        yield c_id
        trace_url = get_datadog_trace_link(
            start=start,
            end=datetime.now(tz=timezone.utc),
            **{"coiled-operation-id": c_id},  # pyright: ignore[reportArgumentType]
        )
        logger.debug(f"Exiting {name}-{c_id} - DD URL: {trace_url}")
        COILED_OP_CONTEXT.set("")
        COILED_OP_NAME.set("")


F = TypeVar("F", bound=Callable[..., Any])
SyncFuncType = Callable[..., Any]
AsyncFuncType = Callable[..., Awaitable[Any]]


def get_trace_context(func: Union[SyncFuncType, AsyncFuncType]):
    if DDTRACE and tracer.current_span():  # type: ignore
        return tracer.trace(name=f"{func.__module__}.{func.__qualname__}"), operation_context(  # type: ignore
            name=f"{func.__module__}.{func.__qualname__}"
        )
    else:
        return nullcontext(), nullcontext()


def track_context(func: F) -> F:
    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            trace_context = get_trace_context(func)
            with trace_context[0], trace_context[1]:
                return await func(*args, **kwargs)

        return cast(F, async_wrapper)
    else:

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            trace_context = get_trace_context(func)
            with trace_context[0], trace_context[1]:
                return func(*args, **kwargs)

        return cast(F, sync_wrapper)


def inject_tracing(headers: Dict[str, str]):
    headers.update(create_trace_data())


def create_trace_data() -> Dict[str, str]:
    trace_data: Dict[str, str] = {
        "coiled-session-id": COILED_SESSION_ID,
        "coiled-request-id": random_str(),
    }
    if DDTRACE:
        span = tracer.current_span()  # type: ignore
        if span:
            HTTPPropagator.inject(span_context=span.context, headers=trace_data)  # type: ignore
    op_id = COILED_OP_CONTEXT.get()
    if op_id:
        trace_data["coiled-operation-id"] = op_id
    op_name = COILED_OP_CONTEXT.get()
    if op_name:
        trace_data["coiled-operation-func"] = op_name
    return trace_data


async def on_request_start(session, trace_config_ctx, params):
    inject_tracing(headers=params.headers)


TRACE_CONFIG.on_request_start.append(on_request_start)
