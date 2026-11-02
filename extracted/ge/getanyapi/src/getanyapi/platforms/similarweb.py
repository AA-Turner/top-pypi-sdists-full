# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the similarweb platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SimilarwebOverviewInput(TypedDict, total=False):
    """Input for Similarweb Website Traffic."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: Required[str]
    """The website's domain, without a scheme or path (e.g. stripe.com)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SimilarwebSimilarSitesInput(TypedDict, total=False):
    """Input for Similarweb Similar Sites."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: Required[str]
    """The website's domain, without a scheme or path (e.g. stripe.com)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SimilarwebOverviewData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avg_visit_duration_seconds: float | None = Field(
        alias="avgVisitDurationSeconds",
        description="Average visit duration in seconds.",
    )
    bounce_rate: float | None = Field(
        alias="bounceRate",
        description="Share of visits that leave after one page, as a fraction from 0 to 1.",
    )
    category: str | None = Field(
        description="Similarweb's category slug for the website (e.g. finance, news_and_media)."
    )
    category_rank: int | None = Field(
        alias="categoryRank",
        description="Rank by traffic within the website's category. Null for websites too small to rank.",
    )
    country_code: str | None = Field(
        alias="countryCode",
        description="Two-letter code of the country countryRank is measured in, the website's top country.",
    )
    country_rank: int | None = Field(
        alias="countryRank",
        description="Rank by traffic within countryCode. Null for websites too small to rank.",
    )
    description: str | None = Field(
        description="The website's meta description as Similarweb records it."
    )
    domain: str = Field(
        description="The website's domain. Populated whenever the provider has data for the entity."
    )
    global_rank: int | None = Field(
        alias="globalRank",
        description="Similarweb global rank by traffic. Null for websites too small to rank. Populated whenever the provider has data for the entity.",
    )
    image: str | None = Field(description="Screenshot of the website's homepage.")
    monthly_visits: int | None = Field(
        alias="monthlyVisits",
        description="Estimated total visits in the snapshot month. Populated whenever the provider has data for the entity.",
    )
    pages_per_visit: float | None = Field(
        alias="pagesPerVisit", description="Average pages viewed per visit."
    )
    snapshot_utc: float | None = Field(
        alias="snapshotUtc",
        description="The month the traffic figures describe: UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str | None = Field(
        description="The website's page title as Similarweb records it."
    )
    top_countries: list[SimilarwebOverviewTopCountrie] = Field(
        alias="topCountries",
        description="Countries sending the most visits, up to five, largest first. Populated whenever the provider has data for the entity.",
    )
    top_keywords: list[SimilarwebOverviewTopKeyword] = Field(
        alias="topKeywords",
        description="Search keywords sending the most visits, up to five. Populated whenever the provider has data for the entity.",
    )
    traffic_sources: SimilarwebOverviewTrafficSource = Field(
        alias="trafficSources",
        description="Where the website's visits come from. Each value is a fraction from 0 to 1 of all visits. Populated whenever the provider has data for the entity.",
    )
    visits_history: list[SimilarwebOverviewVisitsHistory] = Field(
        alias="visitsHistory",
        description="Estimated monthly visits for recent months, oldest first. Populated whenever the provider has data for the entity.",
    )


class SimilarwebOverviewTopCountrie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country_code: str = Field(
        alias="countryCode", description="Two-letter country code."
    )
    country_name: str | None = Field(
        default=None, alias="countryName", description="Country name in English."
    )
    share: float | None = Field(
        default=None,
        description="Share of the website's visits, as a fraction from 0 to 1 (0.25 means 25%).",
    )


class SimilarwebOverviewTopKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cpc_usd: float | None = Field(
        default=None,
        alias="cpcUsd",
        description="Average cost per click in USD. Null when Similarweb has no figure.",
    )
    estimated_value: float | None = Field(
        default=None,
        alias="estimatedValue",
        description="Similarweb's estimated value of the keyword to this website, as Similarweb publishes it.",
    )
    keyword: str = Field(description="The search keyword.")
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Monthly search volume for the keyword.",
    )


