# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the g2 platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class G2ReviewsInput(TypedDict, total=False):
    """Input for G2 Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of reviews to return. The minimum is 50 because G2 review sources will not serve a smaller page. You are billed per returned result, so a lower limit costs less. Range: 50 to 100. Default: 50."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    product: Required[str]
    """G2 product slug, for example hubspot-marketing-hub. A full G2 product URL is also accepted and reduced to its slug."""
    requireFields: NotRequired[list[Literal["productSlug"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `productSlug`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a review that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sortBy: NotRequired[Literal["recent", "helpful", "highest", "lowest", "default"]]
    """Sort order for the returned reviews: newest first, most helpful first, highest or lowest rated first, or G2's own default ordering. Default: recent."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class G2ReviewsData(BaseModel):
    items: list[G2ReviewsItem] = Field(
        description="G2 reviews for the requested product. Populated whenever the provider has data for the entity."
    )


class G2ReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None,
        description="Reviewer's display name. G2 abbreviates most reviewers, for example Michael D. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_country: str | None = Field(
        default=None,
        alias="authorCountry",
        description="Country the reviewer is based in.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) of when the review was published. On older reviews where G2 records no publication date, it is the date the review was submitted. Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    dislikes: str | None = Field(
        default=None,
        description="The reviewer's answer to G2's question about what they dislike. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    helpful_votes: int | None = Field(
        default=None,
        alias="helpfulVotes",
        description="Number of readers who marked the review helpful.",
    )
    id: str = Field(
        description="G2 identifier for the review. Populated whenever the provider has data for the entity."
    )
    likes: str | None = Field(
        default=None,
        description="The reviewer's answer to G2's question about what they like best. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    market_segment: str | None = Field(
        default=None,
        alias="marketSegment",
        description="G2 market segment of the reviewer's company: Small-Business, Mid-Market, or Enterprise. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    nps: int | None = Field(
        default=None,
        description="Likelihood the reviewer would recommend the product, on a 0 to 10 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    problems_solved: str | None = Field(
        default=None,
        alias="problemsSolved",
        description="The reviewer's answer to G2's question about what problems the product solves and how that benefits them. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_id: str | None = Field(
        default=None,
        alias="productId",
        description="G2's numeric product id, as a string.",
    )
    product_name: str | None = Field(
        default=None,
        alias="productName",
        description="Name of the product the review is about. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_slug: str | None = Field(
        default=None,
        alias="productSlug",
        description="G2 slug of the product the review is about.",
    )
    rating: float = Field(
        description="Star rating the reviewer gave, on a 0.5 to 5 scale in half-star steps. Populated whenever the provider has data for the entity."
    )
    ratings: G2ReviewsRating | None = Field(
        default=None,
        description="G2's rating rubric, each on G2's 1 to 7 scale. A reviewer may skip any of them, and the last two are asked far less often.",
    )
    response_type: str | None = Field(
        default=None,
        alias="responseType",
        description="Form the review was submitted in, for example text or video.",
    )
    review_source: str | None = Field(
        default=None,
        alias="reviewSource",
        description="How G2 collected the review, for example organic or vendor.",
    )
    source_type: str | None = Field(
        default=None,
        alias="sourceType",
        description="How G2 collected the review (e.g. vendor, organic).",
    )
    status: str | None = Field(
        default=None,
        description="Moderation status of the review on G2 (e.g. approved).",
    )
    switched_from: bool | None = Field(
        default=None,
        alias="switchedFrom",
        description="Whether the reviewer switched from another product. Null when G2 does not record an answer.",
    )
    title: str | None = Field(
        default=None,
        description="Headline the reviewer gave the review. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical G2 URL for the review. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class G2ReviewsRating(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ease_of_admin: int | None = Field(
        default=None,
        alias="easeOfAdmin",
        description="Rating for how easy the product is to administer.",
    )
    ease_of_doing_business_with: int | None = Field(
        default=None,
        alias="easeOfDoingBusinessWith",
        description="Rating for how easy the vendor is to do business with.",
    )
    ease_of_setup: int | None = Field(
        default=None,
        alias="easeOfSetup",
        description="Rating for how easy the product is to set up.",
    )
    ease_of_use: int | None = Field(
        default=None,
        alias="easeOfUse",
        description="Rating for how easy the product is to use.",
    )
    meets_requirements: int | None = Field(
        default=None,
        alias="meetsRequirements",
        description="Rating for how well the product meets the reviewer's requirements.",
    )
    quality_of_support: int | None = Field(
        default=None,
        alias="qualityOfSupport",
        description="Rating for the quality of the vendor's support.",
    )


class G2Namespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def reviews(
        self, *, options: RequestOptions | None = None, **input: Unpack[G2ReviewsInput]
    ) -> RunResult[G2ReviewsData]:
        """G2 Reviews

        Pull G2 software reviews for any product: star rating, what reviewers like
        and dislike, problems solved, market segment, and G2's rating rubric as
        clean JSON.

        Price: $0.00016 per request plus $0.00005 per result (maximum $0.00496).

        Example:
            res = client.g2.reviews(limit=50, product="hubspot-marketing-hub", sortBy="recent")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "g2.reviews", dict(input), options
        )
        return RunResult[G2ReviewsData].model_validate(raw)


class AsyncG2Namespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def reviews(
        self, *, options: RequestOptions | None = None, **input: Unpack[G2ReviewsInput]
    ) -> RunResult[G2ReviewsData]:
        """G2 Reviews

        Pull G2 software reviews for any product: star rating, what reviewers like
        and dislike, problems solved, market segment, and G2's rating rubric as
        clean JSON.

        Price: $0.00016 per request plus $0.00005 per result (maximum $0.00496).

        Example:
            res = client.g2.reviews(limit=50, product="hubspot-marketing-hub", sortBy="recent")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "g2.reviews", dict(input), options
        )
        return RunResult[G2ReviewsData].model_validate(raw)
