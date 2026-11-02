# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the ikea platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class IkeaSearchInput(TypedDict, total=False):
    """Input for IKEA Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based results page of 24 products. Each page is billed as one request. Range: 1 to 100. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, e.g. "bookshelf" or "desk"."""
    requireFields: NotRequired[list[Literal["memberOffer"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `memberOffer`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class IkeaSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[IkeaSearchItem] = Field(
        description="Matching IKEA US product records for the requested page. Populated whenever the provider has data for the entity."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total number of matching products IKEA reports for the query, or null when not reported.",
    )


class IkeaSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None,
        description='Price currency code, e.g. "USD", or null when no price is shown.',
    )
    dimensions: str | None = Field(
        default=None,
        description='Product dimensions as IKEA lists them, e.g. "31 1/2x11x79 1/2" (inches on the US store), or null when not listed.',
    )
    image: str | None = Field(
        default=None,
        description="Primary product image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    member_offer: str | None = Field(
        default=None,
        alias="memberOffer",
        description='IKEA Family member offer shown on the product, e.g. "In-store only price $65.00", or null when there is none or the serving source does not report it.',
    )
    position: int | None = Field(
        default=None, description="1-based position of the result in this page."
    )
    price: float | None = Field(
        default=None,
        description="Current online price in USD, or null when the result shows no price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    product_id: str = Field(
        alias="productId",
        description="IKEA product id: the 8-digit article number, or an s-prefixed id for a combination. Populated whenever the provider has data for the entity.",
    )
    rating: float | None = Field(
        default=None,
        description="Average customer rating, 0-5, or null when the product is unrated.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of customer ratings, or null when the product has none.",
    )
    title: str = Field(
        description='Product name and type as IKEA lists it, e.g. "BILLY Bookcase white". Populated whenever the provider has data for the entity.'
    )
    url: str | None = Field(
        default=None,
        description="IKEA product page URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class IkeaNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[IkeaSearchInput]
    ) -> RunResult[IkeaSearchData]:
        """IKEA Search

        Search IKEA's US store by keyword and get title, price, rating, and image
        for each product in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.ikea.search(query="bookshelf")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ikea.search", dict(input), options
        )
        return RunResult[IkeaSearchData].model_validate(raw)


class AsyncIkeaNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[IkeaSearchInput]
    ) -> RunResult[IkeaSearchData]:
        """IKEA Search

        Search IKEA's US store by keyword and get title, price, rating, and image
        for each product in one normalized response.

        Price: $0.00085 per request.

        Example:
            res = client.ikea.search(query="bookshelf")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ikea.search", dict(input), options
        )
        return RunResult[IkeaSearchData].model_validate(raw)
