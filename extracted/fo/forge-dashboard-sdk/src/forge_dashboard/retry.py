"""Retry transport for httpx: exponential backoff with jitter on 429/5xx,
honoring a server-sent ``Retry-After`` (seconds or an HTTP-date) ahead of
the computed backoff. Never retries any other 4xx -- it won't succeed the
second time either, and retrying only delays the real error reaching the
caller (rules/sdk-generation.md's "Client shape").

httpx's transport-level hooks (``httpx.BaseTransport``/``AsyncBaseTransport``)
apply this uniformly to every request the client makes, rather than
wrapping each generated call site in a retry loop by hand.
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

import httpx

_RETRYABLE_5XX_AND_429 = 500


@dataclass(frozen=True)
class RetryConfig:
    """Retry policy for :class:`RetryTransport`/:class:`AsyncRetryTransport`.

    Attributes:
        max_retries: Number of additional attempts after the first.
        base_seconds: Starting backoff before jitter and any server-sent
            ``Retry-After``.
    """

    max_retries: int = 3
    base_seconds: float = 0.25


DEFAULT_RETRY_CONFIG = RetryConfig()


def _should_retry(
    attempt: int,
    config: RetryConfig,
    response: httpx.Response | None,
    exc: Exception | None,
) -> bool:
    if attempt >= config.max_retries:
        return False
    if exc is not None:
        # A network-level failure (connection reset, timeout) is
        # retry-worthy the same as a 5xx.
        return True
    if response is None:
        # Every call site passes exactly one of response/exc -- not an
        # assert, so this invariant still holds under -O and doesn't trip
        # bandit's B101.
        raise ValueError("_should_retry needs a response or an exception")
    return response.status_code == httpx.codes.TOO_MANY_REQUESTS or response.status_code >= _RETRYABLE_5XX_AND_429


def _retry_after_seconds(response: httpx.Response) -> float | None:
    value = response.headers.get("retry-after")  # pragma: no mutate - httpx.Headers lookups are case-insensitive
    if not value:
        return None
    value = value.strip()
    try:
        return float(int(value))
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    return max((when - datetime.now(UTC)).total_seconds(), 0.0)


def _backoff_seconds(attempt: int, config: RetryConfig) -> float:
    backoff = config.base_seconds * (2.0**attempt)
    # Retry jitter, not security-sensitive -- a predictable PRNG is fine.
    jitter = random.uniform(0, backoff)  # noqa: S311 # nosec B311
    return backoff / 2 + jitter / 2


def _retry_delay(attempt: int, config: RetryConfig, response: httpx.Response | None) -> float:
    if response is not None:
        retry_after = _retry_after_seconds(response)
        if retry_after is not None:
            return retry_after
    return _backoff_seconds(attempt, config)


class RetryTransport(httpx.BaseTransport):
    """Wraps a sync ``httpx.BaseTransport`` with the retry policy above."""

    def __init__(
        self,
        *,
        transport: httpx.BaseTransport | None = None,
        retry: RetryConfig = DEFAULT_RETRY_CONFIG,
    ) -> None:
        self._transport = transport if transport is not None else httpx.HTTPTransport()
        self._retry = retry

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        # A bounded for-loop, not `while True` plus a hand-incremented
        # counter: `_should_retry` already returns False once `attempt`
        # reaches `max_retries`, so the last iteration always returns or
        # raises from inside the loop -- but driving termination off
        # `range()` too means a broken attempt counter can never turn this
        # into an infinite retry loop, only a wrong retry *count*.
        # The exact upper bound only has to be "enough" -- _should_retry's
        # own attempt >= max_retries check is what actually ends the loop
        # on the right iteration, so range()'s bound is unreachable as a
        # binding constraint whenever _should_retry itself is correct.
        for attempt in range(self._retry.max_retries + 1):  # pragma: no mutate
            try:
                response = self._transport.handle_request(request)
            except httpx.TransportError as exc:
                if not _should_retry(attempt, self._retry, None, exc):
                    raise
                time.sleep(_retry_delay(attempt, self._retry, None))
                continue

            if not _should_retry(attempt, self._retry, response, None):
                return response

            response.close()
            time.sleep(_retry_delay(attempt, self._retry, response))

        # Every loop iteration above returns or raises before falling
        # through, so this is unreachable -- kept only so mypy sees an
        # explicit return on every path.
        raise AssertionError("unreachable")  # pragma: no cover, no mutate

    def close(self) -> None:
        self._transport.close()


class AsyncRetryTransport(httpx.AsyncBaseTransport):
    """Wraps an async ``httpx.AsyncBaseTransport`` with the retry policy above."""

    def __init__(
        self,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        retry: RetryConfig = DEFAULT_RETRY_CONFIG,
    ) -> None:
        self._transport = transport if transport is not None else httpx.AsyncHTTPTransport()
        self._retry = retry

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        # See RetryTransport.handle_request's comments: bounded by
        # range(), not a hand-incremented counter under `while True`, and
        # the exact bound is unreachable as a binding constraint whenever
        # _should_retry itself is correct.
        for attempt in range(self._retry.max_retries + 1):  # pragma: no mutate
            try:
                response = await self._transport.handle_async_request(request)
            except httpx.TransportError as exc:
                if not _should_retry(attempt, self._retry, None, exc):
                    raise
                await asyncio.sleep(_retry_delay(attempt, self._retry, None))
                continue

            if not _should_retry(attempt, self._retry, response, None):
                return response

            await response.aclose()
            await asyncio.sleep(_retry_delay(attempt, self._retry, response))

        raise AssertionError("unreachable")  # pragma: no cover, no mutate

    async def aclose(self) -> None:
        await self._transport.aclose()
