"""Bounded retries for replay-safe SDK operations."""

from __future__ import annotations

import asyncio
import logging
import math
import random
import socket
import ssl
import time
from email.utils import parsedate_to_datetime
from collections.abc import Awaitable, Callable
from typing import TypeVar
from contextlib import contextmanager
from contextvars import ContextVar
from collections.abc import Iterator

import aiohttp
from aiohttp.http_exceptions import HttpProcessingError
import httpx

import runta as _public

T = TypeVar("T")
_MAX_BACKOFF_DELAY = 60.0
_READ_DEADLINE: ContextVar[float | None] = ContextVar(
    "runta_read_deadline", default=None
)
_LOG = logging.getLogger(__name__)
_TRANSIENT_HTTP_STATUSES = {408, 429, 502, 503, 504}


@contextmanager
def read_deadline(deadline: float) -> Iterator[None]:
    outer = _READ_DEADLINE.get()
    token = _READ_DEADLINE.set(deadline if outer is None else min(deadline, outer))
    try:
        yield
    finally:
        _READ_DEADLINE.reset(token)


def read_retry_deadline() -> float:
    deadline = time.monotonic() + 480
    outer = _READ_DEADLINE.get()
    return deadline if outer is None else min(deadline, outer)


def retryable_http_error(error: Exception) -> bool:
    if not isinstance(error, _public.ApiError):
        return False
    if error.status_code is not None:
        return error.status_code in _TRANSIENT_HTTP_STATUSES
    cause = error.__cause__
    if isinstance(cause, (aiohttp.ClientSSLError, aiohttp.ServerFingerprintMismatch)):
        return False
    if isinstance(cause, aiohttp.ClientResponseError):
        # HTTP parser failures correspond to httpx.RemoteProtocolError,
        # not to a completed HTTP response with a retryable status.
        return isinstance(cause.__cause__, HttpProcessingError)
    if isinstance(cause, aiohttp.ClientConnectorError):
        underlying = cause.os_error
        if isinstance(underlying, ssl.SSLError):
            return False
        if isinstance(underlying, socket.gaierror) and underlying.errno in {
            socket.EAI_NONAME,
            socket.EAI_FAIL,
        }:
            return False
        return True
    if isinstance(
        cause,
        (asyncio.TimeoutError, TimeoutError, aiohttp.ClientConnectionError, aiohttp.ClientPayloadError),
    ):
        return True
    if isinstance(
        cause,
        (
            httpx.TimeoutException,
            httpx.ReadError,
            httpx.WriteError,
            httpx.CloseError,
            httpx.RemoteProtocolError,
        ),
    ):
        return True
    if isinstance(cause, httpx.ConnectError):
        nested = cause.__cause__
        while nested is not None:
            if isinstance(nested, ssl.SSLError):
                return False
            if isinstance(nested, socket.gaierror) and nested.errno in {
                socket.EAI_NONAME,
                socket.EAI_FAIL,
            }:
                return False
            nested = nested.__cause__
        return True
    return False


def retryable_delete_error(error: Exception) -> bool:
    """Deletion can safely retry an internal server error on GET or DELETE."""
    return (
        isinstance(error, _public.ApiError) and error.status_code == 500
    ) or retryable_http_error(error)


def is_revision_conflict(error: _public.ApiError) -> bool:
    return (
        error.status_code == 409
        and error.code == "failed_precondition"
        and "runtime revision conflict:" in str(error)
    )


