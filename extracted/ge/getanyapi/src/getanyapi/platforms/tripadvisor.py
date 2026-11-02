# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the tripadvisor platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class TripadvisorReviewsInput(TypedDict, total=False):
    """Input for Tripadvisor Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    languages: NotRequired[list[str]]
    """Only return reviews in these ISO 639-1 languages (e.g. ["en", "es"]); omit for all languages."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    ratings: NotRequired[list[Literal["1", "2", "3", "4", "5"]]]
    """Only return reviews whose bubble rating is in this set (e.g. ["5", "4"] for 4 and 5 star reviews); omit for all ratings."""
    since: NotRequired[str]
    """Only return reviews newer than this date, YYYY-MM-DD or a relative window like '3 months' (e.g. 2026-01-01)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Tripadvisor page URL of the hotel, restaurant, or attraction."""


class TripadvisorSearchInput(TypedDict, total=False):
    """Input for Tripadvisor Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    currency: NotRequired[str]
    """ISO currency code for prices (e.g. USD, EUR). Default: USD."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeAttractions: NotRequired[bool]
    """Include attractions and things to do in the results; set false to exclude them (e.g. false). Defaults to true. Default: true."""
    includeHotels: NotRequired[bool]
    """Include hotels in the results; set false to exclude them (e.g. false). Defaults to true. Default: true."""
    includeRestaurants: NotRequired[bool]
    """Include restaurants in the results; set false to exclude them (e.g. false). Defaults to true. Default: true."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Destination or keyword to search for (e.g. Barcelona)."""
    requireFields: NotRequired[
        list[
            Literal[
                "address",
                "city",
                "country",
                "email",
                "hotelClass",
                "latitude",
                "longitude",
                "phone",
                "postalCode",
                "priceLevel",
                "priceRange",
                "ranking",
                "website",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `phone` or `website`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a place that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TripadvisorReviewsData(BaseModel):
    items: list[TripadvisorReviewsItem] = Field(
        description="Review records for the place: rating, title, review text, publish date, trip type, and reviewer details. Populated whenever the provider has data for the entity."
    )


class TripadvisorReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(default=None, description="Reviewer display name.")
    author_avatar_url: str | None = Field(
        default=None, alias="authorAvatarUrl", description="Reviewer profile photo URL."
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Tripadvisor member identifier of the reviewer.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Tripadvisor profile URL of the reviewer.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether Tripadvisor marks the reviewer as verified.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    helpful_votes: int | None = Field(
        default=None,
        alias="helpfulVotes",
        description="Number of helpful votes the review received.",
    )
    id: str | None = Field(default=None, description="Tripadvisor review identifier.")
    language: str | None = Field(
        default=None, description="Language code the review was written in."
    )
    owner_response_text: str | None = Field(
        default=None,
        alias="ownerResponseText",
        description="Reply the place owner posted to this review.",
    )
    owner_response_utc: float | None = Field(
        default=None,
        alias="ownerResponseUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the owner replied.",
    )
    place_id: str | None = Field(
        default=None,
        alias="placeId",
        description="Tripadvisor location identifier of the reviewed place.",
    )
    place_name: str | None = Field(
        default=None, alias="placeName", description="Name of the reviewed place."
    )
    rating: float = Field(description="Star rating (typically 1-5).")
    stay_utc: float | None = Field(
        default=None,
        alias="stayUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the reviewer stayed or visited.",
    )
    text: str = Field(
        description="Review body text. Populated whenever the provider has data for the entity."
    )
    title: str | None = Field(
        default=None,
        description="Review title or headline. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    trip_type: str | None = Field(
        default=None,
        alias="tripType",
        description="Trip type the reviewer selected (e.g. FAMILY, BUSINESS, COUPLES, NONE).",
    )
    url: str | None = Field(
        default=None,
        description="Canonical review URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class TripadvisorSearchData(BaseModel):
    items: list[TripadvisorSearchItem] = Field(
        description="Matching Tripadvisor place records (hotels, restaurants, attractions). Populated whenever the provider has data for the entity."
    )


class TripadvisorSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Full formatted street address."
    )
    category: str | None = Field(
        default=None,
        description="High-level category (e.g. hotel, restaurant, attraction).",
    )
    city: str | None = Field(default=None, description="City the place is in.")
    country: str | None = Field(default=None, description="Country the place is in.")
    email: str | None = Field(
        default=None, description="Business contact email, when listed."
    )
    hotel_class: str | None = Field(
        default=None,
        alias="hotelClass",
        description="Star rating / hotel class, when applicable.",
    )
    id: str | None = Field(
        default=None,
        description="Tripadvisor location id (stable identifier for the place).",
    )
    image: str | None = Field(default=None, description="Primary place photo URL.")
    latitude: float | None = Field(
        default=None, description="Latitude of the place in decimal degrees."
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the place in decimal degrees."
    )
    phone: str | None = Field(
        default=None, description="Business phone number, when listed."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code of the place."
    )
    price_level: str | None = Field(
        default=None,
        alias="priceLevel",
        description="Relative price level indicator (e.g. $$, $$$$).",
    )
    price_range: str | None = Field(
        default=None,
        alias="priceRange",
        description="Nightly or per-visit price range in the requested currency.",
    )
    ranking: str | None = Field(
        default=None,
        description='Ranking string within its location (e.g. "#2 of 1,885 hotels in Paris").',
    )
    rating: float | None = Field(
        description="Average traveler rating out of 5; null for a place Tripadvisor has not rated (such as a city). Populated whenever the provider has data for the entity."
    )
    review_count: float | None = Field(
        default=None,
        alias="reviewCount",
        description="Total number of traveler reviews; null when the source does not report it.",
    )
    title: str = Field(
        description="Place name. Populated whenever the provider has data for the entity."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Tripadvisor place type (e.g. HOTEL, RESTAURANT, ATTRACTION).",
    )
    url: str = Field(
        description="Canonical Tripadvisor listing page URL. Populated whenever the provider has data for the entity."
    )
    website: str | None = Field(
        default=None, description="The place's own website URL, when listed."
    )


class TripadvisorNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TripadvisorReviewsInput],
    ) -> RunResult[TripadvisorReviewsData]:
        """Tripadvisor Reviews

        Fetch the latest reviews for any Tripadvisor hotel, restaurant, or
        attraction by its page URL: rating, text, date, and trip details as
        normalized JSON.

        Price: $0.003 per request.

        Example:
            res = client.tripadvisor.reviews(limit=3, url="https://www.tripadvisor.com/Hotel_Review-g60763-d93450-Reviews-The_Plaza-New_York_City_New_York.html")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tripadvisor.reviews", dict(input), options
        )
        return RunResult[TripadvisorReviewsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TripadvisorSearchInput],
    ) -> RunResult[TripadvisorSearchData]:
        """Tripadvisor Search

        Search Tripadvisor for hotels, restaurants, and attractions in any
        destination and get rich place records (ratings, review counts, contact
        details, pricing) as normalized JSON.

        Price: $0.003 per request.

        Example:
            res = client.tripadvisor.search(limit=3, query="Paris")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tripadvisor.search", dict(input), options
        )
        return RunResult[TripadvisorSearchData].model_validate(raw)


class AsyncTripadvisorNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TripadvisorReviewsInput],
    ) -> RunResult[TripadvisorReviewsData]:
        """Tripadvisor Reviews

        Fetch the latest reviews for any Tripadvisor hotel, restaurant, or
        attraction by its page URL: rating, text, date, and trip details as
        normalized JSON.

        Price: $0.003 per request.

        Example:
            res = client.tripadvisor.reviews(limit=3, url="https://www.tripadvisor.com/Hotel_Review-g60763-d93450-Reviews-The_Plaza-New_York_City_New_York.html")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tripadvisor.reviews", dict(input), options
        )
        return RunResult[TripadvisorReviewsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TripadvisorSearchInput],
    ) -> RunResult[TripadvisorSearchData]:
        """Tripadvisor Search

        Search Tripadvisor for hotels, restaurants, and attractions in any
        destination and get rich place records (ratings, review counts, contact
        details, pricing) as normalized JSON.

        Price: $0.003 per request.

        Example:
            res = client.tripadvisor.search(limit=3, query="Paris")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tripadvisor.search", dict(input), options
        )
        return RunResult[TripadvisorSearchData].model_validate(raw)
