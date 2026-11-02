# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the duckduckgo platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class DuckduckgoSearchInput(TypedDict, total=False):
    """Input for DuckDuckGo Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[
        Literal[
            "AR",
            "AU",
            "AT",
            "BE",
            "BR",
            "BG",
            "CA",
            "CL",
            "CN",
            "CO",
            "HR",
            "CZ",
            "DK",
            "EE",
            "FI",
            "FR",
            "DE",
            "GR",
            "HK",
            "HU",
            "IS",
            "IN",
            "ID",
            "IE",
            "IL",
            "IT",
            "JP",
            "KR",
            "LV",
            "LT",
            "MY",
            "MX",
            "NL",
            "NZ",
            "NO",
            "PK",
            "PE",
            "PH",
            "PL",
            "PT",
            "RO",
            "RU",
            "SA",
            "SG",
            "SK",
            "SI",
            "ZA",
            "ES",
            "SE",
            "CH",
            "TW",
            "TH",
            "TR",
            "US",
            "UA",
            "GB",
            "VN",
        ]
    ]
    """ISO-3166 alpha-2 country DuckDuckGo searches from, e.g. US, GB, DE: DuckDuckGo's region for that country in its main language (Belgium in Dutch, Canada and the US in English, Switzerland in German, Spain in Spanish). Only the countries DuckDuckGo offers are accepted; every country is served by most sources and US, GB and DE by all of them. Default: US."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of organic results to return (1-10, default 10). DuckDuckGo serves about 10 organic results per page, and some queries carry fewer. Range: 1 to 10. Default: 10."""
    page: NotRequired[int]
    """Which page of 10 results to return, starting at 1: page 2 returns results 11-20. Each page is billed as one request. Pages after the first are served only for country US, GB or DE, by the one source that continues each page exactly where the last ended. DuckDuckGo can repeat a result from the previous page, so deduplicate on url, and a limit below 10 drops the rest of that page. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The DuckDuckGo search query."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class DuckduckgoSearchData(BaseModel):
    items: list[DuckduckgoSearchItem] = Field(
        description="Organic results in DuckDuckGo's ranked order. Ads are not included. Populated whenever the provider has data for the entity."
    )
    query: str = Field(description="The query DuckDuckGo searched.")


class DuckduckgoSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display_url: str | None = Field(
        alias="displayUrl",
        description="The URL as DuckDuckGo displays it under the title, e.g. a host or a host and path. Its format differs by source. null when the source did not send one.",
    )
    domain: str | None = Field(
        description="Host of the result URL without a leading www., e.g. runnersworld.com."
    )
    position: int = Field(
        description="1-based rank of the result. On page 2 and later, some sources count from the top of page 1 and others from the top of the page returned. Populated whenever the provider has data for the entity."
    )
    snippet: str | None = Field(
        default=None,
        description="Text excerpt DuckDuckGo shows under the result. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Result title as DuckDuckGo shows it. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Destination URL of the result. Populated whenever the provider has data for the entity."
    )


class DuckduckgoNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DuckduckgoSearchInput],
    ) -> RunResult[DuckduckgoSearchData]:
        """DuckDuckGo Search

        Run a DuckDuckGo web search and get the ranked organic results (title, URL,
        snippet, position, display URL, domain) as clean JSON, ads left out. Returns
        up to 10 results per call; page deeper with page and pick the country
        DuckDuckGo searches from.

        Price: $0.00085 per request.

        Example:
            res = client.duckduckgo.search(country="US", limit=10, query="best running shoes")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "duckduckgo.search", dict(input), options
        )
        return RunResult[DuckduckgoSearchData].model_validate(raw)


class AsyncDuckduckgoNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DuckduckgoSearchInput],
    ) -> RunResult[DuckduckgoSearchData]:
        """DuckDuckGo Search

        Run a DuckDuckGo web search and get the ranked organic results (title, URL,
        snippet, position, display URL, domain) as clean JSON, ads left out. Returns
        up to 10 results per call; page deeper with page and pick the country
        DuckDuckGo searches from.

        Price: $0.00085 per request.

        Example:
            res = client.duckduckgo.search(country="US", limit=10, query="best running shoes")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "duckduckgo.search", dict(input), options
        )
        return RunResult[DuckduckgoSearchData].model_validate(raw)
