# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the slickdeals platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SlickdealsDealInput(TypedDict, total=False):
    """Input for Slickdeals Deal."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Slickdeals deal page URL, e.g. https://slickdeals.net/f/20177112-lg-55-c6-series-oled-evo-ai-4k-smart-webos-tv-2026-best-buy-amazon-999-99."""


class SlickdealsSearchInput(TypedDict, total=False):
    """Input for Slickdeals Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    hideExpired: NotRequired[bool]
    """Optional; true leaves out deals the community marked expired."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum deal price in USD; deals without a numeric price are left out. Minimum: 0."""
    minDiscount: NotRequired[int]
    """Optional; keep only deals at least this many percent off the list price, e.g. 50. Range: 1 to 99."""
    minPrice: NotRequired[float]
    """Optional minimum deal price in USD; deals without a numeric price are left out. Minimum: 0."""
    page: NotRequired[int]
    """1-based page of 40 deals; Slickdeals stops at page 25. Each page is billed as one request. Range: 1 to 25. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "airpods" or "laptop"."""
    sort: NotRequired[
        Literal["best_match", "new", "popular", "price_low", "price_high"]
    ]
    """Result order; omit for Slickdeals' relevance order (e.g. new for the most recently posted deals first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SlickdealsDealData(BaseModel):
    items: list[SlickdealsDealItem] = Field(
        description="Deal detail records (one per requested deal URL). Populated whenever the provider has data for the entity."
    )


class SlickdealsDealItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    asin: str | None = Field(
        default=None,
        description="Amazon ASIN of the product when the deal links to Amazon, or null otherwise.",
    )
    author: str | None = Field(
        default=None,
        description="Username of the member who posted the deal, or null when not shown.",
    )
    brand: str | None = Field(
        default=None,
        description="Brand Slickdeals files the deal under, or null when none.",
    )
    category: str | None = Field(
        default=None,
        description='Slickdeals category, e.g. "4K TVs", or null when none.',
    )
    comments_count: int | None = Field(
        default=None,
        alias="commentsCount",
        description="Number of comments on the deal, or null when not reported.",
    )
    coupon_code: str | None = Field(
        default=None,
        alias="couponCode",
        description="Coupon code the deal needs, or null when it needs none.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the deal was posted; null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is posted.',
    )
    deal_id: str = Field(
        alias="dealId",
        description="Slickdeals deal id. Populated whenever the provider has data for the entity.",
    )
    deal_link: str | None = Field(
        default=None,
        alias="dealLink",
        description="Slickdeals' \"Get Deal\" link, which redirects to the store's offer, or null when the deal has none.",
    )
    description: str | None = Field(
        default=None,
        description="Deal description as posted, or null when it has none.",
    )
    image: str | None = Field(default=None, description="Primary deal image URL.")
    images: list[str] | None = Field(default=None, description="Deal image URLs.")
    is_expired: bool | None = Field(
        default=None,
        alias="isExpired",
        description="True when the community marked the deal expired, or null when not reported.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="List price the deal compares against, or null when not posted.",
    )
    price: float | None = Field(
        default=None,
        description="Deal price in USD, or null when the deal has no numeric price.",
    )
    price_is_from: bool | None = Field(
        default=None,
        alias="priceIsFrom",
        description='True when the price is a starting ("from") price, false when it is the price, or null when not reported.',
    )
    price_type: str | None = Field(
        default=None,
        alias="priceType",
        description='How Slickdeals qualifies the price, e.g. "fixed" for a plain price, or null when the deal has no numeric price.',
    )
    score: int | None = Field(
        default=None,
        description="Net community thumbs score, or null when not reported.",
    )
    store: str | None = Field(
        default=None,
        description='Store selling the deal, e.g. "Best Buy", or null when not posted.',
    )
    title: str = Field(
        description="Deal title as posted. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Slickdeals deal page URL. Populated whenever the provider has data for the entity."
    )
    views_count: int | None = Field(
        default=None,
        alias="viewsCount",
        description="Number of views of the deal, or null when not reported.",
    )


class SlickdealsSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when another page of deals follows this one (request it with page + 1), or null when not reported.",
    )
    items: list[SlickdealsSearchItem] = Field(
        description="Matching Slickdeals deal records for the requested page. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total number of matching deals Slickdeals reports (it stops counting at 1000), or null when not reported.",
    )


class SlickdealsSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None,
        description="Username of the member who posted the deal, or null when not shown.",
    )
    comments_count: int | None = Field(
        default=None,
        alias="commentsCount",
        description="Number of comments on the deal, or null when not reported.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the deal was posted; null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is posted.',
    )
    deal_id: str = Field(
        alias="dealId",
        description="Slickdeals deal id; use the deal URL with the Slickdeals Deal SKU. Populated whenever the provider has data for the entity.",
    )
    discount_percent: float | None = Field(
        default=None,
        alias="discountPercent",
        description="Percent off the list price, e.g. 21.9, or null when no list price is posted.",
    )
    image: str | None = Field(default=None, description="Deal thumbnail image URL.")
    is_expired: bool | None = Field(
        default=None,
        alias="isExpired",
        description="True when the community marked the deal expired, or null when not reported.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="List price the deal compares against, or null when not posted.",
    )
    price: float | None = Field(
        default=None,
        description="Deal price in USD, or null when the deal has no numeric price.",
    )
    price_is_from: bool | None = Field(
        default=None,
        alias="priceIsFrom",
        description='True when the price is a starting ("from") price, false when it is the price, or null when not reported.',
    )
    price_type: str | None = Field(
        default=None,
        alias="priceType",
        description='How Slickdeals qualifies the price, e.g. "fixed" for a plain price, or null when the deal has no numeric price.',
    )
    score: int | None = Field(
        default=None,
        description="Net community thumbs score, or null when not reported.",
    )
    store: str | None = Field(
        default=None,
        description='Store selling the deal, e.g. "Amazon", or null when not posted.',
    )
    title: str = Field(
        description="Deal title as posted. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Slickdeals deal page URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    views_count: int | None = Field(
        default=None,
        alias="viewsCount",
        description="Number of views of the deal, or null when not reported.",
    )


class SlickdealsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def deal(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SlickdealsDealInput],
    ) -> RunResult[SlickdealsDealData]:
        """Slickdeals Deal

        Fetch one Slickdeals deal by URL and get title, price, list price, store,
        coupon code, score, views, comments, and description in one normalized
        response.

        Price: $0.00213 per request.

        Example:
            res = client.slickdeals.deal(url="https://slickdeals.net/f/20177112-lg-55-c6-series-oled-evo-ai-4k-smart-webos-tv-2026-best-buy-amazon-999-99")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "slickdeals.deal", dict(input), options
        )
        return RunResult[SlickdealsDealData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SlickdealsSearchInput],
    ) -> RunResult[SlickdealsSearchData]:
        """Slickdeals Search

        Search Slickdeals deals by keyword with optional sort, price, discount, and
        page filters and get title, price, list price, store, score, and comment
        count for each deal in one normalized response.

        Price: $0.00213 per request.

        Example:
            res = client.slickdeals.search(query="airpods")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "slickdeals.search", dict(input), options
        )
        return RunResult[SlickdealsSearchData].model_validate(raw)


class AsyncSlickdealsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def deal(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SlickdealsDealInput],
    ) -> RunResult[SlickdealsDealData]:
        """Slickdeals Deal

        Fetch one Slickdeals deal by URL and get title, price, list price, store,
        coupon code, score, views, comments, and description in one normalized
        response.

        Price: $0.00213 per request.

        Example:
            res = client.slickdeals.deal(url="https://slickdeals.net/f/20177112-lg-55-c6-series-oled-evo-ai-4k-smart-webos-tv-2026-best-buy-amazon-999-99")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "slickdeals.deal", dict(input), options
        )
        return RunResult[SlickdealsDealData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SlickdealsSearchInput],
    ) -> RunResult[SlickdealsSearchData]:
        """Slickdeals Search

        Search Slickdeals deals by keyword with optional sort, price, discount, and
        page filters and get title, price, list price, store, score, and comment
        count for each deal in one normalized response.

        Price: $0.00213 per request.

        Example:
            res = client.slickdeals.search(query="airpods")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "slickdeals.search", dict(input), options
        )
        return RunResult[SlickdealsSearchData].model_validate(raw)
