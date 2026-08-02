"""Shared HTTP/SSE/retry helpers for streaming completion adapters.

Provider-agnostic plumbing reused by the adapters and for the retry
machinery.
"""

from collections.abc import AsyncIterator, Callable

import httpx
import structlog
from tenacity import (
    AsyncRetrying,
    RetryCallState,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

logger = structlog.get_logger()

RETRYABLE_STATUS_CODES = frozenset({408, 429, 502, 503, 504})

_RETRYABLE_HTTPX_ERRORS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.RemoteProtocolError,
)


class StreamHTTPError(RuntimeError):
    """Base error for a non-success HTTP response from a streaming LLM API."""

    def __init__(self, message: str, *, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(message)


def is_retryable_httpx_error(exc: BaseException) -> bool:
    """Return whether a transport-level httpx failure is safe to retry."""
    return isinstance(exc, _RETRYABLE_HTTPX_ERRORS)


def is_retryable_stream_error(exc: BaseException) -> bool:
    """Return whether an LLM call failure looks transient and safe to retry."""
    if is_retryable_httpx_error(exc):
        return True
    return isinstance(exc, StreamHTTPError) and exc.status_code in RETRYABLE_STATUS_CODES


def build_stream_open_retrying(
    *,
    retry: Callable[[BaseException], bool] = is_retryable_stream_error,
    log_event: str = "stream_retry",
    status_of: Callable[[BaseException], int | None] = lambda exc: getattr(
        exc, "status_code", None
    ),
) -> AsyncRetrying:
    """Build the retry policy for initial stream acquisition.

    This only wraps the initial request that opens the streaming response.
    Once bytes have started flowing, retrying would risk duplicating already
    emitted downstream chunks.
    """

    def before_sleep(retry_state: RetryCallState) -> None:
        if retry_state.outcome is None:
            return
        exc = retry_state.outcome.exception()
        if exc is None:
            return
        logger.warning(
            log_event,
            attempt=retry_state.attempt_number,
            sleep_seconds=retry_state.next_action.sleep if retry_state.next_action else None,
            exception_type=type(exc).__name__,
            status_code=status_of(exc),
            retryable=retry(exc),
        )

    return AsyncRetrying(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception(retry),
        before_sleep=before_sleep,
        reraise=True,
    )


async def iter_sse_data(response: httpx.Response) -> AsyncIterator[str]:
    """Yield parsed SSE ``data:`` payloads from an HTTP streaming response.

    Comment lines (``:``) and any non-``data:`` lines (such as Anthropic's
    ``event:`` lines) are ignored; multi-line ``data:`` payloads are joined and
    flushed on each blank-line event separator.
    """
    data_lines: list[str] = []

    async for line in response.aiter_lines():
        if not line:
            if data_lines:
                yield "\n".join(data_lines)
                data_lines = []
            continue
        if line.startswith(":"):
            continue
        if not line.startswith("data:"):
            continue

        data_lines.append(line[5:].lstrip())

    if data_lines:
        yield "\n".join(data_lines)
