# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the coinmarketcap platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class CoinmarketcapListingsInput(TypedDict, total=False):
    """Input for CoinMarketCap Listings."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-25, default 25). You are billed per result returned, so a lower limit costs less. Range: 1 to 25."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CoinmarketcapListingsData(BaseModel):
    items: list[CoinmarketcapListingsItem] = Field(
        description="Cryptocurrency listing records: rank, name, symbol, price, market cap, trading volume, and 24h price change. Populated whenever the provider has data for the entity."
    )


class CoinmarketcapListingsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active: bool | None = Field(
        default=None,
        description="Whether CoinMarketCap still tracks the coin as active.",
    )
    ath: float | None = Field(default=None, description="All-time high price in USD.")
    atl: float | None = Field(default=None, description="All-time low price in USD.")
    circulating_supply: float | None = Field(
        default=None,
        alias="circulatingSupply",
        description="Circulating supply (coin count).",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="When CoinMarketCap first listed the coin. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    dominance: float | None = Field(
        default=None,
        description="Share of total crypto market capitalization, in percent.",
    )
    fully_diluted_market_cap: float | None = Field(
        default=None,
        alias="fullyDilutedMarketCap",
        description="Fully diluted market capitalization in USD (total supply at the current price).",
    )
    high24h: float | None = Field(default=None, description="24h high price in USD.")
    id: str = Field(
        description="CoinMarketCap identifier. Populated whenever the provider has data for the entity."
    )
    last_updated: str | None = Field(
        default=None,
        alias="lastUpdated",
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    low24h: float | None = Field(default=None, description="24h low price in USD.")
    market_cap: float | None = Field(
        default=None, alias="marketCap", description="Market capitalization in USD."
    )
    market_pair_count: int | None = Field(
        default=None,
        alias="marketPairCount",
        description="Number of exchange market pairs trading this coin.",
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    percent_change1h: float | None = Field(
        default=None,
        alias="percentChange1h",
        description="Price change over the last hour, in percent.",
    )
    percent_change1y: float | None = Field(
        default=None,
        alias="percentChange1y",
        description="Price change over the last year, in percent.",
    )
    percent_change24h: float | None = Field(
        default=None,
        alias="percentChange24h",
        description="Price change over the last 24 hours, in percent.",
    )
    percent_change30d: float | None = Field(
        default=None,
        alias="percentChange30d",
        description="Price change over the last 30 days, in percent.",
    )
    percent_change60d: float | None = Field(
        default=None,
        alias="percentChange60d",
        description="Price change over the last 60 days, in percent.",
    )
    percent_change7d: float | None = Field(
        default=None,
        alias="percentChange7d",
        description="Price change over the last 7 days, in percent.",
    )
    percent_change90d: float | None = Field(
        default=None,
        alias="percentChange90d",
        description="Price change over the last 90 days, in percent.",
    )
    percent_change_ytd: float | None = Field(
        default=None,
        alias="percentChangeYtd",
        description="Price change year to date, in percent.",
    )
    price: float | None = Field(default=None, description="Latest price in USD.")
    self_reported_circulating_supply: float | None = Field(
        default=None,
        alias="selfReportedCirculatingSupply",
        description="Circulating supply as reported by the project itself (coin count).",
    )
    slug: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    symbol: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    total_supply: float | None = Field(
        default=None, alias="totalSupply", description="Total supply (coin count)."
    )
    turnover: float | None = Field(
        default=None, description="24h trading volume divided by market capitalization."
    )
    volume24h: float | None = Field(
        default=None, description="24h trading volume in USD."
    )
    volume30d: float | None = Field(
        default=None, description="30-day trading volume in USD."
    )
    volume7d: float | None = Field(
        default=None, description="7-day trading volume in USD."
    )


class CoinmarketcapNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CoinmarketcapListingsInput],
    ) -> RunResult[CoinmarketcapListingsData]:
        """CoinMarketCap Listings

        Get the current top cryptocurrencies from CoinMarketCap (rank, price, market
        cap, volume, and 24h change) as normalized JSON.

        Price: $0 per request plus $0.00216 per result (maximum $0.054).

        Example:
            res = client.coinmarketcap.listings(limit=5)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "coinmarketcap.listings", dict(input), options
        )
        return RunResult[CoinmarketcapListingsData].model_validate(raw)


class AsyncCoinmarketcapNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def listings(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CoinmarketcapListingsInput],
    ) -> RunResult[CoinmarketcapListingsData]:
        """CoinMarketCap Listings

        Get the current top cryptocurrencies from CoinMarketCap (rank, price, market
        cap, volume, and 24h change) as normalized JSON.

        Price: $0 per request plus $0.00216 per result (maximum $0.054).

        Example:
            res = client.coinmarketcap.listings(limit=5)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "coinmarketcap.listings", dict(input), options
        )
        return RunResult[CoinmarketcapListingsData].model_validate(raw)
