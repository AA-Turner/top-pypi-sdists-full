from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class SeoCapability(StrEnum):
    SERP_RANK = "serp_rank"
    KEYWORD_METRICS = "keyword_metrics"
    SEARCH_PERFORMANCE = "search_performance"
    WEB_ANALYTICS = "web_analytics"
    PAGE_PERFORMANCE = "page_performance"
    BACKLINKS = "backlinks"
    COMPETITORS = "competitors"
    RAW_PROVIDER = "raw_provider"


class CollectionTrigger(StrEnum):
    SCHEDULED = "scheduled"
    ON_DEMAND = "on_demand"
    BACKFILL = "backfill"
    TEST = "test"


class CredentialReferenceKind(StrEnum):
    PLATFORM_SECRET = "platform_secret"
    INTEGRATION_CONNECTION = "integration_connection"


class CollectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    capability: SeoCapability
    operation: str
    target_ref: str
    site_id: str | None = None
    page_id: str | None = None
    source_crawl_session_id: str | None = None
    observation_period: str
    settings: dict[str, Any] = Field(default_factory=dict)
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND
    credential_reference_id: str | None = None
    credential_reference_kind: CredentialReferenceKind = CredentialReferenceKind.PLATFORM_SECRET
    credential_keys: tuple[str, ...] = ()
    request_id: str | None = None
    execution_id: UUID | None = None
    resume_existing: bool = False
    force_refresh: bool = False
    #: The ``billing.spend_approval`` this collection spends under (OPENSEO-TOOLS-SPEC
    #: §6.1.7). It travels OUT OF BAND: never inside ``settings`` (which is hashed
    #: for reuse and, for DataForSEO, ``extra="forbid"``), and excluded from every
    #: reuse/idempotency hash, so the same request under two approvals is one reuse
    #: hit. Checked after the fresh-run lookup and before ``start_run``.
    spend_approval_id: UUID | None = None
    #: The job asking to spend: the agent tool and action that built this
    #: collection. Out of band exactly like ``spend_approval_id`` (never in
    #: ``settings``, never hashed), and required whenever an approval is passed:
    #: an approval funds only the tool + action the person approved.
    spend_tool: str | None = None
    spend_action: str | None = None

    @field_validator("operation", mode="before")
    @classmethod
    def normalize_operation(cls, value: Any) -> str:
        normalized = str(value).strip()
        if not normalized:
            raise ValueError("SEO collections require a nonblank operation")
        return normalized

    @model_validator(mode="after")
    def require_execution_for_resume(self) -> CollectionRequest:
        if self.resume_existing and not self.execution_id:
            raise ValueError("resume_existing requires a stable execution_id")
        if self.page_id and not self.site_id:
            raise ValueError("page_id requires site_id")
        if self.source_crawl_session_id and not self.site_id:
            raise ValueError("source_crawl_session_id requires site_id")
        self._require_settings_attribution_agrees()
        return self

    def _require_settings_attribution_agrees(self) -> None:
        """DEF-18 guard: ``site_id``/``page_id`` are the ONE canonical attribution
        authority. Provider settings dicts commonly duplicate a host identifier
        (``host_site_id`` / ``host_page_id``) for the adapter's own binding
        resolution — that duplication is fine, but it must never disagree with
        the canonical fields. A contradictory request fails HERE, at
        construction, before any cache lookup, credential resolution, or
        provider call."""
        settings_site_id = self.settings.get("host_site_id")
        if (
            self.site_id is not None
            and isinstance(settings_site_id, str)
            and settings_site_id
            and settings_site_id != self.site_id
        ):
            raise ValueError(
                f"CollectionRequest.site_id ({self.site_id!r}) contradicts "
                f"settings.host_site_id ({settings_site_id!r}); site_id is the one "
                "canonical attribution authority — fix the request builder"
            )
        settings_page_id = self.settings.get("host_page_id")
        if (
            self.page_id is not None
            and isinstance(settings_page_id, str)
            and settings_page_id
            and settings_page_id != self.page_id
        ):
            raise ValueError(
                f"CollectionRequest.page_id ({self.page_id!r}) contradicts "
                f"settings.host_page_id ({settings_page_id!r}); page_id is the one "
                "canonical attribution authority — fix the request builder"
            )


