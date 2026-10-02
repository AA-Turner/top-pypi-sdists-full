from __future__ import annotations

import asyncio
import json
import re
from collections.abc import Awaitable, Callable, Mapping
from contextvars import ContextVar
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Any, Protocol
from urllib.parse import urlsplit

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..adapters import ProviderExecutionContext, SeoProviderAdapter, SeoProviderOperation
from ..contracts import (
    CollectionRequest,
    CredentialReferenceKind,
    HostBindingRequest,
    NormalizationContext,
    ProviderCallRecord,
    ProviderResponse,
    ProviderTaskCheckpoint,
    ResolvedCredential,
    SearchPerformanceObservation,
    SeoCapability,
    SeoIdentityRequest,
    SeoObservation,
)
from ..identity import stable_hash
from ..rank_matching import canonicalize_rank_url


class BingWebmasterOperationName(StrEnum):
    SEARCH_PERFORMANCE = "bing_webmaster.search_performance"
    INTELLIGENCE_SNAPSHOT = "bing_webmaster.intelligence_snapshot"
    SITES = "bing_webmaster.sites.list"
    CRAWL_STATS = "bing_webmaster.crawl.stats"
    CRAWL_ISSUES = "bing_webmaster.crawl.issues"
    URL_INFO = "bing_webmaster.url.info"
    URL_TRAFFIC = "bing_webmaster.url.traffic"
    LINK_COUNTS = "bing_webmaster.links.counts"
    URL_LINKS = "bing_webmaster.links.url"
    FETCHED_URLS = "bing_webmaster.urls.fetched"
    FEEDS = "bing_webmaster.feeds.list"
    FEED_DETAILS = "bing_webmaster.feeds.details"
    FETCHED_URL_DETAILS = "bing_webmaster.urls.fetched_details"
    KEYWORD_IMPRESSIONS = "bing_webmaster.keyword.impressions"
    KEYWORD_STATS = "bing_webmaster.keyword.stats"
    RELATED_KEYWORDS = "bing_webmaster.keyword.related"
    CONTENT_SUBMISSION_QUOTA = "bing_webmaster.quota.content_submission"
    URL_SUBMISSION_QUOTA = "bing_webmaster.quota.url_submission"
    CRAWL_SETTINGS = "bing_webmaster.crawl.settings"
    QUERY_PARAMETERS = "bing_webmaster.site.query_parameters"
    COUNTRY_REGION_SETTINGS = "bing_webmaster.site.country_region"
    SITE_MOVES = "bing_webmaster.site.moves"
    BLOCKED_URLS = "bing_webmaster.site.blocked_urls"
    CONNECTED_PAGES = "bing_webmaster.links.connected_pages"
    PAGE_PREVIEW_BLOCKS = "bing_webmaster.site.page_preview_blocks"
    DEEP_LINK_BLOCKS = "bing_webmaster.site.deep_link_blocks"
    QUERY_TRAFFIC = "bing_webmaster.query.traffic"
    PAGE_QUERIES = "bing_webmaster.page.queries"
    QUERY_PAGE_DETAILS = "bing_webmaster.query_page.details"
    CHILD_URL_TRAFFIC = "bing_webmaster.url.children_traffic"


_REFERENCE_KINDS = (CredentialReferenceKind.INTEGRATION_CONNECTION,)


def _operation(name: BingWebmasterOperationName, capability: SeoCapability) -> SeoProviderOperation:
    return SeoProviderOperation(
        name=name.value,
        capability=capability,
        credential_keys=(),
        reference_kinds=_REFERENCE_KINDS,
    )


BING_WEBMASTER_OPERATIONS = (
    _operation(BingWebmasterOperationName.SEARCH_PERFORMANCE, SeoCapability.SEARCH_PERFORMANCE),
    *(
        _operation(name, SeoCapability.RAW_PROVIDER)
        for name in BingWebmasterOperationName
        if name is not BingWebmasterOperationName.SEARCH_PERFORMANCE
    ),
)


class BingDimensionProfile(StrEnum):
    PROPERTY = "property"
    QUERY = "query"
    PAGE = "page"
    QUERY_PAGE = "query_page"


class BingWebmasterTransport(StrEnum):
    """Wire protocols the first-party adapter is allowed to persist."""

    JSON_HTTP = "json_http"


class BingSearchPerformanceSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_url: str
    host_site_id: str
    start_date: date
    end_date: date
    profiles: tuple[BingDimensionProfile, ...] = (
        BingDimensionProfile.PROPERTY,
        BingDimensionProfile.QUERY,
        BingDimensionProfile.PAGE,
        BingDimensionProfile.QUERY_PAGE,
    )
    max_query_fanout: int = Field(default=50, ge=0, le=250)
    max_calls: int = Field(default=100, ge=1, le=500)

    @field_validator("site_url")
    @classmethod
    def provider_site_url(cls, value: str) -> str:
        normalized = value.strip()
        parsed = urlsplit(normalized)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Bing Webmaster site_url must be an absolute HTTP(S) URL")
        return normalized

    @field_validator("host_site_id")
    @classmethod
    def require_host_site(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Bing Webmaster host_site_id must be nonblank")
        return normalized

    @model_validator(mode="after")
    def validate_window(self) -> BingSearchPerformanceSettings:
        if self.end_date < self.start_date:
            raise ValueError("Bing Webmaster end_date must be on or after start_date")
        if (self.end_date - self.start_date).days > 366:
            raise ValueError("Bing Webmaster backfill window cannot exceed 367 days")
        if not self.profiles or len(self.profiles) != len(set(self.profiles)):
            raise ValueError("Bing Webmaster profiles must be nonempty and unique")
        if BingDimensionProfile.QUERY_PAGE in self.profiles and self.max_query_fanout < 1:
            raise ValueError("query_page collection requires positive max_query_fanout")
        requested = set(self.profiles)
        minimum_calls = len(requested - {BingDimensionProfile.QUERY_PAGE})
        if BingDimensionProfile.QUERY_PAGE in self.profiles:
            minimum_calls += 1  # At least one GetQueryPageStats fanout.
            if BingDimensionProfile.QUERY not in requested:
                minimum_calls += 1  # GetQueryStats discovers fanout queries.
        if self.max_calls < minimum_calls:
            raise ValueError("Bing Webmaster max_calls is smaller than the requested profiles")
        return self


class BingIntelligenceSnapshotSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_url: str
    host_site_id: str
    max_link_pages: int = Field(default=1, ge=1, le=10)

    @field_validator("site_url")
    @classmethod
    def provider_site_url(cls, value: str) -> str:
        return BingSearchPerformanceSettings.provider_site_url(value)

    @field_validator("host_site_id")
    @classmethod
    def require_host_site(cls, value: str) -> str:
        return BingSearchPerformanceSettings.require_host_site(value)


class BingRawSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_url: str | None = None
    url: str | None = None
    feed_url: str | None = None
    query: str | None = None
    country: str | None = None
    language: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    page: int | None = Field(default=None, ge=0, le=1_000)

    @field_validator("site_url", "url", "feed_url")
    @classmethod
    def provider_optional_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        parsed = urlsplit(normalized)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Bing Webmaster URLs must be absolute HTTP(S) URLs")
        return normalized


class BingApiResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any]
    status_code: int = 200
    headers: dict[str, str] = Field(default_factory=dict)
    # Exact outbound request evidence (DEF-1x parity contract). Optional so
    # existing fixture/fake clients keep working without it.
    request_url: str = ""
    transport: BingWebmasterTransport = BingWebmasterTransport.JSON_HTTP


class BingWebmasterClient(Protocol):
    async def call(self, method: str, params: Mapping[str, Any]) -> BingApiResponse: ...


BingClientFactory = Callable[[ResolvedCredential], BingWebmasterClient]
BingPageResourceResolver = Callable[[CollectionRequest, str, list[str]], Awaitable[dict[str, str]]]


class BingCollectionError(RuntimeError):
    def __init__(
        self,
        *,
        attempts: int,
        message: str,
        response: BingApiResponse | None = None,
        attempt_evidence: list[dict[str, Any]] | None = None,
    ) -> None:
        self.attempts = attempts
        self.response = response
        self.attempt_evidence = attempt_evidence or []
        super().__init__(message)


class BingTransportError(RuntimeError):
    pass


class BingSearchDiagnostics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    avg_click_position: Decimal | None = None
    avg_impression_position: Decimal | None = None
    position: Decimal | None = None
    position_semantics: str
    provider_updates: str = "weekly"
    source_method: str


