"""The ONE SerpAPI transport for the platform.

Every SerpAPI call — any engine — goes through :class:`SerpApiClient`. It owns
retry with ``Retry-After``, pacing, concurrency, quota-header capture, the
body-carried error reason, and the per-call cost evidence a budget ledger reads.

**Why one engine matters here more than anywhere else.** Every SerpAPI engine
draws on ONE monthly search allowance. A second client is not a style problem:
it is an untracked hole in a hard, small budget. The client this replaced
(``api_management/serpi_api/search_google.py``) read the key at module scope,
had no retry, captured no quota header, and reported no cost — so every generic
Google or Google-Images search it ran spent the same allowance that rank
tracking depends on, invisibly.

The SEO rank layer (``serpapi.py``) sits ABOVE this client and adds settings
validation, credential resolution, rank matching and observation normalization.
It does not open its own connection.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from email.utils import parsedate_to_datetime
from time import monotonic
from typing import Any, Protocol

import httpx
from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field

SERPAPI_SEARCH_ENDPOINT = "https://serpapi.com/search.json"

RETRYABLE_HTTP_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})


class SerpApiError(RuntimeError):
    pass


class SerpApiRetryExhausted(SerpApiError):
    pass


class SerpApiHttpResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status_code: int
    payload: dict[str, Any]
    headers: dict[str, str] = Field(default_factory=dict)


class SerpApiHttpTransport(Protocol):
    async def get_json(self, url: str, params: Mapping[str, str | int]) -> SerpApiHttpResponse: ...


class HttpxSerpApiTransport:
    def __init__(self, timeout: httpx.Timeout | None = None) -> None:
        self.timeout = timeout or httpx.Timeout(connect=10, read=45, write=10, pool=10)

    async def get_json(self, url: str, params: Mapping[str, str | int]) -> SerpApiHttpResponse:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params)
        try:
            payload = response.json()
        except ValueError as exc:
            raise SerpApiError(f"SerpAPI returned non-JSON HTTP {response.status_code}") from exc
        if not isinstance(payload, dict):
            raise SerpApiError("SerpAPI response must be a JSON object")
        return SerpApiHttpResponse(
            status_code=response.status_code,
            payload=payload,
            headers=dict(response.headers),
        )


@dataclass
class SerpApiCall:
    """One completed SerpAPI search — the payload plus every piece of billing
    and audit evidence, so no consumer has to re-open the transport for it."""

    engine: str
    payload: dict[str, Any]
    status_code: int
    attempts: int
    request_parameters: dict[str, Any]
    search_metadata: dict[str, Any]
    search_id: str | None
    fetched_at: datetime
    estimated_cost: Decimal | None = None
    quota_headers: dict[str, str] = field(default_factory=dict)
    endpoint: str = SERPAPI_SEARCH_ENDPOINT

    @property
    def request_evidence(self) -> dict[str, Any]:
        return {
            "method": "GET",
            "url": self.endpoint,
            # api_key travels in the query string, not a header — it is redacted
            # in place by the client so evidence never carries a live credential.
            "headers": {},
            "params": self.request_parameters,
        }


#: Observers see EVERY SerpAPI call this process makes, rank or generic. The
#: allowance is monthly and small; a host wires an observer so a search can
#: never again be spent without a durable record of it. Observers must never
#: raise — a bookkeeping failure may not kill a search that already cost money.
CallObserver = Callable[[SerpApiCall], None]
_observers: list[CallObserver] = []


def register_serpapi_call_observer(observer: CallObserver) -> None:
    if observer not in _observers:
        _observers.append(observer)


def clear_serpapi_call_observers() -> None:
    _observers.clear()


def _notify(call: SerpApiCall) -> None:
    for observer in list(_observers):
        try:
            observer(call)
        except Exception as exc:  # noqa: BLE001 - never lose a paid search to bookkeeping
            vcprint(
                f"[serpapi] call observer {observer!r} raised {type(exc).__name__}: {exc}",
                color="red",
            )


class SerpApiClient:
    """One paced, retrying, quota-aware SerpAPI transport."""

    def __init__(
        self,
        *,
        transport: SerpApiHttpTransport | None = None,
        endpoint: str = SERPAPI_SEARCH_ENDPOINT,
        max_concurrency: int = 4,
        min_interval_seconds: float = 0,
        max_attempts: int = 4,
        base_backoff_seconds: float = 0.5,
        max_retry_delay_seconds: float = 30,
        estimated_cost_per_search: Decimal | str | int | float | None = None,
    ) -> None:
        if max_concurrency < 1 or max_attempts < 1:
            raise ValueError("max_concurrency and max_attempts must be positive")
        if min_interval_seconds < 0 or base_backoff_seconds < 0:
            raise ValueError("rate interval and retry backoff cannot be negative")
        if max_retry_delay_seconds < 0:
            raise ValueError("max_retry_delay_seconds cannot be negative")
        self.estimated_cost_per_search = _normalize_cost(estimated_cost_per_search)
        self.transport = transport or HttpxSerpApiTransport()
        self.endpoint = endpoint
        self.max_attempts = max_attempts
        self.base_backoff_seconds = base_backoff_seconds
        self.max_retry_delay_seconds = max_retry_delay_seconds
        self.min_interval_seconds = min_interval_seconds
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._pace_lock = asyncio.Lock()
        self._last_request_at = 0.0

    async def search(
        self,
        params: Mapping[str, str | int],
        *,
        api_key: str,
        require_search_id: bool = True,
    ) -> SerpApiCall:
        """Run ONE SerpAPI search and return its payload plus billing evidence.

        `require_search_id` is on by default because a successful SerpAPI
        response always carries ``search_metadata.id`` and its absence means the
        payload is not what it claims to be. A caller that legitimately accepts
        a partial payload turns it off explicitly rather than parsing around it.
        """
        if not api_key:
            raise ValueError("SerpAPI searches require an api_key")
        engine = str(params.get("engine") or "unknown")
        response, attempts = await self._request_with_retry({**params, "api_key": api_key})
        payload = response.payload
        metadata = _mapping(payload.get("search_metadata"))
        error = payload.get("error")
        status = str(metadata.get("status", ""))
        if error or status.lower() == "error":
            raise SerpApiError(str(error or "SerpAPI search ended with Error status"))
        search_id = _optional_string(metadata.get("id"))
        if require_search_id and not search_id:
            raise SerpApiError("successful SerpAPI response omitted search_metadata.id")
        call = SerpApiCall(
            engine=engine,
            payload=payload,
            status_code=response.status_code,
            attempts=attempts,
            # The key is redacted IN the evidence, never merely omitted, so a
            # reader can see that a key was sent without ever seeing its value.
            request_parameters={**params, "api_key": "***"},
            search_metadata=metadata,
            search_id=search_id,
            fetched_at=provider_timestamp(metadata) or datetime.now(UTC),
            estimated_cost=self.estimated_cost_per_search,
            quota_headers=quota_headers(response.headers),
            endpoint=self.endpoint,
        )
        _notify(call)
        return call

    async def _request_with_retry(
        self, params: Mapping[str, str | int]
    ) -> tuple[SerpApiHttpResponse, int]:
        last_status: int | None = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                async with self._semaphore:
                    await self._pace()
                    response = await self.transport.get_json(self.endpoint, params)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                if attempt == self.max_attempts:
                    raise SerpApiRetryExhausted(
                        f"SerpAPI network retries exhausted: {type(exc).__name__}"
                    ) from exc
                await asyncio.sleep(self.base_backoff_seconds * (2 ** (attempt - 1)))
                continue
            last_status = response.status_code
            if response.status_code not in RETRYABLE_HTTP_STATUSES:
                if response.status_code >= 400:
                    # SerpAPI puts the REASON in the body ("Unsupported
                    # `location` parameter"). Dropping it turns a permanently
                    # dead target into an unexplained "HTTP 400" forever.
                    reason = _optional_string(response.payload.get("error"))
                    raise SerpApiError(
                        f"SerpAPI returned HTTP {response.status_code}"
                        + (f": {reason}" if reason else "")
                    )
                return response, attempt
            if attempt < self.max_attempts:
                await asyncio.sleep(
                    min(
                        self.max_retry_delay_seconds,
                        retry_delay(
                            response.headers.get("retry-after"),
                            fallback=self.base_backoff_seconds * (2 ** (attempt - 1)),
                        ),
                    )
                )
        raise SerpApiRetryExhausted(f"SerpAPI HTTP retries exhausted after status {last_status}")

    async def _pace(self) -> None:
        if self.min_interval_seconds <= 0:
            return
        async with self._pace_lock:
            remaining = self.min_interval_seconds - (monotonic() - self._last_request_at)
            if remaining > 0:
                await asyncio.sleep(remaining)
            self._last_request_at = monotonic()


def _normalize_cost(value: Decimal | str | int | float | None) -> Decimal | None:
    if value is None:
        return None
    try:
        normalized = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("estimated_cost_per_search must be a decimal-compatible value") from exc
    if not normalized.is_finite() or normalized < 0:
        raise ValueError("estimated_cost_per_search must be finite and nonnegative")
    return normalized


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def provider_timestamp(metadata: Mapping[str, Any]) -> datetime | None:
    for key in ("processed_at", "created_at"):
        value = _optional_string(metadata.get(key))
        if not value:
            continue
        normalized = value.replace(" UTC", "+00:00")
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError:
            continue
        return parsed.replace(tzinfo=parsed.tzinfo or UTC).astimezone(UTC)
    return None


def retry_delay(value: str | None, *, fallback: float) -> float:
    if not value:
        return fallback
    try:
        return max(0, float(value))
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(value)
        except (TypeError, ValueError, OverflowError):
            return fallback
        now = datetime.now(retry_at.tzinfo or UTC)
        return max(0, (retry_at - now).total_seconds())


def quota_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        key.lower(): value
        for key, value in headers.items()
        if key.lower().startswith(("x-ratelimit-", "x-serpapi-"))
    }


__all__ = [
    "RETRYABLE_HTTP_STATUSES",
    "SERPAPI_SEARCH_ENDPOINT",
    "HttpxSerpApiTransport",
    "SerpApiCall",
    "SerpApiClient",
    "SerpApiError",
    "SerpApiHttpResponse",
    "SerpApiHttpTransport",
    "SerpApiRetryExhausted",
    "clear_serpapi_call_observers",
    "provider_timestamp",
    "quota_headers",
    "register_serpapi_call_observer",
    "retry_delay",
]
