from types import SimpleNamespace
from typing import cast

import httpx
import requests
from tenacity import RetryCallState

from edison_client.clients.exceptions import DataStorageRetrievalError
from edison_client.utils.general import (
    create_retry_if_connection_error,
    create_retry_if_connection_error_not_idempotent,
)


def _retry_state(exc: BaseException) -> RetryCallState:
    """A stand-in tenacity `RetryCallState` whose outcome raised `exc`."""
    return cast(
        RetryCallState, SimpleNamespace(outcome=SimpleNamespace(exception=lambda: exc))
    )


def _requests_http_error(status_code: int) -> requests.HTTPError:
    response = requests.Response()
    response.status_code = status_code
    return requests.HTTPError(response=response)


def test_raw_connection_error_is_retryable():
    should_retry = create_retry_if_connection_error()
    assert should_retry(_retry_state(httpx.ConnectError("boom"))) is True


def test_connection_error_wrapped_via_cause_is_retryable():
    """A transient error re-raised as a domain error (`raise ... from e`) still retries."""
    should_retry = create_retry_if_connection_error()
    try:
        raise httpx.ReadTimeout("Timeout on reading data from socket")
    except httpx.ReadTimeout as e:
        wrapped = DataStorageRetrievalError("An unexpected error occurred")
        wrapped.__cause__ = e
    assert should_retry(_retry_state(wrapped)) is True


def test_non_connection_error_is_not_retryable():
    should_retry = create_retry_if_connection_error()
    try:
        raise ValueError("not transient")
    except ValueError as e:
        wrapped = DataStorageRetrievalError("An unexpected error occurred")
        wrapped.__cause__ = e
    assert should_retry(_retry_state(wrapped)) is False


def test_wrapped_requests_http_error_is_gated_on_status_code():
    """A re-raised requests HTTPError retries on transient 5xx but not on permanent 4xx.

    Unlike connection errors, requests' HTTPError must not be blanket-retried just because
    it is a RequestException (e.g. a 403/404 from a GCS signed-URL download is permanent).
    """
    should_retry = create_retry_if_connection_error()

    wrapped_503 = DataStorageRetrievalError("Failed to download from GCS")
    wrapped_503.__cause__ = _requests_http_error(503)
    assert should_retry(_retry_state(wrapped_503)) is True

    wrapped_403 = DataStorageRetrievalError("Failed to download from GCS")
    wrapped_403.__cause__ = _requests_http_error(403)
    assert should_retry(_retry_state(wrapped_403)) is False


def _httpx_status_error(status_code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://example.test/v0.1/chat")
    return httpx.HTTPStatusError(
        "status", request=request, response=httpx.Response(status_code, request=request)
    )


def test_not_idempotent_retries_only_when_the_request_never_left():
    should_retry = create_retry_if_connection_error_not_idempotent()
    assert should_retry(_retry_state(httpx.ConnectError("refused"))) is True
    assert should_retry(_retry_state(httpx.ConnectTimeout("slow handshake"))) is True
    assert should_retry(_retry_state(requests.ConnectTimeout())) is True
    # The server may already have processed the request.
    assert should_retry(_retry_state(httpx.ReadTimeout("slow response"))) is False
    assert should_retry(_retry_state(httpx.RemoteProtocolError("closed"))) is False
    assert should_retry(_retry_state(requests.Timeout())) is False


def test_not_idempotent_retries_only_a_rate_limit_status():
    should_retry = create_retry_if_connection_error_not_idempotent()
    assert should_retry(_retry_state(_httpx_status_error(429))) is True
    assert should_retry(_retry_state(_httpx_status_error(500))) is False
    assert should_retry(_retry_state(_httpx_status_error(503))) is False
    assert should_retry(_retry_state(_httpx_status_error(502))) is False


def test_not_idempotent_still_walks_the_cause_chain():
    should_retry = create_retry_if_connection_error_not_idempotent()
    wrapped = DataStorageRetrievalError("wrapped")
    wrapped.__cause__ = httpx.ConnectError("refused")
    assert should_retry(_retry_state(wrapped)) is True
