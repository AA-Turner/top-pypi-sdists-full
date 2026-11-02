# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the walmart platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class WalmartProductInput(TypedDict, total=False):
    """Input for Walmart Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["productId"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `productId`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a product that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Walmart product page URL."""


class WalmartReviewsInput(TypedDict, total=False):
    """Input for Walmart Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based page of 10 reviews, Walmart's fixed page size; Walmart serves at most 100 pages. Each page is billed as one request; keep url and sort the same while walking pages. Range: 1 to 100. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "helpfulVotes",
                "rating",
                "ratingDistribution",
                "totalPages",
                "totalReviews",
                "verifiedPurchase",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `totalPages`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal["recent", "oldest", "relevancy", "helpful", "rating_high", "rating_low"]
    ]
    """Review order: recent (newest first, the default), oldest, relevancy, helpful, rating_high, or rating_low (e.g. helpful). Default: recent."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Walmart product page URL (e.g. https://www.walmart.com/ip/Apple-AirPods-Pro-2/5689919121)."""


class WalmartSearchInput(TypedDict, total=False):
    """Input for Walmart Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    facet: NotRequired[str]
    """Optional Walmart facet filter token, e.g. brand:HP to keep only HP products."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum product price in USD. Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum product price in USD. Minimum: 0."""
    page: NotRequired[int]
    """1-based results page of about 40 to 60 products; Walmart serves no products past page 10. Each page is billed as one request. Walmart re-ranks between requests, so consecutive pages can repeat a product: deduplicate on itemId. Range: 1 to 10. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "airpods" or "paper towels"."""
    requireFields: NotRequired[list[Literal["totalPages"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `totalPages`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal[
            "best_match", "best_seller", "price_low", "price_high", "rating_high", "new"
        ]
    ]
    """Result sort order; omit for Walmart's Best Match (e.g. price_low sorts by lowest price first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class WalmartProductData(BaseModel):
    items: list[WalmartProductItem] = Field(
        description="Product detail records (one per requested product URL). Populated whenever the provider has data for the entity."
    )


class WalmartProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    availability: str | None = Field(
        default=None, description='Stock status, e.g. "IN_STOCK".'
    )
    brand: str | None = Field(
        default=None, description="Brand name; empty when not reported."
    )
    description: str | None = Field(
        default=None,
        description="Short product description; empty when the listing has none.",
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None, description="All product image URLs."
    )
    item_id: str | None = Field(
        default=None,
        alias="itemId",
        description="Walmart US item id (usItemId). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    model: str | None = Field(
        default=None, description="Manufacturer model number; empty when not reported."
    )
    order_limit: int | None = Field(
        default=None,
        alias="orderLimit",
        description="Maximum units of this item one order may contain.",
    )
    price_text: str | None = Field(
        default=None,
        alias="priceText",
        description='Current price as displayed, e.g. "$125.00"; empty when unavailable (Walmart returns a formatted string, not a numeric value).',
    )
    product_id: str | None = Field(
        default=None, alias="productId", description="Walmart internal product id."
    )
    rating: float | None = Field(
        default=None, description="Average customer rating, 0-5; 0 when unrated."
    )
    return_window: int | None = Field(
        default=None,
        alias="returnWindow",
        description="Days the buyer has to return the item.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer reviews; 0 when none.",
    )
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="Identifier of the seller fulfilling the offer.",
    )
    seller_name: str | None = Field(
        default=None,
        alias="sellerName",
        description="Name of the seller fulfilling the offer.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    upc: str | None = Field(
        default=None, description="Universal Product Code; empty when not reported."
    )
    url: str = Field(
        description="Canonical Walmart product page URL (condition query param retained, as it selects the offer). Populated whenever the provider has data for the entity."
    )


class WalmartReviewsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[WalmartReviewsItem] = Field(
        description="Customer review records for the requested page. Populated whenever the provider has data for the entity."
    )
    rating: float | None = Field(
        default=None,
        description="Overall product score (1-5), or null when the serving source does not report it.",
    )
    rating_distribution: WalmartReviewsRatingDistribution | None = Field(
        default=None,
        alias="ratingDistribution",
        description='Number of reviews at each star rating, keyed "1" through "5".',
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="Number of 10-review pages Walmart reports for the product (it can exceed the 100 pages this SKU serves), or absent or null when the serving source does not report it.",
    )
    total_reviews: int | None = Field(
        default=None,
        alias="totalReviews",
        description="Total number of reviews for the product, or null when the serving source does not report it.",
    )


class WalmartReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Walmart publishes the review date only, so this is midnight UTC of that date; null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    helpful_votes: int | None = Field(
        default=None,
        alias="helpfulVotes",
        description='Number of "helpful" votes the review received, or null when not reported.',
    )
    rating: float = Field(description="Star rating the reviewer gave, 1-5.")
    review_id: str = Field(
        alias="reviewId",
        description="Walmart review id; use it to deduplicate across pages. Populated whenever the provider has data for the entity.",
    )
    reviewer: str | None = Field(
        default=None,
        description='Reviewer display name as Walmart shows it, e.g. "anonymous"; empty when withheld.',
    )
    text: str = Field(
        description="Full review body text. Populated whenever the provider has data for the entity."
    )
    title: str | None = Field(
        default=None, description="Review headline; empty when the review has none."
    )
    verified_purchase: bool | None = Field(
        default=None,
        alias="verifiedPurchase",
        description="True when Walmart marks the review a verified purchase; null when the serving source reports no badge either way.",
    )


class WalmartReviewsRatingDistribution(BaseModel):
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


class WalmartSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[WalmartSearchItem] = Field(
        description="Matching Walmart product records for the requested page. Populated whenever the provider has data for the entity."
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="Highest page number available for the query; request pages 1 through this value. Absent or null when the serving source does not report it.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total number of matching products Walmart reports for the query, or null when not reported.",
    )


class WalmartSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    availability: str | None = Field(
        default=None,
        description='Stock status as Walmart reports it, e.g. "IN_STOCK" or "OUT_OF_STOCK".',
    )
    brand: str | None = Field(
        default=None,
        description="Brand name, or null when Walmart omits it from the search grid (it publishes brand on clothing-style grids and on no row elsewhere; the Walmart Product SKU always carries it).",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD"; empty when no price is shown.',
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    in_stock: bool | None = Field(
        default=None,
        alias="inStock",
        description="True when the product is in stock, false when it is not, or null when not reported.",
    )
    is_sponsored: bool | None = Field(
        default=None,
        alias="isSponsored",
        description="True when the result is a sponsored placement.",
    )
    item_id: str = Field(
        alias="itemId",
        description="Walmart US item id (usItemId), the number in a walmart.com/ip/ URL; use the product URL with the Walmart Product or Walmart Reviews SKU. Populated whenever the provider has data for the entity.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description='Pre-discount "was" price when the product is on sale, or null when it is not discounted.',
    )
    position: int | None = Field(
        default=None, description="1-based position of the result in this page."
    )
    price: float | None = Field(
        default=None,
        description="Current price in USD as a number, or null when the result shows no current price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer ratings, or null when the product has none.",
    )
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="Identifier of the seller fulfilling the shown offer.",
    )
    seller_name: str | None = Field(
        default=None,
        alias="sellerName",
        description="Name of the seller fulfilling the shown offer.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Walmart product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class WalmartNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WalmartProductInput],
    ) -> RunResult[WalmartProductData]:
        """Walmart Product

        Fetch a Walmart product page by URL and get full product details (title,
        price, availability, ratings, images, and specs) in one normalized response.

        Price: $0.001 per request.

        Example:
            res = client.walmart.product(url="https://www.walmart.com/ip/Apple-AirPods-Pro-2/5689919121")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "walmart.product", dict(input), options
        )
        return RunResult[WalmartProductData].model_validate(raw)

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WalmartReviewsInput],
    ) -> RunResult[WalmartReviewsData]:
        """Walmart Reviews

        Pull a page of 10 customer reviews for any Walmart product by URL, newest
        first or by relevance, helpfulness, or rating: rating, title, text, date,
        reviewer, and verified-purchase badge.

        Price: $0.00085 per request.

        Example:
            res = client.walmart.reviews(url="https://www.walmart.com/ip/Apple-AirPods-Pro-2/5689919121")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "walmart.reviews", dict(input), options
        )
        return RunResult[WalmartReviewsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WalmartSearchInput],
    ) -> RunResult[WalmartSearchData]:
        """Walmart Search

        Search Walmart by keyword with optional sort, price-range, facet, and page
        filters and get title, price, rating, seller, and availability for each
        product in one normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.walmart.search(query="airpods", sort="best_seller")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "walmart.search", dict(input), options
        )
        return RunResult[WalmartSearchData].model_validate(raw)


class AsyncWalmartNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WalmartProductInput],
    ) -> RunResult[WalmartProductData]:
        """Walmart Product

        Fetch a Walmart product page by URL and get full product details (title,
        price, availability, ratings, images, and specs) in one normalized response.

        Price: $0.001 per request.

        Example:
            res = client.walmart.product(url="https://www.walmart.com/ip/Apple-AirPods-Pro-2/5689919121")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "walmart.product", dict(input), options
        )
        return RunResult[WalmartProductData].model_validate(raw)

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WalmartReviewsInput],
    ) -> RunResult[WalmartReviewsData]:
        """Walmart Reviews

        Pull a page of 10 customer reviews for any Walmart product by URL, newest
        first or by relevance, helpfulness, or rating: rating, title, text, date,
        reviewer, and verified-purchase badge.

        Price: $0.00085 per request.

        Example:
            res = client.walmart.reviews(url="https://www.walmart.com/ip/Apple-AirPods-Pro-2/5689919121")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "walmart.reviews", dict(input), options
        )
        return RunResult[WalmartReviewsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WalmartSearchInput],
    ) -> RunResult[WalmartSearchData]:
        """Walmart Search

        Search Walmart by keyword with optional sort, price-range, facet, and page
        filters and get title, price, rating, seller, and availability for each
        product in one normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.walmart.search(query="airpods", sort="best_seller")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "walmart.search", dict(input), options
        )
        return RunResult[WalmartSearchData].model_validate(raw)
