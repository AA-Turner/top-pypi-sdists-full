# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the zillow platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class ZillowAgentInput(TypedDict, total=False):
    """Input for Zillow Agent."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Zillow agent profile URL (e.g. https://www.zillow.com/profile/gregorycarlsonATX/)."""


class ZillowPropertyInput(TypedDict, total=False):
    """Input for Zillow Property."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Zillow property details URL (e.g. https://www.zillow.com/homedetails/123-Main-St-Anytown-CA-90210/12345678_zpid/)."""


class ZillowSearchInput(TypedDict, total=False):
    """Input for Zillow Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    daysOnZillow: NotRequired[
        Literal[
            "1_day",
            "1_week",
            "2_weeks",
            "1_month",
            "3_months",
            "6_months",
            "12_months",
            "24_months",
            "36_months",
        ]
    ]
    """Only include listings on Zillow at most this long (e.g. 1_week)."""
    homeTypes: NotRequired[
        list[
            Literal[
                "singleFamily",
                "multiFamily",
                "townhome",
                "condo",
                "apartment",
                "manufactured",
                "land",
            ]
        ]
    ]
    """Filter by property type; omit for any. Rentals support only singleFamily, multiFamily, townhome, and condo (e.g. ["singleFamily", "condo"])."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeAcceptingBackupOffers: NotRequired[bool]
    """Include listings accepting backup offers, which Zillow excludes by default (e.g. true)."""
    includePendingAndUnderContract: NotRequired[bool]
    """Include pending and under-contract listings, which Zillow excludes by default (e.g. true)."""
    includeRoomForRent: NotRequired[bool]
    """Include room-for-rent listings in rent searches; when omitted or false only entire places are returned (e.g. true)."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-25, default 25). Range: 1 to 25. Default: 25."""
    listingTypes: NotRequired[
        list[
            Literal[
                "fsba",
                "fsbo",
                "newConstruction",
                "comingSoon",
                "auction",
                "foreclosure",
                "foreclosed",
                "preforeclosure",
            ]
        ]
    ]
    """Listing types to include for buy searches; omit for all standard types. fsba = agent listed, fsbo = for sale by owner. Ignored for rent and sold (e.g. ["newConstruction"])."""
    location: Required[str]
    """Region-level location to search: ZIP code, city and state, county, or neighborhood (e.g. 'Austin, TX' or '78701'). Street addresses are not supported; use the property's ZIP code instead."""
    maxBedrooms: NotRequired[int]
    """Maximum number of bedrooms (e.g. 5). Minimum: 0."""
    maxLivingAreaSqft: NotRequired[int]
    """Maximum living area in square feet (e.g. 3000). Minimum: 0."""
    maxPrice: NotRequired[int]
    """Maximum price in USD: monthly rent for rentals, total price for buy/sold (e.g. 750000). Minimum: 0."""
    minBedrooms: NotRequired[int]
    """Minimum number of bedrooms (e.g. 3). Minimum: 0."""
    minLivingAreaSqft: NotRequired[int]
    """Minimum living area in square feet (e.g. 1500). Minimum: 0."""
    minPrice: NotRequired[int]
    """Minimum price in USD: monthly rent for rentals, total price for buy/sold (e.g. 250000). Minimum: 0."""
    operation: NotRequired[Literal["buy", "rent", "sold"]]
    """Listing type: buy (for sale), rent, or sold. Default: buy."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "brokerName",
                "daysOnZillow",
                "images",
                "isZillowOwned",
                "taxAssessedValue",
                "yearBuilt",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `yearBuilt`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    showOnlyPriceReductions: NotRequired[bool]
    """Only show listings with a price reduction. Buy searches only; ignored for rentals (e.g. true)."""
    sortBy: NotRequired[
        Literal[
            "newest",
            "recentlyChanged",
            "price_high",
            "price_low",
            "bedrooms",
            "bathrooms",
            "rentalPriorityScore",
        ]
    ]
    """Sort order for results; omit for Zillow's default relevance. rentalPriorityScore applies to rent searches only (e.g. newest)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ZillowAgentData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bio: str | None = Field(
        default=None, description="Agent's self-written biography, as HTML."
    )
    company: str | None = Field(
        default=None,
        description="Brokerage or business name the agent works under. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    email: str | None = Field(
        default=None,
        description="Agent's email address as listed on the profile. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    for_sale_count: int | None = Field(
        default=None,
        alias="forSaleCount",
        description="Number of active for-sale listings.",
    )
    image: str | None = Field(
        default=None,
        description="Profile photo URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    is_top_agent: bool | None = Field(
        default=None,
        alias="isTopAgent",
        description="True when Zillow flags the agent as a top agent.",
    )
    name: str = Field(
        description="Agent's full name. Populated whenever the provider has data for the entity."
    )
    phone: str | None = Field(
        default=None,
        description="Agent's phone number as listed on the profile (the cell number when one is listed). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None, description="Average review rating out of 5."
    )
    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        description="Number of reviews on the profile.",
    )
    service_areas: list[str] | None = Field(
        default=None,
        alias="serviceAreas",
        description='Cities and areas the agent lists as served, e.g. "Austin, TX".',
    )
    total_sales: int | None = Field(
        default=None,
        alias="totalSales",
        description="Total sales on record for the agent (for a team lead, the team's total).",
    )
    url: str = Field(
        description="Canonical Zillow profile URL. Populated whenever the provider has data for the entity."
    )
    username: str = Field(
        description="Zillow screen name, the last segment of the profile URL. Populated whenever the provider has data for the entity."
    )


