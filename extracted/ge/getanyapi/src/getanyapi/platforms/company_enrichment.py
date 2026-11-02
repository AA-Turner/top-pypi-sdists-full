# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the company_enrichment platform."""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class CompanyEnrichmentCrustdataInput(TypedDict, total=False):
    """Input for Company Enrichment - Crustdata."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: NotRequired[str]
    companyId: NotRequired[Any]
    companyLinkedinUrl: NotRequired[str]
    companyName: NotRequired[str]
    exactMatch: NotRequired[bool]
    fields: NotRequired[Any]
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanyEnrichmentDatalegionInput(TypedDict, total=False):
    """Input for Company Enrichment - Data Legion."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: NotRequired[str]
    """Company website domain, e.g. hubspot.com. The strongest identifier. Send either domain or name, not both."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    minConfidence: NotRequired[Literal["high", "moderate", "low"]]
    """Lowest match confidence that still counts as found. Omit it for Data Legion's default."""
    name: NotRequired[str]
    """Company name, for when you have no domain. A domain matches more reliably."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    required: NotRequired[str]
    """Fields a match must have, as a Data Legion expression over its snake_case field names combined with AND, OR and parentheses, e.g. linkedin_url AND founded. A match without them counts as not found."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanyEnrichmentLushaInput(TypedDict, total=False):
    """Input for Company Enrichment - Lusha."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    company: NotRequired[str]
    """Company name to look up when you have no domain."""
    companyId: NotRequired[str]
    """Lusha's own company identifier, as returned by this SKU's companyId output."""
    domain: NotRequired[str]
    """Company domain, e.g. posthog.com. Send the bare domain, without a scheme or www."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanyEnrichmentPeopledatalabsInput(TypedDict, total=False):
    """Input for Company Enrichment - People Data Labs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    dataInclude: NotRequired[str]
    """Comma-separated People Data Labs fields to include, or a leading - list to exclude. Projection changes the payload only; it does not reduce what the call costs."""
    domain: NotRequired[str]
    """Company website domain, e.g. posthog.com. The strongest identifier."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeIfMatched: NotRequired[bool]
    """Report which of the sent identifiers actually matched."""
    minLikelihood: NotRequired[int]
    """Minimum People Data Labs likelihood score a match must reach to count as found. Range: 1 to 10."""
    name: NotRequired[str]
    """Company name, for when you have no domain."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    required: NotRequired[str]
    """People Data Labs boolean expression over top-level fields that a match must satisfy, e.g. website and industry."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    titlecase: NotRequired[bool]
    """Return text in title case instead of People Data Labs' lowercase default."""


class CompanyEnrichmentProspeoInput(TypedDict, total=False):
    """Input for Company Enrichment - Prospeo."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyId: NotRequired[str]
    """Prospeo's own company identifier, as returned by this SKU's companyId output."""
    companyLinkedinUrl: NotRequired[str]
    """Company LinkedIn page URL."""
    companyName: NotRequired[str]
    """Company name, for when you have no domain."""
    companyWebsite: NotRequired[str]
    """Company domain, e.g. stripe.com. The most reliable identifier."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanyEnrichmentCrustdataData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    acquisition_status: str | None = Field(
        default=None,
        alias="acquisitionStatus",
        description="Acquisition status, when the company has been acquired.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata identifier for the company, accepted back as the companyId input.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Company type, e.g. Privately Held or Public Company.",
    )
    crunchbase_categories: list[str] | None = Field(
        default=None,
        alias="crunchbaseCategories",
        description="Crunchbase category tags, followed by the broader category groups they belong to.",
    )
    description: str | None = Field(
        default=None, description="Company description from its LinkedIn page."
    )
    domain: str | None = Field(
        description="Primary website domain, or null when the upstream holds none for this company."
    )
    domains: list[str] | None = Field(
        default=None, description="All domains associated with the company."
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Latest observed employee count.",
    )
    employee_growth_absolute: (
        CompanyEnrichmentCrustdataEmployeeGrowthAbsolute | None
    ) = Field(
        default=None,
        alias="employeeGrowthAbsolute",
        description="Net headcount change over trailing windows.",
    )
    employee_growth_percent: CompanyEnrichmentCrustdataEmployeeGrowthPercent | None = (
        Field(
            default=None,
            alias="employeeGrowthPercent",
            description="Percent headcount change over trailing windows.",
        )
    )
    employee_range: str | None = Field(
        default=None,
        alias="employeeRange",
        description="Employee count band, e.g. 51-200.",
    )
    estimated_revenue_higher_usd: int | None = Field(
        default=None,
        alias="estimatedRevenueHigherUsd",
        description="Upper bound of estimated annual revenue in USD.",
    )
    estimated_revenue_lower_usd: int | None = Field(
        default=None,
        alias="estimatedRevenueLowerUsd",
        description="Lower bound of estimated annual revenue in USD.",
    )
    fiscal_year_end: str | None = Field(
        default=None, alias="fiscalYearEnd", description="Fiscal year end."
    )
    founded_utc: int | None = Field(
        default=None,
        alias="foundedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Founding date of the company.",
    )
    founded_year: int | None = Field(
        default=None, alias="foundedYear", description="Year the company was founded."
    )
    headcount_by_function_timeseries: Any | None = Field(
        default=None,
        alias="headcountByFunctionTimeseries",
        description="Headcount history broken down by region and by job function. Untyped passthrough: the whole nested structure ships exactly as Crustdata returns it, including its raw grouping keys (GEO_REGION, CURRENT_FUNCTION) and its string observation dates rather than epoch seconds, because the shape cannot be expressed in the canonical field grammar.",
    )
    headcount_by_region: CompanyEnrichmentCrustdataHeadcountByRegion | None = Field(
        default=None,
        alias="headcountByRegion",
        description="Employee count per region, keyed by LinkedIn region name.",
    )
    headcount_by_region_percent: (
        CompanyEnrichmentCrustdataHeadcountByRegionPercent | None
    ) = Field(
        default=None,
        alias="headcountByRegionPercent",
        description="Share of employees per region as a percent, keyed by LinkedIn region name.",
    )
    headcount_by_role: CompanyEnrichmentCrustdataHeadcountByRole | None = Field(
        default=None,
        alias="headcountByRole",
        description="Employee count per job function, keyed by LinkedIn function name.",
    )
    headcount_by_role_percent: (
        CompanyEnrichmentCrustdataHeadcountByRolePercent | None
    ) = Field(
        default=None,
        alias="headcountByRolePercent",
        description="Share of employees per job function as a percent, keyed by LinkedIn function name.",
    )
    headcount_by_role_six_months_growth_percent: Any | None = Field(
        default=None,
        alias="headcountByRoleSixMonthsGrowthPercent",
        description="Six-month percent headcount change per job function, exactly as Crustdata returns it. Untyped passthrough: the structure ships verbatim and is not validated.",
    )
    headcount_by_role_yoy_growth_percent: Any | None = Field(
        default=None,
        alias="headcountByRoleYoyGrowthPercent",
        description="Year-over-year percent headcount change per job function, exactly as Crustdata returns it. Untyped passthrough: the structure ships verbatim and is not validated.",
    )
    headcount_by_skill: CompanyEnrichmentCrustdataHeadcountBySkill | None = Field(
        default=None,
        alias="headcountBySkill",
        description="Employee count per listed skill, keyed by skill name.",
    )
    headcount_by_skill_percent: (
        CompanyEnrichmentCrustdataHeadcountBySkillPercent | None
    ) = Field(
        default=None,
        alias="headcountBySkillPercent",
        description="Share of employees per listed skill as a percent, keyed by skill name.",
    )
    headcount_timeseries: list[CompanyEnrichmentCrustdataHeadcountTimeserie] | None = (
        Field(
            default=None,
            alias="headcountTimeseries",
            description="Historical employee-count observations, oldest first.",
        )
    )
    hq_country: str | None = Field(
        default=None, alias="hqCountry", description="Country of the headquarters."
    )
    hq_state: str | None = Field(
        default=None,
        alias="hqState",
        description="State or province of the headquarters.",
    )
    hq_street_address: str | None = Field(
        default=None,
        alias="hqStreetAddress",
        description="Headquarters street address. Crustdata returns the same string as location for most companies.",
    )
    image: str | None = Field(
        default=None,
        description="Company logo URL. Crustdata's cached copy, which does not expire.",
    )
    industries: list[str] | None = Field(
        default=None, description="All LinkedIn industries listed for the company."
    )
    industry: str | None = Field(default=None, description="Primary LinkedIn industry.")
    ipo_utc: int | None = Field(
        default=None,
        alias="ipoUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Date the company went public.",
    )
    largest_headcount_country: str | None = Field(
        default=None,
        alias="largestHeadcountCountry",
        description="Country holding the largest share of employees.",
    )
    linkedin_company_id: str | None = Field(
        default=None,
        alias="linkedinCompanyId",
        description="LinkedIn's own numeric identifier for the company page.",
    )
    linkedin_profile_name: str | None = Field(
        default=None,
        alias="linkedinProfileName",
        description="Company name as it appears on the LinkedIn page. Usually the same value as name; Crustdata returns both.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="LinkedIn company page URL."
    )
    location: str | None = Field(default=None, description="Headquarters location.")
    naics: CompanyEnrichmentCrustdataNaic | None = Field(
        default=None, description="Primary NAICS industry classification."
    )
    name: str | None = Field(default=None, description="Company name.")
    sic_codes: list[CompanyEnrichmentCrustdataSicCode] | None = Field(
        default=None,
        alias="sicCodes",
        description="SIC industry classifications assigned to the company.",
    )
    specialities: list[str] | None = Field(
        default=None, description="Speciality tags the company lists on LinkedIn."
    )
    twitter_url: str | None = Field(
        default=None, alias="twitterUrl", description="X (Twitter) profile URL."
    )
    website: str | None = Field(default=None, description="Company website URL.")


