# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the mercari platform."""

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


class MercariProductInput(TypedDict, total=False):
    """Input for Mercari Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[Literal["us", "jp"]]
    """Mercari marketplace of the item id: us (USD) or jp (JPY). Ids are not shared between countries. Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    itemId: Required[str]
    """Mercari item id or full listing URL (e.g. m73121443159 or https://www.mercari.com/us/item/m73121443159/). A jp.mercari.com URL is looked up in Japan whatever country says. Every mercari.search and mercari.sold_listings row carries its itemId."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "categories", "sellerJoinedUtc", "sellerOfficial", "sellerQuickShipper"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `sellerJoinedUtc`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class MercariSearchInput(TypedDict, total=False):
    """Input for Mercari Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    brandId: NotRequired[str]
    """Mercari brand id, or several separated by commas; the US and Japan use separate ids (e.g. 319 for Apple in the US). Every US row carries its brandId."""
    categoryId: NotRequired[str]
    """Mercari category id, or several separated by commas; the US and Japan use separate ids and a parent id includes its children (e.g. 778 for US cell phones and smartphones). Every row carries its categoryId."""
    condition: NotRequired[
        list[Literal["new", "like_new", "good", "fair", "poor", "worn"]]
    ]
    """Only listings in any of these condition grades (e.g. ["new", "like_new"]). worn is Japan only."""
    country: NotRequired[Literal["us", "jp"]]
    """Mercari marketplace: us (mercari.com, USD) or jp (jp.mercari.com, JPY). Default: us."""
    cursor: NotRequired[str]
    """Pagination cursor: pass the previous response's nextCursor with the same query and filters; omit for the first page."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[int]
    """Highest price to include, in whole units of the country's currency (e.g. 300). Minimum: 0."""
    minPrice: NotRequired[int]
    """Lowest price to include, in whole units of the country's currency (US dollars or yen) (e.g. 50). Minimum: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword (e.g. nike air jordan 1). Japanese terms return far more in Japan, though Latin brand and model names work."""
    requireFields: NotRequired[list[Literal["categories", "nextCursor", "shopId"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `categories`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal["relevance", "newest", "price_asc", "price_desc", "most_liked"]
    ]
    """Result order; omitted means Mercari's default (relevance). most_liked is Japan only (e.g. price_desc)."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class MercariSoldListingsInput(TypedDict, total=False):
    """Input for Mercari Sold Listings."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    brandId: NotRequired[str]
    """Mercari brand id, or several separated by commas; the US and Japan use separate ids (e.g. 319 for Apple in the US). Every US row carries its brandId."""
    categoryId: NotRequired[str]
    """Mercari category id, or several separated by commas; the US and Japan use separate ids and a parent id includes its children (e.g. 778 for US cell phones and smartphones). Every row carries its categoryId."""
    condition: NotRequired[
        list[Literal["new", "like_new", "good", "fair", "poor", "worn"]]
    ]
    """Only listings in any of these condition grades (e.g. ["new", "like_new"]). worn is Japan only."""
    country: NotRequired[Literal["us", "jp"]]
    """Mercari marketplace: us (mercari.com, USD) or jp (jp.mercari.com, JPY). Default: us."""
    cursor: NotRequired[str]
    """Pagination cursor: pass the previous response's nextCursor with the same query and filters; omit for the first page."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[int]
    """Highest sold price to include, in whole units of the country's currency (e.g. 300). Minimum: 0."""
    minPrice: NotRequired[int]
    """Lowest sold price to include, in whole units of the country's currency (US dollars or yen) (e.g. 50). Minimum: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword (e.g. nike air jordan 1). Japanese terms return far more in Japan, though Latin brand and model names work."""
    requireFields: NotRequired[list[Literal["categories", "nextCursor", "shopId"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `categories`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal[
            "relevance",
            "newest",
            "price_asc",
            "price_desc",
            "most_liked",
            "recently_sold",
        ]
    ]
    """Result order; omitted means Mercari's default (most recently sold first for a US sold search). most_liked is Japan only; recently_sold is US only (e.g. price_desc)."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class MercariProductData(BaseModel):
    items: list[MercariProductItem] = Field(
        description="The one listing record. Populated whenever the provider has data for the entity."
    )


class MercariProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anonymous_shipping: bool | None = Field(
        default=None,
        alias="anonymousShipping",
        description="True when the shipping method hides the names and addresses of buyer and seller from each other. Japan only: null in the US.",
    )
    best_offer_enabled: bool | None = Field(
        default=None,
        alias="bestOfferEnabled",
        description="True when the seller accepts offers on this listing.",
    )
    brand: str | None = Field(
        default=None, description="Brand name the seller tagged; null when untagged."
    )
    brand_id: str | None = Field(
        default=None,
        alias="brandId",
        description="Mercari brand id, usable as the brandId filter in the same country.",
    )
    categories: list[str] | None = Field(
        default=None,
        description="Category path from top level to leaf (e.g. Women, Shoes, Athletic).",
    )
    category: str | None = Field(default=None, description="Leaf category name.")
    category_id: str | None = Field(
        default=None,
        alias="categoryId",
        description="Mercari leaf category id, usable as the categoryId filter in the same country.",
    )
    colors: list[str] | None = Field(
        default=None,
        description="Colour families the seller tagged, as Mercari names them. Japan only: empty in the US and when untagged.",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Number of comments on the listing. Japan only: null in the US.",
    )
    condition: str | None = Field(
        default=None,
        description="Item condition grade: new, like_new, good, fair, poor, or worn (Japan only).",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the item was listed.",
    )
    currency: str | None = Field(
        default=None,
        description="ISO currency code of the price: USD for the US, JPY for Japan. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None, description="Listing description written by the seller."
    )
    handling_days_max: int | None = Field(
        default=None,
        alias="handlingDaysMax",
        description="Most days the seller states it takes to ship after the sale.",
    )
    handling_days_min: int | None = Field(
        default=None,
        alias="handlingDaysMin",
        description="Fewest days the seller states it takes to ship after the sale.",
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None, description="All listing photo URLs, primary first."
    )
    item_id: str = Field(
        alias="itemId",
        description="Mercari item id (m followed by 11 digits, or a 22-character Mercari Shops product id in Japan). Populated whenever the provider has data for the entity.",
    )
    like_count: int | None = Field(
        default=None,
        alias="likeCount",
        description="Number of users who liked the listing.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="First asking price of the listing in USD; differs from price when the seller lowered it or accepted an offer. US only: null in Japan.",
    )
    price: float | None = Field(
        default=None,
        description="Price in the listing currency; it does not include buyer fees, and whether shipping is included depends on shippingPayer. For a sold item (status sold_out or trading) it is the final sale price after any accepted offer. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_id: str | None = Field(
        default=None, alias="sellerId", description="Mercari seller id."
    )
    seller_joined_utc: float | None = Field(
        default=None,
        alias="sellerJoinedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the seller joined Mercari.",
    )
    seller_listings_count: int | None = Field(
        default=None,
        alias="sellerListingsCount",
        description="Number of items the seller has listed.",
    )
    seller_name: str | None = Field(
        default=None, alias="sellerName", description="Seller display name."
    )
    seller_official: bool | None = Field(
        default=None,
        alias="sellerOfficial",
        description="True when the seller is a Mercari official account. Japan only: null in the US.",
    )
    seller_quick_shipper: bool | None = Field(
        default=None,
        alias="sellerQuickShipper",
        description="True when Mercari marks the seller as a quick shipper. Japan only: null in the US.",
    )
    seller_rating: float | None = Field(
        default=None,
        alias="sellerRating",
        description="Seller star rating; null when the seller has no ratings yet.",
    )
    seller_rating_bad: int | None = Field(
        default=None,
        alias="sellerRatingBad",
        description="Number of bad ratings the seller has received. Japan only: null in the US.",
    )
    seller_rating_count: int | None = Field(
        default=None,
        alias="sellerRatingCount",
        description="Number of ratings the seller has received.",
    )
    seller_rating_good: int | None = Field(
        default=None,
        alias="sellerRatingGood",
        description="Number of good ratings the seller has received. Japan only: null in the US.",
    )
    seller_rating_normal: int | None = Field(
        default=None,
        alias="sellerRatingNormal",
        description="Number of normal (neutral) ratings the seller has received. Japan only: null in the US.",
    )
    seller_type: str | None = Field(
        default=None,
        alias="sellerType",
        description="individual for a private seller, shop for a Mercari Shops business seller. Japan only: null in the US.",
    )
    seller_url: str | None = Field(
        default=None,
        alias="sellerUrl",
        description="Seller profile URL. Japan only: null in the US.",
    )
    shipping_method: str | None = Field(
        default=None,
        alias="shippingMethod",
        description="Shipping service the seller chose, as Mercari names it. Japan only: null in the US.",
    )
    shipping_payer: str | None = Field(
        default=None,
        alias="shippingPayer",
        description="Who pays shipping: seller (the price is delivered) or buyer.",
    )
    ships_from: str | None = Field(
        default=None,
        alias="shipsFrom",
        description="Region the item ships from (a US state or Japanese prefecture).",
    )
    size: str | None = Field(
        default=None,
        description="Size label the seller chose (e.g. 8.5 (39)), when the category has sizes.",
    )
    sold_utc: float | None = Field(
        default=None,
        alias="soldUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the item sold. US only, and null unless status is sold_out or trading; in Japan updatedUtc is the nearest proxy.",
    )
    status: str | None = Field(
        default=None,
        description="Listing state: on_sale (active), trading (sold, handover in progress) or sold_out (sold). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Listing title. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the listing last changed.",
    )
    url: str = Field(
        description="Canonical listing URL. Populated whenever the provider has data for the entity."
    )


class MercariSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[MercariSearchItem] = Field(
        description="Active listing records: up to 100 a page in the US and 120 in Japan. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page, or null at the end. Pass it back as cursor with the same query and filters.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="How many listings Mercari reports for the search across all pages. An estimate, not an exact count: broad searches report a ceiling (seen as 10,000 in the US and 15,000 in Japan).",
    )


class MercariSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None,
        description="Brand name the seller tagged; null when untagged (Japan search rows carry no brand: use mercari.product).",
    )
    brand_id: str | None = Field(
        default=None,
        alias="brandId",
        description="Mercari brand id, usable as the brandId filter in the same country.",
    )
    categories: list[str] | None = Field(
        default=None,
        description="Category path from top level to leaf (e.g. Women, Shoes, Athletic). US only: empty on Japan search rows (use mercari.product).",
    )
    category: str | None = Field(
        default=None, description="Leaf category name (US); null on Japan search rows."
    )
    category_id: str | None = Field(
        default=None,
        alias="categoryId",
        description="Mercari leaf category id, usable as the categoryId filter in the same country.",
    )
    condition: str | None = Field(
        default=None,
        description="Item condition grade: new, like_new, good, fair, poor, or worn (Japan only).",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the item was listed. Japan only: null on US search rows (use mercari.product).",
    )
    currency: str | None = Field(
        default=None,
        description="ISO currency code of the price: USD for the US, JPY for Japan. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    item_id: str = Field(
        alias="itemId",
        description="Mercari item id (m followed by 11 digits, or a 22-character Mercari Shops product id in Japan). Populated whenever the provider has data for the entity.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="First asking price of the listing in USD; differs from price when the seller lowered it or accepted an offer. US only: null in Japan.",
    )
    price: float | None = Field(
        default=None,
        description="Current asking price in the listing currency; it does not include buyer fees, and whether shipping is included depends on the listing's shipping terms. On a sold row (status sold_out or trading) it is the final sale price after any accepted offer. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="Mercari seller id; null on a Japan Mercari Shops row that carries none.",
    )
    seller_type: str | None = Field(
        default=None,
        alias="sellerType",
        description="individual for a private seller, shop for a Mercari Shops business seller. Japan only: null in the US.",
    )
    seller_url: str | None = Field(
        default=None,
        alias="sellerUrl",
        description="Seller profile URL. Japan only: null in the US and on a Japan Mercari Shops row that carries no seller id.",
    )
    shipping_payer: str | None = Field(
        default=None,
        alias="shippingPayer",
        description="Who pays shipping: seller (the price is delivered) or buyer. Japan only: null on US search rows (use mercari.product); also null on a Japan Mercari Shops row.",
    )
    shop_id: str | None = Field(
        default=None,
        alias="shopId",
        description="Mercari Shops shop id when sellerType is shop. Japan only: null in the US and for a private seller.",
    )
    size: str | None = Field(
        default=None,
        description="Size label the seller chose (e.g. 8.5 (39)), when the category has sizes.",
    )
    status: str | None = Field(
        default=None,
        description="Listing state: on_sale (active), trading (sold, handover in progress) or sold_out (sold). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Listing title. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the listing last changed. Japan only: null on US search rows.",
    )
    url: str = Field(
        description="Canonical listing URL. Populated whenever the provider has data for the entity."
    )


class MercariSoldListingsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[MercariSoldListingsItem] = Field(
        description="Sold listing records: up to 100 a page in the US and 120 in Japan. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page, or null at the end. Pass it back as cursor with the same query and filters.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="How many listings Mercari reports for the search across all pages. An estimate, not an exact count: broad searches report a ceiling (seen as 10,000 in the US and 15,000 in Japan).",
    )


class MercariSoldListingsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None,
        description="Brand name the seller tagged; null when untagged (Japan search rows carry no brand: use mercari.product).",
    )
    brand_id: str | None = Field(
        default=None,
        alias="brandId",
        description="Mercari brand id, usable as the brandId filter in the same country.",
    )
    categories: list[str] | None = Field(
        default=None,
        description="Category path from top level to leaf (e.g. Women, Shoes, Athletic). US only: empty on Japan search rows (use mercari.product).",
    )
    category: str | None = Field(
        default=None, description="Leaf category name (US); null on Japan search rows."
    )
    category_id: str | None = Field(
        default=None,
        alias="categoryId",
        description="Mercari leaf category id, usable as the categoryId filter in the same country.",
    )
    condition: str | None = Field(
        default=None,
        description="Item condition grade: new, like_new, good, fair, poor, or worn (Japan only).",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the item was listed. Japan only: null on US search rows (use mercari.product).",
    )
    currency: str | None = Field(
        default=None,
        description="ISO currency code of the price: USD for the US, JPY for Japan. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    item_id: str = Field(
        alias="itemId",
        description="Mercari item id (m followed by 11 digits, or a 22-character Mercari Shops product id in Japan). Populated whenever the provider has data for the entity.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="First asking price of the listing in USD; differs from price when the seller lowered it or accepted an offer. US only: null in Japan.",
    )
    price: float | None = Field(
        default=None,
        description="Price in the listing currency. On a sold row (status sold_out or trading) this is the final sale price after any accepted offer; it does not include buyer fees, and whether shipping is included depends on the listing's shipping terms. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="Mercari seller id; null on a Japan Mercari Shops row that carries none.",
    )
    seller_type: str | None = Field(
        default=None,
        alias="sellerType",
        description="individual for a private seller, shop for a Mercari Shops business seller. Japan only: null in the US.",
    )
    seller_url: str | None = Field(
        default=None,
        alias="sellerUrl",
        description="Seller profile URL. Japan only: null in the US and on a Japan Mercari Shops row that carries no seller id.",
    )
    shipping_payer: str | None = Field(
        default=None,
        alias="shippingPayer",
        description="Who pays shipping: seller (the price is delivered) or buyer. Japan only: null on US search rows (use mercari.product); also null on a Japan Mercari Shops row.",
    )
    shop_id: str | None = Field(
        default=None,
        alias="shopId",
        description="Mercari Shops shop id when sellerType is shop. Japan only: null in the US and for a private seller.",
    )
    size: str | None = Field(
        default=None,
        description="Size label the seller chose (e.g. 8.5 (39)), when the category has sizes.",
    )
    status: str | None = Field(
        default=None,
        description="Listing state: on_sale (active), trading (sold, handover in progress) or sold_out (sold). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Listing title. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the listing last changed. Japan only: null on US search rows.",
    )
    url: str = Field(
        description="Canonical listing URL. Populated whenever the provider has data for the entity."
    )


class MercariNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariProductInput],
    ) -> RunResult[MercariProductData]:
        """Mercari Product

        Get one Mercari US or Japan listing by item id or URL: title, description,
        price, original price, status, condition, brand, category, size, photos,
        shipping terms (who pays, method, ships-from region, handling days), whether
        offers are accepted, likes, seller name, rating, listing count and join
        date, when it was listed, and for a sold US item when it sold. For a sold
        item the price is the final sale price after any accepted offer.

        Price: $0.0012 per request.

        Example:
            res = client.mercari.product(itemId="m73121443159")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "mercari.product", dict(input), options
        )
        return RunResult[MercariProductData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSearchInput],
    ) -> RunResult[MercariSearchData]:
        """Mercari Search

        Search active Mercari US or Japan listings for sale by keyword with optional
        price-range, condition, category, brand, and sort filters, page by page,
        with the total result count (price, original price, condition, brand,
        category path, size, seller, image; who pays shipping in Japan). The price
        excludes buyer fees, and whether shipping is included depends on the
        listing's shipping terms.

        Price: $0.0012 per request.

        Example:
            res = client.mercari.search(query="nike air jordan 1")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "mercari.search", dict(input), options
        )
        return RunResult[MercariSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSearchInput],
    ) -> Paginator[MercariSearchItem, MercariSearchData]:
        """Iterate Mercari Search results, following pagination cursors.

        Yields validated `MercariSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "mercari.search",
            dict(input),
            "items",
            item_model=MercariSearchItem,
            data_model=MercariSearchData,
            bare=False,
            options=options,
        )

    def sold_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSoldListingsInput],
    ) -> RunResult[MercariSoldListingsData]:
        """Mercari Sold Listings

        Search Mercari US or Japan sold listings by keyword with optional
        price-range, condition, category, brand, and sort filters, page by page,
        with the total result count; ideal for resale pricing research. The sold
        price is the final price after any accepted offer; it does not include buyer
        fees, and whether shipping is included depends on the listing's shipping
        terms. Rows carry no sale date: call mercari.product for soldUtc (US only).

        Price: $0.0012 per request.

        Example:
            res = client.mercari.sold_listings(query="nike air jordan 1")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "mercari.sold_listings", dict(input), options
        )
        return RunResult[MercariSoldListingsData].model_validate(raw)

    def iter_sold_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSoldListingsInput],
    ) -> Paginator[MercariSoldListingsItem, MercariSoldListingsData]:
        """Iterate Mercari Sold Listings results, following pagination cursors.

        Yields validated `MercariSoldListingsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "mercari.sold_listings",
            dict(input),
            "items",
            item_model=MercariSoldListingsItem,
            data_model=MercariSoldListingsData,
            bare=False,
            options=options,
        )


class AsyncMercariNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariProductInput],
    ) -> RunResult[MercariProductData]:
        """Mercari Product

        Get one Mercari US or Japan listing by item id or URL: title, description,
        price, original price, status, condition, brand, category, size, photos,
        shipping terms (who pays, method, ships-from region, handling days), whether
        offers are accepted, likes, seller name, rating, listing count and join
        date, when it was listed, and for a sold US item when it sold. For a sold
        item the price is the final sale price after any accepted offer.

        Price: $0.0012 per request.

        Example:
            res = client.mercari.product(itemId="m73121443159")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "mercari.product", dict(input), options
        )
        return RunResult[MercariProductData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSearchInput],
    ) -> RunResult[MercariSearchData]:
        """Mercari Search

        Search active Mercari US or Japan listings for sale by keyword with optional
        price-range, condition, category, brand, and sort filters, page by page,
        with the total result count (price, original price, condition, brand,
        category path, size, seller, image; who pays shipping in Japan). The price
        excludes buyer fees, and whether shipping is included depends on the
        listing's shipping terms.

        Price: $0.0012 per request.

        Example:
            res = client.mercari.search(query="nike air jordan 1")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "mercari.search", dict(input), options
        )
        return RunResult[MercariSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSearchInput],
    ) -> AsyncPaginator[MercariSearchItem, MercariSearchData]:
        """Iterate Mercari Search results, following pagination cursors.

        Yields validated `MercariSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "mercari.search",
            dict(input),
            "items",
            item_model=MercariSearchItem,
            data_model=MercariSearchData,
            bare=False,
            options=options,
        )

    async def sold_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSoldListingsInput],
    ) -> RunResult[MercariSoldListingsData]:
        """Mercari Sold Listings

        Search Mercari US or Japan sold listings by keyword with optional
        price-range, condition, category, brand, and sort filters, page by page,
        with the total result count; ideal for resale pricing research. The sold
        price is the final price after any accepted offer; it does not include buyer
        fees, and whether shipping is included depends on the listing's shipping
        terms. Rows carry no sale date: call mercari.product for soldUtc (US only).

        Price: $0.0012 per request.

        Example:
            res = client.mercari.sold_listings(query="nike air jordan 1")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "mercari.sold_listings", dict(input), options
        )
        return RunResult[MercariSoldListingsData].model_validate(raw)

    def iter_sold_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MercariSoldListingsInput],
    ) -> AsyncPaginator[MercariSoldListingsItem, MercariSoldListingsData]:
        """Iterate Mercari Sold Listings results, following pagination cursors.

        Yields validated `MercariSoldListingsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "mercari.sold_listings",
            dict(input),
            "items",
            item_model=MercariSoldListingsItem,
            data_model=MercariSoldListingsData,
            bare=False,
            options=options,
        )
