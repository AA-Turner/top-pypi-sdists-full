# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the bestbuy platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class BestbuyProductInput(TypedDict, total=False):
    """Input for Best Buy Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Best Buy product page URL that carries the numeric Best Buy SKU, either the .../sku/6376564 form the Best Buy Search SKU returns or the older .../6376564.p?skuId=6376564 form."""


class BestbuyReviewsInput(TypedDict, total=False):
    """Input for Best Buy Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based page of 10 reviews; Best Buy serves at most 1000 pages. Each page is billed as one request; keep url and sort the same while walking pages. Range: 1 to 1000. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["incentivized", "rating"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `rating`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal["recent", "oldest", "relevancy", "helpful", "rating_high", "rating_low"]
    ]
    """Review order: recent (newest first, the default), oldest, relevancy, helpful, rating_high, or rating_low (e.g. helpful). Default: recent."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Best Buy product page URL that carries the numeric Best Buy SKU, either the .../sku/6376564 form the Best Buy Search SKU returns or the older .../6376564.p?skuId=6376564 form."""


class BestbuySearchInput(TypedDict, total=False):
    """Input for Best Buy Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum product price in USD. Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum product price in USD. Minimum: 0."""
    page: NotRequired[int]
    """1-based results page of about 18 to 24 products; Best Buy serves no products past page 100. Each page is billed as one request. Page sizes differ between sources, so deduplicate on sku. Range: 1 to 100. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "airpods" or "65 inch tv"."""
    requireFields: NotRequired[
        list[
            Literal[
                "description",
                "inStock",
                "isSponsored",
                "totalResults",
                "upc",
                "variants",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `totalResults`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal[
            "best_match", "best_seller", "price_low", "price_high", "rating_high", "new"
        ]
    ]
    """Result sort order; omit for Best Buy's own relevance order (e.g. price_low sorts by lowest price first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class BestbuyProductData(BaseModel):
    items: list[BestbuyProductItem] = Field(
        description="Product detail records (one per requested product URL). Populated whenever the provider has data for the entity."
    )


class BestbuyProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None,
        description="Brand name, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown.',
    )
    description: str | None = Field(
        default=None,
        description="Product description text, or null when the listing has none.",
    )
    features: list[BestbuyProductFeature] | None = Field(
        default=None,
        description="Feature bullets from the product page; empty when there are none.",
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None, description="All product image URLs, primary first."
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Regular price when the product is on sale, or null when it is not discounted.",
    )
    model: str | None = Field(
        default=None,
        description="Manufacturer model number, or null when not reported.",
    )
    price: float | None = Field(
        default=None,
        description="Current price in USD, or null when the product shows no current price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer reviews, or null when not reported.",
    )
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description='Seller id: "bby" for Best Buy itself, a number for a Marketplace seller, or null when not reported.',
    )
    seller_type: str | None = Field(
        default=None,
        alias="sellerType",
        description='"1P" when Best Buy sells the product itself, "3P" when a Marketplace seller does, or null when not reported.',
    )
    sku: str | None = Field(
        default=None,
        description="Best Buy SKU. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    specifications: list[BestbuyProductSpecification] | None = Field(
        default=None,
        description='The specifications table from the product page, in Best Buy\'s groups ("Key Specs", "General", ...); empty when the page has none.',
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    upc: str | None = Field(
        default=None, description="Universal Product Code, or null when not reported."
    )
    url: str = Field(
        description="Best Buy product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )


class BestbuyProductFeature(BaseModel):
    model_config = ConfigDict(extra="allow")

    description: str | None = Field(default=None, description="Feature text.")
    title: str | None = Field(
        default=None, description="Feature heading, or null when the bullet has none."
    )


class BestbuyProductSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    group: str | None = Field(
        default=None, description='Group heading, e.g. "General".'
    )
    specs: list[BestbuyProductSpec] | None = Field(
        default=None, description="Rows in the group."
    )


class BestbuyProductSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(
        default=None, description='Attribute name, e.g. "Model Number".'
    )
    value: str | None = Field(
        default=None,
        description='Attribute value as Best Buy lists it; yes/no attributes read "true" or "false".',
    )


class BestbuyReviewsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[BestbuyReviewsItem] = Field(
        description="Customer review records for the requested page. Populated whenever the provider has data for the entity."
    )
    rating: float | None = Field(
        default=None,
        description="Overall product score (1-5), or null when the serving source does not report it.",
    )
    rating_distribution: BestbuyReviewsRatingDistribution | None = Field(
        default=None,
        alias="ratingDistribution",
        description='Number of reviews at each star rating, keyed "1" through "5".',
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="Number of 10-review pages Best Buy reports for the product, or null when not reported.",
    )
    total_reviews: int | None = Field(
        default=None,
        alias="totalReviews",
        description="Total number of reviews for the product, or null when not reported.",
    )


class BestbuyReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    helpful_votes: int | None = Field(
        default=None,
        alias="helpfulVotes",
        description='Number of "helpful" votes the review received, or null when not reported.',
    )
    incentivized: bool | None = Field(
        default=None,
        description="True when Best Buy marks the review incentivized (the reviewer received promo considerations or a sweepstakes entry for writing it), false when it does not, or null when not reported. One source reports only the true case and leaves the rest null.",
    )
    ownership_days: int | None = Field(
        default=None,
        alias="ownershipDays",
        description="Days the reviewer had owned the product when they wrote the review, or null when not reported.",
    )
    rating: float = Field(description="Star rating the reviewer gave, 1-5.")
    recommended: bool | None = Field(
        default=None,
        description="True when the reviewer says they would recommend the product, false when they would not, or null when they did not answer.",
    )
    review_id: str = Field(
        alias="reviewId",
        description="Best Buy review id; use it to deduplicate across pages. Populated whenever the provider has data for the entity.",
    )
    reviewer: str | None = Field(
        default=None, description="Reviewer display name; empty when withheld."
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
        description="True when Best Buy marks the review a verified purchase, or null when not reported.",
    )


class BestbuyReviewsRatingDistribution(BaseModel):
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


class BestbuySearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[BestbuySearchItem] = Field(
        description="Matching Best Buy product records for the requested page. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total number of matching products Best Buy reports for the query, or null when the serving source does not report it.",
    )


class BestbuySearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None, description="Brand name, or null when not reported."
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown.',
    )
    description: str | None = Field(
        default=None,
        description="Long product description, or null when the serving source does not report it.",
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    in_stock: bool | None = Field(
        default=None,
        alias="inStock",
        description="True when Best Buy shows the product available to buy, or null when the serving source does not report it.",
    )
    is_sponsored: bool | None = Field(
        default=None,
        alias="isSponsored",
        description="True when the result is a sponsored placement, or null when the serving source does not report it.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Regular price when the product is on sale, or null when it is not discounted.",
    )
    open_box: list[BestbuySearchOpenBox] | None = Field(
        default=None,
        alias="openBox",
        description="Open-box offers for the product, one per condition; empty when there are none.",
    )
    position: int | None = Field(
        default=None, description="1-based position of the result in this page."
    )
    price: float | None = Field(
        default=None,
        description="Current price in USD, or null when the result shows no current price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
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
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description='Seller id: "bby" for Best Buy itself, a number for a Marketplace seller, or null when not reported.',
    )
    seller_type: str | None = Field(
        default=None,
        alias="sellerType",
        description='"1P" when Best Buy sells the product itself, "3P" when a Marketplace seller does, or null when not reported.',
    )
    sku: str = Field(
        description="Best Buy SKU, the number after /sku/ in the product URL; use the product URL with the Best Buy Product or Best Buy Reviews SKU. Populated whenever the provider has data for the entity."
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    upc: str | None = Field(
        default=None,
        description="UPC barcode, or null when the serving source does not report it.",
    )
    url: str | None = Field(
        default=None,
        description="Best Buy product page URL carrying the SKU, with tracking query parameters removed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    variants: list[BestbuySearchVariant] | None = Field(
        default=None,
        description="Sibling versions of the product (colour, size, connector), including this one, or null when the serving source does not report them.",
    )


class BestbuySearchOpenBox(BaseModel):
    model_config = ConfigDict(extra="allow")

    condition: str | None = Field(
        default=None,
        description='Open-box condition as Best Buy names it: "Excellent", "Good" or "Fair".',
    )
    price: float | None = Field(
        default=None,
        description="Open-box price in USD for that condition; absent when the serving source reports only the condition.",
    )


class BestbuySearchVariant(BaseModel):
    model_config = ConfigDict(extra="allow")

    attributes: BestbuySearchAttribute | None = Field(
        default=None,
        description='What sets the variant apart, keyed by Best Buy\'s attribute name, e.g. {"Color": "Black"}.',
    )
    sku: str | None = Field(default=None, description="Best Buy SKU of the variant.")


class BestbuySearchAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class BestbuyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BestbuyProductInput],
    ) -> RunResult[BestbuyProductData]:
        """Best Buy Product

        Fetch a BestBuy.com product by URL and get title, price, brand, model, UPC,
        rating, description, and images in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.bestbuy.product(url="https://www.bestbuy.com/product/apple-airpods-5-true-wireless-active-noise-cancelling-earbuds-with-wireless-charging-case-white/JJGCQP634G/sku/6376564")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bestbuy.product", dict(input), options
        )
        return RunResult[BestbuyProductData].model_validate(raw)

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BestbuyReviewsInput],
    ) -> RunResult[BestbuyReviewsData]:
        """Best Buy Reviews

        Pull a page of 10 customer reviews for any BestBuy.com product by URL,
        newest first or by relevance, helpfulness, or rating: rating, title, text,
        date, reviewer, and verified-purchase badge.

        Price: $0.00085 per request.

        Example:
            res = client.bestbuy.reviews(url="https://www.bestbuy.com/product/apple-airpods-5-true-wireless-active-noise-cancelling-earbuds-with-wireless-charging-case-white/JJGCQP634G/sku/6376564")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bestbuy.reviews", dict(input), options
        )
        return RunResult[BestbuyReviewsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BestbuySearchInput],
    ) -> RunResult[BestbuySearchData]:
        """Best Buy Search

        Search BestBuy.com by keyword with optional sort, price-range, and page
        filters and get title, price, rating, and brand for each product in one
        normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.bestbuy.search(query="airpods")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bestbuy.search", dict(input), options
        )
        return RunResult[BestbuySearchData].model_validate(raw)


class AsyncBestbuyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BestbuyProductInput],
    ) -> RunResult[BestbuyProductData]:
        """Best Buy Product

        Fetch a BestBuy.com product by URL and get title, price, brand, model, UPC,
        rating, description, and images in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.bestbuy.product(url="https://www.bestbuy.com/product/apple-airpods-5-true-wireless-active-noise-cancelling-earbuds-with-wireless-charging-case-white/JJGCQP634G/sku/6376564")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bestbuy.product", dict(input), options
        )
        return RunResult[BestbuyProductData].model_validate(raw)

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BestbuyReviewsInput],
    ) -> RunResult[BestbuyReviewsData]:
        """Best Buy Reviews

        Pull a page of 10 customer reviews for any BestBuy.com product by URL,
        newest first or by relevance, helpfulness, or rating: rating, title, text,
        date, reviewer, and verified-purchase badge.

        Price: $0.00085 per request.

        Example:
            res = client.bestbuy.reviews(url="https://www.bestbuy.com/product/apple-airpods-5-true-wireless-active-noise-cancelling-earbuds-with-wireless-charging-case-white/JJGCQP634G/sku/6376564")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bestbuy.reviews", dict(input), options
        )
        return RunResult[BestbuyReviewsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BestbuySearchInput],
    ) -> RunResult[BestbuySearchData]:
        """Best Buy Search

        Search BestBuy.com by keyword with optional sort, price-range, and page
        filters and get title, price, rating, and brand for each product in one
        normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.bestbuy.search(query="airpods")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bestbuy.search", dict(input), options
        )
        return RunResult[BestbuySearchData].model_validate(raw)
