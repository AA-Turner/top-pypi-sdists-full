# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the google_hotels platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GoogleHotelsDetailsInput(TypedDict, total=False):
    """Input for Google Hotel Details."""

    adults: NotRequired[int]
    """Number of adult guests (default 2). Minimum: 1. Default: 2."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    checkIn: Required[str]
    """Check-in date in YYYY-MM-DD format (e.g. 2027-04-13). Today or later."""
    checkOut: Required[str]
    """Check-out date in YYYY-MM-DD format (e.g. 2027-04-15). After the check-in date."""
    childrenAges: NotRequired[list[int]]
    """Age of each child guest, one entry per child (e.g. [5, 8] for two children aged 5 and 8). Omit it when no children are staying."""
    country: Required[
        Literal[
            "ad",
            "ae",
            "af",
            "ag",
            "al",
            "am",
            "ao",
            "aq",
            "ar",
            "as",
            "at",
            "au",
            "az",
            "ba",
            "bb",
            "bd",
            "be",
            "bf",
            "bg",
            "bh",
            "bi",
            "bj",
            "bn",
            "bo",
            "bq",
            "br",
            "bs",
            "bt",
            "bw",
            "bz",
            "ca",
            "cc",
            "cd",
            "cf",
            "cg",
            "ch",
            "ci",
            "ck",
            "cl",
            "cm",
            "cn",
            "co",
            "cr",
            "cv",
            "cw",
            "cx",
            "cy",
            "cz",
            "de",
            "dj",
            "dk",
            "dm",
            "do",
            "dz",
            "ec",
            "ee",
            "eg",
            "er",
            "es",
            "et",
            "fi",
            "fj",
            "fm",
            "fr",
            "ga",
            "gb",
            "gd",
            "ge",
            "gg",
            "gh",
            "gm",
            "gn",
            "gq",
            "gr",
            "gs",
            "gt",
            "gu",
            "gw",
            "gy",
            "hm",
            "hn",
            "hr",
            "ht",
            "hu",
            "id",
            "ie",
            "il",
            "im",
            "in",
            "iq",
            "is",
            "it",
            "je",
            "jm",
            "jo",
            "jp",
            "ke",
            "kg",
            "kh",
            "ki",
            "km",
            "kn",
            "kr",
            "kw",
            "kz",
            "la",
            "lb",
            "lc",
            "li",
            "lk",
            "lr",
            "ls",
            "lt",
            "lu",
            "lv",
            "ly",
            "ma",
            "mc",
            "md",
            "me",
            "mf",
            "mg",
            "mh",
            "mk",
            "ml",
            "mm",
            "mn",
            "mp",
            "mr",
            "mt",
            "mu",
            "mv",
            "mw",
            "mx",
            "my",
            "mz",
            "na",
            "nc",
            "ne",
            "nf",
            "ng",
            "ni",
            "nl",
            "no",
            "np",
            "nr",
            "nu",
            "nz",
            "om",
            "pa",
            "pe",
            "pf",
            "pg",
            "ph",
            "pk",
            "pl",
            "pm",
            "pn",
            "pt",
            "pw",
            "py",
            "qa",
            "ro",
            "rs",
            "rw",
            "sa",
            "sb",
            "sc",
            "se",
            "sg",
            "sh",
            "si",
            "sk",
            "sl",
            "sm",
            "sn",
            "so",
            "sr",
            "st",
            "sv",
            "sx",
            "sz",
            "td",
            "tf",
            "tg",
            "th",
            "tj",
            "tk",
            "tl",
            "tm",
            "tn",
            "to",
            "tr",
            "tt",
            "tv",
            "tz",
            "ua",
            "ug",
            "um",
            "us",
            "uy",
            "uz",
            "va",
            "vc",
            "ve",
            "vn",
            "vu",
            "wf",
            "ws",
            "ye",
            "za",
            "zm",
            "zw",
        ]
    ]
    """Two-letter lowercase ISO 3166-1 country code of the destination (e.g. us, pt, jp). It must be the country the hotels are in: results are searched from that country."""
    currency: NotRequired[str]
    """ISO 4217 currency code for prices (e.g. USD, EUR, JPY; default USD). Default: USD."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    propertyToken: Required[str]
    """Google Hotels property ID of the hotel, the propertyToken google_hotels.search returns for it."""
    requireFields: NotRequired[list[Literal["images", "stars", "totalPrice"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `stars` or `images`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a hotel that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleHotelsSearchInput(TypedDict, total=False):
    """Input for Google Hotels Search."""

    adults: NotRequired[int]
    """Number of adult guests (default 2). Minimum: 1. Default: 2."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    checkIn: Required[str]
    """Check-in date in YYYY-MM-DD format (e.g. 2027-04-13). Today or later."""
    checkOut: Required[str]
    """Check-out date in YYYY-MM-DD format (e.g. 2027-04-15). After the check-in date."""
    childrenAges: NotRequired[list[int]]
    """Age of each child guest, one entry per child (e.g. [5, 8] for two children aged 5 and 8). Omit it when no children are staying."""
    country: Required[
        Literal[
            "ad",
            "ae",
            "af",
            "ag",
            "al",
            "am",
            "ao",
            "aq",
            "ar",
            "as",
            "at",
            "au",
            "az",
            "ba",
            "bb",
            "bd",
            "be",
            "bf",
            "bg",
            "bh",
            "bi",
            "bj",
            "bn",
            "bo",
            "bq",
            "br",
            "bs",
            "bt",
            "bw",
            "bz",
            "ca",
            "cc",
            "cd",
            "cf",
            "cg",
            "ch",
            "ci",
            "ck",
            "cl",
            "cm",
            "cn",
            "co",
            "cr",
            "cv",
            "cw",
            "cx",
            "cy",
            "cz",
            "de",
            "dj",
            "dk",
            "dm",
            "do",
            "dz",
            "ec",
            "ee",
            "eg",
            "er",
            "es",
            "et",
            "fi",
            "fj",
            "fm",
            "fr",
            "ga",
            "gb",
            "gd",
            "ge",
            "gg",
            "gh",
            "gm",
            "gn",
            "gq",
            "gr",
            "gs",
            "gt",
            "gu",
            "gw",
            "gy",
            "hm",
            "hn",
            "hr",
            "ht",
            "hu",
            "id",
            "ie",
            "il",
            "im",
            "in",
            "iq",
            "is",
            "it",
            "je",
            "jm",
            "jo",
            "jp",
            "ke",
            "kg",
            "kh",
            "ki",
            "km",
            "kn",
            "kr",
            "kw",
            "kz",
            "la",
            "lb",
            "lc",
            "li",
            "lk",
            "lr",
            "ls",
            "lt",
            "lu",
            "lv",
            "ly",
            "ma",
            "mc",
            "md",
            "me",
            "mf",
            "mg",
            "mh",
            "mk",
            "ml",
            "mm",
            "mn",
            "mp",
            "mr",
            "mt",
            "mu",
            "mv",
            "mw",
            "mx",
            "my",
            "mz",
            "na",
            "nc",
            "ne",
            "nf",
            "ng",
            "ni",
            "nl",
            "no",
            "np",
            "nr",
            "nu",
            "nz",
            "om",
            "pa",
            "pe",
            "pf",
            "pg",
            "ph",
            "pk",
            "pl",
            "pm",
            "pn",
            "pt",
            "pw",
            "py",
            "qa",
            "ro",
            "rs",
            "rw",
            "sa",
            "sb",
            "sc",
            "se",
            "sg",
            "sh",
            "si",
            "sk",
            "sl",
            "sm",
            "sn",
            "so",
            "sr",
            "st",
            "sv",
            "sx",
            "sz",
            "td",
            "tf",
            "tg",
            "th",
            "tj",
            "tk",
            "tl",
            "tm",
            "tn",
            "to",
            "tr",
            "tt",
            "tv",
            "tz",
            "ua",
            "ug",
            "um",
            "us",
            "uy",
            "uz",
            "va",
            "vc",
            "ve",
            "vn",
            "vu",
            "wf",
            "ws",
            "ye",
            "za",
            "zm",
            "zw",
        ]
    ]
    """Two-letter lowercase ISO 3166-1 country code of the destination (e.g. us, pt, jp). It must be the country the hotels are in: results are searched from that country."""
    currency: NotRequired[str]
    """ISO 4217 currency code for prices (e.g. USD, EUR, JPY; default USD). Default: USD."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """What to search for, usually a destination or landmark (e.g. hotels near times square new york)."""
    requireFields: NotRequired[list[Literal["amenities", "description", "totalPrice"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `totalPrice` or `amenities`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a hotel that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleHotelsDetailsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    address: str | None = Field(
        default=None,
        description="Street address. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    amenities: list[GoogleHotelsDetailsAmenitie] | None = Field(
        default=None,
        description="Amenities Google lists for the hotel, each with whether the hotel offers it. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    check_in_time: str | None = Field(
        default=None,
        alias="checkInTime",
        description="Earliest check-in time, 24-hour HH:MM local time. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    check_out_time: str | None = Field(
        default=None,
        alias="checkOutTime",
        description="Latest check-out time, 24-hour HH:MM local time. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None,
        description="ISO 4217 currency code every price in this response is in. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None,
        description="Preview photo URLs of the hotel, or null when unknown.",
    )
    latitude: float | None = Field(
        default=None,
        description="Latitude of the hotel. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    longitude: float | None = Field(
        default=None,
        description="Longitude of the hotel. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(description="Hotel name.")
    phone: str | None = Field(
        default=None,
        description="Phone number as published. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    price_per_night: float | None = Field(
        default=None,
        alias="pricePerNight",
        description="Lowest nightly price for the requested dates and guests, in the response currency, or null when no price is offered. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    prices: list[GoogleHotelsDetailsPrice] | None = Field(
        default=None,
        description="Nightly prices offered by each booking site for the requested dates. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    property_token: str = Field(
        alias="propertyToken", description="Google Hotels property ID."
    )
    rating: float | None = Field(
        default=None,
        description="Average guest rating out of 5, or null when the hotel has no ratings. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of guest reviews. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    stars: int | None = Field(
        default=None, description="Hotel star class (1-5), or null when unknown."
    )
    total_price: float | None = Field(
        default=None,
        alias="totalPrice",
        description="Lowest total price for the whole stay, in the response currency, or null when unknown.",
    )
    website: str | None = Field(
        default=None,
        description="The hotel's own website. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class GoogleHotelsDetailsAmenitie(BaseModel):
    model_config = ConfigDict(extra="allow")

    available: bool | None = Field(
        default=None,
        description="Whether the hotel offers it. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(description="Amenity name (e.g. Wi-Fi, Pool).")


class GoogleHotelsDetailsPrice(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    price_per_night: float | None = Field(
        default=None,
        alias="pricePerNight",
        description="Nightly price on this site, in the response currency. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    site: str = Field(description="Booking site name (e.g. Booking.com).")
    total_price: float | None = Field(
        default=None,
        alias="totalPrice",
        description="Total price for the stay on this site, or null when unknown.",
    )
    url: str | None = Field(
        default=None,
        description="Booking link for this offer. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class GoogleHotelsSearchData(BaseModel):
    currency: str | None = Field(
        default=None,
        description="ISO 4217 currency code every price in this response is in. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    hotels: list[GoogleHotelsSearchHotel] = Field(
        description="Hotels matching the search, in Google's order. Populated whenever the provider has data for the entity."
    )


class GoogleHotelsSearchHotel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    amenities: list[str] | None = Field(
        default=None,
        description="Highlighted amenities (e.g. Free Wi-Fi, Parking), or null when unknown.",
    )
    description: str | None = Field(
        default=None,
        description="Short description of the hotel, or null when unknown.",
    )
    images: list[str] | None = Field(
        default=None, description="Preview photo URLs of the hotel."
    )
    latitude: float | None = Field(
        default=None,
        description="Latitude of the hotel. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    longitude: float | None = Field(
        default=None,
        description="Longitude of the hotel. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(description="Hotel name.")
    price_per_night: float | None = Field(
        default=None,
        alias="pricePerNight",
        description="Lowest nightly price for the requested dates and guests, in the response currency, or null when no price is offered. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    property_token: str = Field(
        alias="propertyToken",
        description="Google Hotels property ID. Pass it to google_hotels.details for this hotel's full record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average guest rating out of 5, or null when the hotel has no ratings. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of guest reviews. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    stars: int | None = Field(
        default=None,
        description="Hotel star class (1-5), or null when the property has none.",
    )
    total_price: float | None = Field(
        default=None,
        alias="totalPrice",
        description="Lowest total price for the whole stay, in the response currency, or null when unknown.",
    )


class GoogleHotelsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleHotelsDetailsInput],
    ) -> RunResult[GoogleHotelsDetailsData]:
        """Google Hotel Details

        Get one hotel from Google Hotels by its property ID: address, phone,
        website, rating, nightly price, prices from each booking site, amenities and
        check-in times as normalized JSON.

        Price: $0.0015 per request.

        Example:
            res = client.google_hotels.details(checkIn="2026-12-01", checkOut="2026-12-03", country="us", propertyToken="ChcImaG28Zbom8uuARoKL20vMDNncTd2NBAB")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_hotels.details", dict(input), options
        )
        return RunResult[GoogleHotelsDetailsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleHotelsSearchInput],
    ) -> RunResult[GoogleHotelsSearchData]:
        """Google Hotels Search

        Search Google Hotels by destination and dates and get hotels with their
        Google property ID, nightly price, rating, review count, coordinates, star
        class and photos as normalized JSON.

        Price: $0.0015 per request.

        Example:
            res = client.google_hotels.search(checkIn="2026-12-01", checkOut="2026-12-03", country="us", query="hotels near times square new york")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_hotels.search", dict(input), options
        )
        return RunResult[GoogleHotelsSearchData].model_validate(raw)


class AsyncGoogleHotelsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleHotelsDetailsInput],
    ) -> RunResult[GoogleHotelsDetailsData]:
        """Google Hotel Details

        Get one hotel from Google Hotels by its property ID: address, phone,
        website, rating, nightly price, prices from each booking site, amenities and
        check-in times as normalized JSON.

        Price: $0.0015 per request.

        Example:
            res = client.google_hotels.details(checkIn="2026-12-01", checkOut="2026-12-03", country="us", propertyToken="ChcImaG28Zbom8uuARoKL20vMDNncTd2NBAB")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_hotels.details", dict(input), options
        )
        return RunResult[GoogleHotelsDetailsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleHotelsSearchInput],
    ) -> RunResult[GoogleHotelsSearchData]:
        """Google Hotels Search

        Search Google Hotels by destination and dates and get hotels with their
        Google property ID, nightly price, rating, review count, coordinates, star
        class and photos as normalized JSON.

        Price: $0.0015 per request.

        Example:
            res = client.google_hotels.search(checkIn="2026-12-01", checkOut="2026-12-03", country="us", query="hotels near times square new york")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_hotels.search", dict(input), options
        )
        return RunResult[GoogleHotelsSearchData].model_validate(raw)
