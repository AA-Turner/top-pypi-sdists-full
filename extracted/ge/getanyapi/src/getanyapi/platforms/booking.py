# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the booking platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class BookingSearchInput(TypedDict, total=False):
    """Input for Booking.com Search."""

    adults: NotRequired[int]
    """Number of adult guests (e.g. 2). Minimum: 1."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    checkIn: NotRequired[str]
    """Check-in date in YYYY-MM-DD format (e.g. 2026-07-01). Defaults to tomorrow."""
    checkOut: NotRequired[str]
    """Check-out date in YYYY-MM-DD format (e.g. 2026-07-05). Defaults to the day after check-in."""
    children: NotRequired[int]
    """Number of child guests (e.g. 1). Minimum: 0."""
    currency: NotRequired[str]
    """Currency code for prices (e.g. EUR). Default: USD."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of hotels to return (1-20, default 20). You are billed per result returned, so a lower limit costs less. Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Destination city to search for stays in (e.g. Paris)."""
    rooms: NotRequired[int]
    """Number of rooms to book (e.g. 1). Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class BookingSearchData(BaseModel):
    items: list[BookingSearchItem] = Field(
        description="Hotel result records: name, price, review score, star rating, address, and location. Populated whenever the provider has data for the entity."
    )


class BookingSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = None
    city: str | None = None
    country: str | None = Field(default=None, description="ISO country code.")
    currency: str | None = None
    discount_badge: str | None = Field(
        default=None,
        alias="discountBadge",
        description="Promotion label Booking.com shows on the offer (e.g. Getaway Deal).",
    )
    distance_from_center: str | None = Field(
        default=None,
        alias="distanceFromCenter",
        description="Distance from the city center as Booking.com phrases it.",
    )
    free_cancellation: bool | None = Field(
        default=None,
        alias="freeCancellation",
        description="Whether the offer can be cancelled free of charge.",
    )
    id: str | None = Field(
        default=None,
        description="Booking.com hotel identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Primary hotel photo URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    is_closed: bool | None = Field(
        default=None, alias="isClosed", description="Whether the property is closed."
    )
    is_sold_out: bool | None = Field(
        default=None,
        alias="isSoldOut",
        description="Whether the property is sold out for the requested dates.",
    )
    latitude: float | None = None
    location: str | None = Field(
        default=None, description="Neighborhood or area label."
    )
    longitude: float | None = None
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    no_prepayment: bool | None = Field(
        default=None,
        alias="noPrepayment",
        description="Whether the offer needs no payment up front.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="Pre-discount total stay price in the requested currency.",
    )
    price: float | None = Field(
        default=None, description="Total stay price in the requested currency."
    )
    price_per_night: float | None = Field(default=None, alias="pricePerNight")
    rating: float | None = Field(default=None, description="Guest review score (0-10).")
    review_score: float | None = Field(
        default=None, alias="reviewScore", description="Guest review score (0-10)."
    )
    review_score_label: str | None = Field(
        default=None,
        alias="reviewScoreLabel",
        description="Word Booking.com uses for the review score (e.g. Fabulous).",
    )
    reviews_count: int | None = Field(default=None, alias="reviewsCount")
    room_id: str | None = Field(
        default=None,
        alias="roomId",
        description="Identifier of the room the quoted price is for.",
    )
    stars: int | None = Field(default=None, description="Star rating class (1-5).")
    thumbnail: str | None = Field(default=None, description="Small hotel photo URL.")
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class BookingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BookingSearchInput],
    ) -> RunResult[BookingSearchData]:
        """Booking.com Search

        Search Booking.com stays by destination and dates with optional guest and
        room occupancy and get hotel results (name, price, review score, location)
        as normalized JSON.

        Price: $0.0022 per request plus $0.00495 per result (maximum $0.102).

        Example:
            res = client.booking.search(adults=2, checkIn="2026-12-01", checkOut="2026-12-03", limit=3, query="New York")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "booking.search", dict(input), options
        )
        return RunResult[BookingSearchData].model_validate(raw)


class AsyncBookingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BookingSearchInput],
    ) -> RunResult[BookingSearchData]:
        """Booking.com Search

        Search Booking.com stays by destination and dates with optional guest and
        room occupancy and get hotel results (name, price, review score, location)
        as normalized JSON.

        Price: $0.0022 per request plus $0.00495 per result (maximum $0.102).

        Example:
            res = client.booking.search(adults=2, checkIn="2026-12-01", checkOut="2026-12-03", limit=3, query="New York")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "booking.search", dict(input), options
        )
        return RunResult[BookingSearchData].model_validate(raw)
