# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the google_shopping platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GoogleShoppingSearchInput(TypedDict, total=False):
    """Input for Google Shopping Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    condition: NotRequired[Literal["ANY", "NEW", "USED", "REFURBISHED"]]
    """Only return products in this condition (e.g. "USED"); defaults to any condition."""
    country: NotRequired[str]
    """ISO 3166-1 alpha-2 country code for localized results (e.g. "us", "gb", "de"). Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """ISO 639-1 language code for results (e.g. "en", "es", "fr"). Default: en."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-10, default 10). Range: 1 to 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Product name, brand, or keywords to search for (e.g. "Nike running shoes")."""
    requireFields: NotRequired[
        list[
            Literal[
                "brand", "currency", "discountPercent", "listPriceText", "priceText"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `listPriceText` or `discountPercent`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a product that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sortBy: NotRequired[
        Literal["BEST_MATCH", "LOWEST_PRICE", "HIGHEST_PRICE", "TOP_RATED"]
    ]
    """Sort order for results (e.g. "LOWEST_PRICE"); defaults to relevance."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleShoppingSearchData(BaseModel):
    items: list[GoogleShoppingSearchItem] = Field(
        description="Matching Google Shopping product offers. Populated whenever the provider has data for the entity."
    )


class GoogleShoppingSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None, description="Product brand; empty when not reported."
    )
    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD"; empty when not reported.',
    )
    discount_percent: str | None = Field(
        default=None,
        alias="discountPercent",
        description='Discount label when on sale, e.g. "23% OFF"; empty otherwise.',
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    list_price: float | None = Field(
        default=None,
        alias="listPrice",
        description="Pre-discount list price as a numeric amount; 0 when not on sale or reported only as text.",
    )
    list_price_text: str | None = Field(
        default=None,
        alias="listPriceText",
        description='Pre-discount list price as displayed, e.g. "$130"; empty when not applicable.',
    )
    price: float | None = Field(
        default=None,
        description="Current price as a numeric amount; 0 when the lane reports price only as text (see priceText).",
    )
    price_text: str | None = Field(
        default=None,
        alias="priceText",
        description='Current price as displayed, e.g. "$99.99"; empty when the lane reports a numeric price instead.',
    )
    product_id: str | None = Field(
        default=None, alias="productId", description="Provider product identifier."
    )
    rating: float | None = Field(
        default=None, description="Average product rating, 0-5; null when unrated."
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of ratings / reviews; null when none reported.",
    )
    seller: str | None = Field(
        default=None,
        description='Store / seller name offering the product, e.g. "Target".',
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Google Shopping product page URL (query retained; it encodes the product identity). Populated whenever the provider has data for the entity."
    )


class GoogleShoppingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleShoppingSearchInput],
    ) -> RunResult[GoogleShoppingSearchData]:
        """Google Shopping Search

        Search Google Shopping by keyword and get up to 10 product offers (title,
        price, store, rating, and link), localized by country and language.

        Price: $0.016 per request.

        Example:
            res = client.google_shopping.search(limit=10, query="airpods")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_shopping.search", dict(input), options
        )
        return RunResult[GoogleShoppingSearchData].model_validate(raw)


class AsyncGoogleShoppingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleShoppingSearchInput],
    ) -> RunResult[GoogleShoppingSearchData]:
        """Google Shopping Search

        Search Google Shopping by keyword and get up to 10 product offers (title,
        price, store, rating, and link), localized by country and language.

        Price: $0.016 per request.

        Example:
            res = client.google_shopping.search(limit=10, query="airpods")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_shopping.search", dict(input), options
        )
        return RunResult[GoogleShoppingSearchData].model_validate(raw)
