# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the shopify platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class ShopifyProductInput(TypedDict, total=False):
    """Input for Shopify Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    product: Required[str]
    """Product handle, the slug after /products/ in the product URL, e.g. mens-strider; the full product page URL also works."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    store: Required[str]
    """Domain or URL of a public Shopify store, e.g. allbirds.com or https://kith.com. A store on its own domain is addressed by that domain."""


class ShopifyProductsInput(TypedDict, total=False):
    """Input for Shopify Store Products."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Products the store is asked for per page (1-250, default 50). The filters below are applied to that page, so a filtered page can hold fewer, even none while hasMore is true. Range: 1 to 250. Default: 50."""
    maxPrice: NotRequired[float]
    """Only products priced at or below this, in the store's currency. Minimum: 0."""
    minPrice: NotRequired[float]
    """Only products priced at or above this, in the store's currency. Minimum: 0."""
    onlyInStock: NotRequired[bool]
    """Only products with at least one variant in stock. Default: false."""
    onlyOnSale: NotRequired[bool]
    """Only products with at least one discounted variant. Default: false."""
    page: NotRequired[int]
    """1-based page of the store's product list. Each page is billed as one request. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    productType: NotRequired[str]
    """Only products whose product type contains this text, e.g. "Shoes"."""
    publishedWithinDays: NotRequired[int]
    """Only products published to the store within the last this many days. Minimum: 1."""
    skuContains: NotRequired[str]
    """Only products with a variant whose SKU code contains this text."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    store: Required[str]
    """Domain or URL of a public Shopify store, e.g. allbirds.com or https://kith.com. A store on its own domain is addressed by that domain."""
    tags: NotRequired[list[str]]
    """Only products carrying at least one of these tags."""
    titleContains: NotRequired[str]
    """Only products whose title contains this text."""
    vendor: NotRequired[str]
    """Only products whose vendor (brand) contains this text."""


class ShopifySearchInput(TypedDict, total=False):
    """Input for Shopify Store Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "wool" or "hoodie"."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    store: Required[str]
    """Domain or URL of a public Shopify store, e.g. allbirds.com or https://kith.com. A store on its own domain is addressed by that domain."""


class ShopifyStoreInput(TypedDict, total=False):
    """Input for Shopify Store Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    store: Required[str]
    """Domain or URL of a public Shopify store, e.g. allbirds.com or https://kith.com. A store on its own domain is addressed by that domain."""


class ShopifyProductData(BaseModel):
    items: list[ShopifyProductItem] = Field(
        description="The requested product (one record). Populated whenever the provider has data for the entity."
    )


class ShopifyProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the product was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when the store does not state it.',
    )
    description: str | None = Field(
        default=None,
        description="Product description as plain text, or null when the product has none.",
    )
    handle: str = Field(
        description="Product handle, the slug after /products/ in the product URL; pass it to the Shopify Product SKU for the full product. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Main product image URL, or null when the product has no image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None,
        description="All product image URLs, main image first; empty when the product has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    in_stock: bool = Field(
        alias="inStock",
        description="True when at least one variant can be bought now. Populated whenever the provider has data for the entity.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Lowest regular (compare-at) price when the product is on sale, or null when it is not discounted.",
    )
    on_sale: bool = Field(
        alias="onSale",
        description="True when at least one variant is priced below its regular price. Populated whenever the provider has data for the entity.",
    )
    options: list[ShopifyProductOption] | None = Field(
        default=None,
        description="Options the variants differ by, e.g. Size or Color, each with its values; empty when the product has a single variant.",
    )
    price: float = Field(
        description="Lowest variant price in the store's currency. Populated whenever the provider has data for the entity."
    )
    price_max: float = Field(
        alias="priceMax",
        description="Highest variant price in the store's currency; equals price when every variant costs the same. Populated whenever the provider has data for the entity.",
    )
    product_id: str = Field(
        alias="productId",
        description="Shopify product id. Populated whenever the provider has data for the entity.",
    )
    product_type: str | None = Field(
        default=None,
        alias="productType",
        description='Product type the store assigns, e.g. "Shoes", or null when it sets none.',
    )
    published_utc: float | None = Field(
        default=None,
        alias="publishedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the product was published to the store. Multiply by 1000 for a JS Date in milliseconds.",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Tags the store attaches to the product, as the store writes them; empty when it has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the product was last updated. Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )
    variants: list[ShopifyProductVariant] | None = Field(
        default=None,
        description="Every purchasable variant of the product, e.g. one per size and color. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    vendor: str | None = Field(
        default=None,
        description="Vendor (brand) the store lists the product under, or null when it sets none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class ShopifyProductOption(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = Field(description='Option name, e.g. "Size".')
    values: list[str] = Field(
        description="Values the option takes, in the store's order."
    )


class ShopifyProductVariant(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    in_stock: bool = Field(
        alias="inStock", description="True when this variant can be bought now."
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Regular (compare-at) price when the variant's product is on sale, or null when it is not discounted.",
    )
    options: list[str] | None = Field(
        default=None,
        description="This variant's value for each of the product's options, in option order.",
    )
    price: float = Field(description="Variant price in the store's currency.")
    sku: str | None = Field(
        default=None,
        description="The store's SKU code for the variant, or null when it sets none.",
    )
    title: str = Field(
        description='Variant title, its option values joined, e.g. "10 / Black".'
    )
    variant_id: str = Field(alias="variantId", description="Shopify variant id.")


class ShopifyProductsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when another page of the store's products follows this one (request it with page + 1), even when filters left this page empty; null when not reported.",
    )
    items: list[ShopifyProductsItem] = Field(
        description="Products on the requested page, after any filters. Populated whenever the provider has data for the entity."
    )


class ShopifyProductsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the product was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when the store does not state it.',
    )
    description: str | None = Field(
        default=None,
        description="Product description as plain text, or null when the product has none.",
    )
    handle: str = Field(
        description="Product handle, the slug after /products/ in the product URL; pass it to the Shopify Product SKU for the full product. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Main product image URL, or null when the product has no image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None,
        description="All product image URLs, main image first; empty when the product has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    in_stock: bool = Field(
        alias="inStock",
        description="True when at least one variant can be bought now. Populated whenever the provider has data for the entity.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Lowest regular (compare-at) price when the product is on sale, or null when it is not discounted.",
    )
    on_sale: bool = Field(
        alias="onSale",
        description="True when at least one variant is priced below its regular price. Populated whenever the provider has data for the entity.",
    )
    options: list[ShopifyProductsOption] | None = Field(
        default=None,
        description="Options the variants differ by, e.g. Size or Color, each with its values; empty when the product has a single variant.",
    )
    price: float = Field(
        description="Lowest variant price in the store's currency. Populated whenever the provider has data for the entity."
    )
    price_max: float = Field(
        alias="priceMax",
        description="Highest variant price in the store's currency; equals price when every variant costs the same. Populated whenever the provider has data for the entity.",
    )
    product_id: str = Field(
        alias="productId",
        description="Shopify product id. Populated whenever the provider has data for the entity.",
    )
    product_type: str | None = Field(
        default=None,
        alias="productType",
        description='Product type the store assigns, e.g. "Shoes", or null when it sets none.',
    )
    published_utc: float | None = Field(
        default=None,
        alias="publishedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the product was published to the store. Multiply by 1000 for a JS Date in milliseconds.",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Tags the store attaches to the product, as the store writes them; empty when it has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the product was last updated. Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )
    variants: list[ShopifyProductsVariant] | None = Field(
        default=None,
        description="Every purchasable variant of the product, e.g. one per size and color. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    vendor: str | None = Field(
        default=None,
        description="Vendor (brand) the store lists the product under, or null when it sets none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class ShopifyProductsOption(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = Field(description='Option name, e.g. "Size".')
    values: list[str] = Field(
        description="Values the option takes, in the store's order."
    )


class ShopifyProductsVariant(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    in_stock: bool = Field(
        alias="inStock", description="True when this variant can be bought now."
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Regular (compare-at) price when the variant's product is on sale, or null when it is not discounted.",
    )
    options: list[str] | None = Field(
        default=None,
        description="This variant's value for each of the product's options, in option order.",
    )
    price: float = Field(description="Variant price in the store's currency.")
    sku: str | None = Field(
        default=None,
        description="The store's SKU code for the variant, or null when it sets none.",
    )
    title: str = Field(
        description='Variant title, its option values joined, e.g. "10 / Black".'
    )
    variant_id: str = Field(alias="variantId", description="Shopify variant id.")


class ShopifySearchData(BaseModel):
    items: list[ShopifySearchItem] = Field(
        description="The store's top matches for the query, in its own order; Shopify's store search returns at most 10. Populated whenever the provider has data for the entity."
    )


class ShopifySearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when the store does not state it.',
    )
    handle: str = Field(
        description="Product handle, the slug after /products/ in the product URL; pass it to the Shopify Product SKU for the full product. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Main product image URL, or null when the product has no image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None,
        description="All product image URLs, main image first; empty when the product has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    in_stock: bool = Field(
        alias="inStock",
        description="True when at least one variant can be bought now. Populated whenever the provider has data for the entity.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Lowest regular (compare-at) price when the product is on sale, or null when it is not discounted.",
    )
    on_sale: bool = Field(
        alias="onSale",
        description="True when at least one variant is priced below its regular price. Populated whenever the provider has data for the entity.",
    )
    price: float = Field(
        description="Lowest variant price in the store's currency. Populated whenever the provider has data for the entity."
    )
    price_max: float = Field(
        alias="priceMax",
        description="Highest variant price in the store's currency; equals price when every variant costs the same. Populated whenever the provider has data for the entity.",
    )
    product_id: str = Field(
        alias="productId",
        description="Shopify product id. Populated whenever the provider has data for the entity.",
    )
    product_type: str | None = Field(
        default=None,
        alias="productType",
        description='Product type the store assigns, e.g. "Shoes", or null when it sets none.',
    )
    tags: list[str] | None = Field(
        default=None,
        description="Tags the store attaches to the product, as the store writes them; empty when it has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )
    vendor: str | None = Field(
        default=None,
        description="Vendor (brand) the store lists the product under, or null when it sets none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class ShopifyStoreData(BaseModel):
    items: list[ShopifyStoreItem] = Field(
        description="The requested store (one record). Populated whenever the provider has data for the entity."
    )


class ShopifyStoreItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(
        default=None,
        description="City of the store's business address, or null when not reported.",
    )
    collections_count: int | None = Field(
        default=None,
        alias="collectionsCount",
        description="Number of collections the store publishes, as the store reports it, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    country: str | None = Field(
        default=None,
        description="Two-letter country code of the store's business address, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str = Field(
        description='The store\'s currency code, e.g. "USD". Populated whenever the provider has data for the entity.'
    )
    description: str | None = Field(
        default=None,
        description="Store description as the store publishes it, or null when it has none.",
    )
    domain: str = Field(
        description="The store's primary domain, e.g. www.allbirds.com. Populated whenever the provider has data for the entity."
    )
    name: str = Field(
        description="Store name. Populated whenever the provider has data for the entity."
    )
    products_count: int | None = Field(
        default=None,
        alias="productsCount",
        description="Number of products the store publishes, as the store reports it, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    region: str | None = Field(
        default=None,
        description="State or province of the store's business address, or null when not reported.",
    )
    ships_to_countries: list[str] | None = Field(
        default=None,
        alias="shipsToCountries",
        description="Two-letter codes of the countries the store ships to; empty when not reported.",
    )
    shopify_domain: str | None = Field(
        default=None,
        alias="shopifyDomain",
        description="The store's myshopify.com domain, or null when not reported.",
    )
    social_links: list[str] | None = Field(
        default=None,
        alias="socialLinks",
        description="Social profile URLs the store links to; empty when it lists none.",
    )
    url: str | None = Field(
        default=None, description="Store home page URL, or null when not reported."
    )


class ShopifyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifyProductInput],
    ) -> RunResult[ShopifyProductData]:
        """Shopify Product

        Look up one product on any public Shopify store by its handle or product
        page URL and get title, vendor, type, tags, description, price range, sale
        price, stock, images, options and every variant's SKU, price and stock in
        one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.product(product="mens-strider", store="allbirds.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.product", dict(input), options
        )
        return RunResult[ShopifyProductData].model_validate(raw)

    def products(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifyProductsInput],
    ) -> RunResult[ShopifyProductsData]:
        """Shopify Store Products

        List the products of any public Shopify store by its domain, a page at a
        time, with title, vendor, type, tags, price range, sale price, stock,
        images, options and every variant's SKU, price and stock. Filter by vendor,
        type, tag, title, SKU, price, sale, stock or recent arrivals. A domain that
        is not a public Shopify store comes back not found.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.products(limit=10, store="allbirds.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.products", dict(input), options
        )
        return RunResult[ShopifyProductsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifySearchInput],
    ) -> RunResult[ShopifySearchData]:
        """Shopify Store Search

        Search one public Shopify store's products by keyword with the store's own
        search and get its top matches with title, vendor, type, tags, price range,
        sale price, stock and images. A domain that is not a public Shopify store
        comes back not found.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.search(query="wool", store="allbirds.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.search", dict(input), options
        )
        return RunResult[ShopifySearchData].model_validate(raw)

    def store(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifyStoreInput],
    ) -> RunResult[ShopifyStoreData]:
        """Shopify Store Profile

        Look up any public Shopify store by its domain and get its name,
        description, currency, country and city, the countries it ships to, its
        published product and collection counts and its social links in one
        normalized response. A domain that is not a public Shopify store comes back
        not found.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.store(store="allbirds.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.store", dict(input), options
        )
        return RunResult[ShopifyStoreData].model_validate(raw)


class AsyncShopifyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifyProductInput],
    ) -> RunResult[ShopifyProductData]:
        """Shopify Product

        Look up one product on any public Shopify store by its handle or product
        page URL and get title, vendor, type, tags, description, price range, sale
        price, stock, images, options and every variant's SKU, price and stock in
        one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.product(product="mens-strider", store="allbirds.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.product", dict(input), options
        )
        return RunResult[ShopifyProductData].model_validate(raw)

    async def products(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifyProductsInput],
    ) -> RunResult[ShopifyProductsData]:
        """Shopify Store Products

        List the products of any public Shopify store by its domain, a page at a
        time, with title, vendor, type, tags, price range, sale price, stock,
        images, options and every variant's SKU, price and stock. Filter by vendor,
        type, tag, title, SKU, price, sale, stock or recent arrivals. A domain that
        is not a public Shopify store comes back not found.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.products(limit=10, store="allbirds.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.products", dict(input), options
        )
        return RunResult[ShopifyProductsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifySearchInput],
    ) -> RunResult[ShopifySearchData]:
        """Shopify Store Search

        Search one public Shopify store's products by keyword with the store's own
        search and get its top matches with title, vendor, type, tags, price range,
        sale price, stock and images. A domain that is not a public Shopify store
        comes back not found.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.search(query="wool", store="allbirds.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.search", dict(input), options
        )
        return RunResult[ShopifySearchData].model_validate(raw)

    async def store(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ShopifyStoreInput],
    ) -> RunResult[ShopifyStoreData]:
        """Shopify Store Profile

        Look up any public Shopify store by its domain and get its name,
        description, currency, country and city, the countries it ships to, its
        published product and collection counts and its social links in one
        normalized response. A domain that is not a public Shopify store comes back
        not found.

        Price: $0.00085 per request.

        Example:
            res = client.shopify.store(store="allbirds.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "shopify.store", dict(input), options
        )
        return RunResult[ShopifyStoreData].model_validate(raw)