class CompanyEnrichmentCrustdataEmployeeGrowthAbsolute(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    mom: int | None = Field(default=None, description="Change over the last month.")
    qoq: int | None = Field(default=None, description="Change over the last quarter.")
    six_months: int | None = Field(
        default=None, alias="sixMonths", description="Change over the last six months."
    )
    two_years: int | None = Field(
        default=None, alias="twoYears", description="Change over the last two years."
    )
    yoy: int | None = Field(
        default=None, description="Change over the last twelve months."
    )


class CompanyEnrichmentCrustdataEmployeeGrowthPercent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    mom: float | None = Field(default=None, description="Change over the last month.")
    qoq: float | None = Field(default=None, description="Change over the last quarter.")
    six_months: float | None = Field(
        default=None, alias="sixMonths", description="Change over the last six months."
    )
    two_years: float | None = Field(
        default=None, alias="twoYears", description="Change over the last two years."
    )
    yoy: float | None = Field(
        default=None, description="Change over the last twelve months."
    )


class CompanyEnrichmentCrustdataHeadcountByRegion(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentCrustdataHeadcountByRegionPercent(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentCrustdataHeadcountByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentCrustdataHeadcountByRolePercent(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentCrustdataHeadcountBySkill(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentCrustdataHeadcountBySkillPercent(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentCrustdataHeadcountTimeserie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    date_utc: int | None = Field(
        default=None,
        alias="dateUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Observation date.",
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Employee count observed on that date.",
    )


class CompanyEnrichmentCrustdataNaic(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str | None = Field(default=None, description="Primary NAICS code.")
    industry: str | None = Field(default=None, description="NAICS industry name.")
    industry_group: str | None = Field(
        default=None, alias="industryGroup", description="NAICS industry group name."
    )
    sector: str | None = Field(default=None, description="NAICS sector name.")
    sub_sector: str | None = Field(
        default=None, alias="subSector", description="NAICS sub-sector name."
    )
    year: int | None = Field(
        default=None, description="NAICS revision year the code belongs to."
    )


class CompanyEnrichmentCrustdataSicCode(BaseModel):
    model_config = ConfigDict(extra="allow")

    code: str | None = Field(default=None, description="SIC code.")
    industry: str | None = Field(default=None, description="SIC industry name.")
    year: int | None = Field(
        default=None, description="SIC revision year the code belongs to."
    )


class CompanyEnrichmentDatalegionData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    average_tenure_months: float | None = Field(
        default=None,
        alias="averageTenureMonths",
        description="Average tenure of current employees, in months.",
    )
    dataset_version: str | None = Field(
        default=None,
        alias="datasetVersion",
        description="Data Legion dataset build the record came from.",
    )
    departures: CompanyEnrichmentDatalegionDeparture | None = Field(
        default=None,
        description="Departures over the trailing 1, 3, 6 and 12 months, keyed 1m, 3m, 6m and 12m.",
    )
    domains: list[str] | None = Field(
        default=None,
        description="Every website domain Data Legion links to the company, the primary one included.",
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Employees Data Legion currently counts from the people profiles it holds, usually below the LinkedIn figure.",
    )
    employee_count_by_education: (
        CompanyEnrichmentDatalegionEmployeeCountByEducation | None
    ) = Field(
        default=None,
        alias="employeeCountByEducation",
        description="Current employees per highest degree, e.g. bachelors, masters, doctorate.",
    )
    employee_count_by_expense_category: (
        CompanyEnrichmentDatalegionEmployeeCountByExpenseCategory | None
    ) = Field(
        default=None,
        alias="employeeCountByExpenseCategory",
        description="Current employees per expense category, e.g. research_and_development, sales_and_marketing.",
    )
    employee_count_by_function: (
        CompanyEnrichmentDatalegionEmployeeCountByFunction | None
    ) = Field(
        default=None,
        alias="employeeCountByFunction",
        description="Current employees per job function, e.g. engineering, sales, product.",
    )
    employee_count_by_month: (
        list[CompanyEnrichmentDatalegionEmployeeCountByMonth] | None
    ) = Field(
        default=None,
        alias="employeeCountByMonth",
        description="Monthly headcount history, oldest month first.",
    )
    employee_count_by_seniority: (
        CompanyEnrichmentDatalegionEmployeeCountBySeniority | None
    ) = Field(
        default=None,
        alias="employeeCountBySeniority",
        description="Current employees per seniority level, e.g. c_level, director, manager, senior.",
    )
    employee_count_by_tenure: (
        CompanyEnrichmentDatalegionEmployeeCountByTenure | None
    ) = Field(
        default=None,
        alias="employeeCountByTenure",
        description="Current employees per tenure band, e.g. <1yr, 1-2yr, 2-5yr.",
    )
    employee_growth_rate: CompanyEnrichmentDatalegionEmployeeGrowthRate | None = Field(
        default=None,
        alias="employeeGrowthRate",
        description="Headcount growth rate as a fraction over the trailing 1, 3, 6 and 12 months, keyed 1m, 3m, 6m and 12m.",
    )
    employee_turnover_rate: CompanyEnrichmentDatalegionEmployeeTurnoverRate | None = (
        Field(
            default=None,
            alias="employeeTurnoverRate",
            description="Turnover rate as a fraction over the trailing 1, 3, 6 and 12 months, keyed 1m, 3m, 6m and 12m.",
        )
    )
    founded: int | None = Field(
        default=None, description="Year the company was founded."
    )
    growth_rate_by_expense_category: (
        CompanyEnrichmentDatalegionGrowthRateByExpenseCategory | None
    ) = Field(
        default=None,
        alias="growthRateByExpenseCategory",
        description="Headcount growth rate per expense category, each keyed 1m, 3m, 6m and 12m.",
    )
    growth_rate_by_function: CompanyEnrichmentDatalegionGrowthRateByFunction | None = (
        Field(
            default=None,
            alias="growthRateByFunction",
            description="Headcount growth rate per job function, each keyed 1m, 3m, 6m and 12m.",
        )
    )
    growth_rate_by_seniority: (
        CompanyEnrichmentDatalegionGrowthRateBySeniority | None
    ) = Field(
        default=None,
        alias="growthRateBySeniority",
        description="Headcount growth rate per seniority level, each keyed 1m, 3m, 6m and 12m.",
    )
    headline: str | None = Field(
        default=None, description="One-line company tagline, as the company writes it."
    )
    industry: str | None = Field(
        default=None,
        description="Company industry, lowercase, e.g. software development.",
    )
    last_seen_utc: int | None = Field(
        default=None,
        alias="lastSeenUtc",
        description="UTC epoch timestamp in seconds (Unix time) of the month Data Legion last saw the company, at the first of that month. Multiply by 1000 for a JS Date in milliseconds.",
    )
    legion_id: str | None = Field(
        default=None, alias="legionId", description="Data Legion persistent company id."
    )
    linkedin_employee_count: int | None = Field(
        default=None,
        alias="linkedinEmployeeCount",
        description="Employee count the company's LinkedIn page states.",
    )
    linkedin_followers: int | None = Field(
        default=None, alias="linkedinFollowers", description="LinkedIn follower count."
    )
    linkedin_id: str | None = Field(
        default=None, alias="linkedinId", description="Company LinkedIn numeric id."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Company LinkedIn page URL."
    )
    locations: list[CompanyEnrichmentDatalegionLocation] | None = Field(
        default=None, description="Office locations, the headquarters marked isPrimary."
    )
    match_confidence: str | None = Field(
        default=None,
        alias="matchConfidence",
        description="How sure the match is: high, moderate or low.",
    )
    match_type: str | None = Field(
        default=None,
        alias="matchType",
        description="How the identifier matched, e.g. exact.",
    )
    matched_on: list[str] | None = Field(
        default=None,
        alias="matchedOn",
        description="Identifiers the match was made on, e.g. domain or name.",
    )
    name: str | None = Field(description="Company name as Data Legion displays it.")
    name_normalized: str | None = Field(
        default=None,
        alias="nameNormalized",
        description="Lowercase normalized company name, the form Data Legion matches on.",
    )
    new_hires: CompanyEnrichmentDatalegionNewHire | None = Field(
        default=None,
        alias="newHires",
        description="Hires over the trailing 1, 3, 6 and 12 months, keyed 1m, 3m, 6m and 12m.",
    )
    num_sources: int | None = Field(
        default=None,
        alias="numSources",
        description="Number of sources Data Legion merged into this record.",
    )
    profiles: list[CompanyEnrichmentDatalegionProfile] | None = Field(
        default=None,
        description="Social and directory profiles Data Legion links to the company.",
    )
    size: str | None = Field(
        default=None, description="Employee headcount band, e.g. 51-200."
    )
    summary: str | None = Field(
        default=None, description="Long company description, as the company writes it."
    )
    tickers: list[CompanyEnrichmentDatalegionTicker] | None = Field(
        default=None,
        description="Stock tickers the company trades under. Empty for a private company.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Ownership type, e.g. private, public."
    )
    website: str | None = Field(
        default=None, description="Primary company website domain, e.g. hubspot.com."
    )


class CompanyEnrichmentDatalegionDeparture(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionEmployeeCountByEducation(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionEmployeeCountByExpenseCategory(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionEmployeeCountByFunction(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionEmployeeCountByMonth(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int | None = Field(default=None, description="Employees counted that month.")
    departures: int | None = Field(
        default=None, description="Employees who left that month."
    )
    growth_rate: float | None = Field(
        default=None,
        alias="growthRate",
        description="Change in headcount from the month before, as a fraction.",
    )
    hires: int | None = Field(
        default=None, description="Employees who joined that month."
    )
    month: str = Field(description="Calendar month as YYYY-MM.")
    net_change: int | None = Field(
        default=None,
        alias="netChange",
        description="Change in headcount from the month before.",
    )


class CompanyEnrichmentDatalegionEmployeeCountBySeniority(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionEmployeeCountByTenure(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionEmployeeGrowthRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionEmployeeTurnoverRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionGrowthRateByExpenseCategory(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionGrowthRateByFunction(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionGrowthRateBySeniority(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address_line2: str | None = Field(
        default=None, alias="addressLine2", description="Second line of the address."
    )
    continent: str | None = Field(default=None, description="Continent.")
    country: str | None = Field(default=None, description="Country.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code, e.g. US.",
    )
    geo: str | None = Field(default=None, description='Coordinates as "lat,lon".')
    is_current: bool | None = Field(
        default=None,
        alias="isCurrent",
        description="True while the office is still in use.",
    )
    is_primary: bool | None = Field(
        default=None, alias="isPrimary", description="True for the headquarters."
    )
    last_seen_utc: int | None = Field(
        default=None,
        alias="lastSeenUtc",
        description="UTC epoch timestamp in seconds (Unix time) Data Legion last saw this location. Multiply by 1000 for a JS Date in milliseconds.",
    )
    locality: str | None = Field(default=None, description="City.")
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code."
    )
    region: str | None = Field(default=None, description="State or region.")
    region_code: str | None = Field(
        default=None,
        alias="regionCode",
        description="ISO 3166-2 region code, e.g. US-MA.",
    )
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Street address."
    )


class CompanyEnrichmentDatalegionNewHire(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentDatalegionProfile(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    network: str = Field(
        description="Network the profile is on, e.g. linkedin, facebook, crunchbase."
    )
    profile_id: str | None = Field(
        default=None,
        alias="profileId",
        description="Numeric or opaque id on that network.",
    )
    url: str | None = Field(default=None, description="Profile URL.")
    username: str | None = Field(default=None, description="Handle on that network.")


class CompanyEnrichmentDatalegionTicker(BaseModel):
    model_config = ConfigDict(extra="allow")

    exchange: str | None = Field(
        default=None, description="Exchange the ticker lists on, e.g. NYSE."
    )
    symbol: str = Field(description="Ticker symbol, e.g. HUBS.")


class CompanyEnrichmentLushaData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Headquarters address as one display string."
    )
    alternative_domains: list[str] | None = Field(
        default=None,
        alias="alternativeDomains",
        description="Other domains the company owns.",
    )
    alternative_name: str | None = Field(
        default=None,
        alias="alternativeName",
        description="Alternative name Lusha holds for the company.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Lusha's own company identifier. Send it back as this SKU's companyId input.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Ownership type, e.g. Private Company.",
    )
    description: str | None = Field(default=None, description="Company description.")
    domain: str | None = Field(default=None, description="Primary company domain.")
    email_domain: str | None = Field(
        default=None,
        alias="emailDomain",
        description="Domain the company's work email addresses use.",
    )
    employee_range: str | None = Field(
        default=None,
        alias="employeeRange",
        description="Employee headcount band as Lusha bands it, e.g. 51 - 200.",
    )
    employees_on_linkedin: int | None = Field(
        default=None,
        alias="employeesOnLinkedin",
        description="Employees LinkedIn shows for the company.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Company Facebook page URL."
    )
    founded: int | None = Field(
        default=None, description="Year the company was founded."
    )
    fqdn: str | None = Field(
        default=None, description="Fully qualified host for the company website."
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    linkedin_followers: int | None = Field(
        default=None, alias="linkedinFollowers", description="LinkedIn follower count."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Company LinkedIn page URL."
    )
    location: CompanyEnrichmentLushaLocation | None = Field(
        default=None, description="Headquarters location."
    )
    main_industry: str | None = Field(
        default=None, alias="mainIndustry", description="Top-level industry."
    )
    naics_codes: list[CompanyEnrichmentLushaNaicsCode] | None = Field(
        default=None,
        alias="naicsCodes",
        description="NAICS classification codes for the company.",
    )
    name: str | None = Field(description="Company name.")
    offices: list[CompanyEnrichmentLushaOffice] | None = Field(
        default=None, description="Every office location Lusha holds for the company."
    )
    popularity_tier: int | None = Field(
        default=None,
        alias="popularityTier",
        description="Lusha's popularity tier for the company, 1 being the most prominent.",
    )
    record_id: str | None = Field(
        default=None,
        alias="recordId",
        description="Lusha's internal record id for the company row.",
    )
    revenue_range: list[int] | None = Field(
        default=None,
        alias="revenueRange",
        description="Annual revenue band in USD as [min, max].",
    )
    sic_codes: list[CompanyEnrichmentLushaSicCode] | None = Field(
        default=None,
        alias="sicCodes",
        description="SIC classification codes for the company.",
    )
    specialities: list[str] | None = Field(
        default=None, description="Specialities the company lists for itself."
    )
    sub_industry: str | None = Field(
        default=None, alias="subIndustry", description="Sub-industry."
    )
    website: str | None = Field(default=None, description="Company website URL.")
    x_url: str | None = Field(
        default=None, alias="xUrl", description="Company X (Twitter) profile URL."
    )


class CompanyEnrichmentLushaLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City.")
    continent: str | None = Field(default=None, description="Continent name.")
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    full_location: str | None = Field(
        default=None,
        alias="fullLocation",
        description="Location as one display string.",
    )
    state: str | None = Field(default=None, description="State or region.")
    state_code: str | None = Field(
        default=None, alias="stateCode", description="State or region code."
    )


class CompanyEnrichmentLushaNaicsCode(BaseModel):
    model_config = ConfigDict(extra="allow")

    code: str | None = Field(description="NAICS code.")
    description: str | None = Field(
        default=None, description="What the NAICS code covers."
    )


class CompanyEnrichmentLushaOffice(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City.")
    continent: str | None = Field(default=None, description="Continent name.")
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    full_location: str | None = Field(
        default=None,
        alias="fullLocation",
        description="Location as one display string.",
    )
    state: str | None = Field(default=None, description="State or region.")
    state_code: str | None = Field(
        default=None, alias="stateCode", description="State or region code."
    )


class CompanyEnrichmentLushaSicCode(BaseModel):
    model_config = ConfigDict(extra="allow")

    code: str | None = Field(description="SIC code.")
    description: str | None = Field(
        default=None, description="What the SIC code covers."
    )


class CompanyEnrichmentPeopledatalabsData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    affiliated_entities: list[str | None] | None = Field(
        default=None,
        alias="affiliatedEntities",
        description="People Data Labs company ids of affiliated entities.",
    )
    affiliated_profiles: list[str] | None = Field(
        default=None,
        alias="affiliatedProfiles",
        description="People Data Labs company ids of affiliated profiles.",
    )
    all_subsidiaries: list[str] | None = Field(
        default=None,
        alias="allSubsidiaries",
        description="People Data Labs company ids of every subsidiary, at any depth.",
    )
    alternative_domains: list[str] | None = Field(
        default=None,
        alias="alternativeDomains",
        description="Other domains the company owns.",
    )
    alternative_names: list[str] | None = Field(
        default=None,
        alias="alternativeNames",
        description="Other names the company trades under.",
    )
    average_employee_tenure: float | None = Field(
        default=None,
        alias="averageEmployeeTenure",
        description="Average employee tenure in years.",
    )
    average_tenure_by_level: (
        CompanyEnrichmentPeopledatalabsAverageTenureByLevel | None
    ) = Field(
        default=None,
        alias="averageTenureByLevel",
        description="Average tenure in years, keyed by seniority level.",
    )
    average_tenure_by_role: (
        CompanyEnrichmentPeopledatalabsAverageTenureByRole | None
    ) = Field(
        default=None,
        alias="averageTenureByRole",
        description="Average tenure in years, keyed by role.",
    )
    dataset_version: str | None = Field(
        default=None,
        alias="datasetVersion",
        description="Version of the People Data Labs dataset this record came from.",
    )
    direct_subsidiaries: list[str] | None = Field(
        default=None,
        alias="directSubsidiaries",
        description="People Data Labs company ids of direct subsidiaries.",
    )
    employee_churn_rate: CompanyEnrichmentPeopledatalabsEmployeeChurnRate | None = (
        Field(
            default=None,
            alias="employeeChurnRate",
            description="Churn rate keyed by window, e.g. 12_month.",
        )
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Employees People Data Labs currently counts.",
    )
    employee_count_by_class: (
        CompanyEnrichmentPeopledatalabsEmployeeCountByClas | None
    ) = Field(
        default=None,
        alias="employeeCountByClass",
        description="Headcount keyed by job class.",
    )
    employee_count_by_country: (
        CompanyEnrichmentPeopledatalabsEmployeeCountByCountry | None
    ) = Field(
        default=None,
        alias="employeeCountByCountry",
        description="Headcount keyed by country.",
    )
    employee_count_by_month: (
        CompanyEnrichmentPeopledatalabsEmployeeCountByMonth | None
    ) = Field(
        default=None,
        alias="employeeCountByMonth",
        description="Headcount keyed by YYYY-MM month.",
    )
    employee_count_by_role: (
        CompanyEnrichmentPeopledatalabsEmployeeCountByRole | None
    ) = Field(
        default=None,
        alias="employeeCountByRole",
        description="Headcount keyed by role.",
    )
    employee_count_by_sub_role: (
        CompanyEnrichmentPeopledatalabsEmployeeCountBySubRole | None
    ) = Field(
        default=None,
        alias="employeeCountBySubRole",
        description="Headcount keyed by sub-role.",
    )
    employee_growth_rate: CompanyEnrichmentPeopledatalabsEmployeeGrowthRate | None = (
        Field(
            default=None,
            alias="employeeGrowthRate",
            description="Headcount growth rate keyed by window.",
        )
    )
    employee_growth_rate12_month_by_class: (
        CompanyEnrichmentPeopledatalabsEmployeeGrowthRate12MonthByClas | None
    ) = Field(
        default=None,
        alias="employeeGrowthRate12MonthByClass",
        description="Twelve-month headcount growth rate keyed by job class.",
    )
    employee_growth_rate12_month_by_country: (
        CompanyEnrichmentPeopledatalabsEmployeeGrowthRate12MonthByCountry | None
    ) = Field(
        default=None,
        alias="employeeGrowthRate12MonthByCountry",
        description="Twelve-month headcount growth keyed by country, each entry carrying current and prior headcount.",
    )
    employee_growth_rate12_month_by_role: (
        CompanyEnrichmentPeopledatalabsEmployeeGrowthRate12MonthByRole | None
    ) = Field(
        default=None,
        alias="employeeGrowthRate12MonthByRole",
        description="Twelve-month headcount growth rate keyed by role.",
    )
    employee_turnover_rate: (
        CompanyEnrichmentPeopledatalabsEmployeeTurnoverRate | None
    ) = Field(
        default=None,
        alias="employeeTurnoverRate",
        description="Turnover rate keyed by window, e.g. 3_month, 12_month.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Company Facebook page URL."
    )
    founded: int | None = Field(
        default=None, description="Year the company was founded."
    )
    funding_rounds: int | None = Field(
        default=None,
        alias="fundingRounds",
        description="Number of funding rounds raised.",
    )
    funding_stages: list[str] | None = Field(
        default=None,
        alias="fundingStages",
        description="Every funding stage the company has raised.",
    )
    gross_additions_by_month: (
        CompanyEnrichmentPeopledatalabsGrossAdditionsByMonth | None
    ) = Field(
        default=None,
        alias="grossAdditionsByMonth",
        description="Employees joined, keyed by YYYY-MM month.",
    )
    gross_departures_by_month: (
        CompanyEnrichmentPeopledatalabsGrossDeparturesByMonth | None
    ) = Field(
        default=None,
        alias="grossDeparturesByMonth",
        description="Employees departed, keyed by YYYY-MM month.",
    )
    headline: str | None = Field(default=None, description="One-line company tagline.")
    immediate_parent: str | None = Field(
        default=None,
        alias="immediateParent",
        description="People Data Labs company id of the immediate parent company.",
    )
    industry: str | None = Field(default=None, description="Company industry.")
    industry_v2: str | None = Field(
        default=None,
        alias="industryV2",
        description="Company industry on People Data Labs' newer taxonomy.",
    )
    inferred_revenue: str | None = Field(
        default=None,
        alias="inferredRevenue",
        description="Inferred annual revenue band, e.g. $50M-$100M.",
    )
    last_funding_utc: float | None = Field(
        default=None,
        alias="lastFundingUtc",
        description="UTC epoch timestamp in seconds (Unix time) of the most recent funding round. Multiply by 1000 for a JS Date in milliseconds.",
    )
    latest_funding_stage: str | None = Field(
        default=None,
        alias="latestFundingStage",
        description="Most recent funding stage, e.g. series_e.",
    )
    likelihood: int | None = Field(
        default=None,
        description="People Data Labs' 1 to 10 confidence that this record is the company you asked for.",
    )
    linkedin_followers: int | None = Field(
        default=None, alias="linkedinFollowers", description="LinkedIn follower count."
    )
    linkedin_id: str | None = Field(
        default=None, alias="linkedinId", description="Company LinkedIn numeric id."
    )
    linkedin_slug: str | None = Field(
        default=None, alias="linkedinSlug", description="Company LinkedIn vanity slug."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Company LinkedIn page URL."
    )
    location: CompanyEnrichmentPeopledatalabsLocation | None = Field(
        default=None, description="Company headquarters."
    )
    median_employee_tenure: float | None = Field(
        default=None,
        alias="medianEmployeeTenure",
        description="Median employee tenure in years.",
    )
    median_tenure_by_level: (
        CompanyEnrichmentPeopledatalabsMedianTenureByLevel | None
    ) = Field(
        default=None,
        alias="medianTenureByLevel",
        description="Median tenure in years, keyed by seniority level.",
    )
    median_tenure_by_role: CompanyEnrichmentPeopledatalabsMedianTenureByRole | None = (
        Field(
            default=None,
            alias="medianTenureByRole",
            description="Median tenure in years, keyed by role.",
        )
    )
    mic_exchange: str | None = Field(
        default=None,
        alias="micExchange",
        description="MIC code of the exchange the company lists on.",
    )
    naics_codes: list[CompanyEnrichmentPeopledatalabsNaicsCode] | None = Field(
        default=None,
        alias="naicsCodes",
        description="NAICS classification for the company.",
    )
    name: str | None = Field(
        description="Company name as People Data Labs displays it."
    )
    name_normalized: str | None = Field(
        default=None,
        alias="nameNormalized",
        description="Lowercase normalized company name, the form People Data Labs matches on.",
    )
    pdl_id: str | None = Field(
        default=None,
        alias="pdlId",
        description="People Data Labs persistent company id.",
    )
    profiles: list[str] | None = Field(
        default=None,
        description="Every social profile People Data Labs links to the company.",
    )
    sic_codes: list[CompanyEnrichmentPeopledatalabsSicCode] | None = Field(
        default=None,
        alias="sicCodes",
        description="SIC classification for the company.",
    )
    size: str | None = Field(
        default=None, description="Employee headcount band, e.g. 11-50."
    )
    summary: str | None = Field(default=None, description="Long company description.")
    tags: list[str] | None = Field(
        default=None, description="Descriptive tags for the company."
    )
    ticker: str | None = Field(
        default=None, description="Stock ticker, for listed companies."
    )
    total_funding_raised: float | None = Field(
        default=None,
        alias="totalFundingRaised",
        description="Total capital raised, in USD.",
    )
    twitter_url: str | None = Field(
        default=None, alias="twitterUrl", description="Company X (Twitter) profile URL."
    )
    type_: str | None = Field(
        default=None, alias="type", description="Ownership type, e.g. private, public."
    )
    ultimate_parent: str | None = Field(
        default=None,
        alias="ultimateParent",
        description="People Data Labs company id of the ultimate parent company.",
    )
    website: str | None = Field(default=None, description="Company website domain.")


class CompanyEnrichmentPeopledatalabsAverageTenureByLevel(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsAverageTenureByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeChurnRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeCountByClas(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeCountByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeCountByMonth(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeCountByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeCountBySubRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeGrowthRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeGrowthRate12MonthByClas(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeGrowthRate12MonthByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeGrowthRate12MonthByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsEmployeeTurnoverRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsGrossAdditionsByMonth(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsGrossDeparturesByMonth(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address_line2: str | None = Field(
        default=None, alias="addressLine2", description="Second line of the address."
    )
    continent: str | None = Field(default=None, description="Continent.")
    country: str | None = Field(default=None, description="Country.")
    geo: str | None = Field(default=None, description='Coordinates as "lat,lon".')
    locality: str | None = Field(default=None, description="City.")
    metro: str | None = Field(default=None, description="Metro area.")
    name: str | None = Field(
        default=None, description="Location as one display string."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code."
    )
    region: str | None = Field(default=None, description="State or region.")
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Street address."
    )


class CompanyEnrichmentPeopledatalabsMedianTenureByLevel(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsMedianTenureByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanyEnrichmentPeopledatalabsNaicsCode(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str | None = Field(description="NAICS code.")
    industry_group: str | None = Field(
        default=None, alias="industryGroup", description="NAICS industry group."
    )
    naics_industry: str | None = Field(
        default=None, alias="naicsIndustry", description="NAICS industry."
    )
    national_industry: str | None = Field(
        default=None, alias="nationalIndustry", description="NAICS national industry."
    )
    sector: str | None = Field(default=None, description="NAICS sector.")
    sub_sector: str | None = Field(
        default=None, alias="subSector", description="NAICS sub-sector."
    )


class CompanyEnrichmentPeopledatalabsSicCode(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str | None = Field(description="SIC code.")
    industry_group: str | None = Field(
        default=None, alias="industryGroup", description="SIC industry group."
    )
    industry_sector: str | None = Field(
        default=None, alias="industrySector", description="SIC industry sector."
    )
    major_group: str | None = Field(
        default=None, alias="majorGroup", description="SIC major group."
    )


class CompanyEnrichmentProspeoData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attributes: CompanyEnrichmentProspeoAttribute | None = Field(
        default=None, description="What Prospeo detects about how the company sells."
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Prospeo's own company identifier. Send it back as this SKU's companyId input.",
    )
    crunchbase_url: str | None = Field(
        default=None,
        alias="crunchbaseUrl",
        description="Company Crunchbase profile URL.",
    )
    description: str | None = Field(
        default=None, description="Company description as the company writes it."
    )
    description_ai: str | None = Field(
        default=None,
        alias="descriptionAi",
        description="Prospeo's own AI-written company summary.",
    )
    description_seo: str | None = Field(
        default=None,
        alias="descriptionSeo",
        description="Meta description from the company's website.",
    )
    domain: str | None = Field(default=None, description="Primary company domain.")
    email_tech: CompanyEnrichmentProspeoEmailTech | None = Field(
        default=None,
        alias="emailTech",
        description="How the company's email is hosted.",
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Employees Prospeo currently counts.",
    )
    employee_count_on_prospeo: int | None = Field(
        default=None,
        alias="employeeCountOnProspeo",
        description="Employees of this company that Prospeo holds a profile for.",
    )
    employee_range: str | None = Field(
        default=None,
        alias="employeeRange",
        description="Employee headcount band, e.g. 10000+.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Company Facebook page URL."
    )
    founded: int | None = Field(
        default=None, description="Year the company was founded."
    )
    free_enrichment: bool | None = Field(
        default=None,
        alias="freeEnrichment",
        description="True when Prospeo served this record from cache and did not charge for it.",
    )
    funding: CompanyEnrichmentProspeoFunding | None = Field(
        default=None, description="Funding history."
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    industry: str | None = Field(default=None, description="Company industry.")
    instagram_url: str | None = Field(
        default=None, alias="instagramUrl", description="Company Instagram profile URL."
    )
    job_postings: CompanyEnrichmentProspeoJobPosting | None = Field(
        default=None,
        alias="jobPostings",
        description="Open roles Prospeo currently sees for the company.",
    )
    keywords: list[str] | None = Field(
        default=None, description="Keywords Prospeo assigns the company."
    )
    linkedin_id: str | None = Field(
        default=None, alias="linkedinId", description="Company LinkedIn numeric id."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Company LinkedIn page URL."
    )
    location: CompanyEnrichmentProspeoLocation | None = Field(
        default=None, description="Company headquarters."
    )
    naics_codes: list[str] | None = Field(
        default=None,
        alias="naicsCodes",
        description="NAICS classification codes for the company.",
    )
    name: str | None = Field(description="Company name.")
    other_websites: list[str] | None = Field(
        default=None,
        alias="otherWebsites",
        description="Other domains the company owns.",
    )
    phone_hq: CompanyEnrichmentProspeoPhoneHq | None = Field(
        default=None, alias="phoneHq", description="Headquarters switchboard number."
    )
    revenue_range: CompanyEnrichmentProspeoRevenueRange | None = Field(
        default=None, alias="revenueRange", description="Annual revenue band in USD."
    )
    revenue_range_printed: str | None = Field(
        default=None,
        alias="revenueRangePrinted",
        description="Annual revenue band as a display string.",
    )
    sic_codes: list[str] | None = Field(
        default=None,
        alias="sicCodes",
        description="SIC classification codes for the company.",
    )
    technologies: list[str] | None = Field(
        default=None, description="Technologies Prospeo detects in the company's stack."
    )
    twitter_url: str | None = Field(
        default=None, alias="twitterUrl", description="Company X (Twitter) profile URL."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Ownership type, e.g. Private, Public, Non Profit.",
    )
    website: str | None = Field(default=None, description="Company website URL.")
    youtube_url: str | None = Field(
        default=None, alias="youtubeUrl", description="Company YouTube channel URL."
    )


class CompanyEnrichmentProspeoAttribute(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    has_demo: bool | None = Field(
        default=None, alias="hasDemo", description="The website offers a demo."
    )
    has_downloadable: bool | None = Field(
        default=None,
        alias="hasDownloadable",
        description="The website offers a download.",
    )
    has_free_trial: bool | None = Field(
        default=None,
        alias="hasFreeTrial",
        description="The website offers a free trial.",
    )
    has_mobile_apps: bool | None = Field(
        default=None,
        alias="hasMobileApps",
        description="The company publishes mobile apps.",
    )
    has_online_reviews: bool | None = Field(
        default=None,
        alias="hasOnlineReviews",
        description="The company has online reviews.",
    )
    has_pricing: bool | None = Field(
        default=None, alias="hasPricing", description="The website publishes pricing."
    )
    is_b2b: bool | None = Field(
        default=None, alias="isB2b", description="The company sells to businesses."
    )


class CompanyEnrichmentProspeoEmailTech(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str | None = Field(
        default=None, description="Domain the company's email addresses use."
    )
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider behind the domain's MX records.",
    )


class CompanyEnrichmentProspeoFunding(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    events: list[CompanyEnrichmentProspeoEvent] | None = Field(
        default=None, description="One entry per funding round."
    )
    latest_stage: str | None = Field(
        default=None, alias="latestStage", description="Most recent funding stage."
    )
    latest_utc: float | None = Field(
        default=None,
        alias="latestUtc",
        description="UTC epoch timestamp in seconds (Unix time) of the most recent round. Multiply by 1000 for a JS Date in milliseconds.",
    )
    rounds: int | None = Field(
        default=None, description="Number of funding rounds raised."
    )
    total_raised: float | None = Field(
        default=None, alias="totalRaised", description="Total capital raised, in USD."
    )
    total_raised_printed: str | None = Field(
        default=None,
        alias="totalRaisedPrinted",
        description="Total capital raised as a display string.",
    )


class CompanyEnrichmentProspeoEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    amount: float | None = Field(default=None, description="Amount raised in USD.")
    amount_printed: str | None = Field(
        default=None,
        alias="amountPrinted",
        description="Amount raised as a display string.",
    )
    link: str | None = Field(default=None, description="Source URL for the round.")
    raised_utc: float | None = Field(
        default=None,
        alias="raisedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the round closed. Multiply by 1000 for a JS Date in milliseconds.",
    )
    stage: str | None = Field(default=None, description="Round stage, e.g. Series E-J.")


class CompanyEnrichmentProspeoJobPosting(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active_count: int | None = Field(
        default=None, alias="activeCount", description="Open roles currently posted."
    )
    active_titles: list[str] | None = Field(
        default=None, alias="activeTitles", description="Titles of the open roles."
    )


class CompanyEnrichmentProspeoLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City.")
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    raw_address: str | None = Field(
        default=None,
        alias="rawAddress",
        description="Headquarters address as one display string.",
    )
    state: str | None = Field(default=None, description="State or region.")


class CompanyEnrichmentProspeoPhoneHq(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country: str | None = Field(
        default=None, description="Country the number belongs to."
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 code for that country.",
    )
    international: str | None = Field(
        default=None, description="Number in international format."
    )
    national: str | None = Field(default=None, description="Number in national format.")
    phone: str | None = Field(
        default=None, description="Phone number as Prospeo stores it."
    )


class CompanyEnrichmentProspeoRevenueRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    max: float | None = Field(default=None, description="Upper bound in USD.")
    min: float | None = Field(default=None, description="Lower bound in USD.")


class CompanyEnrichmentNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentCrustdataInput],
    ) -> RunResult[CompanyEnrichmentCrustdataData]:
        """Company Enrichment - Crustdata

        Enrich a company by domain, name, LinkedIn URL, or Crustdata identifier.

        Price: $0.096 per request.

        Example:
            res = client.company_enrichment.crustdata(companyDomain="posthog.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.crustdata", dict(input), options
        )
        return RunResult[CompanyEnrichmentCrustdataData].model_validate(raw)

    def datalegion(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentDatalegionInput],
    ) -> RunResult[CompanyEnrichmentDatalegionData]:
        """Company Enrichment - Data Legion

        Enrich one company from a domain or a company name into Data Legion's
        premium firmographics: industry, size, founding year, office locations,
        stock tickers and social profiles, plus headcount, hiring, attrition, growth
        and turnover, workforce breakdowns by seniority, function and tenure, and
        monthly headcount history.

        Price: $0.00006 per request plus $0.048 per result (maximum $0.04806).

        Example:
            res = client.company_enrichment.datalegion(domain="hubspot.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.datalegion", dict(input), options
        )
        return RunResult[CompanyEnrichmentDatalegionData].model_validate(raw)

    def lusha(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentLushaInput],
    ) -> RunResult[CompanyEnrichmentLushaData]:
        """Company Enrichment - Lusha

        Enrich one company into firmographics, industry classification, headcount,
        revenue band and social profiles from a domain, a company name, or a Lusha
        company id.

        Price: $0.084 per request.

        Example:
            res = client.company_enrichment.lusha(domain="posthog.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.lusha", dict(input), options
        )
        return RunResult[CompanyEnrichmentLushaData].model_validate(raw)

    def peopledatalabs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentPeopledatalabsInput],
    ) -> RunResult[CompanyEnrichmentPeopledatalabsData]:
        """Company Enrichment - People Data Labs

        Enrich one company into firmographics, funding history, NAICS and SIC
        classification, and People Data Labs' headcount growth, tenure and churn
        series from a domain or a company name.

        Price: $0.12 per request.

        Example:
            res = client.company_enrichment.peopledatalabs(domain="posthog.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.peopledatalabs", dict(input), options
        )
        return RunResult[CompanyEnrichmentPeopledatalabsData].model_validate(raw)

    def prospeo(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentProspeoInput],
    ) -> RunResult[CompanyEnrichmentProspeoData]:
        """Company Enrichment - Prospeo

        Enrich one company into firmographics, funding history, technology stack,
        open roles and headquarters contact details from a website, a company name,
        or a LinkedIn page.

        Price: $0.066 per request.

        Example:
            res = client.company_enrichment.prospeo(companyWebsite="stripe.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.prospeo", dict(input), options
        )
        return RunResult[CompanyEnrichmentProspeoData].model_validate(raw)


class AsyncCompanyEnrichmentNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentCrustdataInput],
    ) -> RunResult[CompanyEnrichmentCrustdataData]:
        """Company Enrichment - Crustdata

        Enrich a company by domain, name, LinkedIn URL, or Crustdata identifier.

        Price: $0.096 per request.

        Example:
            res = client.company_enrichment.crustdata(companyDomain="posthog.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.crustdata", dict(input), options
        )
        return RunResult[CompanyEnrichmentCrustdataData].model_validate(raw)

    async def datalegion(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentDatalegionInput],
    ) -> RunResult[CompanyEnrichmentDatalegionData]:
        """Company Enrichment - Data Legion

        Enrich one company from a domain or a company name into Data Legion's
        premium firmographics: industry, size, founding year, office locations,
        stock tickers and social profiles, plus headcount, hiring, attrition, growth
        and turnover, workforce breakdowns by seniority, function and tenure, and
        monthly headcount history.

        Price: $0.00006 per request plus $0.048 per result (maximum $0.04806).

        Example:
            res = client.company_enrichment.datalegion(domain="hubspot.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.datalegion", dict(input), options
        )
        return RunResult[CompanyEnrichmentDatalegionData].model_validate(raw)

    async def lusha(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentLushaInput],
    ) -> RunResult[CompanyEnrichmentLushaData]:
        """Company Enrichment - Lusha

        Enrich one company into firmographics, industry classification, headcount,
        revenue band and social profiles from a domain, a company name, or a Lusha
        company id.

        Price: $0.084 per request.

        Example:
            res = client.company_enrichment.lusha(domain="posthog.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.lusha", dict(input), options
        )
        return RunResult[CompanyEnrichmentLushaData].model_validate(raw)

    async def peopledatalabs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentPeopledatalabsInput],
    ) -> RunResult[CompanyEnrichmentPeopledatalabsData]:
        """Company Enrichment - People Data Labs

        Enrich one company into firmographics, funding history, NAICS and SIC
        classification, and People Data Labs' headcount growth, tenure and churn
        series from a domain or a company name.

        Price: $0.12 per request.

        Example:
            res = client.company_enrichment.peopledatalabs(domain="posthog.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.peopledatalabs", dict(input), options
        )
        return RunResult[CompanyEnrichmentPeopledatalabsData].model_validate(raw)

    async def prospeo(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyEnrichmentProspeoInput],
    ) -> RunResult[CompanyEnrichmentProspeoData]:
        """Company Enrichment - Prospeo

        Enrich one company into firmographics, funding history, technology stack,
        open roles and headquarters contact details from a website, a company name,
        or a LinkedIn page.

        Price: $0.066 per request.

        Example:
            res = client.company_enrichment.prospeo(companyWebsite="stripe.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_enrichment.prospeo", dict(input), options
        )
        return RunResult[CompanyEnrichmentProspeoData].model_validate(raw)
