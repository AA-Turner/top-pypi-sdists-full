"""SerpAPI Google rank collection — the SEO layer ABOVE the ONE SerpAPI engine.

Transport, retry, pacing, quota capture and the body-carried error reason all
live in :mod:`matrx_seo.providers.serpapi_client`. This module owns what is
genuinely SEO: the settings contract, per-organization credentials, rank
matching, and the observations the canonical persistence writes.
"""

from __future__ import annotations

import asyncio
from collections.abc import Mapping, Sequence
from contextvars import ContextVar
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from ..adapters import ProviderExecutionContext, SeoProviderAdapter, SeoProviderOperation
from ..contracts import (
    CollectionReceipt,
    CollectionRequest,
    CollectionTrigger,
    CredentialReferenceKind,
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
from ..rank_matching import RankMatch, RankMatchTarget, canonicalize_domain, match_rank_url
from ..service import SeoCollectionService
from .serpapi_client import (
    SERPAPI_SEARCH_ENDPOINT,
    SerpApiCall,
    SerpApiClient,
    SerpApiHttpTransport,
)

SERPAPI_GOOGLE_RANK_OPERATION = SeoProviderOperation(
    name="google_rank",
    capability=SeoCapability.SERP_RANK,
    credential_keys=("SERPAPI_API_KEY",),
)

_FEATURE_KEYS = (
    "answer_box",
    "knowledge_graph",
    "top_stories",
    "shopping_results",
    "inline_images",
    "related_questions",
    "video_results",
    "ads",
    "local_results",
    "search_information",
)


class SerpApiGoogleRankSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    keyword: str
    target_domain: str | None = None
    target_page_url: str | None = None
    target_url_aliases: tuple[str, ...] = ()
    include_subdomains: bool = True
    host_site_id: str | None = None
    host_page_id: str | None = None

    location: str | None = None
    location_name: str | None = None
    external_location_id: str | None = None
    country_code: str
    region: str | None = None
    city: str | None = None
    postal_code: str | None = None
    timezone: str | None = None
    uule: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    radius_meters: int | None = None

    gl: str
    hl: str
    device: Literal["desktop", "tablet", "mobile"]
    safe: Literal["active", "off"]
    start: int = 0
    google_domain: str = "google.com"
    no_cache: bool = True
    tracked_result_type: Literal["organic", "local_pack"] = "organic"

    @field_validator("keyword", "country_code", "gl", "hl", "google_domain")
    @classmethod
    def require_nonblank(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("SerpAPI rank settings cannot contain blank required values")
        return normalized

    @field_validator("country_code")
    @classmethod
    def normalize_country(cls, value: str) -> str:
        if len(value) != 2:
            raise ValueError("country_code must be an ISO two-letter code")
        return value.upper()

    @field_validator("gl", "hl")
    @classmethod
    def normalize_google_locale(cls, value: str) -> str:
        if len(value) != 2:
            raise ValueError("gl and hl must be two-letter Google locale codes")
        return value.lower()

    @field_validator("target_domain")
    @classmethod
    def normalize_domain(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = canonicalize_domain(value)
        if not normalized:
            raise ValueError("target_domain must contain a hostname")
        return normalized

    @field_validator("start")
    @classmethod
    def validate_start(cls, value: int) -> int:
        if value < 0 or value % 10:
            raise ValueError("start must be a non-negative multiple of 10")
        return value

    @model_validator(mode="after")
    def validate_target_and_location(self) -> SerpApiGoogleRankSettings:
        if not self.target_domain and not self.host_site_id and not self.host_page_id:
            raise ValueError("rank matching requires a target domain or host binding")
        has_coordinates = self.latitude is not None or self.longitude is not None
        if has_coordinates and (self.latitude is None or self.longitude is None):
            raise ValueError("latitude and longitude must be supplied together")
        location_modes = sum((self.location is not None, self.uule is not None, has_coordinates))
        if location_modes > 1:
            raise ValueError("choose at most one location, uule, or latitude/longitude origin")
        if location_modes == 0 and self.tracked_result_type == "local_pack":
            raise ValueError(
                "local_pack tracking requires a location, uule, or latitude/longitude origin — "
                "a local pack only exists relative to a place"
            )
        # Zero location modes = NATIONAL search (gl/hl only) — the standard
        # country-level Google organic check every rank tracker offers.
        if self.radius_meters is not None:
            maximum = 199 if self.device == "desktop" else 1000
            if not 1 <= self.radius_meters <= maximum:
                raise ValueError(f"radius_meters must be between 1 and {maximum} for {self.device}")
            if self.uule is not None:
                raise ValueError("radius_meters is not supported with uule")
        if self.gl != self.country_code.lower():
            raise ValueError("gl must match country_code for reproducible geo targeting")
        return self

    def api_parameters(self) -> dict[str, str | int]:
        # 🚨 A LOCAL PACK MUST BE **ASKED FOR**, NOT HOPED FOR (2026-08-30).
        # Until this date `local_pack` changed only how the RESPONSE was
        # PARSED: every search went to `engine=google` (the blended web SERP)
        # and the code then looked for a `local_results` block that Google
        # includes only when it happens to render a 3-pack for that query.
        # For any query Google answers with plain web results — every B2B
        # service term, e.g. "it asset disposition" in Irvine — the block is
        # simply absent, so "find local competitors" returned NOTHING and
        # dead-ended the user, while a real map search for the same words
        # returns a full page of businesses. `engine=google_local` is
        # SerpAPI's dedicated Google Local (Maps) endpoint: it returns the
        # local business listing for query + place unconditionally, which is
        # exactly the question "who competes with me HERE" asks.
        if self.tracked_result_type == "local_pack":
            params: dict[str, str | int] = {
                "engine": "google_local",
                "q": self.keyword,
                "google_domain": self.google_domain,
                "gl": self.gl,
                "hl": self.hl,
                "device": self.device,
                "start": self.start,
                "no_cache": str(self.no_cache).lower(),
                "output": "json",
            }
        else:
            params = {
                "engine": "google",
                "q": self.keyword,
                "google_domain": self.google_domain,
                "gl": self.gl,
                "hl": self.hl,
                "device": self.device,
                "safe": self.safe,
                "start": self.start,
                "no_cache": str(self.no_cache).lower(),
                "output": "json",
            }
        if self.location is not None:
            params["location"] = self.location
        elif self.uule is not None:
            params["uule"] = self.uule
        elif self.latitude is not None and self.longitude is not None:
            params["lat"] = str(self.latitude)
            params["lon"] = str(self.longitude)
        # No location mode at all = NATIONAL search (gl/hl only).
        if self.radius_meters is not None:
            params["radius"] = self.radius_meters
        return params


class SerpApiRankJob(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    target_ref: str
    observation_period: str
    settings: SerpApiGoogleRankSettings
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND
    credential_reference_id: str | None = None
    credential_reference_kind: CredentialReferenceKind = CredentialReferenceKind.PLATFORM_SECRET
    request_id: str | None = None

    def to_collection_request(self) -> CollectionRequest:
        return CollectionRequest(
            organization_id=self.organization_id,
            created_by=self.created_by,
            capability=SeoCapability.SERP_RANK,
            operation=SERPAPI_GOOGLE_RANK_OPERATION.name,
            target_ref=self.target_ref,
            observation_period=self.observation_period,
            settings=self.settings.model_dump(mode="json"),
            trigger=self.trigger,
            credential_reference_id=self.credential_reference_id,
            credential_reference_kind=self.credential_reference_kind,
            request_id=self.request_id,
        )


class SerpApiGoogleRankAdapter(SeoProviderAdapter):
    provider = "serpapi"
    capabilities = (SeoCapability.SERP_RANK,)
    operations = (SERPAPI_GOOGLE_RANK_OPERATION,)

    def __init__(
        self,
        *,
        transport: SerpApiHttpTransport | None = None,
        endpoint: str = SERPAPI_SEARCH_ENDPOINT,
        max_concurrency: int = 4,
        min_interval_seconds: float = 0,
        max_attempts: int = 4,
        base_backoff_seconds: float = 0.5,
        estimated_cost_per_search: Decimal | str | int | float | None = None,
        max_retry_delay_seconds: float = 30,
        client: SerpApiClient | None = None,
    ) -> None:
        """Rank collection over the ONE SerpAPI engine.

        `client` lets a host share a single process-wide, paced SerpApiClient
        between rank collection and every other SerpAPI caller — which is what
        keeps ONE monthly allowance behind ONE queue. With none supplied the
        adapter builds its own from these settings.
        """
        self._client = client or SerpApiClient(
            transport=transport,
            endpoint=endpoint,
            max_concurrency=max_concurrency,
            min_interval_seconds=min_interval_seconds,
            max_attempts=max_attempts,
            base_backoff_seconds=base_backoff_seconds,
            max_retry_delay_seconds=max_retry_delay_seconds,
            estimated_cost_per_search=estimated_cost_per_search,
        )
        self._api_key: ContextVar[str | None] = ContextVar(
            f"serpapi_api_key_{id(self)}", default=None
        )

    @property
    def transport(self) -> SerpApiHttpTransport:
        return self._client.transport

    @property
    def endpoint(self) -> str:
        return self._client.endpoint

    @property
    def estimated_cost_per_search(self) -> Decimal | None:
        return self._client.estimated_cost_per_search

    @property
    def max_attempts(self) -> int:
        return self._client.max_attempts

    async def authenticate(self, credential: ResolvedCredential) -> None:
        api_key = credential.values.get("SERPAPI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("SERPAPI_API_KEY credential is required")
        self._api_key.set(api_key)

    async def collect_rank_response(
        self,
        settings: SerpApiGoogleRankSettings,
        credential: ResolvedCredential,
    ) -> ProviderResponse:
        await self.authenticate(credential)
        return await self._collect_rank_response(settings)

    async def collect_response(
        self, request: CollectionRequest, execution: ProviderExecutionContext
    ) -> ProviderResponse:
        del execution
        if request.operation != SERPAPI_GOOGLE_RANK_OPERATION.name:
            raise ValueError(f"unsupported SerpAPI operation {request.operation!r}")
        settings = SerpApiGoogleRankSettings.model_validate(request.settings)
        return await self._collect_rank_response(settings)

    async def _collect_rank_response(
        self,
        settings: SerpApiGoogleRankSettings,
    ) -> ProviderResponse:
        api_key = self._api_key.get()
        if not api_key:
            raise RuntimeError("SerpAPI adapter must be authenticated before collection")
        call = await self._client.search(settings.api_parameters(), api_key=api_key)
        return self._provider_response(call)

    @staticmethod
    def _provider_response(call: SerpApiCall) -> ProviderResponse:
        # request_count carries HTTP attempts, not logical searches: a retried
        # call really did hit SerpAPI more than once, and the allowance is what
        # the budget ceiling is defending.
        return ProviderResponse(
            raw=call.payload,
            fetched_at=call.fetched_at,
            provider_schema_version="google-search-json-v1",
            external_task_id=call.search_id,
            request_count=call.attempts,
            estimated_cost=call.estimated_cost,
            currency="USD",
            call_records=[
                ProviderCallRecord(
                    provider_call_key=f"google-search:{call.search_id}",
                    external_task_id=call.search_id,
                    request_count=call.attempts,
                    estimated_cost=call.estimated_cost,
                    fetched_at=call.fetched_at,
                    metadata={
                        "search_metadata": call.search_metadata,
                        "request_parameters": {
                            key: value
                            for key, value in call.request_parameters.items()
                            if key != "api_key"
                        },
                        "http_attempts": call.attempts,
                        "attempts": call.attempts,
                        "quota_headers": call.quota_headers,
                        "request": call.request_evidence,
                        "response_status": call.status_code,
                    },
                )
            ],
        )

    async def normalize(
        self, response: ProviderResponse, context: NormalizationContext
    ) -> list[SeoObservation]:
        if not isinstance(response.raw, dict):
            raise TypeError("SerpAPI Google response must be an object")
        settings = SerpApiGoogleRankSettings.model_validate(context.request.settings)
        target, target_page_id = await self._resolve_match_target(settings, context)
        identity = await context.resolve_identity(
            SeoIdentityRequest(
                keyword=settings.keyword,
                language=settings.hl,
                target_page_id=target_page_id,
                country_code=settings.country_code,
                region=settings.region,
                city=settings.city,
                postal_code=settings.postal_code,
                latitude=settings.latitude,
                longitude=settings.longitude,
                timezone=settings.timezone,
                engine="google",
                device=settings.device,
                search_type=settings.tracked_result_type,
                target_domain=target.canonical_domain,
                settings=settings.model_dump(mode="json"),
            )
        )
        # DEF-25: a site-less request (no `host_site_id`) resolves no
        # rank_target by design (orm_identity.py) — the collection is
        # observation-only: the SERP snapshot below still persists, but no
        # RankObservation is built against a nonexistent target.
        results, matches = _normalize_results(response.raw, settings, target)
        query_settings = {
            "requested": settings.model_dump(mode="json"),
            "provider_request": settings.api_parameters(),
            "provider_response": _mapping(response.raw.get("search_parameters")),
        }
        features = {key: response.raw[key] for key in _FEATURE_KEYS if key in response.raw}
        snapshot = SerpSnapshotObservation(
            keyword_id=identity.keyword_id,
            rank_target_id=identity.rank_target_id,
            location_id=identity.location_id,
            engine="google",
            language=settings.hl,
            device=settings.device,
            search_type=settings.tracked_result_type,
            observed_at=response.fetched_at,
            query_settings=query_settings,
            serp_features=features,
            results=results,
        )
        observations: list[SeoObservation] = [snapshot]
        locale = f"{settings.hl}-{settings.gl.upper()}"
        tracked_matches = [
            item for item in matches if item[0].result_type == settings.tracked_result_type
        ]
        if identity.rank_target_id is not None and tracked_matches:
            result, match = tracked_matches[0]
            observations.append(
                RankObservation(
                    keyword_id=identity.keyword_id,
                    rank_target_id=identity.rank_target_id,
                    location_id=identity.location_id,
                    engine="google",
                    locale=locale,
                    language=settings.hl,
                    device=settings.device,
                    search_type=settings.tracked_result_type,
                    matched_domain=match.matched_domain,
                    matched_url=match.matched_url,
                    organic_rank=result.organic_rank,
                    absolute_rank=result.absolute_rank,
                    result_type=result.result_type,
                    match_rule=match.match_rule,
                    observed_at=response.fetched_at,
                    query_settings=query_settings,
                    serp_features=features,
                    title=result.title,
                    snippet=result.snippet,
                    extras={
                        **result.extras,
                        "primary_match_policy": "first_provider_order_match",
                        "additional_matching_results": [
                            {
                                "result_type": alternative.result_type,
                                "organic_rank": alternative.organic_rank,
                                "position": alternative.absolute_rank,
                                "url": alternative.url,
                                "match_rule": alternative_match.match_rule,
                            }
                            for alternative, alternative_match in matches
                            if alternative is not result
                        ],
                    },
                )
            )
        return observations

    async def _resolve_match_target(
        self,
        settings: SerpApiGoogleRankSettings,
        context: NormalizationContext,
    ) -> tuple[RankMatchTarget, str | None]:
        domain = settings.target_domain
        page_url = settings.target_page_url
        aliases = list(settings.target_url_aliases)
        page_id: str | None = None
        if settings.host_site_id:
            site = await context.resolve_host_binding(
                HostBindingRequest(resource_kind="web_site", resource_id=settings.host_site_id)
            )
            site_domain = canonicalize_domain(site.canonical_url)
            if domain and domain != site_domain:
                raise ValueError("target_domain conflicts with the canonical host site binding")
            domain = site_domain
        if settings.host_page_id:
            page = await context.resolve_host_binding(
                HostBindingRequest(resource_kind="web_page", resource_id=settings.host_page_id)
            )
            page_domain = canonicalize_domain(page.canonical_url)
            if domain and domain != page_domain:
                raise ValueError("rank target conflicts with the canonical host page binding")
            domain = page_domain
            if page_url and page_url != page.canonical_url:
                aliases.append(page_url)
            page_url = page.canonical_url
            page_id = page.page_id
        if not domain:
            raise ValueError("resolved SerpAPI rank target has no canonical domain")
        return (
            RankMatchTarget(
                canonical_domain=domain,
                canonical_url=page_url,
                url_aliases=tuple(aliases),
                include_subdomains=settings.include_subdomains,
            ),
            page_id,
        )


class SerpApiBatchItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int
    target_ref: str
    receipt: CollectionReceipt | None = None
    error: dict[str, str] | None = None


async def collect_serpapi_rank_batch(
    service: SeoCollectionService,
    adapter: SerpApiGoogleRankAdapter,
    jobs: Sequence[SerpApiRankJob],
    *,
    concurrency: int = 4,
) -> list[SerpApiBatchItem]:
    if concurrency < 1:
        raise ValueError("batch concurrency must be positive")
    semaphore = asyncio.Semaphore(concurrency)

    async def collect_one(index: int, job: SerpApiRankJob) -> SerpApiBatchItem:
        async with semaphore:
            try:
                receipt = await service.collect(adapter, job.to_collection_request())
                return SerpApiBatchItem(
                    index=index,
                    target_ref=job.target_ref,
                    receipt=receipt,
                )
            except Exception as exc:
                return SerpApiBatchItem(
                    index=index,
                    target_ref=job.target_ref,
                    error={"type": type(exc).__name__, "message": str(exc)},
                )

    return list(await asyncio.gather(*(collect_one(index, job) for index, job in enumerate(jobs))))


def _normalize_results(
    payload: dict[str, Any],
    settings: SerpApiGoogleRankSettings,
    target: RankMatchTarget,
) -> tuple[list[SerpResultObservation], list[tuple[SerpResultObservation, RankMatch]]]:
    results: list[SerpResultObservation] = []
    matches: list[tuple[SerpResultObservation, RankMatch]] = []
    for item in _object_list(payload.get("organic_results")):
        position = _positive_int(item.get("position"))
        if position is None:
            continue
        url = _optional_string(item.get("link"))
        result = SerpResultObservation(
            result_type="organic",
            organic_rank=settings.start + position,
            absolute_rank=settings.start + position,
            url=url,
            domain=canonicalize_domain(url or "") or None,
            title=_optional_string(item.get("title")),
            snippet=_optional_string(item.get("snippet")),
            extras={
                "provider_position": position,
                "absolute_rank_semantics": "page_offset_plus_provider_position",
                "displayed_link": item.get("displayed_link"),
                "source": item.get("source"),
                "sitelinks": item.get("sitelinks"),
                "about_this_result": item.get("about_this_result"),
            },
        )
        results.append(result)
        match = match_rank_url(url, target)
        if match:
            matches.append((result, match))

    local = payload.get("local_results")
    local_items = _object_list(_mapping(local).get("places") if isinstance(local, dict) else local)
    for item in local_items:
        position = _positive_int(item.get("position"))
        if position is None:
            continue
        url = _optional_string(item.get("website") or item.get("link"))
        result = SerpResultObservation(
            result_type="local_pack",
            organic_rank=None,
            absolute_rank=position,
            url=url,
            domain=canonicalize_domain(url or "") or None,
            title=_optional_string(item.get("title")),
            snippet=_optional_string(item.get("description")),
            extras={
                **item,
                "position_scope": "local_pack",
                "durable_identity": "provider_place_id_evidence_only",
            },
        )
        results.append(result)
        match = match_rank_url(url, target)
        if match:
            matches.append((result, match))
    return results, matches


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _object_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _positive_int(value: Any) -> int | None:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None




