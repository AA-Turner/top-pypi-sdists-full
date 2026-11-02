# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the target platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class TargetProductInput(TypedDict, total=False):
    """Input for Target Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "availability",
                "category",
                "dpci",
                "highlights",
                "images",
                "listPrice",
                "packageDimensions",
                "rating",
                "ratingCount",
                "returnPolicy",
                "specifications",
                "upc",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `availability`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a product that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Target product page URL; the TCIN after /A- identifies the product (e.g. https://www.target.com/p/-/A-91863920)."""


class TargetReviewsInput(TypedDict, total=False):
    """Input for Target Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based page of 10 reviews. Each page is billed as one request; keep url and sort the same while walking pages. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    sort: NotRequired[Literal["recent", "helpful", "rating_high", "rating_low"]]
    """Review order: recent (newest first, the default), helpful, rating_high, or rating_low (e.g. helpful). Default: recent."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Target product page URL; the TCIN after /A- identifies the product (e.g. https://www.target.com/p/-/A-91863920)."""


class TargetSearchInput(TypedDict, total=False):
    """Input for Target Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum product price in USD. Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum product price in USD. Minimum: 0."""
    page: NotRequired[int]
    """1-based results page of 24 products; Target serves no products past page 50. Each page is billed as one request. Range: 1 to 50. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "coffee maker" or "lego"."""
    requireFields: NotRequired[
        list[Literal["hasMore", "images", "isSponsored", "rating", "totalPages"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `totalPages`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal[
            "best_match", "best_seller", "price_low", "price_high", "rating_high", "new"
        ]
    ]
    """Result sort order; omit for Target's own relevance order (e.g. price_low sorts by lowest price first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TargetProductData(BaseModel):
    items: list[TargetProductItem] = Field(
        description="Product detail records (one per requested product URL). Populated whenever the provider has data for the entity."
    )


class TargetProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    availability: str | None = Field(
        default=None,
        description='Stock status as Target reports it, e.g. "InStock", or null when the serving source does not report it.',
    )
    brand: str | None = Field(
        default=None,
        description="Brand name, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    category: str | None = Field(
        default=None,
        description='Target category the product sits in, e.g. "Drip Coffee Makers", or null when the serving source does not report it.',
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown.',
    )
    description: str | None = Field(
        default=None,
        description="Product description text, or null when the listing has none.",
    )
    dpci: str | None = Field(
        default=None,
        description='Target\'s in-store item number (DPCI), e.g. "072-08-0313", or null when not reported.',
    )
    highlights: list[str] | None = Field(
        default=None,
        description="Highlight bullets from the product page, or null when the serving source does not report them.",
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None,
        description="Product image URLs, primary first. One source returns only the primary image.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Regular price when the product is on sale, or null when it is not discounted or the serving source does not report it.",
    )
    package_dimensions: TargetProductPackageDimension | None = Field(
        default=None,
        alias="packageDimensions",
        description="Size and weight of the shipping package as Target lists them, or null when the serving source does not report them.",
    )
    price: float | None = Field(
        default=None,
        description="Current price in USD, or null when the product shows no current price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated. One source rounds it to one decimal.",
    )
    rating_count: int | None = Field(
        default=None,
        alias="ratingCount",
        description="Number of star ratings, including ratings left without a written review, or null when the serving source does not report it.",
    )
    return_policy: str | None = Field(
        default=None,
        alias="returnPolicy",
        description="Target's return policy text for this item, or null when the serving source does not report it.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of written customer reviews, or null when not reported.",
    )
    specifications: list[TargetProductSpecification] | None = Field(
        default=None,
        description="The specifications table from the product page, one name and value per row, or null when the serving source does not report it.",
    )
    tcin: str | None = Field(
        default=None,
        description="Target product id (TCIN). Target rolls a colour or size variant up to its parent product, so it can differ from the id in the requested URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    upc: str | None = Field(
        default=None,
        description="UPC barcode as Target lists it, or null when not reported.",
    )
    url: str = Field(
        description="Target product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )


class TargetProductPackageDimension(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    depth: float | None = Field(
        default=None, description="Package depth, in dimensionUnit."
    )
    dimension_unit: str | None = Field(
        default=None,
        alias="dimensionUnit",
        description='Unit of the three dimensions, e.g. "INCH".',
    )
    height: float | None = Field(
        default=None, description="Package height, in dimensionUnit."
    )
    weight: float | None = Field(
        default=None, description="Package weight, in weightUnit."
    )
    weight_unit: str | None = Field(
        default=None,
        alias="weightUnit",
        description='Unit of the weight, e.g. "POUND".',
    )
    width: float | None = Field(
        default=None, description="Package width, in dimensionUnit."
    )


class TargetProductSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(
        default=None, description='Attribute name as Target labels it, e.g. "Material".'
    )
    value: str | None = Field(
        default=None, description="Attribute value as Target lists it."
    )


class TargetReviewsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[TargetReviewsItem] = Field(
        description="Customer review records for the requested page. Populated whenever the provider has data for the entity."
    )
    rating: float | None = Field(
        default=None,
        description="Overall product score (1-5), or null when not reported.",
    )
    rating_distribution: TargetReviewsRatingDistribution | None = Field(
        default=None,
        alias="ratingDistribution",
        description='Number of ratings at each star rating, keyed "1" through "5".',
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="Number of 10-review pages Target reports for the product, or null when not reported.",
    )
    total_reviews: int | None = Field(
        default=None,
        alias="totalReviews",
        description="Total number of written reviews for the product, or null when not reported.",
    )


class TargetReviewsItem(BaseModel):
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
        description="True when the reviewer received an incentive, such as a free sample, for writing the review, or null when not reported.",
    )
    rating: float = Field(description="Star rating the reviewer gave, 1-5.")
    recommended: bool | None = Field(
        default=None,
        description="True when the reviewer says they would recommend the product, false when they would not, or null when they did not answer.",
    )
    responses: list[TargetReviewsResponse] | None = Field(
        default=None,
        description="Public replies to the review from the brand or Target, oldest first; empty when there are none.",
    )
    review_id: str = Field(
        alias="reviewId",
        description="Target review id; use it to deduplicate across pages. Populated whenever the provider has data for the entity.",
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
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) of the review's last update on Target. Multiply by 1000 for a JS Date in milliseconds. Null when not reported.",
    )
    verified_purchase: bool | None = Field(
        default=None,
        alias="verifiedPurchase",
        description="True when Target marks the review a verified purchase, or null when not reported.",
    )


class TargetReviewsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Null when not reported.",
    )
    name: str | None = Field(
        default=None,
        description="Name the reply is signed with, e.g. the brand's customer team.",
    )
    text: str | None = Field(default=None, description="Reply text.")


class TargetReviewsRatingDistribution(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    field_1: int | None = Field(
        default=None, alias="1", description="Number of 1-star ratings."
    )
    field_2: int | None = Field(
        default=None, alias="2", description="Number of 2-star ratings."
    )
    field_3: int | None = Field(
        default=None, alias="3", description="Number of 3-star ratings."
    )
    field_4: int | None = Field(
        default=None, alias="4", description="Number of 4-star ratings."
    )
    field_5: int | None = Field(
        default=None, alias="5", description="Number of 5-star ratings."
    )


class TargetSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when another page of results exists; request it with page + 1. Null when the serving source does not report it.",
    )
    items: list[TargetSearchItem] = Field(
        description="Matching Target product records for the requested page. Populated whenever the provider has data for the entity."
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="Highest page number available for the query, or null when the serving source does not report it.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total number of matching products Target reports for the query, or null when not reported.",
    )


class TargetSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None, description="Brand name, or null when not reported."
    )
    brand_url: str | None = Field(
        default=None,
        alias="brandUrl",
        description="Target brand page URL, or null when not reported.",
    )
    category: str | None = Field(
        default=None,
        description='Target product type the result belongs to, e.g. "Coffee Makers", or null when not reported.',
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown.',
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None,
        description="All product image URLs, primary first, or null when the serving source returns only the primary image.",
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
    position: int | None = Field(
        default=None, description="1-based position of the result in this page."
    )
    price: float | None = Field(
        default=None,
        description="Current price in USD, or null when the result shows no current price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated. One source rounds it to one decimal.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer ratings, or null when the product has none.",
    )
    tcin: str = Field(
        description="Target product id (TCIN), the number after /A- in a target.com URL; use the product URL with the Target Product or Target Reviews SKU. Populated whenever the provider has data for the entity."
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Target product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class TargetNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TargetProductInput],
    ) -> RunResult[TargetProductData]:
        """Target Product

        Fetch a Target.com product by URL and get title, price, brand, rating,
        description, and images in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.target.product(url="https://www.target.com/p/mr-coffee-12c-programmable-drip-coffee-maker-stainless-steel-finish/-/A-91863920")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "target.product", dict(input), options
        )
        return RunResult[TargetProductData].model_validate(raw)

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TargetReviewsInput],
    ) -> RunResult[TargetReviewsData]:
        """Target Reviews

        Pull a page of 10 customer reviews for any Target.com product by URL, newest
        first or by helpfulness or rating: rating, title, text, date, reviewer, and
        verified-purchase badge.

        Price: $0.00085 per request.

        Example:
            res = client.target.reviews(url="https://www.target.com/p/mr-coffee-12c-programmable-drip-coffee-maker-stainless-steel-finish/-/A-91863920")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "target.reviews", dict(input), options
        )
        return RunResult[TargetReviewsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TargetSearchInput],
    ) -> RunResult[TargetSearchData]:
        """Target Search

        Search Target.com by keyword with optional sort, price-range, and page
        filters and get title, price, rating, and brand for each product in one
        normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.target.search(query="coffee maker")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "target.search", dict(input), options
        )
        return RunResult[TargetSearchData].model_validate(raw)


class AsyncTargetNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TargetProductInput],
    ) -> RunResult[TargetProductData]:
        """Target Product

        Fetch a Target.com product by URL and get title, price, brand, rating,
        description, and images in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.target.product(url="https://www.target.com/p/mr-coffee-12c-programmable-drip-coffee-maker-stainless-steel-finish/-/A-91863920")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "target.product", dict(input), options
        )
        return RunResult[TargetProductData].model_validate(raw)

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TargetReviewsInput],
    ) -> RunResult[TargetReviewsData]:
        """Target Reviews

        Pull a page of 10 customer reviews for any Target.com product by URL, newest
        first or by helpfulness or rating: rating, title, text, date, reviewer, and
        verified-purchase badge.

        Price: $0.00085 per request.

        Example:
            res = client.target.reviews(url="https://www.target.com/p/mr-coffee-12c-programmable-drip-coffee-maker-stainless-steel-finish/-/A-91863920")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "target.reviews", dict(input), options
        )
        return RunResult[TargetReviewsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TargetSearchInput],
    ) -> RunResult[TargetSearchData]:
        """Target Search

        Search Target.com by keyword with optional sort, price-range, and page
        filters and get title, price, rating, and brand for each product in one
        normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.target.search(query="coffee maker")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "target.search", dict(input), options
        )
        return RunResult[TargetSearchData].model_validate(raw)
