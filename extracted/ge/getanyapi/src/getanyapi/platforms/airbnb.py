# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the airbnb platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class AirbnbSearchInput(TypedDict, total=False):
    """Input for Airbnb Search."""

    adults: NotRequired[int]
    """Number of adult guests (e.g. 2). Minimum: 1."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    checkIn: NotRequired[str]
    """Check-in date in YYYY-MM-DD format (e.g. 2026-07-01)."""
    checkOut: NotRequired[str]
    """Check-out date in YYYY-MM-DD format (e.g. 2026-07-05)."""
    children: NotRequired[int]
    """Number of child guests (e.g. 1). Minimum: 0."""
    currency: NotRequired[
        Literal[
            "USD",
            "CZK",
            "AUD",
            "BRL",
            "BGN",
            "CAD",
            "CLP",
            "CNY",
            "COP",
            "CRC",
            "HRK",
            "DKK",
            "EGP",
            "AED",
            "EUR",
            "GHS",
            "HKD",
            "HUF",
            "INR",
            "IDR",
            "ILS",
            "JPY",
            "KZT",
            "KES",
            "MYR",
            "MXN",
            "MAD",
            "TWD",
            "NZD",
            "NOK",
            "PEN",
            "PHP",
            "PLN",
            "GBP",
            "QAR",
            "RON",
            "SAR",
            "SGD",
            "ZAR",
            "KRW",
            "SEK",
            "CHF",
            "THB",
            "TRY",
            "UGX",
            "UAH",
            "UYU",
            "VND",
        ]
    ]
    """Currency code for prices (e.g. EUR). Default: USD."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    infants: NotRequired[int]
    """Number of infant guests (e.g. 1). Minimum: 0."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). You are billed per result returned, so a lower limit costs less. Range: 1 to 20."""
    location: Required[str]
    """Location to search listings in (e.g. London)."""
    minBathrooms: NotRequired[int]
    """Minimum number of bathrooms (e.g. 2). Minimum: 0."""
    minBedrooms: NotRequired[int]
    """Minimum number of bedrooms (e.g. 2). Minimum: 0."""
    minBeds: NotRequired[int]
    """Minimum number of beds (e.g. 2). Minimum: 0."""
    pets: NotRequired[int]
    """Number of pets; only pet-friendly listings are returned when set (e.g. 1). Minimum: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    priceMax: NotRequired[int]
    """Maximum search price in the selected currency (e.g. 300). Minimum: 0."""
    priceMin: NotRequired[int]
    """Minimum search price in the selected currency (e.g. 50). Minimum: 0."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AirbnbSearchData(BaseModel):
    items: list[AirbnbSearchItem] = Field(
        description="Listing records: name, total-stay price label, rating, location, host info, and availability details. Populated whenever the provider has data for the entity."
    )


class AirbnbSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(
        default=None, description="Listing description written by the host."
    )
    host_avatar_url: str | None = Field(
        default=None, alias="hostAvatarUrl", description="Host profile photo URL."
    )
    host_id: str | None = Field(
        default=None, alias="hostId", description="Airbnb host identifier."
    )
    host_name: str | None = Field(default=None, alias="hostName")
    host_rating: float | None = Field(
        default=None,
        alias="hostRating",
        description="Average rating across the host other listings (0-5).",
    )
    host_reviews_count: int | None = Field(
        default=None,
        alias="hostReviewsCount",
        description="Number of reviews across the host other listings.",
    )
    host_verified: bool | None = Field(
        default=None,
        alias="hostVerified",
        description="Whether Airbnb has verified the host identity.",
    )
    id: str = Field(
        description="Airbnb listing identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[AirbnbSearchImage] | None = Field(
        default=None, description="Listing photos."
    )
    is_available: bool | None = Field(default=None, alias="isAvailable")
    is_superhost: bool | None = Field(default=None, alias="isSuperhost")
    latitude: float | None = None
    location: str | None = Field(default=None, description="Location subtitle.")
    longitude: float | None = None
    person_capacity: int | None = Field(default=None, alias="personCapacity")
    price: str | None = Field(
        default=None,
        description="Total-stay price label returned by Airbnb (e.g. $3,149 total).",
    )
    property_type: str | None = Field(default=None, alias="propertyType")
    rating: float | None = Field(
        default=None, description="Guest satisfaction rating (0-5)."
    )
    rating_accuracy: float | None = Field(
        default=None, alias="ratingAccuracy", description="Accuracy sub-rating (0-5)."
    )
    rating_checkin: float | None = Field(
        default=None, alias="ratingCheckin", description="Check-in sub-rating (0-5)."
    )
    rating_cleanliness: float | None = Field(
        default=None,
        alias="ratingCleanliness",
        description="Cleanliness sub-rating (0-5).",
    )
    rating_communication: float | None = Field(
        default=None,
        alias="ratingCommunication",
        description="Communication sub-rating (0-5).",
    )
    rating_location: float | None = Field(
        default=None, alias="ratingLocation", description="Location sub-rating (0-5)."
    )
    rating_value: float | None = Field(
        default=None, alias="ratingValue", description="Value sub-rating (0-5)."
    )
    reviews_count: int | None = Field(default=None, alias="reviewsCount")
    room_type: str | None = Field(default=None, alias="roomType")
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class AirbnbSearchImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    caption: str | None = Field(default=None, description="Photo caption.")
    url: str | None = Field(default=None, description="Photo URL.")


class AirbnbNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AirbnbSearchInput],
    ) -> RunResult[AirbnbSearchData]:
        """Airbnb Search

        Search Airbnb listings by location and dates with optional price,
        beds/bedrooms/bathrooms, and guest-party filters and get results (name,
        total-stay price label, rating, host) as normalized JSON.

        Price: $0.00009 per request plus $0.00165 per result (maximum $0.0331).

        Example:
            res = client.airbnb.search(adults=2, limit=3, location="San Diego", minBedrooms=3)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "airbnb.search", dict(input), options
        )
        return RunResult[AirbnbSearchData].model_validate(raw)


class AsyncAirbnbNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AirbnbSearchInput],
    ) -> RunResult[AirbnbSearchData]:
        """Airbnb Search

        Search Airbnb listings by location and dates with optional price,
        beds/bedrooms/bathrooms, and guest-party filters and get results (name,
        total-stay price label, rating, host) as normalized JSON.

        Price: $0.00009 per request plus $0.00165 per result (maximum $0.0331).

        Example:
            res = client.airbnb.search(adults=2, limit=3, location="San Diego", minBedrooms=3)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "airbnb.search", dict(input), options
        )
        return RunResult[AirbnbSearchData].model_validate(raw)
