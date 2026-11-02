# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the brave platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class BraveSearchInput(TypedDict, total=False):
    """Input for Brave Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[
        Literal[
            "AR",
            "AU",
            "AT",
            "BE",
            "BR",
            "CA",
            "CL",
            "CN",
            "DK",
            "FI",
            "FR",
            "DE",
            "GR",
            "HK",
            "IN",
            "ID",
            "IT",
            "JP",
            "KR",
            "MY",
            "MX",
            "NL",
            "NZ",
            "NO",
            "PL",
            "PT",
            "PH",
            "RU",
            "SA",
            "SG",
            "ZA",
            "ES",
            "SE",
            "CH",
            "TW",
            "TR",
            "GB",
            "US",
        ]
    ]
    """ISO-3166 alpha-2 country Brave searches from, e.g. US, GB, DE. Brave ranks and localizes results for that country. Only the countries Brave offers are accepted; US is served by every source and the others by the sources that can target them. Default: US."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of organic results to return (1-20, default 20). Brave serves about 20 organic results per page, and some queries carry fewer. Range: 1 to 20. Default: 20."""
    page: NotRequired[int]
    """Which page of Brave results to return, starting at 1 (up to 10); a page holds about 20 results. Each page is billed as one request. Pages after the first are served only for country US, by the one source that continues each page exactly where the last ended. A limit below the page size drops the rest of that page, so keep the default limit to walk every result. Range: 1 to 10. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The Brave search query."""
    requireFields: NotRequired[
        list[
            Literal[
                "durationSeconds",
                "image",
                "publishedUtc",
                "relatedSearches",
                "source",
                "videos",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `relatedSearches` or `publishedUtc`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class BraveSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[BraveSearchItem] = Field(
        description="Organic results in Brave's ranked order. Ads are not included. Populated whenever the provider has data for the entity."
    )
    query: str = Field(description="The query Brave searched.")
    related_searches: list[str] | None = Field(
        default=None,
        alias="relatedSearches",
        description="Brave's related searches for the query. An empty array means Brave showed none; null means the source that answered cannot report them.",
    )
    videos: list[BraveSearchVideo] | None = Field(
        default=None,
        description="Video results Brave shows for the query. An empty array means Brave showed none; null means the source that answered cannot report them.",
    )


class BraveSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display_url: str | None = Field(
        alias="displayUrl",
        description="The URL as Brave displays it under the title, e.g. a host or a breadcrumb path. Its format differs by source. null when the source did not send one.",
    )
    domain: str | None = Field(
        description="Host of the result URL without a leading www., e.g. runnersworld.com."
    )
    position: int = Field(
        description="1-based rank of the result. On page 2 and later, some sources count from the top of page 1 and others from the top of the page returned. Populated whenever the provider has data for the entity."
    )
    published_utc: int | None = Field(
        default=None,
        alias="publishedUtc",
        description="Page date Brave shows for the result. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. null when Brave shows no date or the source that answered cannot report it.",
    )
    snippet: str | None = Field(
        default=None,
        description="Text excerpt Brave shows under the result, often led by the page date. Absent on the results where Brave shows none. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Result title as Brave shows it. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Destination URL of the result. Populated whenever the provider has data for the entity."
    )


class BraveSearchVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    duration_seconds: int | None = Field(
        default=None,
        alias="durationSeconds",
        description="Video length in seconds; null when Brave shows none.",
    )
    image: str | None = Field(default=None, description="Thumbnail image URL.")
    published_utc: int | None = Field(
        default=None,
        alias="publishedUtc",
        description="Date Brave shows for the video. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. null when Brave shows no date.",
    )
    source: str | None = Field(
        default=None, description="Site hosting the video, e.g. YouTube."
    )
    title: str | None = Field(
        default=None, description="Video title as Brave shows it."
    )
    url: str = Field(description="URL of the video page.")


class BraveNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BraveSearchInput],
    ) -> RunResult[BraveSearchData]:
        """Brave Search

        Run a Brave web search and get the ranked organic results (title, URL,
        snippet, position, display URL, domain) as clean JSON. Brave answers from
        its own independent index. Returns up to 20 results per call, with related
        searches and video results where the source has them; page deeper with page
        and pick the country Brave searches from.

        Price: $0.00085 per request.

        Example:
            res = client.brave.search(country="US", limit=20, query="best running shoes")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "brave.search", dict(input), options
        )
        return RunResult[BraveSearchData].model_validate(raw)


class AsyncBraveNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BraveSearchInput],
    ) -> RunResult[BraveSearchData]:
        """Brave Search

        Run a Brave web search and get the ranked organic results (title, URL,
        snippet, position, display URL, domain) as clean JSON. Brave answers from
        its own independent index. Returns up to 20 results per call, with related
        searches and video results where the source has them; page deeper with page
        and pick the country Brave searches from.

        Price: $0.00085 per request.

        Example:
            res = client.brave.search(country="US", limit=20, query="best running shoes")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "brave.search", dict(input), options
        )
        return RunResult[BraveSearchData].model_validate(raw)
