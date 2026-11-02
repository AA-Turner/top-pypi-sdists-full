import asyncio
from collections.abc import Awaitable, Callable, Iterable
from typing import TypeVar

import httpx
import requests
from httpx import (
    HTTPStatusError,
    codes,
)
from requests.exceptions import HTTPError as RequestsHTTPError
from tenacity import RetryCallState
from tqdm.asyncio import tqdm

T = TypeVar("T")


# The server refused the request without processing it.
NON_IDEMPOTENT_RETRYABLE_HTTP_STATUS_CODES = {codes.TOO_MANY_REQUESTS}
# Retry if the request is idempotent
RETRYABLE_HTTP_STATUS_CODES = {
    *NON_IDEMPOTENT_RETRYABLE_HTTP_STATUS_CODES,
    codes.INTERNAL_SERVER_ERROR,
    codes.BAD_GATEWAY,
    codes.SERVICE_UNAVAILABLE,
    codes.GATEWAY_TIMEOUT,
}
# The server may have processed the request before failing to answer it.
AMBIGUOUS_HTTP_STATUS_CODES = (
    RETRYABLE_HTTP_STATUS_CODES - NON_IDEMPOTENT_RETRYABLE_HTTP_STATUS_CODES
)


# Always safe to retry
_PRE_REQUEST_CONNECTION_ERRORS = (
    requests.ConnectTimeout,
    httpx.ConnectError,
    httpx.ConnectTimeout,
)
# Can retry if the request is idempotent
_BASE_CONNECTION_ERRORS = (
    *_PRE_REQUEST_CONNECTION_ERRORS,
    ConnectionError,
    # From requests
    requests.Timeout,
    requests.ConnectionError,
    requests.RequestException,
    # From httpx
    httpx.ReadTimeout,
    httpx.ReadError,
    httpx.NetworkError,
    httpx.RemoteProtocolError,
    httpx.CloseError,
)


def _create_retry_predicate(
    connection_errors: tuple[type[BaseException], ...],
    status_codes: set[codes],
    additional_exceptions: tuple[type[BaseException], ...],
) -> Callable[[RetryCallState], bool]:
    def _is_retryable(exception: BaseException | None) -> bool:
        while exception is not None:
            # HTTP status errors are retryable only on transient status codes. Check these
            # before the connection-error families below: requests' HTTPError is itself a
            # RequestException, so a blanket connection-error match would retry permanent
            # 4xx responses (e.g. a 403/404 from a GCS signed-URL download).
            if isinstance(exception, HTTPStatusError):
                return exception.response.status_code in status_codes
            if isinstance(exception, RequestsHTTPError):
                response = exception.response
                if response is None:
                    return False
                return response.status_code in status_codes
            # connection errors
            if isinstance(exception, connection_errors):
                return True
            # custom exceptions provided
            if additional_exceptions and isinstance(exception, additional_exceptions):
                return True
            exception = exception.__cause__
        return False

    def status_retries_with_exceptions(retry_state: RetryCallState) -> bool:
        if retry_state.outcome is not None and hasattr(
            retry_state.outcome, "exception"
        ):
            return _is_retryable(retry_state.outcome.exception())
        return False

    return status_retries_with_exceptions


def create_retry_if_connection_error(
    *additional_exceptions: type[BaseException],
) -> Callable[[RetryCallState], bool]:
    """Create a retry condition with base connection errors, HTTP status errors, plus additional exceptions.

    Walks the `__cause__` chain: methods routinely catch a transient error and re-raise a
    domain error (e.g. `raise DataStorageRetrievalError(...) from e`), which would otherwise hide the
    underlying connection error from this predicate and defeat the retry entirely.
    """
    return _create_retry_predicate(
        _BASE_CONNECTION_ERRORS, RETRYABLE_HTTP_STATUS_CODES, additional_exceptions
    )


def create_retry_if_connection_error_not_idempotent(
    *additional_exceptions: type[BaseException],
) -> Callable[[RetryCallState], bool]:
    """See `create_retry_if_connection_error`, but for requests that aren't idempotent."""
    return _create_retry_predicate(
        _PRE_REQUEST_CONNECTION_ERRORS,
        NON_IDEMPOTENT_RETRYABLE_HTTP_STATUS_CODES,
        additional_exceptions,
    )


retry_if_connection_error = create_retry_if_connection_error()
retry_if_connection_error_not_idempotent = (
    create_retry_if_connection_error_not_idempotent()
)


async def gather_with_concurrency(
    n: int | asyncio.Semaphore, coros: Iterable[Awaitable[T]], progress: bool = False
) -> list[T]:
    """
    Run asyncio.gather with a concurrency limit.

    SEE: https://stackoverflow.com/a/61478547/2392535
    """
    semaphore = asyncio.Semaphore(n) if isinstance(n, int) else n

    async def sem_coro(coro: Awaitable[T]) -> T:
        async with semaphore:
            return await coro

    if progress:
        return await tqdm.gather(
            *(sem_coro(c) for c in coros), desc="Gathering", ncols=0
        )

    return await asyncio.gather(*(sem_coro(c) for c in coros))
