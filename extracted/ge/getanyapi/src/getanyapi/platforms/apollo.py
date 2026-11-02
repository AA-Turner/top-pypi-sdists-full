# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the apollo platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class ApolloOrganizationInput(TypedDict, total=False):
    """Input for Apollo Organization."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    organizationId: Required[str]
    """Organization identifier returned by an Apollo organization endpoint."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ApolloOrganizationEnrichInput(TypedDict, total=False):
    """Input for Apollo Organization Enrichment."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: Required[str]
    """Organization domain without a path, such as apollo.io."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    linkedinUrl: NotRequired[str]
    """LinkedIn company page URL, which Apollo also matches on."""
    name: NotRequired[str]
    """Organization name, which improves match accuracy."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    website: NotRequired[str]
    """Full website URL, which Apollo also matches on."""


class ApolloOrganizationJobsInput(TypedDict, total=False):
    """Input for Apollo Organization Jobs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum job postings returned on this page. Minimum: 1."""
    organizationId: Required[str]
    """Organization identifier returned by an Apollo organization endpoint."""
    page: NotRequired[int]
    """One-based result page. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ApolloOrganizationNewsInput(TypedDict, total=False):
    """Input for Apollo Organization News."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    categories: NotRequired[list[str]]
    """News categories or sub-categories to match, such as hires, investment or contract."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: NotRequired[str]
    """Optional keywords to match in related articles."""
    limit: NotRequired[int]
    """Maximum articles returned on this page. Range: 1 to 100. Default: 25."""
    organizationIds: Required[list[str]]
    """Organization identifiers whose related news should be returned."""
    page: NotRequired[int]
    """One-based result page. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    publishedAtGte: NotRequired[str]
    """Only articles published on or after this date. Format: YYYY-MM-DD."""
    publishedAtLte: NotRequired[str]
    """Only articles published on or before this date. Format: YYYY-MM-DD."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ApolloOrganizationsBulkEnrichInput(TypedDict, total=False):
    """Input for Apollo Bulk Organization Enrichment."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domains: Required[list[str]]
    """Organization domains to enrich, with at most 10 domains per request."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ApolloOrganizationsSearchInput(TypedDict, total=False):
    """Input for Apollo Organization Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domains: NotRequired[list[str]]
    """Organization domains to match, without www, at most 1000."""
    employeeRanges: NotRequired[list[str]]
    """Employee-count ranges in Apollo notation, such as 51,200."""
    excludeDomains: NotRequired[list[str]]
    """Exclude organizations matching any of these domains. Every domain Apollo holds for that organization is excluded."""
    excludeLocations: NotRequired[list[str]]
    """Headquarters locations to exclude, such as ireland."""
    headcountGrowthMonths: NotRequired[int]
    """Trailing window in months for the headcount growth filter. Takes effect only together with minHeadcountGrowthPercent or maxHeadcountGrowthPercent."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    industryIds: NotRequired[list[str]]
    """Apollo industry tag identifiers to match."""
    jobPostedAtGte: NotRequired[str]
    """Only organizations with a job posted on or after this date. Format: YYYY-MM-DD."""
    jobPostedAtLte: NotRequired[str]
    """Only organizations with a job posted on or before this date. Format: YYYY-MM-DD."""
    jobPostingLocations: NotRequired[list[str]]
    """Locations of the organization's active job postings, such as japan."""
    jobPostingTitles: NotRequired[list[str]]
    """Job titles listed in the organization's active job postings, such as sales manager."""
    keywordTags: NotRequired[list[str]]
    """Keywords associated with the organization, such as mining or consulting."""
    keywords: NotRequired[str]
    """Keywords to match across organization records."""
    lastFundingRoundDateGte: NotRequired[str]
    """Only organizations whose most recent funding round is on or after this date. Format: YYYY-MM-DD."""
    lastFundingRoundDateLte: NotRequired[str]
    """Only organizations whose most recent funding round is on or before this date. Format: YYYY-MM-DD."""
    limit: NotRequired[int]
    """Maximum organizations returned on this page. Range: 1 to 100. Default: 25."""
    locations: NotRequired[list[str]]
    """Headquarters locations to match."""
    lookalikeOrganizationIds: NotRequired[list[str]]
    """Apollo organization identifiers to use as lookalike seeds, at most five. Results are narrowed to organizations similar to the seeds, and the seeds themselves are excluded. A seed Apollo holds no lookalike data for returns no results."""
    maxFundingUsd: NotRequired[int]
    """Maximum total funding across all rounds, in whole USD."""
    maxHeadcountGrowthPercent: NotRequired[int]
    """Maximum organization headcount growth over headcountGrowthMonths, as a whole percentage such as 100 for 100%."""
    maxJobs: NotRequired[int]
    """Maximum number of active job postings at the organization."""
    maxLatestFundingUsd: NotRequired[int]
    """Maximum amount raised in the most recent funding round, in whole USD."""
    maxRevenueUsd: NotRequired[int]
    """Maximum organization annual revenue, in whole USD with no symbols."""
    minFundingUsd: NotRequired[int]
    """Minimum total funding across all rounds, in whole USD."""
    minHeadcountGrowthPercent: NotRequired[int]
    """Minimum organization headcount growth over headcountGrowthMonths, as a whole percentage such as 10 for 10%. Negative values are accepted."""
    minJobs: NotRequired[int]
    """Minimum number of active job postings at the organization."""
    minLatestFundingUsd: NotRequired[int]
    """Minimum amount raised in the most recent funding round, in whole USD."""
    minRevenueUsd: NotRequired[int]
    """Minimum organization annual revenue, in whole USD with no symbols."""
    name: NotRequired[str]
    """Organization name to match; partial matches count."""
    organizationIds: NotRequired[list[str]]
    """Apollo organization identifiers to match."""
    page: NotRequired[int]
    """One-based result page. Range: 1 to 500. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    technologySlugOr: NotRequired[list[str]]
    """Only organizations that use ANY of these technologies. Apollo technology identifiers, such as salesforce or google_analytics (spaces and periods become underscores). The technologies output of the Apollo organization SKUs returns them as id."""


class ApolloPeopleSearchInput(TypedDict, total=False):
    """Input for Apollo People Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    emailStatuses: NotRequired[
        list[Literal["verified", "unverified", "likely to engage", "unavailable"]]
    ]
    """Email statuses to match."""
    employeeRanges: NotRequired[list[str]]
    """Organization employee-count ranges in Apollo notation, such as 51,200."""
    excludeOrganizationDomains: NotRequired[list[str]]
    """Exclude people whose current employer matches any of these domains. Every domain Apollo holds for that employer is excluded."""
    headcountGrowthMonths: NotRequired[int]
    """Trailing window in months for the headcount growth filter. Takes effect only together with minHeadcountGrowthPercent or maxHeadcountGrowthPercent."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeSimilarTitles: NotRequired[bool]
    """Whether titles similar to the ones in titles also match. Set false for strict title matches only."""
    jobPostedAtGte: NotRequired[str]
    """Only organizations with a job posted on or after this date. Format: YYYY-MM-DD."""
    jobPostedAtLte: NotRequired[str]
    """Only organizations with a job posted on or before this date. Format: YYYY-MM-DD."""
    jobPostingLocations: NotRequired[list[str]]
    """Locations of the organization's active job postings, such as japan."""
    jobPostingTitles: NotRequired[list[str]]
    """Job titles listed in the organization's active job postings, such as sales manager."""
    keywords: NotRequired[str]
    """Keywords to match across people records."""
    limit: NotRequired[int]
    """Maximum people returned on this page. Range: 1 to 100. Default: 25."""
    lookalikeOrganizationIds: NotRequired[list[str]]
    """Apollo organization identifiers to use as lookalike seeds, at most five. Results are narrowed to organizations similar to the seeds, and the seeds themselves are excluded. A seed Apollo holds no lookalike data for returns no results."""
    maxHeadcountGrowthPercent: NotRequired[int]
    """Maximum organization headcount growth over headcountGrowthMonths, as a whole percentage such as 100 for 100%."""
    maxJobs: NotRequired[int]
    """Maximum number of active job postings at the organization."""
    maxRevenueUsd: NotRequired[int]
    """Maximum organization annual revenue, in whole USD with no symbols."""
    minHeadcountGrowthPercent: NotRequired[int]
    """Minimum organization headcount growth over headcountGrowthMonths, as a whole percentage such as 10 for 10%. Negative values are accepted."""
    minJobs: NotRequired[int]
    """Minimum number of active job postings at the organization."""
    minRevenueUsd: NotRequired[int]
    """Minimum organization annual revenue, in whole USD with no symbols."""
    organizationDomains: NotRequired[list[str]]
    """Domains of the person's current or previous employer, without www, at most 1000."""
    organizationIds: NotRequired[list[str]]
    """Apollo identifiers of the person's current employer."""
    organizationLocations: NotRequired[list[str]]
    """Organization headquarters locations to match."""
    page: NotRequired[int]
    """One-based result page. Range: 1 to 500. Default: 1."""
    personLocations: NotRequired[list[str]]
    """Person locations to match."""
    personName: NotRequired[str]
    """Person name to match; results include people whose name contains every word."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    seniorities: NotRequired[
        list[
            Literal[
                "owner",
                "founder",
                "c_suite",
                "partner",
                "vp",
                "head",
                "director",
                "manager",
                "senior",
                "entry",
                "intern",
            ]
        ]
    ]
    """Seniority levels to match."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    technologySlugAnd: NotRequired[list[str]]
    """Only people whose current employer uses ALL of these technologies. Apollo technology identifiers, such as salesforce or google_analytics (spaces and periods become underscores). The technologies output of the Apollo organization SKUs returns them as id."""
    technologySlugNot: NotRequired[list[str]]
    """Exclude people whose current employer uses any of these technologies. Apollo technology identifiers, such as salesforce or google_analytics (spaces and periods become underscores). The technologies output of the Apollo organization SKUs returns them as id."""
    technologySlugOr: NotRequired[list[str]]
    """Only people whose current employer uses ANY of these technologies. Apollo technology identifiers, such as salesforce or google_analytics (spaces and periods become underscores). The technologies output of the Apollo organization SKUs returns them as id."""
    titles: NotRequired[list[str]]
    """Job titles to match."""


