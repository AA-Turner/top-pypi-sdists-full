# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the yelp platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class YelpSearchInput(TypedDict, total=False):
    """Input for Yelp Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1 to 20, default 20). Range: 1 to 20. Default: 20."""
    location: Required[str]
    """City and state defining the search area (e.g. San Francisco, CA)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search term or category to look for (e.g. sushi)."""
    requireFields: NotRequired[
        list[
            Literal[
                "address2",
                "address3",
                "dialable_phone",
                "is_closed",
                "localized_phone",
                "photo_count",
                "price",
                "unrounded_avg_rating",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `is_closed` or `price`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a place that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class YelpSearchData(BaseModel):
    items: list[YelpSearchItem] = Field(
        description="Business listing records: name, categories, rating, review count, address, and core business info. Populated whenever the provider has data for the entity."
    )


class YelpSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    address1: str | None = Field(
        default=None, description="Primary street address line."
    )
    address2: str | None = Field(default=None, description="Secondary address line.")
    address3: str | None = Field(default=None, description="Tertiary address line.")
    alias: str = Field(
        description="URL slug for the business. Populated whenever the provider has data for the entity."
    )
    avg_rating: float | None = Field(
        default=None, description="Rounded average star rating."
    )
    categories: list[YelpSearchCategorie] | None = Field(
        default=None, description="Business category tags."
    )
    city: str | None = Field(default=None, description="City name.")
    country: str | None = Field(default=None, description="ISO country code.")
    dialable_phone: str | None = Field(
        default=None, description="Dialable phone number."
    )
    id: str = Field(
        description="Stable Yelp business identifier. Populated whenever the provider has data for the entity."
    )
    is_closed: bool | None = Field(
        default=None, description="Whether the business is permanently closed."
    )
    latitude: float | None = Field(
        default=None, description="Latitude of the business."
    )
    localized_phone: str | None = Field(
        default=None, description="Formatted local phone number."
    )
    localized_price: str | None = Field(
        default=None, description="Localized price tier (e.g. $$)."
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the business."
    )
    name: str = Field(
        description="Business display name. Populated whenever the provider has data for the entity."
    )
    neighborhoods: list[str] | None = Field(
        default=None, description="Neighborhood labels for the location."
    )
    phone: str | None = Field(default=None, description="Raw phone number.")
    photo_count: int | None = Field(default=None, description="Total photo count.")
    photo_url: str | None = Field(
        default=None,
        description="Primary photo URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    price: int | None = Field(default=None, description="Numeric price tier.")
    review_count: int | None = Field(default=None, description="Number of reviews.")
    state: str | None = Field(default=None, description="State or region code.")
    unrounded_avg_rating: float | None = Field(
        default=None, description="Unrounded average star rating."
    )
    url: str | None = Field(default=None, description="Public Yelp business page URL.")
    zip: str | None = Field(default=None, description="Postal code.")


class YelpSearchCategorie(BaseModel):
    model_config = ConfigDict(extra="allow")


class YelpNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[YelpSearchInput]
    ) -> RunResult[YelpSearchData]:
        """Yelp Search

        Search Yelp for businesses by keyword and location: up to 20 listings with
        ratings, categories, and core business info per request.

        Price: $0.0035 per request.

        Example:
            res = client.yelp.search(limit=20, location="Chicago, IL", query="pizza")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "yelp.search", dict(input), options
        )
        return RunResult[YelpSearchData].model_validate(raw)


class AsyncYelpNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[YelpSearchInput]
    ) -> RunResult[YelpSearchData]:
        """Yelp Search

        Search Yelp for businesses by keyword and location: up to 20 listings with
        ratings, categories, and core business info per request.

        Price: $0.0035 per request.

        Example:
            res = client.yelp.search(limit=20, location="Chicago, IL", query="pizza")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "yelp.search", dict(input), options
        )
        return RunResult[YelpSearchData].model_validate(raw)
