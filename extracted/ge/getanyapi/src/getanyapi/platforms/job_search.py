# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the job_search platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class JobSearchTheirstackInput(TypedDict, total=False):
    """Input for Job Search - TheirStack."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyCountryCodeNot: NotRequired[list[str]]
    """Return companies whose HQ country code is not any of the ones passed here, case sensitive. Pass ISO2 country codes."""
    companyCountryCodeOr: NotRequired[list[str]]
    """Return companies whose HQ country code is any of the ones passed here, case sensitive. Pass ISO2 country codes."""
    companyDescriptionPatternAccentInsensitive: NotRequired[bool]
    """Set to True to make company description searches accent insensitive. For example, "á" will match "a" as well."""
    companyDescriptionPatternNot: NotRequired[list[str]]
    """Case-insensitive patterns to match in the company description. Will return companies that match any of the patterns."""
    companyDescriptionPatternOr: NotRequired[list[str]]
    """Case-insensitive patterns to match in the company description. Will return companies that match any of the patterns."""
    companyDomainNot: NotRequired[list[str]]
    """Only return companies that don't match these domains exactly. It accepts full urls (https://www.google.com/) and emails (john.polo@gmail.com)."""
    companyDomainOr: NotRequired[list[str]]
    """Only return companies that match these domains exactly. It accepts full urls (https://www.google.com/) and emails (john.polo@gmail.com). This filter acts as an OR filter, so if you pass more than one company domain, it will return companies that match any of the domains."""
    companyIdOr: NotRequired[list[str]]
    """Only return companies that match these IDs exactly. This filter acts as an OR filter, so if you pass more than one company ID, it will return companies that match any of the IDs."""
    companyInvestorsOr: NotRequired[list[str]]
    """Investors of the company"""
    companyInvestorsPartialMatchOr: NotRequired[list[str]]
    """Investors of the company. Will return companies for which any of their investors contains any of the substrings passed here. For example, if you pass 'andree', all funds that match it (like 'Andreessen Horowitz', 'Andreessen Horowitz LLC', etc)."""
    companyKeywordSlugAnd: NotRequired[list[str]]
    """Return results from companies that have mentioned all of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    companyKeywordSlugNot: NotRequired[list[str]]
    """Return results from companies that haven't mentioned any of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    companyKeywordSlugOr: NotRequired[list[str]]
    """Return results from companies that have mentioned any of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    companyLinkedinUrlExists: NotRequired[bool]
    """(Use `property_exists_or / property_exists_and` instead) Only return companies with a LinkedIn URL"""
    companyLinkedinUrlOr: NotRequired[list[str]]
    """Return companies whose LinkedIn URL matches any of the slugs passed here. Can also pass full LinkedIn company URLs."""
    companyListIdNot: NotRequired[list[str]]
    """Return companies that don't belong to any of the company lists passed here"""
    companyListIdOr: NotRequired[list[str]]
    """Return companies that belong to any of the company lists passed here"""
    companyLocationPatternOr: NotRequired[list[str]]
    """Return companies whose city matches any of the patterns passed here. Case insensitive. For example, if you pass 'san francisco', it will return companies whose city is 'San Francisco', 'San Francisco Bay Area', etc."""
    companyNameCaseInsensitiveOr: NotRequired[list[str]]
    """Only return companies that match these names exactly, case-insensitively."""
    companyNameNot: NotRequired[list[str]]
    """Only return companies that don't match these names exactly, case-sensitively."""
    companyNameOr: NotRequired[list[str]]
    """Only return companies that match these names exactly, case-sensitively. This filter acts as an OR filter, so if you pass more than one company name, it will return companies that match any of the names."""
    companyNamePartialMatchNot: NotRequired[list[str]]
    """Company names. Will return companies whose name doesn't contain any of the the substrings passed here, case-insensitively. For example, if you pass 'google', it will exclude 'Google', 'Google LLC', 'Google Inc', etc."""
    companyNamePartialMatchOr: NotRequired[list[str]]
    """Company names. Will return companies whose name contain any of the the substrings passed here, case-insensitively. For example, if you pass "google", it will return "Google", "Google LLC", "Google Inc", etc."""
    companyTagsOr: NotRequired[list[str]]
    """Return companies that match any of these keywords"""
    companyTechnologySlugAnd: NotRequired[list[str]]
    """Will return jobs from companies that that have mentioned all of these technologies in their jobs (not necessarily in the jobs returned). Case sensitive. Pass slugs. Check out all the technologies we track at GET /v0/catalog/technologies. Deprecated: use company_keyword_slug_and instead."""
    companyTechnologySlugNot: NotRequired[list[str]]
    """Will return jobs from companies that that haven't mentioned any of these technologies in their jobs. Case sensitive. Pass slugs. Check out all the technologies we track at GET /v0/catalog/technologies. Deprecated: use company_keyword_slug_not instead."""
    companyTechnologySlugOr: NotRequired[list[str]]
    """Will return jobs from companies that that have mentioned any of these technologies in their jobs (not necessarily in the jobs returned). Case sensitive. Pass slugs. Check out all the technologies we track at GET /v0/catalog/technologies. Deprecated: use company_keyword_slug_or instead."""
    companyType: NotRequired[str]
    """Filter by company type."""
    discoveredAtGte: NotRequired[str]
    """Only jobs discovered by TheirStack on this date or datetime or after will be returned. In UTC timezone."""
    discoveredAtLte: NotRequired[str]
    """Only jobs discovered by TheirStack on this date or datetime or before will be returned. In UTC timezone."""
    discoveredAtMaxAgeDays: NotRequired[int]
    """If 0, only return jobs added to our database in the current day. If 1, from today and yesterday, etc."""
    discoveredAtMinAgeDays: NotRequired[int]
    """If 1, only return jobs discovered by TheirStack until yesterday. If 2, until 2 days ago, etc."""
    easyApply: NotRequired[bool]
    """If True, only return jobs that can be applied directly through the job board. If False, only return jobs that require redirecting to the company's website."""
    employmentStatusesOr: NotRequired[list[str]]
    """Filter jobs by employment status. Returns jobs that match any of the specified employment types. If no values are provided or an empty list is sent, all jobs regardless of employment status will be returned."""
    finalUrlExists: NotRequired[bool]
    """(Use `property_exists_or / property_exists_and` instead) Only return jobs with a final URL. Typically jobs that were originally posted on an ATS. If True, only return jobs with a final URL. If False, only return jobs without a final URL. If None, return all jobs."""
    fundingStageOr: NotRequired[list[str]]
    """Funding stages of companies returned. Possible values: ['angel', 'convertible_note', 'debt_financing', 'equity_crowdfunding', 'other', 'private_equity', 'seed', 'series_a', 'series_b', 'series_c', 'series_d', 'series_e', 'series_f', 'series_g', 'series_h', 'venture_round_not_specified', 'series_i', 'series_j', 'undisclosed', 'series_unknown', 'pre_seed', 'post_ipo_secondary', 'post_ipo_equity', 'post_ipo_debt', 'non_equity_assistance', 'late_vc', 'initial_coin_offering', 'growth_equity_vc', 'grant', 'early_vc', 'corporate_round', 'secondary_market', 'product_crowdfunding']"""
    hiringManagersExists: NotRequired[bool]
    """(Use `property_exists_or / property_exists_and` instead) If True, only return jobs with a hiring manager. If False, only return jobs without a hiring manager. If None, return all jobs."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeTotalResults: NotRequired[bool]
    """When enabled, calculates and returns `total_results` and `total_companies` fields in the response. WARNING: This significantly slows down responses as it requires reading the entire dataset. Recommended usage: enable only for the initial request to get totals, then disable for subsequent pagination requests."""
    industryIdNot: NotRequired[list[str]]
    """Industry ids to exclude.You can use any of LinkedIn's Industry Codes V2 or GET /v0/catalog/industries"""
    industryIdOr: NotRequired[list[str]]
    """Industry codes. You can use any of LinkedIn's Industry Codes V2 or GET /v0/catalog/industries"""
    industryNot: NotRequired[list[str]]
    """Names of industries, case-insensitive. Results will exclude companies that belong to any of the industries specified in this parameter. Available values: GET /v0/catalog/industries WARNING: Deprecated parameter. Use the industry_id_not field instead."""
    industryOr: NotRequired[list[str]]
    """Names of industries, case-insensitive. Results will only include companies that belong to any of the industries specified in this parameter. Available values: GET /v0/catalog/industries WARNING: Deprecated parameter. Use the industry_id_or field instead."""
    jobCountryCodeNot: NotRequired[list[str]]
    """2-letter ISO country code of the location of the job. Can pass more than 1. Will exclude jobs from these countries"""
    jobCountryCodeOr: NotRequired[list[str]]
    """2-letter ISO country code of the location of the job. Can pass more than 1"""
    jobDescriptionContainsNot: NotRequired[list[str]]
    """Exclude jobs whose description contains any of these whole words using word boundaries (\\b). Case-insensitive by default, except for the patterns that are uppercase - in that case we'll respect it. Only finds complete words (e.g., searching 'quality' won't match 'inequality'). Results will exclude jobs whose description contains any of these words."""
    jobDescriptionContainsOr: NotRequired[list[str]]
    """Search for whole words in job descriptions using word boundaries (\\b). Case-insensitive by default, except for the patterns that are uppercase - in that case we'll respect it. Only finds complete words (e.g., searching 'quality' won't match 'inequality'). Results will include jobs whose description contains any of these words."""
    jobDescriptionPatternAnd: NotRequired[list[str]]
    """Regex patterns that must ALL match the job description (AND logic). Use (?i) at the start of a pattern to make it case-insensitive. Results will only include jobs whose description matches every pattern in this list."""
    jobDescriptionPatternCaseSensitiveOr: NotRequired[list[str]]
    """Deprecated. Use job_description_pattern_or instead, which now behaves identically."""
    jobDescriptionPatternIsCaseInsensitive: NotRequired[bool]
    """Deprecated. Has no effect."""
    jobDescriptionPatternNot: NotRequired[list[str]]
    """Regex patterns to look for in job descriptions. Case-sensitive. Results will include jobs whose description don't match any of these patterns. Use (?i) at the start of a pattern to make it case-insensitive. Can pass more than one."""
    jobDescriptionPatternOr: NotRequired[list[str]]
    """Regex patterns to look for in job descriptions. Case-sensitive. Results will include jobs whose description matches any of these patterns. Use (?i) at the start of a pattern to make it case-insensitive. Can pass more than one."""
    jobIdNot: NotRequired[list[str]]
    """Exclude jobs with these IDs."""
    jobIdOr: NotRequired[list[str]]
    """Get jobs with these IDs only."""
    jobIds: NotRequired[list[str]]
    """Get jobs with these IDs only. Deprecated parameter, use job_id_or instead."""
    jobKeywordSlugAnd: NotRequired[list[str]]
    """Will return jobs where all of these keyword slugs appear. Case sensitive. Check out all the keywords we track at GET /v0/catalog/keywords"""
    jobKeywordSlugNot: NotRequired[list[str]]
    """Will return jobs where none of these keyword slugs appear. Case sensitive. Check out all the keywords we track at GET /v0/catalog/keywords"""
    jobKeywordSlugOr: NotRequired[list[str]]
    """Will return jobs where any of these keyword slugs appear. Case sensitive. Check out all the keywords we track at GET /v0/catalog/keywords"""
    jobLocationNot: NotRequired[list[str]]
    """Filter jobs by location. Returns jobs whose locations DO NOT match ANY of the specified location criteria. Each location criteria is specified using a JobLocationFilter object. (You can find location IDs using the locations catalog endpoint)"""
    jobLocationOr: NotRequired[list[str]]
    """Filter jobs by location. Returns jobs whose locations match ANY of the specified location criteria. Each location criteria is specified using a JobLocationFilter object. (You can find location IDs using the locations catalog endpoint)"""
    jobLocationPatternNot: NotRequired[list[str]]
    """Regex patterns to exclude job locations. Case-insensitive. Searches both the location field and the enhanced locations array (using normalized city and state name fields within each location element). Jobs matching ANY of the provided patterns will be EXCLUDED from results. Use this to filter out specific locations."""
    jobLocationPatternOr: NotRequired[list[str]]
    """Regex patterns to match job locations. Case-insensitive. Searches both the location field and the enhanced locations array (using normalized city and state name fields within each location element). Jobs matching ANY of the provided patterns will be returned. Use this to find jobs in specific cities, states, or regions."""
    jobSeniorityOr: NotRequired[list[str]]
    """Will return jobs where the seniority is any of the ones passed here"""
    jobTechnologySlugAnd: NotRequired[list[str]]
    """Will return jobs where all of these technologies appear. Case sensitive. Pass slugs. Check out all the technologies we track with the technologies endpoint."""
    jobTechnologySlugNot: NotRequired[list[str]]
    """Will return jobs where none of these technologies appear. Case sensitive. Pass slugs. Check out all the technologies we track with the technologies endpoint."""
    jobTechnologySlugOr: NotRequired[list[str]]
    """Will return jobs where any of these technologies appear. Case sensitive. Pass slugs. Check out all the technologies we track with the technologies endpoint. If you pass more than one technology, we will return jobs that mentnion all of the technologies."""
    jobTitleNot: NotRequired[list[str]]
    """Natural language patterns to match job titles. Case-insensitive. Only jobs with title that do not match any of these patterns will be returned. Uses Postgres full text search."""
    jobTitleOr: NotRequired[list[str]]
    """Natural language patterns to match job titles. Case-insensitive. Only jobs with title that match any of these patterns will be returned. Uses Postgres full text search."""
    jobTitlePatternAnd: NotRequired[list[str]]
    """Regex patterns to match job titles. Case-insensitive. Only jobs with title that match all of these patterns will be returned."""
    jobTitlePatternNot: NotRequired[list[str]]
    """Regex patterns to match job titles. Case-insensitive. Jobs whose job title doesn't match any of the patterns will be returned."""
    jobTitlePatternOr: NotRequired[list[str]]
    """Regex patterns to match job titles. Case-insensitive. Jobs whose job title matches of the filters will be returned."""
    lastFundingRoundDateGte: NotRequired[str]
    """Only return companies whose last funding round date is after or on this date. Format: 'YYYY-MM-DD'"""
    lastFundingRoundDateLte: NotRequired[str]
    """Only return companies whose last funding round date is before or on this date. Format: 'YYYY-MM-DD'"""
    limit: NotRequired[int]
    """Rows to return on this page, up to TheirStack's maximum of 500. Every row returned is billed. Range: 1 to 148. Default: 25."""
    maxEmployeeCount: NotRequired[int]
    """Maximum number of employees in a company"""
    maxEmployeeCountOrNull: NotRequired[int]
    """Maximum number of employees in a company. If we don't have company size information, we will return it as well."""
    maxFundingUsd: NotRequired[int]
    """Maximum company funding, in USD"""
    maxRevenueUsd: NotRequired[int]
    """Maximum company revenue, in USD"""
    maxSalaryUsd: NotRequired[float]
    """Maximum annual salary in USD. For example, 150000 means $150,000."""
    minEmployeeCount: NotRequired[int]
    """Minimum number of employees in a company"""
    minEmployeeCountOrNull: NotRequired[int]
    """Minimum number of employees in a company. If we don't have company size information, we will return it as well."""
    minFundingUsd: NotRequired[int]
    """Minimum company funding, in USD"""
    minRevenueUsd: NotRequired[int]
    """Minimum company revenue, in USD"""
    minSalaryUsd: NotRequired[float]
    """Minimum annual salary in USD. For example, 100000 means $100,000."""
    offset: NotRequired[int]
    """Number of results to skip. Required for offset-based pagination."""
    onlyJobsWithHiringManagers: NotRequired[bool]
    """Only return jobs with a hiring manager. If True, only return jobs with a hiring manager. If False, only return jobs without a hiring manager. If None, return all jobs."""
    onlyJobsWithReportsTo: NotRequired[bool]
    """Only return jobs where we identified the role the hired person would report to. Deprecated field, use reports_to_exists instead."""
    onlyYcCompanies: NotRequired[bool]
    """Only return YC companies"""
    orderBy: NotRequired[list[str]]
    """List of column objects. You can pass several columns to order by, in order of priority. Only `field` is required, `desc` is True by default."""
    page: NotRequired[int]
    """Page number. Required when using page-based pagination."""
    postedAtGte: NotRequired[str]
    """ISO 8601 date string (yyyy-mm-dd). Only jobs published in this date or after will be returned."""
    postedAtLte: NotRequired[str]
    """ISO 8601 date string (yyyy-mm-dd). Only jobs published in this date or before will be returned."""
    postedAtMaxAgeDays: NotRequired[int]
    """Date posted max age in days. If 0, only return jobs posted today. If 1, from today and yesterday, etc."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    propertyExistsAnd: NotRequired[list[str]]
    propertyExistsOr: NotRequired[list[str]]
    """Return jobs that have any of these fields not null. For example, if you pass ['final_url'], it will return jobs that have a final_url set. This field also support chaining of fields. For example, if you pass ['company_object.domain', 'company_object.linkedin_url'], it will return jobs that have a company domain or a company linkedin_url set."""
    remote: NotRequired[bool]
    """True: only show remote jobs. False: only show non-remote jobs. None: show all jobs."""
    reportsToExists: NotRequired[bool]
    """Only return jobs where we identified the role the hired person would report to. If True, only return jobs where we identified the role the hired person would report to. If False, only return jobs where we didn't identify the role the hired person would report to. If None, return all jobs."""
    scraperNamePatternOr: NotRequired[list[str]]
    """Regex patterns to match job sources. Case-insensitive."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    urlDomainNot: NotRequired[list[str]]
    """Exclude jobs if their URL domain (from `url` or `source_url`) is in the provided case-insensitive list. For example, ['greenhouse.io', 'workable.com'] will exclude URLs containing 'greenhouse.io' or 'workable.com'. Refer to our list of sources at https://theirstack.com/en/docs/data/job/sources."""
    urlDomainOr: NotRequired[list[str]]
    """Include jobs only if their URL domain (from `url` or `source_url`) is in the provided case-insensitive list. For example, ['greenhouse.io', 'workable.com'] will match URLs containing 'greenhouse.io' or 'workable.com'. Refer to our list of sources at https://theirstack.com/en/docs/data/job/sources."""