class BingWebmasterAdapter(SeoProviderAdapter):
    provider = "bing_webmaster"
    capabilities = (SeoCapability.SEARCH_PERFORMANCE, SeoCapability.RAW_PROVIDER)
    operations = BING_WEBMASTER_OPERATIONS
    _RETRYABLE_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})
    _RETRYABLE_ERROR_CODES = frozenset({1, 2, 4, 5})
    _ATTEMPT_BODY_LIMIT_BYTES = 32_768

    def __init__(
        self,
        *,
        client_factory: BingClientFactory,
        page_resource_resolver: BingPageResourceResolver | None = None,
        max_attempts: int = 3,
        base_backoff_seconds: float = 0.5,
        max_retry_delay_seconds: float = 8,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("Bing Webmaster max_attempts must be positive")
        self._client_factory = client_factory
        self._page_resource_resolver = page_resource_resolver
        self._max_attempts = max_attempts
        self._base_backoff = base_backoff_seconds
        self._max_retry_delay = max_retry_delay_seconds
        self._sleep = sleep
        self._client: ContextVar[BingWebmasterClient | None] = ContextVar(
            f"bing_webmaster_client_{id(self)}", default=None
        )

    async def authenticate(self, credential: ResolvedCredential) -> None:
        values = credential.values
        if not values.get("access_token") and not values.get("BING_WEBMASTER_API_KEY"):
            raise ValueError("Bing Webmaster requires a resolved OAuth token or vaulted API key")
        self._client.set(self._client_factory(credential))

    async def collect_response(
        self,
        request: CollectionRequest,
        execution: ProviderExecutionContext,
    ) -> ProviderResponse:
        try:
            operation = BingWebmasterOperationName(request.operation)
        except ValueError as exc:
            raise ValueError(f"unsupported Bing Webmaster operation {request.operation!r}") from exc
        client = self._client.get()
        if client is None:
            raise RuntimeError("Bing Webmaster adapter must be authenticated before collection")
        checkpoints = {
            task.external_task_id: task
            for task in await execution.resumable_tasks()
            if task.endpoint == request.operation
        }
        pages: list[dict[str, Any]] = []
        calls: list[ProviderCallRecord] = []
        failures: list[dict[str, Any]] = []
        if operation is BingWebmasterOperationName.INTELLIGENCE_SNAPSHOT:
            settings = BingIntelligenceSnapshotSettings.model_validate(request.settings)
            calls_to_make = [
                ("GetCrawlStats", {"siteUrl": settings.site_url}, "crawl_stats"),
                ("GetCrawlIssues", {"siteUrl": settings.site_url}, "crawl_issues"),
                ("GetFeeds", {"siteUrl": settings.site_url}, "feeds"),
                ("GetFetchedUrls", {"siteUrl": settings.site_url}, "fetched_urls"),
                (
                    "GetContentSubmissionQuota",
                    {"siteUrl": settings.site_url},
                    "content_submission_quota",
                ),
                (
                    "GetUrlSubmissionQuota",
                    {"siteUrl": settings.site_url},
                    "url_submission_quota",
                ),
                *[
                    ("GetLinkCounts", {"siteUrl": settings.site_url, "page": page}, "link_counts")
                    for page in range(settings.max_link_pages)
                ],
            ]
            for method, params, profile in calls_to_make:
                await self._collect_one(
                    client,
                    execution,
                    request,
                    checkpoints,
                    method,
                    params,
                    pages,
                    calls,
                    failures,
                    profile=profile,
                )
            return _provider_response(
                request.operation,
                pages,
                calls,
                failures,
                metadata={
                    "site_url": settings.site_url,
                    "host_site_id": settings.host_site_id,
                    "snapshot_kind": "free_first_party_site_intelligence",
                },
            )

        if operation is not BingWebmasterOperationName.SEARCH_PERFORMANCE:
            settings = BingRawSettings.model_validate(request.settings)
            method, params = _raw_method_and_params(operation, settings)
            await self._collect_one(
                client, execution, request, checkpoints, method, params, pages, calls, failures
            )
            return _provider_response(request.operation, pages, calls, failures)

        settings = BingSearchPerformanceSettings.model_validate(request.settings)
        call_budget = settings.max_calls
        query_values: list[str] = []
        selected_queries: list[str] = []
        base = (
            (BingDimensionProfile.PROPERTY, "GetRankAndTrafficStats"),
            (BingDimensionProfile.QUERY, "GetQueryStats"),
            (BingDimensionProfile.PAGE, "GetPageStats"),
        )
        required_profiles = set(settings.profiles)
        if BingDimensionProfile.QUERY_PAGE in required_profiles:
            required_profiles.add(BingDimensionProfile.QUERY)
        for profile, method in base:
            if profile not in required_profiles:
                continue
            if call_budget < 1:
                failures.append(_budget_failure(method))
                continue
            page = await self._collect_one(
                client,
                execution,
                request,
                checkpoints,
                method,
                {"siteUrl": settings.site_url},
                pages,
                calls,
                failures,
                profile=profile.value,
            )
            call_budget -= 1
            if profile is BingDimensionProfile.QUERY and page and not page.get("error"):
                for query in _queries_in_window(page, settings.start_date, settings.end_date):
                    if query not in query_values:
                        query_values.append(query)

        if BingDimensionProfile.QUERY_PAGE in settings.profiles:
            for query in query_values[: settings.max_query_fanout]:
                if call_budget < 1:
                    break
                selected_queries.append(query)
                await self._collect_one(
                    client,
                    execution,
                    request,
                    checkpoints,
                    "GetQueryPageStats",
                    {"siteUrl": settings.site_url, "query": query},
                    pages,
                    calls,
                    failures,
                    profile=BingDimensionProfile.QUERY_PAGE.value,
                )
                call_budget -= 1
        return _provider_response(
            request.operation,
            pages,
            calls,
            failures,
            metadata={
                "query_page_fanout": {
                    "available_queries": len(query_values),
                    "selected_queries": selected_queries,
                    "selection": "window_impressions_desc_clicks_desc_query_asc",
                    "cap": settings.max_query_fanout,
                    "budget_limited": len(selected_queries)
                    < min(len(query_values), settings.max_query_fanout),
                }
            },
        )

    async def _collect_one(
        self,
        client: BingWebmasterClient,
        execution: ProviderExecutionContext,
        request: CollectionRequest,
        checkpoints: dict[str, ProviderTaskCheckpoint],
        method: str,
        params: dict[str, Any],
        pages: list[dict[str, Any]],
        calls: list[ProviderCallRecord],
        failures: list[dict[str, Any]],
        *,
        profile: str = "raw",
    ) -> dict[str, Any] | None:
        checkpoint_id = stable_hash(
            [execution.run.id, self.provider, request.operation, method, params]
        )
        prior = checkpoints.get(checkpoint_id)
        if prior is not None and prior.status == "completed":
            page = _page_from_checkpoint(prior, method, profile)
            pages.append(page)
            calls.extend(_calls_from_checkpoint(prior, page))
            return page
        prior_requests = prior.request_count if prior is not None else 0
        prior_call_history = _call_history(prior)
        provider_call_key = f"{checkpoint_id}:attempt:{prior_requests}"
        started_at = datetime.now(UTC)
        try:
            response, attempts, attempt_evidence = await self._call_with_retry(
                client, method, params
            )
        except BingCollectionError as exc:
            failure = {
                "method": method,
                "profile": profile,
                "type": type(exc).__name__,
                "message": str(exc),
            }
            failures.append(failure)
            finished_at = datetime.now(UTC)
            payload = (
                exc.response.payload if exc.response is not None else {"transport_error": failure}
            )
            failure_request_evidence = _request_evidence(
                exc.response.request_url if exc.response is not None else "",
                params,
                transport=(
                    exc.response.transport
                    if exc.response is not None
                    else BingWebmasterTransport.JSON_HTTP
                ),
            )
            checkpoint = ProviderTaskCheckpoint(
                external_task_id=checkpoint_id,
                endpoint=request.operation,
                status="failed",
                request_payload={
                    "method": method,
                    "params": params,
                    "profile": profile,
                    "provider_call_key": provider_call_key,
                    "current_attempt_request_count": exc.attempts,
                    "attempt_evidence": exc.attempt_evidence,
                    "request_evidence": failure_request_evidence,
                    "call_history": [
                        *prior_call_history,
                        _call_history_entry(
                            provider_call_key=provider_call_key,
                            request_count=exc.attempts,
                            fetched_at=finished_at,
                            method=method,
                            profile=profile,
                            request=params,
                            status_code=(exc.response.status_code if exc.response else None),
                            quota_headers=(
                                _quota_headers(exc.response.headers) if exc.response else {}
                            ),
                            attempt_evidence=exc.attempt_evidence,
                            request_evidence=failure_request_evidence,
                            error=failure,
                        ),
                    ],
                    "quota_headers": _quota_headers(exc.response.headers)
                    if exc.response is not None
                    else {},
                },
                response_payload=payload,
                request_count=prior_requests + exc.attempts,
                provider_cost=Decimal(0),
                submitted_at=prior.submitted_at if prior else started_at,
                last_polled_at=finished_at,
                completed_at=finished_at,
                error=failure,
            )
            await execution.checkpoint(checkpoint)
            page = {
                "method": method,
                "profile": profile,
                "request": params,
                "response": payload,
                "status_code": exc.response.status_code if exc.response else None,
                "quota_headers": _quota_headers(exc.response.headers) if exc.response else {},
                "attempt_evidence": exc.attempt_evidence,
                "request_evidence": failure_request_evidence,
                "error": failure,
            }
            pages.append(page)
            calls.extend(_calls_from_checkpoint(checkpoint, page))
            return page
        finished_at = datetime.now(UTC)
        request_evidence = _request_evidence(
            response.request_url,
            params,
            transport=response.transport,
        )
        page = {
            "method": method,
            "profile": profile,
            "request": params,
            "response": response.payload,
            "status_code": response.status_code,
            "quota_headers": _quota_headers(response.headers),
            "attempt_evidence": attempt_evidence,
            "request_evidence": request_evidence,
        }
        checkpoint = ProviderTaskCheckpoint(
            external_task_id=checkpoint_id,
            endpoint=request.operation,
            status="completed",
            request_payload={
                "method": method,
                "params": params,
                "profile": profile,
                "provider_call_key": provider_call_key,
                "current_attempt_request_count": attempts,
                "attempt_evidence": attempt_evidence,
                "request_evidence": request_evidence,
                "call_history": [
                    *prior_call_history,
                    _call_history_entry(
                        provider_call_key=provider_call_key,
                        request_count=attempts,
                        fetched_at=finished_at,
                        method=method,
                        profile=profile,
                        request=params,
                        status_code=response.status_code,
                        quota_headers=page["quota_headers"],
                        attempt_evidence=attempt_evidence,
                        request_evidence=request_evidence,
                        error=None,
                    ),
                ],
                "quota_headers": page["quota_headers"],
            },
            response_payload=response.payload,
            request_count=prior_requests + attempts,
            provider_cost=Decimal(0),
            submitted_at=prior.submitted_at if prior else started_at,
            last_polled_at=finished_at,
            completed_at=finished_at,
        )
        await execution.checkpoint(checkpoint)
        pages.append(page)
        calls.extend(_calls_from_checkpoint(checkpoint, page))
        return page

    async def _call_with_retry(
        self, client: BingWebmasterClient, method: str, params: Mapping[str, Any]
    ) -> tuple[BingApiResponse, int, list[dict[str, Any]]]:
        last_response = None
        last_error: Exception | None = None
        evidence: list[dict[str, Any]] = []
        for attempt in range(1, self._max_attempts + 1):
            try:
                response = await client.call(method, params)
            except (httpx.TimeoutException, httpx.TransportError, BingTransportError) as exc:
                last_error = exc
                evidence.append(
                    {
                        "attempt": attempt,
                        "transport_error": type(exc).__name__,
                        "message": str(exc),
                    }
                )
                if attempt < self._max_attempts:
                    await self._sleep(self._retry_delay(attempt, {}))
                    continue
                break
            last_response = response
            fault = _api_fault(response.payload)
            evidence.append(
                {
                    "attempt": attempt,
                    "status_code": response.status_code,
                    "quota_headers": _quota_headers(response.headers),
                    "response": _bounded_payload(
                        response.payload, limit=self._ATTEMPT_BODY_LIMIT_BYTES
                    ),
                    "api_fault": ({"code": fault[0], "message": fault[1]} if fault else None),
                }
            )
            if response.status_code < 400 and fault is None:
                try:
                    _response_data(response.payload)
                except ValueError as exc:
                    raise BingCollectionError(
                        attempts=attempt,
                        message=str(exc),
                        response=response,
                        attempt_evidence=evidence,
                    ) from exc
                return response, attempt, evidence
            retryable = response.status_code in self._RETRYABLE_STATUSES or (
                fault is not None and fault[0] in self._RETRYABLE_ERROR_CODES
            )
            if retryable and attempt < self._max_attempts:
                await self._sleep(self._retry_delay(attempt, response.headers))
                continue
            message = fault[1] if fault else f"Bing Webmaster HTTP {response.status_code}"
            raise BingCollectionError(
                attempts=attempt,
                message=message,
                response=response,
                attempt_evidence=evidence,
            )
        raise BingCollectionError(
            attempts=self._max_attempts,
            message=f"Bing Webmaster {method} transport retries exhausted: {last_error}",
            response=last_response,
            attempt_evidence=evidence,
        )

    def _retry_delay(self, attempt: int, headers: Mapping[str, str]) -> float:
        retry_after = headers.get("Retry-After") or headers.get("retry-after")
        if retry_after:
            try:
                return min(max(float(retry_after), 0), self._max_retry_delay)
            except ValueError:
                pass
        return min(self._base_backoff * (2 ** (attempt - 1)), self._max_retry_delay)

    async def normalize(
        self, response: ProviderResponse, context: NormalizationContext
    ) -> list[SeoObservation]:
        if context.request.operation != BingWebmasterOperationName.SEARCH_PERFORMANCE.value:
            return []
        settings = BingSearchPerformanceSettings.model_validate(context.request.settings)
        site = await context.resolve_host_binding(
            HostBindingRequest(resource_kind="web_site", resource_id=settings.host_site_id)
        )
        if canonicalize_rank_url(site.canonical_url) != canonicalize_rank_url(settings.site_url):
            raise ValueError("Bing Webmaster property does not match the canonical host site")
        rows = _performance_rows(
            response.raw,
            settings.start_date,
            settings.end_date,
            profiles=set(settings.profiles),
        )
        page_urls = sorted({row["page"] for row in rows if row.get("page")})
        if page_urls and self._page_resource_resolver is None:
            raise RuntimeError("Bing page observations require the canonical page resolver")
        page_ids_by_url: dict[str, str] = {}
        if page_urls and self._page_resource_resolver is not None:
            resources = await self._page_resource_resolver(
                context.request, settings.host_site_id, page_urls
            )
            missing = sorted(set(page_urls) - set(resources))
            if missing:
                raise ValueError(
                    f"Bing Webmaster could not resolve {len(missing)} in-scope page URL(s)"
                )
            for page_url, resource_id in resources.items():
                binding = await context.resolve_host_binding(
                    HostBindingRequest(resource_kind="web_page", resource_id=resource_id)
                )
                if binding.site_id != site.site_id:
                    raise ValueError("Bing Webmaster page resolved outside the requested site")
                if binding.page_id is None:
                    raise ValueError("Bing web_page binding resolved without a page id")
                page_ids_by_url[page_url] = binding.page_id
        queries = sorted({row["query"] for row in rows if row.get("query")})
        identities = await context.resolve_identities(
            [
                SeoIdentityRequest(
                    keyword=query,
                    language="und",
                    settings={"source": "bing_webmaster"},
                )
                for query in queries
            ]
        )
        keyword_ids = {
            query: identity.keyword_id for query, identity in zip(queries, identities, strict=True)
        }
        observations: list[SeoObservation] = []
        for row in rows:
            clicks = _whole(row.get("Clicks", 0), "Clicks")
            impressions = _whole(row.get("Impressions", 0), "Impressions")
            diagnostics = BingSearchDiagnostics(
                avg_click_position=_decimal(row.get("AvgClickPosition")),
                avg_impression_position=_decimal(row.get("AvgImpressionPosition")),
                position=_decimal(row.get("Position")),
                position_semantics="provider aggregate; never an exact live rank",
                provider_updates=(
                    "daily" if row["method"] == "GetRankAndTrafficStats" else "weekly"
                ),
                source_method=row["method"],
            )
            observations.append(
                SearchPerformanceObservation(
                    site_id=site.site_id,
                    page_id=page_ids_by_url.get(row.get("page")),
                    keyword_id=keyword_ids.get(row.get("query")),
                    date=row["date"],
                    query=row.get("query"),
                    dimension_profile=row["profile"],
                    clicks=clicks,
                    impressions=impressions,
                    ctr=(Decimal(clicks) / Decimal(impressions)) if impressions else Decimal(0),
                    average_position=diagnostics.avg_impression_position or diagnostics.position,
                    extras={
                        "bing": diagnostics.model_dump(mode="json"),
                        "page_url": row.get("page"),
                        "provider_history_is_top_rows": row["profile"] != "property",
                    },
                )
            )
        return observations


def _provider_response(
    operation: str,
    pages: list[dict[str, Any]],
    calls: list[ProviderCallRecord],
    failures: list[dict[str, Any]],
    *,
    metadata: dict[str, Any] | None = None,
) -> ProviderResponse:
    return ProviderResponse(
        raw={
            "operation": operation,
            "pages": pages,
            "failures": failures,
            "metadata": metadata or {},
        },
        fetched_at=datetime.now(UTC),
        provider_schema_version="bing-webmaster-json-v1",
        call_records=calls,
        error=(
            {
                "type": "BingWebmasterPartialCollectionError",
                "message": (
                    f"{len(failures)} Bing Webmaster call(s) failed: "
                    f"{failures[0].get('message', 'unknown provider failure')}"
                ),
                "failures": failures,
            }
            if failures
            else None
        ),
    )


def _response_data(payload: dict[str, Any]) -> Any:
    if "d" not in payload:
        raise ValueError("Bing Webmaster JSON response must contain the 'd' envelope")
    data = payload["d"]
    if not isinstance(data, dict | list) and data is not None:
        raise ValueError("Bing Webmaster 'd' envelope has an invalid shape")
    return data


def _api_fault(payload: dict[str, Any]) -> tuple[int, str] | None:
    candidate = payload.get("error") or payload.get("Error")
    if candidate is None and "ErrorCode" in payload:
        candidate = payload
    if candidate is None and isinstance(payload.get("d"), dict):
        value = payload["d"]
        if "ErrorCode" in value:
            candidate = value
    if not isinstance(candidate, dict):
        return None
    raw_code = candidate.get("ErrorCode", candidate.get("code", 2))
    try:
        code = int(raw_code)
    except (TypeError, ValueError):
        code = 2
    return code, str(candidate.get("Message") or candidate.get("message") or "Bing API fault")


def _bounded_payload(payload: dict[str, Any], *, limit: int) -> dict[str, Any]:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    size = len(encoded.encode("utf-8"))
    if size <= limit:
        return {"body": payload, "bytes": size, "truncated": False}
    preview = encoded.encode("utf-8")[:limit].decode("utf-8", errors="replace")
    return {
        "body_preview": preview,
        "bytes": size,
        "truncated": True,
        "checksum": stable_hash([encoded]),
    }


_DATE_RE = re.compile(r"^/Date\((?P<millis>-?\d+)(?P<offset>[+-]\d{4})?\)/$")


def parse_bing_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    match = _DATE_RE.match(text)
    if match:
        moment = datetime.fromtimestamp(int(match.group("millis")) / 1_000, tz=UTC)
        offset = match.group("offset")
        if offset:
            sign = 1 if offset[0] == "+" else -1
            moment += sign * timedelta(hours=int(offset[1:3]), minutes=int(offset[3:5]))
        return moment.date()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError as exc:
        raise ValueError(f"invalid Bing Webmaster date {text!r}") from exc


def _queries_in_window(page: dict[str, Any], start: date, end: date) -> list[str]:
    data = _response_data(page["response"])
    if not isinstance(data, list):
        raise ValueError("Bing Webmaster GetQueryStats expected a list response")
    totals: dict[str, tuple[int, int]] = {}
    for row in data:
        if not isinstance(row, dict):
            raise ValueError("Bing Webmaster query row must be an object")
        query = str(row.get("Query") or "").strip()
        if query and start <= parse_bing_date(row.get("Date")) <= end:
            impressions, clicks = totals.get(query, (0, 0))
            totals[query] = (
                impressions + _whole(row.get("Impressions", 0), "Impressions"),
                clicks + _whole(row.get("Clicks", 0), "Clicks"),
            )
    return sorted(
        totals,
        key=lambda query: (
            -totals[query][0],
            -totals[query][1],
            query.casefold(),
            query,
        ),
    )


def _performance_rows(
    raw: dict[str, Any],
    start: date,
    end: date,
    *,
    profiles: set[BingDimensionProfile],
) -> list[dict[str, Any]]:
    pages = raw.get("pages")
    if not isinstance(pages, list):
        raise ValueError("Bing Webmaster raw response must contain pages")
    output: list[dict[str, Any]] = []
    for page in pages:
        if not isinstance(page, dict) or page.get("error"):
            continue
        profile = str(page.get("profile"))
        if profile not in {item.value for item in BingDimensionProfile}:
            continue
        if BingDimensionProfile(profile) not in profiles:
            continue
        data = _response_data(page.get("response") or {})
        if not isinstance(data, list):
            raise ValueError(f"Bing Webmaster {page.get('method')} expected a list response")
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Bing Webmaster performance row must be an object")
            observed_date = parse_bing_date(item.get("Date"))
            if not start <= observed_date <= end:
                continue
            value = str(item.get("Query") or "").strip() or None
            query = value if profile == BingDimensionProfile.QUERY.value else None
            page_url = value if profile in {"page", "query_page"} else None
            if profile == "query_page":
                query = str((page.get("request") or {}).get("query") or "").strip() or None
            output.append(
                {
                    **item,
                    "date": observed_date,
                    "profile": profile,
                    "method": page.get("method"),
                    "query": query,
                    "page": canonicalize_rank_url(page_url) if page_url else None,
                }
            )
    return output


def _whole(value: Any, name: str) -> int:
    metric = Decimal(str(value))
    if not metric.is_finite() or metric < 0 or metric != metric.to_integral_value():
        raise ValueError(f"Bing Webmaster {name} must be a nonnegative whole number")
    return int(metric)


def _decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    metric = Decimal(str(value))
    # Bing uses -1 for an unavailable aggregate position (observed on rows
    # with impressions but no clicks). It is absence, not a negative rank.
    if metric == Decimal(-1):
        return None
    if not metric.is_finite() or metric < 0:
        raise ValueError("Bing Webmaster position must be finite and nonnegative")
    return metric


def _quota_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        key.lower(): value
        for key, value in headers.items()
        if key.lower().startswith(("x-ratelimit-", "x-ms-")) or key.lower() == "retry-after"
    }


