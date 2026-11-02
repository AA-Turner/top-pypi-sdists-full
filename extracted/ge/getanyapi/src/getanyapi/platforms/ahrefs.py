# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the ahrefs platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class AhrefsBacklinksInput(TypedDict, total=False):
    """Input for Ahrefs Backlinks."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    mode: NotRequired[Literal["exact", "subdomains"]]
    """Match scope: "exact" for the given URL only, or "subdomains" to include the domain and its subdomains. Default: subdomains."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The domain or page URL to find backlinks for (e.g. "ahrefs.com")."""


class AhrefsKeywordIdeasInput(TypedDict, total=False):
    """Input for Ahrefs Keyword Ideas."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Two-letter country code that scopes the suggestions (e.g. us, gb, de). Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: Required[str]
    """The seed keyword to expand into related suggestions (e.g. "coffee")."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AhrefsKeywordsInput(TypedDict, total=False):
    """Input for Ahrefs Keyword Difficulty."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Two-letter country code that scopes volume and difficulty (e.g. us, gb, de). Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: Required[str]
    """The search term to analyze (e.g. "seo tools")."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AhrefsOverviewInput(TypedDict, total=False):
    """Input for Ahrefs Domain Overview."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    mode: NotRequired[Literal["exact", "subdomains"]]
    """Analysis scope: subdomains covers the whole domain, exact matches only the given URL. Default: subdomains."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The domain or page URL to analyze (e.g. ahrefs.com)."""


class AhrefsTrafficInput(TypedDict, total=False):
    """Input for Ahrefs Traffic Overview."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    mode: NotRequired[Literal["exact", "subdomains", "prefix", "domain"]]
    """Analysis scope: subdomains covers the domain and its subdomains, domain covers the root domain only, prefix covers every page under the given path, exact matches only the given URL. Default: subdomains."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The domain or page URL to analyze (e.g. ahrefs.com)."""


class AhrefsBacklinksData(BaseModel):
    items: list[AhrefsBacklinksItem] = Field(
        description="Referring pages that link to the domain or URL. Populated whenever the provider has data for the entity."
    )


class AhrefsBacklinksItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor: str | None = Field(default=None, description="Anchor text of the link.")
    context_after: str | None = Field(
        default=None,
        alias="contextAfter",
        description="Text immediately after the anchor on the referring page.",
    )
    context_before: str | None = Field(
        default=None,
        alias="contextBefore",
        description="Text immediately before the anchor on the referring page.",
    )
    domain_rating: float | None = Field(
        default=None,
        alias="domainRating",
        description="Ahrefs Domain Rating (0-100) of the linking domain.",
    )
    title: str | None = Field(default=None, description="Title of the referring page.")
    url_from: str = Field(
        alias="urlFrom",
        description="URL of the referring page that contains the link. Populated whenever the provider has data for the entity.",
    )
    url_to: str | None = Field(
        default=None, alias="urlTo", description="Target URL the link points to."
    )


class AhrefsKeywordIdeasData(BaseModel):
    items: list[AhrefsKeywordIdeasItem] = Field(
        description="Keyword-idea records: the seed keyword and its related keyword suggestions, each with an Ahrefs difficulty and search-volume bucket. Populated whenever the provider has data for the entity."
    )


class AhrefsKeywordIdeasItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country: str | None = Field(
        default=None,
        description="Two-letter country code the suggestions are scoped to.",
    )
    ideas: list[AhrefsKeywordIdeasIdea] | None = Field(
        default=None,
        description="Related keyword suggestions for the seed term. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    questions: list[AhrefsKeywordIdeasQuestion] | None = Field(
        default=None,
        description="Question-shaped keyword suggestions for the seed term.",
    )
    search_engine: str | None = Field(
        default=None,
        alias="searchEngine",
        description="Search engine the suggestions are drawn from (e.g. Google).",
    )
    source_keyword: str = Field(
        alias="sourceKeyword",
        description="The seed keyword the suggestions were expanded from. Populated whenever the provider has data for the entity.",
    )