class ZillowPropertyData(BaseModel):
    items: list[ZillowPropertyItem] = Field(
        description="The matched property record (single element for a property lookup). Populated whenever the provider has data for the entity."
    )


class ZillowPropertyItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address_line: str | None = Field(
        default=None,
        alias="addressLine",
        description="Street address line of the property.",
    )
    baths: float | None = Field(default=None, description="Number of bathrooms.")
    beds: float | None = Field(default=None, description="Number of bedrooms.")
    city: str | None = Field(default=None, description="City the property is in.")
    country: str | None = Field(default=None, description="Country the property is in.")
    county: str | None = Field(default=None, description="County the property is in.")
    currency: str | None = Field(
        default=None, description="Currency code for the price (e.g. USD)."
    )
    days_on_zillow: int | None = Field(
        default=None,
        alias="daysOnZillow",
        description="Days the listing has been on Zillow.",
    )
    description: str | None = Field(
        default=None, description="Listing description text."
    )
    home_status: str | None = Field(
        default=None,
        alias="homeStatus",
        description="Listing status (e.g. FOR_SALE, RECENTLY_SOLD, OTHER).",
    )
    home_type: str | None = Field(
        default=None,
        alias="homeType",
        description="Home type (e.g. SINGLE_FAMILY, CONDO, TOWNHOUSE).",
    )
    image: str | None = Field(default=None, description="Primary listing photo URL.")
    images: list[ZillowPropertyImage] | None = Field(
        default=None, description="Listing photos."
    )
    latitude: float | None = Field(
        default=None, description="Latitude of the property in decimal degrees."
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the property in decimal degrees."
    )
    mls_name: str | None = Field(
        default=None,
        alias="mlsName",
        description="Name of the multiple listing service the listing came from.",
    )
    postal_code: str | None = Field(
        default=None,
        alias="postalCode",
        description="Postal (ZIP) code of the property.",
    )
    price: float | None = Field(
        default=None, description="Listed price in the listing currency."
    )
    property_tax_rate: float | None = Field(
        default=None,
        alias="propertyTaxRate",
        description="Annual property tax rate as a percentage.",
    )
    rent_zestimate: float | None = Field(
        default=None,
        alias="rentZestimate",
        description="Zillow estimated monthly rent, or null when Zillow shows no rent Zestimate for the property.",
    )
    sqft: float | None = Field(
        default=None, description="Interior living area in square feet."
    )
    state: str | None = Field(
        default=None, description="Two-letter state code the property is in."
    )
    title: str | None = Field(
        default=None, description="Street address line used as the property title."
    )
    url: str = Field(
        description="Canonical Zillow property detail page URL. Populated whenever the provider has data for the entity."
    )
    zestimate: float | None = Field(
        default=None,
        description="Zillow estimated market value, or null when Zillow shows no Zestimate for the property.",
    )
    zpid: str = Field(
        description="Zillow property id (zpid), the stable identifier for the property. Populated whenever the provider has data for the entity."
    )


class ZillowPropertyImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str | None = Field(default=None, description="Photo URL.")


class ZillowSearchData(BaseModel):
    items: list[ZillowSearchItem] = Field(
        description="Property listing records matching the search: address, price, beds, baths, living area, property type, status, Zestimate, and coordinates. Populated whenever the provider has data for the entity."
    )


class ZillowSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    baths: float | None = Field(default=None, description="Number of bathrooms.")
    beds: float | None = Field(default=None, description="Number of bedrooms.")
    broker_name: str | None = Field(
        default=None, alias="brokerName", description="Listing brokerage name."
    )
    city: str | None = None
    currency: str | None = Field(
        default=None, description="ISO currency code of the price (e.g. USD)."
    )
    days_on_zillow: int | None = Field(
        default=None,
        alias="daysOnZillow",
        description="Days the listing has been on Zillow.",
    )
    image: str | None = Field(
        default=None,
        description="URL of the primary listing photo. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(default=None, description="Listing photo URLs.")
    is_zillow_owned: bool | None = Field(
        default=None,
        alias="isZillowOwned",
        description="True when Zillow itself owns the property.",
    )
    latitude: float | None = None
    living_area: float | None = Field(
        default=None,
        alias="livingArea",
        description="Interior living area in square feet.",
    )
    longitude: float | None = None
    lot_size: float | None = Field(
        default=None,
        alias="lotSize",
        description="Lot size as Zillow states it, in the unit named by lotSizeUnit (square feet or acres), or null when the listing has no lot size.",
    )
    lot_size_unit: str | None = Field(
        default=None,
        alias="lotSizeUnit",
        description="Unit of lotSize: sqft or acres. Null when the listing has no lot size or the serving source does not name the unit.",
    )
    price: float | None = Field(
        default=None, description="List price in the listing currency."
    )
    property_type: str | None = Field(
        default=None,
        alias="propertyType",
        description="Property type (e.g. SINGLE_FAMILY, CONDO, TOWNHOUSE).",
    )
    rent_zestimate: float | None = Field(
        default=None,
        alias="rentZestimate",
        description="Zillow estimated monthly rent, or null when Zillow shows no rent Zestimate for the listing.",
    )
    state: str | None = Field(default=None, description="Two-letter state code.")
    status: str | None = Field(
        default=None,
        description="Listing status (e.g. FOR_SALE, FOR_RENT, RECENTLY_SOLD).",
    )
    street_address: str | None = Field(
        default=None,
        alias="streetAddress",
        description="Street address of the property. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    tax_assessed_value: float | None = Field(
        default=None,
        alias="taxAssessedValue",
        description="Assessed value the county tax authority carries for the property, or null when none is published.",
    )
    url: str = Field(
        description="Absolute Zillow listing URL. Populated whenever the provider has data for the entity."
    )
    year_built: int | None = Field(
        default=None,
        alias="yearBuilt",
        description="Year the home was built, or null when the serving source does not publish it.",
    )
    zestimate: float | None = Field(
        default=None,
        description="Zillow estimated market value, or null when Zillow shows no Zestimate for the listing.",
    )
    zipcode: str | None = None
    zpid: str = Field(
        description="Zillow property id (zpid). Populated whenever the provider has data for the entity."
    )


class ZillowNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def agent(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZillowAgentInput],
    ) -> RunResult[ZillowAgentData]:
        """Zillow Agent

        Fetch one Zillow real estate agent's profile by URL: name, phone, email,
        brokerage, rating, review count, sales, and service areas.

        Price: $0.0008 per request.

        Example:
            res = client.zillow.agent(url="https://www.zillow.com/profile/gregorycarlsonATX/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zillow.agent", dict(input), options
        )
        return RunResult[ZillowAgentData].model_validate(raw)

    def property(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZillowPropertyInput],
    ) -> RunResult[ZillowPropertyData]:
        """Zillow Property

        Fetch full details for a single Zillow property listing by URL (price, facts
        and features, photos, and price/tax history).

        Price: $0.0008 per request.

        Example:
            res = client.zillow.property(url="https://www.zillow.com/homedetails/4510-Secure-Ln-Austin-TX-78725/83126034_zpid/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zillow.property", dict(input), options
        )
        return RunResult[ZillowPropertyData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZillowSearchInput],
    ) -> RunResult[ZillowSearchData]:
        """Zillow Search

        Search Zillow for-sale, rental, or sold listings by region-level location
        (city, ZIP, county, or neighborhood) with optional price, bedroom,
        living-area, home-type, recency, and sort filters and get matching
        properties (price, address, beds, baths, living area, status, Zestimate) as
        normalized JSON.

        Price: $0.0008 per request.

        Example:
            res = client.zillow.search(limit=3, location="Austin, TX", maxPrice=900000, minBedrooms=3, operation="buy")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zillow.search", dict(input), options
        )
        return RunResult[ZillowSearchData].model_validate(raw)


class AsyncZillowNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def agent(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZillowAgentInput],
    ) -> RunResult[ZillowAgentData]:
        """Zillow Agent

        Fetch one Zillow real estate agent's profile by URL: name, phone, email,
        brokerage, rating, review count, sales, and service areas.

        Price: $0.0008 per request.

        Example:
            res = client.zillow.agent(url="https://www.zillow.com/profile/gregorycarlsonATX/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zillow.agent", dict(input), options
        )
        return RunResult[ZillowAgentData].model_validate(raw)

    async def property(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZillowPropertyInput],
    ) -> RunResult[ZillowPropertyData]:
        """Zillow Property

        Fetch full details for a single Zillow property listing by URL (price, facts
        and features, photos, and price/tax history).

        Price: $0.0008 per request.

        Example:
            res = client.zillow.property(url="https://www.zillow.com/homedetails/4510-Secure-Ln-Austin-TX-78725/83126034_zpid/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zillow.property", dict(input), options
        )
        return RunResult[ZillowPropertyData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZillowSearchInput],
    ) -> RunResult[ZillowSearchData]:
        """Zillow Search

        Search Zillow for-sale, rental, or sold listings by region-level location
        (city, ZIP, county, or neighborhood) with optional price, bedroom,
        living-area, home-type, recency, and sort filters and get matching
        properties (price, address, beds, baths, living area, status, Zestimate) as
        normalized JSON.

        Price: $0.0008 per request.

        Example:
            res = client.zillow.search(limit=3, location="Austin, TX", maxPrice=900000, minBedrooms=3, operation="buy")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zillow.search", dict(input), options
        )
        return RunResult[ZillowSearchData].model_validate(raw)
