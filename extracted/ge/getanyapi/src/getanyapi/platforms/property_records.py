# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the property_records platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class PropertyRecordsEnformionInput(TypedDict, total=False):
    """Input for Property Records - Enformion."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    city: Required[str]
    """City of the property, e.g. Austin."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    state: Required[str]
    """US state of the property, as its two-letter code, e.g. TX."""
    street: Required[str]
    """Street line of one US property address, e.g. 4510 Secure Ln. Include a unit number when there is one."""
    zip: NotRequired[str]
    """Five-digit ZIP code, optionally with its four-digit extension, e.g. 78725."""


class PropertyRecordsEnformionData(BaseModel):
    records: list[PropertyRecordsEnformionRecord] = Field(
        description="Every parcel on record at the address. A campus or multi-parcel address returns several."
    )


class PropertyRecordsEnformionRecord(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    apn: str | None = Field(
        default=None,
        description="Assessor's parcel number (APN) the county files this parcel under.",
    )
    appraised_value: float | None = Field(
        default=None,
        alias="appraisedValue",
        description="Total appraised value, in US dollars.",
    )
    assessed_improvement_value: float | None = Field(
        default=None,
        alias="assessedImprovementValue",
        description="Assessed value of the buildings and other improvements, in US dollars.",
    )
    assessed_land_value: float | None = Field(
        default=None,
        alias="assessedLandValue",
        description="Assessed value of the land alone, in US dollars.",
    )
    assessed_value: float | None = Field(
        default=None,
        alias="assessedValue",
        description="Total assessed value for property tax, in US dollars.",
    )
    assessed_year: int | None = Field(
        default=None, alias="assessedYear", description="Year of the assessment."
    )
    baths: float | None = Field(
        default=None,
        description="Number of bathrooms. Absent when the county records none.",
    )
    beds: int | None = Field(
        default=None,
        description="Number of bedrooms. Absent when the county records none.",
    )
    city: str | None = Field(default=None, description="City of the property.")
    county: str | None = Field(
        default=None, description="County the parcel is recorded in."
    )
    current_owners: list[PropertyRecordsEnformionCurrentOwner] | None = Field(
        default=None,
        alias="currentOwners",
        description="Owners on the current county record.",
    )
    fips_code: str | None = Field(
        default=None,
        alias="fipsCode",
        description="Five-digit FIPS code of the county. Pair it with apn to identify the parcel nationally.",
    )
    foreclosure_stage: str | None = Field(
        default=None,
        alias="foreclosureStage",
        description="Foreclosure stage code, when the parcel is in foreclosure.",
    )
    land_use: str | None = Field(
        default=None,
        alias="landUse",
        description="Land use as the county describes it, e.g. CONDOMINIUM or LABORATORY.",
    )
    last_sale_price: float | None = Field(
        default=None,
        alias="lastSalePrice",
        description="Price of the most recent recorded sale, in US dollars.",
    )
    last_sale_utc: float | None = Field(
        default=None,
        alias="lastSaleUtc",
        description="Date of the most recent recorded sale, as a UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    latitude: float | None = Field(default=None, description="Latitude of the parcel.")
    living_area_sqft: int | None = Field(
        default=None,
        alias="livingAreaSqft",
        description="Living area in square feet. Absent when the county records none.",
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the parcel."
    )
    lot_size: float | None = Field(
        default=None,
        alias="lotSize",
        description="Lot size as the county records it, usually in square feet.",
    )
    market_improvement_value: float | None = Field(
        default=None,
        alias="marketImprovementValue",
        description="Market value of the buildings and other improvements, in US dollars.",
    )
    market_land_value: float | None = Field(
        default=None,
        alias="marketLandValue",
        description="Market value of the land alone, in US dollars.",
    )
    market_value: float | None = Field(
        default=None,
        alias="marketValue",
        description="Total market value the county records, in US dollars.",
    )
    owner_mailing_address: str | None = Field(
        default=None,
        alias="ownerMailingAddress",
        description="Where the current owner receives mail, when the county records it.",
    )
    owner_occupied: bool | None = Field(
        default=None,
        alias="ownerOccupied",
        description="True when the owner lives at the property.",
    )
    previous_owners: list[PropertyRecordsEnformionPreviousOwner] | None = Field(
        default=None,
        alias="previousOwners",
        description="Earlier owners of the parcel, most recent first.",
    )
    property_type: str | None = Field(
        default=None,
        alias="propertyType",
        description="Property type, e.g. SINGLE FAMILY RESIDENCE, INDUSTRIAL, or EXEMPT.",
    )
    state: str | None = Field(default=None, description="Two-letter US state code.")
    street: str | None = Field(
        description="Street line of the property address, e.g. 4510 Secure LN."
    )
    tax_account_number: str | None = Field(
        default=None,
        alias="taxAccountNumber",
        description="The county tax account number for the parcel.",
    )
    tax_amount: float | None = Field(
        default=None,
        alias="taxAmount",
        description="Annual property tax billed, in US dollars.",
    )
    tax_year: int | None = Field(
        default=None, alias="taxYear", description="Year the tax amount was billed for."
    )
    year_built: int | None = Field(
        default=None, alias="yearBuilt", description="Year the main building was built."
    )
    zip: str | None = Field(default=None, description="Five-digit ZIP code.")
    zoning: str | None = Field(
        default=None,
        description="Zoning code or zoning description on the county record.",
    )


class PropertyRecordsEnformionCurrentOwner(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    is_business: bool | None = Field(
        default=None,
        alias="isBusiness",
        description="True when the owner is a company or other organization rather than a person.",
    )
    name: str | None = Field(description="Owner name, a person or a business.")
    recorded_utc: float | None = Field(
        default=None,
        alias="recordedUtc",
        description="Date the ownership record was captured, as a UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. It is not necessarily the purchase date; see lastSaleUtc.",
    )


class PropertyRecordsEnformionPreviousOwner(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = Field(description="Owner name, a person or a business.")
    recorded_utc: float | None = Field(
        default=None,
        alias="recordedUtc",
        description="Date the ownership record was captured, as a UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class PropertyRecordsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def enformion(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PropertyRecordsEnformionInput],
    ) -> RunResult[PropertyRecordsEnformionData]:
        """Property Records - Enformion

        Look up the public property records for one US address: current and previous
        owners, parcel number (APN), last sale, assessed and market values, property
        tax, beds, baths, living area, lot size, year built, land use, and zoning.
        One address can match several parcels, and every match is returned. Billed
        only when a record is found.

        Price: $0.1536 per request.

        Example:
            res = client.property_records.enformion(city="Austin", state="TX", street="4510 Secure Ln", zip="78725")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "property_records.enformion", dict(input), options
        )
        return RunResult[PropertyRecordsEnformionData].model_validate(raw)


class AsyncPropertyRecordsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def enformion(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PropertyRecordsEnformionInput],
    ) -> RunResult[PropertyRecordsEnformionData]:
        """Property Records - Enformion

        Look up the public property records for one US address: current and previous
        owners, parcel number (APN), last sale, assessed and market values, property
        tax, beds, baths, living area, lot size, year built, land use, and zoning.
        One address can match several parcels, and every match is returned. Billed
        only when a record is found.

        Price: $0.1536 per request.

        Example:
            res = client.property_records.enformion(city="Austin", state="TX", street="4510 Secure Ln", zip="78725")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "property_records.enformion", dict(input), options
        )
        return RunResult[PropertyRecordsEnformionData].model_validate(raw)
