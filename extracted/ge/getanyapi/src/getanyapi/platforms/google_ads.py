# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the google_ads platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult
from .._pagination import (
    AsyncPaginator,
    Paginator,
    apaginate,
    paginate,
)

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GoogleAdsAdDetailsInput(TypedDict, total=False):
    """Input for Google Ads Ad Details."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Google Ads Transparency Center creative URL (e.g. "https://adstransparency.google.com/advertiser/AR.../creative/CR...")."""


class GoogleAdsAdvertiserSearchInput(TypedDict, total=False):
    """Input for Google Ads Advertiser Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Advertiser name or keyword to search for (e.g. "lululemon")."""
    region: NotRequired[str]
    """Two-letter country code to scope results (e.g. "AU", "CA"). Defaults to US."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleAdsCompanyAdsInput(TypedDict, total=False):
    """Input for Google Ads Company Ads."""

    advertiserId: NotRequired[str]
    """Advertiser ID. Provide either domain or advertiserId."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor."""
    domain: NotRequired[str]
    """Company domain (e.g. "lululemon.com"). Provide either domain or advertiserId."""
    endDate: NotRequired[str]
    """Only return ads first shown on or before this date, format YYYY-MM-DD (e.g. 2024-12-31)."""
    format: NotRequired[Literal["text", "image", "video"]]
    """Ad format filter."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    platform: NotRequired[
        Literal[
            "google_maps", "google_play", "google_search", "google_shopping", "youtube"
        ]
    ]
    """Platform filter."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[str]
    """Two-letter country code to scope results (e.g. "US", "AU")."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Only return ads first shown on or after this date, format YYYY-MM-DD (e.g. 2024-01-01)."""
    topic: NotRequired[Literal["all", "political"]]
    """Search topic. "political" requires a region."""


