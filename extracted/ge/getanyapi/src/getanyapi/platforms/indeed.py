# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the indeed platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class IndeedJobsInput(TypedDict, total=False):
    """Input for Indeed Jobs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Two-letter country site code (e.g. us, uk, de). Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). Range: 1 to 20."""
    location: NotRequired[str]
    """City, state, zip, or 'remote'."""
    postedLimit: NotRequired[Literal["24h", "week"]]
    """Only return jobs posted within this window: 24h (past day) or week (past 7 days). Omit for all dates. This can raise your price: a dearer source serves a request that sets it, and you are quoted and charged its price."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Job search keywords (e.g. software engineer)."""
    requireFields: NotRequired[
        list[
            Literal[
                "admin2Code",
                "companyRevenue",
                "discoveredUtc",
                "expired",
                "language",
                "rating",
                "reviewCount",
                "streetAddress",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `rating` or `streetAddress`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class IndeedJobsData(BaseModel):
    items: list[IndeedJobsItem] = Field(
        description="Job listing records: title, employer, location, salary when available, job type, posting date, and description. Populated whenever the provider has data for the entity."
    )


class IndeedJobsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    admin2_code: str | None = Field(
        default=None,
        alias="admin2Code",
        description="Second-level administrative division code (county) for the job location.",
    )
    apply_url: str | None = Field(
        default=None,
        alias="applyUrl",
        description="External URL that starts the application, usually the employer's own tracking system.",
    )
    city: str | None = None
    company: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_description: str | None = Field(
        default=None,
        alias="companyDescription",
        description="Short employer description as Indeed publishes it.",
    )
    company_revenue: str | None = Field(
        default=None,
        alias="companyRevenue",
        description="Employer revenue band as Indeed words it.",
    )
    company_size: str | None = Field(
        default=None,
        alias="companySize",
        description='Employer headcount band as Indeed words it (e.g. "501 to 1,000").',
    )
    company_url: str | None = Field(
        default=None,
        alias="companyUrl",
        description="Indeed company page URL for the employer.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer's own website."
    )
    country: str | None = None
    date_published: str | None = Field(
        default=None, alias="datePublished", description="ISO 8601 publish date."
    )
    description: str | None = Field(
        default=None, description="Plain-text job description."
    )
    discovered_utc: float | None = Field(
        default=None,
        alias="discoveredUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the listing appeared on Indeed. Multiply by 1000 for a JS Date in milliseconds.",
    )
    expired: bool | None = None
    job_id: str = Field(
        alias="jobId",
        description="Indeed job key. Populated whenever the provider has data for the entity.",
    )
    language: str | None = Field(
        default=None, description="Language code of the posting, e.g. en."
    )
    latitude: float | None = Field(
        default=None, description="Latitude of the job location."
    )
    logo_url: str | None = Field(
        default=None, alias="logoUrl", description="Employer logo image URL."
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the job location."
    )
    postal_code: str | None = Field(default=None, alias="postalCode")
    rating: float | None = Field(
        default=None, description="Employer star rating on Indeed."
    )
    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        description="Number of employer reviews on Indeed.",
    )
    salary_currency: str | None = Field(default=None, alias="salaryCurrency")
    salary_max: float | None = Field(default=None, alias="salaryMax")
    salary_min: float | None = Field(default=None, alias="salaryMin")
    salary_unit: str | None = Field(
        default=None,
        alias="salaryUnit",
        description="Salary period, e.g. YEAR or HOUR.",
    )
    state: str | None = None
    street_address: str | None = Field(
        default=None,
        alias="streetAddress",
        description="Street address of the job location.",
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Indeed job posting URL. Populated whenever the provider has data for the entity."
    )


class IndeedNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[IndeedJobsInput]
    ) -> RunResult[IndeedJobsData]:
        """Indeed Jobs

        Search Indeed job listings by keyword, location, and country, with up to 20
        normalized job records per request.

        Price: $0.00125 per request.

        Example:
            res = client.indeed.jobs(limit=3, location="Austin, TX", query="data analyst")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "indeed.jobs", dict(input), options
        )
        return RunResult[IndeedJobsData].model_validate(raw)


class AsyncIndeedNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[IndeedJobsInput]
    ) -> RunResult[IndeedJobsData]:
        """Indeed Jobs

        Search Indeed job listings by keyword, location, and country, with up to 20
        normalized job records per request.

        Price: $0.00125 per request.

        Example:
            res = client.indeed.jobs(limit=3, location="Austin, TX", query="data analyst")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "indeed.jobs", dict(input), options
        )
        return RunResult[IndeedJobsData].model_validate(raw)
