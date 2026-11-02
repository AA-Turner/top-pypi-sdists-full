# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the people_search platform."""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult
from .._pagination import (
    AsyncPaginator,
    Paginator,
    apaginate,
    paginate,
)

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class PeopleSearchAiArkInput(TypedDict, total=False):
    """Input for People Search - AI Ark."""

    account: NotRequired[dict[str, Any]]
    """Company-level filters, keyed by filter name. Accepted names: domain, employeeSize, foundedYear, funding, geoLocation, industries, keyword, language, linkedin, metric, naics, name, phoneNumber, productAndServices, retailSize, revenue, socialMedia, socialMediaLink, technologies, technology, type, url, location. Any other name is rejected. Most names take {"any"|"all": {"include": [...], "exclude": [...]}}, for example {"type": {"any": {"include": ["PUBLIC_COMPANY"]}}}. The any/all object goes INSIDE the filter name, never at the top of account. Size and money filters (employeeSize, foundedYear, revenue, retailSize) instead take {"type": "RANGE", "range": {"start": 50, "end": 200}} or {"type": "ALL"|"NONE"}; geoLocation takes {"position": {"lat": 0, "lng": 0}, "radius": 50, "unit": "km"|"mi"}; keyword takes {"any"|"all": {"include"|"exclude": {"content": ["..."], "sources": [{"mode": "WORD"|"SMART"|"STRICT", "source": "NAME"|"KEYWORD"|"SEO"|"DESCRIPTION"|"INDUSTRY"}]}}}."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    contact: NotRequired[dict[str, Any]]
    """Person-level filters, keyed by filter name. Accepted names: certification, certifications, company, contactLanguage, contactLocation, currentCompany, department, departmentAndFunction, education, experience, fullName, function, keyword, language, linkedin, location, name, pastCompany, profileBadge, seniority, skill, skills, socialMedia, socialMediaFollower, socialMediaLink, socialProfile, title. Any other name is rejected. Names take {"any"|"all": {"include": [...], "exclude": [...]}}, with the any/all object INSIDE the filter name rather than at the top of contact. Free-text search goes through keyword, which takes {"any"|"all": {"include"|"exclude": {"content": ["..."], "sources": [{"mode": "WORD"|"SMART"|"STRICT", "source": "HEADLINE"|"SUMMARY"|"ORGANIZATION"|"SKILL"|"WORK_HISTORY_DESCRIPTION"|"EDUCATION_DESCRIPTION"|"CERTIFICATION"|"PUBLICATION"|"PATENT"|"AWARD"|"COURSE"|"PROJECTS"|"VOLUNTEERING"|"LANGUAGE_SKILL"|"TEST_SCORE"}]}}}, for example {"keyword": {"any": {"include": {"content": ["engineer"], "sources": [{"mode": "SMART", "source": "HEADLINE"}]}}}}."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lists: NotRequired[dict[str, Any]]
    """AI Ark saved-list filter expression."""
    page: NotRequired[int]
    """Zero-based result page. Minimum: 0. Default: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    size: NotRequired[int]
    """Maximum people to return on this page. Range: 1 to 100. Default: 10."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PeopleSearchCrustdataInput(TypedDict, total=False):
    """Input for People Search - Crustdata."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: Required[str]
    """Company domain without a path."""
    country: NotRequired[str]
    fuzzyTitle: NotRequired[bool]
    """Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Range: 1 to 100. Default: 3."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileKeywords: NotRequired[Any]
    requireVerifiedEmail: NotRequired[bool]
    """Default: false."""
    seniority: NotRequired[Any]
    """Crustdata seniority level, or one of the listed shorthands (vp, manager, founder...); an array matches any of them."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    titleKeywords: Required[Any]


class PeopleSearchCrustdataV3Input(TypedDict, total=False):
    """Input for People Search - Crustdata v3 (legacy)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: Required[str]
    """Company domain without a path."""
    country: NotRequired[str]
    fuzzyTitle: NotRequired[bool]
    """Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Range: 1 to 100. Default: 3."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileKeywords: NotRequired[Any]
    requireVerifiedEmail: NotRequired[bool]
    """Default: false."""
    seniority: NotRequired[Any]
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    titleKeywords: Required[Any]


class PeopleSearchFullenrichInput(TypedDict, total=False):
    """Input for People Search - FullEnrich."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    currentCompanyDomains: NotRequired[list[dict[str, Any]]]
    """Filter by current employer domain. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyFoundedYears: NotRequired[list[dict[str, Any]]]
    """Filter by current employer founding year. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyHeadcounts: NotRequired[list[dict[str, Any]]]
    """Filter by current employer headcount band. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyHeadquarters: NotRequired[list[dict[str, Any]]]
    """Filter by current employer headquarters location. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyIds: NotRequired[list[dict[str, Any]]]
    """Filter by FullEnrich company id of the current employer. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyIndustries: NotRequired[list[dict[str, Any]]]
    """Filter by current employer industry. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyLinkedinUrls: NotRequired[list[dict[str, Any]]]
    """Filter by current employer LinkedIn URL. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyNames: NotRequired[list[dict[str, Any]]]
    """Filter by current employer name. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanySpecialties: NotRequired[list[dict[str, Any]]]
    """Filter by a current employer specialty. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentCompanyTypes: NotRequired[list[dict[str, Any]]]
    """Filter by current employer ownership type. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentPositionJobFunctions: NotRequired[list[dict[str, Any]]]
    """Filter by current job function. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentPositionSeniorityLevel: NotRequired[list[dict[str, Any]]]
    """Filter by seniority, e.g. Owner, Founder, C-level, VP, Director, Manager. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentPositionSubFunctions: NotRequired[list[dict[str, Any]]]
    """Filter by current job sub-function. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentPositionTitles: NotRequired[list[dict[str, Any]]]
    """Filter by current job title. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    currentPositionYearsIn: NotRequired[list[dict[str, Any]]]
    """Filter by years spent in the current position. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    cursor: NotRequired[str]
    """Cursor from a previous response's nextCursor. Works at any depth, including past the 10000 offset ceiling."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Rows to return on this page, up to FullEnrich's maximum of 100. Every row returned is billed. Range: 1 to 100. Default: 10."""
    offset: NotRequired[int]
    """Rows to skip. FullEnrich caps offset at 10000; past that, page with cursor. Minimum: 0. Default: 0."""
    pastCompanyDomains: NotRequired[list[dict[str, Any]]]
    """Filter by the domain of a past employer. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    pastCompanyNames: NotRequired[list[dict[str, Any]]]
    """Filter by an employer the person worked at before. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    pastPositionTitles: NotRequired[list[dict[str, Any]]]
    """Filter by a job title the person held before. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    personIds: NotRequired[list[dict[str, Any]]]
    """Filter by FullEnrich person id. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    personLanguages: NotRequired[list[dict[str, Any]]]
    """Filter by a language the person speaks. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    personLinkedinUrls: NotRequired[list[dict[str, Any]]]
    """Filter by person LinkedIn URL. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    personLocations: NotRequired[list[dict[str, Any]]]
    """Filter by the person's city, region or country. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    personNames: NotRequired[list[dict[str, Any]]]
    """Filter by person name. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    personSkills: NotRequired[list[dict[str, Any]]]
    """Filter by a skill the person lists. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PeopleSearchLushaInput(TypedDict, total=False):
    """Input for People Search - Lusha."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    excludeDnc: NotRequired[bool]
    """Exclude contacts whose phone numbers are all marked do-not-call."""
    filters: Required[dict[str, Any]]
    """Prospecting filters. Two keys are accepted, contacts and companies, and each takes an include and an exclude object. contacts.include and contacts.exclude accept departments, seniority, locations, existing_data_points and signals; companies.include and companies.exclude accept names, locations, sizes, revenues, technologies, intentTopics, mainIndustriesIds, subIndustriesIds, naicsCodes and sicCodes. Locations are objects such as {"country": "United States"}; sizes and revenues are ranges such as {"min": 200, "max": 500}. Example: {"companies": {"include": {"names": ["PostHog"]}}, "contacts": {"include": {"departments": ["Engineering & Technical"]}}}."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includePartialContact: NotRequired[bool]
    """Include contacts Lusha holds only partial information for. Defaults to true upstream."""
    pages: NotRequired[dict[str, Any]]
    """Which page of results to return. Lusha charges one flat price per page whatever its size."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PeopleSearchPeopledatalabsInput(TypedDict, total=False):
    """Input for People Search - People Data Labs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    dataInclude: NotRequired[str]
    """Comma-separated People Data Labs fields to include, or a leading - list to exclude. Projection changes the payload only; billing still follows profiles returned."""
    dataset: NotRequired[str]
    """People Data Labs dataset to search, when your plan exposes more than one."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum profiles to return. Every profile returned is billed, so start at 1 to check a query and read total before asking for more. Range: 1 to 59. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: NotRequired[dict[str, Any]]
    """Elasticsearch-style query over the People Data Labs person dataset, e.g. {"bool": {"must": [{"term": {"job_company_website": "posthog.com"}}]}}. Send this or sql, never both."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    sql: NotRequired[str]
    """People Data Labs SQL, in the form SELECT * FROM person WHERE ... . String literals take single quotes, only SELECT * is supported, and field names must be real People Data Labs person fields including nested subfields such as experience.title.name. Do not include a LIMIT clause; People Data Labs rejects it. Use limit instead. Send this or query, never both."""
    titlecase: NotRequired[bool]
    """Return text in title case instead of People Data Labs' lowercase default."""


class PeopleSearchProspeoInput(TypedDict, total=False):
    """Input for People Search - Prospeo."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    company: NotRequired[dict[str, Any]]
    """Filter by company names or websites, e.g. {"names": {"include": ["Stripe"]}, "websites": {"include": ["stripe.com"]}}."""
    companyAttributes: NotRequired[dict[str, Any]]
    """Filter by company characteristics, e.g. B2B, has pricing, has a free trial."""
    companyEmailProvider: NotRequired[list[str]]
    """Filter by the company's email MX provider."""
    companyFounded: NotRequired[dict[str, Any]]
    """Filter by founding year range."""
    companyFunding: NotRequired[dict[str, Any]]
    """Filter by funding stage or amount raised."""
    companyHeadcountByDepartment: NotRequired[list[str]]
    """Filter by headcount within a department."""
    companyHeadcountCustom: NotRequired[dict[str, Any]]
    """Filter by a custom employee count range."""
    companyHeadcountGrowth: NotRequired[dict[str, Any]]
    """Filter by headcount growth."""
    companyHeadcountRange: NotRequired[list[str]]
    """Filter by Prospeo's predefined employee count bands."""
    companyIndustry: NotRequired[dict[str, Any]]
    """Filter by company industry."""
    companyJobPostingHiringFor: NotRequired[list[str]]
    """Filter by the roles the company is currently hiring for."""
    companyJobPostingQuantity: NotRequired[dict[str, Any]]
    """Filter by how many roles the company has open."""
    companyKeywords: NotRequired[dict[str, Any]]
    """Filter by keywords found in company data."""
    companyLocationSearch: NotRequired[dict[str, Any]]
    """Filter by company headquarters location."""
    companyNaics: NotRequired[dict[str, Any]]
    """Filter by NAICS codes."""
    companyRevenue: NotRequired[dict[str, Any]]
    """Filter by revenue range."""
    companySics: NotRequired[dict[str, Any]]
    """Filter by SIC codes."""
    companyTechnology: NotRequired[dict[str, Any]]
    """Filter by technologies the company uses."""
    companyType: NotRequired[Literal["Private", "Public", "Non Profit", "Other"]]
    """Filter by ownership type."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPersonPerCompany: NotRequired[int]
    """Cap how many people one company may contribute to the results. Minimum: 1."""
    page: NotRequired[int]
    """Page number, one-based. Prospeo returns 25 results per page and charges one flat price per page. Minimum: 1. Default: 1."""
    personContactDetails: NotRequired[dict[str, Any]]
    """Filter by which contact channels Prospeo holds for the person."""
    personDepartment: NotRequired[dict[str, Any]]
    """Filter by department."""
    personDuplicateControl: NotRequired[dict[str, Any]]
    """Duplicate-control settings exported from the Prospeo dashboard."""
    personJobTitle: NotRequired[dict[str, Any]]
    """Filter by job title, with exact, contains and boolean semantics, e.g. {"include": ["VP Sales"]}."""
    personLocationSearch: NotRequired[dict[str, Any]]
    """Filter by where the person is located."""
    personName: NotRequired[dict[str, Any]]
    """Filter by person name."""
    personNameOrJobTitle: NotRequired[str]
    """Free-text search across person name and job title."""
    personSeniority: NotRequired[dict[str, Any]]
    """Filter by seniority. Prospeo's own values are case sensitive: Founder/Owner, C-Suite, Partner, Vice President, Head, Director, Manager, Senior, Entry, Intern. Common aliases such as vp and founder are normalized before the call."""
    personTimeInCurrentCompany: NotRequired[dict[str, Any]]
    """Filter by time at the current company, as a numeric range."""
    personTimeInCurrentRole: NotRequired[dict[str, Any]]
    """Filter by time in the current role, as a numeric range."""
    personYearOfExperience: NotRequired[dict[str, Any]]
    """Filter by total years of experience, as a numeric range."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PeopleSearchQuickenrichInput(TypedDict, total=False):
    """Input for People Search - QuickEnrich."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    city: NotRequired[dict[str, Any]]
    """Filter on city name."""
    companyDomain: NotRequired[dict[str, Any]]
    """Filter on employer website domain."""
    companyName: NotRequired[dict[str, Any]]
    """Filter on employer name."""
    country: NotRequired[dict[str, Any]]
    """Filter on ISO 3166-1 alpha-2 country code, e.g. "US"."""
    employeeCount: NotRequired[dict[str, Any]]
    """Filter on employer headcount band. These bands differ from the companyEmployeeCount string returned on a result."""
    hasEmail: NotRequired[bool]
    """Keep only people with a work email on file. The address itself is not returned here."""
    hasPhone: NotRequired[bool]
    """Keep only people with a phone on file. The number itself is not returned here."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    industry: NotRequired[dict[str, Any]]
    """Filter on the employer's LinkedIn industry label. Values must match the QuickEnrich industry vocabulary exactly, e.g. "IT Services and IT Consulting"."""
    limit: NotRequired[int]
    """Maximum people to return on this page. Range: 1 to 100. Default: 10."""
    linkedinBio: NotRequired[dict[str, Any]]
    """Filter on words found in the employer's LinkedIn bio."""
    locality: NotRequired[dict[str, Any]]
    """Filter on locality."""
    page: NotRequired[int]
    """One-based result page. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    revenue: NotRequired[dict[str, Any]]
    """Filter on employer revenue band."""
    services: NotRequired[dict[str, Any]]
    """Filter on the services the employer lists."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    title: NotRequired[dict[str, Any]]
    """Filter on job title."""


