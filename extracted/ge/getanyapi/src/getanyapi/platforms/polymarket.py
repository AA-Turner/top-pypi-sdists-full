# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the polymarket platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class PolymarketMarketsInput(TypedDict, total=False):
    """Input for Polymarket Markets."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (10-25, default 25). You are billed per result returned, so a lower limit costs less. Range: 10 to 25."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search term for markets (e.g. election, bitcoin, super bowl)."""
    sortBy: NotRequired[
        Literal[
            "volume_24hr",
            "volume",
            "liquidity",
            "start_date",
            "ending_soon",
            "competitive",
        ]
    ]
    """How discovered markets are ordered before results are returned (e.g. volume_24hr for recent momentum). Default: volume_24hr."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    status: NotRequired[Literal["active", "resolved"]]
    """Return "active" markets for current prices and volume, or "resolved" markets for historical outcomes. Default: active."""


class PolymarketMarketsData(BaseModel):
    items: list[PolymarketMarketsItem] = Field(
        description="Prediction-market records: market question, outcomes with current prices, volume, liquidity, and end date. Populated whenever the provider has data for the entity."
    )


class PolymarketMarketsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    best_ask: float | None = Field(
        default=None,
        alias="bestAsk",
        description="Best ask currently on the order book (0 to 1).",
    )
    best_bid: float | None = Field(
        default=None,
        alias="bestBid",
        description="Best bid currently on the order book (0 to 1).",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Number of comments on the event.",
    )
    condition_id: str | None = Field(
        default=None,
        alias="conditionId",
        description="On-chain condition identifier for the market.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the market was created.",
    )
    description: str | None = Field(
        default=None, description="Resolution rules for the market."
    )
    ends_utc: float | None = Field(
        default=None,
        alias="endsUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the market resolves/ends.",
    )
    event_id: str | None = Field(
        default=None,
        alias="eventId",
        description="Identifier of the parent event grouping this market.",
    )
    event_title: str | None = Field(
        default=None,
        alias="eventTitle",
        description="Title of the parent event grouping this market.",
    )
    id: str = Field(
        description="Polymarket market identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="Event image URL.")
    last_trade_price: float | None = Field(
        default=None,
        alias="lastTradePrice",
        description="Price of the most recent trade (0 to 1).",
    )
    liquidity_usd: float | None = Field(
        default=None, alias="liquidityUsd", description="Available liquidity in USD."
    )
    open_interest_usd: float | None = Field(
        default=None, alias="openInterestUsd", description="Open interest in USD."
    )
    outcomes: list[PolymarketMarketsOutcome] | None = Field(
        default=None, description="Market outcomes with their current implied prices."
    )
    slug: str | None = Field(default=None, description="URL slug of the market.")
    spread: float | None = Field(
        default=None, description="Difference between the best ask and the best bid."
    )
    starts_utc: float | None = Field(
        default=None,
        alias="startsUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When trading opened.",
    )
    status: str | None = Field(
        default=None, description="Market status, e.g. active or closed."
    )
    tags: list[PolymarketMarketsTag] | None = Field(
        default=None, description="Polymarket topic tags for the event."
    )
    title: str = Field(
        description="The market question. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the market was last updated.",
    )
    url: str = Field(
        description="Polymarket URL for the market event. Populated whenever the provider has data for the entity."
    )
    volume1m_usd: float | None = Field(
        default=None,
        alias="volume1mUsd",
        description="Traded volume in USD over the past month.",
    )
    volume1w_usd: float | None = Field(
        default=None,
        alias="volume1wUsd",
        description="Traded volume in USD over the past week.",
    )
    volume24h_usd: float | None = Field(
        default=None,
        alias="volume24hUsd",
        description="Traded volume in USD over the past 24 hours.",
    )
    volume_usd: float | None = Field(
        default=None, alias="volumeUsd", description="Total traded volume in USD."
    )


class PolymarketMarketsOutcome(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(default=None, description="Outcome label, e.g. Yes or No.")
    price: float | None = Field(
        default=None,
        description="Current implied probability price for the outcome (0 to 1).",
    )


class PolymarketMarketsTag(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(default=None, description="Tag label, e.g. Politics.")
    slug: str | None = Field(default=None, description="Tag slug.")


class PolymarketNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def markets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PolymarketMarketsInput],
    ) -> RunResult[PolymarketMarketsData]:
        """Polymarket Markets

        Discover Polymarket prediction markets (question, outcome prices, volume,
        liquidity, and end dates) by keyword or sorted by activity, as normalized
        JSON.

        Price: $0.116 per request plus $0.00066 per result (maximum $0.132).

        Example:
            res = client.polymarket.markets(limit=10, query="election")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "polymarket.markets", dict(input), options
        )
        return RunResult[PolymarketMarketsData].model_validate(raw)


class AsyncPolymarketNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def markets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PolymarketMarketsInput],
    ) -> RunResult[PolymarketMarketsData]:
        """Polymarket Markets

        Discover Polymarket prediction markets (question, outcome prices, volume,
        liquidity, and end dates) by keyword or sorted by activity, as normalized
        JSON.

        Price: $0.116 per request plus $0.00066 per result (maximum $0.132).

        Example:
            res = client.polymarket.markets(limit=10, query="election")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "polymarket.markets", dict(input), options
        )
        return RunResult[PolymarketMarketsData].model_validate(raw)
