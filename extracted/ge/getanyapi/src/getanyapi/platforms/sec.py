# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the sec platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SecFilingsInput(TypedDict, total=False):
    """Input for SEC EDGAR Filings."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyName: NotRequired[str]
    """Company name to search for (partial match supported, e.g. 'Tesla' or 'Berkshire'). Use this when you do not have the ticker symbol. If both ticker and companyName are given, ticker takes precedence."""
    dateFrom: NotRequired[str]
    """Only return filings filed on or after this date, in YYYY-MM-DD format (e.g. 2025-01-01)."""
    dateTo: NotRequired[str]
    """Only return filings filed on or before this date, in YYYY-MM-DD format (e.g. 2026-06-01)."""
    form: NotRequired[str]
    """Filter filings by SEC form type (e.g. 10-K, 10-Q, 8-K, 4, DEF 14A, S-1, 13F-HR); omit for all forms."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of filings to return (1-25, default 25). You are billed per result returned, so a lower limit costs less. Range: 1 to 25."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    ticker: NotRequired[str]
    """Company stock ticker symbol, e.g. AAPL, MSFT, or TSLA. Provide either ticker or companyName; ticker is the more precise lookup."""


class SecFilingsData(BaseModel):
    items: list[SecFilingsItem] = Field(
        description="Filing records: company and CIK, form type, filing date, accession number, and document links. Populated whenever the provider has data for the entity."
    )


class SecFilingsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    accession_number: str = Field(
        alias="accessionNumber",
        description="SEC accession number uniquely identifying the filing. Populated whenever the provider has data for the entity.",
    )
    cik: str | None = Field(
        default=None,
        description="SEC Central Index Key for the filer. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Filer company name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None, description="Primary document description, e.g. the form label."
    )
    filed_utc: float | None = Field(
        default=None,
        alias="filedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Date the filing was filed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    filing_url: str | None = Field(
        default=None,
        alias="filingUrl",
        description="Link to the filing index/folder on sec.gov.",
    )
    fiscal_year_end: str | None = Field(
        default=None,
        alias="fiscalYearEnd",
        description="Fiscal year end as MMDD, e.g. 0926.",
    )
    form: str | None = Field(
        default=None,
        description="SEC form type, e.g. 10-K, 10-Q, 8-K. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reported_utc: float | None = Field(
        default=None,
        alias="reportedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Period-of-report date for the filing.",
    )
    sic: str | None = Field(
        default=None, description="SIC industry code SEC files the company under."
    )
    ticker: str | None = Field(
        default=None, description="Stock ticker symbol of the filer, when known."
    )
    url: str = Field(
        description="Direct link to the primary filing document on sec.gov. Populated whenever the provider has data for the entity."
    )


class SecNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def filings(
        self, *, options: RequestOptions | None = None, **input: Unpack[SecFilingsInput]
    ) -> RunResult[SecFilingsData]:
        """SEC EDGAR Filings

        List a public company's SEC EDGAR filings - form type, filing date,
        accession number, and document links - by ticker, company name, or CIK, with
        optional form-type and date filters.

        Price: $0.0022 per request plus $0.00044 per result (maximum $0.0132).

        Example:
            res = client.sec.filings(limit=3, ticker="AAPL")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "sec.filings", dict(input), options
        )
        return RunResult[SecFilingsData].model_validate(raw)


class AsyncSecNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def filings(
        self, *, options: RequestOptions | None = None, **input: Unpack[SecFilingsInput]
    ) -> RunResult[SecFilingsData]:
        """SEC EDGAR Filings

        List a public company's SEC EDGAR filings - form type, filing date,
        accession number, and document links - by ticker, company name, or CIK, with
        optional form-type and date filters.

        Price: $0.0022 per request plus $0.00044 per result (maximum $0.0132).

        Example:
            res = client.sec.filings(limit=3, ticker="AAPL")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "sec.filings", dict(input), options
        )
        return RunResult[SecFilingsData].model_validate(raw)