class PeopleSearchQuickenrichCompanyInput(TypedDict, total=False):
    """Input for People Search - QuickEnrich Company Contacts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: Required[str]
    """Company website domain, normalized upstream (example.com or https://example.com both work)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """One-based result page. Each page holds up to 20 people. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    title: NotRequired[str]
    """One job title, or several comma-separated, e.g. "CEO, CFO"."""


class PeopleSearchAiArkData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page: int = Field(
        description="Zero-based page number returned by the source. Minimum: 0."
    )
    people: list[PeopleSearchAiArkPeople] = Field(
        description="People returned on this page."
    )
    size: int = Field(description="Configured page size. Minimum: 0.")
    total: int = Field(description="Total matching people. Minimum: 0.")
    total_pages: int = Field(
        alias="totalPages", description="Total result pages. Minimum: 0."
    )


class PeopleSearchAiArkPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    birth_date: str | None = Field(
        default=None,
        alias="birthDate",
        description="Birthday as published on the profile, in YYYY-MM-DD form. LinkedIn lets a member hide the year, and the source encodes that as the placeholder year 1600 - treat the year as unknown when it reads 1600 rather than as a real date.",
    )
    career_start_utc: int | None = Field(
        default=None,
        alias="careerStartUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    city: str | None = Field(default=None, description="Location city.")
    company_acquisition_count: int | None = Field(
        default=None,
        alias="companyAcquisitionCount",
        description="Number of acquisitions the source records for the current company. Minimum: 0.",
    )
    company_acquisitions: list[PeopleSearchAiArkCompanyAcquisition] | None = Field(
        default=None,
        alias="companyAcquisitions",
        description="Acquisitions the source records for the current company, with the role telling you which side the company was on.",
    )
    company_address: str | None = Field(
        default=None,
        alias="companyAddress",
        description="Current company headquarters address as published by the source.",
    )
    company_city: str | None = Field(
        default=None,
        alias="companyCity",
        description="Current company headquarters city.",
    )
    company_continent: str | None = Field(
        default=None,
        alias="companyContinent",
        description="Current company headquarters continent.",
    )
    company_country: str | None = Field(
        default=None,
        alias="companyCountry",
        description="Current company headquarters country.",
    )
    company_crunchbase_url: str | None = Field(
        default=None,
        alias="companyCrunchbaseUrl",
        description="Current company's Crunchbase URL.",
    )
    company_description: str | None = Field(
        default=None,
        alias="companyDescription",
        description="Current company description.",
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Current company domain."
    )
    company_domain_ltd: str | None = Field(
        default=None,
        alias="companyDomainLtd",
        description="The source's second copy of the current company's domain. Usually identical to companyDomain; it can differ when the source resolves a redirect or a country domain differently, so compare the two rather than assuming they match.",
    )
    company_employee_count: int | None = Field(
        default=None,
        alias="companyEmployeeCount",
        description="Estimated employees at the current company. Minimum: 0.",
    )
    company_employee_range_min: int | None = Field(
        default=None,
        alias="companyEmployeeRangeMin",
        description="Lower bound of the current company's published employee range. Minimum: 0.",
    )
    company_facebook_url: str | None = Field(
        default=None,
        alias="companyFacebookUrl",
        description="Current company's canonical Facebook URL.",
    )
    company_founded_year: int | None = Field(
        default=None,
        alias="companyFoundedYear",
        description="Year the current company was founded.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="The source's own record identifier for the current company, exposed so you can trace a result back to the record it came from.",
    )
    company_image: str | None = Field(
        default=None,
        alias="companyImage",
        description="Current company logo URL. This is a SIGNED, EXPIRING image-proxy URL - the path carries an exp: epoch roughly five days out - so fetch and store the image promptly rather than storing this URL.",
    )
    company_industries: list[str] | None = Field(
        default=None,
        alias="companyIndustries",
        description="Additional industries for the current company.",
    )
    company_industry: str | None = Field(
        default=None,
        alias="companyIndustry",
        description="Current company's primary industry.",
    )
    company_keywords: list[str] | None = Field(
        default=None,
        alias="companyKeywords",
        description="Keywords describing the current company.",
    )
    company_languages: list[str] | None = Field(
        default=None,
        alias="companyLanguages",
        description="Languages the current company publishes in.",
    )
    company_latitude: float | None = Field(
        default=None,
        alias="companyLatitude",
        description="Current company headquarters latitude in decimal degrees.",
    )
    company_legal_name: str | None = Field(
        default=None,
        alias="companyLegalName",
        description="Current company's registered legal name.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Current company's canonical LinkedIn URL.",
    )
    company_locations: list[PeopleSearchAiArkCompanyLocation] | None = Field(
        default=None,
        alias="companyLocations",
        description="Every office the source lists for the current company, including the headquarters already reported in the companyCountry/companyCity fields.",
    )
    company_longitude: float | None = Field(
        default=None,
        alias="companyLongitude",
        description="Current company headquarters longitude in decimal degrees.",
    )
    company_naics: list[str] | None = Field(
        default=None,
        alias="companyNaics",
        description="NAICS codes for the current company.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Current company name."
    )
    company_overview: str | None = Field(
        default=None,
        alias="companyOverview",
        description="Longer overview of the current company. Overlaps companyDescription but is a separately maintained blurb and is often longer or more current.",
    )
    company_postal_code: str | None = Field(
        default=None,
        alias="companyPostalCode",
        description="Current company headquarters postal code.",
    )
    company_revenue_max: int | None = Field(
        default=None,
        alias="companyRevenueMax",
        description="Upper bound of the current company's estimated annual revenue in USD. Minimum: 0.",
    )
    company_revenue_min: int | None = Field(
        default=None,
        alias="companyRevenueMin",
        description="Lower bound of the current company's estimated annual revenue in USD. Minimum: 0.",
    )
    company_revenue_range: str | None = Field(
        default=None,
        alias="companyRevenueRange",
        description="The same annual revenue estimate as a single hyphenated range string, for example 500000000-1000000000. It duplicates companyRevenueMin and companyRevenueMax; use those for arithmetic.",
    )
    company_seo_description: str | None = Field(
        default=None,
        alias="companySeoDescription",
        description="The meta description the source scraped from the current company's website. It is site copy, not the source's own writing, so it may be in another language or out of date.",
    )
    company_start_utc: int | None = Field(
        default=None,
        alias="companyStartUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    company_state: str | None = Field(
        default=None,
        alias="companyState",
        description="Current company headquarters state or region.",
    )
    company_street: str | None = Field(
        default=None,
        alias="companyStreet",
        description="Current company headquarters street or neighbourhood line.",
    )
    company_sub_organizations: list[str] | None = Field(
        default=None,
        alias="companySubOrganizations",
        description="The source's own record identifiers for the current company's sub-organizations, exposed so you can look each one up in the company endpoints.",
    )
    company_technologies: list[PeopleSearchAiArkCompanyTechnologie] | None = Field(
        default=None,
        alias="companyTechnologies",
        description="Technologies detected on the current company's web presence.",
    )
    company_twitter_url: str | None = Field(
        default=None,
        alias="companyTwitterUrl",
        description="Current company's canonical X (Twitter) URL.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Current company's organization type.",
    )
    company_updated_utc: int | None = Field(
        default=None,
        alias="companyUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    company_website_url: str | None = Field(
        default=None,
        alias="companyWebsiteUrl",
        description="Current company website URL.",
    )
    connection_count: int | None = Field(
        default=None,
        alias="connectionCount",
        description="LinkedIn connection count. Minimum: 0.",
    )
    country: str | None = Field(default=None, description="Location country.")
    creator: bool | None = Field(
        default=None, description="Whether the profile is in LinkedIn creator mode."
    )
    departments: list[str] | None = Field(
        default=None, description="Departments the current role belongs to."
    )
    educations: list[PeopleSearchAiArkEducation] | None = Field(
        default=None, description="Education history listed on the profile."
    )
    experience: list[PeopleSearchAiArkExperience] | None = Field(
        default=None, description="Work history grouped by company, most recent first."
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical Facebook profile URL."
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="Person's first name."
    )
    followable: Any | None = Field(
        default=None,
        description="Whether the profile can be followed without connecting. Untyped passthrough: the source returns null for most profiles, so its populated shape is not yet proven and this field carries whatever the source sends without reshaping it.",
    )
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="LinkedIn follower count. Minimum: 0.",
    )
    full_name: str | None = Field(alias="fullName", description="Person's full name.")
    functions: list[str] | None = Field(
        default=None, description="Job functions the current role covers."
    )
    github_url: str | None = Field(
        default=None, alias="githubUrl", description="Canonical GitHub profile URL."
    )
    headline: str | None = Field(
        default=None, description="Professional profile headline."
    )
    hiring: bool | None = Field(
        default=None, description="Whether the profile is flagged as hiring."
    )
    image: str | None = Field(
        default=None,
        description="Profile photo URL. This is a SIGNED, EXPIRING image-proxy URL - the path carries an exp: epoch roughly five days out - so fetch and store the image promptly rather than storing this URL.",
    )
    industry: str | None = Field(
        default=None, description="Industry the person works in."
    )
    influencer: bool | None = Field(
        default=None,
        description="Whether the profile carries a LinkedIn influencer badge.",
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Person's last name."
    )
    linkedin_handle: str | None = Field(
        default=None,
        alias="linkedinHandle",
        description="LinkedIn public profile handle, the trailing segment of the profile URL.",
    )
    linkedin_url: str | None = Field(
        alias="linkedinUrl", description="Canonical LinkedIn profile URL."
    )
    location: str | None = Field(default=None, description="Formatted location.")
    location_position: Any | None = Field(
        default=None,
        alias="locationPosition",
        description="Coordinates for the person's location as the source returns them. Untyped passthrough: the source returns null for most profiles, so its populated shape is not yet proven and this field carries whatever the source sends without reshaping it.",
    )
    location_short: str | None = Field(
        default=None,
        alias="locationShort",
        description="Shorter form of the same location, usually city and state without country or continent. It duplicates part of location.",
    )
    middle_name: str | None = Field(
        default=None, alias="middleName", description="Person's middle name."
    )
    network_influencer: bool | None = Field(
        default=None,
        alias="networkInfluencer",
        description="The same influencer flag as the badge above, carried on the source's network statistics instead of its badge block. Expected to agree with influencer; compare them if the distinction matters to you.",
    )
    open_to_work: bool | None = Field(
        default=None,
        alias="openToWork",
        description="Whether the profile is flagged open to work.",
    )
    premium: bool | None = Field(
        default=None,
        description="Whether the profile carries a LinkedIn premium badge.",
    )
    previous_job_titles: Any | None = Field(
        default=None,
        alias="previousJobTitles",
        description="Job titles the person held before the current one, as the source returns them. Untyped passthrough: the source returns null for most profiles, so its populated shape is not yet proven and this field carries whatever the source sends without reshaping it. The experience array carries the same history in a typed form.",
    )
    primary_language: str | None = Field(
        default=None,
        alias="primaryLanguage",
        description="Primary profile language code.",
    )
    primary_language_country: str | None = Field(
        default=None,
        alias="primaryLanguageCountry",
        description="Country code paired with the primary profile language, for example US.",
    )
    profile_background: Any | None = Field(
        default=None,
        alias="profileBackground",
        description="The profile background or cover image as the source returns it. Untyped passthrough: the source returns null for most profiles, so its populated shape is not yet proven and this field carries whatever the source sends without reshaping it.",
    )
    profile_id: str | None = Field(
        default=None,
        alias="profileId",
        description="The source's own record identifier for this person, exposed so you can trace a result back to the record it came from.",
    )
    profile_languages: Any | None = Field(
        default=None,
        alias="profileLanguages",
        description="Languages the person lists on the profile, as the source returns them. Untyped passthrough: the source returns null for most profiles, so its populated shape is not yet proven and this field carries whatever the source sends without reshaping it.",
    )
    seniority: str | None = Field(
        default=None, description="Seniority level inferred for the current role."
    )
    skills: list[str] | None = Field(
        default=None, description="Skills listed on the profile."
    )
    state: str | None = Field(default=None, description="Location state or region.")
    sub_departments: list[str] | None = Field(
        default=None,
        alias="subDepartments",
        description="Sub-departments the current role belongs to.",
    )
    summary: str | None = Field(
        default=None, description="Profile summary or about section."
    )
    supported_locales: list[PeopleSearchAiArkSupportedLocale] | None = Field(
        default=None,
        alias="supportedLocales",
        description="Every locale the profile is available in. The first entry usually repeats primaryLanguage and primaryLanguageCountry.",
    )
    title: str | None = Field(default=None, description="Current job title.")
    title_start_utc: int | None = Field(
        default=None,
        alias="titleStartUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical X (Twitter) profile URL.",
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    verified: bool | None = Field(
        default=None, description="Whether LinkedIn has verified the profile."
    )


class PeopleSearchAiArkCompanyAcquisition(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    announced_utc: int | None = Field(
        default=None,
        alias="announcedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    image_key: str | None = Field(
        default=None,
        alias="imageKey",
        description="The source's internal image key for the counterparty. It is a bare key, not a URL.",
    )
    name: str | None = Field(
        default=None, description="Counterparty organization name."
    )
    record_id: str | None = Field(
        default=None,
        alias="recordId",
        description="The source's own slug for the counterparty organization.",
    )
    role: str | None = Field(
        default=None,
        description="The current company's side of the deal, for example acquiree.",
    )


class PeopleSearchAiArkCompanyLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Office address as published by the source."
    )
    city: str | None = Field(default=None, description="Office city.")
    continent: str | None = Field(default=None, description="Office continent.")
    country: str | None = Field(default=None, description="Office country.")
    latitude: float | None = Field(
        default=None, description="Office latitude in decimal degrees."
    )
    longitude: float | None = Field(
        default=None, description="Office longitude in decimal degrees."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Office postal code."
    )
    state: str | None = Field(default=None, description="Office state or region.")
    street: str | None = Field(
        default=None, description="Office street or neighbourhood line."
    )


class PeopleSearchAiArkCompanyTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")

    category: str | None = Field(default=None, description="Technology category.")
    name: str | None = Field(default=None, description="Technology name.")


class PeopleSearchAiArkEducation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    degree_name: str | None = Field(
        default=None, alias="degreeName", description="Degree earned."
    )
    end_utc: int | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    field_of_study: str | None = Field(
        default=None, alias="fieldOfStudy", description="Field of study."
    )
    grade: str | None = Field(
        default=None, description="Grade as published on the profile."
    )
    school_id: Any | None = Field(
        default=None,
        alias="schoolId",
        description="The source's own record identifier for the school. Untyped passthrough: the source returns null on the profiles observed so far, so its populated shape is not yet proven and this field carries whatever the source sends without reshaping it.",
    )
    school_image: Any | None = Field(
        default=None,
        alias="schoolImage",
        description="The school logo as the source returns it. Untyped passthrough: the source returns null on the profiles observed so far, so its populated shape is not yet proven and this field carries whatever the source sends without reshaping it.",
    )
    school_name: str | None = Field(
        default=None, alias="schoolName", description="School name."
    )
    school_url: str | None = Field(
        default=None, alias="schoolUrl", description="Canonical school page URL."
    )
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class PeopleSearchAiArkExperience(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_employee_range_max: int | None = Field(
        default=None,
        alias="companyEmployeeRangeMax",
        description="Upper bound of this company's published employee range. Minimum: 0.",
    )
    company_employee_range_min: int | None = Field(
        default=None,
        alias="companyEmployeeRangeMin",
        description="Lower bound of this company's published employee range. Minimum: 0.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="The source's own record identifier for this company, exposed so you can trace a result back to the record it came from.",
    )
    company_image: str | None = Field(
        default=None,
        alias="companyImage",
        description="Company logo URL. This is a SIGNED, EXPIRING image-proxy URL - the path carries an exp: epoch roughly five days out - so fetch and store the image promptly rather than storing this URL.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Canonical LinkedIn URL for this company.",
    )
    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Company name for this block of work history.",
    )
    end_utc: int | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    positions: list[PeopleSearchAiArkPosition] | None = Field(
        default=None, description="Individual roles held at this company."
    )
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class PeopleSearchAiArkPosition(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Company name as published on the role.",
    )
    description: str | None = Field(default=None, description="Role description.")
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type, for example Full-time.",
    )
    end_utc: int | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    location: str | None = Field(default=None, description="Role location.")
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str | None = Field(default=None, description="Role title.")


class PeopleSearchAiArkSupportedLocale(BaseModel):
    model_config = ConfigDict(extra="allow")

    country: str | None = Field(
        default=None, description="Country code for this locale."
    )
    language: str | None = Field(
        default=None, description="Language code for this locale."
    )


class PeopleSearchCrustdataData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when more profiles exist beyond this page.",
    )
    profiles: list[PeopleSearchCrustdataProfile] = Field(
        description="Matching professional profiles."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total number of profiles matching the search. Minimum: 0.",
    )


