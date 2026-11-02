# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the semrush platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SemrushKeywordsInput(TypedDict, total=False):
    """Input for Semrush Keyword Research."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    database: NotRequired[str]
    """Two-letter Semrush regional database that scopes the metrics (e.g. us, uk, de). Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: Required[str]
    """The search term to research (e.g. "best running shoes")."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SemrushOverviewInput(TypedDict, total=False):
    """Input for Semrush Domain Overview."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    database: NotRequired[str]
    """Two-letter Semrush regional database that scopes the metrics (e.g. us, uk, de). Default: us."""
    domain: Required[str]
    """The domain to analyze (e.g. ahrefs.com)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeMoz: NotRequired[bool]
    """Add Moz Domain Authority and Spam Score to the response. Default: false."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SemrushKeywordsData(BaseModel):
    items: list[SemrushKeywordsItem] = Field(
        description="Keyword-research records: search volume, CPC, competition, keyword difficulty, plus related keywords and question keywords for the researched term. Populated whenever the provider has data for the entity."
    )


class SemrushKeywordsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    competition: float | None = Field(
        default=None,
        description="Paid-search competition density, 0 to 1, or null when Semrush has no data for the keyword.",
    )
    cpc_usd: float | None = Field(
        default=None,
        alias="cpcUsd",
        description="Average cost per click in USD, or null when Semrush has no data for the keyword.",
    )
    database: str | None = Field(
        default=None,
        description="Two-letter Semrush regional database the metrics are scoped to.",
    )
    intents: list[str] | None = Field(
        default=None,
        description="Search-intent labels for the keyword (e.g. commercial, informational). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    keyword: str = Field(
        description="The researched search term. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Semrush Keyword Difficulty, 0 to 100, or null when Semrush has no data for the keyword.",
    )
    organic_results_count: int | None = Field(
        default=None,
        alias="organicResultsCount",
        description="Number of organic results Google returns for the keyword, or null when Semrush has no data for the keyword.",
    )
    questions: list[SemrushKeywordsQuestion] | None = Field(
        default=None,
        description="Question-phrased keyword variations with their own volume and difficulty. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    referring_domains_median: int | None = Field(
        default=None,
        alias="referringDomainsMedian",
        description="Median number of referring domains across the ranking pages, or null when Semrush has no data for the keyword.",
    )
    related_keywords: list[SemrushKeywordsRelatedKeyword] | None = Field(
        default=None,
        alias="relatedKeywords",
        description="Related keyword suggestions with their own volume and difficulty. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume in the selected database, or null when Semrush has no data for the keyword.",
    )


class SemrushKeywordsQuestion(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    keyword: str = Field(description="The question keyword.")
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Semrush Keyword Difficulty for the question keyword, 0 to 100, or null when Semrush has no data for the keyword.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the question keyword, or null when Semrush has no data for the keyword.",
    )


class SemrushKeywordsRelatedKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    keyword: str = Field(description="The related keyword.")
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Semrush Keyword Difficulty for the related keyword, 0 to 100, or null when Semrush has no data for the keyword.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the related keyword, or null when Semrush has no data for the keyword.",
    )


class SemrushOverviewData(BaseModel):
    items: list[SemrushOverviewItem] = Field(
        description="Domain overview records: Authority Score, organic and paid traffic, keyword and backlink counts, top country, and the domain's top organic keywords. Populated whenever the provider has data for the entity."
    )


class SemrushOverviewItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_visibility: int | None = Field(
        default=None,
        alias="aiVisibility",
        description="Semrush AI visibility metric for the domain.",
    )
    authority_score: int | None = Field(
        default=None,
        alias="authorityScore",
        description="Semrush Authority Score, 0-100.",
    )
    backlinks: int | None = Field(
        default=None, description="Total number of backlinks pointing at the domain."
    )
    database: str | None = Field(
        default=None,
        description="Two-letter Semrush regional database the metrics are scoped to.",
    )
    domain: str = Field(
        description="The analyzed domain. Populated whenever the provider has data for the entity."
    )
    follow_backlinks: int | None = Field(
        default=None,
        alias="followBacklinks",
        description="Number of dofollow backlinks.",
    )
    moz_domain_authority: int | None = Field(
        default=None,
        alias="mozDomainAuthority",
        description="Moz Domain Authority, 0-100, or null when includeMoz is false or Moz has no data for the domain.",
    )
    moz_spam_score: str | None = Field(
        default=None,
        alias="mozSpamScore",
        description="Moz Spam Score as a percentage string, or null when includeMoz is false or Moz has no data for the domain.",
    )
    nofollow_backlinks: int | None = Field(
        default=None,
        alias="nofollowBacklinks",
        description="Number of nofollow backlinks.",
    )
    organic_keywords: int | None = Field(
        default=None,
        alias="organicKeywords",
        description="Number of keywords the domain ranks for organically.",
    )
    organic_traffic: int | None = Field(
        default=None,
        alias="organicTraffic",
        description="Estimated monthly organic search traffic.",
    )
    organic_traffic_cost_usd: float | None = Field(
        default=None,
        alias="organicTrafficCostUsd",
        description="Estimated USD value of the organic traffic.",
    )
    paid_keywords: int | None = Field(
        default=None,
        alias="paidKeywords",
        description="Number of keywords the domain bids on.",
    )
    paid_traffic: int | None = Field(
        default=None,
        alias="paidTraffic",
        description="Estimated monthly paid search traffic.",
    )
    paid_traffic_cost_usd: float | None = Field(
        default=None,
        alias="paidTrafficCostUsd",
        description="Estimated USD value of the paid traffic.",
    )
    referring_domains: int | None = Field(
        default=None,
        alias="referringDomains",
        description="Number of unique domains linking to the domain.",
    )
    top_country: str | None = Field(
        default=None,
        alias="topCountry",
        description="Two-letter code of the country sending the most traffic.",
    )
    top_country_traffic: int | None = Field(
        default=None,
        alias="topCountryTraffic",
        description="Estimated monthly traffic from the top country.",
    )
    top_keywords: list[SemrushOverviewTopKeyword] | None = Field(
        default=None,
        alias="topKeywords",
        description="The domain's top organic keywords with position, volume, and value. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    total_traffic: int | None = Field(
        default=None,
        alias="totalTraffic",
        description="Estimated total monthly traffic across organic and paid.",
    )


class SemrushOverviewTopKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cpc_usd: float | None = Field(
        default=None, alias="cpcUsd", description="Average cost per click in USD."
    )
    intents: list[str] | None = Field(
        default=None, description="Search intents associated with the keyword."
    )
    keyword: str = Field(description="The organic keyword.")
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Semrush Keyword Difficulty, 0-100.",
    )
    position: int | None = Field(
        default=None, description="Current SERP position for this keyword."
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Monthly search volume for this keyword.",
    )
    traffic: int | None = Field(
        default=None,
        description="Estimated monthly traffic this keyword drives to the domain.",
    )
    url: str | None = Field(default=None, description="The ranking URL on the domain.")


class SemrushNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SemrushKeywordsInput],
    ) -> RunResult[SemrushKeywordsData]:
        """Semrush Keyword Research

        Semrush keyword research for any term: monthly search volume, CPC,
        competition, keyword difficulty, plus related keywords and question
        keywords.

        Price: $0 per request plus $0.00495 per result (maximum $0.00495).

        Example:
            res = client.semrush.keywords(database="us", keyword="best running shoes")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "semrush.keywords", dict(input), options
        )
        return RunResult[SemrushKeywordsData].model_validate(raw)

    def overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SemrushOverviewInput],
    ) -> RunResult[SemrushOverviewData]:
        """Semrush Domain Overview

        a Semrush SEO overview for any domain: Authority Score, organic and paid
        traffic, keyword and backlink counts, top country, and the domain's top
        organic keywords.

        Price: $0 per request plus $0.00495 per result (maximum $0.00495).

        Example:
            res = client.semrush.overview(database="us", domain="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "semrush.overview", dict(input), options
        )
        return RunResult[SemrushOverviewData].model_validate(raw)


class AsyncSemrushNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SemrushKeywordsInput],
    ) -> RunResult[SemrushKeywordsData]:
        """Semrush Keyword Research

        Semrush keyword research for any term: monthly search volume, CPC,
        competition, keyword difficulty, plus related keywords and question
        keywords.

        Price: $0 per request plus $0.00495 per result (maximum $0.00495).

        Example:
            res = client.semrush.keywords(database="us", keyword="best running shoes")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "semrush.keywords", dict(input), options
        )
        return RunResult[SemrushKeywordsData].model_validate(raw)

    async def overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SemrushOverviewInput],
    ) -> RunResult[SemrushOverviewData]:
        """Semrush Domain Overview

        a Semrush SEO overview for any domain: Authority Score, organic and paid
        traffic, keyword and backlink counts, top country, and the domain's top
        organic keywords.

        Price: $0 per request plus $0.00495 per result (maximum $0.00495).

        Example:
            res = client.semrush.overview(database="us", domain="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "semrush.overview", dict(input), options
        )
        return RunResult[SemrushOverviewData].model_validate(raw)
