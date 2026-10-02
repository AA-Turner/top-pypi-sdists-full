from __future__ import annotations

import asyncio
import random
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any, Protocol

import httpx

# ---------------------------------------------------------------------------
# BILLABLE-CALL OBSERVERS — the ONE seam a host uses to put DataForSEO money on
# a ledger.
#
# DataForSEO reports its OWN price: every response envelope carries a top-level
# `cost` (USD) for that request. That is a real invoice line, not an estimate,
# and it is what the host records — no knob needed except as a fallback for a
# response that somehow carries none.
#
# This package owns no ledger and never will (it must install and run alone),
# so the host registers an observer. aidream wires `record_external_api_cost`
# here at startup. Observers MUST never raise: a bookkeeping failure may not
# kill a task that already cost money.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DataForSeoBillableCall:
    """One DataForSEO request and what it cost. `path` is the API path
    (`/v3/serp/google/organic/live/advanced`), `cost_usd` the price DataForSEO
    reported in the envelope (None when it reported none)."""

    method: str
    path: str
    status_code: int
    cost_usd: float | None
    tasks: int


DataForSeoCallObserver = Callable[[DataForSeoBillableCall], None]
_call_observers: list[DataForSeoCallObserver] = []


def register_dataforseo_call_observer(observer: DataForSeoCallObserver) -> None:
    """Install a host observer. Idempotent — a callable registered twice would
    double-bill every task."""
    if observer not in _call_observers:
        _call_observers.append(observer)


def clear_dataforseo_call_observers() -> None:
    _call_observers.clear()


def _notify_billable(call: DataForSeoBillableCall) -> None:
    for observer in list(_call_observers):
        try:
            observer(call)
        except Exception as exc:  # noqa: BLE001 - never lose a paid task to bookkeeping
            from matrx_utils import vcprint

            vcprint(
                f"[dataforseo] call observer {observer!r} raised "
                f"{type(exc).__name__}: {exc}",
                color="red",
            )


def _envelope_cost(payload: dict[str, Any]) -> float | None:
    """The USD DataForSEO says this request cost. `0.0` is a REAL answer (a
    free endpoint: tasks_ready, a cached task_get) and is returned as 0.0, never
    conflated with "unknown" — the host must be able to tell a free call from an
    unpriced one."""
    raw = payload.get("cost")
    if raw is None or isinstance(raw, bool):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


class DataForSeoTransportError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        attempts: int = 1,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
        response_body: str | None = None,
    ) -> None:
        self.attempts = attempts
        self.status_code = status_code
        self.headers = headers or {}
        self.response_body = response_body
        super().__init__(message)


class DataForSeoHttpError(DataForSeoTransportError):
    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        attempts: int,
        headers: dict[str, str],
    ) -> None:
        super().__init__(
            f"DataForSEO HTTP {status_code}: {message}",
            attempts=attempts,
            status_code=status_code,
            headers=headers,
            response_body=message,
        )


@dataclass(frozen=True)
class JsonResponse:
    payload: dict[str, Any]
    headers: dict[str, str]
    status_code: int = 200
    request: dict[str, Any] | None = None


class DataForSeoTransport(Protocol):
    async def request(
        self,
        method: str,
        path: str,
        *,
        json_body: list[dict[str, Any]] | dict[str, Any] | None = None,
    ) -> JsonResponse: ...


class AdaptiveRateLimiter:
    def __init__(self, *, calls_per_minute: int = 2_000, concurrency: int = 30) -> None:
        if calls_per_minute < 1:
            raise ValueError("calls_per_minute must be positive")
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        self._interval = 60.0 / calls_per_minute
        self._next_at = 0.0
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(concurrency)

    async def __aenter__(self) -> AdaptiveRateLimiter:
        await self._semaphore.acquire()
        async with self._lock:
            now = time.monotonic()
            delay = max(0.0, self._next_at - now)
            self._next_at = max(now, self._next_at) + self._interval
        if delay:
            await asyncio.sleep(delay)
        return self

    async def __aexit__(self, *_: object) -> None:
        self._semaphore.release()

    async def observe(self, headers: dict[str, str]) -> None:
        limit = headers.get("x-ratelimit-limit") or headers.get("X-RateLimit-Limit")
        if limit and limit.isdigit() and int(limit) > 0:
            async with self._lock:
                self._interval = 60.0 / int(limit)