class GoogleAdsSearchInput(TypedDict, total=False):
    """Input for Google Ads Transparency."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). You are billed per result returned, so a lower limit costs less. Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """A Google Ads Transparency Center URL for a selected advertiser or domain (e.g. https://adstransparency.google.com/advertiser/AR01614014350098432001?region=US)."""


class GoogleAdsAdDetailsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    advertiser_id: str = Field(
        alias="advertiserId",
        description="Populated whenever the provider has data for the entity.",
    )
    creative_id: str = Field(
        alias="creativeId",
        description="Populated whenever the provider has data for the entity.",
    )
    first_shown: str = Field(alias="firstShown", description="ISO 8601 date.")
    format: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    impressions_max: int | None = Field(
        alias="impressionsMax",
        description="Upper bound of the impressions range. Null when Google does not publish one for this creative.",
    )
    impressions_min: int | None = Field(
        alias="impressionsMin",
        description="Lower bound of the impressions range. Null when Google does not publish one for this creative.",
    )
    last_shown: str = Field(alias="lastShown", description="ISO 8601 date.")
    url: str | None = Field(
        default=None, description="Google Ads Transparency Center URL for the creative."
    )
    variations: list[GoogleAdsAdDetailsVariation] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GoogleAdsAdDetailsVariation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    all_text: str = Field(alias="allText")
    description: str
    destination_url: str = Field(alias="destinationUrl")
    headline: str
    image_url: str = Field(alias="imageUrl")


class GoogleAdsAdvertiserSearchData(BaseModel):
    advertisers: list[GoogleAdsAdvertiserSearchAdvertiser] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GoogleAdsAdvertiserSearchAdvertiser(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ads_estimate: int = Field(
        alias="adsEstimate",
        description="Estimated number of ads for this advertiser/region.",
    )
    advertiser_id: str = Field(
        alias="advertiserId",
        description="Populated whenever the provider has data for the entity.",
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    region: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GoogleAdsCompanyAdsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[GoogleAdsCompanyAdsAd] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    ads_estimate: int = Field(
        alias="adsEstimate", description="Estimated total number of ads."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of ads, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class GoogleAdsCompanyAdsAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_url: str = Field(
        alias="adUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    advertiser_id: str = Field(
        alias="advertiserId",
        description="Populated whenever the provider has data for the entity.",
    )
    advertiser_name: str = Field(
        alias="advertiserName",
        description="Populated whenever the provider has data for the entity.",
    )
    creative_id: str = Field(
        alias="creativeId",
        description="Populated whenever the provider has data for the entity.",
    )
    domain: str | None = Field(
        default=None, description="Registrable domain the ad links to."
    )
    first_shown: str = Field(alias="firstShown", description="ISO 8601 date.")
    format: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image_url: str = Field(alias="imageUrl")
    last_shown: str = Field(alias="lastShown", description="ISO 8601 date.")


class GoogleAdsSearchData(BaseModel):
    items: list[GoogleAdsSearchItem] = Field(
        description="Ad records from the Transparency Center: advertiser, ad format, creative details, preview URL, and first/last shown dates. Populated whenever the provider has data for the entity."
    )


class GoogleAdsSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    advertiser: str | None = Field(
        default=None,
        description="Advertiser display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    advertiser_id: str | None = Field(
        default=None,
        alias="advertiserId",
        description="Google Ads advertiser identifier.",
    )
    first_shown_utc: float | None = Field(
        default=None,
        alias="firstShownUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the ad was first shown.",
    )
    format: str | None = Field(
        default=None, description="Ad format, e.g. TEXT, IMAGE, VIDEO."
    )
    id: str = Field(
        description="Google Ads creative identifier. Populated whenever the provider has data for the entity."
    )
    last_shown_utc: float | None = Field(
        default=None,
        alias="lastShownUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the ad was last shown.",
    )
    num_served_days: int | None = Field(
        default=None,
        alias="numServedDays",
        description="Number of days the ad has been served.",
    )
    preview_url: str | None = Field(
        default=None,
        alias="previewUrl",
        description="URL to a rendered preview of the creative.",
    )
    url: str = Field(
        description="Ads Transparency Center URL for the creative. Populated whenever the provider has data for the entity."
    )
    variations: list[GoogleAdsSearchVariation] | None = Field(
        default=None,
        description="Creative variations for the ad, each with image, headline, and body text where present.",
    )


class GoogleAdsSearchVariation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    headline: str | None = Field(default=None, description="Creative headline text.")
    image_url: str | None = Field(
        default=None, alias="imageUrl", description="Creative image URL."
    )
    text: str | None = Field(
        default=None, description="Creative body/description text."
    )


class GoogleAdsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ad_details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsAdDetailsInput],
    ) -> RunResult[GoogleAdsAdDetailsData]:
        """Google Ads Ad Details

        Look up a single Google Ads Transparency Center creative by URL and get its
        format, run dates, impression range, regions, and creative variations as
        clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.google_ads.ad_details(url="https://adstransparency.google.com/advertiser/AR01614014350098432001/creative/CR10449491775734153217")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.ad_details", dict(input), options
        )
        return RunResult[GoogleAdsAdDetailsData].model_validate(raw)

    def advertiser_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsAdvertiserSearchInput],
    ) -> RunResult[GoogleAdsAdvertiserSearchData]:
        """Google Ads Advertiser Search

        Search the Google Ads Transparency Center for advertisers by keyword and get
        matching advertiser IDs, regions, and estimated ad counts as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.google_ads.advertiser_search(query="lululemon")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.advertiser_search", dict(input), options
        )
        return RunResult[GoogleAdsAdvertiserSearchData].model_validate(raw)

    def company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsCompanyAdsInput],
    ) -> RunResult[GoogleAdsCompanyAdsData]:
        """Google Ads Company Ads

        List the ads a company is running from the Google Ads Transparency Center by
        domain or advertiser ID (creative ID, format, ad URL, and first/last shown
        dates) with cursor pagination.

        Price: $0.00085 per request.

        Example:
            res = client.google_ads.company_ads(domain="lululemon.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.company_ads", dict(input), options
        )
        return RunResult[GoogleAdsCompanyAdsData].model_validate(raw)

    def iter_company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsCompanyAdsInput],
    ) -> Paginator[GoogleAdsCompanyAdsAd, GoogleAdsCompanyAdsData]:
        """Iterate Google Ads Company Ads results, following pagination cursors.

        Yields validated `GoogleAdsCompanyAdsAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "google_ads.company_ads",
            dict(input),
            "ads",
            item_model=GoogleAdsCompanyAdsAd,
            data_model=GoogleAdsCompanyAdsData,
            bare=False,
            options=options,
        )

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsSearchInput],
    ) -> RunResult[GoogleAdsSearchData]:
        """Google Ads Transparency

        Pull the ads an advertiser is currently running from the Google Ads
        Transparency Center (creative details, formats, and run dates) as clean
        JSON.

        Price: $0.00006 per request plus $0.00143 per result (maximum $0.0287).

        Example:
            res = client.google_ads.search(limit=3, url="https://adstransparency.google.com/?region=US&domain=nike.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.search", dict(input), options
        )
        return RunResult[GoogleAdsSearchData].model_validate(raw)


class AsyncGoogleAdsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ad_details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsAdDetailsInput],
    ) -> RunResult[GoogleAdsAdDetailsData]:
        """Google Ads Ad Details

        Look up a single Google Ads Transparency Center creative by URL and get its
        format, run dates, impression range, regions, and creative variations as
        clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.google_ads.ad_details(url="https://adstransparency.google.com/advertiser/AR01614014350098432001/creative/CR10449491775734153217")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.ad_details", dict(input), options
        )
        return RunResult[GoogleAdsAdDetailsData].model_validate(raw)

    async def advertiser_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsAdvertiserSearchInput],
    ) -> RunResult[GoogleAdsAdvertiserSearchData]:
        """Google Ads Advertiser Search

        Search the Google Ads Transparency Center for advertisers by keyword and get
        matching advertiser IDs, regions, and estimated ad counts as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.google_ads.advertiser_search(query="lululemon")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.advertiser_search", dict(input), options
        )
        return RunResult[GoogleAdsAdvertiserSearchData].model_validate(raw)

    async def company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsCompanyAdsInput],
    ) -> RunResult[GoogleAdsCompanyAdsData]:
        """Google Ads Company Ads

        List the ads a company is running from the Google Ads Transparency Center by
        domain or advertiser ID (creative ID, format, ad URL, and first/last shown
        dates) with cursor pagination.

        Price: $0.00085 per request.

        Example:
            res = client.google_ads.company_ads(domain="lululemon.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.company_ads", dict(input), options
        )
        return RunResult[GoogleAdsCompanyAdsData].model_validate(raw)

    def iter_company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsCompanyAdsInput],
    ) -> AsyncPaginator[GoogleAdsCompanyAdsAd, GoogleAdsCompanyAdsData]:
        """Iterate Google Ads Company Ads results, following pagination cursors.

        Yields validated `GoogleAdsCompanyAdsAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "google_ads.company_ads",
            dict(input),
            "ads",
            item_model=GoogleAdsCompanyAdsAd,
            data_model=GoogleAdsCompanyAdsData,
            bare=False,
            options=options,
        )

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAdsSearchInput],
    ) -> RunResult[GoogleAdsSearchData]:
        """Google Ads Transparency

        Pull the ads an advertiser is currently running from the Google Ads
        Transparency Center (creative details, formats, and run dates) as clean
        JSON.

        Price: $0.00006 per request plus $0.00143 per result (maximum $0.0287).

        Example:
            res = client.google_ads.search(limit=3, url="https://adstransparency.google.com/?region=US&domain=nike.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_ads.search", dict(input), options
        )
        return RunResult[GoogleAdsSearchData].model_validate(raw)
