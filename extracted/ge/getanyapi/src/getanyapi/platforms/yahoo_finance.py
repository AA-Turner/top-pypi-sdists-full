# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the yahoo_finance platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class YahooFinanceQuoteInput(TypedDict, total=False):
    """Input for Yahoo Finance Quote."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    ticker: Required[str]
    """The ticker symbol to look up."""


class YahooFinanceQuoteData(BaseModel):
    items: list[YahooFinanceQuoteItem] = Field(
        description="Quote records for the ticker: current price, day range, volume, and market cap. Populated whenever the provider has data for the entity."
    )


class YahooFinanceQuoteItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    as_of_utc: float | None = Field(
        default=None,
        alias="asOfUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    asset_type: str | None = Field(
        default=None,
        alias="assetType",
        description="Instrument type Yahoo classifies the symbol as (e.g. EQUITY, ETF).",
    )
    change: float | None = Field(
        default=None, description="Absolute price change from the previous close."
    )
    change_percent: float | None = Field(
        default=None,
        alias="changePercent",
        description="Percent price change from the previous close (e.g. 3.14 means +3.14%).",
    )
    day_high: float | None = Field(
        default=None,
        alias="dayHigh",
        description="Highest trade price during the current session.",
    )
    day_low: float | None = Field(
        default=None,
        alias="dayLow",
        description="Lowest trade price during the current session.",
    )
    industry: str | None = Field(
        default=None, description="Industry the issuer belongs to."
    )
    market_cap: int | None = Field(
        default=None,
        alias="marketCap",
        description="Total market capitalization in the security's native currency.",
    )
    name: str | None = Field(
        default=None,
        description='The security\'s display name, e.g. "Apple Inc.". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    previous_close: float | None = Field(
        default=None,
        alias="previousClose",
        description="The previous session's closing price.",
    )
    price: float = Field(
        description="The latest trade price in the security's native currency. Populated whenever the provider has data for the entity."
    )
    sector: str | None = Field(
        default=None, description="Sector the issuer belongs to."
    )
    symbol: str | None = Field(
        default=None,
        description='The resolved ticker symbol for the quote, e.g. "AAPL". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    volume: int | None = Field(
        default=None, description="Number of shares traded during the current session."
    )


class YahooFinanceNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def quote(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[YahooFinanceQuoteInput],
    ) -> RunResult[YahooFinanceQuoteData]:
        """Yahoo Finance Quote

        Look up a stock or ETF by ticker symbol and get its Yahoo Finance quote
        (price, market cap, volume, and key stats) as normalized JSON.

        Price: $0.00006 per request plus $0.00108 per result (maximum $0.00114).

        Example:
            res = client.yahoo_finance.quote(ticker="AAPL")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "yahoo_finance.quote", dict(input), options
        )
        return RunResult[YahooFinanceQuoteData].model_validate(raw)


class AsyncYahooFinanceNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def quote(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[YahooFinanceQuoteInput],
    ) -> RunResult[YahooFinanceQuoteData]:
        """Yahoo Finance Quote

        Look up a stock or ETF by ticker symbol and get its Yahoo Finance quote
        (price, market cap, volume, and key stats) as normalized JSON.

        Price: $0.00006 per request plus $0.00108 per result (maximum $0.00114).

        Example:
            res = client.yahoo_finance.quote(ticker="AAPL")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "yahoo_finance.quote", dict(input), options
        )
        return RunResult[YahooFinanceQuoteData].model_validate(raw)
