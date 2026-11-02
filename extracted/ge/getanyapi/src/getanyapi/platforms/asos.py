# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the asos platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class AsosProductInput(TypedDict, total=False):
    """Input for ASOS Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["sizeGuide"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `sizeGuide`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """ASOS product page URL, e.g. https://www.asos.com/pullbear/pullbear-casual-trainers-in-white/prd/211299341, or the short form https://www.asos.com/prd/211299341. The store is read from the URL path (/us/, /au/, /de/ and so on; none means the UK store), and prices come back in that store's currency."""


class AsosSearchInput(TypedDict, total=False):
    """Input for ASOS Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[
        Literal["gb", "us", "au", "de", "fr", "it", "es", "nl", "se", "dk", "pl"]
    ]
    """ASOS country store to search, which also sets the price currency (gb GBP, us USD, au AUD, de/fr/it/es/nl EUR, se SEK, dk DKK, pl PLN); defaults to gb, the UK store. Product ids and URLs are store-specific. Default: gb."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum product price, in the store's currency. Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum product price, in the store's currency. Minimum: 0."""
    page: NotRequired[int]
    """1-based results page of 48 products. Each page is billed as one request. Range: 1 to 200. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "white sneakers" or "summer dress"."""
    requireFields: NotRequired[list[Literal["inStock"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `inStock`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[Literal["best_match", "new", "price_low", "price_high"]]
    """Result sort order; omit for ASOS's recommended order (e.g. new for newest arrivals first)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AsosProductData(BaseModel):
    items: list[AsosProductItem] = Field(
        description="Product detail records (one per requested product URL). Populated whenever the provider has data for the entity."
    )


class AsosProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None,
        description="Brand name, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    care_instructions: str | None = Field(
        default=None,
        alias="careInstructions",
        description='Care instructions as ASOS lists them, e.g. "Machine wash according to instructions on care label", or null when not listed.',
    )
    colour: str | None = Field(
        default=None,
        description="Colour name as ASOS lists it, or null when not reported.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "GBP" or "USD", or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    description: str | None = Field(
        default=None,
        description="Product description as ASOS publishes it (HTML), or null when the listing has none.",
    )
    gender: str | None = Field(
        default=None,
        description='Department the product is listed under, e.g. "Men" or "Women", or null when not reported.',
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None, description="All product image URLs, primary first."
    )
    in_stock: bool | None = Field(
        default=None,
        alias="inStock",
        description="True when at least one size is in stock, false when none is, or null when not reported.",
    )
    is_discontinued: bool | None = Field(
        default=None,
        alias="isDiscontinued",
        description="True when ASOS has discontinued the product, or null when not reported.",
    )
    materials: str | None = Field(
        default=None,
        description='ASOS\'s "About me" section: fabric and material composition, as HTML, or null when not listed.',
    )
    price: float | None = Field(
        default=None,
        description="Current price in the store's currency, or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_id: str | None = Field(
        default=None,
        alias="productId",
        description="ASOS product id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    size_guide: str | None = Field(
        default=None,
        alias="sizeGuide",
        description="Link to the ASOS size guide for this product, or null when the serving source does not report one.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="ASOS product page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )
    variants: list[AsosProductVariant] | None = Field(
        default=None, description="One entry per size the product is sold in."
    )


class AsosProductVariant(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    colour: str | None = Field(
        default=None,
        description="Colour of this variant as ASOS lists it, or null when not reported.",
    )
    currency: str | None = Field(
        default=None,
        description='Currency code of this size\'s price, e.g. "GBP", or null when not shown.',
    )
    ean: str | None = Field(
        default=None, description="EAN barcode of this size, or null when not reported."
    )
    in_stock: bool | None = Field(
        default=None,
        alias="inStock",
        description="True when this size is in stock, or null when not reported.",
    )
    price: float | None = Field(
        default=None,
        description="Current price of this size in the store's currency, or null when not shown.",
    )
    size: str | None = Field(
        default=None,
        description='Size label as ASOS shows it, e.g. "UK 8", or null when not reported.',
    )
    sku: str | None = Field(
        default=None, description="ASOS SKU of this size, or null when not reported."
    )
    variant_id: str | None = Field(
        default=None,
        alias="variantId",
        description="ASOS variant id of this size, or null when not reported.",
    )


class AsosSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when another page of results follows this one (request it with page + 1), or null when not reported.",
    )
    items: list[AsosSearchItem] = Field(
        description="Matching ASOS product records for the requested page. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total number of matching products ASOS reports for the query, or null when not reported.",
    )


class AsosSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None, description="Brand name, or null when not reported."
    )
    colour: str | None = Field(
        default=None,
        description="Colour name as ASOS lists it, or null when not reported.",
    )
    colour_way_id: str | None = Field(
        default=None,
        alias="colourWayId",
        description="Id of the colourway this result shows; it appears as #colourWayId-<id> in ASOS product links. Null when not reported.",
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "GBP" or "USD", or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    images: list[str] | None = Field(
        default=None, description="All product image URLs, primary first."
    )
    in_stock: bool | None = Field(
        default=None,
        alias="inStock",
        description="True when the product is in stock, false when it is not, or null when the serving source does not report stock in search results.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Previous price when the product is marked down, or null when it is not.",
    )
    position: int | None = Field(
        default=None, description="1-based position of the result in this page."
    )
    price: float | None = Field(
        default=None,
        description="Current price in the store's currency, or null when the result shows no price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_code: str | None = Field(
        default=None,
        alias="productCode",
        description="ASOS product code (the style number printed on the product page), or null when not reported.",
    )
    product_id: str = Field(
        alias="productId",
        description="ASOS product id, the number after /prd/ in the product URL; use the product URL with the ASOS Product SKU. Populated whenever the provider has data for the entity.",
    )
    selling_fast: bool | None = Field(
        default=None,
        alias="sellingFast",
        description="True when ASOS flags the product as selling fast, or null when not reported.",
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="ASOS product page URL in the searched store, with tracking and colour fragments removed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class AsosNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AsosProductInput],
    ) -> RunResult[AsosProductData]:
        """ASOS Product

        Fetch an ASOS product by URL from any of its 11 country stores and get
        title, price, brand, colour, description, images, and per-size stock in one
        normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.asos.product(url="https://www.asos.com/pullbear/pullbear-casual-trainers-in-white/prd/211299341")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "asos.product", dict(input), options
        )
        return RunResult[AsosProductData].model_validate(raw)

    def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[AsosSearchInput]
    ) -> RunResult[AsosSearchData]:
        """ASOS Search

        Search ASOS by keyword in any of its 11 country stores with optional sort,
        price-range, and page filters and get title, price, brand, and colour for
        each product in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.asos.search(country="us", query="white sneakers")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "asos.search", dict(input), options
        )
        return RunResult[AsosSearchData].model_validate(raw)


class AsyncAsosNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AsosProductInput],
    ) -> RunResult[AsosProductData]:
        """ASOS Product

        Fetch an ASOS product by URL from any of its 11 country stores and get
        title, price, brand, colour, description, images, and per-size stock in one
        normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.asos.product(url="https://www.asos.com/pullbear/pullbear-casual-trainers-in-white/prd/211299341")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "asos.product", dict(input), options
        )
        return RunResult[AsosProductData].model_validate(raw)

    async def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[AsosSearchInput]
    ) -> RunResult[AsosSearchData]:
        """ASOS Search

        Search ASOS by keyword in any of its 11 country stores with optional sort,
        price-range, and page filters and get title, price, brand, and colour for
        each product in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.asos.search(country="us", query="white sneakers")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "asos.search", dict(input), options
        )
        return RunResult[AsosSearchData].model_validate(raw)