class AsyncHttpTransport:
    RETRYABLE_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})

    def __init__(
        self,
        *,
        username: str,
        password: str,
        base_url: str = "https://api.dataforseo.com",
        timeout: httpx.Timeout | None = None,
        max_attempts: int = 4,
        rate_limiter: AdaptiveRateLimiter | None = None,
        sleeper: Callable[[float], Awaitable[None]] = asyncio.sleep,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        self.max_attempts = max_attempts
        self._sleeper = sleeper
        self._limiter = rate_limiter or AdaptiveRateLimiter()
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url,
            auth=httpx.BasicAuth(username, password),
            timeout=timeout or httpx.Timeout(connect=10.0, read=90.0, write=30.0, pool=10.0),
            headers={"Accept": "application/json", "User-Agent": "matrx-seo/0.1"},
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_body: list[dict[str, Any]] | dict[str, Any] | None = None,
    ) -> JsonResponse:
        last_error: Exception | None = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                async with self._limiter:
                    response = await self._client.request(method, path, json=json_body)
                headers = dict(response.headers)
                await self._limiter.observe(headers)
                if response.status_code in self.RETRYABLE_STATUS and attempt < self.max_attempts:
                    await self._retry_delay(attempt, headers)
                    continue
                if response.is_error:
                    raise DataForSeoHttpError(
                        response.status_code,
                        response.text[:500],
                        attempts=attempt,
                        headers=headers,
                    )
                payload = response.json()
                if not isinstance(payload, dict):
                    raise DataForSeoTransportError("DataForSEO returned a non-object JSON envelope")
                # DataForSEO served this request and priced it in the envelope.
                # An errored/retried attempt never reaches here, which is right:
                # the account is charged for the served call, not the refused one.
                _notify_billable(
                    DataForSeoBillableCall(
                        method=str(method).upper(),
                        path=str(path),
                        status_code=response.status_code,
                        cost_usd=_envelope_cost(payload),
                        tasks=int(payload.get("tasks_count") or 0),
                    )
                )
                return JsonResponse(
                    payload=payload,
                    headers=headers,
                    status_code=response.status_code,
                    request={
                        "method": response.request.method,
                        "url": str(response.request.url),
                        "headers": {
                            key: "<redacted>" if key.lower() == "authorization" else value
                            for key, value in response.request.headers.items()
                        },
                        "json": json_body,
                    },
                )
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                last_error = exc
                if attempt == self.max_attempts:
                    break
                await self._retry_delay(attempt, {})
        raise DataForSeoTransportError(
            "DataForSEO request retries exhausted",
            attempts=self.max_attempts,
        ) from last_error

    async def _retry_delay(self, attempt: int, headers: dict[str, str]) -> None:
        retry_after = headers.get("retry-after") or headers.get("Retry-After")
        if retry_after:
            try:
                delay = min(float(retry_after), 60.0)
            except ValueError:
                try:
                    retry_at = parsedate_to_datetime(retry_after)
                    now = datetime.now(retry_at.tzinfo)
                    delay = min(max((retry_at - now).total_seconds(), 0.25), 60.0)
                except (TypeError, ValueError, OverflowError):
                    delay = min(0.5 * (2 ** (attempt - 1)), 8.0)
        else:
            delay = min(0.5 * (2 ** (attempt - 1)) + random.uniform(0, 0.25), 8.0)
        await self._sleeper(delay)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()


class ReplayTransport:
    def __init__(self, responses: list[dict[str, Any] | JsonResponse]) -> None:
        self._responses = list(responses)
        self.requests: list[tuple[str, str, object]] = []

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_body: list[dict[str, Any]] | dict[str, Any] | None = None,
    ) -> JsonResponse:
        self.requests.append((method, path, json_body))
        if not self._responses:
            raise AssertionError(f"unexpected DataForSEO request {method} {path}")
        response = self._responses.pop(0)
        if isinstance(response, JsonResponse):
            return response
        return JsonResponse(
            response,
            {},
            request={
                "method": method,
                "url": path,
                "headers": {},
                "json": json_body,
            },
        )