class JobSearchTheirstackData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    jobs: list[JobSearchTheirstackJob] = Field(
        description="Matching job posts, each carrying the hiring company's firmographic record."
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


class JobSearchTheirstackJob(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avg_annual_salary_usd: float | None = Field(
        default=None,
        alias="avgAnnualSalaryUsd",
        description="Midpoint of the posted annual salary, converted to USD.",
    )
    cities: list[str] | None = Field(
        default=None, description="Every city the post covers."
    )
    closed_utc: float | None = Field(
        default=None,
        alias="closedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the post closed. Multiply by 1000 for a JS Date in milliseconds.",
    )
    company: JobSearchTheirstackCompany | None = Field(
        default=None,
        description="The hiring company's full TheirStack firmographic record.",
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Hiring company domain."
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Hiring company name."
    )
    continents: list[str] | None = Field(
        default=None, description="Every continent the post covers."
    )
    countries: list[str] | None = Field(
        default=None, description="Every country the post covers."
    )
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    country_codes: list[str] | None = Field(
        default=None,
        alias="countryCodes",
        description="Every country code the post covers.",
    )
    description: str | None = Field(
        default=None, description="Full job description text."
    )
    discovered_utc: float | None = Field(
        default=None,
        alias="discoveredUtc",
        description="UTC epoch timestamp in seconds (Unix time) TheirStack first saw the post. Multiply by 1000 for a JS Date in milliseconds.",
    )
    easy_apply: bool | None = Field(
        default=None,
        alias="easyApply",
        description="True when the post supports one-click apply.",
    )
    employment_statuses: list[str] | None = Field(
        default=None,
        alias="employmentStatuses",
        description="Employment types, e.g. full_time.",
    )
    final_url: str | None = Field(
        default=None,
        alias="finalUrl",
        description="URL the post redirects to, when it does.",
    )
    has_blurred_data: bool | None = Field(
        default=None,
        alias="hasBlurredData",
        description="True when TheirStack redacted part of the record on this plan.",
    )
    hybrid: bool | None = Field(default=None, description="True for a hybrid role.")
    job_id: str | None = Field(
        alias="jobId", description="TheirStack's own identifier for the post."
    )
    keyword_slugs: list[str] | None = Field(
        default=None,
        alias="keywordSlugs",
        description="Keyword slugs found in the post.",
    )
    latitude: float | None = Field(
        default=None, description="Latitude of the posted location."
    )
    location: str | None = Field(default=None, description="Location as posted.")
    locations: list[JobSearchTheirstackLocation] | None = Field(
        default=None,
        description="Every resolved location the post covers, with TheirStack's geographic breakdown.",
    )
    long_location: str | None = Field(
        default=None, alias="longLocation", description="Long form of the location."
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the posted location."
    )
    manager_roles: list[str] | None = Field(
        default=None,
        alias="managerRoles",
        description="Manager roles TheirStack extracted from the post.",
    )
    matching_phrases: list[str] | None = Field(
        default=None,
        alias="matchingPhrases",
        description="Phrases from your pattern filters that matched this post.",
    )
    matching_words: list[str] | None = Field(
        default=None,
        alias="matchingWords",
        description="Words from your pattern filters that matched this post.",
    )
    max_annual_salary: float | None = Field(
        default=None,
        alias="maxAnnualSalary",
        description="Upper bound of the posted annual salary, in the posted currency.",
    )
    max_annual_salary_usd: float | None = Field(
        default=None,
        alias="maxAnnualSalaryUsd",
        description="Upper bound of the posted annual salary, converted to USD.",
    )
    min_annual_salary: float | None = Field(
        default=None,
        alias="minAnnualSalary",
        description="Lower bound of the posted annual salary, in the posted currency.",
    )
    min_annual_salary_usd: float | None = Field(
        default=None,
        alias="minAnnualSalaryUsd",
        description="Lower bound of the posted annual salary, converted to USD.",
    )
    normalized_title: str | None = Field(
        default=None,
        alias="normalizedTitle",
        description="TheirStack's normalized form of the title.",
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code."
    )
    posted_utc: float | None = Field(
        default=None,
        alias="postedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the job was posted. Multiply by 1000 for a JS Date in milliseconds.",
    )
    remote: bool | None = Field(
        default=None, description="True for a fully remote role."
    )
    reposted: bool | None = Field(
        default=None, description="True when the post is a repost of an earlier one."
    )
    reposted_utc: float | None = Field(
        default=None,
        alias="repostedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the post was last reposted. Multiply by 1000 for a JS Date in milliseconds.",
    )
    salary_currency: str | None = Field(
        default=None,
        alias="salaryCurrency",
        description="Currency the posted salary is in.",
    )
    salary_string: str | None = Field(
        default=None,
        alias="salaryString",
        description="Salary exactly as the post states it.",
    )
    seniority: str | None = Field(
        default=None, description="Seniority band TheirStack assigns, e.g. mid_level."
    )
    short_location: str | None = Field(
        default=None, alias="shortLocation", description="Short form of the location."
    )
    source_url: str | None = Field(
        default=None, alias="sourceUrl", description="URL TheirStack found the post at."
    )
    state_code: str | None = Field(
        default=None, alias="stateCode", description="State or region code."
    )
    technology_slugs: list[str] | None = Field(
        default=None,
        alias="technologySlugs",
        description="Technology slugs found in the post.",
    )
    title: str | None = Field(description="Job title as posted.")
    url: str | None = Field(default=None, description="URL of the job post.")


class JobSearchTheirstackCompany(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alexa_ranking: int | None = Field(
        default=None,
        alias="alexaRanking",
        description="Alexa traffic rank for the company website.",
    )
    annual_revenue_readable: str | None = Field(
        default=None,
        alias="annualRevenueReadable",
        description="Estimated annual revenue as a display string, e.g. 4.2M.",
    )
    annual_revenue_usd: float | None = Field(
        default=None,
        alias="annualRevenueUsd",
        description="Estimated annual revenue in USD.",
    )
    apollo_id: str | None = Field(
        default=None,
        alias="apolloId",
        description="Apollo's identifier for the same company.",
    )
    city: str | None = Field(default=None, description="Headquarters city.")
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="TheirStack's own company identifier.",
    )
    company_keywords: list[str] | None = Field(
        default=None,
        alias="companyKeywords",
        description="Keywords TheirStack assigns the company.",
    )
    company_tags: list[str] | None = Field(
        default=None,
        alias="companyTags",
        description="Tags TheirStack assigns the company.",
    )
    country: str | None = Field(default=None, description="Headquarters country.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    domain: str | None = Field(default=None, description="Primary company domain.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Employees TheirStack currently counts.",
    )
    employee_count_range: str | None = Field(
        default=None,
        alias="employeeCountRange",
        description="Employee headcount band, e.g. 201-500.",
    )
    founded_year: int | None = Field(
        default=None, alias="foundedYear", description="Year the company was founded."
    )
    funding_stage: str | None = Field(
        default=None,
        alias="fundingStage",
        description="Most recent funding stage, e.g. series_b.",
    )
    has_blurred_data: bool | None = Field(
        default=None,
        alias="hasBlurredData",
        description="True when TheirStack redacted part of the record on this plan.",
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    industry: str | None = Field(default=None, description="Company industry.")
    industry_id: str | None = Field(
        default=None,
        alias="industryId",
        description="TheirStack's identifier for that industry.",
    )
    investors: list[str] | None = Field(
        default=None, description="Investors TheirStack records for the company."
    )
    is_recruiting_agency: bool | None = Field(
        default=None,
        alias="isRecruitingAgency",
        description="True when TheirStack classifies the company as a recruiting agency rather than a direct employer.",
    )
    keyword_slugs: list[str] | None = Field(
        default=None,
        alias="keywordSlugs",
        description="Keyword slugs found in the company's job posts. These are the values the keyword filters take.",
    )
    last_funding_round_readable: str | None = Field(
        default=None,
        alias="lastFundingRoundReadable",
        description="Most recent round size as a display string, e.g. $15M.",
    )
    last_funding_round_utc: float | None = Field(
        default=None,
        alias="lastFundingRoundUtc",
        description="UTC epoch timestamp in seconds (Unix time) of the most recent funding round. Multiply by 1000 for a JS Date in milliseconds.",
    )
    linkedin_id: str | None = Field(
        default=None, alias="linkedinId", description="Company LinkedIn numeric id."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Company LinkedIn page URL."
    )
    long_description: str | None = Field(
        default=None,
        alias="longDescription",
        description="Company description as the company writes it.",
    )
    name: str | None = Field(default=None, description="Company name.")
    num_buying_intent_topics: int | None = Field(
        default=None,
        alias="numBuyingIntentTopics",
        description="Distinct buying-intent topics detected in the company's job posts.",
    )
    num_jobs: int | None = Field(
        default=None,
        alias="numJobs",
        description="Job posts TheirStack holds for the company, all time.",
    )
    num_jobs_last30_days: int | None = Field(
        default=None,
        alias="numJobsLast30Days",
        description="Job posts published in the last 30 days.",
    )
    num_keywords: int | None = Field(
        default=None,
        alias="numKeywords",
        description="Distinct keywords detected in the company's job posts.",
    )
    num_technologies: int | None = Field(
        default=None,
        alias="numTechnologies",
        description="Distinct technologies detected in the company's job posts.",
    )
    possible_domains: list[str] | None = Field(
        default=None,
        alias="possibleDomains",
        description="Every domain TheirStack associates with the company.",
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Headquarters postal code."
    )
    publicly_traded_exchange: str | None = Field(
        default=None,
        alias="publiclyTradedExchange",
        description="Exchange the company lists on.",
    )
    publicly_traded_symbol: str | None = Field(
        default=None,
        alias="publiclyTradedSymbol",
        description="Stock ticker, for listed companies.",
    )
    seo_description: str | None = Field(
        default=None,
        alias="seoDescription",
        description="Meta description from the company's website.",
    )
    technology_names: list[str] | None = Field(
        default=None,
        alias="technologyNames",
        description="Human-readable names for those technologies.",
    )
    technology_slugs: list[str] | None = Field(
        default=None,
        alias="technologySlugs",
        description="Technology slugs found in the company's job posts. These are the values the technology filters take.",
    )
    total_funding_usd: float | None = Field(
        default=None,
        alias="totalFundingUsd",
        description="Total capital raised, in USD.",
    )
    url: str | None = Field(default=None, description="Company website URL.")
    yc_batch: str | None = Field(
        default=None,
        alias="ycBatch",
        description="Y Combinator batch, e.g. W20, for companies that went through it.",
    )


class JobSearchTheirstackLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Street address, when the post gives one."
    )
    admin1_code: str | None = Field(
        default=None,
        alias="admin1Code",
        description="First-level administrative division code.",
    )
    admin1_name: str | None = Field(
        default=None,
        alias="admin1Name",
        description="First-level administrative division name.",
    )
    admin2_code: str | None = Field(
        default=None,
        alias="admin2Code",
        description="Second-level administrative division code.",
    )
    admin2_name: str | None = Field(
        default=None,
        alias="admin2Name",
        description="Second-level administrative division name.",
    )
    city: str | None = Field(default=None, description="City.")
    continent: str | None = Field(default=None, description="Continent code, e.g. NA.")
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    display_name: str | None = Field(
        default=None, alias="displayName", description="Location as one display string."
    )
    feature_code: str | None = Field(
        default=None,
        alias="featureCode",
        description="GeoNames feature code for the place.",
    )
    latitude: float | None = Field(default=None, description="Latitude.")
    location_id: str | None = Field(
        default=None,
        alias="locationId",
        description="TheirStack's identifier for the place.",
    )
    longitude: float | None = Field(default=None, description="Longitude.")
    name: str | None = Field(description="Location name.")
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code."
    )
    state: str | None = Field(default=None, description="State or region.")
    state_code: str | None = Field(
        default=None, alias="stateCode", description="State or region code."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Granularity of the place, e.g. city, state, country.",
    )


class JobSearchNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def theirstack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[JobSearchTheirstackInput],
    ) -> RunResult[JobSearchTheirstackData]:
        """Job Search - TheirStack

        Search TheirStack's job-post index by company, technology, keyword, title,
        seniority, salary, location and how recently the post appeared, and get the
        hiring company's full firmographic record with every post. Billed per job
        returned.

        Price: $0 per request plus $0.0672 per result (maximum $9.9456).

        Example:
            res = client.job_search.theirstack(companyDomainOr=["stripe.com"], limit=1, postedAtMaxAgeDays=30)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "job_search.theirstack", dict(input), options
        )
        return RunResult[JobSearchTheirstackData].model_validate(raw)


class AsyncJobSearchNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def theirstack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[JobSearchTheirstackInput],
    ) -> RunResult[JobSearchTheirstackData]:
        """Job Search - TheirStack

        Search TheirStack's job-post index by company, technology, keyword, title,
        seniority, salary, location and how recently the post appeared, and get the
        hiring company's full firmographic record with every post. Billed per job
        returned.

        Price: $0 per request plus $0.0672 per result (maximum $9.9456).

        Example:
            res = client.job_search.theirstack(companyDomainOr=["stripe.com"], limit=1, postedAtMaxAgeDays=30)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "job_search.theirstack", dict(input), options
        )
        return RunResult[JobSearchTheirstackData].model_validate(raw)
