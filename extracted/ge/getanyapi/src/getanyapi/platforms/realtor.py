# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the realtor platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class RealtorSearchInput(TypedDict, total=False):
    """Input for Realtor.com Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    bathsMin: NotRequired[int]
    """Minimum number of bathrooms (e.g. 2). Minimum: 0."""
    bedsMin: NotRequired[int]
    """Minimum number of bedrooms (e.g. 3). Minimum: 0."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: NotRequired[str]
    """Free-text keyword that must appear in the listing description (e.g. 'pool')."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-25, default 25). You are billed per result returned, so a lower limit costs less. Range: 1 to 25."""
    location: Required[str]
    """City, ZIP code, neighborhood or state to search (e.g. Las Vegas, NV)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    priceMax: NotRequired[int]
    """Maximum listing price in USD (e.g. 750000). Minimum: 0."""
    priceMin: NotRequired[int]
    """Minimum listing price in USD (e.g. 250000). Minimum: 0."""
    propertyTypes: NotRequired[
        list[
            Literal[
                "single_family",
                "townhomes",
                "condo_townhome",
                "multi_family",
                "land",
                "farm",
                "manufactured",
                "mobile",
                "apartment",
                "coop",
                "duplex_triplex",
            ]
        ]
    ]
    """Filter by one or more property types; omit for all types (e.g. ["single_family", "townhomes"])."""
    searchMode: NotRequired[Literal["for_sale", "sold"]]
    """Listing type to search: for_sale or sold (e.g. for_sale). Default: for_sale."""
    searchStatuses: NotRequired[
        list[
            Literal[
                "for_sale", "ready_to_build", "pending", "coming_soon", "contingent"
            ]
        ]
    ]
    """Listing statuses to include in for_sale mode; omit for active For Sale + Ready to Build. Ignored in sold mode (e.g. ["for_sale", "pending"])."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class RealtorSearchData(BaseModel):
    items: list[RealtorSearchItem] = Field(
        description="Matching Realtor.com property listing records. Populated whenever the provider has data for the entity."
    )


class RealtorSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address_line: str | None = Field(
        default=None,
        alias="addressLine",
        description="Street address line of the property.",
    )
    agent_email: str | None = Field(
        default=None,
        alias="agentEmail",
        description="Contact email for the listing agent.",
    )
    agent_name: str | None = Field(
        default=None, alias="agentName", description="Name of the listing agent."
    )
    agent_phone: str | None = Field(
        default=None,
        alias="agentPhone",
        description="Contact phone number for the listing agent.",
    )
    agent_url: str | None = Field(
        default=None,
        alias="agentUrl",
        description="Realtor.com profile URL of the listing agent.",
    )
    baths: str | None = Field(
        default=None,
        description='Consolidated bathroom count (e.g. "3.5" for three full and one half bath).',
    )
    beds: float | None = Field(default=None, description="Number of bedrooms.")
    broker_name: str | None = Field(
        default=None,
        alias="brokerName",
        description="Listing brokerage or office name.",
    )
    city: str | None = Field(default=None, description="City the property is in.")
    country: str | None = Field(default=None, description="Country the property is in.")
    county: str | None = Field(default=None, description="County the property is in.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    days_on_market: float | None = Field(
        default=None,
        alias="daysOnMarket",
        description="Number of days the listing has been on the market.",
    )
    description: str | None = Field(
        default=None, description="Listing description written by the agent."
    )
    garage_spaces: float | None = Field(
        default=None, alias="garageSpaces", description="Number of garage spaces."
    )
    hoa_fee: float | None = Field(
        default=None,
        alias="hoaFee",
        description="Homeowners association fee, in US dollars, at the frequency Realtor.com reports.",
    )
    image: str | None = Field(default=None, description="Primary listing photo URL.")
    images: list[str] | None = Field(default=None, description="Listing photo URLs.")
    is_new_construction: bool | None = Field(
        default=None,
        alias="isNewConstruction",
        description="True when the listing is new construction.",
    )
    latitude: float | None = Field(
        default=None, description="Latitude of the property in decimal degrees."
    )
    listing_id: str | None = Field(
        default=None,
        alias="listingId",
        description="Realtor.com listing id for this specific listing of the property.",
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the property in decimal degrees."
    )
    lot_sqft: float | None = Field(
        default=None, alias="lotSqft", description="Lot size in square feet."
    )
    mls_id: str | None = Field(
        default=None, alias="mlsId", description="MLS number for the listing."
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
        default=None, description="Current list price in US dollars."
    )
    price_per_sqft: float | None = Field(
        default=None,
        alias="pricePerSqft",
        description="List price per square foot in US dollars.",
    )
    property_id: str = Field(
        alias="propertyId",
        description="Realtor.com property id (stable identifier for the listing). Populated whenever the provider has data for the entity.",
    )
    property_type: str | None = Field(
        default=None,
        alias="propertyType",
        description="Property type (e.g. single_family, condos, townhomes).",
    )
    sqft: float | None = Field(
        default=None, description="Interior living area in square feet."
    )
    state: str | None = Field(
        default=None, description="Two-letter state code the property is in."
    )
    status: (
        Literal[
            "for_sale", "ready_to_build", "sold", "pending", "contingent", "coming_soon"
        ]
        | None
    ) = Field(
        default=None,
        description="Display listing status, including ready-to-build, pending, contingent, and coming-soon sub-statuses when present.",
    )
    stories: float | None = Field(
        default=None, description="Number of storeys in the home."
    )
    tags: list[str] | None = Field(
        default=None,
        description="Realtor.com feature tags for the property (e.g. central_air, garage_1_or_more).",
    )
    tax_amount: float | None = Field(
        default=None,
        alias="taxAmount",
        description="Most recent annual property tax paid, in US dollars.",
    )
    tax_assessed_value: float | None = Field(
        default=None,
        alias="taxAssessedValue",
        description="Most recent assessed value from the county tax authority, in US dollars, or null when none is published (common on new construction).",
    )
    title: str | None = Field(
        default=None,
        description="Human-readable street address line used as the listing title.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the listing was last updated.",
    )
    url: str = Field(
        description="Canonical Realtor.com listing detail page URL. Populated whenever the provider has data for the entity."
    )
    year_built: float | None = Field(
        default=None, alias="yearBuilt", description="Year the property was built."
    )


class RealtorNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RealtorSearchInput],
    ) -> RunResult[RealtorSearchData]:
        """Realtor.com Search

        Search Realtor.com listings by location with optional price, property-type,
        beds/baths, listing-status, and keyword filters and get property records
        (price, address, beds, baths) as normalized JSON.

        Price: $0.0055 per request plus $0.00165 per result (maximum $0.0468).

        Example:
            res = client.realtor.search(bedsMin=4, limit=3, location="Austin, TX", propertyTypes=["single_family"], searchStatuses=["pending"])
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "realtor.search", dict(input), options
        )
        return RunResult[RealtorSearchData].model_validate(raw)


class AsyncRealtorNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RealtorSearchInput],
    ) -> RunResult[RealtorSearchData]:
        """Realtor.com Search

        Search Realtor.com listings by location with optional price, property-type,
        beds/baths, listing-status, and keyword filters and get property records
        (price, address, beds, baths) as normalized JSON.

        Price: $0.0055 per request plus $0.00165 per result (maximum $0.0468).

        Example:
            res = client.realtor.search(bedsMin=4, limit=3, location="Austin, TX", propertyTypes=["single_family"], searchStatuses=["pending"])
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "realtor.search", dict(input), options
        )
        return RunResult[RealtorSearchData].model_validate(raw)