def patch_matches(body: object, runtime: object) -> bool:
    """Check only the public patch fields the caller actually supplied."""
    desired = body.to_dict()  # type: ignore[attr-defined]
    current = runtime.to_dict()  # type: ignore[attr-defined]
    for section, values in desired.get("resources", {}).items():
        for field, value in values.items():
            if current["resources"][section].get(field) != value:
                return False
    policy = desired.get("egress_policy")
    if policy is not None:
        existing = current["egress_policy"]
        if existing.get("mode") != policy["mode"]:
            return False
        field = "allowed_hosts" if policy["mode"] == "allowlist" else "denied_hosts"
        if set(existing.get(field, [])) != set(policy.get(field, [])):
            return False
    for name in ("auto_shutdown_policy", "auto_delete_policy"):
        policy = desired.get(name)
        if policy is not None:
            # An enabled policy resets its clock on save. Matching configuration
            # cannot prove this request applied, even if its seconds are equal.
            if policy["mode"] == "enabled" or current.get(name) != policy:
                return False
    if "tcp_allowlist" in desired:
        if set(current.get("tcp_allowlist", [])) != set(desired["tcp_allowlist"]):
            return False
    return True


def _delay(attempt: int, remaining: float | None) -> float:
    return _full_jitter_delay(float(2 ** (attempt - 1)), remaining)


def _full_jitter_delay(maximum: float, remaining: float | None) -> float:
    maximum = min(_MAX_BACKOFF_DELAY, maximum)
    if remaining is not None:
        maximum = min(maximum, max(0.0, remaining))
    return random.uniform(0.0, maximum)


def http_retry_delay(error: Exception, attempt: int, remaining: float | None) -> float:
    """Honor a valid 429 Retry-After without exceeding the operation retry budget."""
    value = getattr(error, "_retry_after", None)
    if isinstance(error, _public.ApiError) and error.status_code == 429 and value:
        try:
            value = value.strip()
            if value.isascii() and value.isdigit():
                delay = float(int(value))
            else:
                date = parsedate_to_datetime(value)
                if date.tzinfo is None:
                    raise ValueError("Retry-After date must include a timezone")
                delay = max(0.0, date.timestamp() - time.time())
            if not math.isfinite(delay):
                raise ValueError("Retry-After must be finite")
        except (ValueError, TypeError, OverflowError):
            pass
        else:
            return delay if remaining is None else min(delay, max(0.0, remaining))
    return _delay(attempt, remaining)


def retry_sync(
    operation: Callable[[float | None], T],
    *,
    name: str,
    attempts: int,
    retryable: Callable[[Exception], bool],
    deadline: float | None = None,
    delay: Callable[[Exception, int, float | None], float] | None = None,
) -> T:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            if last_error is not None:
                _LOG.error(
                    "%s exhausted after %d attempts: %s", name, attempt - 1, last_error
                )
                raise last_error.with_traceback(last_error.__traceback__)
            raise TimeoutError(f"{name} exceeded its operation deadline")
        try:
            return operation(remaining)
        except Exception as error:
            if not retryable(error):
                raise
            last_error = error
            remaining = None if deadline is None else deadline - time.monotonic()
            if attempt == attempts or (remaining is not None and remaining <= 0):
                _LOG.error("%s exhausted after %d attempts: %s", name, attempt, error)
                raise
            time.sleep(
                delay(error, attempt, remaining)
                if delay
                else _delay(attempt, remaining)
            )
    raise AssertionError("retry loop did not terminate")


async def retry_async(
    operation: Callable[[float | None], Awaitable[T]],
    *,
    name: str,
    attempts: int,
    retryable: Callable[[Exception], bool],
    deadline: float | None = None,
    delay: Callable[[Exception, int, float | None], float] | None = None,
) -> T:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            if last_error is not None:
                _LOG.error(
                    "%s exhausted after %d attempts: %s", name, attempt - 1, last_error
                )
                raise last_error.with_traceback(last_error.__traceback__)
            raise TimeoutError(f"{name} exceeded its operation deadline")
        try:
            return await operation(remaining)
        except Exception as error:
            if not retryable(error):
                raise
            last_error = error
            remaining = None if deadline is None else deadline - time.monotonic()
            if attempt == attempts or (remaining is not None and remaining <= 0):
                _LOG.error("%s exhausted after %d attempts: %s", name, attempt, error)
                raise
            await asyncio.sleep(
                delay(error, attempt, remaining)
                if delay
                else _delay(attempt, remaining)
            )
    raise AssertionError("retry loop did not terminate")