def _request_evidence(
    url: str,
    params: Mapping[str, Any],
    *,
    transport: BingWebmasterTransport = BingWebmasterTransport.JSON_HTTP,
) -> dict[str, Any]:
    """Exact outbound request evidence (DEF-1x parity contract). The Bing
    Webmaster transport is always an HTTP GET; the credential travels as an
    Authorization bearer header or an `apikey` query parameter injected
    host-side after `params` is built here, so it never appears in `params`
    and the header slot is redacted uniformly."""

    return {
        "transport": transport.value,
        "method": "GET",
        "url": url,
        "headers": {"Authorization": "Bearer ***"},
        "params": dict(params),
    }


def _page_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint, method: str, profile: str
) -> dict[str, Any]:
    if not isinstance(checkpoint.response_payload, dict):
        raise ValueError("completed Bing Webmaster checkpoint has no response payload")
    return {
        "method": method,
        "profile": profile,
        "request": checkpoint.request_payload.get("params", {}),
        "response": checkpoint.response_payload,
        "status_code": 200,
        "quota_headers": checkpoint.request_payload.get("quota_headers", {}),
        "attempt_evidence": checkpoint.request_payload.get("attempt_evidence", []),
        "request_evidence": checkpoint.request_payload.get(
            "request_evidence", _request_evidence("", checkpoint.request_payload.get("params", {}))
        ),
        "resumed_from_checkpoint": True,
    }


