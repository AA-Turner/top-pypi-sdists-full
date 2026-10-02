"""Sync HTTP helper for v16-server / LT requests.

httpx + tenacity, fresh client per request (no stale connections across a long device
session), retry on transport errors and transient status codes. 4xx pass through — a
404 from /api/v1/autoheal is an authoritative "no match", not something to retry.

RETRY POLICY. Three things decide whether an attempt is repeated:

- Transient STATUS codes (408/429/499/502/503/504) retry for every method. The server
  declined before doing the work, so there is no side effect to duplicate.
- CONNECT failures (ConnectError, ConnectTimeout) retry for every method. The
  connection never opened, so the request was never sent.
- RESPONSE failures (ReadError, RemoteProtocolError) retry for IDEMPOTENT methods
  only. They mean the request WAS sent and the reply was lost; re-sending a
  POST/PUT/PATCH/DELETE on that evidence duplicates a side effect the server may
  already have applied — a second row, a second charge, a second delete. DELETE
  counts as non-idempotent here, deliberately unlike the HTTP spec's classification.

TIMEOUT SEMANTICS. `timeout` is the httpx client timeout, so it bounds ONE attempt.
Callers that also pass `total_timeout_s` get one wall-clock budget shared by every
attempt and retry wait; each attempt receives only what remains of that budget.
"""
import logging
import os
import time

import httpx
from tenacity import (
    Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential,
)

from testmu_appium import _config
from testmu_appium._step import get_instruction_id

logging.getLogger("httpx").setLevel(logging.ERROR)  # only surface httpx errors
_log = logging.getLogger("testmu_appium")
_monotonic = time.monotonic

# 408 Request Timeout, 429 Too Many Requests, 499 Client Closed Request,
# 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout.
TRANSIENT_HTTP_STATUS_CODES = {408, 429, 499, 502, 503, 504}

#: Total attempts, including the first. Bounded so one bad gateway cannot turn a
#: mobile session's calls into a stampede.
MAX_ATTEMPTS = 3

#: Module-level so tests can swap it for wait_none() and exercise the COUNT.
_RETRY_WAIT = wait_exponential(multiplier=1, min=1, max=10)

#: Retryable whatever the method: nothing was sent, or nothing was done.
_ALWAYS_RETRYABLE = (httpx.ConnectError, httpx.ConnectTimeout)

#: Retryable only when re-sending is harmless — see the module docstring.
_RESPONSE_RETRYABLE = (httpx.ReadError, httpx.RemoteProtocolError)

#: Methods whose replay may duplicate a server-side side effect.
_NON_IDEMPOTENT_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


class TransientHTTPError(Exception):
    """A transient HTTP status that should be retried."""

    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message or f"Transient HTTP error with status code {status_code}"
        super().__init__(self.message)


def _is_transient_http_error(status_code: int) -> bool:
    return status_code in TRANSIENT_HTTP_STATUS_CODES


def _is_non_idempotent(method: str) -> bool:
    return str(method or "").upper() in _NON_IDEMPOTENT_METHODS


def _retry_predicate(method: str):
    """The exception types worth repeating for this method."""
    retryable = _ALWAYS_RETRYABLE + (TransientHTTPError,)
    if not _is_non_idempotent(method):
        retryable += _RESPONSE_RETRYABLE
    return retry_if_exception_type(retryable)


def auth() -> tuple | None:
    """Basic auth from LT credentials, or None when they are absent."""
    username = os.getenv("LT_USERNAME", "")
    accesskey = os.getenv("LT_ACCESS_KEY", "")
    if username and accesskey:
        return (username, accesskey)
    return None


def headers() -> dict:
    """Shared request headers: session id + source, mirroring the web bindings.

    Accept-Encoding is pinned to gzip/deflate: the gateway answers a br-negotiated
    request with a bogus 400.
    """
    result = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "x-source": os.getenv("TESTMUAI_SOURCE", "local"),
    }
    session_id = os.getenv("TESTMUAI_SESSION_ID", "")
    if session_id:
        result["x-session-id"] = session_id
    test_id = _config.get("test_id") or os.getenv("TESTMUAI_TEST_ID", "")
    if test_id:
        result["x-test-id"] = test_id
    instruction_id = get_instruction_id()
    if instruction_id:
        result["x-instruction-id"] = instruction_id
    return result


def _request_once(
    method: str,
    url: str,
    *,
    headers: dict | None = None,
    json_data: dict | None = None,
    data=None,
    params: dict | None = None,
    timeout: int = 120,
    auth: tuple | None = None,
    verify: bool = True,
    proxy: str | None = None,
    silent: bool = False,
    follow_redirects: bool = True,
) -> httpx.Response:
    """One attempt. Raises TransientHTTPError so the retry layer can see the status."""
    if not silent:
        _log.info("%s -> %s", method, url)
    start = time.time()
    with httpx.Client(timeout=timeout, follow_redirects=follow_redirects, verify=verify, proxy=proxy) as client:
        kwargs: dict = {"headers": headers}
        if params:
            kwargs["params"] = params
        if json_data is not None:
            kwargs["json"] = json_data
        elif data is not None:
            if isinstance(data, (str, bytes, bytearray, memoryview)):
                kwargs["content"] = data
            else:
                kwargs["data"] = data
        if auth is not None:
            kwargs["auth"] = auth

        response = client.request(method, url, **kwargs)
        if not silent:
            _log.info(
                "%s -> %s completed in %.2fs (status: %s)",
                method, url, time.time() - start, response.status_code,
            )
        if _is_transient_http_error(response.status_code):
            raise TransientHTTPError(
                response.status_code,
                f"Transient HTTP error: {response.status_code} for {method} {url}",
            )
        return response


def request_with_retry(
    method: str,
    url: str,
    *,
    total_timeout_s: float | None = None,
    **kwargs,
) -> httpx.Response:
    """Issue one HTTP request, repeating it only where repeating is safe.

    The retry predicate is built per call because it depends on the METHOD — see the
    module docstring.

    `timeout` (in kwargs) bounds one attempt. `total_timeout_s`, when supplied,
    bounds all attempts and backoff together.
    """
    deadline = (
        None if total_timeout_s is None
        else _monotonic() + max(0.0, float(total_timeout_s))
    )
    configured_timeout = kwargs.get("timeout")

    def bounded_request(method, url, **attempt_kwargs):
        if deadline is not None:
            remaining = deadline - _monotonic()
            if remaining <= 0:
                raise httpx.TimeoutException(
                    f"request retry budget exhausted for {method} {url}"
                )
            if configured_timeout is None:
                attempt_kwargs["timeout"] = remaining
            else:
                attempt_kwargs["timeout"] = min(
                    float(configured_timeout), remaining
                )
        return _request_once(method, url, **attempt_kwargs)

    def bounded_wait(retry_state):
        delay = float(_RETRY_WAIT(retry_state))
        if deadline is None:
            return delay
        return min(delay, max(0.0, deadline - _monotonic()))

    retryer = Retrying(
        stop=stop_after_attempt(MAX_ATTEMPTS),
        wait=bounded_wait,
        retry=_retry_predicate(method),
        reraise=True,
    )
    return retryer(bounded_request, method, url, **kwargs)
