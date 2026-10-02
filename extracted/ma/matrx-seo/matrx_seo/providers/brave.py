from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from contextlib import AbstractAsyncContextManager
from contextvars import ContextVar
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal

from matrx_scraper.search import (
    BraveSearchClient,
    BraveSearchParams,
    BraveSearchResponse,
    NullRateLimiter,
    RateLimiter,
    RateLimiterLike,
    interval_for_rate,
)
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..adapters import ProviderExecutionContext, SeoProviderAdapter, SeoProviderOperation
from ..contracts import (
    CollectionRequest,
    HostBindingRequest,
    NormalizationContext,
    ProviderCallRecord,
    ProviderResponse,
    RankObservation,
    ResolvedCredential,
    SeoCapability,
    SeoIdentityRequest,
    SeoObservation,
    SerpResultObservation,
    SerpSnapshotObservation,
)
from ..identity import stable_hash
from ..rank_matching import RankMatchTarget, canonicalize_domain, match_rank_url

BRAVE_SEARCH_COST_PER_REQUEST = Decimal("0.005")

# Conservative default for an untuned key (1 req/sec plan) until the first
# response's x-ratelimit-limit header re-tunes the interval. Pacing policy —
# the FLOOR, the safety margin, and the header-driven re-tuning — lives ONCE,
# in matrx_scraper's canonical Brave engine; this package consumes it.
BRAVE_DEFAULT_MIN_INTERVAL_SECONDS = interval_for_rate(1)


class BraveSeoRankSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=400)
    host_site_id: str | None = None
    host_page_id: str | None = None
    target_domain: str | None = None
    target_url: str | None = None
    target_url_aliases: tuple[str, ...] = ()
    include_subdomains: bool = True
    country: str = "US"
    search_lang: str = "en"
    ui_lang: str = "en-US"
    safesearch: Literal["off", "moderate", "strict"] = "moderate"
    count: int = Field(default=20, ge=1, le=20)
    offset: int = Field(default=0, ge=0, le=9)
    max_pages: int = Field(default=1, ge=1, le=10)
    device: Literal["desktop", "mobile"] = "desktop"

    @field_validator("country")
    @classmethod
    def normalize_country(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 2 and normalized != "ALL":
            raise ValueError("country must be a two-letter code or ALL")
        return normalized

    @field_validator("search_lang")
    @classmethod
    def normalize_search_language(cls, value: str) -> str:
        normalized = value.strip().lower()
        if len(normalized) < 2:
            raise ValueError("search_lang must contain at least two characters")
        return normalized

    @field_validator("ui_lang")
    @classmethod
    def normalize_ui_language(cls, value: str) -> str:
        normalized = value.strip()
        if "-" not in normalized:
            raise ValueError("ui_lang must use language-country form")
        language, country = normalized.split("-", 1)
        return f"{language.lower()}-{country.upper()}"

    @model_validator(mode="after")
    def validate_page_window(self) -> BraveSeoRankSettings:
        if self.offset + self.max_pages > 10:
            raise ValueError("offset + max_pages cannot exceed Brave's 10-page window")
        if not (self.target_domain or self.host_site_id or self.host_page_id):
            raise ValueError("Brave rank collection requires a target or host binding")
        return self

    def engine_params(self, page_offset: int) -> BraveSearchParams:
        """This request as the canonical engine's parameter object.

        Rank collection asks for exactly the web section, no spellcheck and no
        extra snippets: it measures where a URL sits, not what the page says.
        `search_lang` / `ui_lang` are the reason a non-US locale is measurable
        at all — the engine carries them for every caller now, not just this one.
        """
        return BraveSearchParams(
            query=self.query,
            country=self.country,
            search_lang=self.search_lang,
            ui_lang=self.ui_lang,
            safe_search=self.safesearch,
            count=self.count,
            offset=page_offset,
            spellcheck=False,
            text_decorations=False,
            extra_snippets=False,
            result_filter="web",
            device=self.device,
        )

    def request_params(self, page_offset: int) -> dict[str, Any]:
        return self.engine_params(page_offset).to_dict()

    def persisted_profile(self) -> dict[str, Any]:
        return {
            **self.request_params(self.offset),
            "max_pages": self.max_pages,
            "device": self.device,
        }


class BraveSeoRankAdapter(SeoProviderAdapter):
    provider = "brave"
    capabilities = (SeoCapability.SERP_RANK,)
    operations = (
        SeoProviderOperation(
            name="brave.web.rank",
            capabilities=(SeoCapability.SERP_RANK,),
            credential_keys=("BRAVE_SEARCH_API_KEY",),
        ),
    )

    def __init__(
        self,
        *,
        client_factory: Callable[[], AbstractAsyncContextManager[Any]] | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        max_concurrency: int = 4,
        min_interval_seconds: float = 0,
        max_attempts: int = 6,
        base_backoff_seconds: float = 0.25,
        max_retry_delay_seconds: float = 40.0,
        timeout_seconds: float = 15.0,
        rate_limiter: RateLimiterLike | None = None,
    ) -> None:
        """The SEO layer above the ONE Brave engine.

        Transport, pacing policy, adaptive header re-tuning, bounded retry and
        the typed 429 all live in ``matrx_scraper.search.BraveSearchClient``.
        This adapter owns what is genuinely SEO: the settings contract, the
        per-organization credential, rank matching, and the cost/quota evidence
        the budget ledger reads. It never opens a Brave connection of its own.

        `rate_limiter` is how a host shares ONE process-wide Brave queue across
        every caller (aidream passes matrx_scraper's shared limiter). With no
        limiter and no `min_interval_seconds`, the adapter is deliberately
        UNPACED — only correct for tests and for a caller that paces elsewhere.
        """
        if max_concurrency < 1 or max_attempts < 1:
            raise ValueError("max_concurrency and max_attempts must be positive")
        if min_interval_seconds < 0 or base_backoff_seconds < 0:
            raise ValueError("rate interval and retry backoff cannot be negative")
        if max_retry_delay_seconds < 0 or timeout_seconds <= 0:
            raise ValueError("retry delay must be nonnegative and timeout must be positive")
        self._api_key: ContextVar[str | None] = ContextVar(
            f"brave_seo_api_key_{id(self)}", default=None
        )
        if rate_limiter is not None:
            self._rate_limiter: RateLimiterLike = rate_limiter
        elif min_interval_seconds > 0:
            self._rate_limiter = RateLimiter(min_interval=min_interval_seconds)
        else:
            self._rate_limiter = NullRateLimiter()
        # allow_missing_key: the key for a rank check is the ORGANIZATION's,
        # resolved per request from the secrets battery — never the process env.
        self._engine = BraveSearchClient(
            allow_missing_key=True,
            client_factory=client_factory,
            sleep=sleep,
            max_concurrency=max_concurrency,
        )
        self._client_factory = client_factory or BraveSearchClient._default_client_factory
        self._max_attempts = max_attempts
        self._base_backoff = base_backoff_seconds
        self._max_retry_delay = max_retry_delay_seconds
        self._timeout = timeout_seconds

    async def authenticate(self, credential: ResolvedCredential) -> None:
        key = credential.values.get("BRAVE_SEARCH_API_KEY")
        if not key:
            raise ValueError("Brave SEO rank collection requires BRAVE_SEARCH_API_KEY")
        self._api_key.set(key)

    async def collect_rank_response(
        self,
        settings: BraveSeoRankSettings,
        credential: ResolvedCredential,
    ) -> ProviderResponse:
        await self.authenticate(credential)
        return await self._collect_rank_response(settings)

    async def collect_response(
        self, request: CollectionRequest, execution: ProviderExecutionContext
    ) -> ProviderResponse:
        del execution
        settings = BraveSeoRankSettings.model_validate(request.settings)
        return await self._collect_rank_response(settings)

    async def _collect_rank_response(
        self,
        settings: BraveSeoRankSettings,
    ) -> ProviderResponse:
        if self._api_key.get() is None:
            raise RuntimeError("Brave SEO adapter is not authenticated")
        pages: list[dict[str, Any]] = []
        quota: list[dict[str, str]] = []
        call_records: list[ProviderCallRecord] = []
        successful_requests = 0
        async with self._client_factory() as client:
            for page_offset in range(settings.offset, settings.offset + settings.max_pages):
                call_started_at = datetime.now(UTC)
                engine_params = settings.engine_params(page_offset)
                response = await self._request_page(client, engine_params)
                successful_requests += 1
                payload = response.payload
                pages.append({"offset": page_offset, "response": payload})
                quota.append(response.quota)
                call_records.append(
                    ProviderCallRecord(
                        provider_call_key=stable_hash(
                            [
                                "brave.web.rank",
                                settings.query,
                                settings.target_domain,
                                settings.target_url,
                                settings.host_site_id,
                                settings.host_page_id,
                                page_offset,
                                call_started_at,
                            ]
                        ),
                        # request_count stays 1 per successful page fetch — cost
                        # is billed per logical request, not per HTTP attempt;
                        # `attempts` (below, in metadata) is separate evidence.
                        request_count=1,
                        # DEF-20 (2026-07-23): Brave Search bills by subscription
                        # tier, not a per-call cost the API reports — there is no
                        # real cost to capture. Estimated_cost stays the only
                        # value, and cost_is_estimated=True on the metadata makes
                        # that explicit to every reader instead of implying a
                        # provider-reported figure.
                        estimated_cost=BRAVE_SEARCH_COST_PER_REQUEST,
                        fetched_at=call_started_at,
                        metadata={
                            "offset": page_offset,
                            "quota": quota[-1],
                            "cost_is_estimated": True,
                            "attempts": response.attempts,
                            "request": {
                                "method": "GET",
                                "url": response.url,
                                # X-Subscription-Token is the secret — never persisted.
                                "headers": {
                                    "Accept": "application/json",
                                    "User-Agent": response.user_agent,
                                },
                                "params": response.request_params,
                            },
                            "response_status": response.status_code,
                        },
                    )
                )
                query = payload.get("query") if isinstance(payload, dict) else None
                if not isinstance(query, dict) or not query.get("more_results_available", False):
                    break
        fetched_at = datetime.now(UTC)
        return ProviderResponse(
            raw={
                "profile": settings.persisted_profile(),
                "pages": pages,
                "quota": quota,
            },
            fetched_at=fetched_at,
            provider_schema_version="brave-web-search-v1",
            request_count=successful_requests,
            estimated_cost=BRAVE_SEARCH_COST_PER_REQUEST * successful_requests,
            currency="USD",
            call_records=call_records,
        )

    async def _request_page(
        self, client: Any, params: BraveSearchParams
    ) -> BraveSearchResponse:
        api_key = self._api_key.get()
        if api_key is None:
            raise RuntimeError("Brave SEO adapter is not authenticated")
        return await self._engine.search_response(
            params,
            api_key=api_key,
            rate_limiter=self._rate_limiter,
            timeout=self._timeout,
            max_attempts=self._max_attempts,
            base_backoff_seconds=self._base_backoff,
            max_retry_delay_seconds=self._max_retry_delay,
            client=client,
        )

    async def normalize(
        self, response: ProviderResponse, context: NormalizationContext
    ) -> list[SeoObservation]:
        settings = BraveSeoRankSettings.model_validate(context.request.settings)
        target, target_page_id = await self._resolve_match_target(settings, context)
        identity = await context.resolve_identity(
            SeoIdentityRequest(
                keyword=settings.query,
                language=settings.search_lang,
                target_page_id=target_page_id,
                country_code=settings.country if settings.country != "ALL" else None,
                engine="brave",
                device=settings.device,
                search_type="organic",
                target_domain=target.canonical_domain,
                settings=settings.model_dump(mode="json"),
            )
        )
        # DEF-25: a site-less request (no `host_site_id`) resolves no
        # rank_target by design (orm_identity.py) — the collection is
        # observation-only: the SERP snapshot below still persists, but no
        # RankObservation is built against a nonexistent target.
        raw = response.raw
        if not isinstance(raw, dict) or not isinstance(raw.get("pages"), list):
            raise TypeError("Brave SEO response must contain a pages list")
        results: list[SerpResultObservation] = []
        query_metadata: list[dict[str, Any]] = []
        for page in raw["pages"]:
            page_offset = int(page["offset"])
            page_response = page["response"]
            query = page_response.get("query", {})
            query_metadata.append({"offset": page_offset, **query})
            web = page_response.get("web", {})
            page_results = web.get("results", []) if isinstance(web, dict) else []
            for index, item in enumerate(page_results, start=1):
                if not isinstance(item, dict):
                    continue
                results.append(
                    SerpResultObservation(
                        absolute_rank=page_offset * settings.count + index,
                        organic_rank=page_offset * settings.count + index,
                        url=item.get("url"),
                        domain=_domain(item.get("url")),
                        title=item.get("title"),
                        snippet=item.get("description"),
                        extras={
                            "page_offset": page_offset,
                            "page_rank": index,
                            "profile": item.get("profile"),
                            "language": item.get("language"),
                            "family_friendly": item.get("family_friendly"),
                        },
                    )
                )
        snapshot = SerpSnapshotObservation(
            keyword_id=identity.keyword_id,
            rank_target_id=identity.rank_target_id,
            location_id=identity.location_id,
            engine="brave",
            language=settings.search_lang,
            device=settings.device,
            search_type="organic",
            observed_at=response.fetched_at,
            query_settings=settings.persisted_profile(),
            serp_features={"query_pages": query_metadata},
            results=results,
        )
        matched_result = None
        matched = None
        for result in results:
            candidate = match_rank_url(result.url, target)
            if candidate is not None:
                matched_result = result
                matched = candidate
                break
        observations: list[SeoObservation] = [snapshot]
        if (
            identity.rank_target_id is not None
            and matched is not None
            and matched_result is not None
        ):
            observations.append(
                RankObservation(
                    keyword_id=identity.keyword_id,
                    rank_target_id=identity.rank_target_id,
                    location_id=identity.location_id,
                    engine="brave",
                    locale=settings.country,
                    language=settings.search_lang,
                    device=settings.device,
                    search_type="organic",
                    matched_domain=matched.matched_domain,
                    matched_url=matched.matched_url,
                    organic_rank=matched_result.organic_rank,
                    absolute_rank=matched_result.absolute_rank,
                    result_type=matched_result.result_type,
                    match_rule=matched.match_rule,
                    observed_at=response.fetched_at,
                    query_settings=settings.persisted_profile(),
                    title=matched_result.title,
                    snippet=matched_result.snippet,
                    extras={"brave_query_pages": query_metadata},
                )
            )
        return observations

    async def _resolve_match_target(
        self,
        settings: BraveSeoRankSettings,
        context: NormalizationContext,
    ) -> tuple[RankMatchTarget, str | None]:
        domain = settings.target_domain
        page_url = settings.target_url
        aliases = list(settings.target_url_aliases)
        page_id: str | None = None
        if settings.host_site_id:
            site = await context.resolve_host_binding(
                HostBindingRequest(resource_kind="web_site", resource_id=settings.host_site_id)
            )
            site_domain = canonicalize_domain(site.canonical_url)
            if domain and canonicalize_domain(domain) != site_domain:
                raise ValueError("target_domain conflicts with canonical host site binding")
            domain = site_domain
        if settings.host_page_id:
            page = await context.resolve_host_binding(
                HostBindingRequest(resource_kind="web_page", resource_id=settings.host_page_id)
            )
            page_domain = canonicalize_domain(page.canonical_url)
            if domain is None:
                domain = page_domain
            elif page_domain != canonicalize_domain(domain) and not page_domain.endswith(
                f".{canonicalize_domain(domain)}"
            ):
                raise ValueError("canonical host page conflicts with target site binding")
            if page_url and page_url != page.canonical_url:
                aliases.append(page_url)
            page_url = page.canonical_url
            page_id = page.page_id
        if not domain:
            raise ValueError("resolved Brave rank target has no canonical domain")
        return (
            RankMatchTarget(
                canonical_domain=domain,
                canonical_url=page_url,
                url_aliases=tuple(aliases),
                include_subdomains=settings.include_subdomains,
            ),
            page_id,
        )




def _domain(url: Any) -> str | None:
    if not isinstance(url, str):
        return None
    from urllib.parse import urlsplit

    hostname = urlsplit(url).hostname
    return hostname.casefold() if hostname else None
