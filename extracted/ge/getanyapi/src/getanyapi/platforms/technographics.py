# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the technographics platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class TechnographicsTheirstackInput(TypedDict, total=False):
    """Input for Technographics - TheirStack."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: NotRequired[str]
    """Only return companies that match this domain exactly. It accepts full urls (https://www.google.com/) and emails (john.polo@gmail.com)."""
    companyId: NotRequired[str]
    """Only return companies that match this TheirStack Company ID exactly. This ID is temporary and internal and will change in the future and become stable. Until then, it is only meant to be used internally by our UI (app.theirstack.com). For deduplication logic, use company_domain or company_linkedin_url instead."""
    companyKeywordSlugOr: NotRequired[list[str]]
    """Return companies that have mentioned any of these keywords (technologies or buying intent topics) in their jobs. Case sensitive. Pass slugs. Check out all keywords at GET /v0/catalog/keywords"""
    companyLinkedinUrl: NotRequired[str]
    """Return companies whose LinkedIn URL matches this URL exactly."""
    companyName: NotRequired[str]
    """Only return companies that match this name exactly, case-sensitively."""
    companyNameOr: NotRequired[list[str]]
    """Only return companies that match these names exactly, case-sensitively. Deprecated, use the `company_name` filter instead."""
    companyTechnologySlugOr: NotRequired[list[str]]
    """Return companies that have mentioned any of these keywords (technologies or buying intent topics) in their jobs. Case sensitive. Pass slugs. Check out all keywords at GET /v0/catalog/keywords"""
    confidenceOr: NotRequired[list[str]]
    """Returns technologies with any of these confidence values that the companies use them. Available values: "high", "medium", "low" """
    firstDateFoundGte: NotRequired[str]
    """Only return technologies where the first time they were found was after or on this date. Format: "YYYY-MM-DD" """
    firstDateFoundLte: NotRequired[str]
    """Only return technologies where the first time they were found was before or on this date. Format: "YYYY-MM-DD" """
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeTotalResults: NotRequired[bool]
    """When enabled, calculates and returns `total_results` and `total_companies` fields in the response. WARNING: This significantly slows down responses as it requires reading the entire dataset. Recommended usage: enable only for the initial request to get totals, then disable for subsequent pagination requests."""
    keywordCategorySlugOr: NotRequired[list[str]]
    """Return companies that have mentioned any keyword from any of these categories in their jobs. Case sensitive. Pass slugs. Check out all keyword categories at GET /v0/catalog/keywords/categories"""
    keywordParentCategorySlugOr: NotRequired[list[str]]
    """Return companies that have mentioned any keyword from any of these parent categories in their jobs. Case sensitive. Pass slugs. Check out all keyword categories at GET /v0/catalog/keywords/categories"""
    keywordSlugOr: NotRequired[list[str]]
    """Return companies that have mentioned any of these keywords (technologies or buying intent topics) in their jobs. Case sensitive. Pass slugs. Check out all keywords at GET /v0/catalog/keywords"""
    lastDateFoundGte: NotRequired[str]
    """Only return technologies where the last time they were found was after or on this date. Format: "YYYY-MM-DD" """
    lastDateFoundLte: NotRequired[str]
    """Only return technologies where the last time they were found was before or on this date. Format: "YYYY-MM-DD" """
    limit: NotRequired[int]
    """Rows to return on this page, up to TheirStack's maximum of 500. Every row returned is billed. Range: 1 to 50. Default: 25."""
    maxJobs: NotRequired[int]
    """Maximum number of jobs found by each company using a technology"""
    maxRank: NotRequired[int]
    """The rank measures how common is a technology within its category. The technology most used among similar ones by a company will have a rank of 1, the second: 2, etc. This is useful to filter results by technology and get only results for the primary technology."""
    minJobs: NotRequired[int]
    """Minimum number of jobs found by each company using a technology"""
    minRelativeOccurrence: NotRequired[float]
    """Minimum value of relative_occurrence_within_category for each technology. Higher values increase the probability that this technology is actually used by the company, because it means a higher percentage of mentions to technologies among this category are of this technology."""
    offset: NotRequired[int]
    """Number of results to skip. Required for offset-based pagination."""
    orderBy: NotRequired[list[str]]
    """List of column objects. You can pass several columns to order by, in order of priority. Only `field` is required, `desc` is True by default."""
    page: NotRequired[int]
    """Page number. Required when using page-based pagination."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    technologyCategorySlugOr: NotRequired[list[str]]
    """Deprecated: use `keyword_category_slug_or` instead. Will return companies that have mentioned any keyword from any of these categories in their jobs. Case sensitive. Pass slugs."""
    technologyParentCategorySlugOr: NotRequired[list[str]]
    """Deprecated: use `keyword_parent_category_slug_or` instead. Will return companies that have mentioned any keyword from any of these parent categories in their jobs. Case sensitive. Pass slugs."""
    technologySlugOr: NotRequired[list[str]]
    """Deprecated: use `keyword_slug_or` instead. Will return companies that have mentioned any of these technologies in their jobs. Case sensitive. Pass slugs."""


class TechnographicsTheirstackData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    technologies: list[TechnographicsTheirstackTechnologie] = Field(
        description="Technologies detected for the company, most prominent first."
    )
    total_companies: int | None = Field(
        default=None,
        alias="totalCompanies",
        description="Distinct companies matching the filters. TheirStack computes it only when you send includeTotalResults.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Rows matching the filters across all pages. TheirStack computes it only when you send includeTotalResults, and omits it otherwise.",
    )
    truncated_companies: int | None = Field(
        default=None,
        alias="truncatedCompanies",
        description="Companies TheirStack withheld because the plan's result ceiling was reached.",
    )
    truncated_results: int | None = Field(
        default=None,
        alias="truncatedResults",
        description="Rows TheirStack withheld because the plan's result ceiling was reached.",
    )


class TechnographicsTheirstackTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    confidence: str | None = Field(
        description="How sure TheirStack is that the company uses it: high, medium or low."
    )
    first_found_utc: float | None = Field(
        default=None,
        alias="firstFoundUtc",
        description="UTC epoch timestamp in seconds (Unix time) the technology was first seen. Multiply by 1000 for a JS Date in milliseconds.",
    )
    jobs: int | None = Field(
        default=None, description="Job posts mentioning the technology, all time."
    )
    jobs_last180_days: int | None = Field(
        default=None,
        alias="jobsLast180Days",
        description="Job posts mentioning it in the last 180 days.",
    )
    jobs_last30_days: int | None = Field(
        default=None,
        alias="jobsLast30Days",
        description="Job posts mentioning it in the last 30 days.",
    )
    jobs_last7_days: int | None = Field(
        default=None,
        alias="jobsLast7Days",
        description="Job posts mentioning it in the last 7 days.",
    )
    last_found_utc: float | None = Field(
        default=None,
        alias="lastFoundUtc",
        description="UTC epoch timestamp in seconds (Unix time) the technology was last seen. Multiply by 1000 for a JS Date in milliseconds.",
    )
    rank_within_category: int | None = Field(
        default=None,
        alias="rankWithinCategory",
        description="Rank of this technology among the company's technologies in the same category, 1 being the most used.",
    )
    relative_occurrence_within_category: float | None = Field(
        default=None,
        alias="relativeOccurrenceWithinCategory",
        description="Share of the company's mentions within this category that are of this technology, 0 to 1. A higher value means the company more likely really uses it.",
    )
    technology: TechnographicsTheirstackTechnology | None = Field(
        default=None, description="The technology itself."
    )


class TechnographicsTheirstackTechnology(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category: str | None = Field(
        default=None, description="Category the technology sits in, e.g. Languages."
    )
    category_slug: str | None = Field(
        default=None, alias="categorySlug", description="Slug for that category."
    )
    image: str | None = Field(default=None, description="Technology logo URL.")
    name: str | None = Field(default=None, description="Technology name, e.g. Python.")
    parent_category: str | None = Field(
        default=None,
        alias="parentCategory",
        description="Parent category, e.g. Programming Languages And Frameworks.",
    )
    parent_category_slug: str | None = Field(
        default=None,
        alias="parentCategorySlug",
        description="Slug for that parent category.",
    )
    slug: str | None = Field(
        default=None,
        description="Technology slug. This is the value the technology filters take.",
    )
    thumbnail: str | None = Field(
        default=None, description="Smaller technology logo URL."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Whether the row is a technology or a buying-intent keyword.",
    )


class TechnographicsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def theirstack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TechnographicsTheirstackInput],
    ) -> RunResult[TechnographicsTheirstackData]:
        """Technographics - TheirStack

        Read the technology stack TheirStack detects for a company from its job
        posts, with how many posts mention each technology, when it was first and
        last seen, and how dominant it is within its category. Billed per technology
        returned.

        Price: $0 per request plus $0.1992 per result (maximum $9.96).

        Example:
            res = client.technographics.theirstack(companyDomain="posthog.com", limit=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "technographics.theirstack", dict(input), options
        )
        return RunResult[TechnographicsTheirstackData].model_validate(raw)


class AsyncTechnographicsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def theirstack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TechnographicsTheirstackInput],
    ) -> RunResult[TechnographicsTheirstackData]:
        """Technographics - TheirStack

        Read the technology stack TheirStack detects for a company from its job
        posts, with how many posts mention each technology, when it was first and
        last seen, and how dominant it is within its category. Billed per technology
        returned.

        Price: $0 per request plus $0.1992 per result (maximum $9.96).

        Example:
            res = client.technographics.theirstack(companyDomain="posthog.com", limit=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "technographics.theirstack", dict(input), options
        )
        return RunResult[TechnographicsTheirstackData].model_validate(raw)
