# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the levels platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class LevelsJobsInput(TypedDict, total=False):
    """Input for Levels.fyi Jobs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of jobs to return (1-20, default 20). Levels.fyi groups jobs by company, up to 3 per company, so several results can come from one employer. Range: 1 to 20. Default: 20."""
    location: NotRequired[str]
    """Levels.fyi location slug as it appears in Levels.fyi URLs, e.g. united-states. Not a free-text city name; omit it to search everywhere."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Job title, keywords or company name to search, e.g. software engineer or google."""
    sortBy: NotRequired[Literal["relevance", "date", "compensation"]]
    """Sort order: best match (relevance), most recently posted (date), or highest total compensation (compensation). Default: relevance."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LevelsJobsData(BaseModel):
    items: list[LevelsJobsItem] = Field(
        description="Jobs in Levels.fyi's order, grouped by company. Populated whenever the provider has data for the entity."
    )
    total: int | None = Field(
        default=None,
        description="Total number of jobs Levels.fyi matches for the search, beyond the ones returned.",
    )


class LevelsJobsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    apply_url: str | None = Field(
        default=None,
        alias="applyUrl",
        description="URL that starts the application, usually the employer's own careers page or a job board.",
    )
    company: str | None = Field(
        default=None,
        description="Hiring company name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_slug: str | None = Field(
        default=None,
        alias="companySlug",
        description="Levels.fyi company slug, e.g. google; null when the source did not send one.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="When the job was posted. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    is_sponsored: bool | None = Field(
        default=None,
        alias="isSponsored",
        description="Whether the listing is a paid placement on Levels.fyi.",
    )
    job_id: str = Field(
        alias="jobId",
        description="Levels.fyi job id. Populated whenever the provider has data for the entity.",
    )
    location: str | None = Field(
        default=None,
        description="Job location as Levels.fyi shows it, e.g. San Jose, CA. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    logo_url: str | None = Field(
        default=None, alias="logoUrl", description="Company logo image URL."
    )
    remote: bool | None = Field(
        default=None,
        description="Whether Levels.fyi marks the job as remote; null when it does not say.",
    )
    salary_currency: str | None = Field(
        default=None,
        alias="salaryCurrency",
        description="ISO 4217 currency of the salary and compensation figures, e.g. USD.",
    )
    salary_max: float | None = Field(
        default=None,
        alias="salaryMax",
        description="High end of the base salary range in salaryCurrency per salaryUnit. null when Levels.fyi shows no salary for the job. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    salary_min: float | None = Field(
        default=None,
        alias="salaryMin",
        description="Low end of the base salary range in salaryCurrency per salaryUnit. null when Levels.fyi shows no salary for the job. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    salary_source: str | None = Field(
        default=None,
        alias="salarySource",
        description="Where the base salary range comes from, as Levels.fyi labels it, e.g. Levels.fyi base salary. null when the job has no salary range.",
    )
    salary_unit: str | None = Field(
        default=None,
        alias="salaryUnit",
        description="Pay period of the salary and compensation figures, e.g. YEAR.",
    )
    title: str = Field(
        description="Job title. Populated whenever the provider has data for the entity."
    )
    total_compensation_max: float | None = Field(
        default=None,
        alias="totalCompensationMax",
        description="High end of the total compensation range (base, stock and bonus). Some ranges are Levels.fyi estimates. null when Levels.fyi shows none.",
    )
    total_compensation_min: float | None = Field(
        default=None,
        alias="totalCompensationMin",
        description="Low end of the total compensation range (base, stock and bonus). Some ranges are Levels.fyi estimates. null when Levels.fyi shows none.",
    )
    total_compensation_source: str | None = Field(
        default=None,
        alias="totalCompensationSource",
        description="Where the total compensation range comes from, as Levels.fyi labels it, e.g. Levels.fyi total compensation. Some ranges are Levels.fyi estimates rather than figures the employer posted. null when the job has no total compensation range.",
    )
    url: str = Field(
        description="Levels.fyi job listing URL. Populated whenever the provider has data for the entity."
    )
    workplace_types: list[str] | None = Field(
        default=None,
        alias="workplaceTypes",
        description="Where the job is worked as Levels.fyi lists it, e.g. office or remote. null when Levels.fyi does not say.",
    )


class LevelsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[LevelsJobsInput]
    ) -> RunResult[LevelsJobsData]:
        """Levels.fyi Jobs

        Search Levels.fyi job listings by title or keyword and get each job with its
        salary range and estimated total compensation where Levels.fyi has them,
        plus company, location, posting date and apply link. Returns up to 20 jobs
        per call, grouped by company; filter by location and sort by relevance, date
        or pay.

        Price: $0.00085 per request.

        Example:
            res = client.levels.jobs(limit=10, location="united-states", query="software engineer")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "levels.jobs", dict(input), options
        )
        return RunResult[LevelsJobsData].model_validate(raw)


class AsyncLevelsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[LevelsJobsInput]
    ) -> RunResult[LevelsJobsData]:
        """Levels.fyi Jobs

        Search Levels.fyi job listings by title or keyword and get each job with its
        salary range and estimated total compensation where Levels.fyi has them,
        plus company, location, posting date and apply link. Returns up to 20 jobs
        per call, grouped by company; filter by location and sort by relevance, date
        or pay.

        Price: $0.00085 per request.

        Example:
            res = client.levels.jobs(limit=10, location="united-states", query="software engineer")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "levels.jobs", dict(input), options
        )
        return RunResult[LevelsJobsData].model_validate(raw)
