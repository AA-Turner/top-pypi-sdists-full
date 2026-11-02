# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the capterra platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class CapterraReviewsInput(TypedDict, total=False):
    """Input for Capterra Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of reviews to return. The minimum is 10 because the cheapest Capterra review source will not serve a smaller page. You are billed per returned result, so a lower limit costs less. Range: 10 to 100. Default: 25."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    product: Required[str]
    """Capterra product URL, for example https://www.capterra.com/p/135003/Slack/. Capterra identifies a product by both its numeric id and its slug, so the full URL is required."""
    requireFields: NotRequired[list[Literal["ownerResponse"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `ownerResponse`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a review that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sortBy: NotRequired[Literal["recent", "complete", "highest", "lowest"]]
    """Sort order for the returned reviews: newest first, most complete first, or highest or lowest rated first. Default: recent."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CapterraReviewsData(BaseModel):
    items: list[CapterraReviewsItem] = Field(
        description="Capterra reviews for the requested product. Populated whenever the provider has data for the entity."
    )


class CapterraReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alternatives_considered: list[CapterraReviewsAlternativesConsidered] | None = Field(
        default=None,
        alias="alternativesConsidered",
        description="Products the reviewer evaluated before choosing this one.",
    )
    anonymous: bool | None = Field(
        default=None, description="Whether the reviewer chose to stay anonymous."
    )
    author: str | None = Field(
        default=None,
        description="Reviewer's display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_company_size: str | None = Field(
        default=None,
        alias="authorCompanySize",
        description="Employee-count band of the reviewer's company, for example 11-50 employees. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_industry: str | None = Field(
        default=None,
        alias="authorIndustry",
        description="Industry of the reviewer's company. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_title: str | None = Field(
        default=None,
        alias="authorTitle",
        description="Reviewer's job title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    chosen_reasons: str | None = Field(
        default=None,
        alias="chosenReasons",
        description="The reviewer's stated reason for choosing this product over the alternatives.",
    )
    comments: str | None = Field(
        default=None,
        description="The reviewer's overall comments about using the product. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cons: str | None = Field(
        default=None,
        description="What the reviewer disliked about the product. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    customer_support_rating: float | None = Field(
        default=None,
        alias="customerSupportRating",
        description="Reviewer's customer support rating, on a 1 to 5 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    ease_of_use_rating: float | None = Field(
        default=None,
        alias="easeOfUseRating",
        description="Reviewer's ease of use rating, on a 1 to 5 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    functionality_rating: float | None = Field(
        default=None,
        alias="functionalityRating",
        description="Reviewer's functionality rating, on a 1 to 5 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Capterra identifier for the review. Populated whenever the provider has data for the entity."
    )
    incentivized: bool | None = Field(
        default=None,
        description="Whether the reviewer received an incentive for the review (for example a nominal gift); null when the source does not say. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    owner_response: str | None = Field(
        default=None,
        alias="ownerResponse",
        description="The vendor's public reply to the review.",
    )
    product_url: str | None = Field(
        default=None,
        alias="productUrl",
        description="Canonical Capterra URL for the reviewed product. Capterra has no per-review permalink; anchor to a review with productUrl, then # and the review id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    pros: str | None = Field(
        default=None,
        description="What the reviewer liked about the product. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float = Field(
        description="Overall star rating the reviewer gave, on a 1 to 5 scale. Populated whenever the provider has data for the entity."
    )
    recommendation_score: float | None = Field(
        default=None,
        alias="recommendationScore",
        description="How likely the reviewer is to recommend the product, on a 0 to 10 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    review_source: str | None = Field(
        default=None,
        alias="reviewSource",
        description="Capterra's explanation of how the review was collected and whether any incentive was offered.",
    )
    source_site: str | None = Field(
        default=None,
        alias="sourceSite",
        description="Which site in Capterra's review network the review was written on, for example Capterra, GetApp, or Software Advice. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    switched_from: list[CapterraReviewsSwitchedFrom] | None = Field(
        default=None,
        alias="switchedFrom",
        description="Products the reviewer switched away from to this one.",
    )
    switching_reasons: str | None = Field(
        default=None,
        alias="switchingReasons",
        description="The reviewer's stated reason for switching to this product.",
    )
    time_used_product: str | None = Field(
        default=None,
        alias="timeUsedProduct",
        description="How long the reviewer has used the product, for example 2+ years. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str | None = Field(
        default=None,
        description="Headline the reviewer gave the review. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    validated: bool | None = Field(
        default=None,
        description="Whether Capterra validated the reviewer's identity. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    value_for_money_rating: float | None = Field(
        default=None,
        alias="valueForMoneyRating",
        description="Reviewer's value for money rating, on a 1 to 5 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    verified_linked_in: bool | None = Field(
        default=None,
        alias="verifiedLinkedIn",
        description="Whether the reviewer verified their identity through LinkedIn. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class CapterraReviewsAlternativesConsidered(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = Field(
        default=None, description="Capterra identifier for the alternative product."
    )
    name: str | None = Field(
        default=None, description="Name of the alternative product."
    )
    slug: str | None = Field(
        default=None, description="Capterra slug of the alternative product."
    )


class CapterraReviewsSwitchedFrom(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = Field(
        default=None, description="Capterra identifier for the previous product."
    )
    name: str | None = Field(default=None, description="Name of the previous product.")
    slug: str | None = Field(
        default=None, description="Capterra slug of the previous product."
    )


class CapterraNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CapterraReviewsInput],
    ) -> RunResult[CapterraReviewsData]:
        """Capterra Reviews

        Pull Capterra software reviews for any product: overall and sub-ratings,
        pros and cons, reviewer job title, company size, and industry as clean JSON.

        Price: $0.0055 per request plus $0.00088 per result (maximum $0.0935).

        Example:
            res = client.capterra.reviews(limit=25, product="https://www.capterra.com/p/135003/Slack/", sortBy="recent")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "capterra.reviews", dict(input), options
        )
        return RunResult[CapterraReviewsData].model_validate(raw)


class AsyncCapterraNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CapterraReviewsInput],
    ) -> RunResult[CapterraReviewsData]:
        """Capterra Reviews

        Pull Capterra software reviews for any product: overall and sub-ratings,
        pros and cons, reviewer job title, company size, and industry as clean JSON.

        Price: $0.0055 per request plus $0.00088 per result (maximum $0.0935).

        Example:
            res = client.capterra.reviews(limit=25, product="https://www.capterra.com/p/135003/Slack/", sortBy="recent")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "capterra.reviews", dict(input), options
        )
        return RunResult[CapterraReviewsData].model_validate(raw)
