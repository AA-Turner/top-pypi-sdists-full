# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the aliexpress platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class AliexpressProductInput(TypedDict, total=False):
    """Input for AliExpress Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Ship-to country as a 2-letter ISO code, e.g. US or DE. It changes prices, stock and the delivery estimate. Default: US."""
    currency: NotRequired[str]
    """Price currency as a 3-letter ISO code, e.g. USD or EUR. Default: USD."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    productId: Required[str]
    """AliExpress product id, the number in the product URL (https://www.aliexpress.com/item/<id>.html), e.g. 3256807039224587. The AliExpress Search SKU returns it as productId."""
    requireFields: NotRequired[
        list[
            Literal[
                "freeShipping", "returnPolicy", "shippingCost", "video", "wishlistCount"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `video`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AliexpressReviewsInput(TypedDict, total=False):
    """Input for AliExpress Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based page of 20 reviews in AliExpress's default order. Each page is billed as one request. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    productId: Required[str]
    """AliExpress product id, the number in the product URL (https://www.aliexpress.com/item/<id>.html), e.g. 3256807039224587. The AliExpress Search SKU returns it as productId."""
    requireFields: NotRequired[
        list[
            Literal[
                "followUpImages",
                "followUpText",
                "followUpUtc",
                "helpfulVotes",
                "unhelpfulVotes",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `helpfulVotes`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AliexpressSearchInput(TypedDict, total=False):
    """Input for AliExpress Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Ship-to country as a 2-letter ISO code, e.g. US or DE. It changes prices, availability and delivery estimates. Default: US."""
    currency: NotRequired[str]
    """Price currency as a 3-letter ISO code, e.g. USD or EUR. Default: USD."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum product price, in the requested currency. Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum product price, in the requested currency. Minimum: 0."""
    page: NotRequired[int]
    """1-based results page of about 60 products; AliExpress serves no results past page 60. Each page is billed as one request. Range: 1 to 60. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "wireless earbuds"."""
    requireFields: NotRequired[
        list[
            Literal[
                "deliveryDaysMax",
                "deliveryDaysMin",
                "isChoice",
                "listedUtc",
                "shipFrom",
                "storeName",
                "totalResults",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `shipFrom`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[Literal["best_match", "best_seller", "price_low", "price_high"]]
    """Result order: best_match (AliExpress relevance, the default), best_seller (most orders first), price_low, or price_high. Default: best_match."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AliexpressProductData(BaseModel):
    items: list[AliexpressProductItem] = Field(
        description="Product detail records (one per requested product id). Populated whenever the provider has data for the entity."
    )


class AliexpressProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    delivery_days_max: int | None = Field(
        default=None,
        alias="deliveryDaysMax",
        description="Most days the default shipping option takes to the requested country, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    delivery_days_min: int | None = Field(
        default=None,
        alias="deliveryDaysMin",
        description="Fewest days the default shipping option takes to the requested country, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    free_shipping: bool | None = Field(
        default=None,
        alias="freeShipping",
        description="True when the default shipping option to the requested country costs nothing after AliExpress's buyer promotions, or null when the serving source does not report it.",
    )
    images: list[str] | None = Field(
        default=None,
        description="Product image URLs, primary first. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    is_top_rated_seller: bool | None = Field(
        default=None,
        alias="isTopRatedSeller",
        description="True when AliExpress marks the store as a top-rated seller, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    options: list[AliexpressProductOption] | None = Field(
        default=None,
        description="The choices a buyer picks from, e.g. Color and Size, each with its values. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="Price of the default variant before the current discount, or null when not shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    price: float | None = Field(
        default=None,
        description="Current price of the default variant in the requested currency (the lowest variant price when the page shows a range), or null when not shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_id: str = Field(
        alias="productId",
        description="AliExpress product id. Populated whenever the provider has data for the entity.",
    )
    quantity_available: int | None = Field(
        default=None,
        alias="quantityAvailable",
        description="Units in stock across all variants, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    return_policy: str | None = Field(
        default=None,
        alias="returnPolicy",
        description='The returns promise AliExpress shows on the product, e.g. "Free returns within 90 days", or null when the serving source does not report it.',
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer reviews, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_country: str | None = Field(
        default=None,
        alias="sellerCountry",
        description='Country the store is registered in, as AliExpress names it, e.g. "China", or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    seller_feedback_count: int | None = Field(
        default=None,
        alias="sellerFeedbackCount",
        description="Number of buyer feedback ratings the store has received, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_feedback_percent: float | None = Field(
        default=None,
        alias="sellerFeedbackPercent",
        description="Share of the store's buyer feedback that is positive, as a percentage, e.g. 95.9, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_level: str | None = Field(
        default=None,
        alias="sellerLevel",
        description='The store\'s AliExpress seller level code, e.g. "25-s", or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    seller_opened_utc: float | None = Field(
        default=None,
        alias="sellerOpenedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. The day the store opened on AliExpress, as midnight UTC of that date; null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_score: int | None = Field(
        default=None,
        alias="sellerScore",
        description="The store's AliExpress feedback score, the points AliExpress shows beside the store, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    ship_from: str | None = Field(
        default=None,
        alias="shipFrom",
        description='Country the default shipping option ships from, as AliExpress names it, e.g. "China", or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    shipping_cost: float | None = Field(
        default=None,
        alias="shippingCost",
        description="Shipping cost of the default option to the requested country, in the requested currency, or null when not reported or the serving source does not report it in that currency. AliExpress applies buyer promotions to it, so sources can differ.",
    )
    sold_count: int | None = Field(
        default=None,
        alias="soldCount",
        description='Units sold, read from AliExpress\'s rounded label, so "4,000+ sold" comes back as 4000; null when not shown.',
    )
    specifications: list[AliexpressProductSpecification] | None = Field(
        default=None,
        description="The seller's specifications table, one name and value per row. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    store_id: str | None = Field(
        default=None,
        alias="storeId",
        description="Storefront number of the store, the digits in https://www.aliexpress.com/store/<id>, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    store_name: str | None = Field(
        default=None,
        alias="storeName",
        description="Name of the store selling the product, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="AliExpress product page URL with tracking query parameters removed."
    )
    variants: list[AliexpressProductVariant] | None = Field(
        default=None,
        description="One entry per purchasable combination of options. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video: str | None = Field(
        default=None,
        description="Product video URL (MP4), or null when the product has none or the serving source does not report it.",
    )
    wishlist_count: int | None = Field(
        default=None,
        alias="wishlistCount",
        description="Number of shoppers who added the product to their wish list, or null when the serving source does not report it.",
    )


class AliexpressProductOption(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(
        default=None, description='Option name as AliExpress shows it, e.g. "Color".'
    )
    values: list[str] | None = Field(
        default=None, description='Values a buyer can pick, e.g. ["green", "Purple"].'
    )


class AliexpressProductSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(
        default=None,
        description='Attribute name as the seller lists it, e.g. "Material".',
    )
    value: str | None = Field(
        default=None, description="Attribute value as the seller lists it."
    )


class AliexpressProductVariant(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attributes: AliexpressProductAttribute | None = Field(
        default=None,
        description='The option values that make up this variant, keyed by option name, e.g. {"Color": "Purple", "Size": "XL"}, or null when the serving source does not report them.',
    )
    image: str | None = Field(
        default=None,
        description="Picture of this variant, or null when it has none or the serving source does not report it.",
    )
    in_stock: bool | None = Field(
        default=None,
        alias="inStock",
        description="True when this variant can be bought now, or null when not reported.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="Price of this variant before the current discount, or null when not reported.",
    )
    price: float | None = Field(
        default=None,
        description="Current price of this variant, or null when the serving source does not report it.",
    )
    quantity_available: int | None = Field(
        default=None,
        alias="quantityAvailable",
        description="Units of this variant in stock, or null when not reported.",
    )
    sku_id: str | None = Field(
        default=None, alias="skuId", description="AliExpress id of this variant."
    )


class AliexpressProductAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class AliexpressReviewsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[AliexpressReviewsItem] = Field(
        description="Buyer review records for the requested page. Populated whenever the provider has data for the entity."
    )
    rating: float | None = Field(
        default=None,
        description="Overall product score (1-5), or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating_distribution: AliexpressReviewsRatingDistribution | None = Field(
        default=None,
        alias="ratingDistribution",
        description='Number of reviews at each star rating, keyed "1" through "5". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="Number of 20-review pages AliExpress reports for the product, or null when not reported.",
    )
    total_reviews: int | None = Field(
        default=None,
        alias="totalReviews",
        description="Total number of reviews for the product, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class AliexpressReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    aspects: list[AliexpressReviewsAspect] = Field(
        description='The buyer\'s ratings of named aspects of the product, e.g. {"name": "Durability", "value": "Poor"}; empty when the buyer rated none.'
    )
    country: str | None = Field(
        default=None,
        description='2-letter ISO code of the buyer\'s country, e.g. "US", or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. AliExpress publishes the review date only, so this is midnight UTC of that date; null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    follow_up_images: list[str] | None = Field(
        default=None,
        alias="followUpImages",
        description="Photo URLs attached to the follow-up review; empty when it has none, null when the serving source does not report follow-ups.",
    )
    follow_up_text: str | None = Field(
        default=None,
        alias="followUpText",
        description="Text of the follow-up review the buyer added later, or null when there is none or the serving source does not report it.",
    )
    follow_up_utc: float | None = Field(
        default=None,
        alias="followUpUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. The day the buyer added the follow-up review, as midnight UTC of that date; null when there is none or the serving source does not report it.",
    )
    helpful_votes: int | None = Field(
        default=None,
        alias="helpfulVotes",
        description='Number of "helpful" votes the review received, or null when the serving source does not report it.',
    )
    images: list[str] | None = Field(
        default=None,
        description="Photo URLs the buyer attached; empty when there are none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float = Field(description="Star rating the buyer gave, 1-5.")
    review_id: str = Field(
        alias="reviewId",
        description="AliExpress review id; use it to deduplicate across pages. Populated whenever the provider has data for the entity.",
    )
    reviewer: str | None = Field(
        default=None,
        description='Buyer display name as AliExpress shows it, usually masked (e.g. "A***r") or "AliExpress Shopper". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    shipping_method: str | None = Field(
        default=None,
        alias="shippingMethod",
        description='Shipping service the buyer\'s order came by, as AliExpress names it, e.g. "AliExpress Selection Standard Shipping", or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    sku_info: str | None = Field(
        default=None,
        alias="skuInfo",
        description='The variant the buyer bought, as AliExpress prints it, e.g. "Color:Yellow Size:XXL", or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    text: str = Field(
        description="Review body text in the buyer's own language; empty when the buyer left a rating only. Populated whenever the provider has data for the entity."
    )
    unhelpful_votes: int | None = Field(
        default=None,
        alias="unhelpfulVotes",
        description='Number of "not helpful" votes the review received, or null when the serving source does not report it.',
    )


class AliexpressReviewsAspect(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(
        default=None, description='Aspect the buyer rated, e.g. "Durability".'
    )
    value: str | None = Field(
        default=None,
        description='The buyer\'s rating of it, e.g. "Poor", or null when not reported.',
    )


class AliexpressReviewsRatingDistribution(BaseModel):
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


class AliexpressSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[AliexpressSearchItem] = Field(
        description="Matching AliExpress product cards for the requested page. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total products AliExpress reports for the search, or null when the serving source does not report it.",
    )


class AliexpressSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    delivery_days_max: int | None = Field(
        default=None,
        alias="deliveryDaysMax",
        description="Most days the estimated delivery to the requested country takes, or null when not reported.",
    )
    delivery_days_min: int | None = Field(
        default=None,
        alias="deliveryDaysMin",
        description="Fewest days the estimated delivery to the requested country takes, or null when not reported.",
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL, or null when the card shows none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] = Field(
        description="Every product image URL the card carries, primary first; empty when the card shows none."
    )
    is_choice: bool | None = Field(
        default=None,
        alias="isChoice",
        description="True when the product carries the AliExpress Choice badge, or null when the serving source does not report it.",
    )
    is_sponsored: bool | None = Field(
        alias="isSponsored",
        description="True when the card is a paid placement, or null when not reported.",
    )
    listed_utc: float | None = Field(
        default=None,
        alias="listedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. The day the product was first listed, as midnight UTC of that date; null when the serving source does not report it.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="Price before the current discount, or null when the product is not discounted.",
    )
    price: float | None = Field(
        default=None,
        description="Current price in the requested currency, or null when the card shows no price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_id: str = Field(
        alias="productId",
        description="AliExpress product id, the number in the product URL; pass it to the AliExpress Product or AliExpress Reviews SKU. Populated whenever the provider has data for the entity.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated.",
    )
    ship_from: str | None = Field(
        default=None,
        alias="shipFrom",
        description='2-letter ISO code of the country the product ships from, e.g. "CN", or null when not reported.',
    )
    sku_id: str | None = Field(
        default=None,
        alias="skuId",
        description="Id of the product variant the card's price is for, or null when not reported.",
    )
    sold_count: int | None = Field(
        default=None,
        alias="soldCount",
        description='Number of units sold, or null when not shown. One source reads it from AliExpress\'s rounded label, so "60,000+ sold" comes back as 60000. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    store_name: str | None = Field(
        default=None,
        alias="storeName",
        description="Name of the store selling the product, or null when the card does not show it.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="AliExpress product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )


class AliexpressNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AliexpressProductInput],
    ) -> RunResult[AliexpressProductData]:
        """AliExpress Product

        Look up one AliExpress product by id and get its price, original price,
        rating, reviews count, images, options, variants with stock, specifications,
        store, ship-from country and delivery estimate in one normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.aliexpress.product(productId="3256807039224587")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "aliexpress.product", dict(input), options
        )
        return RunResult[AliexpressProductData].model_validate(raw)

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AliexpressReviewsInput],
    ) -> RunResult[AliexpressReviewsData]:
        """AliExpress Reviews

        Get one page of buyer reviews for an AliExpress product by id, with rating,
        text, buyer country, date, bought variant and photos for each review, plus
        the product's total reviews, average rating and star distribution, in one
        normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.aliexpress.reviews(productId="3256807039224587")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "aliexpress.reviews", dict(input), options
        )
        return RunResult[AliexpressReviewsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AliexpressSearchInput],
    ) -> RunResult[AliexpressSearchData]:
        """AliExpress Search

        Search AliExpress by keyword with optional sort, price-range, page, ship-to
        country and currency, and get title, price, original price, units sold and
        image for each product in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.aliexpress.search(query="minecraft room projector")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "aliexpress.search", dict(input), options
        )
        return RunResult[AliexpressSearchData].model_validate(raw)


class AsyncAliexpressNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AliexpressProductInput],
    ) -> RunResult[AliexpressProductData]:
        """AliExpress Product

        Look up one AliExpress product by id and get its price, original price,
        rating, reviews count, images, options, variants with stock, specifications,
        store, ship-from country and delivery estimate in one normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.aliexpress.product(productId="3256807039224587")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "aliexpress.product", dict(input), options
        )
        return RunResult[AliexpressProductData].model_validate(raw)

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AliexpressReviewsInput],
    ) -> RunResult[AliexpressReviewsData]:
        """AliExpress Reviews

        Get one page of buyer reviews for an AliExpress product by id, with rating,
        text, buyer country, date, bought variant and photos for each review, plus
        the product's total reviews, average rating and star distribution, in one
        normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.aliexpress.reviews(productId="3256807039224587")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "aliexpress.reviews", dict(input), options
        )
        return RunResult[AliexpressReviewsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AliexpressSearchInput],
    ) -> RunResult[AliexpressSearchData]:
        """AliExpress Search

        Search AliExpress by keyword with optional sort, price-range, page, ship-to
        country and currency, and get title, price, original price, units sold and
        image for each product in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.aliexpress.search(query="minecraft room projector")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "aliexpress.search", dict(input), options
        )
        return RunResult[AliexpressSearchData].model_validate(raw)
