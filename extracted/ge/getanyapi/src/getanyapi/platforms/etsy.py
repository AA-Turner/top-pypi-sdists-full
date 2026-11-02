# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the etsy platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class EtsyProductInput(TypedDict, total=False):
    """Input for Etsy Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    listingId: Required[str]
    """Etsy listing id, the number in the listing URL (https://www.etsy.com/listing/<id>/...), e.g. 1810545592. The Etsy Search and Etsy Shop Listings SKUs return it as listingId."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "favoriteCount", "materials", "quantityAvailable", "shipFrom", "video"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `materials`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EtsySearchInput(TypedDict, total=False):
    """Input for Etsy Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[float]
    """Optional maximum listing price, in USD. Minimum: 0."""
    minPrice: NotRequired[float]
    """Optional minimum listing price, in USD. Minimum: 0."""
    page: NotRequired[int]
    """1-based results page. Each page is billed as one request. Range: 1 to 250. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "cover letter template". For an Etsy /market page, pass its words: https://www.etsy.com/market/habit_tracker_2027 is the query "habit tracker 2027"."""
    requireFields: NotRequired[list[Literal["rating", "reviewsCount", "totalResults"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `rating`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[Literal["relevance", "newest", "price_low", "price_high"]]
    """Result order: relevance (Etsy's own order, the default), newest, price_low, or price_high. Default: relevance."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EtsyShopInput(TypedDict, total=False):
    """Input for Etsy Shop."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "banner", "description", "followers", "image", "ownerId", "reviewsCount"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `followers`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    shopName: Required[str]
    """Etsy shop name, as in the shop URL (https://www.etsy.com/shop/<name>), e.g. StudioStelleHD. The Etsy Search and Etsy Product SKUs return it as shopName."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EtsyShopListingsInput(TypedDict, total=False):
    """Input for Etsy Shop Listings."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based results page of the shop's listings. Each page is billed as one request. Range: 1 to 250. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    shopName: Required[str]
    """Etsy shop name, as in the shop URL (https://www.etsy.com/shop/<name>), e.g. StudioStelleHD. The Etsy Search and Etsy Product SKUs return it as shopName."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EtsyProductData(BaseModel):
    items: list[EtsyProductItem] = Field(
        description="Listing detail records (one per requested listing id). Populated whenever the provider has data for the entity."
    )


class EtsyProductItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category: str | None = Field(
        default=None,
        description='Etsy category trail from top level down, joined with " > ", e.g. "Jewelry > Necklaces > Monogram & Name Necklaces", or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    description: str | None = Field(
        default=None,
        description="The seller's listing description, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    favorite_count: int | None = Field(
        default=None,
        alias="favoriteCount",
        description="Number of shoppers who favorited the listing, or null when the serving source does not report it.",
    )
    images: list[str] | None = Field(
        default=None,
        description="Listing image URLs, primary first. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    listing_id: str = Field(
        alias="listingId",
        description="Etsy listing id. Populated whenever the provider has data for the entity.",
    )
    materials: list[str] | None = Field(
        default=None,
        description='Materials the seller lists, e.g. ["14k/Yellow Gold/Pearl"], or null when the serving source does not report them.',
    )
    price: float | None = Field(
        default=None,
        description="Current price in the listing currency (the lowest variation price when the listing shows a range), or null when not shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    quantity_available: int | None = Field(
        default=None,
        alias="quantityAvailable",
        description="Units in stock, or null when the serving source does not report it.",
    )
    rating: float | None = Field(
        default=None,
        description="Average rating, 0-5, or null when the listing is unrated. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of reviews, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    ship_from: str | None = Field(
        default=None,
        alias="shipFrom",
        description='Country the listing ships from as a 2-letter ISO code, e.g. "US", or null when not reported.',
    )
    shop_id: str | None = Field(
        alias="shopId",
        description="Etsy id of the shop selling the listing, or null when not reported.",
    )
    shop_name: str | None = Field(
        default=None,
        alias="shopName",
        description="Name of the shop selling the listing; pass it to the Etsy Shop SKU. Null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Listing title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Etsy listing page URL with tracking query parameters removed."
    )
    variations: list[EtsyProductVariation] | None = Field(
        default=None,
        description="The choices a buyer picks from, e.g. Finish and Length, each with its values. Empty when the listing has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video: str | None = Field(
        default=None,
        description="Listing video URL (MP4), or null when the listing has none or the serving source does not report it.",
    )


class EtsyProductVariation(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(
        default=None,
        description='Variation name as the seller lists it, e.g. "Length", or null when the serving source does not report it.',
    )
    values: list[str] | None = Field(
        default=None,
        description='Values a buyer can pick, as Etsy labels them, e.g. ["14 inches ($29.25)", "16 inches ($29.25)"].',
    )


class EtsySearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[EtsySearchItem] = Field(
        description="Matching Etsy listing cards for the requested page, ads included where Etsy shows them. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total listings Etsy reports for the search, or null when the serving source does not report it.",
    )


class EtsySearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL, or null when the listing has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    is_sponsored: bool | None = Field(
        default=None,
        alias="isSponsored",
        description="True when the listing is an ad Etsy placed in the results, or null when not reported.",
    )
    listing_id: str = Field(
        alias="listingId",
        description="Etsy listing id, the number in the listing URL (https://www.etsy.com/listing/<id>/...); pass it to the Etsy Product SKU. Populated whenever the provider has data for the entity.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="Price before the current sale, or null when the listing is not on sale.",
    )
    price: float | None = Field(
        default=None,
        description="Current price in the listing currency, or null when not shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average rating of the listing, 0-5, or null when unrated or the serving source does not report it.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of reviews of the listing, or null when not reported.",
    )
    shop_id: str | None = Field(
        default=None,
        alias="shopId",
        description="Etsy's numeric shop id, or null when not reported.",
    )
    shop_name: str | None = Field(
        default=None,
        alias="shopName",
        description="Name of the shop selling the listing; pass it to the Etsy Shop or Etsy Shop Listings SKU. Null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Listing title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Etsy listing page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )


class EtsyShopData(BaseModel):
    items: list[EtsyShopItem] = Field(
        description="Shop profile records (one per requested shop name). Populated whenever the provider has data for the entity."
    )


class EtsyShopItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    banner: str | None = Field(
        default=None,
        description="Shop banner image URL, or null when the shop has none or the serving source does not report it.",
    )
    description: str | None = Field(
        default=None,
        description="The shop's headline, or null when the serving source does not report it.",
    )
    followers: int | None = Field(
        default=None,
        description="Number of shoppers following the shop, or null when the serving source does not report it.",
    )
    image: str | None = Field(
        default=None,
        description="Shop logo URL, or null when the serving source does not report it.",
    )
    listing_count: int | None = Field(
        default=None,
        alias="listingCount",
        description="Number of active listings, or null when not reported. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    location: str | None = Field(
        default=None,
        description='Where the shop says it is based, e.g. "Shrewsbury, United Kingdom", or null when not shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    name: str = Field(
        description="Shop name as Etsy shows it. Populated whenever the provider has data for the entity."
    )
    owner_id: str | None = Field(
        default=None,
        alias="ownerId",
        description="Etsy user id of the shop owner, or null when the serving source does not report it.",
    )
    rating: float | None = Field(
        default=None,
        description="Average shop rating, 0-5, or null when unrated. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of shop reviews, or null when the serving source does not report it.",
    )
    sales_count: int | None = Field(
        default=None,
        alias="salesCount",
        description="Lifetime sales the shop shows, or null when hidden. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    shop_id: str = Field(
        alias="shopId",
        description="Etsy's numeric shop id. Populated whenever the provider has data for the entity.",
    )
    url: str = Field(
        description="Etsy shop page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )


class EtsyShopListingsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[EtsyShopListingsItem] = Field(
        description="The shop's active listings for the requested page, in the shop's own order. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        alias="totalResults",
        description="Total listings the shop has for sale, or null when not reported.",
    )


class EtsyShopListingsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    image: str | None = Field(
        default=None,
        description="Primary listing image URL, or null when the listing has none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    listing_id: str = Field(
        alias="listingId",
        description="Etsy listing id, the number in the listing URL (https://www.etsy.com/listing/<id>/...); pass it to the Etsy Product SKU. Populated whenever the provider has data for the entity.",
    )
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="Price before the current sale, or null when the listing is not on sale.",
    )
    price: float | None = Field(
        default=None,
        description="Current price in the listing currency, or null when not shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Listing title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Etsy listing page URL with tracking query parameters removed. Populated whenever the provider has data for the entity."
    )


class EtsyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EtsyProductInput],
    ) -> RunResult[EtsyProductData]:
        """Etsy Product

        Look up one Etsy listing by id and get its price, images, description,
        rating, reviews count, shop, category, variations, stock, ship-from country,
        favorites and materials in one normalized response.

        Price: $0.00187 per request.

        Example:
            res = client.etsy.product(listingId="1810545592")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.product", dict(input), options
        )
        return RunResult[EtsyProductData].model_validate(raw)

    def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[EtsySearchInput]
    ) -> RunResult[EtsySearchData]:
        """Etsy Search

        Search Etsy listings by keyword, the same results an Etsy search or /market
        page shows, with optional sort, price range and page, and get title, price,
        original price, image, shop, rating and ad flag for each listing in one
        normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.etsy.search(query="cover letter template")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.search", dict(input), options
        )
        return RunResult[EtsySearchData].model_validate(raw)

    def shop(
        self, *, options: RequestOptions | None = None, **input: Unpack[EtsyShopInput]
    ) -> RunResult[EtsyShopData]:
        """Etsy Shop

        Look up one Etsy shop by name and get its id, location, sales, active
        listings, rating, reviews count, followers, description, logo and banner in
        one normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.etsy.shop(shopName="StudioStelleHD")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.shop", dict(input), options
        )
        return RunResult[EtsyShopData].model_validate(raw)

    def shop_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EtsyShopListingsInput],
    ) -> RunResult[EtsyShopListingsData]:
        """Etsy Shop Listings

        List one Etsy shop's active listings by shop name, a page at a time, and get
        title, price, original price and image for each listing in one normalized
        response.

        Price: $0.0009 per request.

        Example:
            res = client.etsy.shop_listings(shopName="StudioStelleHD")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.shop_listings", dict(input), options
        )
        return RunResult[EtsyShopListingsData].model_validate(raw)


class AsyncEtsyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EtsyProductInput],
    ) -> RunResult[EtsyProductData]:
        """Etsy Product

        Look up one Etsy listing by id and get its price, images, description,
        rating, reviews count, shop, category, variations, stock, ship-from country,
        favorites and materials in one normalized response.

        Price: $0.00187 per request.

        Example:
            res = client.etsy.product(listingId="1810545592")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.product", dict(input), options
        )
        return RunResult[EtsyProductData].model_validate(raw)

    async def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[EtsySearchInput]
    ) -> RunResult[EtsySearchData]:
        """Etsy Search

        Search Etsy listings by keyword, the same results an Etsy search or /market
        page shows, with optional sort, price range and page, and get title, price,
        original price, image, shop, rating and ad flag for each listing in one
        normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.etsy.search(query="cover letter template")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.search", dict(input), options
        )
        return RunResult[EtsySearchData].model_validate(raw)

    async def shop(
        self, *, options: RequestOptions | None = None, **input: Unpack[EtsyShopInput]
    ) -> RunResult[EtsyShopData]:
        """Etsy Shop

        Look up one Etsy shop by name and get its id, location, sales, active
        listings, rating, reviews count, followers, description, logo and banner in
        one normalized response.

        Price: $0.0009 per request.

        Example:
            res = client.etsy.shop(shopName="StudioStelleHD")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.shop", dict(input), options
        )
        return RunResult[EtsyShopData].model_validate(raw)

    async def shop_listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EtsyShopListingsInput],
    ) -> RunResult[EtsyShopListingsData]:
        """Etsy Shop Listings

        List one Etsy shop's active listings by shop name, a page at a time, and get
        title, price, original price and image for each listing in one normalized
        response.

        Price: $0.0009 per request.

        Example:
            res = client.etsy.shop_listings(shopName="StudioStelleHD")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "etsy.shop_listings", dict(input), options
        )
        return RunResult[EtsyShopListingsData].model_validate(raw)