def _call_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint, page: dict[str, Any]
) -> ProviderCallRecord:
    return ProviderCallRecord(
        provider_call_key=str(
            checkpoint.request_payload.get("provider_call_key") or checkpoint.external_task_id
        ),
        external_task_id=checkpoint.external_task_id,
        request_count=int(
            checkpoint.request_payload.get(
                "current_attempt_request_count", checkpoint.request_count
            )
        ),
        reported_cost=Decimal(0),
        fetched_at=checkpoint.completed_at or checkpoint.submitted_at,
        metadata={
            "method": page["method"],
            "profile": page["profile"],
            "request": page["request"],
            "status_code": page.get("status_code"),
            "response_status": page.get("status_code"),
            "quota_headers": page.get("quota_headers", {}),
            "attempt_evidence": page.get("attempt_evidence", []),
            "request_evidence": page.get("request_evidence", {}),
            "error": page.get("error"),
        },
    )


def _call_history(checkpoint: ProviderTaskCheckpoint | None) -> list[dict[str, Any]]:
    if checkpoint is None:
        return []
    value = checkpoint.request_payload.get("call_history", [])
    if not isinstance(value, list):
        raise ValueError("Bing Webmaster checkpoint call_history must be a list")
    return [dict(item) for item in value if isinstance(item, dict)]


