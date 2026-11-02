"""Customer-safe discovery models shared by the handwritten SDK methods."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class FlatPricingOffer(BaseModel):
    """A fixed, per-request discovery offer."""

    model_config = ConfigDict(
        extra="ignore", strict=True, populate_by_name=True, allow_inf_nan=False
    )

    model: Literal["flat"]
    unit: Literal["request"]
    #: USD billed for ONE request.
    max_usd: float = Field(alias="maxUsd", ge=0)
    #: The same maximum quoted per 1,000 requests, read from the gateway as published.
    max_per1k_usd: float = Field(alias="maxPer1kUsd", ge=0)


class LinearPricingOffer(BaseModel):
    """A capped base-plus-unit discovery offer."""

    model_config = ConfigDict(
        extra="ignore", strict=True, populate_by_name=True, allow_inf_nan=False
    )

    model: Literal["linear"]
    unit: str = Field(min_length=1)
    base_usd: float = Field(alias="baseUsd", ge=0)
    per_unit_usd: float = Field(alias="perUnitUsd", ge=0)
    #: USD billed for ONE request at the cap.
    max_usd: float = Field(alias="maxUsd", ge=0)
    #: The same maximum quoted per 1,000 requests, read from the gateway as published.
    max_per1k_usd: float = Field(alias="maxPer1kUsd", ge=0)


PricingOffer = Annotated[
    FlatPricingOffer | LinearPricingOffer, Field(discriminator="model")
]


class DiscoveryPricing(BaseModel):
    model_config = ConfigDict(
        extra="ignore", strict=True, populate_by_name=True, allow_inf_nan=False
    )

    from_offer: PricingOffer = Field(alias="from")
    failover_max_usd: float = Field(alias="failoverMaxUsd", ge=0)
    #: The failover ceiling per 1,000 requests, read from the gateway as published.
    failover_max_per1k_usd: float = Field(alias="failoverMaxPer1kUsd", ge=0)


class DiscoveryExecution(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)

    mode: Literal["sync", "durable"]


class DiscoverySource(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)

    id: str
    name: str
    kind: Literal["anonymous", "brand"]
    artwork_key: str = Field(alias="artworkKey")


class LaneHealth(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)

    window: str
    uptime_pct: float = Field(alias="uptimePct", ge=0, le=100)
    latency_p50_ms: int = Field(alias="latencyP50Ms", ge=0)
    uptime_sample: int = Field(alias="uptimeSample", ge=0)
    latency_sample: int = Field(alias="latencySample", ge=0)
    requests: int = Field(ge=0)
    served_requests: int = Field(alias="servedRequests", ge=0)


class DiscoveryLane(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)

    pricing: PricingOffer
    source: DiscoverySource
    health: LaneHealth | None = None


class DiscoveryLatency(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)

    window: str
    p50_ms: int = Field(alias="p50Ms", ge=0)
    p95_ms: int = Field(alias="p95Ms", ge=0)
    p99_ms: int = Field(alias="p99Ms", ge=0)
    sample: int = Field(ge=1)
    basis: Literal["service_time_excludes_caller_requested_delay"]


class CatalogEntry(BaseModel):
    """One customer-safe API returned by ``catalog`` or ``describe``."""

    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)

    id: str
    slug: str
    name: str
    category: str
    description: str
    method: Literal["POST"]
    path: str = Field(min_length=2, pattern=r"^/[^/]")
    execution: DiscoveryExecution
    provider: Literal["AnyAPI"]
    pricing: DiscoveryPricing
    lanes: list[DiscoveryLane]
    heavy: bool = False
    try_eligible: bool = Field(alias="tryEligible")
    try_max_items: int | None = Field(default=None, alias="tryMaxItems", ge=1)
    failover: bool | None = None
    excludes_caller_delay: bool | None = Field(
        default=None, alias="excludesCallerDelay"
    )
    input_schema: dict[str, Any] | None = Field(default=None, alias="inputSchema")
    output_schema: dict[str, Any] | None = Field(default=None, alias="outputSchema")
    latency: DiscoveryLatency | None = None


class HighlightField(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)

    path: str
    type: str
    why: str | None = None


class CatalogSearchResult(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)

    slug: str
    platform_id: str = Field(alias="platformId")
    name: str
    description: str
    category: str
    method: Literal["POST"]
    path: str = Field(min_length=2, pattern=r"^/[^/]")
    execution: DiscoveryExecution
    provider: Literal["AnyAPI"]
    pricing: DiscoveryPricing
    try_max_items: int | None = Field(default=None, alias="tryMaxItems", ge=1)
    failover: bool
    excludes_caller_delay: bool | None = Field(
        default=None, alias="excludesCallerDelay"
    )
    relevance: float = Field(gt=0, le=1)
    highlight_fields: list[HighlightField] | None = Field(
        default=None, alias="highlightFields"
    )


class CatalogSearchResults(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)

    results: list[CatalogSearchResult]
    total: int = Field(ge=0)
    ranking: Literal["semantic", "keyword"]
