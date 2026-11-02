# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the trustpilot platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class TrustpilotReviewsInput(TypedDict, total=False):
    """Input for Trustpilot Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    company: Required[str]
    """Brand name or Trustpilot review-page URL to fetch reviews for (e.g. nike or https://www.trustpilot.com/review/nike.com)."""
    countries: NotRequired[list[str]]
    """Only return reviews from reviewers in these ISO 3166-1 alpha-2 countries (e.g. ["US", "GB"]). Omit this field for all countries and to stay on the cheapest price; a country filter routes to the dearest source."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    languages: NotRequired[list[str]]
    """Only return reviews in these ISO 639-1 languages (e.g. ["en", "de"]). Omit this field for all languages and to stay on the cheapest price; a language filter routes to the dearest source."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-200, default 200). Trustpilot serves at most 200 reviews per company. Range: 1 to 200. Default: 200."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["avatarUrl"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `avatarUrl`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a review whose reviewer has no photo."""
    sortBy: NotRequired[Literal["auto", "relevancy", "recent"]]
    """Review ordering: auto, relevancy, or recent (e.g. recent). Default: auto."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    stars: NotRequired[str]
    """Limit reviews to a single star rating from 1 to 5 (e.g. 5)."""
    startDate: NotRequired[str]
    """Only return reviews on or after this date, inclusive, in YYYY-MM-DD format (e.g. 2026-01-01). Omit this field to stay on the cheapest price; a date floor routes to the dearest source."""
    verifiedOnly: NotRequired[bool]
    """Set true to return only verified reviews (e.g. true). Omit this field, or send false, to stay on the cheapest price; true routes to a dearer source. Default: false."""


class TrustpilotReviewsData(BaseModel):
    items: list[TrustpilotReviewsItem] = Field(
        description="Review records: star rating, review title and text, date, reviewer name and country, and company reply when present. Populated whenever the provider has data for the entity."
    )


class TrustpilotReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None, description="Display name of the reviewer."
    )
    author_country: str | None = Field(
        default=None,
        alias="authorCountry",
        description="Two-letter country code of the reviewer.",
    )
    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="URL of the reviewer's avatar image, or null when the reviewer has no photo.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    language: str | None = Field(
        default=None, description="Language code of the review text, e.g. en."
    )
    owner_response_text: str | None = Field(
        default=None,
        alias="ownerResponseText",
        description="The company's public reply to the review. Absent when the company has not replied.",
    )
    owner_response_utc: float | None = Field(
        default=None,
        alias="ownerResponseUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the company replied; absent when it has not.",
    )
    rating: float = Field(description="Star rating (1-5).")
    reviewer_reviews_count: int | None = Field(
        default=None,
        alias="reviewerReviewsCount",
        description="Number of reviews the reviewer has written on Trustpilot.",
    )
    text: str = Field(
        description="Review body text. Populated whenever the provider has data for the entity."
    )
    title: str | None = Field(
        default=None,
        description="Review title or headline. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical review URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    verified: bool | None = Field(
        default=None, description="Whether the reviewer is verified."
    )


class TrustpilotNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TrustpilotReviewsInput],
    ) -> RunResult[TrustpilotReviewsData]:
        """Trustpilot Reviews

        Pull Trustpilot reviews for any company by brand name: star ratings, review
        text, dates, and reviewer details as clean JSON.

        Price: $0.0008 per request.

        Example:
            res = client.trustpilot.reviews(company="stripe.com", limit=3)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "trustpilot.reviews", dict(input), options
        )
        return RunResult[TrustpilotReviewsData].model_validate(raw)


class AsyncTrustpilotNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TrustpilotReviewsInput],
    ) -> RunResult[TrustpilotReviewsData]:
        """Trustpilot Reviews

        Pull Trustpilot reviews for any company by brand name: star ratings, review
        text, dates, and reviewer details as clean JSON.

        Price: $0.0008 per request.

        Example:
            res = client.trustpilot.reviews(company="stripe.com", limit=3)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "trustpilot.reviews", dict(input), options
        )
        return RunResult[TrustpilotReviewsData].model_validate(raw)
