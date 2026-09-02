"""The ONE Brave Search transport for the platform.

Every Brave call in every repo funnels through this module. It owns, in one
place: key selection, adaptive per-key rate limiting, the full Brave web-search
parameter surface, bounded retry with ``Retry-After`` support, and the typed
429 error that must never be mistaken for an empty result set.

**There is exactly one Brave client.** matrx-seo's rank adapter consumes this
engine and layers budget / rank-matching / credential resolution ABOVE it — it
does not open its own httpx connection. Two clients against one API is how the
429-as-empty-results defence ended up living in only half the codebase.
"""

import asyncio
import os
from collections.abc import Awaitable, Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Any, Literal, Protocol

import httpx
from matrx_utils import vcprint

from matrx_scraper.search.rate_limiter import (
    RateLimiter,
    brave_search_rate_limiter,
    interval_for_rate,
)

#: THE Brave key. Arman's ruling 2026-08-20 — the AI (PRO) key and nothing
#: else. BRAVE_SEARCH_API_KEY / BRAVE_SEARCH_API_KEY_AI / BRAVE_API_KEY are
#: retired and deliberately not read: they return a degraded search rather than
#: an error, so a fallback to them is invisible. See `BraveSearchClient.__init__`.
BRAVE_KEY_ENV_VAR = "BRAVE_SEARCH_API_KEY_PRO_AI"

BRAVE_API_ROOT = "https://api.search.brave.com/res/v1"
BRAVE_WEB_SEARCH_URL = f"{BRAVE_API_ROOT}/web/search"

#: The Brave endpoints this engine speaks, and the per-endpoint truths that
#: differ. `max_count` is Brave's own ceiling, VERIFIED live 2026-08-20 (each
#: endpoint returned exactly that many results) — clamping here means a caller
#: asking for 200 news articles gets Brave's real maximum instead of a 422.
#:
#: `params` is the parameter surface each endpoint actually accepts. Sending a
#: web-only parameter (result_filter / goggles / summary / units /
#: text_decorations) to the news or image endpoint is not a no-op we can rely
#: on, so each endpoint sends only its own.
#:
#: NOT here, deliberately: suggest, spellcheck and llm/context. All three
#: return 400 OPTION_NOT_IN_PLAN on our subscription (verified 2026-08-20), so
#: shipping a method for them would be a method that only ever fails.
_WEB_ONLY = frozenset(
    {"offset", "extra_snippets", "text_decorations", "result_filter", "units", "goggles", "summary"}
)
_COMMON = frozenset({"q", "count", "country", "search_lang", "ui_lang", "safesearch", "spellcheck"})

BRAVE_ENDPOINTS: dict[str, dict[str, Any]] = {
    "web": {
        "url": BRAVE_WEB_SEARCH_URL,
        "max_count": 20,
        "params": _COMMON | _WEB_ONLY | {"freshness"},
    },
    "news": {
        "url": f"{BRAVE_API_ROOT}/news/search",
        "max_count": 50,
        "params": _COMMON | {"freshness", "offset", "extra_snippets"},
    },
    "videos": {
        "url": f"{BRAVE_API_ROOT}/videos/search",
        "max_count": 50,
        "params": _COMMON | {"freshness", "offset"},
    },
    "images": {"url": f"{BRAVE_API_ROOT}/images/search", "max_count": 200, "params": _COMMON},
}

#: Local endpoints. `place_search` takes a free-text location or lat/lon; the
#: other two take the ids `place_search` returns. All three are PRO-plan only.
BRAVE_PLACE_SEARCH_URL = f"{BRAVE_API_ROOT}/local/place_search"
BRAVE_LOCAL_POIS_URL = f"{BRAVE_API_ROOT}/local/pois"
BRAVE_LOCAL_DESCRIPTIONS_URL = f"{BRAVE_API_ROOT}/local/descriptions"

#: The summarizer is a TWO-CALL contract and there is no way to shortcut it: a
#: web search with `summary=True` returns an opaque `summarizer.key`, and that
#: key — not the query — is what this endpoint takes.
BRAVE_SUMMARIZER_URL = f"{BRAVE_API_ROOT}/summarizer/search"