class PeopleSearchCrustdataProfile(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City of residence.")
    continent: str | None = Field(default=None, description="Continent of residence.")
    country: str | None = Field(default=None, description="Country of residence.")
    current_employers: list[PeopleSearchCrustdataCurrentEmployer] | None = Field(
        default=None,
        alias="currentEmployers",
        description="Positions the person currently holds.",
    )
    education_background: Any | None = Field(
        default=None,
        alias="educationBackground",
        description="Education history exactly as Crustdata returns it (school, degree, years, location). Untyped passthrough: the structure ships verbatim and is not validated.",
    )
    flagship_profile_url: str | None = Field(
        default=None,
        alias="flagshipProfileUrl",
        description="LinkedIn flagship profile URL. Usually the same value as linkedinUrl; Crustdata returns both and they can differ when the profile has a vanity URL.",
    )
    headline: str | None = Field(default=None, description="LinkedIn headline.")
    image: str | None = Field(default=None, description="Profile picture URL.")
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="LinkedIn profile URL."
    )
    name: str | None = Field(description="Full name of the person.")
    past_employers: list[PeopleSearchCrustdataPastEmployer] | None = Field(
        default=None,
        alias="pastEmployers",
        description="Positions the person previously held.",
    )
    person_id: str | None = Field(
        default=None,
        alias="personId",
        description="Crustdata identifier for this person.",
    )
    record_updated_utc: int | None = Field(
        default=None,
        alias="recordUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When Crustdata last wrote the record. Differs from updatedUtc, which reports the profile's own last-updated stamp.",
    )
    region: str | None = Field(
        default=None, description="Region string as published on the profile."
    )
    state: str | None = Field(
        default=None, description="State or province of residence."
    )
    twitter_handle: str | None = Field(
        default=None,
        alias="twitterHandle",
        description="X (Twitter) handle listed on the profile.",
    )


class PeopleSearchCrustdataCurrentEmployer(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_email_verified: bool | None = Field(
        default=None,
        alias="businessEmailVerified",
        description="True when a business email at this employer has been verified.",
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_headcount: int | None = Field(
        default=None,
        alias="companyHeadcount",
        description="Latest observed employee count at the employer.",
    )
    company_headcount_range: str | None = Field(
        default=None,
        alias="companyHeadcountRange",
        description="Employer headcount band, e.g. 51-200.",
    )
    company_headquarters_country: str | None = Field(
        default=None,
        alias="companyHeadquartersCountry",
        description="Country of the employer's headquarters.",
    )
    company_hq_location: str | None = Field(
        default=None,
        alias="companyHqLocation",
        description="Full headquarters location of the employer.",
    )
    company_hq_location_address_components: list[str] | None = Field(
        default=None,
        alias="companyHqLocationAddressComponents",
        description="The employer's headquarters location split into address components (city, county, state, country). Restates companyHqLocation in parts.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata company identifier for this employer, accepted by the Company Enrichment endpoint.",
    )
    company_industries: list[str] | None = Field(
        default=None,
        alias="companyIndustries",
        description="All LinkedIn industries listed for the employer.",
    )
    company_industry: str | None = Field(
        default=None,
        alias="companyIndustry",
        description="Primary LinkedIn industry of the employer.",
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="LinkedIn's own numeric identifier for the employer company page.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company page URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Employer company type, e.g. Privately Held or Public Company.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer website URL."
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type, e.g. Full-time or Contract.",
    )
    function_category: str | None = Field(
        default=None,
        alias="functionCategory",
        description="Job function category, e.g. Engineering or Sales.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="LinkedIn's own numeric identifier for the employer page. Crustdata returns the same value as companyLinkedinId on this record.",
    )
    location: str | None = Field(default=None, description="Location of the role.")
    position_id: str | None = Field(
        default=None,
        alias="positionId",
        description="Crustdata identifier for this specific position record.",
    )
    primary_employer: bool | None = Field(
        default=None,
        alias="primaryEmployer",
        description="True when this is the profile's primary listed position.",
    )
    seniority: str | None = Field(
        default=None,
        description="Seniority level of the role, e.g. Entry Level or Owner / Partner.",
    )
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Start of the role.",
    )
    title: str | None = Field(
        default=None, description="Job title held at this employer."
    )
    years_at_company: int | None = Field(
        default=None,
        alias="yearsAtCompany",
        description="Whole years spent at this employer.",
    )
    years_at_company_range: str | None = Field(
        default=None,
        alias="yearsAtCompanyRange",
        description="Human-readable tenure band, e.g. 3 to 5 years.",
    )


class PeopleSearchCrustdataPastEmployer(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_email_verified: bool | None = Field(
        default=None,
        alias="businessEmailVerified",
        description="True when a business email at this employer has been verified.",
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_headcount: int | None = Field(
        default=None,
        alias="companyHeadcount",
        description="Latest observed employee count at the employer.",
    )
    company_headcount_range: str | None = Field(
        default=None,
        alias="companyHeadcountRange",
        description="Employer headcount band, e.g. 51-200.",
    )
    company_headquarters_country: str | None = Field(
        default=None,
        alias="companyHeadquartersCountry",
        description="Country of the employer's headquarters.",
    )
    company_hq_location: str | None = Field(
        default=None,
        alias="companyHqLocation",
        description="Full headquarters location of the employer.",
    )
    company_hq_location_address_components: list[str] | None = Field(
        default=None,
        alias="companyHqLocationAddressComponents",
        description="The employer's headquarters location split into address components (city, county, state, country). Restates companyHqLocation in parts.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata company identifier for this employer, accepted by the Company Enrichment endpoint.",
    )
    company_industries: list[str] | None = Field(
        default=None,
        alias="companyIndustries",
        description="All LinkedIn industries listed for the employer.",
    )
    company_industry: str | None = Field(
        default=None,
        alias="companyIndustry",
        description="Primary LinkedIn industry of the employer.",
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="LinkedIn's own numeric identifier for the employer company page.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company page URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Employer company type, e.g. Privately Held or Public Company.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer website URL."
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type, e.g. Full-time or Contract.",
    )
    end_utc: int | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. End of the role.",
    )
    function_category: str | None = Field(
        default=None,
        alias="functionCategory",
        description="Job function category, e.g. Engineering or Sales.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="LinkedIn's own numeric identifier for the employer page. Crustdata returns the same value as companyLinkedinId on this record.",
    )
    location: str | None = Field(default=None, description="Location of the role.")
    position_id: str | None = Field(
        default=None,
        alias="positionId",
        description="Crustdata identifier for this specific position record.",
    )
    primary_employer: bool | None = Field(
        default=None,
        alias="primaryEmployer",
        description="True when this is the profile's primary listed position.",
    )
    seniority: str | None = Field(
        default=None,
        description="Seniority level of the role, e.g. Entry Level or Owner / Partner.",
    )
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Start of the role.",
    )
    title: str | None = Field(
        default=None, description="Job title held at this employer."
    )
    years_at_company: int | None = Field(
        default=None,
        alias="yearsAtCompany",
        description="Whole years spent at this employer.",
    )
    years_at_company_range: str | None = Field(
        default=None,
        alias="yearsAtCompanyRange",
        description="Human-readable tenure band, e.g. 3 to 5 years.",
    )


class PeopleSearchCrustdataV3Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when more profiles exist beyond this page.",
    )
    profiles: list[PeopleSearchCrustdataV3Profile] = Field(
        description="Matching professional profiles."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total number of profiles matching the search. Minimum: 0.",
    )


