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


class VrboListingInput(TypedDict, total=False):
    """Input for Vrbo Listing."""

    adults: NotRequired[int]
    """Number of adult guests to price for (1-20, default 2). Range: 1 to 20. Default: 2."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    checkIn: NotRequired[str]
    """Check-in date to price and check availability for, in YYYY-MM-DD format (e.g. 2027-01-15). Today or later. Without dates, a 3-night stay about a month ahead is priced; the dates used are in stay."""
    checkOut: NotRequired[str]
    """Check-out date in YYYY-MM-DD format (e.g. 2027-01-18). After the check-in date. With a check-in date alone, the stay is 3 nights."""
    childrenAges: NotRequired[list[int]]
    """Age of each child guest, one entry per child (e.g. [5, 8] for two children aged 5 and 8). Omit it when no children are staying."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    propertyId: Required[str]
    """Vrbo property ID: the id vrbo.search returns for a listing (e.g. 69764328)."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class VrboSearchInput(TypedDict, total=False):
    """Input for Vrbo Search."""

    adults: NotRequired[int]
    """Number of adult guests (e.g. 2). Range: 1 to 20."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    checkIn: Required[str]
    """Check-in date in YYYY-MM-DD format (e.g. 2027-01-15). Today or later."""
    checkOut: Required[str]
    """Check-out date in YYYY-MM-DD format (e.g. 2027-01-18). After the check-in date."""
    childrenAges: NotRequired[list[int]]
    """Age of each child guest, one entry per child (e.g. [5, 8] for two children aged 5 and 8). Omit it when no children are staying."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of listings to return (1-50, default 50). The price is the same whatever the limit. Range: 1 to 50. Default: 50."""
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
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class VrboListingData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    address: VrboListingAddres | None = Field(
        default=None,
        description="Where the property is. Vrbo shows the area, not the street.",
    )
    amenities: list[VrboListingAmenitie] | None = Field(
        default=None,
        description="Amenities grouped as Vrbo groups them (Essentials, Kitchen, Outdoor...). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    availability_message: str | None = Field(
        default=None,
        alias="availabilityMessage",
        description="Vrbo's reason when it cannot be booked for the stay (e.g. the dates are taken, or too many guests); null when it can.",
    )
    available: bool | None = Field(
        default=None, description="Whether the property can be booked for the stay."
    )
    bathrooms: float | None = Field(
        default=None,
        description="Number of bathrooms, or null when the listing does not say (a 3+ shows as 3).",
    )
    bedrooms: int | None = Field(
        default=None,
        description="Number of bedrooms, or null when the listing does not say.",
    )
    beds: int | None = Field(
        default=None,
        description="Number of beds, or null when the listing does not say.",
    )
    description: str | None = Field(
        default=None,
        description="Full listing description written by the host. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    fees_note: str | None = Field(
        default=None,
        alias="feesNote",
        description="Vrbo's note on what prices include.",
    )
    house_rules: list[VrboListingHouseRule] | None = Field(
        default=None,
        alias="houseRules",
        description="House rules: check-in and check-out times, minimum age, children, events, pets, smoking and the host's own rules.",
    )
    id: str = Field(description="Vrbo property ID, the id vrbo.search returns.")
    images: list[VrboListingImage] | None = Field(
        default=None,
        description="Every listing photo, in Vrbo's order. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    important_info: list[VrboListingImportantInfo] | None = Field(
        default=None,
        alias="importantInfo",
        description="Important information the host and Vrbo publish: fees, deposits, safety features, registration numbers.",
    )
    latitude: float | None = Field(
        default=None,
        description="Latitude of the property. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    listing_id: str | None = Field(
        default=None,
        alias="listingId",
        description="Vrbo's public listing number, the one in the listing link (e.g. 2394927 or 249998ha).",
    )
    longitude: float | None = Field(
        default=None,
        description="Longitude of the property. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(description="Listing title.")
    property_type: str | None = Field(
        default=None,
        alias="propertyType",
        description="Property type (e.g. House, Condo), when Vrbo states it.",
    )
    rating: float | None = Field(
        default=None,
        description="Average guest rating on ratingScale (Vrbo rates out of 10), or null when the property has no reviews.",
    )
    rating_categories: list[VrboListingRatingCategorie] | None = Field(
        default=None,
        alias="ratingCategories",
        description="Average score per rating category (Cleanliness, Check-in, Communication, Location, Listing accuracy), on ratingScale.",
    )
    rating_label: str | None = Field(
        default=None,
        alias="ratingLabel",
        description="Vrbo's word for the rating (e.g. Exceptional, Wonderful).",
    )
    rating_scale: float | None = Field(
        default=None,
        alias="ratingScale",
        description="Top of the rating scale, 10 on Vrbo.",
    )
    reviews: list[VrboListingReview] | None = Field(
        default=None,
        description="Up to 10 of the latest guest reviews; reviewsCount has the total.",
    )
    reviews_count: int | None = Field(
        default=None, alias="reviewsCount", description="Total number of guest reviews."
    )
    sleeps: int | None = Field(
        default=None,
        description="Most guests the property sleeps. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    space_overview: list[str] | None = Field(
        default=None,
        alias="spaceOverview",
        description="Vrbo's summary chips for the space, as shown (e.g. 4 bedrooms, 3+ bathrooms, Sleeps 10); keeps a 3+ that bathrooms reads as 3. Some listings separate the chips with a lone • entry.",
    )
    stay: VrboListingStay | None = Field(
        default=None,
        description="The stay that availability and prices were checked for. When no dates were sent, Vrbo picks them.",
    )
    tagline: str | None = Field(
        default=None, description="Short tagline under the title, when Vrbo shows one."
    )
    units: list[VrboListingUnit] | None = Field(
        default=None,
        description="Bookable units with their price for the stay; empty when the property cannot be booked for it.",
    )
    url: str = Field(description="Link to the listing on Vrbo.")


class VrboListingAddres(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City.")
    country_code_iso3: str | None = Field(
        default=None,
        alias="countryCodeIso3",
        description="Three-letter ISO 3166 country code (e.g. USA, PRT).",
    )
    line: str | None = Field(
        default=None,
        description="Address line as Vrbo shows it (e.g. South Lake Tahoe, CA).",
    )
    parent_region: str | None = Field(
        default=None,
        alias="parentRegion",
        description="Wider area Vrbo files the property under.",
    )
    region: str | None = Field(default=None, description="State, province or region.")


class VrboListingAmenitie(BaseModel):
    model_config = ConfigDict(extra="allow")

    group: str = Field(description="Group name.")
    items: list[str] | None = Field(
        default=None, description="Amenities in this group."
    )


class VrboListingHouseRule(BaseModel):
    model_config = ConfigDict(extra="allow")

    blocks: list[VrboListingBlock] | None = Field(
        default=None,
        description="Blocks of the section, each with an optional heading.",
    )
    title: str | None = Field(default=None, description="Section title.")


class VrboListingBlock(BaseModel):
    model_config = ConfigDict(extra="allow")

    heading: str | None = Field(
        default=None, description="Block heading (e.g. Pets), or null."
    )
    lines: list[str] | None = Field(default=None, description="Lines of the block.")


class VrboListingImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    caption: str | None = Field(
        default=None, description="Photo caption (e.g. Exterior, Kitchen)."
    )
    url: str = Field(description="Photo URL.")


class VrboListingImportantInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    blocks: list[VrboListingBlock] | None = Field(
        default=None,
        description="Blocks of the section, each with an optional heading.",
    )
    title: str | None = Field(default=None, description="Section title.")


class VrboListingRatingCategorie(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: str = Field(description="Category name.")
    score: float | None = Field(
        default=None, description="Average score in this category."
    )


class VrboListingReview(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    highlights: list[str] | None = Field(
        default=None,
        description="What the guest liked or disliked, as Vrbo summarizes it.",
    )
    id: str = Field(description="Review ID.")
    is_verified: bool | None = Field(
        default=None,
        alias="isVerified",
        description="Whether Vrbo marks the review as from a verified stay.",
    )
    language: str | None = Field(
        default=None,
        description="Language of the review as a locale code (e.g. en_US).",
    )
    rating: float | None = Field(
        default=None, description="Guest's score on ratingScale."
    )
    rating_label: str | None = Field(
        default=None,
        alias="ratingLabel",
        description="Vrbo's word for the score (e.g. Excellent).",
    )
    rating_scale: float | None = Field(
        default=None,
        alias="ratingScale",
        description="Top of the score scale, 10 on Vrbo.",
    )
    stay: str | None = Field(
        default=None,
        description="Stay the review is about, as Vrbo states it (e.g. Stayed 4 nights in Oct 2026).",
    )
    text: str | None = Field(default=None, description="Review text.")
    title: str | None = Field(
        default=None, description="Review title, when the guest wrote one."
    )


class VrboListingStay(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    adults: int | None = Field(default=None, description="Number of adult guests.")
    check_in: str | None = Field(
        default=None, alias="checkIn", description="Check-in date, YYYY-MM-DD."
    )
    check_out: str | None = Field(
        default=None, alias="checkOut", description="Check-out date, YYYY-MM-DD."
    )
    children_ages: list[int] | None = Field(
        default=None,
        alias="childrenAges",
        description="Age of each child guest; empty when none.",
    )


class VrboListingUnit(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    features: list[str] | None = Field(
        default=None, description="Unit features (e.g. Sleeps 6)."
    )
    id: str = Field(description="Unit ID.")
    name: str | None = Field(default=None, description="Unit name.")
    rate_plans: list[VrboListingRatePlan] | None = Field(
        default=None,
        alias="ratePlans",
        description="Prices offered for the unit for the stay, fees included.",
    )


class VrboListingRatePlan(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None, description="ISO 4217 currency code of the prices."
    )
    price_per_night: float | None = Field(
        default=None,
        alias="pricePerNight",
        description="Average price per night, fees included, in currency.",
    )
    total_price: float | None = Field(
        default=None,
        alias="totalPrice",
        description="Total price for the stay, fees included, in currency.",
    )
    total_price_text: str | None = Field(
        default=None,
        alias="totalPriceText",
        description="Total price as Vrbo displays it (e.g. $2,630).",
    )


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

    def listing(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[VrboListingInput],
    ) -> RunResult[VrboListingData]:
        """Vrbo Listing

        Get one Vrbo vacation rental by its property ID: name, link, address,
        coordinates, bedrooms, bathrooms, beds and guest capacity, guest rating with
        category scores and review count, amenities by group, full description,
        house rules, important information, availability and price for your dates
        (total and average per night, fees included), every photo with its caption
        and the latest guest reviews, as normalized JSON. Takes the id vrbo.search
        returns.

        Price: $0.00085 per request.

        Example:
            res = client.vrbo.listing(adults=2, checkIn="2026-12-23", checkOut="2026-12-26", propertyId="69764328")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "vrbo.listing", dict(input), options
        )
        return RunResult[VrboListingData].model_validate(raw)

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

        Price: $0.00085 per request.

        Example:
            res = client.vrbo.search(adults=2, checkIn="2026-12-23", checkOut="2026-12-26", location="Lake Tahoe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "vrbo.search", dict(input), options
        )
        return RunResult[VrboSearchData].model_validate(raw)


class AsyncVrboNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def listing(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[VrboListingInput],
    ) -> RunResult[VrboListingData]:
        """Vrbo Listing

        Get one Vrbo vacation rental by its property ID: name, link, address,
        coordinates, bedrooms, bathrooms, beds and guest capacity, guest rating with
        category scores and review count, amenities by group, full description,
        house rules, important information, availability and price for your dates
        (total and average per night, fees included), every photo with its caption
        and the latest guest reviews, as normalized JSON. Takes the id vrbo.search
        returns.

        Price: $0.00085 per request.

        Example:
            res = client.vrbo.listing(adults=2, checkIn="2026-12-23", checkOut="2026-12-26", propertyId="69764328")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "vrbo.listing", dict(input), options
        )
        return RunResult[VrboListingData].model_validate(raw)

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

        Price: $0.00085 per request.

        Example:
            res = client.vrbo.search(adults=2, checkIn="2026-12-23", checkOut="2026-12-26", location="Lake Tahoe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "vrbo.search", dict(input), options
        )
        return RunResult[VrboSearchData].model_validate(raw)