#: Statuses worth another attempt. A 429 is included, but exhausting the
#: attempts on one raises `BraveRateLimitError` rather than a generic HTTP
#: error, because the two demand different caller behaviour.
#: This module deliberately does NOT call ``load_dotenv()``. It used to, at
#: import time, which meant merely importing the Brave engine mutated the host
#: process's environment — a thing no library may do, and one that leaked into
#: every consumer the moment matrx-seo started importing it. Every real entry
#: point (aidream's asgi/config, the scraper server's config, every CLI) loads
#: its own ``.env`` before anything here reads ``os.getenv``.
RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})

#: The default is ONE attempt: the scraper's `async_brave_search` owns its own
#: throttle back-off loop above this client, and multiplying the two would turn
#: a throttled query into a minutes-long stall. Callers that own no outer loop
#: (the SEO rank adapter) pass a real `max_attempts`.
DEFAULT_MAX_ATTEMPTS = 1

DESKTOP_USER_AGENT = "BraveSearchClient/1.0"
MOBILE_USER_AGENT = "BraveSearchClient/1.0 (Mobile)"

_QUOTA_HEADERS = (
    "x-ratelimit-limit",
    "x-ratelimit-policy",
    "x-ratelimit-remaining",
    "x-ratelimit-reset",
)

#: Sentinel for "use my own per-key limiter". Distinct from an explicit
#: `rate_limiter=None`, which means "do not pace this call at all".
_USE_KEY_LIMITER: Any = object()


class BraveRateLimitError(Exception):
    """Brave returned HTTP 429 (throttled). This is a transient, retryable
    condition — NOT an empty result set. Callers MUST treat it as a failure to
    retry/back off, never as 'zero results found' (which is what silently
    returning None used to do, masking throttling as a genuine empty search)."""


class RateLimiterLike(Protocol):
    min_interval: float

    async def acquire(self) -> None: ...

    def update_min_interval(self, min_interval: float) -> None: ...


class NullRateLimiter:
    """Explicitly unpaced. Only for tests and for a caller that has proven it
    paces elsewhere — never a default in production wiring."""

    min_interval = 0.0

    async def acquire(self) -> None:
        return None

    def update_min_interval(self, min_interval: float) -> None:
        return None


class _HttpClient(Protocol):
    async def get(self, url: str, **kwargs: Any) -> httpx.Response: ...


@dataclass
class BraveSearchParams:
    """Brave's web-search parameter surface.

    Every optional field defaults to ``None`` and is OMITTED from the wire when
    unset, so a caller that passes nothing sends exactly what it sent before
    these parameters existed.
    """

    query: str
    #: Which Brave endpoint this request is for — see `BRAVE_ENDPOINTS`. It
    #: selects the URL, the `count` ceiling, and which parameters go on the wire.
    endpoint: Literal["web", "news", "videos", "images"] = "web"
    count: int = 20
    offset: int = 0
    country: str = "us"
    extra_snippets: bool = True
    safe_search: str = "off"
    freshness: str | None = None
    text_decorations: bool = False
    # Locale separation: `search_lang` selects the language of the CONTENT,
    # `ui_lang` the language of Brave's own UI strings in the payload. Both are
    # required for any non-US locale.
    search_lang: str | None = None
    ui_lang: str | None = None
    spellcheck: bool | None = None
    #: Comma-separated section list ("web", "news,videos", ...). Cuts payload
    #: and latency when a caller wants only one section.
    result_filter: str | None = None
    units: str | None = None
    goggles: str | None = None
    #: Asks for the summarizer key (AI plan). The answer itself is a second call.
    summary: bool | None = None
    device: Literal["desktop", "mobile"] = "desktop"

    def to_dict(self) -> dict[str, Any]:
        spec = BRAVE_ENDPOINTS[self.endpoint]
        allowed: frozenset[str] = spec["params"]
        params: dict[str, Any] = {
            "q": self.query,
            "count": min(self.count, spec["max_count"]),
            "offset": self.offset,
            "country": self.country,
            "extra_snippets": self.extra_snippets,
            "text_decorations": self.text_decorations,
            "safesearch": self.safe_search,
        }
        if self.freshness:
            params["freshness"] = self.freshness.lower()
        if self.search_lang is not None:
            params["search_lang"] = self.search_lang
        if self.ui_lang is not None:
            params["ui_lang"] = self.ui_lang
        if self.spellcheck is not None:
            params["spellcheck"] = self.spellcheck
        if self.result_filter is not None:
            params["result_filter"] = self.result_filter
        if self.units is not None:
            params["units"] = self.units
        if self.goggles is not None:
            params["goggles"] = self.goggles
        if self.summary is not None:
            params["summary"] = self.summary
        return {name: value for name, value in params.items() if name in allowed}

    @property
    def url(self) -> str:
        return BRAVE_ENDPOINTS[self.endpoint]["url"]

    @property
    def user_agent(self) -> str:
        return MOBILE_USER_AGENT if self.device == "mobile" else DESKTOP_USER_AGENT


