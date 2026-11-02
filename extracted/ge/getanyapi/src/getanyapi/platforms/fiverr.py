# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the fiverr platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class FiverrSearchInput(TypedDict, total=False):
    """Input for Fiverr Gig Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). You are billed per result returned, so a lower limit costs less. Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Fiverr search or category page URL to extract gigs from."""


class FiverrSearchData(BaseModel):
    items: list[FiverrSearchItem] = Field(
        description="Gig records from the search or category URL. Operators may return additional fields beyond those documented here. Populated whenever the provider has data for the entity."
    )


class FiverrSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category_id: str | None = Field(
        default=None,
        alias="categoryId",
        description="Fiverr's numeric top-level category id for the gig, as a string.",
    )
    duration: int | None = Field(default=None, description="Delivery time in days.")
    gig_id: str = Field(
        alias="gigId",
        description="Stable Fiverr gig identifier. Populated whenever the provider has data for the entity.",
    )
    gig_url: str = Field(
        alias="gigUrl",
        description="Canonical Fiverr URL for the gig. Populated whenever the provider has data for the entity.",
    )
    image: str | None = Field(default=None, description="Primary gig thumbnail URL.")
    price: float | None = Field(default=None, description="Starting price in USD.")
    seller_country: str | None = Field(
        default=None, alias="sellerCountry", description="Seller country code."
    )
    seller_display_name: str | None = Field(
        default=None, alias="sellerDisplayName", description="Seller display name."
    )
    seller_level: str | None = Field(
        default=None, alias="sellerLevel", description="Fiverr seller level."
    )
    seller_name: str | None = Field(
        default=None, alias="sellerName", description="Seller username."
    )
    seller_rating_count: int | None = Field(
        default=None, alias="sellerRatingCount", description="Number of seller ratings."
    )
    seller_rating_score: float | None = Field(
        default=None, alias="sellerRatingScore", description="Average seller rating."
    )
    seller_url: str | None = Field(
        default=None, alias="sellerUrl", description="Seller profile URL."
    )
    title: str = Field(
        description="Gig headline. Populated whenever the provider has data for the entity."
    )


class FiverrNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FiverrSearchInput],
    ) -> RunResult[FiverrSearchData]:
        """Fiverr Gig Search

        Extract Fiverr gig listings from any search or category URL: titles,
        sellers, ratings, and pricing as structured JSON.

        Price: $0 per request plus $0.00165 per result (maximum $0.033).

        Example:
            res = client.fiverr.search(limit=3, url="https://www.fiverr.com/search/gigs?query=logo%20design")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "fiverr.search", dict(input), options
        )
        return RunResult[FiverrSearchData].model_validate(raw)


class AsyncFiverrNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FiverrSearchInput],
    ) -> RunResult[FiverrSearchData]:
        """Fiverr Gig Search

        Extract Fiverr gig listings from any search or category URL: titles,
        sellers, ratings, and pricing as structured JSON.

        Price: $0 per request plus $0.00165 per result (maximum $0.033).

        Example:
            res = client.fiverr.search(limit=3, url="https://www.fiverr.com/search/gigs?query=logo%20design")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "fiverr.search", dict(input), options
        )
        return RunResult[FiverrSearchData].model_validate(raw)