def _call_history_entry(
    *,
    provider_call_key: str,
    request_count: int,
    fetched_at: datetime,
    method: str,
    profile: str,
    request: dict[str, Any],
    status_code: int | None,
    quota_headers: dict[str, str],
    attempt_evidence: list[dict[str, Any]],
    request_evidence: dict[str, Any] | None = None,
    error: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "provider_call_key": provider_call_key,
        "request_count": request_count,
        "fetched_at": fetched_at.isoformat(),
        "metadata": {
            "method": method,
            "profile": profile,
            "request": request,
            "status_code": status_code,
            "response_status": status_code,
            "quota_headers": quota_headers,
            "attempt_evidence": attempt_evidence,
            "request_evidence": request_evidence or _request_evidence("", request),
            "error": error,
        },
    }


def _calls_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint, page: dict[str, Any]
) -> list[ProviderCallRecord]:
    history = _call_history(checkpoint)
    if not history:
        return [_call_from_checkpoint(checkpoint, page)]
    output: list[ProviderCallRecord] = []
    for item in history:
        metadata = item.get("metadata")
        if not isinstance(metadata, dict):
            raise ValueError("Bing Webmaster checkpoint call metadata must be an object")
        output.append(
            ProviderCallRecord(
                provider_call_key=str(item["provider_call_key"]),
                external_task_id=checkpoint.external_task_id,
                request_count=int(item["request_count"]),
                reported_cost=Decimal(0),
                fetched_at=datetime.fromisoformat(str(item["fetched_at"])),
                metadata=metadata,
            )
        )
    return output