@dataclass
class BraveSearchResponse:
    """One completed Brave request — the payload plus the evidence a billing /
    audit layer needs, so no consumer has to re-open the transport to get it."""

    payload: dict[str, Any]
    status_code: int
    attempts: int
    request_params: dict[str, Any]
    user_agent: str
    url: str = BRAVE_WEB_SEARCH_URL
    quota: dict[str, str] = field(default_factory=dict)


def _quota_from(response: httpx.Response) -> dict[str, str]:
    return {name: response.headers[name] for name in _QUOTA_HEADERS if name in response.headers}


def _retry_delay(value: str | None, *, fallback: float) -> float:
    """`Retry-After` is either delta-seconds or an HTTP date; both are legal."""
    if not value:
        return fallback
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(value)
        except (TypeError, ValueError, OverflowError):
            return fallback
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=UTC)
        return max(0.0, (retry_at - datetime.now(UTC)).total_seconds())


class BraveSearchClient:
    """The single, centralized Brave handler for this process.

    ONE key (`BRAVE_SEARCH_API_KEY_PRO_AI`) unless a caller brings its own, and
    one adaptive `RateLimiter` per key value, re-tuned from Brave's own
    `x-ratelimit-limit` response header — so a caller-supplied key that is
    slower than ours self-corrects on its first response with no code edit.

    """

    BASE_URL = BRAVE_WEB_SEARCH_URL

    def __init__(
        self,
        api_key: str | None = None,
        *,
        allow_missing_key: bool = False,
        client_factory: Callable[[], AbstractAsyncContextManager[_HttpClient]] | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        max_concurrency: int | None = None,
    ):
        """Build a client from an explicitly-supplied key, or from the environment.

        **ONE key.** Arman's ruling, 2026-08-20: the platform uses the Brave AI
        (PRO) key and nothing else. There is no fallback to a second env var and
        no per-request key selection, because the retired keys did not fail —
        they SUCCEEDED with less. Measured on the same query and parameters,
        the base and standard-AI keys returned no `faq`, `discussions`,
        `infobox`, `locations` or `summarizer` section, the base key returned
        zero `extra_snippets`, neither could reach `place_search` or the
        summarizer endpoint at all, and both paced at 1 req/sec against this
        key's 50. A fallback to either is a quieter, worse answer wearing a
        success costume — the same shape as the 429-as-empty-results bug this
        module was hardened against.

        `api_key` stays, and is the point rather than an exception: **a caller
        may always bring its own key.** The desktop client passes the user's own
        key from its in-app store, and every user-supplied-key path the platform
        grows uses this same argument. An explicit key is used exactly as given
        and is never second-guessed against the environment.

        `allow_missing_key=True` is for a consumer that resolves a key PER CALL
        from somewhere else (matrx-seo resolves an organization's own key from
        the secrets battery); the missing-key error then fires at call time,
        where it can name the request, instead of at construction.
        """
        self._api_key = api_key or os.getenv(BRAVE_KEY_ENV_VAR)

        if not self._api_key and not allow_missing_key:
            raise ValueError(
                f"No Brave API key: pass api_key= or set {BRAVE_KEY_ENV_VAR}. "
                "BRAVE_SEARCH_API_KEY, BRAVE_SEARCH_API_KEY_AI and BRAVE_API_KEY "
                "are RETIRED and are deliberately not read — they return a "
                "degraded search, not an error."
            )

        self._client_factory = client_factory or self._default_client_factory
        self._sleep = sleep
        self._semaphore = asyncio.Semaphore(max_concurrency) if max_concurrency else None

        # One limiter per key value. The configured key reuses the shared module
        # singleton so every client in the process paces against one queue; a
        # per-call key (a user's own) gets its own limiter on first use. Seeded
        # at the PRO floor and re-tuned from `x-ratelimit-limit` on the first
        # response, so a caller's slower key self-corrects without a code edit.
        self._limiters: dict[str, RateLimiterLike] = {}
        if self._api_key:
            self._limiters[self._api_key] = brave_search_rate_limiter

    @staticmethod
    def _default_client_factory() -> AbstractAsyncContextManager[_HttpClient]:
        return httpx.AsyncClient()

    def _limiter_for(self, api_key: str) -> RateLimiterLike:
        limiter = self._limiters.get(api_key)
        if limiter is None:
            # A key we have not seen before (a caller's own). Seed at the PRO
            # floor and let `_tune_limiter` correct it from the very first
            # `x-ratelimit-limit` header if that key is slower.
            limiter = RateLimiter(min_interval=interval_for_rate(50))
            self._limiters[api_key] = limiter
        return limiter

    @staticmethod
    def _tune_limiter(limiter: RateLimiterLike, response: httpx.Response) -> None:
        # Brave advertises the live ceiling as `x-ratelimit-limit: "<sec>, <month>"`.
        # Re-pace this key's limiter to match. Present on 200s AND 429s, so a
        # throttled key still keeps a correct interval.
        raw = response.headers.get("x-ratelimit-limit")
        if not raw:
            return
        try:
            per_second = float(raw.split(",")[0].strip())
        except (ValueError, IndexError):
            return
        new_interval = interval_for_rate(per_second)
        if abs(new_interval - limiter.min_interval) > 1e-6:
            vcprint(
                f"[brave_search] Re-tuned pacing to {new_interval:.2f}s/req "
                f"(key advertises {per_second:g} req/sec)",
                color="blue",
            )
            limiter.update_min_interval(new_interval)

    async def search_response(
        self,
        params: BraveSearchParams,
        *,
        api_key: str | None = None,
        rate_limiter: RateLimiterLike | None = _USE_KEY_LIMITER,
        timeout: float = 10,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        base_backoff_seconds: float = 0.25,
        max_retry_delay_seconds: float = 40.0,
        client: _HttpClient | None = None,
    ) -> BraveSearchResponse:
        """Run ONE logical Brave request, with pacing, adaptive re-tuning and a
        bounded retry, and return the payload plus its billing evidence.

        `api_key` overrides key selection for this call — that is how a consumer
        holding a per-organization key (matrx-seo) rides this engine's pacing
        and throttle handling instead of re-implementing them.
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        key = api_key or self._api_key
        if not key:
            raise ValueError(
                f"No Brave API key for this request: pass api_key=, or set {BRAVE_KEY_ENV_VAR}"
            )
        limiter = self._limiter_for(key) if rate_limiter is _USE_KEY_LIMITER else rate_limiter
        url = params.url
        wire_params = params.to_dict()
        headers = {
            "X-Subscription-Token": key,
            "Accept": "application/json",
            "User-Agent": params.user_agent,
        }

        if client is not None:
            return await self._attempt_loop(
                client,
                url,
                wire_params,
                headers,
                params,
                limiter,
                timeout,
                max_attempts,
                base_backoff_seconds,
                max_retry_delay_seconds,
            )
        async with self._client_factory() as owned_client:
            return await self._attempt_loop(
                owned_client,
                url,
                wire_params,
                headers,
                params,
                limiter,
                timeout,
                max_attempts,
                base_backoff_seconds,
                max_retry_delay_seconds,
            )

    async def _attempt_loop(
        self,
        client: _HttpClient,
        url: str,
        wire_params: dict[str, Any],
        headers: dict[str, str],
        params: BraveSearchParams,
        limiter: RateLimiterLike | None,
        timeout: float,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
        max_attempts: int,
        base_backoff_seconds: float,
        max_retry_delay_seconds: float,
    ) -> BraveSearchResponse:
        for attempt in range(1, max_attempts + 1):
            try:
                async with self._concurrency():
                    if limiter is not None:
                        await limiter.acquire()
                    response = await client.get(
                        url,
                        headers=headers,
                        params=wire_params,
                        timeout=timeout,
                    )
            except httpx.TimeoutException as exc:
                if attempt == max_attempts:
                    raise Exception(f"Request timed out after {timeout} seconds") from exc
                await self._sleep(base_backoff_seconds * (2 ** (attempt - 1)))
                continue
            except httpx.TransportError as exc:
                if attempt == max_attempts:
                    raise Exception(f"HTTP error occurred: {exc}") from exc
                await self._sleep(base_backoff_seconds * (2 ** (attempt - 1)))
                continue

            if limiter is not None:
                self._tune_limiter(limiter, response)

            if response.status_code not in RETRYABLE_STATUSES:
                self._raise_for_status(response, params)
                return BraveSearchResponse(
                    payload=response.json(),
                    status_code=response.status_code,
                    attempts=attempt,
                    request_params=wire_params,
                    user_agent=headers["User-Agent"],
                    url=url,
                    quota=_quota_from(response),
                )
            if attempt == max_attempts:
                self._raise_for_status(response, params)
                # A retryable status that is not an error status (Brave has none
                # today) still owes the caller a payload rather than a silent None.
                return BraveSearchResponse(
                    payload=response.json(),
                    status_code=response.status_code,
                    attempts=attempt,
                    request_params=wire_params,
                    user_agent=headers["User-Agent"],
                    url=url,
                    quota=_quota_from(response),
                )
            await self._sleep(
                min(
                    _retry_delay(
                        response.headers.get("retry-after"),
                        fallback=base_backoff_seconds * (2 ** (attempt - 1)),
                    ),
                    max_retry_delay_seconds,
                )
            )
        raise RuntimeError("unreachable Brave retry state")

    def _concurrency(self) -> AbstractAsyncContextManager[Any]:
        if self._semaphore is not None:
            return self._semaphore
        return _NULL_CONCURRENCY

    def _raise_for_status(self, response: httpx.Response, params: BraveSearchParams) -> None:
        if response.status_code == 429:
            raise BraveRateLimitError(f"Brave rate limit (429) for query: {params.query[:80]!r}")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise
        except httpx.HTTPError as exc:
            raise Exception(f"HTTP error occurred: {exc}") from exc

    async def search(
        self,
        query: str,
        count: int = 20,
        offset: int = 0,
        country: str = "us",
        extra_snippets: bool = True,
        safe_search: str = "off",
        freshness: str | None = None,
        timeout: int = 10,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
        *,
        search_lang: str | None = None,
        ui_lang: str | None = None,
        spellcheck: bool | None = None,
        result_filter: str | None = None,
        units: str | None = None,
        goggles: str | None = None,
        summary: bool | None = None,
        device: Literal["desktop", "mobile"] = "desktop",
        api_key: str | None = None,
    ) -> dict[str, Any] | None:
        """Payload-only convenience over `search_response`. Raises
        `BraveRateLimitError` on a 429 — never returns an empty result set."""
        response = await self.search_response(
            BraveSearchParams(
                query=query,
                count=count,
                offset=offset,
                country=country,
                extra_snippets=extra_snippets,
                safe_search=safe_search,
                freshness=freshness,
                search_lang=search_lang,
                ui_lang=ui_lang,
                spellcheck=spellcheck,
                result_filter=result_filter,
                units=units,
                goggles=goggles,
                summary=summary,
                device=device,
            ),
            api_key=api_key,
            timeout=timeout,
        )
        return response.payload

    async def search_news(
        self, query: str, *, count: int = 20, **kwargs: Any
    ) -> dict[str, Any] | None:
        """Brave's dedicated NEWS index — not the `news` side-section of a web
        search. Deeper (count up to 50 vs the web endpoint's 20) and it accepts
        the same freshness windows, including a custom `YYYY-MM-DDtoYYYY-MM-DD`
        range."""
        return await self._endpoint_payload("news", query, count=count, **kwargs)

    async def search_videos(
        self, query: str, *, count: int = 20, **kwargs: Any
    ) -> dict[str, Any] | None:
        """Brave's dedicated VIDEO index (count up to 50)."""
        return await self._endpoint_payload("videos", query, count=count, **kwargs)

    async def search_images(
        self, query: str, *, count: int = 50, **kwargs: Any
    ) -> dict[str, Any] | None:
        """Brave's dedicated IMAGE index (count up to 200 — by far the deepest
        of the four). Each result carries `properties.url` (the ORIGINAL image),
        a proxied 500px `thumbnail`, and dimensions when Brave knows them."""
        return await self._endpoint_payload("images", query, count=count, **kwargs)

    async def _endpoint_payload(
        self,
        endpoint: Literal["web", "news", "videos", "images"],
        query: str,
        *,
        timeout: float = 10,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
        api_key: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        response = await self.search_response(
            BraveSearchParams(query=query, endpoint=endpoint, **kwargs),
            api_key=api_key,
            timeout=timeout,
        )
        return response.payload

    async def search_places(
        self,
        query: str,
        *,
        location: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        count: int = 20,
        country: str = "US",
        timeout: float = 10,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
        api_key: str | None = None,
    ) -> dict[str, Any] | None:
        """Brave Place Search — ~200M points of interest.

        Takes EITHER a free-text `location` ("austin texas") or a lat/lon pair.
        With neither, Brave runs its "explore" mode around whatever the query
        implies. Results carry postal address, coordinates, rating, price range,
        categories, cuisine, opening hours, contact, profiles and pictures, and
        the response additionally breaks the area down into `addresses`,
        `streets`, `neighborhoods`, `cities`, `regions` and `countries`.

        PRO-plan only: a non-PRO key gets 400 OPTION_NOT_IN_PLAN.
        """
        # `country` on THIS endpoint is a strict uppercase enum ("US"), unlike
        # web search, which accepts "us". Passing the web endpoint's lowercase
        # default here is a 422 with no useful message, so normalize it.
        params: dict[str, Any] = {"q": query, "count": count, "country": country.upper()}
        if location is not None:
            params["location"] = location
        if latitude is not None and longitude is not None:
            params["latitude"] = latitude
            params["longitude"] = longitude
        return await self._raw_get(
            BRAVE_PLACE_SEARCH_URL, params, query=query, timeout=timeout, api_key=api_key
        )

    async def fetch_summary(
        self,
        summarizer_key: str,
        *,
        entity_info: bool = True,
        timeout: float = 20,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
        api_key: str | None = None,
    ) -> dict[str, Any] | None:
        """Second half of the summarizer contract: exchange the opaque
        `summarizer.key` from a `summary=True` web search for Brave's cited AI
        answer.

        There is no one-call form — the key, not the query, is the input, and it
        encodes the exact result set the answer is grounded in. Pass the key
        through verbatim; it is opaque JSON and must not be reconstructed.

        PRO-plan only. `timeout` defaults higher than a search because the
        answer is generated, not looked up.
        """
        return await self._raw_get(
            BRAVE_SUMMARIZER_URL,
            {"key": summarizer_key, "entity_info": entity_info},
            query=summarizer_key[:80],
            timeout=timeout,
            api_key=api_key,
        )

    async def _raw_get(
        self,
        url: str,
        wire_params: dict[str, Any],
        *,
        query: str,
        timeout: float,  # noqa: ASYNC109 - httpx per-request timeout, not a cancellation scope
        api_key: str | None,
    ) -> dict[str, Any] | None:
        """Shared path for the endpoints whose parameter surface is genuinely
        not `BraveSearchParams` (local, summarizer). Still rides this engine's
        key selection, pacing, adaptive re-tuning and 429 contract — nothing
        opens its own transport."""
        key = api_key or self._api_key
        if not key:
            raise ValueError(
                f"No Brave API key for this request: pass api_key=, or set {BRAVE_KEY_ENV_VAR}"
            )
        limiter = self._limiter_for(key)
        headers = {
            "X-Subscription-Token": key,
            "Accept": "application/json",
            "User-Agent": DESKTOP_USER_AGENT,
        }
        probe = BraveSearchParams(query=query)
        async with self._client_factory() as client:
            async with self._concurrency():
                await limiter.acquire()
                response = await client.get(
                    url, headers=headers, params=wire_params, timeout=timeout
                )
            self._tune_limiter(limiter, response)
            self._raise_for_status(response, probe)
            return response.json()


class _NullConcurrency:
    async def __aenter__(self) -> None:
        return None

    async def __aexit__(self, *_args: Any) -> None:
        return None


_NULL_CONCURRENCY = _NullConcurrency()


_client: BraveSearchClient | None = None


def configure_client(api_key: str | None) -> BraveSearchClient | None:
    """Install the process-wide client from host-held keys, or clear it.

    A host whose Brave key lives outside the environment (a desktop key store,
    a settings row, a per-user secret) calls this whenever the key changes, so
    the very next `async_brave_search` uses it — no restart, no env var. This is
    THE user-supplied-key path: the key given here is used exactly as given.

    Passing a falsy `api_key` clears the client, which is how "the user removed
    their key" is expressed; the next search then raises the normal missing-key
    error instead of silently using a stale one.

    The retired `ai_api_key` / `ai_key_is_pro` arguments are gone — there is one
    key now. Callers passing one positional argument are unaffected.
    """
    global _client
    if not api_key:
        _client = None
        return None
    _client = BraveSearchClient(api_key=api_key)
    return _client


def get_client() -> BraveSearchClient:
    global _client
    if _client is None:
        _client = BraveSearchClient()
    return _client
