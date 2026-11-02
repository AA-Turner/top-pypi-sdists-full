# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the samsclub platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SamsclubProductInput(TypedDict, total=False):
    """Input for Sam's Club Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Sam's Club product page URL, e.g. https://www.samsclub.com/ip/Bounty-Select-A-Size-2-Ply-Paper-Towels-12-Rolls-110-sheets-roll/18040450426. Prices and stock are those of Sam's Club's default club."""


class SamsclubSearchInput(TypedDict, total=False):
    """Input for Sam's Club Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum member price in USD. Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum member price in USD. Minimum: 0."""
    page: NotRequired[int]
    """1-based results page of about 40 to 50 products. Each page is billed as one request. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "paper towels" or "tv"."""
    sort: NotRequired[Literal["best_match", "price_low", "price_high"]]
    """Result sort order; omit for Sam's Club's Best Match (e.g. price_low sorts by lowest price first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SamsclubProductData(BaseModel):
    items: list[SamsclubProductItem] = Field(
        description="Product detail records (one per requested product URL). Populated whenever the provider has data for the entity."
    )


class SamsclubProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    availability: str | None = Field(
        default=None,
        description='Stock status as Sam\'s Club reports it, e.g. "IN_STOCK", or null when not reported.',
    )
    brand: str | None = Field(
        default=None, description="Brand name, or null when not reported."
    )
    club_name: str | None = Field(
        default=None,
        alias="clubName",
        description="Name of the Sam's Club location the price and stock come from, e.g. \"Dallas Sam's Club\", or null when not reported.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown.',
    )
    description: str | None = Field(
        default=None,
        description="Product description text, or null when the listing has none.",
    )
    highlights: list[SamsclubProductHighlight] | None = Field(
        default=None, description="Key facts Sam's Club highlights on the product page."
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None, description="All product image URLs, primary first."
    )
    item_id: str | None = Field(
        default=None,
        alias="itemId",
        description="Sam's Club item id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Price before Instant Savings, or null when the product is not discounted.",
    )
    member_limit: int | None = Field(
        default=None,
        alias="memberLimit",
        description="Most units one member may buy, or null when no limit is shown.",
    )
    model: str | None = Field(
        default=None,
        description="Manufacturer model number, or null when not reported.",
    )
    order_limit: int | None = Field(
        default=None,
        alias="orderLimit",
        description="Most units one order may contain, or null when no limit is shown.",
    )
    price: float | None = Field(
        default=None,
        description="Current member price in USD, or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated.",
    )
    rating_distribution: SamsclubProductRatingDistribution | None = Field(
        default=None,
        alias="ratingDistribution",
        description='Number of reviews at each star rating, keyed "1" through "5".',
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer reviews, or null when the product has none.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    unit_price: str | None = Field(
        default=None,
        alias="unitPrice",
        description='Unit price as Sam\'s Club shows it, e.g. "$0.04/sft", or null when not shown.',
    )
    upc: str | None = Field(
        default=None, description="Universal Product Code, or null when not reported."
    )
    url: str = Field(
        description="Sam's Club product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )


class SamsclubProductHighlight(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: str | None = Field(default=None, description='Highlight name, e.g. "Brand".')
    value: str | None = Field(
        default=None, description='Highlight value, e.g. "Bounty".'
    )


class SamsclubProductRatingDistribution(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    field_1: int | None = Field(
        default=None, alias="1", description="Number of 1-star reviews."
    )
    field_2: int | None = Field(
        default=None, alias="2", description="Number of 2-star reviews."
    )
    field_3: int | None = Field(
        default=None, alias="3", description="Number of 3-star reviews."
    )
    field_4: int | None = Field(
        default=None, alias="4", description="Number of 4-star reviews."
    )
    field_5: int | None = Field(
        default=None, alias="5", description="Number of 5-star reviews."
    )


class SamsclubSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when another page of results follows this one (request it with page + 1), or null when not reported.",
    )
    items: list[SamsclubSearchItem] = Field(
        description="Matching Sam's Club product records for the requested page, sponsored tiles left out. Prices are those of Sam's Club's default club. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Number of organic products Sam's Club returns for the query (sponsored tiles are left out), or null when not reported.",
    )
    total_results_exact: bool | None = Field(
        default=None,
        alias="totalResultsExact",
        description="True when totalResults is an exact count, false when it is an estimate, or null when not reported.",
    )


class SamsclubSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    availability: str | None = Field(
        default=None,
        description='Stock status as Sam\'s Club reports it, e.g. "IN_STOCK", or null when not reported.',
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown.',
    )
    fulfillment: list[str] | None = Field(
        default=None,
        description='Ways the item can be fulfilled at the pickup club, e.g. "PICKUP", "DELIVERY", "SHIPPING"; empty when none is offered.',
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    item_id: str = Field(
        alias="itemId",
        description="Sam's Club item id, the number at the end of a samsclub.com/ip/ URL; use the product URL with the Sam's Club Product SKU. Populated whenever the provider has data for the entity.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Price before Instant Savings, or null when the product is not discounted.",
    )
    pickup_club_id: str | None = Field(
        default=None,
        alias="pickupClubId",
        description="Id of the Sam's Club location whose stock and fulfillment the result reflects, or null when not reported.",
    )
    position: int | None = Field(
        default=None, description="1-based organic position of the result in this page."
    )
    price: float | None = Field(
        default=None,
        description="Current member price in USD, or null when the result shows no price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    promotions: list[str] | None = Field(
        default=None,
        description='Promotion labels shown on the result, e.g. "$40 off" or "Sam\'s Cash Offer"; empty when none.',
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer reviews, or null when the product has none.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Sam's Club product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SamsclubNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SamsclubProductInput],
    ) -> RunResult[SamsclubProductData]:
        """Sam's Club Product

        Fetch a SamsClub.com product by URL and get title, member price, stock,
        brand, model, UPC, rating, description, and images in one normalized
        response.

        Price: $0.00319 per request.

        Example:
            res = client.samsclub.product(url="https://www.samsclub.com/ip/Bounty-Select-A-Size-2-Ply-Paper-Towels-12-Rolls-110-sheets-roll/18040450426")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "samsclub.product", dict(input), options
        )
        return RunResult[SamsclubProductData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SamsclubSearchInput],
    ) -> RunResult[SamsclubSearchData]:
        """Sam's Club Search

        Search SamsClub.com by keyword with optional sort, price-range, and page
        filters and get title, member price, stock, and rating for each product in
        one normalized response.

        Price: $0.00319 per request.

        Example:
            res = client.samsclub.search(query="paper towels")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "samsclub.search", dict(input), options
        )
        return RunResult[SamsclubSearchData].model_validate(raw)


class AsyncSamsclubNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SamsclubProductInput],
    ) -> RunResult[SamsclubProductData]:
        """Sam's Club Product

        Fetch a SamsClub.com product by URL and get title, member price, stock,
        brand, model, UPC, rating, description, and images in one normalized
        response.

        Price: $0.00319 per request.

        Example:
            res = client.samsclub.product(url="https://www.samsclub.com/ip/Bounty-Select-A-Size-2-Ply-Paper-Towels-12-Rolls-110-sheets-roll/18040450426")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "samsclub.product", dict(input), options
        )
        return RunResult[SamsclubProductData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SamsclubSearchInput],
    ) -> RunResult[SamsclubSearchData]:
        """Sam's Club Search

        Search SamsClub.com by keyword with optional sort, price-range, and page
        filters and get title, member price, stock, and rating for each product in
        one normalized response.

        Price: $0.00319 per request.

        Example:
            res = client.samsclub.search(query="paper towels")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "samsclub.search", dict(input), options
        )
        return RunResult[SamsclubSearchData].model_validate(raw)