class PeopleSearchCrustdataV3Profile(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    all_employers: list[PeopleSearchCrustdataV3AllEmployer] | None = Field(
        default=None,
        alias="allEmployers",
        description="Every employer on the profile, current and past. Duplicates the contents of currentEmployers and pastEmployers in one combined list.",
    )
    certifications: list[PeopleSearchCrustdataV3Certification] | None = Field(
        default=None, description="Certifications listed on the profile."
    )
    city: str | None = Field(default=None, description="City of residence.")
    connection_count: int | None = Field(
        default=None,
        alias="connectionCount",
        description="Number of LinkedIn connections.",
    )
    contact_updated_utc: int | None = Field(
        default=None,
        alias="contactUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time the contact section was refreshed.",
    )
    continent: str | None = Field(default=None, description="Continent of residence.")
    country: str | None = Field(default=None, description="Country of residence.")
    current_employers: list[PeopleSearchCrustdataV3CurrentEmployer] | None = Field(
        default=None,
        alias="currentEmployers",
        description="Positions the person currently holds.",
    )
    education_background: Any | None = Field(
        default=None,
        alias="educationBackground",
        description="Education history exactly as Crustdata returns it. Untyped passthrough: the structure ships verbatim and is not validated, because it was empty for every profile we captured.",
    )
    education_updated_utc: int | None = Field(
        default=None,
        alias="educationUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time the education section was refreshed.",
    )
    emails: list[str] | None = Field(
        default=None, description="Email addresses found for the person."
    )
    employer_updated_utc: int | None = Field(
        default=None,
        alias="employerUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time the employment section was refreshed.",
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="Given name of the person."
    )
    flagship_profile_url: str | None = Field(
        default=None,
        alias="flagshipProfileUrl",
        description="LinkedIn flagship profile URL. Usually the same value as linkedinUrl; Crustdata returns both and they can differ when the profile has a vanity URL.",
    )
    follower_count: int | None = Field(
        default=None, alias="followerCount", description="Number of LinkedIn followers."
    )
    headline: str | None = Field(default=None, description="LinkedIn headline.")
    honors: Any | None = Field(
        default=None,
        description="Honors and awards exactly as Crustdata returns them. Untyped passthrough: the structure ships verbatim and is not validated, because it was empty for every profile we captured.",
    )
    image: str | None = Field(default=None, description="Profile picture URL.")
    indexed_utc: int | None = Field(
        default=None,
        alias="indexedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When Crustdata last indexed the record for search, which is usually just after recordUpdatedUtc.",
    )
    languages: list[str] | None = Field(
        default=None, description="Languages listed on the profile."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Family name of the person."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="LinkedIn profile URL."
    )
    name: str | None = Field(description="Full name of the person.")
    open_to_cards: Any | None = Field(
        default=None,
        alias="openToCards",
        description="LinkedIn open-to cards (open to work, hiring, providing services) exactly as Crustdata returns them. Untyped passthrough: the structure ships verbatim and is not validated, because it was empty for every profile we captured.",
    )
    past_employers: list[PeopleSearchCrustdataV3PastEmployer] | None = Field(
        default=None,
        alias="pastEmployers",
        description="Positions the person previously held.",
    )
    person_id: str | None = Field(
        default=None,
        alias="personId",
        description="Crustdata identifier for this person.",
    )
    profile_language: str | None = Field(
        default=None,
        alias="profileLanguage",
        description="Language the profile itself is written in.",
    )
    profile_picture_url: str | None = Field(
        default=None,
        alias="profilePictureUrl",
        description="Profile photo URL as LinkedIn serves it, query string intact because LinkedIn signs these URLs. The image field carries Crustdata's cached copy of the same photo, which does not expire.",
    )
    profile_updated_utc: int | None = Field(
        default=None,
        alias="profileUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time the profile section was refreshed.",
    )
    recently_changed_jobs: bool | None = Field(
        default=None,
        alias="recentlyChangedJobs",
        description="True when the person changed employer recently.",
    )
    record_updated_utc: int | None = Field(
        default=None,
        alias="recordUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When Crustdata last wrote the record. Differs from updatedUtc, which reports the profile's own last-updated stamp.",
    )
    region: str | None = Field(
        default=None, description="Region string as published on the profile."
    )
    region_address_components: list[str] | None = Field(
        default=None,
        alias="regionAddressComponents",
        description="The region string split into address components (city, county, state, country). Restates region in parts.",
    )
    skills: list[str] | None = Field(
        default=None, description="Skills listed on the profile."
    )
    state: str | None = Field(
        default=None, description="State or province of residence."
    )
    summary: str | None = Field(
        default=None, description="Profile summary or About section text."
    )
    twitter_handle: str | None = Field(
        default=None,
        alias="twitterHandle",
        description="X (Twitter) handle listed on the profile.",
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time any part of this profile record was refreshed.",
    )
    years_of_experience: int | None = Field(
        default=None,
        alias="yearsOfExperience",
        description="Total whole years of professional experience.",
    )
    years_of_experience_range: str | None = Field(
        default=None,
        alias="yearsOfExperienceRange",
        description="Human-readable experience band, e.g. More than 10 years.",
    )


class PeopleSearchCrustdataV3AllEmployer(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_email_verified: bool | None = Field(
        default=None,
        alias="businessEmailVerified",
        description="True when a business email at this employer has been verified.",
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_headcount: int | None = Field(
        default=None,
        alias="companyHeadcount",
        description="Latest observed employee count at the employer.",
    )
    company_headcount_range: str | None = Field(
        default=None,
        alias="companyHeadcountRange",
        description="Employer headcount band, e.g. 51-200.",
    )
    company_headquarters_country: str | None = Field(
        default=None,
        alias="companyHeadquartersCountry",
        description="Country of the employer's headquarters.",
    )
    company_hq_location: str | None = Field(
        default=None,
        alias="companyHqLocation",
        description="Full headquarters location of the employer.",
    )
    company_hq_location_address_components: list[str] | None = Field(
        default=None,
        alias="companyHqLocationAddressComponents",
        description="The employer's headquarters location split into address components (city, county, state, country). Restates companyHqLocation in parts.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata company identifier for this employer, accepted by the Company Enrichment endpoint.",
    )
    company_industries: list[str] | None = Field(
        default=None,
        alias="companyIndustries",
        description="All LinkedIn industries listed for the employer.",
    )
    company_industry: str | None = Field(
        default=None,
        alias="companyIndustry",
        description="Primary LinkedIn industry of the employer.",
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="LinkedIn's own numeric identifier for the employer company page.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company page URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Employer company type, e.g. Privately Held or Public Company.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer website URL."
    )
    description: str | None = Field(
        default=None, description="Role description as written on the profile."
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type, e.g. Full-time or Contract.",
    )
    end_utc: int | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. End of the role.",
    )
    function_category: str | None = Field(
        default=None,
        alias="functionCategory",
        description="Job function category, e.g. Engineering or Sales.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="LinkedIn's own numeric identifier for the employer page. Crustdata returns the same value as companyLinkedinId on this record.",
    )
    location: str | None = Field(default=None, description="Location of the role.")
    position_id: str | None = Field(
        default=None,
        alias="positionId",
        description="Crustdata identifier for this specific position record.",
    )
    primary_employer: bool | None = Field(
        default=None,
        alias="primaryEmployer",
        description="True when this is the profile's primary listed position.",
    )
    seniority: str | None = Field(
        default=None,
        description="Seniority level of the role, e.g. Entry Level or Owner / Partner.",
    )
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Start of the role.",
    )
    title: str | None = Field(
        default=None, description="Job title held at this employer."
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time this employment record was refreshed.",
    )
    years_at_company: int | None = Field(
        default=None,
        alias="yearsAtCompany",
        description="Whole years spent at this employer.",
    )
    years_at_company_range: str | None = Field(
        default=None,
        alias="yearsAtCompanyRange",
        description="Human-readable tenure band, e.g. 3 to 5 years.",
    )


class PeopleSearchCrustdataV3Certification(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    certification_id: str | None = Field(
        default=None,
        alias="certificationId",
        description="Crustdata identifier for this certification record.",
    )
    expires_utc: int | None = Field(
        default=None,
        alias="expiresUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the certification expires.",
    )
    issued_utc: int | None = Field(
        default=None,
        alias="issuedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the certification was issued.",
    )
    issuer: str | None = Field(
        default=None, description="Organization that issued the certification."
    )
    issuer_linkedin_id: str | None = Field(
        default=None,
        alias="issuerLinkedinId",
        description="LinkedIn's own numeric identifier for the issuing organization page.",
    )
    name: str | None = Field(default=None, description="Certification name.")
    url: str | None = Field(default=None, description="Link to the certification.")


class PeopleSearchCrustdataV3CurrentEmployer(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_email_verified: bool | None = Field(
        default=None,
        alias="businessEmailVerified",
        description="True when a business email at this employer has been verified.",
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_headcount: int | None = Field(
        default=None,
        alias="companyHeadcount",
        description="Latest observed employee count at the employer.",
    )
    company_headcount_range: str | None = Field(
        default=None,
        alias="companyHeadcountRange",
        description="Employer headcount band, e.g. 51-200.",
    )
    company_headquarters_country: str | None = Field(
        default=None,
        alias="companyHeadquartersCountry",
        description="Country of the employer's headquarters.",
    )
    company_hq_location: str | None = Field(
        default=None,
        alias="companyHqLocation",
        description="Full headquarters location of the employer.",
    )
    company_hq_location_address_components: list[str] | None = Field(
        default=None,
        alias="companyHqLocationAddressComponents",
        description="The employer's headquarters location split into address components (city, county, state, country). Restates companyHqLocation in parts.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata company identifier for this employer, accepted by the Company Enrichment endpoint.",
    )
    company_industries: list[str] | None = Field(
        default=None,
        alias="companyIndustries",
        description="All LinkedIn industries listed for the employer.",
    )
    company_industry: str | None = Field(
        default=None,
        alias="companyIndustry",
        description="Primary LinkedIn industry of the employer.",
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="LinkedIn's own numeric identifier for the employer company page.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company page URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Employer company type, e.g. Privately Held or Public Company.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer website URL."
    )
    description: str | None = Field(
        default=None, description="Role description as written on the profile."
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type, e.g. Full-time or Contract.",
    )
    function_category: str | None = Field(
        default=None,
        alias="functionCategory",
        description="Job function category, e.g. Engineering or Sales.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="LinkedIn's own numeric identifier for the employer page. Crustdata returns the same value as companyLinkedinId on this record.",
    )
    location: str | None = Field(default=None, description="Location of the role.")
    position_id: str | None = Field(
        default=None,
        alias="positionId",
        description="Crustdata identifier for this specific position record.",
    )
    primary_employer: bool | None = Field(
        default=None,
        alias="primaryEmployer",
        description="True when this is the profile's primary listed position.",
    )
    seniority: str | None = Field(
        default=None,
        description="Seniority level of the role, e.g. Entry Level or Owner / Partner.",
    )
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Start of the role.",
    )
    title: str | None = Field(
        default=None, description="Job title held at this employer."
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time this employment record was refreshed.",
    )
    years_at_company: int | None = Field(
        default=None,
        alias="yearsAtCompany",
        description="Whole years spent at this employer.",
    )
    years_at_company_range: str | None = Field(
        default=None,
        alias="yearsAtCompanyRange",
        description="Human-readable tenure band, e.g. 3 to 5 years.",
    )


class PeopleSearchCrustdataV3PastEmployer(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_email_verified: bool | None = Field(
        default=None,
        alias="businessEmailVerified",
        description="True when a business email at this employer has been verified.",
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_headcount: int | None = Field(
        default=None,
        alias="companyHeadcount",
        description="Latest observed employee count at the employer.",
    )
    company_headcount_range: str | None = Field(
        default=None,
        alias="companyHeadcountRange",
        description="Employer headcount band, e.g. 51-200.",
    )
    company_headquarters_country: str | None = Field(
        default=None,
        alias="companyHeadquartersCountry",
        description="Country of the employer's headquarters.",
    )
    company_hq_location: str | None = Field(
        default=None,
        alias="companyHqLocation",
        description="Full headquarters location of the employer.",
    )
    company_hq_location_address_components: list[str] | None = Field(
        default=None,
        alias="companyHqLocationAddressComponents",
        description="The employer's headquarters location split into address components (city, county, state, country). Restates companyHqLocation in parts.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata company identifier for this employer, accepted by the Company Enrichment endpoint.",
    )
    company_industries: list[str] | None = Field(
        default=None,
        alias="companyIndustries",
        description="All LinkedIn industries listed for the employer.",
    )
    company_industry: str | None = Field(
        default=None,
        alias="companyIndustry",
        description="Primary LinkedIn industry of the employer.",
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="LinkedIn's own numeric identifier for the employer company page.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company page URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Employer company type, e.g. Privately Held or Public Company.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer website URL."
    )
    description: str | None = Field(
        default=None, description="Role description as written on the profile."
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type, e.g. Full-time or Contract.",
    )
    end_utc: int | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. End of the role.",
    )
    function_category: str | None = Field(
        default=None,
        alias="functionCategory",
        description="Job function category, e.g. Engineering or Sales.",
    )
    linkedin_id: str | None = Field(
        default=None,
        alias="linkedinId",
        description="LinkedIn's own numeric identifier for the employer page. Crustdata returns the same value as companyLinkedinId on this record.",
    )
    location: str | None = Field(default=None, description="Location of the role.")
    position_id: str | None = Field(
        default=None,
        alias="positionId",
        description="Crustdata identifier for this specific position record.",
    )
    primary_employer: bool | None = Field(
        default=None,
        alias="primaryEmployer",
        description="True when this is the profile's primary listed position.",
    )
    seniority: str | None = Field(
        default=None,
        description="Seniority level of the role, e.g. Entry Level or Owner / Partner.",
    )
    start_utc: int | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Start of the role.",
    )
    title: str | None = Field(
        default=None, description="Job title held at this employer."
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last time this employment record was refreshed.",
    )
    years_at_company: int | None = Field(
        default=None,
        alias="yearsAtCompany",
        description="Whole years spent at this employer.",
    )
    years_at_company_range: str | None = Field(
        default=None,
        alias="yearsAtCompanyRange",
        description="Human-readable tenure band, e.g. 3 to 5 years.",
    )


class PeopleSearchFullenrichData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Cursor for the next page, or null when this lane is complete. Send it back as cursor.",
    )
    offset: int | None = Field(
        default=None, description="Rows skipped before this page."
    )
    people: list[PeopleSearchFullenrichPeople] = Field(
        description="Matching people, each with their current employer's firmographic record. Email addresses and phone numbers are not included; FullEnrich reveals those through its enrichment endpoints."
    )
    total: int | None = Field(
        default=None, description="Rows matching the filters across all pages."
    )


class PeopleSearchFullenrichPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City the person is in.")
    company: PeopleSearchFullenrichCompany | None = Field(
        default=None,
        description="The person's current employer, with FullEnrich's full firmographic record.",
    )
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    description: str | None = Field(default=None, description="Profile summary text.")
    educations: list[PeopleSearchFullenrichEducation] | None = Field(
        default=None, description="Education history."
    )
    experience: list[PeopleSearchFullenrichExperience] | None = Field(
        default=None, description="Known employment history."
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="First name."
    )
    full_name: str | None = Field(alias="fullName", description="Person's full name.")
    headline: str | None = Field(default=None, description="LinkedIn headline.")
    is_current: bool | None = Field(
        default=None,
        alias="isCurrent",
        description="True while FullEnrich treats the role as current.",
    )
    job_start_utc: float | None = Field(
        default=None,
        alias="jobStartUtc",
        description="UTC epoch timestamp in seconds (Unix time) the current role started. Multiply by 1000 for a JS Date in milliseconds.",
    )
    job_title: str | None = Field(
        default=None, alias="jobTitle", description="Current job title."
    )
    languages: list[PeopleSearchFullenrichLanguage] | None = Field(
        default=None, description="Languages the person speaks."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Last name."
    )
    linkedin_connections: int | None = Field(
        default=None,
        alias="linkedinConnections",
        description="LinkedIn connection count.",
    )
    linkedin_handle: str | None = Field(
        default=None, alias="linkedinHandle", description="LinkedIn vanity handle."
    )
    linkedin_id: str | None = Field(
        default=None, alias="linkedinId", description="LinkedIn numeric member id."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="LinkedIn profile URL."
    )
    person_id: str | None = Field(
        default=None,
        alias="personId",
        description="FullEnrich's own person identifier.",
    )
    region: str | None = Field(default=None, description="State or region.")
    seniority: str | None = Field(
        default=None,
        description="Seniority band for the current role, e.g. Manager, C-level.",
    )
    skills: list[str] | None = Field(
        default=None, description="Skills the person lists."
    )


class PeopleSearchFullenrichCompany(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="FullEnrich's own company identifier.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Ownership type, e.g. Public Company, Privately Held.",
    )
    description: str | None = Field(default=None, description="Company description.")
    domain: str | None = Field(default=None, description="Primary company domain.")
    founded_year: int | None = Field(
        default=None,
        alias="foundedYear",
        description="Year the company was founded. Zero when FullEnrich holds none.",
    )
    headcount: int | None = Field(
        default=None, description="Employees FullEnrich currently counts."
    )
    headcount_range: str | None = Field(
        default=None,
        alias="headcountRange",
        description="Employee headcount band, e.g. 5001-10000.",
    )
    headquarters: PeopleSearchFullenrichHeadquarter | None = Field(
        default=None, description="Headquarters address."
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    industry: str | None = Field(default=None, description="Main industry.")
    linkedin_followers: int | None = Field(
        default=None, alias="linkedinFollowers", description="LinkedIn follower count."
    )
    linkedin_handle: str | None = Field(
        default=None,
        alias="linkedinHandle",
        description="Company LinkedIn vanity handle.",
    )
    linkedin_id: str | None = Field(
        default=None, alias="linkedinId", description="Company LinkedIn numeric id."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Company LinkedIn page URL."
    )
    name: str | None = Field(default=None, description="Company name.")
    offices: list[PeopleSearchFullenrichOffice] | None = Field(
        default=None, description="Every other office FullEnrich holds for the company."
    )
    specialties: list[str] | None = Field(
        default=None, description="Specialties the company lists for itself."
    )
    website: str | None = Field(default=None, description="Company website URL.")


class PeopleSearchFullenrichHeadquarter(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City.")
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    line1: str | None = Field(default=None, description="First address line.")
    line2: str | None = Field(
        default=None,
        description="Second address line, carrying city, region, postal code and country.",
    )
    region: str | None = Field(default=None, description="State or region.")


class PeopleSearchFullenrichOffice(BaseModel):
    model_config = ConfigDict(extra="allow")

    line1: str | None = Field(default=None, description="First address line.")
    line2: str | None = Field(
        default=None,
        description="Second address line, carrying city, region, postal code and country.",
    )


class PeopleSearchFullenrichEducation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    degree: str | None = Field(default=None, description="Degree earned.")
    end_utc: float | None = Field(
        default=None,
        alias="endUtc",
        description="UTC epoch timestamp in seconds (Unix time) study ended. Multiply by 1000 for a JS Date in milliseconds.",
    )
    school_name: str | None = Field(alias="schoolName", description="School name.")
    start_utc: float | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time) study started. Multiply by 1000 for a JS Date in milliseconds.",
    )


class PeopleSearchFullenrichExperience(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_city: str | None = Field(
        default=None, alias="companyCity", description="Employer headquarters city."
    )
    company_country: str | None = Field(
        default=None,
        alias="companyCountry",
        description="Employer headquarters country.",
    )
    company_description: str | None = Field(
        default=None, alias="companyDescription", description="Employer description."
    )
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer primary domain."
    )
    company_founded_year: int | None = Field(
        default=None,
        alias="companyFoundedYear",
        description="Year the employer was founded.",
    )
    company_headcount: int | None = Field(
        default=None,
        alias="companyHeadcount",
        description="Employer headcount. Minimum: 0.",
    )
    company_headcount_range: str | None = Field(
        default=None,
        alias="companyHeadcountRange",
        description="Employer headcount range, e.g. 5001-10000.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="FullEnrich identifier for the employer.",
    )
    company_image: str | None = Field(
        default=None, alias="companyImage", description="Employer logo URL."
    )
    company_industry: str | None = Field(
        default=None, alias="companyIndustry", description="Employer primary industry."
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="Employer LinkedIn numeric id.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn page URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_region: str | None = Field(
        default=None,
        alias="companyRegion",
        description="Employer headquarters region or state.",
    )
    company_street: str | None = Field(
        default=None,
        alias="companyStreet",
        description="Employer headquarters street address.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Employer company type, e.g. Privately Held.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer website URL."
    )
    is_current: bool | None = Field(
        default=None, alias="isCurrent", description="Whether this is a current role."
    )
    seniority: str | None = Field(
        default=None, description="Seniority band for the role."
    )
    start_utc: float | None = Field(
        default=None,
        alias="startUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str | None = Field(default=None, description="Role title.")


class PeopleSearchFullenrichLanguage(BaseModel):
    model_config = ConfigDict(extra="allow")

    language: str | None = Field(description="Language name.")
    proficiency: str | None = Field(
        default=None, description="Proficiency band, e.g. FULL_PROFESSIONAL."
    )


class PeopleSearchLushaData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    current_page: int | None = Field(
        default=None,
        alias="currentPage",
        description="Zero-based page number this response holds.",
    )
    page_length: int | None = Field(
        default=None, alias="pageLength", description="Contacts returned on this page."
    )
    people: list[PeopleSearchLushaPeople] = Field(
        description="Contacts on this page. Email addresses and phone numbers are not included here; reveal them with Person Enrichment - Lusha."
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total contacts matching the filters across all pages.",
    )


class PeopleSearchLushaPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    available: PeopleSearchLushaAvailable | None = Field(
        default=None,
        description="What Lusha holds for this contact and would return on reveal. Every flag is a boolean; privateEmail can also come back as a redaction marker.",
    )
    company_description: str | None = Field(
        default=None, alias="companyDescription", description="Employer description."
    )
    company_domain: str | None = Field(
        default=None,
        alias="companyDomain",
        description="Fully qualified host for the employer's website.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Lusha's own company identifier for the employer.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    contact_id: str | None = Field(
        default=None,
        alias="contactId",
        description="Lusha's contact identifier for this search row.",
    )
    full_name: str | None = Field(alias="fullName", description="Person's full name.")
    image: str | None = Field(default=None, description="Employer logo URL.")
    is_shown: bool | None = Field(
        default=None,
        alias="isShown",
        description="True when this contact has already been revealed on the Lusha account.",
    )
    job_title: str | None = Field(
        default=None, alias="jobTitle", description="Current job title."
    )
    person_id: str | None = Field(
        default=None, alias="personId", description="Lusha's own person identifier."
    )


class PeopleSearchLushaAvailable(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_city: bool | None = Field(
        default=None, alias="companyCity", description="Employer city is available."
    )
    company_country: bool | None = Field(
        default=None,
        alias="companyCountry",
        description="Employer country is available.",
    )
    company_employees_count: bool | None = Field(
        default=None,
        alias="companyEmployeesCount",
        description="Employer headcount is available.",
    )
    company_funding: bool | None = Field(
        default=None,
        alias="companyFunding",
        description="Employer funding data is available.",
    )
    company_intent: bool | None = Field(
        default=None,
        alias="companyIntent",
        description="Employer buying-intent data is available.",
    )
    company_main_industry: bool | None = Field(
        default=None,
        alias="companyMainIndustry",
        description="Employer top-level industry is available.",
    )
    company_revenue: bool | None = Field(
        default=None,
        alias="companyRevenue",
        description="Employer revenue is available.",
    )
    company_sub_industry: bool | None = Field(
        default=None,
        alias="companySubIndustry",
        description="Employer sub-industry is available.",
    )
    company_technologies: bool | None = Field(
        default=None,
        alias="companyTechnologies",
        description="Employer technology stack is available.",
    )
    contact_location: bool | None = Field(
        default=None,
        alias="contactLocation",
        description="The person's location is available.",
    )
    department: bool | None = Field(
        default=None, description="A department is available."
    )
    direct_phone: bool | None = Field(
        default=None, alias="directPhone", description="A direct dial is available."
    )
    emails: bool | None = Field(
        default=None, description="Any email address is available."
    )
    mobile_phone: bool | None = Field(
        default=None, alias="mobilePhone", description="A mobile number is available."
    )
    phones: bool | None = Field(
        default=None, description="Any phone number is available."
    )
    private_email: Any | None = Field(
        default=None,
        alias="privateEmail",
        description="A personal email address is available. Lusha redacts this flag on some plans, in which case it is a string marker rather than a boolean.",
    )
    seniority: bool | None = Field(
        default=None, description="A seniority band is available."
    )
    social_link: bool | None = Field(
        default=None,
        alias="socialLink",
        description="A social profile link is available.",
    )
    work_email: bool | None = Field(
        default=None,
        alias="workEmail",
        description="A work email address is available.",
    )


class PeopleSearchPeopledatalabsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataset_version: str | None = Field(
        default=None,
        alias="datasetVersion",
        description="Version of the People Data Labs dataset these records came from.",
    )
    people: list[PeopleSearchPeopledatalabsPeople] = Field(
        description="Matching person profiles, up to limit."
    )
    total: int | None = Field(
        default=None,
        description="Profiles matching the query across the whole dataset, not just this page.",
    )


class PeopleSearchPeopledatalabsPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    activity_score: str | None = Field(
        default=None,
        alias="activityScore",
        description="People Data Labs' qualitative score for how recently the profile showed activity.",
    )
    available: PeopleSearchPeopledatalabsAvailable | None = Field(
        default=None,
        description="What People Data Labs holds for this person but does not return in search. Each flag is true when Person Enrichment - People Data Labs would return that field for this profile.",
    )
    company_address_line2: str | None = Field(
        default=None,
        alias="companyAddressLine2",
        description="Second line of the current employer's headquarters address.",
    )
    company_continent: str | None = Field(
        default=None,
        alias="companyContinent",
        description="Current employer headquarters continent.",
    )
    company_facebook_url: str | None = Field(
        default=None,
        alias="companyFacebookUrl",
        description="Current employer Facebook page URL.",
    )
    company_founded: int | None = Field(
        default=None,
        alias="companyFounded",
        description="Year the current employer was founded.",
    )
    company_geo: str | None = Field(
        default=None,
        alias="companyGeo",
        description='Current employer headquarters coordinates as "lat,lon".',
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="People Data Labs company id for the current employer.",
    )
    company_industry: str | None = Field(
        default=None, alias="companyIndustry", description="Current employer industry."
    )
    company_industry_v2: str | None = Field(
        default=None,
        alias="companyIndustryV2",
        description="Current employer industry on People Data Labs' newer taxonomy.",
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="Current employer LinkedIn numeric id.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Current employer LinkedIn page URL.",
    )
    company_locality: str | None = Field(
        default=None,
        alias="companyLocality",
        description="Current employer headquarters city.",
    )
    company_location_country: str | None = Field(
        default=None,
        alias="companyLocationCountry",
        description="Current employer headquarters country.",
    )
    company_location_name: str | None = Field(
        default=None,
        alias="companyLocationName",
        description="Current employer headquarters as one display string.",
    )
    company_metro: str | None = Field(
        default=None,
        alias="companyMetro",
        description="Current employer headquarters metro area.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Current employer name."
    )
    company_postal_code: str | None = Field(
        default=None,
        alias="companyPostalCode",
        description="Current employer headquarters postal code.",
    )
    company_region: str | None = Field(
        default=None,
        alias="companyRegion",
        description="Current employer headquarters state or region.",
    )
    company_size: str | None = Field(
        default=None,
        alias="companySize",
        description="Current employer headcount band.",
    )
    company_street_address: str | None = Field(
        default=None,
        alias="companyStreetAddress",
        description="Current employer headquarters street address.",
    )
    company_twitter_url: str | None = Field(
        default=None,
        alias="companyTwitterUrl",
        description="Current employer X (Twitter) profile URL.",
    )
    company_website: str | None = Field(
        default=None,
        alias="companyWebsite",
        description="Current employer website domain.",
    )
    continent: str | None = Field(default=None, description="Continent.")
    countries: list[str] | None = Field(
        default=None, description="Every country associated with the person."
    )
    country: str | None = Field(default=None, description="Country.")
    education: list[PeopleSearchPeopledatalabsEducation] | None = Field(
        default=None, description="Education history."
    )
    emails: list[PeopleSearchPeopledatalabsEmail] | None = Field(
        default=None,
        description="One entry per email address People Data Labs holds for the person. Search returns the kind only; the address itself comes from Person Enrichment - People Data Labs.",
    )
    experience: list[PeopleSearchPeopledatalabsExperience] | None = Field(
        default=None, description="Work history."
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="First name."
    )
    full_name: str | None = Field(alias="fullName", description="Person's full name.")
    geo: str | None = Field(default=None, description='Coordinates as "lat,lon".')
    industry: str | None = Field(
        default=None, description="Industry the person works in."
    )
    interests: list[str] | None = Field(
        default=None, description="Interests the person lists."
    )
    job_changed_utc: float | None = Field(
        default=None,
        alias="jobChangedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the person last changed jobs. Multiply by 1000 for a JS Date in milliseconds.",
    )
    job_start_date: str | None = Field(
        default=None,
        alias="jobStartDate",
        description="When the current role started: YYYY, YYYY-MM or YYYY-MM-DD.",
    )
    job_title: str | None = Field(
        default=None, alias="jobTitle", description="Current job title."
    )
    job_title_class: str | None = Field(
        default=None, alias="jobTitleClass", description="Normalized title class."
    )
    job_title_levels: list[str] | None = Field(
        default=None,
        alias="jobTitleLevels",
        description="Seniority levels for the current title.",
    )
    job_title_role: str | None = Field(
        default=None,
        alias="jobTitleRole",
        description="Normalized role for the current title.",
    )
    job_title_sub_role: str | None = Field(
        default=None,
        alias="jobTitleSubRole",
        description="Normalized sub-role for the current title.",
    )
    job_verified_utc: float | None = Field(
        default=None,
        alias="jobVerifiedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the current role was last verified. Multiply by 1000 for a JS Date in milliseconds.",
    )
    last_initial: str | None = Field(
        default=None, alias="lastInitial", description="Last initial."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Last name."
    )
    linkedin_id: str | None = Field(
        default=None, alias="linkedinId", description="LinkedIn numeric member id."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="LinkedIn profile URL."
    )
    linkedin_username: str | None = Field(
        default=None, alias="linkedinUsername", description="LinkedIn vanity handle."
    )
    locality: str | None = Field(default=None, description="City.")
    location_name: str | None = Field(
        default=None,
        alias="locationName",
        description="Where the person lives, as one display string.",
    )
    location_names: list[str] | None = Field(
        default=None,
        alias="locationNames",
        description="Every location People Data Labs has associated with the person.",
    )
    location_updated_utc: float | None = Field(
        default=None,
        alias="locationUpdatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the person's location was last updated. Multiply by 1000 for a JS Date in milliseconds.",
    )
    metro: str | None = Field(default=None, description="Metro area.")
    middle_initial: str | None = Field(
        default=None, alias="middleInitial", description="Middle initial."
    )
    middle_name: str | None = Field(
        default=None, alias="middleName", description="Middle name."
    )
    pdl_id: str | None = Field(
        default=None,
        alias="pdlId",
        description="People Data Labs persistent person id. Send it to Person Enrichment - People Data Labs to re-pull this record.",
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code."
    )
    profile_score: str | None = Field(
        default=None,
        alias="profileScore",
        description="People Data Labs' qualitative score for how complete the profile is.",
    )
    profiles: list[PeopleSearchPeopledatalabsProfile] | None = Field(
        default=None,
        description="Networks People Data Labs has a profile for. Search returns the network name only; profile URLs and handles come from Person Enrichment - People Data Labs.",
    )
    region: str | None = Field(default=None, description="State or region.")
    regions: list[str] | None = Field(
        default=None, description="Every region associated with the person."
    )
    sex: str | None = Field(default=None, description="Sex recorded for the person.")
    skills: list[str] | None = Field(
        default=None, description="Skills the person lists."
    )


class PeopleSearchPeopledatalabsAvailable(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    birth_date: bool | None = Field(
        default=None, alias="birthDate", description="A birth date is available."
    )
    birth_year: bool | None = Field(
        default=None, alias="birthYear", description="A birth year is available."
    )
    facebook_id: bool | None = Field(
        default=None,
        alias="facebookId",
        description="A Facebook numeric id is available.",
    )
    facebook_url: bool | None = Field(
        default=None,
        alias="facebookUrl",
        description="A Facebook profile URL is available.",
    )
    facebook_username: bool | None = Field(
        default=None,
        alias="facebookUsername",
        description="A Facebook handle is available.",
    )
    github_url: bool | None = Field(
        default=None,
        alias="githubUrl",
        description="A GitHub profile URL is available.",
    )
    github_username: bool | None = Field(
        default=None,
        alias="githubUsername",
        description="A GitHub handle is available.",
    )
    location_address_line2: bool | None = Field(
        default=None,
        alias="locationAddressLine2",
        description="A second address line is available.",
    )
    location_street_address: bool | None = Field(
        default=None,
        alias="locationStreetAddress",
        description="The current street address is available.",
    )
    mobile_phone: bool | None = Field(
        default=None,
        alias="mobilePhone",
        description="A mobile phone number is available.",
    )
    personal_emails: bool | None = Field(
        default=None,
        alias="personalEmails",
        description="Personal email addresses are available.",
    )
    phone_numbers: bool | None = Field(
        default=None, alias="phoneNumbers", description="Phone numbers are available."
    )
    recommended_personal_email: bool | None = Field(
        default=None,
        alias="recommendedPersonalEmail",
        description="A recommended personal email address is available.",
    )
    street_addresses: bool | None = Field(
        default=None,
        alias="streetAddresses",
        description="Street addresses are available.",
    )
    twitter_url: bool | None = Field(
        default=None,
        alias="twitterUrl",
        description="An X (Twitter) profile URL is available.",
    )
    twitter_username: bool | None = Field(
        default=None,
        alias="twitterUsername",
        description="An X (Twitter) handle is available.",
    )
    work_email: bool | None = Field(
        default=None,
        alias="workEmail",
        description="A work email address is available.",
    )


class PeopleSearchPeopledatalabsEducation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    degrees: list[str] | None = Field(default=None, description="Degrees earned.")
    end_date: str | None = Field(
        default=None, alias="endDate", description="When study ended."
    )
    gpa: float | None = Field(
        default=None, description="Grade point average, when published."
    )
    majors: list[str] | None = Field(default=None, description="Majors studied.")
    minors: list[str] | None = Field(default=None, description="Minors studied.")
    school_id: str | None = Field(
        default=None,
        alias="schoolId",
        description="PeopleDataLabs identifier for the school.",
    )
    school_linkedin_url: str | None = Field(
        default=None, alias="schoolLinkedinUrl", description="School LinkedIn page URL."
    )
    school_location_name: str | None = Field(
        default=None,
        alias="schoolLocationName",
        description="School location as one display string.",
    )
    school_name: str | None = Field(
        default=None, alias="schoolName", description="School name."
    )
    school_type: str | None = Field(
        default=None, alias="schoolType", description="School type."
    )
    school_website: str | None = Field(
        default=None, alias="schoolWebsite", description="School website domain."
    )
    start_date: str | None = Field(
        default=None, alias="startDate", description="When study started."
    )


class PeopleSearchPeopledatalabsEmail(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type_: str | None = Field(
        default=None,
        alias="type",
        description="Address kind, e.g. professional or personal.",
    )


class PeopleSearchPeopledatalabsExperience(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_continent: str | None = Field(
        default=None,
        alias="companyContinent",
        description="Employer headquarters continent.",
    )
    company_facebook_url: str | None = Field(
        default=None,
        alias="companyFacebookUrl",
        description="Employer Facebook page URL.",
    )
    company_founded: int | None = Field(
        default=None,
        alias="companyFounded",
        description="Year the employer was founded.",
    )
    company_geo: str | None = Field(
        default=None,
        alias="companyGeo",
        description='Employer headquarters coordinates as "lat,lon".',
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="People Data Labs company id for the employer.",
    )
    company_industry: str | None = Field(
        default=None, alias="companyIndustry", description="Employer industry."
    )
    company_industry_v2: str | None = Field(
        default=None,
        alias="companyIndustryV2",
        description="Employer industry on the newer PeopleDataLabs taxonomy.",
    )
    company_linkedin_id: str | None = Field(
        default=None,
        alias="companyLinkedinId",
        description="Employer LinkedIn numeric id.",
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn page URL.",
    )
    company_locality: str | None = Field(
        default=None,
        alias="companyLocality",
        description="Employer headquarters locality.",
    )
    company_location_country: str | None = Field(
        default=None,
        alias="companyLocationCountry",
        description="Employer headquarters country.",
    )
    company_location_name: str | None = Field(
        default=None,
        alias="companyLocationName",
        description="Employer headquarters location as one display string.",
    )
    company_metro: str | None = Field(
        default=None,
        alias="companyMetro",
        description="Employer headquarters metro area.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_region: str | None = Field(
        default=None,
        alias="companyRegion",
        description="Employer headquarters region or state.",
    )
    company_size: str | None = Field(
        default=None, alias="companySize", description="Employer headcount band."
    )
    company_twitter_url: str | None = Field(
        default=None,
        alias="companyTwitterUrl",
        description="Employer X or Twitter profile URL.",
    )
    company_website: str | None = Field(
        default=None, alias="companyWebsite", description="Employer website domain."
    )
    end_date: str | None = Field(
        default=None,
        alias="endDate",
        description="When the role ended, absent while the role is current.",
    )
    is_primary: bool | None = Field(
        default=None,
        alias="isPrimary",
        description="True for the role People Data Labs treats as current.",
    )
    start_date: str | None = Field(
        default=None,
        alias="startDate",
        description="When the role started: YYYY, YYYY-MM or YYYY-MM-DD.",
    )
    title: str | None = Field(default=None, description="Job title held.")
    title_class: str | None = Field(
        default=None, alias="titleClass", description="Normalized job class."
    )
    title_levels: list[str] | None = Field(
        default=None, alias="titleLevels", description="Seniority levels for the title."
    )
    title_role: str | None = Field(
        default=None, alias="titleRole", description="Normalized role for the title."
    )
    title_sub_role: str | None = Field(
        default=None, alias="titleSubRole", description="Normalized job sub-role."
    )


class PeopleSearchPeopledatalabsProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    network: str | None = Field(
        description="Network name, e.g. linkedin, facebook, twitter."
    )


class PeopleSearchProspeoData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    current_page: int | None = Field(
        default=None,
        alias="currentPage",
        description="Page number this response holds, one-based.",
    )
    people: list[PeopleSearchProspeoPeople] = Field(
        description="Matching people, each with their current employer's firmographic record. Email addresses and mobile numbers come back masked; reveal them with Person Enrichment - Prospeo."
    )
    per_page: int | None = Field(
        default=None,
        alias="perPage",
        description="Results Prospeo returns per page. Prospeo fixes this at 25 and charges one flat price per page.",
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Results matching the filters across all pages.",
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="Pages of results behind these filters.",
    )


class PeopleSearchProspeoPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company: PeopleSearchProspeoCompany | None = Field(
        default=None,
        description="The person's current employer, with Prospeo's full firmographic record.",
    )
    email: PeopleSearchProspeoEmail | None = Field(
        default=None,
        description="Work email address. Prospeo returns the address only once it is revealed; status says why it is absent otherwise.",
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="First name."
    )
    full_name: str | None = Field(alias="fullName", description="Person's full name.")
    headline: str | None = Field(default=None, description="LinkedIn headline.")
    job_change_detected_utc: float | None = Field(
        default=None,
        alias="jobChangeDetectedUtc",
        description="UTC epoch timestamp in seconds (Unix time) Prospeo last detected a job change. Multiply by 1000 for a JS Date in milliseconds.",
    )
    job_history: list[PeopleSearchProspeoJobHistory] | None = Field(
        default=None,
        alias="jobHistory",
        description="Every role Prospeo holds for the person, most recent first.",
    )
    job_key: str | None = Field(
        default=None,
        alias="jobKey",
        description="Prospeo's identifier for the current role.",
    )
    job_title: str | None = Field(
        default=None, alias="jobTitle", description="Current job title."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Last name."
    )
    linkedin_member_id: str | None = Field(
        default=None,
        alias="linkedinMemberId",
        description="LinkedIn numeric member id.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="LinkedIn profile URL."
    )
    location: PeopleSearchProspeoLocation | None = Field(
        default=None, description="Where the person is located."
    )
    mobile: PeopleSearchProspeoMobile | None = Field(
        default=None,
        description="Mobile phone number. Digits are masked until the number is revealed; send enrichMobile to reveal it.",
    )
    person_id: str | None = Field(
        default=None,
        alias="personId",
        description="Prospeo's own person identifier. Send it back as this SKU's personId input.",
    )
    skills: list[str] | None = Field(
        default=None, description="Skills the person lists."
    )


class PeopleSearchProspeoCompany(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attributes: PeopleSearchProspeoAttribute | None = Field(
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
    email_tech: PeopleSearchProspeoEmailTech | None = Field(
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
    funding: PeopleSearchProspeoFunding | None = Field(
        default=None, description="Funding history."
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    industry: str | None = Field(default=None, description="Company industry.")
    instagram_url: str | None = Field(
        default=None, alias="instagramUrl", description="Company Instagram profile URL."
    )
    job_postings: PeopleSearchProspeoJobPosting | None = Field(
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
    location: PeopleSearchProspeoLocation2 | None = Field(
        default=None, description="Company headquarters."
    )
    naics_codes: list[str] | None = Field(
        default=None,
        alias="naicsCodes",
        description="NAICS classification codes for the company.",
    )
    name: str | None = Field(default=None, description="Company name.")
    other_websites: list[str] | None = Field(
        default=None,
        alias="otherWebsites",
        description="Other domains the company owns.",
    )
    phone_hq: PeopleSearchProspeoPhoneHq | None = Field(
        default=None, alias="phoneHq", description="Headquarters switchboard number."
    )
    revenue_range: PeopleSearchProspeoRevenueRange | None = Field(
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


class PeopleSearchProspeoAttribute(BaseModel):
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


class PeopleSearchProspeoEmailTech(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str | None = Field(
        default=None, description="Domain the company's email addresses use."
    )
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider behind the domain's MX records.",
    )


class PeopleSearchProspeoFunding(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    events: list[PeopleSearchProspeoEvent] | None = Field(
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


class PeopleSearchProspeoEvent(BaseModel):
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


class PeopleSearchProspeoJobPosting(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active_count: int | None = Field(
        default=None, alias="activeCount", description="Open roles currently posted."
    )
    active_titles: list[str] | None = Field(
        default=None, alias="activeTitles", description="Titles of the open roles."
    )


class PeopleSearchProspeoLocation2(BaseModel):
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


class PeopleSearchProspeoPhoneHq(BaseModel):
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


class PeopleSearchProspeoRevenueRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    max: float | None = Field(default=None, description="Upper bound in USD.")
    min: float | None = Field(default=None, description="Lower bound in USD.")


class PeopleSearchProspeoEmail(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    email: str | None = Field(
        default=None, description="The email address, when Prospeo revealed one."
    )
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider behind the address domain, e.g. Google.",
    )
    revealed: bool | None = Field(
        default=None,
        description="True when the address below is the full value rather than a masked preview.",
    )
    status: str | None = Field(
        default=None,
        description="Prospeo's verdict for the address, e.g. VERIFIED or UNAVAILABLE.",
    )


class PeopleSearchProspeoJobHistory(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Prospeo company id for the employer.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    current: bool | None = Field(
        default=None, description="True while the role is current."
    )
    departments: list[str] | None = Field(
        default=None, description="Departments Prospeo assigns the role."
    )
    duration_months: int | None = Field(
        default=None,
        alias="durationMonths",
        description="How long the role has run, in months.",
    )
    end_month: int | None = Field(
        default=None,
        alias="endMonth",
        description="Month the role ended, absent while current.",
    )
    end_year: int | None = Field(
        default=None,
        alias="endYear",
        description="Year the role ended, absent while current.",
    )
    job_key: str | None = Field(
        default=None, alias="jobKey", description="Prospeo's identifier for this role."
    )
    seniority: str | None = Field(
        default=None, description="Seniority band, e.g. C-Suite, Manager, Entry."
    )
    start_month: int | None = Field(
        default=None, alias="startMonth", description="Month the role started, 1 to 12."
    )
    start_year: int | None = Field(
        default=None, alias="startYear", description="Year the role started."
    )
    title: str | None = Field(default=None, description="Job title held.")


class PeopleSearchProspeoLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City.")
    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="ISO 3166-1 alpha-2 country code.",
    )
    state: str | None = Field(default=None, description="State or region.")
    time_zone: str | None = Field(
        default=None,
        alias="timeZone",
        description="IANA time zone, e.g. America/New_York.",
    )
    time_zone_offset: float | None = Field(
        default=None,
        alias="timeZoneOffset",
        description="Current offset from UTC in hours.",
    )


class PeopleSearchProspeoMobile(BaseModel):
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
    mobile: str | None = Field(
        default=None, description="The number as Prospeo stores it."
    )
    national: str | None = Field(default=None, description="Number in national format.")
    revealed: bool | None = Field(
        default=None,
        description="True when the digits below are the full number rather than a masked preview.",
    )
    status: str | None = Field(
        default=None,
        description="Prospeo's verdict for the number, e.g. VERIFIED or UNAVAILABLE.",
    )


class PeopleSearchQuickenrichData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool = Field(
        alias="hasMore",
        description="Whether the upstream reports further pages beyond this one.",
    )
    page: int = Field(description="One-based page this response covers.")
    page_size: int = Field(
        alias="pageSize", description="Records per page upstream applied."
    )
    people: list[PeopleSearchQuickenrichPeople] = Field(
        description="People on this page."
    )
    total: int = Field(description="Total records matching the request.")
    total_pages: int = Field(alias="totalPages", description="Total pages available.")


class PeopleSearchQuickenrichPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Street address on the employer record."
    )
    address_line2: str | None = Field(
        default=None,
        alias="addressLine2",
        description="Second address line on the employer record.",
    )
    city: str | None = Field(default=None, description="City on the employer record.")
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_email: str | None = Field(
        default=None,
        alias="companyEmail",
        description="Public address published on the employer home page.",
    )
    company_employee_count: str | None = Field(
        default=None,
        alias="companyEmployeeCount",
        description='Employer headcount band, e.g. "20 - 99". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    company_industry: str | None = Field(
        default=None, alias="companyIndustry", description="Employer industry label."
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_phone: str | None = Field(
        default=None, alias="companyPhone", description="Employer main phone line."
    )
    company_revenue: str | None = Field(
        default=None,
        alias="companyRevenue",
        description='Employer revenue band, e.g. "1 - 2.5 Million". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    country: str | None = Field(
        default=None,
        description="ISO 3166-1 alpha-2 country code on the employer record.",
    )
    email_domain: str | None = Field(
        default=None,
        alias="emailDomain",
        description="Domain the work email resolves to.",
    )
    emp_id: str | None = Field(
        default=None,
        alias="empId",
        description="QuickEnrich's stable record id for this person, for de-duplicating across pages.",
    )
    first_name: str | None = Field(
        alias="firstName", description="Person's first name."
    )
    has_email: bool | None = Field(
        alias="hasEmail",
        description="Whether a work email is held for this person. The address itself is masked on this SKU.",
    )
    has_linkedin: bool | None = Field(
        alias="hasLinkedin",
        description="Whether a LinkedIn profile is held for this person.",
    )
    has_phone: bool | None = Field(
        alias="hasPhone",
        description="Whether a phone is held for this person. The number itself is masked on this SKU.",
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Person's last name."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Person's LinkedIn profile URL."
    )
    locality: str | None = Field(
        default=None, description="Locality on the employer record."
    )
    postal_code: str | None = Field(
        default=None,
        alias="postalCode",
        description="Postal code on the employer record.",
    )
    region: str | None = Field(
        default=None, description="State or region code on the employer record."
    )
    title: str | None = Field(default=None, description="Person's job title.")


class PeopleSearchQuickenrichCompanyData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page: int = Field(description="One-based page this response covers.")
    page_size: int = Field(
        alias="pageSize", description="Records per page upstream applied."
    )
    people: list[PeopleSearchQuickenrichCompanyPeople] = Field(
        description="People on this page."
    )
    total: int = Field(description="Total records matching the request.")
    total_pages: int = Field(alias="totalPages", description="Total pages available.")


class PeopleSearchQuickenrichCompanyPeople(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Street address on the employer record."
    )
    city: str | None = Field(default=None, description="City on the employer record.")
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_employee_count: str | None = Field(
        default=None,
        alias="companyEmployeeCount",
        description='Employer headcount band, e.g. "20 - 99". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    company_industry: str | None = Field(
        default=None, alias="companyIndustry", description="Employer industry label."
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_phone: str | None = Field(
        default=None, alias="companyPhone", description="Employer main phone line."
    )
    company_revenue: str | None = Field(
        default=None,
        alias="companyRevenue",
        description='Employer revenue band, e.g. "1 - 2.5 Million". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    country: str | None = Field(
        default=None,
        description="ISO 3166-1 alpha-2 country code on the employer record.",
    )
    email: str | None = Field(default=None, description="Work email address.")
    email_domain: str | None = Field(
        default=None,
        alias="emailDomain",
        description="Domain the work email resolves to.",
    )
    email_verified_utc: float | None = Field(
        default=None,
        alias="emailVerifiedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    first_name: str | None = Field(
        alias="firstName", description="Person's first name."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Person's last name."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Person's LinkedIn profile URL."
    )
    phone: str | None = Field(
        default=None,
        description="Direct business phone line held for the person. Mostly desk lines; read phoneType before treating it as a mobile.",
    )
    phone_type: str | None = Field(
        default=None,
        alias="phoneType",
        description='Line type reported upstream, e.g. "mobile" or "landline".',
    )
    postal_code: str | None = Field(
        default=None,
        alias="postalCode",
        description="Postal code on the employer record.",
    )
    region: str | None = Field(
        default=None, description="State or region code on the employer record."
    )
    title: str | None = Field(default=None, description="Person's job title.")


class PeopleSearchNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ai_ark(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchAiArkInput],
    ) -> RunResult[PeopleSearchAiArkData]:
        """People Search - AI Ark

        Search professional profiles with account, contact, and saved-list filters.

        Price: $0 per request plus $0.0084 per result (maximum $0.84).

        Example:
            res = client.people_search.ai_ark(page=0, size=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.ai_ark", dict(input), options
        )
        return RunResult[PeopleSearchAiArkData].model_validate(raw)

    def crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchCrustdataInput],
    ) -> RunResult[PeopleSearchCrustdataData]:
        """People Search - Crustdata

        Find up to 100 professional profiles by company domain and title keywords.

        Price: $0.0012 per request plus $0.00144 per result (maximum $0.1452).

        Example:
            res = client.people_search.crustdata(companyDomain="posthog.com", limit=1, titleKeywords="engineer")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.crustdata", dict(input), options
        )
        return RunResult[PeopleSearchCrustdataData].model_validate(raw)

    def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchCrustdataV3Input],
    ) -> RunResult[PeopleSearchCrustdataV3Data]:
        """People Search - Crustdata v3 (legacy)

        Find up to 100 professional profiles by company domain and title keywords.

        Price: $0.144 per request.

        Example:
            res = client.people_search.crustdata_v3(companyDomain="posthog.com", limit=1, titleKeywords="engineer")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.crustdata_v3", dict(input), options
        )
        return RunResult[PeopleSearchCrustdataV3Data].model_validate(raw)

    def fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchFullenrichInput],
    ) -> RunResult[PeopleSearchFullenrichData]:
        """People Search - FullEnrich

        Prospect FullEnrich's person database by title, seniority, function, skill,
        language and location, plus any current or past employer firmographic. Every
        row carries the person's employer record. Billed per person returned.

        Price: $0 per request plus $0.0252 per result (maximum $2.52).

        Example:
            res = client.people_search.fullenrich(currentCompanyDomains=[{"exact_match": True, "value": "stripe.com"}], limit=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.fullenrich", dict(input), options
        )
        return RunResult[PeopleSearchFullenrichData].model_validate(raw)

    def iter_fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchFullenrichInput],
    ) -> Paginator[PeopleSearchFullenrichPeople, PeopleSearchFullenrichData]:
        """Iterate People Search - FullEnrich results, following pagination cursors.

        Yields validated `PeopleSearchFullenrichPeople` items from the `people` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "people_search.fullenrich",
            dict(input),
            "people",
            item_model=PeopleSearchFullenrichPeople,
            data_model=PeopleSearchFullenrichData,
            bare=False,
            options=options,
        )

    def lusha(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchLushaInput],
    ) -> RunResult[PeopleSearchLushaData]:
        """People Search - Lusha

        Prospect Lusha's contact database by department, seniority, job title,
        location, company size, industry and technology. One flat price per page;
        reveal a contact's email and phone with Person Enrichment - Lusha.

        Price: $0.084 per request.

        Example:
            res = client.people_search.lusha(filters={"companies": {"include": {"names": ["PostHog"]}}, "contacts": {"include": {"departments": ["Engineering & Technical"]}}}, pages={"page": 0, "size": 10})
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.lusha", dict(input), options
        )
        return RunResult[PeopleSearchLushaData].model_validate(raw)

    def peopledatalabs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchPeopledatalabsInput],
    ) -> RunResult[PeopleSearchPeopledatalabsData]:
        """People Search - People Data Labs

        Search People Data Labs' person dataset with SQL or an Elasticsearch query.
        Results carry the professional and firmographic record plus availability
        flags for contact data; pull the actual email and phone with Person
        Enrichment - People Data Labs. Billed per profile returned.

        Price: $0 per request plus $0.168 per result (maximum $9.912).

        Example:
            res = client.people_search.peopledatalabs(limit=1, sql="SELECT * FROM person WHERE job_company_website = 'posthog.com'")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.peopledatalabs", dict(input), options
        )
        return RunResult[PeopleSearchPeopledatalabsData].model_validate(raw)

    def prospeo(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchProspeoInput],
    ) -> RunResult[PeopleSearchProspeoData]:
        """People Search - Prospeo

        Prospect Prospeo's contact database by job title, department, seniority,
        experience, location and any company firmographic. One flat price per page
        of 25.

        Price: $0.066 per request.

        Example:
            res = client.people_search.prospeo(company={"websites": {"include": ["stripe.com"]}}, page=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.prospeo", dict(input), options
        )
        return RunResult[PeopleSearchProspeoData].model_validate(raw)

    def quickenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchQuickenrichInput],
    ) -> RunResult[PeopleSearchQuickenrichData]:
        """People Search - QuickEnrich

        Build a prospect list by title, industry, headcount, revenue, or location,
        and see which people have a work email or phone on file before you pay to
        reveal one. Contact values themselves are masked here; use Person Enrichment
        or the QuickEnrich company contacts search to resolve them.

        Price: $0.0005 per request.

        Example:
            res = client.people_search.quickenrich(country={"include": ["US"]}, hasEmail=True, limit=2, title={"include": ["CEO"]})
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.quickenrich", dict(input), options
        )
        return RunResult[PeopleSearchQuickenrichData].model_validate(raw)

    def quickenrich_company(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchQuickenrichCompanyInput],
    ) -> RunResult[PeopleSearchQuickenrichCompanyData]:
        """People Search - QuickEnrich Company Contacts

        List the known contacts at one company domain, with work emails and direct
        phone lines where they are held. Returns up to 20 people per page for a flat
        per-request price. Coverage is strongest for small and local businesses.

        Price: $0.0072 per request.

        Example:
            res = client.people_search.quickenrich_company(companyDomain="southmemphisfence.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.quickenrich_company", dict(input), options
        )
        return RunResult[PeopleSearchQuickenrichCompanyData].model_validate(raw)


class AsyncPeopleSearchNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ai_ark(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchAiArkInput],
    ) -> RunResult[PeopleSearchAiArkData]:
        """People Search - AI Ark

        Search professional profiles with account, contact, and saved-list filters.

        Price: $0 per request plus $0.0084 per result (maximum $0.84).

        Example:
            res = client.people_search.ai_ark(page=0, size=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.ai_ark", dict(input), options
        )
        return RunResult[PeopleSearchAiArkData].model_validate(raw)

    async def crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchCrustdataInput],
    ) -> RunResult[PeopleSearchCrustdataData]:
        """People Search - Crustdata

        Find up to 100 professional profiles by company domain and title keywords.

        Price: $0.0012 per request plus $0.00144 per result (maximum $0.1452).

        Example:
            res = client.people_search.crustdata(companyDomain="posthog.com", limit=1, titleKeywords="engineer")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.crustdata", dict(input), options
        )
        return RunResult[PeopleSearchCrustdataData].model_validate(raw)

    async def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchCrustdataV3Input],
    ) -> RunResult[PeopleSearchCrustdataV3Data]:
        """People Search - Crustdata v3 (legacy)

        Find up to 100 professional profiles by company domain and title keywords.

        Price: $0.144 per request.

        Example:
            res = client.people_search.crustdata_v3(companyDomain="posthog.com", limit=1, titleKeywords="engineer")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.crustdata_v3", dict(input), options
        )
        return RunResult[PeopleSearchCrustdataV3Data].model_validate(raw)

    async def fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchFullenrichInput],
    ) -> RunResult[PeopleSearchFullenrichData]:
        """People Search - FullEnrich

        Prospect FullEnrich's person database by title, seniority, function, skill,
        language and location, plus any current or past employer firmographic. Every
        row carries the person's employer record. Billed per person returned.

        Price: $0 per request plus $0.0252 per result (maximum $2.52).

        Example:
            res = client.people_search.fullenrich(currentCompanyDomains=[{"exact_match": True, "value": "stripe.com"}], limit=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.fullenrich", dict(input), options
        )
        return RunResult[PeopleSearchFullenrichData].model_validate(raw)

    def iter_fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchFullenrichInput],
    ) -> AsyncPaginator[PeopleSearchFullenrichPeople, PeopleSearchFullenrichData]:
        """Iterate People Search - FullEnrich results, following pagination cursors.

        Yields validated `PeopleSearchFullenrichPeople` items from the `people` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "people_search.fullenrich",
            dict(input),
            "people",
            item_model=PeopleSearchFullenrichPeople,
            data_model=PeopleSearchFullenrichData,
            bare=False,
            options=options,
        )

    async def lusha(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchLushaInput],
    ) -> RunResult[PeopleSearchLushaData]:
        """People Search - Lusha

        Prospect Lusha's contact database by department, seniority, job title,
        location, company size, industry and technology. One flat price per page;
        reveal a contact's email and phone with Person Enrichment - Lusha.

        Price: $0.084 per request.

        Example:
            res = client.people_search.lusha(filters={"companies": {"include": {"names": ["PostHog"]}}, "contacts": {"include": {"departments": ["Engineering & Technical"]}}}, pages={"page": 0, "size": 10})
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.lusha", dict(input), options
        )
        return RunResult[PeopleSearchLushaData].model_validate(raw)

    async def peopledatalabs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchPeopledatalabsInput],
    ) -> RunResult[PeopleSearchPeopledatalabsData]:
        """People Search - People Data Labs

        Search People Data Labs' person dataset with SQL or an Elasticsearch query.
        Results carry the professional and firmographic record plus availability
        flags for contact data; pull the actual email and phone with Person
        Enrichment - People Data Labs. Billed per profile returned.

        Price: $0 per request plus $0.168 per result (maximum $9.912).

        Example:
            res = client.people_search.peopledatalabs(limit=1, sql="SELECT * FROM person WHERE job_company_website = 'posthog.com'")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.peopledatalabs", dict(input), options
        )
        return RunResult[PeopleSearchPeopledatalabsData].model_validate(raw)

    async def prospeo(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchProspeoInput],
    ) -> RunResult[PeopleSearchProspeoData]:
        """People Search - Prospeo

        Prospect Prospeo's contact database by job title, department, seniority,
        experience, location and any company firmographic. One flat price per page
        of 25.

        Price: $0.066 per request.

        Example:
            res = client.people_search.prospeo(company={"websites": {"include": ["stripe.com"]}}, page=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.prospeo", dict(input), options
        )
        return RunResult[PeopleSearchProspeoData].model_validate(raw)

    async def quickenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchQuickenrichInput],
    ) -> RunResult[PeopleSearchQuickenrichData]:
        """People Search - QuickEnrich

        Build a prospect list by title, industry, headcount, revenue, or location,
        and see which people have a work email or phone on file before you pay to
        reveal one. Contact values themselves are masked here; use Person Enrichment
        or the QuickEnrich company contacts search to resolve them.

        Price: $0.0005 per request.

        Example:
            res = client.people_search.quickenrich(country={"include": ["US"]}, hasEmail=True, limit=2, title={"include": ["CEO"]})
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.quickenrich", dict(input), options
        )
        return RunResult[PeopleSearchQuickenrichData].model_validate(raw)

    async def quickenrich_company(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PeopleSearchQuickenrichCompanyInput],
    ) -> RunResult[PeopleSearchQuickenrichCompanyData]:
        """People Search - QuickEnrich Company Contacts

        List the known contacts at one company domain, with work emails and direct
        phone lines where they are held. Returns up to 20 people per page for a flat
        per-request price. Coverage is strongest for small and local businesses.

        Price: $0.0072 per request.

        Example:
            res = client.people_search.quickenrich_company(companyDomain="southmemphisfence.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "people_search.quickenrich_company", dict(input), options
        )
        return RunResult[PeopleSearchQuickenrichCompanyData].model_validate(raw)