def _budget_failure(method: str) -> dict[str, Any]:
    return {
        "method": method,
        "type": "BingWebmasterCallBudgetExceeded",
        "message": "approved max_calls budget was exhausted",
    }


def _raw_method_and_params(
    operation: BingWebmasterOperationName, settings: BingRawSettings
) -> tuple[str, dict[str, Any]]:
    mapping = {
        BingWebmasterOperationName.SITES: ("GetUserSites", ()),
        BingWebmasterOperationName.CRAWL_STATS: ("GetCrawlStats", ("siteUrl",)),
        BingWebmasterOperationName.CRAWL_ISSUES: ("GetCrawlIssues", ("siteUrl",)),
        BingWebmasterOperationName.URL_INFO: ("GetUrlInfo", ("siteUrl", "url")),
        BingWebmasterOperationName.URL_TRAFFIC: ("GetUrlTrafficInfo", ("siteUrl", "url")),
        BingWebmasterOperationName.LINK_COUNTS: ("GetLinkCounts", ("siteUrl", "page")),
        BingWebmasterOperationName.URL_LINKS: ("GetUrlLinks", ("siteUrl", "url", "page")),
        BingWebmasterOperationName.FETCHED_URLS: ("GetFetchedUrls", ("siteUrl",)),
        BingWebmasterOperationName.FEEDS: ("GetFeeds", ("siteUrl",)),
        BingWebmasterOperationName.FEED_DETAILS: (
            "GetFeedDetails",
            ("siteUrl", "feedUrl"),
        ),
        BingWebmasterOperationName.FETCHED_URL_DETAILS: (
            "GetFetchedUrlDetails",
            ("siteUrl", "url"),
        ),
        BingWebmasterOperationName.KEYWORD_IMPRESSIONS: (
            "GetKeyword",
            ("q", "country", "language", "startDate", "endDate"),
        ),
        BingWebmasterOperationName.KEYWORD_STATS: (
            "GetKeywordStats",
            ("q", "country", "language"),
        ),
        BingWebmasterOperationName.RELATED_KEYWORDS: (
            "GetRelatedKeywords",
            ("q", "country", "language", "startDate", "endDate"),
        ),
        BingWebmasterOperationName.CONTENT_SUBMISSION_QUOTA: (
            "GetContentSubmissionQuota",
            ("siteUrl",),
        ),
        BingWebmasterOperationName.URL_SUBMISSION_QUOTA: (
            "GetUrlSubmissionQuota",
            ("siteUrl",),
        ),
        BingWebmasterOperationName.CRAWL_SETTINGS: ("GetCrawlSettings", ("siteUrl",)),
        BingWebmasterOperationName.QUERY_PARAMETERS: (
            "GetQueryParameters",
            ("siteUrl",),
        ),
        BingWebmasterOperationName.COUNTRY_REGION_SETTINGS: (
            "GetCountryRegionSettings",
            ("siteUrl",),
        ),
        BingWebmasterOperationName.SITE_MOVES: ("GetSiteMoves", ("siteUrl",)),
        BingWebmasterOperationName.BLOCKED_URLS: ("GetBlockedUrls", ("siteUrl",)),
        BingWebmasterOperationName.CONNECTED_PAGES: (
            "GetConnectedPages",
            ("siteUrl",),
        ),
        BingWebmasterOperationName.PAGE_PREVIEW_BLOCKS: (
            "GetActivePagePreviewBlocks",
            ("siteUrl",),
        ),
        BingWebmasterOperationName.DEEP_LINK_BLOCKS: (
            "GetDeepLinkBlocks",
            ("siteUrl",),
        ),
        BingWebmasterOperationName.QUERY_TRAFFIC: (
            "GetQueryTrafficStats",
            ("siteUrl", "q"),
        ),
        BingWebmasterOperationName.PAGE_QUERIES: (
            "GetPageQueryStats",
            ("siteUrl", "url"),
        ),
        BingWebmasterOperationName.QUERY_PAGE_DETAILS: (
            "GetQueryPageDetailStats",
            ("siteUrl", "q", "url"),
        ),
        BingWebmasterOperationName.CHILD_URL_TRAFFIC: (
            "GetChildrenUrlTrafficInfo",
            ("siteUrl", "url", "page"),
        ),
    }
    method, required = mapping[operation]
    values = {
        "siteUrl": settings.site_url,
        "url": settings.url,
        "feedUrl": settings.feed_url,
        "q": settings.query,
        "country": settings.country,
        "language": settings.language,
        "startDate": settings.start_date.isoformat() if settings.start_date else None,
        "endDate": settings.end_date.isoformat() if settings.end_date else None,
        "page": settings.page,
    }
    missing = [name for name in required if values.get(name) is None]
    if missing:
        raise ValueError(f"Bing Webmaster {operation.value} requires: {', '.join(missing)}")
    return method, {name: values[name] for name in required}


__all__ = [
    "BING_WEBMASTER_OPERATIONS",
    "BingApiResponse",
    "BingCollectionError",
    "BingDimensionProfile",
    "BingIntelligenceSnapshotSettings",
    "BingRawSettings",
    "BingSearchDiagnostics",
    "BingSearchPerformanceSettings",
    "BingTransportError",
    "BingWebmasterAdapter",
    "BingWebmasterOperationName",
    "parse_bing_date",
]
