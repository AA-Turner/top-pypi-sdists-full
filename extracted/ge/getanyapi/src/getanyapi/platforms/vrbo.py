# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the vrbo platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class VrboSearchInput(TypedDict, total=False):
    """Input for Vrbo Search."""

    adults: NotRequired[int]
    """Number of adult guests (e.g. 2). Range: 1 to 20."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    checkIn: Required[str]
    """Check-in date in YYYY-MM-DD format (e.g. 2027-01-15). Today or later."""
    checkOut: Required[str]
    """Check-out date in YYYY-MM-DD format (e.g. 2027-01-18). After the check-in date."""
    childrenAges: NotRequired[list[int]]
    """Age of each child guest, one entry per child (e.g. [5, 8] for two children aged 5 and 8). Omit it when no children are staying."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of listings to return (1-50, default 20). The price is the same whatever the limit. Range: 1 to 50. Default: 20."""
    location: Required[str]
    """Destination to search rentals in: a city, region or area (e.g. Lake Tahoe, Lisbon, Outer Banks, North Carolina)."""
    minBathrooms: NotRequired[int]
    """Minimum number of bathrooms (e.g. 2). Range: 1 to 50."""
    minBedrooms: NotRequired[int]
    """Minimum number of bedrooms (e.g. 3). Range: 0 to 50."""
    minBeds: NotRequired[int]
    """Minimum number of beds (e.g. 4). Range: 1 to 20."""
    offset: NotRequired[int]
    """Number of listings to skip, for paging: send offset 20 with limit 20 for the second page. Range: 0 to 1000. Default: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    priceMax: NotRequired[int]
    """Maximum price in the currency results are priced in (each listing's currency), per night or for the whole stay as priceType says (e.g. 400). With a price filter, only listings Vrbo prices for your dates are returned. Range: 1 to 1000000."""
    priceMin: NotRequired[int]
    """Minimum price in the currency results are priced in (each listing's currency), per night or for the whole stay as priceType says (e.g. 100). Range: 0 to 1000000."""
    priceType: NotRequired[Literal["nightly", "total"]]
    """Whether priceMin and priceMax are a nightly price (default) or the total for the stay. Default: nightly."""
    sort: NotRequired[
        Literal[
            "recommended",
            "price_low_to_high",
            "price_high_to_low",
            "review",
            "review_count",
        ]
    ]
    """Result order: recommended (Vrbo's default), price_low_to_high, price_high_to_low, review (highest rated first) or review_count (most reviewed first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class VrboSearchData(BaseModel):
    items: list[VrboSearchItem] = Field(
        description="Vrbo listings priced for the requested dates and guests, in Vrbo's order. A listing Vrbo shows without a price for the dates is left out. Populated whenever the provider has data for the entity."
    )


class VrboSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bedrooms: int | None = Field(
        default=None,
        description="Number of bedrooms. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    beds: int | None = Field(
        default=None,
        description="Number of beds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None,
        description="ISO 4217 currency code of the prices (e.g. USD). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    fees_note: str | None = Field(
        default=None,
        alias="feesNote",
        description="Vrbo's note on what the price includes (e.g. All fees included).",
    )
    id: str = Field(description="Vrbo property ID.")
    images: list[str] | None = Field(
        default=None,
        description="Listing photo URLs. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(
        description='Listing name. Vrbo often shows a generic name such as "Condo in Kings Beach".'
    )
    nights: int | None = Field(
        default=None, description="Number of nights the total price covers."
    )
    original_price_per_night: float | None = Field(
        default=None,
        alias="originalPricePerNight",
        description="Nightly price before Vrbo's discount, or null when the listing is not discounted.",
    )
    overview: str | None = Field(
        default=None,
        description='Vrbo\'s one-line summary of the listing (e.g. "3 bedrooms · 6 beds · Free cancellation until Dec 16"). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    price_per_night: float | None = Field(
        default=None,
        alias="pricePerNight",
        description="Nightly price for the requested dates and guests, in currency. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    property_type: str | None = Field(
        default=None,
        alias="propertyType",
        description="Property type (e.g. Condo, House), or null when Vrbo does not state it in search results.",
    )
    rating: float | None = Field(
        default=None,
        description="Average guest rating out of 10, or null when the listing has no rating. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating_label: str | None = Field(
        default=None,
        alias="ratingLabel",
        description="Vrbo's word for the rating (e.g. Exceptional, Wonderful).",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of guest reviews, or null when Vrbo does not show a count.",
    )
    total_price: float | None = Field(
        default=None,
        alias="totalPrice",
        description="Total price for the whole stay, in currency. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str = Field(description="Vrbo listing URL.")


class VrboNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[VrboSearchInput]
    ) -> RunResult[VrboSearchData]:
        """Vrbo Search

        Search Vrbo vacation rentals by destination and dates, with guest, bedroom,
        bed, bathroom and price filters, and get up to 50 listings per call: Vrbo
        property ID and link, name, summary line, property type, bedrooms, beds,
        guest rating and review count, nightly and total stay price with the
        original nightly price before any discount, and photos as normalized JSON.
        Page with offset; the price is the same whatever the limit.

        Price: $0.001 per request.

        Example:
            res = client.vrbo.search(adults=2, checkIn="2026-12-06", checkOut="2026-12-09", limit=5, location="Lake Tahoe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "vrbo.search", dict(input), options
        )
        return RunResult[VrboSearchData].model_validate(raw)


class AsyncVrboNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[VrboSearchInput]
    ) -> RunResult[VrboSearchData]:
        """Vrbo Search

        Search Vrbo vacation rentals by destination and dates, with guest, bedroom,
        bed, bathroom and price filters, and get up to 50 listings per call: Vrbo
        property ID and link, name, summary line, property type, bedrooms, beds,
        guest rating and review count, nightly and total stay price with the
        original nightly price before any discount, and photos as normalized JSON.
        Page with offset; the price is the same whatever the limit.

        Price: $0.001 per request.

        Example:
            res = client.vrbo.search(adults=2, checkIn="2026-12-06", checkOut="2026-12-09", limit=5, location="Lake Tahoe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "vrbo.search", dict(input), options
        )
        return RunResult[VrboSearchData].model_validate(raw)
