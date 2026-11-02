# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the ebay platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class EbayProductInput(TypedDict, total=False):
    """Input for eBay Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full eBay listing URL (e.g. https://www.ebay.com/itm/133576802017). The marketplace is taken from the host, so an ebay.co.uk or ebay.de URL returns that site's listing and currency. Item ids come back on every row of ebay.search and ebay.sold_listings."""


class EbayProductFullInput(TypedDict, total=False):
    """Input for eBay Product Full."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full eBay listing URL (e.g. https://www.ebay.com/itm/133576802017). Works on ended and sold listings as well as live ones, so it composes with ebay.sold_listings: pull the comps cheaply, then enrich the few you care about."""


class EbaySearchInput(TypedDict, total=False):
    """Input for eBay Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    condition: NotRequired[
        list[Literal["new", "open_box", "refurbished", "used", "for_parts"]]
    ]
    """Filter by one or more item conditions; omit for all conditions (e.g. ["new", "open_box"])."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1 to 25, default 25). Range: 1 to 25."""
    listingType: NotRequired[Literal["all", "auction", "buy_it_now"]]
    """Restrict to a listing format; omit or use all for both (e.g. buy_it_now for fixed-price only)."""
    maxPrice: NotRequired[int]
    """Optional maximum item price in USD. Minimum: 0."""
    minPrice: NotRequired[int]
    """Optional minimum item price in USD. Minimum: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "nintendo switch" or "vintage levis 501"."""
    requireFields: NotRequired[
        list[
            Literal[
                "listingType",
                "sellerFeedbackCount",
                "sellerFeedbackPercent",
                "sellerName",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `sellerName`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[
        Literal[
            "best_match", "ending_soonest", "newly_listed", "price_low", "price_high"
        ]
    ]
    """Result sort order; omit for eBay's Best Match (e.g. price_low sorts by lowest price plus shipping first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EbaySoldListingsInput(TypedDict, total=False):
    """Input for eBay Sold Listings."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    categoryId: NotRequired[str]
    """Optional numeric eBay category id to search within (e.g. 9355 for Cell Phones & Smartphones, 9394 for Cell Phone Accessories)."""
    condition: NotRequired[Literal["any", "new", "used"]]
    """Item condition filter (e.g. used). Default: any."""
    endDate: NotRequired[str]
    """Only return listings sold on or before this date, inclusive, in YYYY-MM-DD format (e.g. 2026-09-15). This bound is applied to each page after it is fetched, so a page can hold fewer than limit listings, or none, while hasMore is still true: keep requesting the next page until hasMore is false."""
    freeShipping: NotRequired[bool]
    """Not supported by the current sources: only false (no filter) is accepted; true is refused without charge."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-60, default 25). Range: 1 to 60. Default: 25."""
    listingType: NotRequired[Literal["all", "auction", "buy_it_now"]]
    """Restrict to a listing format; omit or use all for both (e.g. auction for auction sales only)."""
    maxPrice: NotRequired[float]
    """Optional maximum sold price in the site currency (e.g. 500). Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum sold price in the site currency (e.g. 200). Minimum: 0."""
    page: NotRequired[int]
    """1-based results page. Use with hasMore in the output to paginate, and keep query, filters, and limit the same while walking pages, because limit sets the page size. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword for sold items (e.g. iphone 13 pro)."""
    returnsAccepted: NotRequired[bool]
    """Not supported by the current sources: only false (no filter) is accepted; true is refused without charge."""
    seller: NotRequired[str]
    """Not supported by the current sources: a request that sets it is refused without charge."""
    site: NotRequired[Literal["ebay.com"]]
    """eBay country site to search. Sold-listing coverage is currently US only. Default: ebay.com."""
    sort: NotRequired[Literal["ended_recently", "price_low", "price_high"]]
    """Result sort order; omitted means ended_recently (e.g. price_high sorts by highest sold price plus shipping first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Only return listings sold on or after this date, inclusive, in YYYY-MM-DD format (e.g. 2026-09-01)."""


class EbaySoldListingsThinInput(TypedDict, total=False):
    """Input for eBay Sold Listings (Basic)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    condition: NotRequired[Literal["any", "new", "used"]]
    """Item condition filter (e.g. used). Default: any."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-60, default 25). Range: 1 to 60. Default: 25."""
    listingType: NotRequired[Literal["all", "auction", "buy_it_now"]]
    """Restrict to a listing format; omit or use all for both (e.g. auction for auction sales only)."""
    maxPrice: NotRequired[float]
    """Optional maximum sold price in the site currency (e.g. 500). Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum sold price in the site currency (e.g. 200). Minimum: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword for sold items (e.g. iphone 13 pro)."""
    site: NotRequired[Literal["ebay.com"]]
    """eBay country site to search. Sold-listing coverage is currently US only. Default: ebay.com."""
    sort: NotRequired[Literal["ended_recently", "price_low", "price_high"]]
    """Result sort order; omitted means ended_recently (e.g. price_high sorts by highest sold price plus shipping first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EbayProductData(BaseModel):
    items: list[EbayProductItem] = Field(
        description="Listing detail record (one element, for the requested listing URL). Populated whenever the provider has data for the entity."
    )


class EbayProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    availability: str | None = Field(
        default=None,
        description="Stock state as eBay reports it (e.g. InStock, OutOfStock).",
    )
    best_offer_enabled: bool | None = Field(
        default=None,
        alias="bestOfferEnabled",
        description="True when the seller accepts Best Offer on this listing.",
    )
    bid_count: int | None = Field(
        default=None,
        alias="bidCount",
        description="Bids placed so far, for auction listings.",
    )
    brand: str | None = Field(
        default=None, description="Brand as listed, when the seller filled it in."
    )
    categories: list[str] | None = Field(
        default=None, description="eBay category path the listing sits in."
    )
    condition: str | None = Field(
        default=None,
        description="Item condition as listed (e.g. New, Used). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None, description="ISO currency code of the price (e.g. USD, GBP)."
    )
    ends_utc: float | None = Field(
        default=None,
        alias="endsUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    free_shipping: bool | None = Field(
        default=None,
        alias="freeShipping",
        description="True when the listing ships free.",
    )
    gtin: str | None = Field(
        default=None, description="Global Trade Item Number (UPC/EAN) as listed."
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[EbayProductImage] | None = Field(
        default=None, description="All listing images, primary first."
    )
    item_id: str = Field(
        alias="itemId",
        description="eBay item identifier. Populated whenever the provider has data for the entity.",
    )
    item_location: str | None = Field(
        default=None,
        alias="itemLocation",
        description="Where the item ships from, as displayed (e.g. Brooklyn, New York, United States).",
    )
    listing_type: str | None = Field(
        default=None,
        alias="listingType",
        description="Sale format (e.g. Buy It Now, Auction).",
    )
    model: str | None = Field(
        default=None, description="Model as listed, when the seller filled it in."
    )
    mpn: str | None = Field(
        default=None,
        description='Manufacturer part number as listed. eBay sellers frequently set this to the literal "Does Not Apply"; ebay.product_full returns the full item-specifics table instead.',
    )
    price: float | None = Field(
        default=None,
        description="Current asking price, or the current bid on a live auction, in the site currency. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_id: str | None = Field(
        default=None,
        alias="productId",
        description="eBay catalog product identifier the listing is matched to.",
    )
    quantity_available: int | None = Field(
        default=None,
        alias="quantityAvailable",
        description="Units the seller still has available, when the listing shows a quantity.",
    )
    quantity_sold: int | None = Field(
        default=None,
        alias="quantitySold",
        description="Units sold on this listing, when eBay shows a sold count.",
    )
    returns_accepted: bool | None = Field(
        default=None,
        alias="returnsAccepted",
        description="True when the seller accepts returns.",
    )
    seller_feedback_count: int | None = Field(
        default=None,
        alias="sellerFeedbackCount",
        description="Seller's lifetime feedback count.",
    )
    seller_feedback_percent: float | None = Field(
        default=None,
        alias="sellerFeedbackPercent",
        description="Seller's positive-feedback percentage.",
    )
    seller_name: str | None = Field(
        default=None,
        alias="sellerName",
        description="Seller's eBay username, or the store's display name when the seller runs an eBay Store. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_url: str | None = Field(
        default=None,
        alias="sellerUrl",
        description="Seller's eBay store or listings page.",
    )
    shipping_cost: float | None = Field(
        default=None,
        alias="shippingCost",
        description="Shipping cost to the default destination as a numeric amount; absent when eBay quotes no flat cost.",
    )
    subtitle: str | None = Field(
        default=None, description="Seller subtitle shown under the listing title."
    )
    title: str = Field(
        description="Listing title as it appears on eBay. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the listing was last modified.",
    )
    url: str = Field(
        description="Canonical listing URL (tracking query params stripped). Populated whenever the provider has data for the entity."
    )
    watchers: int | None = Field(
        default=None,
        description="Number of shoppers watching the listing, when eBay shows it.",
    )


class EbayProductImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    height: int | None = Field(default=None, description="Image height in pixels.")
    url: str | None = Field(default=None, description="Image URL.")
    width: int | None = Field(default=None, description="Image width in pixels.")


class EbayProductFullData(BaseModel):
    items: list[EbayProductFullItem] = Field(
        description="Listing detail record with the full item-specifics table (one element, for the requested listing URL). Populated whenever the provider has data for the entity."
    )


class EbayProductFullItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    availability: str | None = Field(
        default=None,
        description="Stock state as eBay reports it (e.g. in_stock, out_of_stock).",
    )
    brand: str | None = Field(
        default=None, description="Brand as listed, when the seller filled it in."
    )
    category: str | None = Field(
        default=None,
        description='Full category path, e.g. "Electronics>Cell Phones & Accessories>Cell Phones & Smartphones".',
    )
    condition: str | None = Field(
        default=None,
        description="Item condition as listed (e.g. New, Used). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO country code of the eBay marketplace the listing is on.",
    )
    currency: str | None = Field(
        default=None, description="ISO currency code of the price (e.g. USD, GBP)."
    )
    description: str | None = Field(
        default=None,
        description="The seller's own listing description, as plain text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    gtin: str | None = Field(
        default=None, description="Global Trade Item Number (UPC/EAN) as listed."
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None,
        description="All listing image URLs, primary first. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    item_id: str = Field(
        alias="itemId",
        description="eBay item identifier. Populated whenever the provider has data for the entity.",
    )
    item_location: str | None = Field(
        default=None,
        alias="itemLocation",
        description="Where the item ships from, as displayed (e.g. Brooklyn, New York, United States).",
    )
    listing_type: str | None = Field(
        default=None,
        alias="listingType",
        description="Sale format (e.g. Buy It Now, Auction, Buy It Now + Best Offer).",
    )
    price: float | None = Field(
        default=None,
        description="Current effective price in the site currency: the discounted price when the seller is running a sale, otherwise the asking price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    quantity_available: int | None = Field(
        default=None,
        alias="quantityAvailable",
        description="Units the seller still has available, when the listing shows a quantity.",
    )
    quantity_sold: int | None = Field(
        default=None,
        alias="quantitySold",
        description="Units sold on this listing, when eBay shows a sold count.",
    )
    return_window: int | None = Field(
        default=None,
        alias="returnWindow",
        description="Days the buyer has to return the item, when the seller accepts returns.",
    )
    seller_feedback_count: int | None = Field(
        default=None,
        alias="sellerFeedbackCount",
        description="Seller's lifetime feedback count.",
    )
    seller_feedback_percent: float | None = Field(
        default=None,
        alias="sellerFeedbackPercent",
        description="Seller's positive-feedback percentage.",
    )
    seller_name: str | None = Field(
        default=None,
        alias="sellerName",
        description="Seller's eBay username, or the store's display name when the seller runs an eBay Store. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_url: str | None = Field(
        default=None,
        alias="sellerUrl",
        description="Seller's eBay store or listings page.",
    )
    specifications: list[EbayProductFullSpecification] | None = Field(
        default=None,
        description="The listing's item-specifics table, as the seller filled it in. This is where MPN, Model, Storage Capacity, Compatible Brand and every other per-category attribute lives; the set of names varies by category. eBay's boilerplate condition blurb is removed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Listing title as it appears on eBay. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical listing URL (tracking query params stripped). Populated whenever the provider has data for the entity."
    )


class EbayProductFullSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(
        default=None,
        description="Attribute name as eBay labels it (e.g. MPN, Storage Capacity).",
    )
    value: str | None = Field(
        default=None, description="Attribute value as the seller entered it."
    )


class EbaySearchData(BaseModel):
    items: list[EbaySearchItem] = Field(
        description="Listing records: title, price, condition, shipping cost, seller info, image, and item URL. Populated whenever the provider has data for the entity."
    )


class EbaySearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid_count: int | None = Field(
        default=None,
        alias="bidCount",
        description="Bids placed so far, for auction listings.",
    )
    condition: str | None = None
    currency: str | None = Field(
        default=None, description="ISO currency code of the price (e.g. USD)."
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    item_id: str = Field(
        alias="itemId",
        description="eBay item identifier. Populated whenever the provider has data for the entity.",
    )
    listing_type: str | None = Field(
        default=None,
        alias="listingType",
        description="Auction, FixedPrice, etc. Null when the serving source does not publish the listing format.",
    )
    price: float | None = Field(default=None, description="Listing price.")
    seller_feedback_count: float | None = Field(
        default=None,
        alias="sellerFeedbackCount",
        description="Seller's lifetime feedback count, or null when the serving source does not publish it.",
    )
    seller_feedback_percent: float | None = Field(
        default=None,
        alias="sellerFeedbackPercent",
        description="Seller positive-feedback percentage, or null when the serving source does not publish it.",
    )
    seller_name: str | None = Field(
        default=None,
        alias="sellerName",
        description="Seller username, or null when the serving source does not publish the seller.",
    )
    shipping_cost: str | None = Field(
        default=None,
        alias="shippingCost",
        description="Shipping cost or free-delivery label.",
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class EbaySoldListingsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when another results page exists. With endDate set a page can be short or empty while this is still true; request page + 1 to continue.",
    )
    items: list[EbaySoldListingsItem] = Field(
        description="Sold listing records: title, sold price, sale date, condition, seller, and item URL. Populated whenever the provider has data for the entity."
    )


class EbaySoldListingsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    best_offer_accepted: bool | None = Field(
        default=None,
        alias="bestOfferAccepted",
        description="True when eBay marked the sale as Best Offer accepted. Absent when the source could not tell.",
    )
    bid_count: int | None = Field(
        default=None,
        alias="bidCount",
        description="Number of bids the listing received, for auction sales.",
    )
    condition: str | None = Field(
        default=None, description="Item condition as listed (e.g. Pre-Owned)."
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO country code of the eBay marketplace the sale happened on.",
    )
    epid: str | None = Field(
        default=None,
        description="eBay catalog product identifier (ePID), when the listing is matched to a catalog product.",
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None, description="All listing image URLs, primary first."
    )
    item_id: str = Field(
        alias="itemId",
        description="eBay item identifier. Populated whenever the provider has data for the entity.",
    )
    listing_type: str | None = Field(
        default=None,
        alias="listingType",
        description="Sale format: Auction or Fixed price.",
    )
    seller_feedback_count: int | None = Field(
        default=None,
        alias="sellerFeedbackCount",
        description="Seller's lifetime feedback count. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_feedback_percent: float | None = Field(
        default=None,
        alias="sellerFeedbackPercent",
        description="Seller's positive-feedback percentage. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_username: str | None = Field(
        default=None,
        alias="sellerUsername",
        description="Seller's eBay username. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    shipping_cost: str | None = Field(
        default=None,
        alias="shippingCost",
        description='Shipping the buyer paid, in the site currency (e.g. "$5.55"; "$0" is free shipping).',
    )
    sold_currency: str | None = Field(
        default=None,
        alias="soldCurrency",
        description="ISO currency code of the sold price (e.g. USD).",
    )
    sold_price: float | None = Field(
        default=None,
        alias="soldPrice",
        description="Final sold price in the site currency. When bestOfferAccepted is true this is the listing's asking price: eBay does not publish the accepted offer amount.",
    )
    sold_utc: float | None = Field(
        default=None,
        alias="soldUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str = Field(
        description="Listing title as it appeared on eBay. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical listing URL. Populated whenever the provider has data for the entity."
    )


class EbaySoldListingsThinData(BaseModel):
    items: list[EbaySoldListingsThinItem] = Field(
        description="Sold listing records: title, sold price, sale date, condition, format, bids, and item URL, without seller details. Populated whenever the provider has data for the entity."
    )


class EbaySoldListingsThinItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    best_offer_accepted: bool | None = Field(
        default=None,
        alias="bestOfferAccepted",
        description="True when eBay marked the sale as Best Offer accepted. Absent when the source could not tell.",
    )
    bid_count: int | None = Field(
        default=None,
        alias="bidCount",
        description="Number of bids the listing received, for auction sales.",
    )
    condition: str | None = Field(
        default=None, description="Item condition as listed (e.g. Pre-Owned)."
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    item_id: str = Field(
        alias="itemId",
        description="eBay item identifier. Populated whenever the provider has data for the entity.",
    )
    listing_type: str | None = Field(
        default=None,
        alias="listingType",
        description="Sale format: Auction or Fixed price.",
    )
    shipping_cost: str | None = Field(
        default=None,
        alias="shippingCost",
        description='Shipping the buyer paid, in the site currency (e.g. "$5.55"; "$0" is free shipping).',
    )
    sold_currency: str | None = Field(
        default=None,
        alias="soldCurrency",
        description="ISO currency code of the sold price (e.g. USD).",
    )
    sold_price: float | None = Field(
        default=None,
        alias="soldPrice",
        description="Final sold price in the site currency. When bestOfferAccepted is true this is the listing's asking price: eBay does not publish the accepted offer amount.",
    )
    sold_utc: float | None = Field(
        default=None,
        alias="soldUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str = Field(
        description="Listing title as it appeared on eBay. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical listing URL. Populated whenever the provider has data for the entity."
    )


class EbayNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbayProductInput],
    ) -> RunResult[EbayProductData]:
        """eBay Product

        Fetch one eBay listing by URL and get the full offer record: price,
        condition, shipping, item location, seller feedback, quantity, watchers, and
        live auction state (bid count and end time).

        Price: $0.0012 per request.

        Example:
            res = client.ebay.product(url="https://www.ebay.com/itm/133576802017")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.product", dict(input), options
        )
        return RunResult[EbayProductData].model_validate(raw)

    def product_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbayProductFullInput],
    ) -> RunResult[EbayProductFullData]:
        """eBay Product Full

        Fetch one eBay listing by URL with the complete item-specifics table the
        seller filled in (MPN, model, capacity, compatibility and every other
        per-category attribute), the seller's full description, every listing image,
        and the seller's feedback record.

        Price: $0.0018 per request.

        Example:
            res = client.ebay.product_full(url="https://www.ebay.com/itm/133576802017")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.product_full", dict(input), options
        )
        return RunResult[EbayProductFullData].model_validate(raw)

    def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[EbaySearchInput]
    ) -> RunResult[EbaySearchData]:
        """eBay Search

        Search eBay active listings by keyword with optional price-range,
        item-condition, listing-type, and sort filters and get title, price,
        condition, shipping, and seller in one normalized response.

        Price: $0.0012 per request.

        Example:
            res = client.ebay.search(limit=3, query="nintendo switch", sort="price_low")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.search", dict(input), options
        )
        return RunResult[EbaySearchData].model_validate(raw)

    def sold_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbaySoldListingsInput],
    ) -> RunResult[EbaySoldListingsData]:
        """eBay Sold Listings

        Retrieve recently sold eBay listings for any keyword with optional
        price-range, condition, category, sold-date, and sort filters, page by page
        (sold price, sale date, condition, seller, item details); ideal for pricing
        research.

        Price: $0.003 per request.

        Example:
            res = client.ebay.sold_listings(limit=10, query="iphone 13 pro", sort="ended_recently")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.sold_listings", dict(input), options
        )
        return RunResult[EbaySoldListingsData].model_validate(raw)

    def sold_listings_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbaySoldListingsThinInput],
    ) -> RunResult[EbaySoldListingsThinData]:
        """eBay Sold Listings (Basic)

        Retrieve recently sold eBay listings for any keyword with the sold price,
        sale date, condition, format, bids, and whether a Best Offer was accepted,
        without seller details; the lighter sibling of eBay Sold Listings for price
        comps.

        Price: $0.003 per request.

        Example:
            res = client.ebay.sold_listings_thin(limit=10, query="iphone 13 pro", sort="ended_recently")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.sold_listings_thin", dict(input), options
        )
        return RunResult[EbaySoldListingsThinData].model_validate(raw)


class AsyncEbayNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbayProductInput],
    ) -> RunResult[EbayProductData]:
        """eBay Product

        Fetch one eBay listing by URL and get the full offer record: price,
        condition, shipping, item location, seller feedback, quantity, watchers, and
        live auction state (bid count and end time).

        Price: $0.0012 per request.

        Example:
            res = client.ebay.product(url="https://www.ebay.com/itm/133576802017")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.product", dict(input), options
        )
        return RunResult[EbayProductData].model_validate(raw)

    async def product_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbayProductFullInput],
    ) -> RunResult[EbayProductFullData]:
        """eBay Product Full

        Fetch one eBay listing by URL with the complete item-specifics table the
        seller filled in (MPN, model, capacity, compatibility and every other
        per-category attribute), the seller's full description, every listing image,
        and the seller's feedback record.

        Price: $0.0018 per request.

        Example:
            res = client.ebay.product_full(url="https://www.ebay.com/itm/133576802017")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.product_full", dict(input), options
        )
        return RunResult[EbayProductFullData].model_validate(raw)

    async def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[EbaySearchInput]
    ) -> RunResult[EbaySearchData]:
        """eBay Search

        Search eBay active listings by keyword with optional price-range,
        item-condition, listing-type, and sort filters and get title, price,
        condition, shipping, and seller in one normalized response.

        Price: $0.0012 per request.

        Example:
            res = client.ebay.search(limit=3, query="nintendo switch", sort="price_low")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.search", dict(input), options
        )
        return RunResult[EbaySearchData].model_validate(raw)

    async def sold_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbaySoldListingsInput],
    ) -> RunResult[EbaySoldListingsData]:
        """eBay Sold Listings

        Retrieve recently sold eBay listings for any keyword with optional
        price-range, condition, category, sold-date, and sort filters, page by page
        (sold price, sale date, condition, seller, item details); ideal for pricing
        research.

        Price: $0.003 per request.

        Example:
            res = client.ebay.sold_listings(limit=10, query="iphone 13 pro", sort="ended_recently")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.sold_listings", dict(input), options
        )
        return RunResult[EbaySoldListingsData].model_validate(raw)

    async def sold_listings_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EbaySoldListingsThinInput],
    ) -> RunResult[EbaySoldListingsThinData]:
        """eBay Sold Listings (Basic)

        Retrieve recently sold eBay listings for any keyword with the sold price,
        sale date, condition, format, bids, and whether a Best Offer was accepted,
        without seller details; the lighter sibling of eBay Sold Listings for price
        comps.

        Price: $0.003 per request.

        Example:
            res = client.ebay.sold_listings_thin(limit=10, query="iphone 13 pro", sort="ended_recently")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ebay.sold_listings_thin", dict(input), options
        )
        return RunResult[EbaySoldListingsThinData].model_validate(raw)
