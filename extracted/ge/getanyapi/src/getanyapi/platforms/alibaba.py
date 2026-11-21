# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the alibaba platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class AlibabaSearchInput(TypedDict, total=False):
    """Input for Alibaba Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-25, default 25). You are billed per result returned, so a lower limit costs less. Range: 1 to 25."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keywords to search for on Alibaba (e.g. "bluetooth speaker wholesale")."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AlibabaSearchData(BaseModel):
    items: list[AlibabaSearchItem] = Field(
        description="Matching Alibaba wholesale listings. Populated whenever the provider has data for the entity."
    )


class AlibabaSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Alibaba supplier company identifier.",
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description='Supplier country ISO code, e.g. "CN".',
    )
    currency: str | None = Field(
        default=None, description='Price currency symbol or code, e.g. "$".'
    )
    image: str | None = Field(default=None, description="Primary product image URL.")
    images: list[str] | None = Field(default=None, description="Product image URLs.")
    is_sponsored: bool | None = Field(
        default=None,
        alias="isSponsored",
        description="True when the listing is a paid placement.",
    )
    moq: str | None = Field(
        default=None,
        description='Minimum order quantity text, e.g. "Min. order: 1 piece".',
    )
    price: float | None = Field(
        default=None,
        description="Lowest price in the displayed range, as a numeric amount; 0 when Alibaba shows no price.",
    )
    price_text: str | None = Field(
        default=None,
        alias="priceText",
        description='Price or price range as displayed, e.g. "$40.80-45.80" (Alibaba lists ranges, not a single numeric value).',
    )
    product_id: str | None = Field(
        default=None, alias="productId", description="Alibaba product identifier."
    )
    promotion_price: str | None = Field(
        default=None,
        alias="promotionPrice",
        description="Discounted promotional price when the listing is on sale; empty otherwise.",
    )
    rating: float | None = Field(
        default=None,
        description="Average buyer review score, 0-5; null when Alibaba shows no review score for the supplier.",
    )
    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        description="Number of buyer reviews; null when Alibaba shows no review count for the supplier.",
    )
    supplier_name: str | None = Field(
        default=None, alias="supplierName", description="Supplier / company name."
    )
    supplier_url: str | None = Field(
        default=None,
        alias="supplierUrl",
        description="Supplier storefront URL on Alibaba.",
    )
    supplier_years: str | None = Field(
        default=None,
        alias="supplierYears",
        description='Gold Supplier tenure text, e.g. "3 yrs"; empty when not a Gold Supplier.',
    )
    title: str = Field(
        description="Listing title as shown on Alibaba (may contain the supplier's inline markup). Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical product detail page URL (tracking query params stripped). Populated whenever the provider has data for the entity."
    )


class AlibabaNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AlibabaSearchInput],
    ) -> RunResult[AlibabaSearchData]:
        """Alibaba Search

        Search Alibaba by keyword and get up to 25 wholesale listings (title, price
        range, minimum order, and supplier) in one normalized response.

        Price: $0 per request plus $0.00084 per result (maximum $0.021).

        Example:
            res = client.alibaba.search(limit=3, query="bluetooth speaker")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "alibaba.search", dict(input), options
        )
        return RunResult[AlibabaSearchData].model_validate(raw)


class AsyncAlibabaNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AlibabaSearchInput],
    ) -> RunResult[AlibabaSearchData]:
        """Alibaba Search

        Search Alibaba by keyword and get up to 25 wholesale listings (title, price
        range, minimum order, and supplier) in one normalized response.

        Price: $0 per request plus $0.00084 per result (maximum $0.021).

        Example:
            res = client.alibaba.search(limit=3, query="bluetooth speaker")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "alibaba.search", dict(input), options
        )
        return RunResult[AlibabaSearchData].model_validate(raw)
