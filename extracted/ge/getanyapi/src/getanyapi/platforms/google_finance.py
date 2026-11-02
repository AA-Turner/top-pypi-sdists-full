# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the google_finance platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GoogleFinanceQuoteInput(TypedDict, total=False):
    """Input for Google Finance Quote."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    symbol: Required[str]
    """The symbol to quote. US stocks use a plain ticker (e.g. AAPL, TSLA); non-US stocks add a market suffix (e.g. VOW3.DE, BABA.HK, BARC.L); indices use a caret (e.g. ^GSPC, ^DJI); crypto and currencies use pair form (e.g. BTC-USD, EURUSD=X); mutual funds and futures use their symbol (e.g. VFIAX, ES=F). Common alternate forms are accepted and normalized (e.g. AAPL:NASDAQ, .DJI, BTC/USD). Exact symbols only, not a company-name search."""


class GoogleFinanceQuoteData(BaseModel):
    items: list[GoogleFinanceQuoteItem] = Field(
        description="The quote for the requested symbol: name, current price, day change (absolute and percent), quote currency, exchange and market state, plus intraday and reference figures. Up to one element (empty when the symbol did not resolve). Populated whenever the provider has data for the entity."
    )


class GoogleFinanceQuoteItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    as_of_utc: float | None = Field(
        default=None,
        alias="asOfUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    ask: float | None = Field(default=None, description="Current ask price.")
    asset_type: str | None = Field(
        default=None,
        alias="assetType",
        description="Instrument class (e.g. EQUITY, ETF, CRYPTOCURRENCY, CURRENCY, INDEX, MUTUALFUND, FUTURE).",
    )
    average_volume: float | None = Field(
        default=None, alias="averageVolume", description="Average daily trading volume."
    )
    bid: float | None = Field(default=None, description="Current bid price.")
    change: float | None = Field(
        default=None,
        description="Absolute price change on the day, in the quote currency.",
    )
    change_percent: float | None = Field(
        default=None,
        alias="changePercent",
        description="Percent price change on the day.",
    )
    currency: str | None = Field(
        default=None,
        description="ISO currency the quote is priced in (e.g. USD). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    day_high: float | None = Field(
        default=None,
        alias="dayHigh",
        description="Highest price so far in the current session.",
    )
    day_low: float | None = Field(
        default=None,
        alias="dayLow",
        description="Lowest price so far in the current session.",
    )
    exchange: str | None = Field(
        default=None,
        description="Exchange the instrument trades on (e.g. NasdaqGS). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    fifty_two_week_high: float | None = Field(
        default=None,
        alias="fiftyTwoWeekHigh",
        description="Highest price over the trailing 52 weeks.",
    )
    fifty_two_week_low: float | None = Field(
        default=None,
        alias="fiftyTwoWeekLow",
        description="Lowest price over the trailing 52 weeks.",
    )
    market_cap: float | None = Field(
        default=None,
        alias="marketCap",
        description="Market capitalization in the quote currency.",
    )
    market_state: str | None = Field(
        default=None,
        alias="marketState",
        description="Current market state (e.g. REGULAR, PRE, POST, CLOSED).",
    )
    name: str | None = Field(
        default=None,
        description="Instrument or company name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    open: float | None = Field(
        default=None, description="Opening price for the current session."
    )
    previous_close: float | None = Field(
        default=None, alias="previousClose", description="Previous session close price."
    )
    price: float = Field(description="Current price in the quote currency.")
    symbol: str = Field(
        description="Resolved ticker symbol for the quote. Populated whenever the provider has data for the entity."
    )
    volume: float | None = Field(
        default=None, description="Traded volume for the current session."
    )


class GoogleFinanceNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def quote(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleFinanceQuoteInput],
    ) -> RunResult[GoogleFinanceQuoteData]:
        """Google Finance Quote

        Fetch a live quote for any stock, index, ETF, mutual fund, currency pair, or
        crypto symbol: name, current price, the absolute and percent change on the
        day, quote currency, exchange and market state, plus intraday and reference
        figures (open, day high/low, previous close, volume, market cap, and the
        52-week range).

        Price: $0.00055 per request plus $0.00165 per result (maximum $0.0022).

        Example:
            res = client.google_finance.quote(symbol="AAPL:NASDAQ")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_finance.quote", dict(input), options
        )
        return RunResult[GoogleFinanceQuoteData].model_validate(raw)


class AsyncGoogleFinanceNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def quote(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleFinanceQuoteInput],
    ) -> RunResult[GoogleFinanceQuoteData]:
        """Google Finance Quote

        Fetch a live quote for any stock, index, ETF, mutual fund, currency pair, or
        crypto symbol: name, current price, the absolute and percent change on the
        day, quote currency, exchange and market state, plus intraday and reference
        figures (open, day high/low, previous close, volume, market cap, and the
        52-week range).

        Price: $0.00055 per request plus $0.00165 per result (maximum $0.0022).

        Example:
            res = client.google_finance.quote(symbol="AAPL:NASDAQ")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_finance.quote", dict(input), options
        )
        return RunResult[GoogleFinanceQuoteData].model_validate(raw)
