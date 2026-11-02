# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the upwork platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class UpworkJobsInput(TypedDict, total=False):
    """Input for Upwork Jobs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    experienceLevel: NotRequired[Literal["entry", "intermediate", "expert"]]
    """Filter by required experience level."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    jobType: NotRequired[Literal["fixed", "hourly"]]
    """Filter by payment type: fixed-price or hourly jobs."""
    limit: NotRequired[int]
    """Maximum number of results to return (10-25, default 25). Range: 10 to 25."""
    location: NotRequired[str]
    """Filter by client location - a region, subregion, or country (e.g. United States, Europe)."""
    paymentVerified: NotRequired[bool]
    """When true, only return jobs from clients with a verified payment method."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keywords to search Upwork jobs for (e.g. react developer)."""
    requireFields: NotRequired[list[Literal["premium", "reposted"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `premium` or `reposted`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a job that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[Literal["newest", "relevance"]]
    """Sort order for listings: newest or relevance (e.g. newest). Default: newest."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class UpworkJobsData(BaseModel):
    items: list[UpworkJobsItem] = Field(
        description="Job records: title, description, budget or hourly rate, required skills, posted date, and client details. Populated whenever the provider has data for the entity."
    )


class UpworkJobsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    budget: str | None = Field(
        default=None,
        description="Fixed-price budget in USD (e.g. $4000). Absent on hourly jobs, which carry hourlyRateMin and hourlyRateMax.",
    )
    client_location: str | None = Field(
        default=None, alias="clientLocation", description="Client country or location."
    )
    client_rating: float | None = Field(
        default=None, alias="clientRating", description="Client average rating."
    )
    client_review_count: int | None = Field(
        default=None,
        alias="clientReviewCount",
        description="Number of reviews the client has received from past contracts.",
    )
    client_total_spent: float | None = Field(
        default=None,
        alias="clientTotalSpent",
        description="Client lifetime spend (USD).",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    currency: str | None = Field(
        default=None,
        description="ISO currency code the budget is quoted in (e.g. USD).",
    )
    description: str | None = Field(
        default=None,
        description="Full job posting description text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    duration: str | None = Field(
        default=None,
        description='Expected engagement length as Upwork words it (e.g. "1 to 3 months").',
    )
    experience_level: str | None = Field(
        default=None,
        alias="experienceLevel",
        description="Required experience level (e.g. Entry, Intermediate, Expert).",
    )
    hourly_rate_max: float | None = Field(
        default=None,
        alias="hourlyRateMax",
        description="Upper bound of the client's hourly rate range in USD. Absent on fixed-price jobs.",
    )
    hourly_rate_min: float | None = Field(
        default=None,
        alias="hourlyRateMin",
        description="Lower bound of the client's hourly rate range in USD. Absent on fixed-price jobs.",
    )
    job_id: str = Field(
        alias="jobId",
        description="Upwork job identifier. Populated whenever the provider has data for the entity.",
    )
    job_type: str | None = Field(
        default=None, alias="jobType", description="Fixed or Hourly."
    )
    payment_verified: bool | None = Field(
        default=None,
        alias="paymentVerified",
        description="Whether the client's payment method is verified; null when Upwork reports it as unknown.",
    )
    premium: bool | None = Field(
        default=None, description="Whether Upwork flags the posting as premium."
    )
    proposals: int | None = Field(
        default=None, description="Number of proposals submitted."
    )
    reposted: bool | None = Field(
        default=None, description="Whether the posting is a repost of an earlier job."
    )
    tags: list[str] | None = Field(default=None, description="Skill tags.")
    title: str = Field(
        description="Job posting title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Upwork job posting URL. Populated whenever the provider has data for the entity."
    )


class UpworkNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[UpworkJobsInput]
    ) -> RunResult[UpworkJobsData]:
        """Upwork Jobs

        Search Upwork job postings by keyword, with up to 25 fresh listings per
        request.

        Price: $0.007 per request.

        Example:
            res = client.upwork.jobs(jobType="fixed", limit=10, query="web developer")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "upwork.jobs", dict(input), options
        )
        return RunResult[UpworkJobsData].model_validate(raw)


class AsyncUpworkNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[UpworkJobsInput]
    ) -> RunResult[UpworkJobsData]:
        """Upwork Jobs

        Search Upwork job postings by keyword, with up to 25 fresh listings per
        request.

        Price: $0.007 per request.

        Example:
            res = client.upwork.jobs(jobType="fixed", limit=10, query="web developer")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "upwork.jobs", dict(input), options
        )
        return RunResult[UpworkJobsData].model_validate(raw)
