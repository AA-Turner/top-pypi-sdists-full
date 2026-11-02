# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the glassdoor platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GlassdoorJobsInput(TypedDict, total=False):
    """Input for Glassdoor Jobs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    easyApply: NotRequired[bool]
    """When true, only return jobs offering Easy Apply. Keyword mode only."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). Range: 1 to 20."""
    location: NotRequired[str]
    """City, region, or country to search within (keyword mode; e.g. United States, New York)."""
    postedLimit: NotRequired[Literal["24h", "week", "month"]]
    """Only jobs posted within this window (past 24 hours, week, or month). Keyword mode only."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: NotRequired[str]
    """Job title or keywords to search (keyword mode). Provide this or a url."""
    requireFields: NotRequired[
        list[
            Literal[
                "companyIndustry",
                "companyRevenue",
                "companySize",
                "companyType",
                "expired",
                "logoUrl",
                "normalizedTitle",
                "sector",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `companyIndustry` or `logoUrl`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a job listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sortBy: NotRequired[Literal["date", "relevance"]]
    """Sort order: most recent (date) or best match (relevance). Keyword mode only."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Alternatively, a Glassdoor company or job search page URL to scrape (e.g. https://www.glassdoor.com/Jobs/Google-Jobs-E9079.htm). The filters below apply in keyword (query) mode."""
    workplaceType: NotRequired[Literal["remote", "hybrid", "onsite"]]
    """Filter by workplace type (remote, hybrid, or onsite). Keyword mode only."""


class GlassdoorJobsData(BaseModel):
    items: list[GlassdoorJobsItem] = Field(
        description="Job listing records for the search or company page. Populated whenever the provider has data for the entity."
    )


class GlassdoorJobsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    age_in_days: int | None = Field(
        default=None,
        alias="ageInDays",
        description="Days since the listing was posted.",
    )
    apply_url: str | None = Field(
        default=None,
        alias="applyUrl",
        description="Absolute Glassdoor URL that starts the application.",
    )
    company: str | None = Field(
        default=None,
        description="Hiring employer name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Glassdoor's numeric employer id, as a string.",
    )
    company_industry: str | None = Field(
        default=None,
        alias="companyIndustry",
        description="Primary industry of the hiring employer.",
    )
    company_revenue: str | None = Field(
        default=None,
        alias="companyRevenue",
        description="Employer revenue band as Glassdoor words it.",
    )
    company_size: str | None = Field(
        default=None,
        alias="companySize",
        description='Employer headcount band as Glassdoor words it (e.g. "1001 to 5000 Employees").',
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description='Employer ownership type (e.g. "Company - Private").',
    )
    description: str | None = Field(
        default=None, description="Full job description (may contain HTML)."
    )
    easy_apply: bool | None = Field(
        default=None,
        alias="easyApply",
        description="Whether the listing supports Glassdoor Easy Apply.",
    )
    expired: bool | None = Field(
        default=None, description="Whether Glassdoor reports the listing as expired."
    )
    id: str = Field(
        description="Glassdoor job listing id. Populated whenever the provider has data for the entity."
    )
    is_sponsored: bool | None = Field(
        default=None,
        alias="isSponsored",
        description="Whether the listing is a paid placement.",
    )
    location: str | None = Field(
        default=None, description="Job location (city, region)."
    )
    logo_url: str | None = Field(
        default=None, alias="logoUrl", description="Employer square logo image URL."
    )
    normalized_title: str | None = Field(
        default=None,
        alias="normalizedTitle",
        description="Glassdoor's normalized occupation title for the listing.",
    )
    rating: float | None = Field(
        default=None, description="Employer Glassdoor star rating (0 when not rated)."
    )
    salary: GlassdoorJobsSalary | None = Field(
        default=None, description="Estimated salary range for the listing."
    )
    sector: str | None = Field(
        default=None, description="Sector of the hiring employer."
    )
    title: str = Field(
        description="Job title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Absolute Glassdoor job listing URL. Populated whenever the provider has data for the entity."
    )


class GlassdoorJobsSalary(BaseModel):
    model_config = ConfigDict(extra="allow")

    currency: str | None = Field(
        default=None, description="ISO currency code for the salary figures."
    )
    max: float | None = Field(
        default=None, description="High end of the estimated salary range."
    )
    median: float | None = Field(
        default=None, description="Median of the estimated salary range."
    )
    min: float | None = Field(
        default=None, description="Low end of the estimated salary range."
    )
    period: str | None = Field(
        default=None, description="Pay period the figures cover (e.g. ANNUAL, HOURLY)."
    )


class GlassdoorNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GlassdoorJobsInput],
    ) -> RunResult[GlassdoorJobsData]:
        """Glassdoor Jobs

        Search Glassdoor job listings by keyword and location, or scrape any
        Glassdoor company or job search page URL - up to 20 normalized job records
        per request.

        Price: $0.007 per request.

        Example:
            res = client.glassdoor.jobs(limit=3, url="https://www.glassdoor.com/Jobs/Google-Jobs-E9079.htm")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "glassdoor.jobs", dict(input), options
        )
        return RunResult[GlassdoorJobsData].model_validate(raw)


class AsyncGlassdoorNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GlassdoorJobsInput],
    ) -> RunResult[GlassdoorJobsData]:
        """Glassdoor Jobs

        Search Glassdoor job listings by keyword and location, or scrape any
        Glassdoor company or job search page URL - up to 20 normalized job records
        per request.

        Price: $0.007 per request.

        Example:
            res = client.glassdoor.jobs(limit=3, url="https://www.glassdoor.com/Jobs/Google-Jobs-E9079.htm")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "glassdoor.jobs", dict(input), options
        )
        return RunResult[GlassdoorJobsData].model_validate(raw)