class SimilarwebOverviewTrafficSource(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    affiliate: float | None = Field(
        default=None,
        description="Share of visits that arrive from affiliate and paid referral links, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    direct: float | None = Field(
        default=None,
        description="Share of visits that arrive from typing the address or bookmarks, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    display_ads: float | None = Field(
        default=None,
        alias="displayAds",
        description="Share of visits that arrive from display ads, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    gen_ai: float | None = Field(
        default=None,
        alias="genAi",
        description="Share of visits that arrive from AI chatbots such as ChatGPT, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    mail: float | None = Field(
        default=None,
        description="Share of visits that arrive from email, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    referrals: float | None = Field(
        default=None,
        description="Share of visits that arrive from links on other websites, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    search_organic: float | None = Field(
        default=None,
        alias="searchOrganic",
        description="Share of visits that arrive from unpaid search results, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    search_paid: float | None = Field(
        default=None,
        alias="searchPaid",
        description="Share of visits that arrive from paid search ads, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    social_organic: float | None = Field(
        default=None,
        alias="socialOrganic",
        description="Share of visits that arrive from unpaid social media, as a fraction from 0 to 1 (0.25 means 25%).",
    )
    social_paid: float | None = Field(
        default=None,
        alias="socialPaid",
        description="Share of visits that arrive from paid social media ads, as a fraction from 0 to 1 (0.25 means 25%).",
    )


class SimilarwebOverviewVisitsHistory(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month_utc: float = Field(
        alias="monthUtc",
        description="First day of the month: UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    visits: int | None = Field(
        default=None, description="Estimated visits in that month."
    )


class SimilarwebSimilarSitesData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category: str | None = Field(
        description="Similarweb category of the website (e.g. Finance)."
    )
    description: str | None = Field(
        description="The website's meta description as Similarweb records it."
    )
    domain: str = Field(
        description="The website's domain. Populated whenever the provider has data for the entity."
    )
    sites: list[SimilarwebSimilarSitesSite] = Field(
        description="Websites most similar to this one, up to 20, most similar first. Populated whenever the provider has data for the entity."
    )
    tags: list[str] = Field(description="Topic tags Similarweb assigns the website.")
    title: str | None = Field(
        description="The website's page title as Similarweb records it."
    )
    total_visits: int | None = Field(
        alias="totalVisits", description="Estimated monthly visits to the website."
    )


class SimilarwebSimilarSitesSite(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category: str | None = Field(
        default=None,
        description="Similarweb category path of the similar website (e.g. Finance/Banking_Credit_and_Lending).",
    )
    description: str | None = Field(
        default=None, description="The similar website's meta description."
    )
    domain: str = Field(description="The similar website's domain.")
    image: str | None = Field(
        default=None, description="Screenshot of the similar website's homepage."
    )
    similarity_rank: int | None = Field(
        default=None,
        alias="similarityRank",
        description="Position in the similarity list, 1 being most similar.",
    )
    similarity_score: float | None = Field(
        default=None,
        alias="similarityScore",
        description="Similarweb's similarity score from 0 to 1, higher meaning more similar.",
    )
    top_country_rank: int | None = Field(
        default=None,
        alias="topCountryRank",
        description="The similar website's traffic rank in its own top country.",
    )
    total_visits: int | None = Field(
        default=None,
        alias="totalVisits",
        description="Estimated monthly visits to the similar website.",
    )


class SimilarwebNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SimilarwebOverviewInput],
    ) -> RunResult[SimilarwebOverviewData]:
        """Similarweb Website Traffic

        Get the Similarweb traffic overview for any website: estimated monthly
        visits and a three-month history, global, country, and category rank, bounce
        rate, pages per visit, visit duration, traffic sources including AI
        chatbots, top countries, and top search keywords - as normalized JSON.

        Price: $0.00002 per request plus $0.00165 per result (maximum $0.00167).

        Example:
            res = client.similarweb.overview(domain="stripe.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "similarweb.overview", dict(input), options
        )
        return RunResult[SimilarwebOverviewData].model_validate(raw)

    def similar_sites(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SimilarwebSimilarSitesInput],
    ) -> RunResult[SimilarwebSimilarSitesData]:
        """Similarweb Similar Sites

        Find the websites Similarweb ranks as most similar to any website: up to 20
        competitor and alternative sites in similarity order, each with its
        similarity score, category, top-country rank, estimated monthly visits, and
        description - as normalized JSON.

        Price: $0.00002 per request plus $0.00165 per result (maximum $0.00167).

        Example:
            res = client.similarweb.similar_sites(domain="stripe.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "similarweb.similar_sites", dict(input), options
        )
        return RunResult[SimilarwebSimilarSitesData].model_validate(raw)


class AsyncSimilarwebNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SimilarwebOverviewInput],
    ) -> RunResult[SimilarwebOverviewData]:
        """Similarweb Website Traffic

        Get the Similarweb traffic overview for any website: estimated monthly
        visits and a three-month history, global, country, and category rank, bounce
        rate, pages per visit, visit duration, traffic sources including AI
        chatbots, top countries, and top search keywords - as normalized JSON.

        Price: $0.00002 per request plus $0.00165 per result (maximum $0.00167).

        Example:
            res = client.similarweb.overview(domain="stripe.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "similarweb.overview", dict(input), options
        )
        return RunResult[SimilarwebOverviewData].model_validate(raw)

    async def similar_sites(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SimilarwebSimilarSitesInput],
    ) -> RunResult[SimilarwebSimilarSitesData]:
        """Similarweb Similar Sites

        Find the websites Similarweb ranks as most similar to any website: up to 20
        competitor and alternative sites in similarity order, each with its
        similarity score, category, top-country rank, estimated monthly visits, and
        description - as normalized JSON.

        Price: $0.00002 per request plus $0.00165 per result (maximum $0.00167).

        Example:
            res = client.similarweb.similar_sites(domain="stripe.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "similarweb.similar_sites", dict(input), options
        )
        return RunResult[SimilarwebSimilarSitesData].model_validate(raw)