class ResolvedCredential(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_id: str | None = None
    reference_kind: CredentialReferenceKind | None = None
    values: dict[str, str]
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProviderCallRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider_call_key: str
    external_task_id: str | None = None
    request_count: int = 1
    reported_cost: Decimal | None = None
    estimated_cost: Decimal | None = None
    currency: str = "USD"
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("provider_call_key")
    @classmethod
    def require_call_key(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider_call_key must be nonblank")
        return normalized

    @field_validator("request_count")
    @classmethod
    def require_request_count(cls, value: int) -> int:
        if value < 0:
            raise ValueError("request_count cannot be negative")
        return value

    @field_validator("reported_cost", "estimated_cost")
    @classmethod
    def require_nonnegative_cost(cls, value: Decimal | None) -> Decimal | None:
        if value is not None and value < 0:
            raise ValueError("provider call cost cannot be negative")
        return value

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 3:
            raise ValueError("currency must be a three-letter code")
        return normalized


class ProviderResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw: dict[str, Any] | list[Any]
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    provider_schema_version: str | None = None
    external_task_id: str | None = None
    request_count: int = 1
    reported_cost: Decimal | None = None
    estimated_cost: Decimal | None = None
    currency: str = "USD"
    call_records: list[ProviderCallRecord] = Field(default_factory=list)
    error: dict[str, Any] | None = None

    @model_validator(mode="after")
    def derive_call_aggregates(self) -> ProviderResponse:
        if not self.call_records:
            return self
        call_keys = [record.provider_call_key for record in self.call_records]
        if len(call_keys) != len(set(call_keys)):
            raise ValueError("provider call records must have unique call keys")
        currencies = {record.currency for record in self.call_records}
        if len(currencies) != 1:
            raise ValueError("provider call records must use one currency")
        self.request_count = sum(record.request_count for record in self.call_records)
        reported = [record.reported_cost for record in self.call_records]
        estimated = [record.estimated_cost for record in self.call_records]
        self.reported_cost = (
            sum((cost for cost in reported if cost is not None), Decimal(0))
            if all(cost is not None for cost in reported)
            else None
        )
        self.estimated_cost = (
            sum((cost for cost in estimated if cost is not None), Decimal(0))
            if all(cost is not None for cost in estimated)
            else None
        )
        self.currency = next(iter(currencies))
        return self


class StoredPayloadReceipt(BaseModel):
    cloud_file_id: str
    checksum: str
    size_bytes: int
    content_type: str = "application/json"


class RawPayloadEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] | list[Any] | None = None
    cloud_file_id: str | None = None
    checksum: str
    size_bytes: int
    content_type: str = "application/json"
    offload_error: dict[str, str] | None = None


class ProviderTaskCheckpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    external_task_id: str
    endpoint: str | None = None
    status: Literal["submitted", "polling", "completed", "failed", "cancelled"]
    request_payload: dict[str, Any] = Field(default_factory=dict)
    response_payload: dict[str, Any] | list[Any] | None = None
    request_count: int = 1
    provider_cost: Decimal | None = None
    estimated_cost: Decimal | None = None
    currency: str = "USD"
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_polled_at: datetime | None = None
    completed_at: datetime | None = None
    error: dict[str, Any] | None = None


class RankObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["rank"] = "rank"
    keyword_id: str
    rank_target_id: str
    location_id: str | None = None
    engine: str
    locale: str
    language: str = "en"
    device: str = "desktop"
    search_type: str = "organic"
    matched_domain: str | None = None
    matched_url: str | None = None
    organic_rank: int | None = None
    absolute_rank: int | None = None
    result_type: str = "organic"
    match_rule: str = "domain"
    observed_at: datetime
    query_settings: dict[str, Any] = Field(default_factory=dict)
    serp_features: dict[str, Any] = Field(default_factory=dict)
    title: str | None = None
    snippet: str | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class SerpResultObservation(BaseModel):
    result_type: str = "organic"
    organic_rank: int | None = None
    absolute_rank: int
    url: str | None = None
    domain: str | None = None
    title: str | None = None
    snippet: str | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class SerpSnapshotObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["serp_snapshot"] = "serp_snapshot"
    keyword_id: str
    rank_target_id: str | None = None
    location_id: str | None = None
    engine: str
    language: str = "en"
    device: str = "desktop"
    search_type: str = "organic"
    observed_at: datetime
    query_settings: dict[str, Any] = Field(default_factory=dict)
    serp_features: dict[str, Any] = Field(default_factory=dict)
    results: list[SerpResultObservation] = Field(default_factory=list)


class MonthlySearch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    year: int
    month: int
    search_volume: int


class KeywordMarketObservation(BaseModel):
    """One provider result element for one (keyword, location_code) —
    persisted as a ``seo.keyword_market`` upsert (merge, never append).
    ``location_code`` is the provider/Google Ads integer (US = 2840), NEVER a
    ``seo.location`` uuid. Provider ``intent`` is deliberately absent — the
    classifier owns intent (``seo.keyword_facet`` ``intent_class``); provider
    intent stays as evidence in ``raw``. Provider ``difficulty`` is NOT a
    classification: it is a provider-scored property of the (keyword, market)
    pair like ``competition_index``, so it has typed columns
    (``seo.keyword_market.difficulty*``). ``raw`` is overwritten by whichever
    provider wrote last, so difficulty kept only there would vanish at the next
    Google Ads volume refresh. ``None`` means "this observation did not score
    difficulty" and never clears a stored value (OPENSEO-TOOLS-SPEC §4.1)."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["keyword_market"] = "keyword_market"
    keyword_id: str
    location_code: int
    search_volume: int | None = None
    competition: str | None = None
    competition_index: int | None = None
    cpc: Decimal | None = None
    low_top_of_page_bid: Decimal | None = None
    high_top_of_page_bid: Decimal | None = None
    monthly_searches: list[MonthlySearch] = Field(default_factory=list)
    metrics_task_id: str | None = None
    #: Provider keyword difficulty, 0-100. Written to the projection only when
    #: set, under its own newer-or-equal guard (``difficulty_observed_at``).
    difficulty: int | None = Field(default=None, ge=0, le=100)
    raw: dict[str, Any] = Field(default_factory=dict)
    observed_at: datetime


class SearchPerformanceObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["search_performance"] = "search_performance"
    site_id: str
    page_id: str | None = None
    keyword_id: str | None = None
    date: date
    query: str | None = None
    country: str | None = None
    device: str | None = None
    dimension_profile: str = "default"
    search_appearance: str | None = None
    clicks: int = 0
    impressions: int = 0
    ctr: Decimal | None = None
    average_position: Decimal | None = None
    extras: dict[str, Any] = Field(default_factory=dict)

    @field_validator("dimension_profile")
    @classmethod
    def require_dimension_profile(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("search performance dimension_profile must be nonblank")
        return normalized


class WebAnalyticsObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["web_analytics"] = "web_analytics"
    site_id: str
    page_id: str | None = None
    date: date
    source: str | None = None
    medium: str | None = None
    channel: str | None = None
    campaign: str | None = None
    device: str | None = None
    landing_page: str | None = None
    currency_code: str | None = None
    property_timezone: str | None = None
    sessions: int = 0
    users: int = 0
    engaged_sessions: int = 0
    views: int = 0
    engagement_rate: Decimal | None = Field(default=None, ge=0, le=1)
    key_events: Decimal = Field(default=Decimal(0), ge=0)
    conversions: Decimal = Decimal(0)
    revenue: Decimal | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class PagePerformanceObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["page_performance"] = "page_performance"
    page_id: str
    site_id: str | None = None
    strategy: Literal["desktop", "mobile"]
    performance_score: Decimal | None = None
    accessibility_score: Decimal | None = None
    best_practices_score: Decimal | None = None
    seo_score: Decimal | None = None
    lighthouse: dict[str, Any] = Field(default_factory=dict)
    crux: dict[str, Any] = Field(default_factory=dict)
    diagnostics: dict[str, Any] = Field(default_factory=dict)
    observed_at: datetime


class BacklinkItem(BaseModel):
    source_url: str
    source_domain: str | None = None
    target_url: str
    anchor_text: str | None = None
    link_type: str | None = None
    is_dofollow: bool | None = None
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    lost_at: datetime | None = None
    state: Literal["active", "new", "lost"] = "active"
    source_rank: Decimal | None = None
    domain_rank: Decimal | None = None
    spam_score: Decimal | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class BacklinkDimensionItem(BaseModel):
    dimension_kind: Literal["referring_domain", "anchor", "target_page", "competitor_domain"]
    dimension_key: str
    label: str | None = None
    url: str | None = None
    backlinks: int | None = None
    referring_domains: int | None = None
    rank_score: Decimal | None = None
    spam_score: Decimal | None = None
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class BacklinkSnapshotObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["backlink_snapshot"] = "backlink_snapshot"
    site_id: str
    page_id: str | None = None
    dataset: str = "summary"
    target: str
    target_type: Literal["domain", "url"] = "domain"
    total_backlinks: int | None = None
    referring_domains: int | None = None
    referring_ips: int | None = None
    referring_subnets: int | None = None
    dofollow_backlinks: int | None = None
    nofollow_backlinks: int | None = None
    new_backlinks: int | None = None
    lost_backlinks: int | None = None
    broken_backlinks: int | None = None
    rank_score: Decimal | None = None
    spam_score: Decimal | None = None
    observed_at: datetime
    backlinks: list[BacklinkItem] = Field(default_factory=list)
    dimensions: list[BacklinkDimensionItem] = Field(default_factory=list)
    extras: dict[str, Any] = Field(default_factory=dict)

    @field_validator("dataset", "target")
    @classmethod
    def require_nonblank_backlink_identity(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("backlink dataset and target must be nonblank")
        return normalized


class CompetitorObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["competitor"] = "competitor"
    competitor_domain: str
    competitor_url: str | None = None
    organic_keywords: int | None = None
    traffic_estimate: Decimal | None = None
    intersections: dict[str, Any] = Field(default_factory=dict)
    observed_at: datetime
    extras: dict[str, Any] = Field(default_factory=dict)


class LinkGapMatchItem(BaseModel):
    """One (gap domain → competitor) link relationship.

    ``source_url`` is deliberately optional and is ALWAYS ``None`` from
    ``/v3/backlinks/domain_intersection/live``: that endpoint reports per-target
    aggregates (``referring_pages`` counts), never the individual linking page.
    "From what page" needs a second, per-domain call — see FEATURE.md.
    """

    model_config = ConfigDict(extra="forbid")

    competitor_domain: str
    source_url: str | None = None
    target_url: str | None = None
    backlinks: int | None = None
    referring_pages: int | None = None
    domain_rank: Decimal | None = None
    spam_score: Decimal | None = None
    is_dofollow: bool | None = None
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    lost_at: datetime | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class LinkGapDomainItem(BaseModel):
    """A domain that links to competitors and not to us.

    ``match_count`` is the industry's primary sort — Semrush calls it "Matches",
    Ahrefs the intersect count. It is the provider's ``intersections_count``,
    not a value we compute, so it cannot drift from the evidence.
    """

    model_config = ConfigDict(extra="forbid")

    normalized_domain: str
    display_domain: str
    match_count: int
    domain_rank: Decimal | None = None
    spam_score: Decimal | None = None
    total_backlinks: int | None = None
    referring_domains: int | None = None
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    matches: list[LinkGapMatchItem] = Field(default_factory=list)
    extras: dict[str, Any] = Field(default_factory=dict)


class LinkGapObservation(BaseModel):
    """The result of asking "who links to my competitors but not to me".

    ``excluded_targets`` records the domains the provider was told to subtract —
    normally our own site. Without it a stored observation cannot be read back
    honestly, because "gap" is meaningless without knowing the gap FROM what.
    """

    model_config = ConfigDict(extra="forbid")

    kind: Literal["link_gap"] = "link_gap"
    site_id: str
    competitor_targets: dict[str, str]
    excluded_targets: list[str] = Field(default_factory=list)
    total_available: int | None = None
    observed_at: datetime
    domains: list[LinkGapDomainItem] = Field(default_factory=list)
    extras: dict[str, Any] = Field(default_factory=dict)


class SerpProspectMentionItem(BaseModel):
    """One SERP appearance of a prospect domain — the evidence row.

    ``query`` is the literal string sent to the engine, operators included, and
    is deliberately TEXT — prospecting queries never mint universal
    ``seo.keyword`` rows (an operator string is not a keyword; see
    ``serp_prospecting.py``'s module docstring).
    """

    model_config = ConfigDict(extra="forbid")

    query: str
    variant: str
    seed_keyword: str | None = None
    url: str
    title: str | None = None
    snippet: str | None = None
    rank: int | None = None
    result_type: str = "organic"
    extras: dict[str, Any] = Field(default_factory=dict)


class SerpProspectDomainItem(BaseModel):
    """A domain that ranks for the campaign's prospecting queries."""

    model_config = ConfigDict(extra="forbid")

    normalized_domain: str
    display_domain: str
    mention_count: int
    best_rank: int | None = None
    variants: list[str] = Field(default_factory=list)
    mentions: list[SerpProspectMentionItem] = Field(default_factory=list)
    extras: dict[str, Any] = Field(default_factory=dict)


class SerpProspectObservation(BaseModel):
    """The result of SERP/keyword prospecting: who ranks for these queries.

    The SERP twin of :class:`LinkGapObservation` — one observation per run,
    aggregated by registrable domain, persisted into ``seo.serp_opportunity`` /
    ``seo.serp_mention``. ``excluded_domains`` records what was subtracted
    (normally our own site), for the same honesty reason the link gap records
    ``excluded_targets``.
    """

    model_config = ConfigDict(extra="forbid")

    kind: Literal["serp_prospect"] = "serp_prospect"
    site_id: str
    queries: list[str] = Field(default_factory=list)
    excluded_domains: list[str] = Field(default_factory=list)
    observed_at: datetime
    domains: list[SerpProspectDomainItem] = Field(default_factory=list)
    extras: dict[str, Any] = Field(default_factory=dict)


SeoObservation = Annotated[
    SerpSnapshotObservation
    | RankObservation
    | KeywordMarketObservation
    | SearchPerformanceObservation
    | WebAnalyticsObservation
    | PagePerformanceObservation
    | BacklinkSnapshotObservation
    | CompetitorObservation
    | LinkGapObservation
    | SerpProspectObservation,
    Field(discriminator="kind"),
]


class CollectionRun(BaseModel):
    id: str
    provider: str
    request: CollectionRequest
    settings_hash: str
    idempotency_key: str
    status: str
    created: bool
    claimed: bool = True
    lease_owner: str | None = None
    lease_expires_at: datetime | None = None
    attempt_count: int = 1


class SeoIdentityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    keyword: str
    language: str = "en"
    target_page_id: str | None = None
    country_code: str | None = None
    region: str | None = None
    city: str | None = None
    postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    timezone: str | None = None
    engine: str | None = None
    device: str = "desktop"
    search_type: str = "organic"
    target_domain: str | None = None
    settings: dict[str, Any] = Field(default_factory=dict)


class ResolvedSeoIdentity(BaseModel):
    keyword_id: str
    location_id: str | None = None
    rank_target_id: str | None = None


class HostBindingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resource_kind: Literal["web_site", "web_page"]
    resource_id: str


class ResolvedHostBinding(BaseModel):
    site_id: str
    page_id: str | None = None
    canonical_url: str


class NormalizationContext(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    request: CollectionRequest
    run: CollectionRun
    raw_payload_id: str
    identity_resolver: Any = Field(exclude=True)
    host_binding_resolver: Any = Field(exclude=True)

    async def resolve_identity(self, identity: SeoIdentityRequest) -> ResolvedSeoIdentity:
        return await self.identity_resolver.resolve(self.request, identity)

    async def resolve_identities(
        self, identities: list[SeoIdentityRequest]
    ) -> list[ResolvedSeoIdentity]:
        return await self.identity_resolver.resolve_many(self.request, identities)

    async def resolve_host_binding(self, binding: HostBindingRequest) -> ResolvedHostBinding:
        return await self.host_binding_resolver.resolve(self.request, binding)


class RawPayloadReceipt(BaseModel):
    id: str
    checksum: str
    created: bool


class UpsertReceipt(BaseModel):
    created: int = 0
    existing: int = 0
    observation_ids: list[str] = Field(default_factory=list)


class CollectionReceipt(BaseModel):
    run_id: str
    raw_payload_id: str | None = None
    created_observations: int = 0
    existing_observations: int = 0
    reused_completed_run: bool = False
    from_cache: bool = False
    cache_age_seconds: int | None = None
    freshness_ttl_seconds: int | None = None


class SpendQuery(BaseModel):
    """One spend-aggregation slice — every field left ``None`` widens the
    scope (``organization_id=None`` = every organization, i.e. the global
    platform total). Used identically by the in-memory and ORM repositories
    so budget enforcement behaves the same in tests and production."""

    model_config = ConfigDict(extra="forbid")

    organization_id: str | None = None
    provider: str | None = None
    created_by: str | None = None
    period_start: datetime
    period_end: datetime


class SpendSummary(BaseModel):
    """What one slice of provider spend cost, and how much of it is *known*.

    🚨 NULL is unmeasured, never zero. A run that carries no cost evidence at
    all is counted in :attr:`unpriced_run_count`, never folded into
    :attr:`effective_cost` as ``$0.00`` — that coalesce is what let 112 live
    SerpAPI runs spend nothing against every ceiling. A run that *reported*
    ``0.00`` (Search Console, Bing Webmaster, PageSpeed, our own crawl) has
    evidence and is genuinely free."""

    model_config = ConfigDict(extra="forbid")

    query: SpendQuery
    reported_cost: Decimal = Decimal(0)
    estimated_cost: Decimal = Decimal(0)
    # effective_cost = sum over runs that HAVE cost evidence of
    # COALESCE(reported, estimated) — the conservative "what we believe we
    # spent" figure. Never reported_cost + estimated_cost (that double-counts a
    # run that has both), and never a coalesce of an absent cost to zero.
    effective_cost: Decimal = Decimal(0)
    #: Runs in this slice with NULL in BOTH cost columns. Real spend nobody
    #: measured; ``matrx_seo.budget`` charges each one the
    #: ``seo.unpriced_run_assumed_cost_usd`` knob before comparing to a ceiling.
    unpriced_run_count: int = 0
    run_count: int = 0

    @property
    def has_unmeasured_spend(self) -> bool:
        """True when this figure understates reality. A surface rendering
        ``effective_cost`` without saying so is reporting a confident number it
        does not have."""
        return self.unpriced_run_count > 0


class CollectionInProgressError(RuntimeError):
    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        super().__init__(f"SEO collection run {run_id} is already processing")


@dataclass(frozen=True)
class _ProviderResponseErrorInfo:
    error_type: str
    message: str
    user_message: str
    code: str
    details: dict[str, Any]
    status_code: int = 502


def _provider_response_error_message(error: dict[str, Any]) -> str:
    summary = str(error.get("message") or "SEO provider response failed")
    failures = error.get("failures")
    if not isinstance(failures, list):
        return summary
    for failure in failures:
        if not isinstance(failure, dict):
            continue
        detail = failure.get("message")
        if isinstance(detail, str) and detail.strip() and detail.strip() != summary:
            return f"{summary}: {detail.strip()}"
    return summary


class ProviderResponseError(RuntimeError):
    def __init__(self, error: dict[str, Any], *, run_id: str | None = None) -> None:
        self.error = error
        self.run_id = run_id
        message = _provider_response_error_message(error)
        code = str(error.get("type") or "ProviderResponseError")
        self.error_info = _ProviderResponseErrorInfo(
            error_type="seo_provider_response_error",
            message=message,
            user_message=message,
            code=code,
            details=error,
        )
        super().__init__(message)