class ApolloPersonEnrichInput(TypedDict, total=False):
    """Input for Apollo Person Enrichment."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: NotRequired[str]
    """Organization domain used with the person's name."""
    email: NotRequired[str]
    """Work or personal email used to identify the person."""
    emailHash: NotRequired[str]
    """MD5 or SHA-256 hash of the person's email, used to identify the person."""
    firstName: NotRequired[str]
    """Person first name, used with lastName and an organization identifier."""
    fullName: NotRequired[str]
    """Person full name, used with an organization identifier instead of firstName and lastName."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lastName: NotRequired[str]
    """Person last name, used with firstName and an organization identifier."""
    linkedinUrl: NotRequired[str]
    """LinkedIn profile URL used to identify the person."""
    organizationName: NotRequired[str]
    """Organization name used with the person's name."""
    personId: NotRequired[str]
    """Apollo person identifier, such as an id returned by apollo.people_search."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    revealPersonalEmails: NotRequired[bool]
    """Whether to include personal emails. Apollo withholds them for people in GDPR regions. Default: true."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ApolloOrganizationData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alexa_ranking: int | None = Field(
        default=None,
        alias="alexaRanking",
        description="Alexa global traffic rank of the organization website.",
    )
    angellist_url: str | None = Field(
        default=None,
        alias="angellistUrl",
        description="Canonical AngelList profile URL.",
    )
    annual_revenue: float | None = Field(
        default=None,
        alias="annualRevenue",
        description="Estimated annual revenue in USD. Minimum: 0.",
    )
    annual_revenue_display: str | None = Field(
        default=None,
        alias="annualRevenueDisplay",
        description="Human-readable estimated annual revenue.",
    )
    city: str | None = Field(default=None, description="Headquarters city.")
    country: str | None = Field(default=None, description="Headquarters country.")
    crunchbase_url: str | None = Field(
        default=None,
        alias="crunchbaseUrl",
        description="Canonical Crunchbase profile URL.",
    )
    description: str | None = Field(default=None, description="Organization summary.")
    domain: str | None = Field(default=None, description="Primary organization domain.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated employee count. Minimum: 0.",
    )
    employee_metrics: list[ApolloOrganizationEmployeeMetric] | None = Field(
        default=None,
        alias="employeeMetrics",
        description="Monthly headcount flow per department.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical Facebook page URL."
    )
    founded_year: int | None = Field(
        default=None,
        alias="foundedYear",
        description="Year the organization was founded.",
    )
    funding_events: list[ApolloOrganizationFundingEvent] | None = Field(
        default=None,
        alias="fundingEvents",
        description="Funding rounds Apollo records for the organization.",
    )
    id: str | None = Field(description="Stable organization identifier.")
    image: str | None = Field(default=None, description="Organization logo URL.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the organization."
    )
    industry: str | None = Field(default=None, description="Primary industry.")
    industry_tag_id: str | None = Field(
        default=None,
        alias="industryTagId",
        description="Apollo industry tag identifier of the primary industry, accepted by apollo.organizations_search industryIds.",
    )
    industry_tag_ids: ApolloOrganizationIndustryTagId | None = Field(
        default=None,
        alias="industryTagIds",
        description="Apollo industry tag identifier for each industry, keyed by industry name. The identifiers are accepted by apollo.organizations_search industryIds.",
    )
    keywords: list[str] | None = Field(
        default=None, description="Keywords associated with the organization."
    )
    languages: list[str] | None = Field(
        default=None, description="Languages the organization operates in."
    )
    latest_funding_detected_utc: float | None = Field(
        default=None,
        alias="latestFundingDetectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    latest_funding_stage: str | None = Field(
        default=None,
        alias="latestFundingStage",
        description="Latest disclosed funding stage.",
    )
    latest_funding_utc: float | None = Field(
        default=None,
        alias="latestFundingUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="Organization LinkedIn numeric id.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn company URL."
    )
    naics_codes: list[str] | None = Field(
        default=None, alias="naicsCodes", description="NAICS industry codes."
    )
    name: str | None = Field(description="Organization name.")
    org_chart_root_person_ids: list[str] | None = Field(
        default=None,
        alias="orgChartRootPersonIds",
        description="Apollo person identifiers at the top of the organization's org chart, accepted by apollo.person_enrich personId.",
    )
    parent_organization_id: str | None = Field(
        default=None,
        alias="parentOrganizationId",
        description="Identifier of the organization that owns this one.",
    )
    parent_organization_name: str | None = Field(
        default=None,
        alias="parentOrganizationName",
        description="Name of the organization that owns this one.",
    )
    parent_organization_website_url: str | None = Field(
        default=None,
        alias="parentOrganizationWebsiteUrl",
        description="Website URL of the organization that owns this one.",
    )
    phone: str | None = Field(
        default=None, description="Organization phone number in international format."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Headquarters postal code."
    )
    publicly_traded_exchange: str | None = Field(
        default=None,
        alias="publiclyTradedExchange",
        description="Exchange the company lists on, such as nyse.",
    )
    publicly_traded_symbol: str | None = Field(
        default=None,
        alias="publiclyTradedSymbol",
        description="Stock ticker, for listed companies.",
    )
    raw_address: str | None = Field(
        default=None,
        alias="rawAddress",
        description="Headquarters address as one display string.",
    )
    retail_location_count: int | None = Field(
        default=None,
        alias="retailLocationCount",
        description="Number of retail locations Apollo records for the organization. Minimum: 0.",
    )
    sanitized_phone: str | None = Field(
        default=None,
        alias="sanitizedPhone",
        description="Organization phone number in international E.164 form, such as +14152985539.",
    )
    secondary_industries: list[str] | None = Field(
        default=None,
        alias="secondaryIndustries",
        description="Industries associated with the organization besides the primary industry.",
    )
    sic_codes: list[str] | None = Field(
        default=None, alias="sicCodes", description="SIC industry codes."
    )
    state: str | None = Field(default=None, description="Headquarters state or region.")
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Street address."
    )
    suborganization_count: int | None = Field(
        default=None,
        alias="suborganizationCount",
        description="Number of related organizations Apollo lists under this one. Minimum: 0.",
    )
    suborganizations: list[ApolloOrganizationSuborganization] | None = Field(
        default=None,
        description="Related organizations Apollo lists under this one, usually subsidiaries or acquisitions.",
    )
    technologies: list[ApolloOrganizationTechnologie] | None = Field(
        default=None,
        description="Technologies detected at the organization, with their category.",
    )
    technology_names: list[str] | None = Field(
        default=None,
        alias="technologyNames",
        description="Technologies detected at the organization.",
    )
    total_funding: float | None = Field(
        default=None,
        alias="totalFunding",
        description="Total disclosed funding in USD. Minimum: 0.",
    )
    total_funding_display: str | None = Field(
        default=None,
        alias="totalFundingDisplay",
        description="Human-readable total disclosed funding.",
    )
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical X or Twitter profile URL.",
    )
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloOrganizationEmployeeMetric(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    departments: list[ApolloOrganizationDepartment] | None = Field(
        default=None, description="Headcount flow per department in the month."
    )
    start_utc: float | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class ApolloOrganizationDepartment(BaseModel):
    model_config = ConfigDict(extra="allow")

    churned: int | None = Field(
        default=None,
        description="People who left the department in the month. Minimum: 0.",
    )
    department: str | None = Field(
        default=None,
        description="Apollo department name. Absent on the row Apollo does not attribute to a department.",
    )
    new: int | None = Field(
        default=None,
        description="People who joined the department in the month. Minimum: 0.",
    )
    retained: int | None = Field(
        default=None,
        description="People who stayed in the department through the month. Minimum: 0.",
    )


class ApolloOrganizationFundingEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    amount_display: str | None = Field(
        default=None,
        alias="amountDisplay",
        description="Amount raised in this round as Apollo displays it, such as 100M.",
    )
    currency: str | None = Field(
        default=None, description="Currency symbol of the amount, such as $."
    )
    detected_utc: float | None = Field(
        default=None,
        alias="detectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(default=None, description="Funding round identifier.")
    investors: str | None = Field(
        default=None,
        description="Investors in this round as one comma-separated string, exactly as Apollo returns it. A single investor name can itself contain a comma.",
    )
    news_url: str | None = Field(
        default=None, alias="newsUrl", description="Article reporting the round."
    )
    raised_utc: float | None = Field(
        default=None,
        alias="raisedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Funding round type, such as Series D."
    )


class ApolloOrganizationIndustryTagId(BaseModel):
    model_config = ConfigDict(extra="allow")


class ApolloOrganizationSuborganization(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country: str | None = Field(default=None, description="Headquarters country.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated employee count. Minimum: 0.",
    )
    id: str | None = Field(default=None, description="Organization identifier.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the organization."
    )
    name: str | None = Field(default=None, description="Organization name.")
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloOrganizationTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")

    category: str | None = Field(default=None, description="Technology category.")
    id: str | None = Field(
        default=None,
        description="Technology identifier, accepted by the technologySlug filters of apollo.organizations_search and apollo.people_search.",
    )
    name: str | None = Field(default=None, description="Technology name.")


class ApolloOrganizationEnrichData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alexa_ranking: int | None = Field(
        default=None,
        alias="alexaRanking",
        description="Alexa global traffic rank of the organization website.",
    )
    angellist_url: str | None = Field(
        default=None,
        alias="angellistUrl",
        description="Canonical AngelList profile URL.",
    )
    annual_revenue: float | None = Field(
        default=None,
        alias="annualRevenue",
        description="Estimated annual revenue in USD. Minimum: 0.",
    )
    annual_revenue_display: str | None = Field(
        default=None,
        alias="annualRevenueDisplay",
        description="Human-readable estimated annual revenue.",
    )
    city: str | None = Field(default=None, description="Headquarters city.")
    country: str | None = Field(default=None, description="Headquarters country.")
    crunchbase_url: str | None = Field(
        default=None,
        alias="crunchbaseUrl",
        description="Canonical Crunchbase profile URL.",
    )
    description: str | None = Field(default=None, description="Organization summary.")
    domain: str | None = Field(default=None, description="Primary organization domain.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated employee count. Minimum: 0.",
    )
    employee_growth: ApolloOrganizationEnrichEmployeeGrowth | None = Field(
        default=None,
        alias="employeeGrowth",
        description="Headcount change over trailing windows, in percent.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical Facebook page URL."
    )
    founded_year: int | None = Field(
        default=None,
        alias="foundedYear",
        description="Year the organization was founded.",
    )
    funding_events: list[ApolloOrganizationEnrichFundingEvent] | None = Field(
        default=None,
        alias="fundingEvents",
        description="Funding rounds Apollo records for the organization.",
    )
    headcount_by_role: ApolloOrganizationEnrichHeadcountByRole | None = Field(
        default=None,
        alias="headcountByRole",
        description="Employee count per department, keyed by Apollo department name.",
    )
    id: str | None = Field(description="Stable organization identifier.")
    image: str | None = Field(default=None, description="Organization logo URL.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the organization."
    )
    industry: str | None = Field(default=None, description="Primary industry.")
    industry_tag_id: str | None = Field(
        default=None,
        alias="industryTagId",
        description="Apollo industry tag identifier of the primary industry, accepted by apollo.organizations_search industryIds.",
    )
    industry_tag_ids: ApolloOrganizationEnrichIndustryTagId | None = Field(
        default=None,
        alias="industryTagIds",
        description="Apollo industry tag identifier for each industry, keyed by industry name. The identifiers are accepted by apollo.organizations_search industryIds.",
    )
    keywords: list[str] | None = Field(
        default=None, description="Keywords associated with the organization."
    )
    languages: list[str] | None = Field(
        default=None, description="Languages the organization operates in."
    )
    latest_funding_detected_utc: float | None = Field(
        default=None,
        alias="latestFundingDetectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    latest_funding_stage: str | None = Field(
        default=None,
        alias="latestFundingStage",
        description="Latest disclosed funding stage.",
    )
    latest_funding_utc: float | None = Field(
        default=None,
        alias="latestFundingUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="Organization LinkedIn numeric id.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn company URL."
    )
    naics_codes: list[str] | None = Field(
        default=None, alias="naicsCodes", description="NAICS industry codes."
    )
    name: str | None = Field(description="Organization name.")
    org_chart_root_person_ids: list[str] | None = Field(
        default=None,
        alias="orgChartRootPersonIds",
        description="Apollo person identifiers at the top of the organization's org chart, accepted by apollo.person_enrich personId.",
    )
    parent_organization_id: str | None = Field(
        default=None,
        alias="parentOrganizationId",
        description="Identifier of the organization that owns this one.",
    )
    phone: str | None = Field(
        default=None, description="Organization phone number in international format."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Headquarters postal code."
    )
    publicly_traded_exchange: str | None = Field(
        default=None,
        alias="publiclyTradedExchange",
        description="Exchange the company lists on, such as nyse.",
    )
    publicly_traded_symbol: str | None = Field(
        default=None,
        alias="publiclyTradedSymbol",
        description="Stock ticker, for listed companies.",
    )
    raw_address: str | None = Field(
        default=None,
        alias="rawAddress",
        description="Headquarters address as one display string.",
    )
    retail_location_count: int | None = Field(
        default=None,
        alias="retailLocationCount",
        description="Number of retail locations Apollo records for the organization. Minimum: 0.",
    )
    sanitized_phone: str | None = Field(
        default=None,
        alias="sanitizedPhone",
        description="Organization phone number in international E.164 form, such as +14152985539.",
    )
    secondary_industries: list[str] | None = Field(
        default=None,
        alias="secondaryIndustries",
        description="Industries associated with the organization besides the primary industry.",
    )
    sic_codes: list[str] | None = Field(
        default=None, alias="sicCodes", description="SIC industry codes."
    )
    state: str | None = Field(default=None, description="Headquarters state or region.")
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Street address."
    )
    suborganization_count: int | None = Field(
        default=None,
        alias="suborganizationCount",
        description="Number of related organizations Apollo lists under this one. Minimum: 0.",
    )
    suborganizations: list[ApolloOrganizationEnrichSuborganization] | None = Field(
        default=None,
        description="Related organizations Apollo lists under this one, usually subsidiaries or acquisitions.",
    )
    technologies: list[ApolloOrganizationEnrichTechnologie] | None = Field(
        default=None,
        description="Technologies detected at the organization, with their category.",
    )
    technology_names: list[str] | None = Field(
        default=None,
        alias="technologyNames",
        description="Technologies detected at the organization.",
    )
    total_funding: float | None = Field(
        default=None,
        alias="totalFunding",
        description="Total disclosed funding in USD. Minimum: 0.",
    )
    total_funding_display: str | None = Field(
        default=None,
        alias="totalFundingDisplay",
        description="Human-readable total disclosed funding.",
    )
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical X or Twitter profile URL.",
    )
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloOrganizationEnrichEmployeeGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent24m: float | None = Field(
        default=None, description="Percent change over the last twenty-four months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class ApolloOrganizationEnrichFundingEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    amount_display: str | None = Field(
        default=None,
        alias="amountDisplay",
        description="Amount raised in this round as Apollo displays it, such as 100M.",
    )
    currency: str | None = Field(
        default=None, description="Currency symbol of the amount, such as $."
    )
    detected_utc: float | None = Field(
        default=None,
        alias="detectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(default=None, description="Funding round identifier.")
    investors: str | None = Field(
        default=None,
        description="Investors in this round as one comma-separated string, exactly as Apollo returns it. A single investor name can itself contain a comma.",
    )
    news_url: str | None = Field(
        default=None, alias="newsUrl", description="Article reporting the round."
    )
    raised_utc: float | None = Field(
        default=None,
        alias="raisedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Funding round type, such as Series D."
    )


class ApolloOrganizationEnrichHeadcountByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class ApolloOrganizationEnrichIndustryTagId(BaseModel):
    model_config = ConfigDict(extra="allow")


class ApolloOrganizationEnrichSuborganization(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country: str | None = Field(default=None, description="Headquarters country.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated employee count. Minimum: 0.",
    )
    id: str | None = Field(default=None, description="Organization identifier.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the organization."
    )
    name: str | None = Field(default=None, description="Organization name.")
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloOrganizationEnrichTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")

    category: str | None = Field(default=None, description="Technology category.")
    id: str | None = Field(
        default=None,
        description="Technology identifier, accepted by the technologySlug filters of apollo.organizations_search and apollo.people_search.",
    )
    name: str | None = Field(default=None, description="Technology name.")


class ApolloOrganizationJobsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    jobs: list[ApolloOrganizationJobsJob] = Field(description="Current job postings.")
    limit: int = Field(description="Page size returned. Minimum: 0.")
    page: int = Field(description="One-based page returned. Minimum: 1.")
    total: int = Field(description="Total current job postings. Minimum: 0.")
    total_pages: int = Field(
        alias="totalPages", description="Total available pages. Minimum: 0."
    )


class ApolloOrganizationJobsJob(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="Job city.")
    country: str | None = Field(default=None, description="Job country.")
    id: str | None = Field(description="Stable job posting identifier.")
    last_seen_utc: float | None = Field(
        default=None,
        alias="lastSeenUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    posted_utc: float | None = Field(
        default=None,
        alias="postedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    state: str | None = Field(default=None, description="Job state or region.")
    title: str | None = Field(description="Job title.")
    url: str | None = Field(description="Canonical job posting URL.")


class ApolloOrganizationNewsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    articles: list[ApolloOrganizationNewsArticle] = Field(
        description="Related news articles on this page."
    )
    limit: int = Field(description="Page size returned. Minimum: 0.")
    page: int = Field(description="One-based page returned. Minimum: 1.")
    total: int = Field(description="Total matching articles. Minimum: 0.")
    total_pages: int = Field(
        alias="totalPages", description="Total available pages. Minimum: 0."
    )


class ApolloOrganizationNewsArticle(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str | None = Field(default=None, description="Publishing domain.")
    event_categories: list[str] | None = Field(
        default=None,
        alias="eventCategories",
        description="Detected business event categories.",
    )
    id: str | None = Field(description="Stable article identifier.")
    organization_ids: list[str] | None = Field(
        default=None,
        alias="organizationIds",
        description="Organization identifiers associated with the article.",
    )
    published_utc: float | None = Field(
        default=None,
        alias="publishedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    snippet: str | None = Field(default=None, description="Article summary or excerpt.")
    title: str | None = Field(description="Article title.")
    url: str | None = Field(description="Canonical article URL.")


class ApolloOrganizationsBulkEnrichData(BaseModel):
    enriched: int = Field(
        description="Number of uniquely enriched organizations. Minimum: 0."
    )
    missing: int = Field(
        description="Number of requested domains without a match. Minimum: 0."
    )
    organizations: list[ApolloOrganizationsBulkEnrichOrganization | None] = Field(
        description="Enriched organizations, positionally aligned with the requested domains: index i of this array is the result for index i of the domains input, and the array is always the same length as that input. An entry is null when the domain had no match, so a partial batch still returns every domain it did resolve."
    )
    requested: int = Field(description="Number of requested domains. Minimum: 0.")


class ApolloOrganizationsBulkEnrichOrganization(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alexa_ranking: int | None = Field(
        default=None,
        alias="alexaRanking",
        description="Alexa global traffic rank of the organization website.",
    )
    angellist_url: str | None = Field(
        default=None,
        alias="angellistUrl",
        description="Canonical AngelList profile URL.",
    )
    annual_revenue: float | None = Field(
        default=None,
        alias="annualRevenue",
        description="Estimated annual revenue in USD. Minimum: 0.",
    )
    annual_revenue_display: str | None = Field(
        default=None,
        alias="annualRevenueDisplay",
        description="Human-readable estimated annual revenue.",
    )
    city: str | None = Field(default=None, description="Headquarters city.")
    country: str | None = Field(default=None, description="Headquarters country.")
    crunchbase_url: str | None = Field(
        default=None,
        alias="crunchbaseUrl",
        description="Canonical Crunchbase profile URL.",
    )
    description: str | None = Field(default=None, description="Organization summary.")
    domain: str | None = Field(default=None, description="Primary organization domain.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated employee count. Minimum: 0.",
    )
    employee_growth: ApolloOrganizationsBulkEnrichEmployeeGrowth | None = Field(
        default=None,
        alias="employeeGrowth",
        description="Headcount change over trailing windows, in percent.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical Facebook page URL."
    )
    founded_year: int | None = Field(
        default=None,
        alias="foundedYear",
        description="Year the organization was founded.",
    )
    funding_events: list[ApolloOrganizationsBulkEnrichFundingEvent] | None = Field(
        default=None,
        alias="fundingEvents",
        description="Funding rounds Apollo records for the organization.",
    )
    headcount_by_role: ApolloOrganizationsBulkEnrichHeadcountByRole | None = Field(
        default=None,
        alias="headcountByRole",
        description="Employee count per department, keyed by Apollo department name.",
    )
    id: str | None = Field(description="Stable organization identifier.")
    image: str | None = Field(default=None, description="Organization logo URL.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the organization."
    )
    industry: str | None = Field(default=None, description="Primary industry.")
    industry_tag_id: str | None = Field(
        default=None,
        alias="industryTagId",
        description="Apollo industry tag identifier of the primary industry, accepted by apollo.organizations_search industryIds.",
    )
    industry_tag_ids: ApolloOrganizationsBulkEnrichIndustryTagId | None = Field(
        default=None,
        alias="industryTagIds",
        description="Apollo industry tag identifier for each industry, keyed by industry name. The identifiers are accepted by apollo.organizations_search industryIds.",
    )
    keywords: list[str] | None = Field(
        default=None, description="Keywords associated with the organization."
    )
    languages: list[str] | None = Field(
        default=None, description="Languages the organization operates in."
    )
    latest_funding_detected_utc: float | None = Field(
        default=None,
        alias="latestFundingDetectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    latest_funding_stage: str | None = Field(
        default=None,
        alias="latestFundingStage",
        description="Latest disclosed funding stage.",
    )
    latest_funding_utc: float | None = Field(
        default=None,
        alias="latestFundingUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="Organization LinkedIn numeric id.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn company URL."
    )
    naics_codes: list[str] | None = Field(
        default=None, alias="naicsCodes", description="NAICS industry codes."
    )
    name: str | None = Field(description="Organization name.")
    ownership_chain_ids: list[str] | None = Field(
        default=None,
        alias="ownershipChainIds",
        description="Identifiers of the organizations in this organization's ownership chain.",
    )
    parent_organization_id: str | None = Field(
        default=None,
        alias="parentOrganizationId",
        description="Identifier of the organization that owns this one.",
    )
    parent_organization_name: str | None = Field(
        default=None,
        alias="parentOrganizationName",
        description="Name of the organization that owns this one.",
    )
    parent_organization_website_url: str | None = Field(
        default=None,
        alias="parentOrganizationWebsiteUrl",
        description="Website URL of the organization that owns this one.",
    )
    phone: str | None = Field(
        default=None, description="Organization phone number in international format."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Headquarters postal code."
    )
    publicly_traded_exchange: str | None = Field(
        default=None,
        alias="publiclyTradedExchange",
        description="Exchange the company lists on, such as nyse.",
    )
    publicly_traded_symbol: str | None = Field(
        default=None,
        alias="publiclyTradedSymbol",
        description="Stock ticker, for listed companies.",
    )
    raw_address: str | None = Field(
        default=None,
        alias="rawAddress",
        description="Headquarters address as one display string.",
    )
    retail_location_count: int | None = Field(
        default=None,
        alias="retailLocationCount",
        description="Number of retail locations Apollo records for the organization. Minimum: 0.",
    )
    sanitized_phone: str | None = Field(
        default=None,
        alias="sanitizedPhone",
        description="Organization phone number in international E.164 form, such as +14152985539.",
    )
    secondary_industries: list[str] | None = Field(
        default=None,
        alias="secondaryIndustries",
        description="Industries associated with the organization besides the primary industry.",
    )
    sic_codes: list[str] | None = Field(
        default=None, alias="sicCodes", description="SIC industry codes."
    )
    state: str | None = Field(default=None, description="Headquarters state or region.")
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Street address."
    )
    suborganization_count: int | None = Field(
        default=None,
        alias="suborganizationCount",
        description="Number of related organizations Apollo lists under this one. Minimum: 0.",
    )
    subsidiary_countries: list[str] | None = Field(
        default=None,
        alias="subsidiaryCountries",
        description="Countries Apollo rolls up across the organization's corporate family.",
    )
    subsidiary_employee_count: int | None = Field(
        default=None,
        alias="subsidiaryEmployeeCount",
        description="Estimated employee count Apollo rolls up across the organization's corporate family. Minimum: 0.",
    )
    subsidiary_industries: list[str] | None = Field(
        default=None,
        alias="subsidiaryIndustries",
        description="Industries Apollo rolls up across the organization's corporate family.",
    )
    total_funding: float | None = Field(
        default=None,
        alias="totalFunding",
        description="Total disclosed funding in USD. Minimum: 0.",
    )
    total_funding_display: str | None = Field(
        default=None,
        alias="totalFundingDisplay",
        description="Human-readable total disclosed funding.",
    )
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical X or Twitter profile URL.",
    )
    ultimate_parent_organization_id: str | None = Field(
        default=None,
        alias="ultimateParentOrganizationId",
        description="Identifier of the top organization in this organization's ownership chain.",
    )
    ultimate_parent_organization_name: str | None = Field(
        default=None,
        alias="ultimateParentOrganizationName",
        description="Name of the top organization in this organization's ownership chain.",
    )
    ultimate_parent_organization_website_url: str | None = Field(
        default=None,
        alias="ultimateParentOrganizationWebsiteUrl",
        description="Website URL of the top organization in this organization's ownership chain.",
    )
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloOrganizationsBulkEnrichEmployeeGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent24m: float | None = Field(
        default=None, description="Percent change over the last twenty-four months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class ApolloOrganizationsBulkEnrichFundingEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    amount_display: str | None = Field(
        default=None,
        alias="amountDisplay",
        description="Amount raised in this round as Apollo displays it, such as 100M.",
    )
    currency: str | None = Field(
        default=None, description="Currency symbol of the amount, such as $."
    )
    detected_utc: float | None = Field(
        default=None,
        alias="detectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(default=None, description="Funding round identifier.")
    investors: str | None = Field(
        default=None,
        description="Investors in this round as one comma-separated string, exactly as Apollo returns it. A single investor name can itself contain a comma.",
    )
    news_url: str | None = Field(
        default=None, alias="newsUrl", description="Article reporting the round."
    )
    raised_utc: float | None = Field(
        default=None,
        alias="raisedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Funding round type, such as Series D."
    )


class ApolloOrganizationsBulkEnrichHeadcountByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class ApolloOrganizationsBulkEnrichIndustryTagId(BaseModel):
    model_config = ConfigDict(extra="allow")


class ApolloOrganizationsSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    limit: int = Field(
        description="Page size returned by the upstream database. Minimum: 0."
    )
    organizations: list[ApolloOrganizationsSearchOrganization] = Field(
        description="Organizations on this page."
    )
    page: int = Field(description="One-based page returned. Minimum: 1.")
    total: int = Field(description="Total matching organizations. Minimum: 0.")
    total_pages: int = Field(
        alias="totalPages", description="Total available pages. Minimum: 0."
    )


class ApolloOrganizationsSearchOrganization(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alexa_ranking: int | None = Field(
        default=None,
        alias="alexaRanking",
        description="Alexa global traffic rank of the organization website.",
    )
    angellist_url: str | None = Field(
        default=None,
        alias="angellistUrl",
        description="Canonical AngelList profile URL.",
    )
    annual_revenue: float | None = Field(
        default=None,
        alias="annualRevenue",
        description="Estimated annual revenue in USD. Minimum: 0.",
    )
    annual_revenue_display: str | None = Field(
        default=None,
        alias="annualRevenueDisplay",
        description="Human-readable estimated annual revenue.",
    )
    crunchbase_url: str | None = Field(
        default=None,
        alias="crunchbaseUrl",
        description="Canonical Crunchbase profile URL.",
    )
    domain: str | None = Field(default=None, description="Primary organization domain.")
    employee_growth: ApolloOrganizationsSearchEmployeeGrowth | None = Field(
        default=None,
        alias="employeeGrowth",
        description="Headcount change over trailing windows, in percent.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical Facebook page URL."
    )
    founded_year: int | None = Field(
        default=None,
        alias="foundedYear",
        description="Year the organization was founded.",
    )
    id: str | None = Field(description="Stable organization identifier.")
    image: str | None = Field(default=None, description="Organization logo URL.")
    languages: list[str] | None = Field(
        default=None, description="Languages the organization operates in."
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="Organization LinkedIn numeric id.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn company URL."
    )
    naics_codes: list[str] | None = Field(
        default=None, alias="naicsCodes", description="NAICS industry codes."
    )
    name: str | None = Field(description="Organization name.")
    ownership_chain_ids: list[str] | None = Field(
        default=None,
        alias="ownershipChainIds",
        description="Identifiers of the organizations in this organization's ownership chain.",
    )
    parent_organization_id: str | None = Field(
        default=None,
        alias="parentOrganizationId",
        description="Identifier of the organization that owns this one.",
    )
    parent_organization_name: str | None = Field(
        default=None,
        alias="parentOrganizationName",
        description="Name of the organization that owns this one.",
    )
    parent_organization_website_url: str | None = Field(
        default=None,
        alias="parentOrganizationWebsiteUrl",
        description="Website URL of the organization that owns this one.",
    )
    phone: str | None = Field(
        default=None, description="Organization phone number in international format."
    )
    publicly_traded_exchange: str | None = Field(
        default=None,
        alias="publiclyTradedExchange",
        description="Exchange the company lists on, such as nyse.",
    )
    publicly_traded_symbol: str | None = Field(
        default=None,
        alias="publiclyTradedSymbol",
        description="Stock ticker, for listed companies.",
    )
    retail_location_count: int | None = Field(
        default=None,
        alias="retailLocationCount",
        description="Number of retail locations Apollo records for the organization. Minimum: 0.",
    )
    sanitized_phone: str | None = Field(
        default=None,
        alias="sanitizedPhone",
        description="Organization phone number in international E.164 form, such as +14152985539.",
    )
    sic_codes: list[str] | None = Field(
        default=None, alias="sicCodes", description="SIC industry codes."
    )
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical X or Twitter profile URL.",
    )
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloOrganizationsSearchEmployeeGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent24m: float | None = Field(
        default=None, description="Percent change over the last twenty-four months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class ApolloPeopleSearchData(BaseModel):
    people: list[ApolloPeopleSearchPeople] = Field(
        description="People on this result page."
    )
    total: int = Field(description="Total matching people. Minimum: 0.")


class ApolloPeopleSearchPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    first_name: str | None = Field(alias="firstName", description="Person first name.")
    has_city: bool | None = Field(
        default=None,
        alias="hasCity",
        description="Whether city data is available through enrichment.",
    )
    has_country: bool | None = Field(
        default=None,
        alias="hasCountry",
        description="Whether country data is available through enrichment.",
    )
    has_direct_phone: bool | None = Field(
        default=None,
        alias="hasDirectPhone",
        description="Whether direct phone data is available through asynchronous enrichment.",
    )
    has_email: bool | None = Field(
        default=None,
        alias="hasEmail",
        description="Whether an email is available through enrichment.",
    )
    has_state: bool | None = Field(
        default=None,
        alias="hasState",
        description="Whether state or region data is available through enrichment.",
    )
    id: str | None = Field(description="Stable person identifier.")
    last_name_initial: str | None = Field(
        default=None,
        alias="lastNameInitial",
        description="Obfuscated last-name initial.",
    )
    last_refreshed_utc: float | None = Field(
        default=None,
        alias="lastRefreshedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    organization: ApolloPeopleSearchOrganization | None = Field(
        default=None, description="Availability summary for the current organization."
    )
    title: str | None = Field(default=None, description="Current job title.")


class ApolloPeopleSearchOrganization(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    has_city: bool | None = Field(
        default=None,
        alias="hasCity",
        description="Whether organization city data is available.",
    )
    has_country: bool | None = Field(
        default=None,
        alias="hasCountry",
        description="Whether organization country data is available.",
    )
    has_employee_count: bool | None = Field(
        default=None,
        alias="hasEmployeeCount",
        description="Whether organization employee-count data is available.",
    )
    has_industry: bool | None = Field(
        default=None,
        alias="hasIndustry",
        description="Whether industry data is available.",
    )
    has_phone: bool | None = Field(
        default=None,
        alias="hasPhone",
        description="Whether an organization phone is available.",
    )
    has_postal_code: bool | None = Field(
        default=None,
        alias="hasPostalCode",
        description="Whether organization postal-code data is available.",
    )
    has_revenue: bool | None = Field(
        default=None,
        alias="hasRevenue",
        description="Whether organization revenue data is available.",
    )
    has_state: bool | None = Field(
        default=None,
        alias="hasState",
        description="Whether organization state data is available.",
    )
    name: str | None = Field(default=None, description="Current organization name.")


class ApolloPersonEnrichData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Full address as one display string."
    )
    catch_all: bool | None = Field(
        default=None, alias="catchAll", description="Domain accepts all addresses."
    )
    catch_all_verdict: str | None = Field(
        default=None,
        alias="catchAllVerdict",
        description="Apollo's verdict on the catch-all email domain, such as allow.",
    )
    city: str | None = Field(default=None, description="City.")
    confidence: str | None = Field(
        default=None,
        description="Apollo match confidence for this person: high, medium or low.",
    )
    country: str | None = Field(default=None, description="Country.")
    departments: list[str] | None = Field(
        default=None, description="Current departments."
    )
    email: str | None = Field(default=None, description="Available work email.")
    email_status: str | None = Field(
        default=None,
        alias="emailStatus",
        description="Verification status of the work email.",
    )
    employment_history: list[ApolloPersonEnrichEmploymentHistory] | None = Field(
        default=None, alias="employmentHistory", description="Known employment history."
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical Facebook profile URL."
    )
    first_name: str | None = Field(alias="firstName", description="Person first name.")
    functions: list[str] | None = Field(
        default=None, description="Current business functions."
    )
    github_url: str | None = Field(
        default=None, alias="githubUrl", description="Canonical GitHub profile URL."
    )
    headline: str | None = Field(default=None, description="Professional headline.")
    id: str | None = Field(description="Stable person identifier.")
    image: str | None = Field(default=None, description="Profile image URL.")
    last_name: str | None = Field(alias="lastName", description="Person last name.")
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn profile URL."
    )
    name: str | None = Field(description="Full person name.")
    organization: ApolloPersonEnrichOrganization | None = Field(
        default=None, description="Current organization summary."
    )
    organization_id: str | None = Field(
        default=None,
        alias="organizationId",
        description="Identifier of the person's current organization.",
    )
    personal_emails: list[str] | None = Field(
        default=None,
        alias="personalEmails",
        description="Available personal email addresses, included automatically.",
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code."
    )
    seniority: str | None = Field(
        default=None, description="Current seniority classification."
    )
    state: str | None = Field(default=None, description="State or region.")
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Street address."
    )
    subdepartments: list[str] | None = Field(
        default=None, description="Current subdepartments."
    )
    time_zone: str | None = Field(
        default=None, alias="timeZone", description="IANA time-zone identifier."
    )
    title: str | None = Field(default=None, description="Current job title.")
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical X or Twitter profile URL.",
    )


class ApolloPersonEnrichEmploymentHistory(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    current: bool | None = Field(
        default=None, description="Whether this is a current role."
    )
    end_utc: float | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(description="Stable employment record identifier.")
    organization_id: str | None = Field(
        default=None, alias="organizationId", description="Organization identifier."
    )
    organization_name: str | None = Field(
        default=None, alias="organizationName", description="Organization name."
    )
    start_utc: float | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str | None = Field(default=None, description="Role title.")


class ApolloPersonEnrichOrganization(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alexa_ranking: int | None = Field(
        default=None,
        alias="alexaRanking",
        description="Alexa global traffic rank of the organization website.",
    )
    angellist_url: str | None = Field(
        default=None,
        alias="angellistUrl",
        description="Canonical AngelList profile URL.",
    )
    annual_revenue: float | None = Field(
        default=None,
        alias="annualRevenue",
        description="Estimated annual revenue in USD. Minimum: 0.",
    )
    annual_revenue_display: str | None = Field(
        default=None,
        alias="annualRevenueDisplay",
        description="Human-readable estimated annual revenue.",
    )
    city: str | None = Field(default=None, description="Headquarters city.")
    country: str | None = Field(default=None, description="Headquarters country.")
    crunchbase_url: str | None = Field(
        default=None,
        alias="crunchbaseUrl",
        description="Canonical Crunchbase profile URL.",
    )
    description: str | None = Field(default=None, description="Organization summary.")
    domain: str | None = Field(default=None, description="Primary organization domain.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated employee count. Minimum: 0.",
    )
    employee_growth: ApolloPersonEnrichEmployeeGrowth | None = Field(
        default=None,
        alias="employeeGrowth",
        description="Headcount change over trailing windows, in percent.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical Facebook page URL."
    )
    founded_year: int | None = Field(
        default=None,
        alias="foundedYear",
        description="Year the organization was founded.",
    )
    funding_events: list[ApolloPersonEnrichFundingEvent] | None = Field(
        default=None,
        alias="fundingEvents",
        description="Funding rounds Apollo records for the organization.",
    )
    id: str = Field(description="Stable organization identifier.")
    image: str | None = Field(default=None, description="Organization logo URL.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the organization."
    )
    industry: str | None = Field(default=None, description="Primary industry.")
    industry_tag_id: str | None = Field(
        default=None,
        alias="industryTagId",
        description="Apollo industry tag identifier of the primary industry, accepted by apollo.organizations_search industryIds.",
    )
    industry_tag_ids: ApolloPersonEnrichIndustryTagId | None = Field(
        default=None,
        alias="industryTagIds",
        description="Apollo industry tag identifier for each industry, keyed by industry name. The identifiers are accepted by apollo.organizations_search industryIds.",
    )
    keywords: list[str] | None = Field(
        default=None, description="Keywords associated with the organization."
    )
    languages: list[str] | None = Field(
        default=None, description="Languages the organization operates in."
    )
    latest_funding_detected_utc: float | None = Field(
        default=None,
        alias="latestFundingDetectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    latest_funding_stage: str | None = Field(
        default=None,
        alias="latestFundingStage",
        description="Latest disclosed funding stage.",
    )
    latest_funding_utc: float | None = Field(
        default=None,
        alias="latestFundingUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="Organization LinkedIn numeric id.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn company URL."
    )
    naics_codes: list[str] | None = Field(
        default=None, alias="naicsCodes", description="NAICS industry codes."
    )
    name: str = Field(description="Organization name.")
    org_chart_root_person_ids: list[str] | None = Field(
        default=None,
        alias="orgChartRootPersonIds",
        description="Apollo person identifiers at the top of the organization's org chart, accepted by apollo.person_enrich personId.",
    )
    parent_organization_id: str | None = Field(
        default=None,
        alias="parentOrganizationId",
        description="Identifier of the organization that owns this one.",
    )
    phone: str | None = Field(
        default=None, description="Organization phone number in international format."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Headquarters postal code."
    )
    publicly_traded_exchange: str | None = Field(
        default=None,
        alias="publiclyTradedExchange",
        description="Exchange the company lists on, such as nyse.",
    )
    publicly_traded_symbol: str | None = Field(
        default=None,
        alias="publiclyTradedSymbol",
        description="Stock ticker, for listed companies.",
    )
    raw_address: str | None = Field(
        default=None,
        alias="rawAddress",
        description="Headquarters address as one display string.",
    )
    retail_location_count: int | None = Field(
        default=None,
        alias="retailLocationCount",
        description="Number of retail locations Apollo records for the organization. Minimum: 0.",
    )
    sanitized_phone: str | None = Field(
        default=None,
        alias="sanitizedPhone",
        description="Organization phone number in international E.164 form, such as +14152985539.",
    )
    secondary_industries: list[str] | None = Field(
        default=None,
        alias="secondaryIndustries",
        description="Industries associated with the organization besides the primary industry.",
    )
    sic_codes: list[str] | None = Field(
        default=None, alias="sicCodes", description="SIC industry codes."
    )
    state: str | None = Field(default=None, description="Headquarters state or region.")
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Street address."
    )
    suborganization_count: int | None = Field(
        default=None,
        alias="suborganizationCount",
        description="Number of related organizations Apollo lists under this one. Minimum: 0.",
    )
    suborganizations: list[ApolloPersonEnrichSuborganization] | None = Field(
        default=None,
        description="Related organizations Apollo lists under this one, usually subsidiaries or acquisitions.",
    )
    technologies: list[ApolloPersonEnrichTechnologie] | None = Field(
        default=None,
        description="Technologies detected at the organization, with their category.",
    )
    technology_names: list[str] | None = Field(
        default=None,
        alias="technologyNames",
        description="Technologies detected at the organization.",
    )
    total_funding: float | None = Field(
        default=None,
        alias="totalFunding",
        description="Total disclosed funding in USD. Minimum: 0.",
    )
    total_funding_display: str | None = Field(
        default=None,
        alias="totalFundingDisplay",
        description="Human-readable total disclosed funding.",
    )
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical X or Twitter profile URL.",
    )
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloPersonEnrichEmployeeGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent24m: float | None = Field(
        default=None, description="Percent change over the last twenty-four months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class ApolloPersonEnrichFundingEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    amount_display: str | None = Field(
        default=None,
        alias="amountDisplay",
        description="Amount raised in this round as Apollo displays it, such as 100M.",
    )
    currency: str | None = Field(
        default=None, description="Currency symbol of the amount, such as $."
    )
    detected_utc: float | None = Field(
        default=None,
        alias="detectedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(default=None, description="Funding round identifier.")
    investors: str | None = Field(
        default=None,
        description="Investors in this round as one comma-separated string, exactly as Apollo returns it. A single investor name can itself contain a comma.",
    )
    news_url: str | None = Field(
        default=None, alias="newsUrl", description="Article reporting the round."
    )
    raised_utc: float | None = Field(
        default=None,
        alias="raisedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Funding round type, such as Series D."
    )


class ApolloPersonEnrichIndustryTagId(BaseModel):
    model_config = ConfigDict(extra="allow")


class ApolloPersonEnrichSuborganization(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country: str | None = Field(default=None, description="Headquarters country.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated employee count. Minimum: 0.",
    )
    id: str | None = Field(default=None, description="Organization identifier.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the organization."
    )
    name: str | None = Field(default=None, description="Organization name.")
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Canonical organization website URL.",
    )


class ApolloPersonEnrichTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")

    category: str | None = Field(default=None, description="Technology category.")
    id: str | None = Field(
        default=None,
        description="Technology identifier, accepted by the technologySlug filters of apollo.organizations_search and apollo.people_search.",
    )
    name: str | None = Field(default=None, description="Technology name.")


class ApolloNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def organization(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationInput],
    ) -> RunResult[ApolloOrganizationData]:
        """Apollo Organization

        Get a complete organization profile by ID including company, industry,
        employee, monthly headcount flow, revenue, funding rounds, ownership,
        location, and technology data.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization(organizationId="5fc8de5191bd9400bfc52051")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization", dict(input), options
        )
        return RunResult[ApolloOrganizationData].model_validate(raw)

    def organization_enrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationEnrichInput],
    ) -> RunResult[ApolloOrganizationEnrichData]:
        """Apollo Organization Enrichment

        Enrich an organization by domain, optionally with its LinkedIn URL, website,
        or name, with company profile, industry, headcount growth, department
        headcount, revenue, funding rounds, location, and technology data.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization_enrich(domain="apollo.io")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization_enrich", dict(input), options
        )
        return RunResult[ApolloOrganizationEnrichData].model_validate(raw)

    def organization_jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationJobsInput],
    ) -> RunResult[ApolloOrganizationJobsData]:
        """Apollo Organization Jobs

        Get current job postings for an organization by ID with title, location,
        source URL, and timestamps, one page at a time.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization_jobs(organizationId="5e66b6381e05b4008c8331b8")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization_jobs", dict(input), options
        )
        return RunResult[ApolloOrganizationJobsData].model_validate(raw)

    def organization_news(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationNewsInput],
    ) -> RunResult[ApolloOrganizationNewsData]:
        """Apollo Organization News

        Search news related to one or more organizations, optionally by category and
        publish date range, with article details, categories, and pagination totals.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization_news(limit=3, organizationIds=["5e66b6381e05b4008c8331b8"], page=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization_news", dict(input), options
        )
        return RunResult[ApolloOrganizationNewsData].model_validate(raw)

    def organizations_bulk_enrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationsBulkEnrichInput],
    ) -> RunResult[ApolloOrganizationsBulkEnrichData]:
        """Apollo Bulk Organization Enrichment

        Enrich up to 10 organization domains in one request with normalized company
        profile, industry, employee, revenue, and location data. Priced per request
        rather than per domain, so a full batch of 10 costs the same as a batch of
        1. Results are positionally aligned with the domains you send, and a domain
        with no match returns null in its slot.

        Price: $0.06 per request.

        Example:
            res = client.apollo.organizations_bulk_enrich(domains=["apollo.io", "openai.com"])
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organizations_bulk_enrich", dict(input), options
        )
        return RunResult[ApolloOrganizationsBulkEnrichData].model_validate(raw)

    def organizations_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationsSearchInput],
    ) -> RunResult[ApolloOrganizationsSearchData]:
        """Apollo Organization Search

        Search organizations by location, employee range, industry, keywords,
        domain, name, revenue, funding, technology, hiring activity, headcount
        growth, or lookalike seeds, with normalized company records and pagination
        totals.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organizations_search(keywords="Apollo", limit=3, page=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organizations_search", dict(input), options
        )
        return RunResult[ApolloOrganizationsSearchData].model_validate(raw)

    def people_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloPeopleSearchInput],
    ) -> RunResult[ApolloPeopleSearchData]:
        """Apollo People Search

        Search people by title, seniority, name, location, employer domain or id,
        email status, and employer revenue, technology, hiring, and headcount
        growth, with normalized profile summaries.

        Price: $0.01 per request.

        Example:
            res = client.apollo.people_search(limit=3, page=1, titles=["CEO"])
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.people_search", dict(input), options
        )
        return RunResult[ApolloPeopleSearchData].model_validate(raw)

    def person_enrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloPersonEnrichInput],
    ) -> RunResult[ApolloPersonEnrichData]:
        """Apollo Person Enrichment

        Enrich a person by email, email hash, LinkedIn URL, Apollo person id, or
        name and organization with contact, role, location, and company data.

        Price: $0.012 per request.

        Example:
            res = client.apollo.person_enrich(domain="apollo.io", firstName="Tim", lastName="Zheng")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.person_enrich", dict(input), options
        )
        return RunResult[ApolloPersonEnrichData].model_validate(raw)


class AsyncApolloNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def organization(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationInput],
    ) -> RunResult[ApolloOrganizationData]:
        """Apollo Organization

        Get a complete organization profile by ID including company, industry,
        employee, monthly headcount flow, revenue, funding rounds, ownership,
        location, and technology data.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization(organizationId="5fc8de5191bd9400bfc52051")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization", dict(input), options
        )
        return RunResult[ApolloOrganizationData].model_validate(raw)

    async def organization_enrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationEnrichInput],
    ) -> RunResult[ApolloOrganizationEnrichData]:
        """Apollo Organization Enrichment

        Enrich an organization by domain, optionally with its LinkedIn URL, website,
        or name, with company profile, industry, headcount growth, department
        headcount, revenue, funding rounds, location, and technology data.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization_enrich(domain="apollo.io")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization_enrich", dict(input), options
        )
        return RunResult[ApolloOrganizationEnrichData].model_validate(raw)

    async def organization_jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationJobsInput],
    ) -> RunResult[ApolloOrganizationJobsData]:
        """Apollo Organization Jobs

        Get current job postings for an organization by ID with title, location,
        source URL, and timestamps, one page at a time.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization_jobs(organizationId="5e66b6381e05b4008c8331b8")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization_jobs", dict(input), options
        )
        return RunResult[ApolloOrganizationJobsData].model_validate(raw)

    async def organization_news(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationNewsInput],
    ) -> RunResult[ApolloOrganizationNewsData]:
        """Apollo Organization News

        Search news related to one or more organizations, optionally by category and
        publish date range, with article details, categories, and pagination totals.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organization_news(limit=3, organizationIds=["5e66b6381e05b4008c8331b8"], page=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organization_news", dict(input), options
        )
        return RunResult[ApolloOrganizationNewsData].model_validate(raw)

    async def organizations_bulk_enrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationsBulkEnrichInput],
    ) -> RunResult[ApolloOrganizationsBulkEnrichData]:
        """Apollo Bulk Organization Enrichment

        Enrich up to 10 organization domains in one request with normalized company
        profile, industry, employee, revenue, and location data. Priced per request
        rather than per domain, so a full batch of 10 costs the same as a batch of
        1. Results are positionally aligned with the domains you send, and a domain
        with no match returns null in its slot.

        Price: $0.06 per request.

        Example:
            res = client.apollo.organizations_bulk_enrich(domains=["apollo.io", "openai.com"])
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organizations_bulk_enrich", dict(input), options
        )
        return RunResult[ApolloOrganizationsBulkEnrichData].model_validate(raw)

    async def organizations_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloOrganizationsSearchInput],
    ) -> RunResult[ApolloOrganizationsSearchData]:
        """Apollo Organization Search

        Search organizations by location, employee range, industry, keywords,
        domain, name, revenue, funding, technology, hiring activity, headcount
        growth, or lookalike seeds, with normalized company records and pagination
        totals.

        Price: $0.012 per request.

        Example:
            res = client.apollo.organizations_search(keywords="Apollo", limit=3, page=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.organizations_search", dict(input), options
        )
        return RunResult[ApolloOrganizationsSearchData].model_validate(raw)

    async def people_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloPeopleSearchInput],
    ) -> RunResult[ApolloPeopleSearchData]:
        """Apollo People Search

        Search people by title, seniority, name, location, employer domain or id,
        email status, and employer revenue, technology, hiring, and headcount
        growth, with normalized profile summaries.

        Price: $0.01 per request.

        Example:
            res = client.apollo.people_search(limit=3, page=1, titles=["CEO"])
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.people_search", dict(input), options
        )
        return RunResult[ApolloPeopleSearchData].model_validate(raw)

    async def person_enrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ApolloPersonEnrichInput],
    ) -> RunResult[ApolloPersonEnrichData]:
        """Apollo Person Enrichment

        Enrich a person by email, email hash, LinkedIn URL, Apollo person id, or
        name and organization with contact, role, location, and company data.

        Price: $0.012 per request.

        Example:
            res = client.apollo.person_enrich(domain="apollo.io", firstName="Tim", lastName="Zheng")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "apollo.person_enrich", dict(input), options
        )
        return RunResult[ApolloPersonEnrichData].model_validate(raw)