class AhrefsKeywordIdeasIdea(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    difficulty: str | None = Field(
        default=None,
        description="Relative Ahrefs difficulty bucket (a letter such as E, M, or H), not an exact number.",
    )
    keyword: str = Field(
        description="The suggested related keyword. Populated whenever the provider has data for the entity."
    )
    updated_at: str | None = Field(
        default=None,
        alias="updatedAt",
        description="Timestamp the suggestion metrics were last updated.",
    )
    volume: str | None = Field(
        default=None,
        description="Relative search-volume bucket (a letter grade), not an exact number.",
    )


class AhrefsKeywordIdeasQuestion(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    difficulty: str | None = Field(
        default=None,
        description="Relative Ahrefs difficulty bucket (a letter such as E, M, or H), not an exact number.",
    )
    keyword: str | None = Field(
        default=None, description="The suggested question keyword."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    volume: str | None = Field(
        default=None,
        description="Relative search-volume bucket (a letter grade), not an exact number.",
    )


class AhrefsKeywordsData(BaseModel):
    items: list[AhrefsKeywordsItem] = Field(
        description="Keyword-difficulty records: the difficulty score and the referring-domain gap needed to rank in the top 10. Populated whenever the provider has data for the entity."
    )


class AhrefsKeywordsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country: str | None = Field(
        default=None, description="Two-letter country code the metrics are scoped to."
    )
    cpc_usd: float | None = Field(
        default=None,
        alias="cpcUsd",
        description="Ahrefs' estimated paid-search cost per click in USD.",
    )
    difficulty: int | None = Field(
        default=None, description="Ahrefs Keyword Difficulty, 0-100."
    )
    keyword: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    referring_domains_to_rank: int | None = Field(
        default=None,
        alias="referringDomainsToRank",
        description="Estimated number of referring domains a page needs to rank in the top 10 for this keyword.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the keyword in the requested country.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class AhrefsOverviewData(BaseModel):
    items: list[AhrefsOverviewItem] = Field(
        description="Domain authority records: the requested domain plus its Domain Rating, total backlinks, and referring-domain counts. Populated whenever the provider has data for the entity."
    )


class AhrefsOverviewItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    backlinks: int | None = Field(
        default=None, description="Total number of backlinks pointing to the domain."
    )
    dofollow_backlinks_pct: int | None = Field(
        default=None,
        alias="dofollowBacklinksPct",
        description="Percentage (0-100) of backlinks that are dofollow.",
    )
    dofollow_referring_domains_pct: int | None = Field(
        default=None,
        alias="dofollowReferringDomainsPct",
        description="Percentage (0-100) of referring domains that provide a dofollow link.",
    )
    domain: str = Field(
        description="The domain or URL the metrics are scoped to. Populated whenever the provider has data for the entity."
    )
    domain_rating: float | None = Field(
        default=None,
        alias="domainRating",
        description="Ahrefs Domain Rating, 0-100, measuring backlink-profile strength.",
    )
    mode: str | None = Field(
        default=None,
        description="Analysis scope used: subdomains (whole domain) or exact (the given URL only).",
    )
    referring_domains: int | None = Field(
        default=None,
        alias="referringDomains",
        description="Number of unique referring domains linking to the domain.",
    )


class AhrefsTrafficData(BaseModel):
    items: list[AhrefsTrafficItem] = Field(
        description="Traffic overview records: the requested domain plus its monthly organic traffic, top ranking keywords, top pages, top countries, and traffic history. Populated whenever the provider has data for the entity."
    )


class AhrefsTrafficItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str = Field(
        description="The domain or URL the metrics are scoped to. Populated whenever the provider has data for the entity."
    )
    mode: str | None = Field(
        default=None,
        description="Analysis scope used: subdomains, domain, prefix, or exact.",
    )
    monthly_traffic: int | None = Field(
        default=None,
        alias="monthlyTraffic",
        description="Estimated monthly organic search visits.",
    )
    monthly_traffic_value_usd: float | None = Field(
        default=None,
        alias="monthlyTrafficValueUsd",
        description="Estimated monthly USD value of the organic traffic, what the same clicks would cost in paid search.",
    )
    top_countries: list[AhrefsTrafficTopCountrie] | None = Field(
        default=None,
        alias="topCountries",
        description="Countries sending the most organic traffic, up to five.",
    )
    top_keywords: list[AhrefsTrafficTopKeyword] | None = Field(
        default=None,
        alias="topKeywords",
        description="The top organic keywords the domain already ranks for, up to five. Not ordered by traffic. For the full ranked-keyword list, use seo.ranked_keywords. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    top_pages: list[AhrefsTrafficTopPage] | None = Field(
        default=None,
        alias="topPages",
        description="The pages receiving the most organic traffic, up to five.",
    )
    traffic_history: list[AhrefsTrafficTrafficHistory] | None = Field(
        default=None,
        alias="trafficHistory",
        description="Monthly organic traffic estimates for recent months, oldest first.",
    )


class AhrefsTrafficTopCountrie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country: str = Field(description="Two-letter country code.")
    share_pct: float | None = Field(
        default=None,
        alias="sharePct",
        description="Share (0-100) of the domain's organic traffic from this country.",
    )


class AhrefsTrafficTopKeyword(BaseModel):
    model_config = ConfigDict(extra="allow")

    keyword: str = Field(description="The organic keyword.")
    position: int | None = Field(
        default=None, description="Current Google organic position for this keyword."
    )
    traffic: int | None = Field(
        default=None,
        description="Estimated monthly traffic this keyword drives to the domain.",
    )


class AhrefsTrafficTopPage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    share_pct: float | None = Field(
        default=None,
        alias="sharePct",
        description="Share (0-100) of the domain's organic traffic this page receives.",
    )
    traffic: int | None = Field(
        default=None, description="Estimated monthly organic visits to the page."
    )
    url: str = Field(description="The page URL.")


class AhrefsTrafficTrafficHistory(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month_utc: float = Field(
        alias="monthUtc",
        description="UTC epoch timestamp in seconds (Unix time) of the first day of the month. Multiply by 1000 for a JS Date in milliseconds.",
    )
    organic_traffic: int | None = Field(
        default=None,
        alias="organicTraffic",
        description="Estimated organic search visits in that month.",
    )


class AhrefsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def backlinks(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsBacklinksInput],
    ) -> RunResult[AhrefsBacklinksData]:
        """Ahrefs Backlinks

        Get the referring pages linking to a domain or URL, each with the source
        page, anchor text, linking domain rating, and page title.

        Price: $0.00501 per request plus $0 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.backlinks(mode="exact", url="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.backlinks", dict(input), options
        )
        return RunResult[AhrefsBacklinksData].model_validate(raw)

    def keyword_ideas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsKeywordIdeasInput],
    ) -> RunResult[AhrefsKeywordIdeasData]:
        """Ahrefs Keyword Ideas

        Get related keyword suggestions for any seed term, each with an Ahrefs
        difficulty and search-volume bucket.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.keyword_ideas(country="us", keyword="coffee")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.keyword_ideas", dict(input), options
        )
        return RunResult[AhrefsKeywordIdeasData].model_validate(raw)

    def keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsKeywordsInput],
    ) -> RunResult[AhrefsKeywordsData]:
        """Ahrefs Keyword Difficulty

        Get the Ahrefs keyword-difficulty metrics for any search term: the
        difficulty score (0-100) and the number of referring domains a page needs to
        rank in the top 10 - as normalized JSON.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.keywords(country="us", keyword="seo tools")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.keywords", dict(input), options
        )
        return RunResult[AhrefsKeywordsData].model_validate(raw)

    def overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsOverviewInput],
    ) -> RunResult[AhrefsOverviewData]:
        """Ahrefs Domain Overview

        Get an SEO authority overview for any domain or URL: Domain Rating, total
        backlinks, and referring domains - as normalized JSON. For the keywords a
        domain ranks for, use seo.ranked_keywords.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.overview(mode="subdomains", url="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.overview", dict(input), options
        )
        return RunResult[AhrefsOverviewData].model_validate(raw)

    def traffic(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsTrafficInput],
    ) -> RunResult[AhrefsTrafficData]:
        """Ahrefs Traffic Overview

        Get the Ahrefs organic traffic overview for any domain or URL: monthly
        traffic estimate and value, the top 5 keywords it already ranks for with
        position and traffic, top pages, traffic by country, and a monthly traffic
        history - as normalized JSON. For a domain's full ranked-keyword list with
        search volume and difficulty, use seo.ranked_keywords.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.traffic(mode="subdomains", url="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.traffic", dict(input), options
        )
        return RunResult[AhrefsTrafficData].model_validate(raw)


class AsyncAhrefsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def backlinks(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsBacklinksInput],
    ) -> RunResult[AhrefsBacklinksData]:
        """Ahrefs Backlinks

        Get the referring pages linking to a domain or URL, each with the source
        page, anchor text, linking domain rating, and page title.

        Price: $0.00501 per request plus $0 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.backlinks(mode="exact", url="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.backlinks", dict(input), options
        )
        return RunResult[AhrefsBacklinksData].model_validate(raw)

    async def keyword_ideas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsKeywordIdeasInput],
    ) -> RunResult[AhrefsKeywordIdeasData]:
        """Ahrefs Keyword Ideas

        Get related keyword suggestions for any seed term, each with an Ahrefs
        difficulty and search-volume bucket.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.keyword_ideas(country="us", keyword="coffee")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.keyword_ideas", dict(input), options
        )
        return RunResult[AhrefsKeywordIdeasData].model_validate(raw)

    async def keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsKeywordsInput],
    ) -> RunResult[AhrefsKeywordsData]:
        """Ahrefs Keyword Difficulty

        Get the Ahrefs keyword-difficulty metrics for any search term: the
        difficulty score (0-100) and the number of referring domains a page needs to
        rank in the top 10 - as normalized JSON.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.keywords(country="us", keyword="seo tools")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.keywords", dict(input), options
        )
        return RunResult[AhrefsKeywordsData].model_validate(raw)

    async def overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsOverviewInput],
    ) -> RunResult[AhrefsOverviewData]:
        """Ahrefs Domain Overview

        Get an SEO authority overview for any domain or URL: Domain Rating, total
        backlinks, and referring domains - as normalized JSON. For the keywords a
        domain ranks for, use seo.ranked_keywords.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.overview(mode="subdomains", url="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.overview", dict(input), options
        )
        return RunResult[AhrefsOverviewData].model_validate(raw)

    async def traffic(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AhrefsTrafficInput],
    ) -> RunResult[AhrefsTrafficData]:
        """Ahrefs Traffic Overview

        Get the Ahrefs organic traffic overview for any domain or URL: monthly
        traffic estimate and value, the top 5 keywords it already ranks for with
        position and traffic, top pages, traffic by country, and a monthly traffic
        history - as normalized JSON. For a domain's full ranked-keyword list with
        search volume and difficulty, use seo.ranked_keywords.

        Price: $0.00006 per request plus $0.00495 per result (maximum $0.00501).

        Example:
            res = client.ahrefs.traffic(mode="subdomains", url="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "ahrefs.traffic", dict(input), options
        )
        return RunResult[AhrefsTrafficData].model_validate(raw)
