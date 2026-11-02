# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the company_search platform."""

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


class CompanySearchAiArkInput(TypedDict, total=False):
    """Input for Company Search - AI Ark."""

    account: NotRequired[dict[str, Any]]
    """AI Ark account filter expression. Nested generic any/all filter objects are accepted as documented by the source and are not further constrained."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lists: NotRequired[dict[str, Any]]
    """AI Ark saved-list filter expression."""
    lookalikeDomains: NotRequired[list[str]]
    """Domains whose company characteristics should guide the search."""
    name: NotRequired[str]
    """Company-name search text."""
    page: NotRequired[int]
    """Zero-based result page. Minimum: 0. Default: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    size: NotRequired[int]
    """Maximum companies to return on this page. Range: 1 to 100. Default: 10."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanySearchCrustdataInput(TypedDict, total=False):
    """Input for Company Search - Crustdata."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    fields: NotRequired[Any]
    """Response groups to return. Omit for the default set: basic_info, headcount, funding, revenue, locations, social_profiles, taxonomy, followers and metadata."""
    filters: Required[dict[str, Any]]
    """Crustdata company-search filter expression. A condition is {"field": <field>, "type": <operator>, "value": <match>}; a group is {"op": "and"|"or", "conditions": [<condition or group>, ...]}. Pass one condition or one group. Operators: = != < =< > => in not_in (.) (fuzzy text) [.] (exact token). Common fields: basic_info.primary_domain, basic_info.name, basic_info.industries, basic_info.employee_count_range, basic_info.year_founded, headcount.total, headcount.growth_percent.12m, locations.country, locations.headquarters, taxonomy.professional_network_industry, funding.last_round_type, funding.total_investment_usd, funding.last_fundraise_date, revenue.estimated.lower_bound_usd, followers.count. An `in` list takes at most 5 values."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum companies to return on this page. Every company returned is billed; the page is capped at 250 to bound the cost of a single call. Range: 1 to 250. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    sorts: NotRequired[list[dict[str, Any]]]
    """Sort directives applied in order, each {"field": <field>, "order": "asc"|"desc"}. Sortable fields include basic_info.name, basic_info.year_founded, headcount.total, funding.total_investment_usd, funding.last_fundraise_date, revenue.estimated.lower_bound_usd and followers.count."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanySearchCrustdataV3Input(TypedDict, total=False):
    """Input for Company Search - Crustdata v3 (legacy)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    fields: NotRequired[Any]
    filters: Required[Any]
    """Crustdata company-database filter expression. A leaf condition is {"filter_type": <column>, "type": <operator>, "value": <match>}; a group is {"op": "and"|"or", "conditions": [<leaf>, ...]}. Pass a single leaf, an array of leaves, or a group. See the example for a domain lookup."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum companies to return on this page. Every company returned is billed; the page is capped at 250 to bound the cost of a single call. Range: 1 to 250. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    sorts: NotRequired[list[dict[str, Any]]]
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanySearchFullenrichInput(TypedDict, total=False):
    """Input for Company Search - FullEnrich."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyIds: NotRequired[list[dict[str, Any]]]
    """Filter by FullEnrich company id. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    cursor: NotRequired[str]
    """Cursor from a previous response's nextCursor. Works at any depth, including past the 10000 offset ceiling."""
    domains: NotRequired[list[dict[str, Any]]]
    """Filter by company domain, e.g. stripe.com. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    foundedYears: NotRequired[list[dict[str, Any]]]
    """Filter by founding year. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    headcounts: NotRequired[list[dict[str, Any]]]
    """Filter by employee headcount band. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    headquartersLocations: NotRequired[list[dict[str, Any]]]
    """Filter by headquarters city, region or country. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    industries: NotRequired[list[dict[str, Any]]]
    """Filter by company industry, e.g. Software Development. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    keywords: NotRequired[list[dict[str, Any]]]
    """Filter by words in the company description. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    limit: NotRequired[int]
    """Rows to return on this page, up to FullEnrich's maximum of 100. Every row returned is billed. Range: 1 to 100. Default: 10."""
    linkedinUrls: NotRequired[list[dict[str, Any]]]
    """Filter by company LinkedIn URL. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    names: NotRequired[list[dict[str, Any]]]
    """Filter by company name. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    offset: NotRequired[int]
    """Rows to skip. FullEnrich caps offset at 10000; past that, page with cursor. Minimum: 0. Default: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    specialties: NotRequired[list[dict[str, Any]]]
    """Filter by company specialty. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""
    types: NotRequired[list[dict[str, Any]]]
    """Filter by ownership type, e.g. Public Company, Privately Held, Nonprofit. Each entry is an object taking a `value` string and an optional `exact_match` boolean, e.g. [{"value": "stripe.com", "exact_match": true}]. A bare string is rejected."""


class CompanySearchPeopledatalabsInput(TypedDict, total=False):
    """Input for Company Search - People Data Labs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    dataInclude: NotRequired[str]
    """Comma-separated People Data Labs fields to include, or a leading - list to exclude. Projection changes the payload only; billing still follows companies returned."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum companies to return. Every company returned is billed, so start at 1 to check a query and read total before asking for more. Range: 1 to 83. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: NotRequired[dict[str, Any]]
    """Elasticsearch-style query over the People Data Labs company dataset, e.g. {"bool": {"must": [{"term": {"website": "posthog.com"}}]}}. Send this or sql, never both."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    sql: NotRequired[str]
    """People Data Labs SQL, in the form SELECT * FROM company WHERE ... . String literals take single quotes, only SELECT * is supported, and field names must be real People Data Labs company fields including nested subfields such as location.country. Do not include a LIMIT clause; People Data Labs rejects it. Use limit instead. Send this or query, never both."""
    titlecase: NotRequired[bool]
    """Return text in title case instead of People Data Labs' lowercase default."""


class CompanySearchProspeoInput(TypedDict, total=False):
    """Input for Company Search - Prospeo."""

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
    page: NotRequired[int]
    """Page number, one-based. Prospeo returns 25 results per page and charges one flat price per page. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanySearchQuickenrichInput(TypedDict, total=False):
    """Input for Company Search - QuickEnrich."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    city: NotRequired[dict[str, Any]]
    """Filter on city name."""
    companyDomain: NotRequired[dict[str, Any]]
    """Filter on company website domain. Include only; exclude is rejected upstream."""
    companyName: NotRequired[dict[str, Any]]
    """Filter on company name."""
    country: NotRequired[dict[str, Any]]
    """Filter on ISO 3166-1 alpha-2 country code, e.g. "US"."""
    employeeCount: NotRequired[dict[str, Any]]
    """Filter on headcount band. Note these bands differ from the employeeCount string returned on a result."""
    homePageText: NotRequired[dict[str, Any]]
    """Filter on words found in the company home page text."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeFullText: NotRequired[bool]
    """Return the full home page text on each company instead of a snippet."""
    industry: NotRequired[dict[str, Any]]
    """Filter on industry label. Values must match the QuickEnrich industry vocabulary exactly, e.g. "IT Services and IT Consulting"."""
    limit: NotRequired[int]
    """Maximum companies to return on this page. Every company returned is billed. Range: 1 to 100. Default: 10."""
    linkedinBio: NotRequired[dict[str, Any]]
    """Filter on words found in the company LinkedIn bio."""
    page: NotRequired[int]
    """One-based result page. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    revenue: NotRequired[dict[str, Any]]
    """Filter on revenue band."""
    services: NotRequired[dict[str, Any]]
    """Filter on the services a company lists."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanySearchTheirstackInput(TypedDict, total=False):
    """Input for Company Search - TheirStack."""

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
    expandTechnologySlugs: NotRequired[list[str]]
    """Specify technology slugs to include detailed technology usage information for each company. The response will include a 'technologies_found' field containing metrics like confidence score, ranking, and job count for each specified technology. Note: If a technology is not listed for a company, it means that company does not use that technology. This feature is useful for enriching company data with their technology stack details."""
    fundingStageOr: NotRequired[list[str]]
    """Funding stages of companies returned. Possible values: ['angel', 'convertible_note', 'debt_financing', 'equity_crowdfunding', 'other', 'private_equity', 'seed', 'series_a', 'series_b', 'series_c', 'series_d', 'series_e', 'series_f', 'series_g', 'series_h', 'venture_round_not_specified', 'series_i', 'series_j', 'undisclosed', 'series_unknown', 'pre_seed', 'post_ipo_secondary', 'post_ipo_equity', 'post_ipo_debt', 'non_equity_assistance', 'late_vc', 'initial_coin_offering', 'growth_equity_vc', 'grant', 'early_vc', 'corporate_round', 'secondary_market', 'product_crowdfunding']"""
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
    jobFilters: NotRequired[dict[str, Any]]
    keywordSlugAnd: NotRequired[list[str]]
    """Return results from companies that have mentioned all of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    keywordSlugNot: NotRequired[list[str]]
    """Return results from companies that haven't mentioned any of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    keywordSlugOr: NotRequired[list[str]]
    """Return results from companies that have mentioned any of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    lastFundingRoundDateGte: NotRequired[str]
    """Only return companies whose last funding round date is after or on this date. Format: 'YYYY-MM-DD'"""
    lastFundingRoundDateLte: NotRequired[str]
    """Only return companies whose last funding round date is before or on this date. Format: 'YYYY-MM-DD'"""
    limit: NotRequired[int]
    """Rows to return on this page, up to TheirStack's maximum of 500. Every row returned is billed. Range: 1 to 50. Default: 25."""
    maxEmployeeCount: NotRequired[int]
    """Maximum number of employees in a company"""
    maxEmployeeCountOrNull: NotRequired[int]
    """Maximum number of employees in a company. If we don't have company size information, we will return it as well."""
    maxFundingUsd: NotRequired[int]
    """Maximum company funding, in USD"""
    maxRevenueUsd: NotRequired[int]
    """Maximum company revenue, in USD"""
    minEmployeeCount: NotRequired[int]
    """Minimum number of employees in a company"""
    minEmployeeCountOrNull: NotRequired[int]
    """Minimum number of employees in a company. If we don't have company size information, we will return it as well."""
    minFundingUsd: NotRequired[int]
    """Minimum company funding, in USD"""
    minRevenueUsd: NotRequired[int]
    """Minimum company revenue, in USD"""
    offset: NotRequired[int]
    """Number of results to skip. Required for offset-based pagination."""
    onlyYcCompanies: NotRequired[bool]
    """Only return YC companies"""
    orderBy: NotRequired[list[str]]
    """List of column objects. You can pass several columns to order by, in order of priority. Only `field` is required, `desc` is True by default"""
    page: NotRequired[int]
    """Page number. Required when using page-based pagination."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    propertyExistsAnd: NotRequired[list[str]]
    """Return companies that have all of these fields not null. For example, if you pass ['domain', 'linkedin_url'], it will return companies that have both domain AND linkedin_url set."""
    propertyExistsOr: NotRequired[list[str]]
    """Return companies that have any of these fields not null. For example, if you pass ['domain', 'linkedin_url'], it will return companies that have a domain OR a linkedin_url set."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    techFilters: NotRequired[dict[str, Any]]
    """Filter by technologies and buying intent topics detected for the company"""
    technologySlugAnd: NotRequired[list[str]]
    """Return results from companies that have mentioned all of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    technologySlugNot: NotRequired[list[str]]
    """Return results from companies that haven't mentioned any of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""
    technologySlugOr: NotRequired[list[str]]
    """Return results from companies that have mentioned any of these keywords in their jobs. Case sensitive. Pass slugs. Check out all the keywords we track at GET /v0/catalog/keywords"""


class CompanySearchAiArkData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchAiArkCompanie] = Field(
        description="Companies returned on this page."
    )
    page: int = Field(
        description="Zero-based page number returned by the source. Minimum: 0."
    )
    size: int = Field(description="Configured page size. Minimum: 0.")
    total: int = Field(description="Total matching companies. Minimum: 0.")
    total_pages: int = Field(
        alias="totalPages", description="Total result pages. Minimum: 0."
    )


class CompanySearchAiArkCompanie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Headquarters address as published by the source."
    )
    city: str | None = Field(default=None, description="Headquarters city.")
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="The source's own record identifier for this company, exposed so you can trace a result back to the record it came from.",
    )
    continent: str | None = Field(default=None, description="Headquarters continent.")
    country: str | None = Field(default=None, description="Headquarters country.")
    crunchbase_url: str | None = Field(
        default=None, alias="crunchbaseUrl", description="Company Crunchbase URL."
    )
    description: str | None = Field(
        default=None, description="Company description when available."
    )
    diversity_investment_count: int | None = Field(
        default=None,
        alias="diversityInvestmentCount",
        description="Number of diversity-flagged investments the source records for the company. Minimum: 0.",
    )
    diversity_investments: list[CompanySearchAiArkDiversityInvestment] | None = Field(
        default=None,
        alias="diversityInvestments",
        description="Investments the source has flagged with a diversity spotlight.",
    )
    domain: str | None = Field(
        description="Company website domain, or null when the upstream holds none for this company."
    )
    domain_ltd: str | None = Field(
        default=None,
        alias="domainLtd",
        description="The source's second copy of the company domain. Usually identical to domain; it can differ when the source resolves a redirect or a country domain differently, so compare the two rather than assuming they match.",
    )
    email: str | None = Field(default=None, description="Public company contact email.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Estimated total employees. Minimum: 0.",
    )
    employee_range_max: int | None = Field(
        default=None,
        alias="employeeRangeMax",
        description="Upper bound of the published employee range. Minimum: 0.",
    )
    employee_range_min: int | None = Field(
        default=None,
        alias="employeeRangeMin",
        description="Lower bound of the published employee range. Minimum: 0.",
    )
    facebook_url: str | None = Field(
        default=None, alias="facebookUrl", description="Canonical company Facebook URL."
    )
    founded_year: int | None = Field(
        default=None, alias="foundedYear", description="Year the company was founded."
    )
    funded_utc: int | None = Field(
        default=None,
        alias="fundedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    funding_last_amount: int | None = Field(
        default=None,
        alias="fundingLastAmount",
        description="Amount raised in the most recent round in USD. Minimum: 0.",
    )
    funding_last_type: str | None = Field(
        default=None,
        alias="fundingLastType",
        description="Type of the most recent funding round.",
    )
    funding_round_count: int | None = Field(
        default=None,
        alias="fundingRoundCount",
        description="Number of funding rounds raised. Minimum: 0.",
    )
    funding_rounds: list[CompanySearchAiArkFundingRound] | None = Field(
        default=None,
        alias="fundingRounds",
        description="Funding rounds the company has raised.",
    )
    funding_total_amount: int | None = Field(
        default=None,
        alias="fundingTotalAmount",
        description="Total capital raised across all rounds in USD. Minimum: 0.",
    )
    hashtags: list[str] | None = Field(
        default=None, description="Hashtags the company publishes under."
    )
    image: str | None = Field(
        default=None,
        description="Company logo URL. This is a SIGNED, EXPIRING image-proxy URL - the path carries an exp: epoch roughly five days out - so fetch and store the image promptly rather than storing this URL.",
    )
    industries: list[str] | None = Field(
        default=None, description="Additional company industries."
    )
    industry: str | None = Field(default=None, description="Primary company industry.")
    investor_count: int | None = Field(
        default=None,
        alias="investorCount",
        description="Number of distinct investors. Minimum: 0.",
    )
    keywords: list[str] | None = Field(
        default=None, description="Keywords describing the company."
    )
    languages: list[str] | None = Field(
        default=None, description="Languages the company publishes in."
    )
    latitude: float | None = Field(
        default=None, description="Headquarters latitude in decimal degrees."
    )
    legal_name: str | None = Field(
        default=None,
        alias="legalName",
        description="Registered company name when available.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical company LinkedIn URL."
    )
    locations: list[CompanySearchAiArkLocation] | None = Field(
        default=None,
        description="Every office location the source lists for the company.",
    )
    longitude: float | None = Field(
        default=None, description="Headquarters longitude in decimal degrees."
    )
    naics: list[str] | None = Field(
        default=None, description="NAICS codes for the company."
    )
    name: str | None = Field(description="Company name.")
    overview: str | None = Field(
        default=None,
        description="Longer company overview written by the source. Overlaps description but is a separately maintained blurb and is often longer or more current.",
    )
    phone: str | None = Field(
        default=None, description="Sanitized public company phone number."
    )
    phone_raw: str | None = Field(
        default=None,
        alias="phoneRaw",
        description="The same phone number in the source's unsanitized spelling, keeping spaces, dashes and brackets. Use phone for dialing and this for display fidelity.",
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Headquarters postal code."
    )
    revenue_max: int | None = Field(
        default=None,
        alias="revenueMax",
        description="Upper bound of estimated annual revenue in USD. Minimum: 0.",
    )
    revenue_min: int | None = Field(
        default=None,
        alias="revenueMin",
        description="Lower bound of estimated annual revenue in USD. Minimum: 0.",
    )
    revenue_range: str | None = Field(
        default=None,
        alias="revenueRange",
        description="The same annual revenue estimate as a single hyphenated range string, for example 500000000-1000000000. It duplicates revenueMin and revenueMax; use those for arithmetic.",
    )
    seo_description: str | None = Field(
        default=None,
        alias="seoDescription",
        description="The meta description the source scraped from the company website. It is site copy, not the source's own writing, so it may be in another language or out of date.",
    )
    sic: list[str] | None = Field(
        default=None, description="SIC codes for the company."
    )
    state: str | None = Field(default=None, description="Headquarters state or region.")
    technologies: list[CompanySearchAiArkTechnologie] | None = Field(
        default=None, description="Technologies detected on the company's web presence."
    )
    twitter_url: str | None = Field(
        default=None,
        alias="twitterUrl",
        description="Canonical company X (Twitter) URL.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Company organization type."
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    website_url: str | None = Field(
        default=None, alias="websiteUrl", description="Canonical company website URL."
    )


class CompanySearchAiArkDiversityInvestment(BaseModel):
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
    round_image_key: str | None = Field(
        default=None,
        alias="roundImageKey",
        description="The source's internal image key for the round. It is a bare key, not a URL.",
    )
    round_name: str | None = Field(
        default=None,
        alias="roundName",
        description="Funding round name as published by the source.",
    )
    round_raised_amount: int | None = Field(
        default=None,
        alias="roundRaisedAmount",
        description="Amount raised in this round in USD. Minimum: 0.",
    )
    round_record_id: str | None = Field(
        default=None,
        alias="roundRecordId",
        description="The source's own slug for the funding round.",
    )
    round_type: str | None = Field(
        default=None,
        alias="roundType",
        description="Funding round type, for example GRANT.",
    )
    spotlights: list[CompanySearchAiArkSpotlight] | None = Field(
        default=None,
        description="Diversity spotlights the source attached to this investment.",
    )


class CompanySearchAiArkSpotlight(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = Field(
        default=None, description="Human-readable spotlight label."
    )
    record_id: str | None = Field(
        default=None,
        alias="recordId",
        description="The source's own slug for the spotlight, for example women-founded.",
    )


class CompanySearchAiArkFundingRound(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    announced_utc: int | None = Field(
        default=None,
        alias="announcedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    investors: list[str] | None = Field(
        default=None, description="Investors named in this round."
    )
    raised_amount: int | None = Field(
        default=None,
        alias="raisedAmount",
        description="Amount raised in this round in USD. Minimum: 0.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Funding round type."
    )


class CompanySearchAiArkLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Location address as published by the source."
    )
    city: str | None = Field(default=None, description="Location city.")
    continent: str | None = Field(default=None, description="Location continent.")
    country: str | None = Field(default=None, description="Location country.")
    latitude: float | None = Field(
        default=None, description="Location latitude in decimal degrees."
    )
    longitude: float | None = Field(
        default=None, description="Location longitude in decimal degrees."
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Location postal code."
    )
    state: str | None = Field(default=None, description="Location state or region.")


class CompanySearchAiArkTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")

    category: str | None = Field(default=None, description="Technology category.")
    name: str | None = Field(default=None, description="Technology name.")


class CompanySearchCrustdataData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchCrustdataCompanie] = Field(
        description="Matching companies."
    )
    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when more companies exist beyond this page.",
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque continuation token; null when the walk is complete.",
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total number of companies matching the filters. Minimum: 0.",
    )


class CompanySearchCrustdataCompanie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    acquisition_status: str | None = Field(
        default=None,
        alias="acquisitionStatus",
        description="Acquisition status, when the company has been acquired.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata identifier for the company, accepted by the Company Enrichment endpoint.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Company type, e.g. Privately Held or Public Company.",
    )
    contact_email: str | None = Field(
        default=None,
        alias="contactEmail",
        description="Publicly listed contact email address.",
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
        default=None,
        description="Primary website domain, or null when the upstream holds none for this company.",
    )
    domains: list[str] | None = Field(
        default=None, description="All domains associated with the company."
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Latest observed employee count.",
    )
    employee_growth: CompanySearchCrustdataEmployeeGrowth | None = Field(
        default=None,
        alias="employeeGrowth",
        description="Headcount change over trailing windows, absolute and percent.",
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
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="Latest LinkedIn follower count.",
    )
    follower_growth: CompanySearchCrustdataFollowerGrowth | None = Field(
        default=None,
        alias="followerGrowth",
        description="LinkedIn follower change over trailing windows, in percent.",
    )
    founded_year: int | None = Field(
        default=None, alias="foundedYear", description="Year the company was founded."
    )
    growth_calculated_utc: int | None = Field(
        default=None,
        alias="growthCalculatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the growth metrics on this record were last calculated.",
    )
    headquarters: str | None = Field(default=None, description="Headquarters location.")
    hq_country: str | None = Field(
        default=None, alias="hqCountry", description="Country of the headquarters."
    )
    hq_street_address_and_city: str | None = Field(
        default=None,
        alias="hqStreetAddressAndCity",
        description="Headquarters street address and city. Crustdata returns the same string as headquarters for most companies.",
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    indexed_utc: int | None = Field(
        default=None,
        alias="indexedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When Crustdata last indexed the record for search, which is usually just after updatedUtc.",
    )
    industries: list[str] | None = Field(
        default=None, description="All LinkedIn industries listed for the company."
    )
    industry: str | None = Field(default=None, description="Primary LinkedIn industry.")
    investors: list[str] | None = Field(
        default=None, description="Investors named on the Crunchbase profile."
    )
    is_investor: bool | None = Field(
        default=None,
        alias="isInvestor",
        description="True when the company itself invests in other companies.",
    )
    largest_headcount_country: str | None = Field(
        default=None,
        alias="largestHeadcountCountry",
        description="Country holding the largest share of employees.",
    )
    last_funding_type: str | None = Field(
        default=None,
        alias="lastFundingType",
        description="Type of the most recent funding round, e.g. series_e.",
    )
    last_funding_usd: int | None = Field(
        default=None,
        alias="lastFundingUsd",
        description="Amount raised in the most recent funding round, in USD.",
    )
    last_funding_utc: int | None = Field(
        default=None,
        alias="lastFundingUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Date of the most recent funding round.",
    )
    linkedin_categories: list[str] | None = Field(
        default=None,
        alias="linkedinCategories",
        description="LinkedIn speciality tags listed by the company.",
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
    markets: list[str] | None = Field(
        default=None,
        description="Markets the company trades in, e.g. PRIVATE or NASDAQ.",
    )
    name: str | None = Field(description="Company name.")
    office_addresses: Any | None = Field(
        default=None,
        alias="officeAddresses",
        description="Office addresses exactly as Crustdata returns them. Untyped passthrough: the structure ships verbatim and is not validated, because it was empty for every company we captured.",
    )
    phone: str | None = Field(default=None, description="Publicly listed phone number.")
    stock_symbols: list[str] | None = Field(
        default=None, alias="stockSymbols", description="Stock ticker symbols."
    )
    total_funding_usd: int | None = Field(
        default=None,
        alias="totalFundingUsd",
        description="Total investment raised to date, in USD.",
    )
    twitter_url: str | None = Field(
        default=None, alias="twitterUrl", description="X (Twitter) profile URL."
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When this company record was last refreshed.",
    )
    website: str | None = Field(default=None, description="Company website URL.")


class CompanySearchCrustdataEmployeeGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    absolute12m: int | None = Field(
        default=None, description="Net change over the last twelve months."
    )
    absolute1m: int | None = Field(
        default=None, description="Net change over the last month."
    )
    absolute3m: int | None = Field(
        default=None, description="Net change over the last three months."
    )
    absolute6m: int | None = Field(
        default=None, description="Net change over the last six months."
    )
    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent1m: float | None = Field(
        default=None, description="Percent change over the last month."
    )
    percent3m: float | None = Field(
        default=None, description="Percent change over the last three months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class CompanySearchCrustdataFollowerGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent1m: float | None = Field(
        default=None, description="Percent change over the last month."
    )
    percent3m: float | None = Field(
        default=None, description="Percent change over the last three months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class CompanySearchCrustdataV3Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchCrustdataV3Companie] = Field(
        description="Matching companies."
    )
    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when more companies exist beyond this page.",
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque continuation token; null when the walk is complete.",
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total number of companies matching the filters. Minimum: 0.",
    )


class CompanySearchCrustdataV3Companie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    acquisition_status: str | None = Field(
        default=None,
        alias="acquisitionStatus",
        description="Acquisition status, when the company has been acquired.",
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="Crustdata identifier for the company, accepted by the Company Enrichment endpoint.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Company type, e.g. Privately Held or Public Company.",
    )
    competitor_ids: list[int] | None = Field(
        default=None,
        alias="competitorIds",
        description="Crustdata identifiers for the companies Crustdata lists as competitors. These are the same identifiers companyId reports, returned here as numbers, and line up positionally with competitorWebsites.",
    )
    competitor_websites: list[str] | None = Field(
        default=None,
        alias="competitorWebsites",
        description="Websites of companies Crustdata considers competitors.",
    )
    contact_email: str | None = Field(
        default=None,
        alias="contactEmail",
        description="Publicly listed contact email address.",
    )
    crunchbase_categories: list[str] | None = Field(
        default=None,
        alias="crunchbaseCategories",
        description="Crunchbase category tags.",
    )
    crunchbase_url: str | None = Field(
        default=None, alias="crunchbaseUrl", description="Crunchbase profile URL."
    )
    crunchbase_uuid: str | None = Field(
        default=None,
        alias="crunchbaseUuid",
        description="Crunchbase organization UUID.",
    )
    description: str | None = Field(
        default=None, description="Company description from its LinkedIn page."
    )
    domain: str | None = Field(
        default=None,
        description="Primary website domain, or null when the upstream holds none for this company.",
    )
    domains: list[str] | None = Field(
        default=None, description="All domains associated with the company."
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Latest observed employee count.",
    )
    employee_growth: CompanySearchCrustdataV3EmployeeGrowth | None = Field(
        default=None,
        alias="employeeGrowth",
        description="Headcount change over trailing windows, absolute and percent.",
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
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="Latest LinkedIn follower count.",
    )
    follower_growth: CompanySearchCrustdataV3FollowerGrowth | None = Field(
        default=None,
        alias="followerGrowth",
        description="LinkedIn follower change over trailing windows, absolute and percent.",
    )
    founded_year: int | None = Field(
        default=None, alias="foundedYear", description="Year the company was founded."
    )
    growth_calculated_utc: int | None = Field(
        default=None,
        alias="growthCalculatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the growth metrics on this record were last calculated.",
    )
    headcount_by_region: CompanySearchCrustdataV3HeadcountByRegion | None = Field(
        default=None,
        alias="headcountByRegion",
        description="Employee count per region, keyed by LinkedIn region name.",
    )
    headcount_by_role: CompanySearchCrustdataV3HeadcountByRole | None = Field(
        default=None,
        alias="headcountByRole",
        description="Employee count per job function, keyed by LinkedIn function name.",
    )
    headcount_by_role_percent: CompanySearchCrustdataV3HeadcountByRolePercent | None = (
        Field(
            default=None,
            alias="headcountByRolePercent",
            description="Share of employees per job function as a percent, keyed by LinkedIn function name.",
        )
    )
    headcount_by_skill: CompanySearchCrustdataV3HeadcountBySkill | None = Field(
        default=None,
        alias="headcountBySkill",
        description="Employee count per listed skill, keyed by skill name.",
    )
    headcount_by_skill_percent: (
        CompanySearchCrustdataV3HeadcountBySkillPercent | None
    ) = Field(
        default=None,
        alias="headcountBySkillPercent",
        description="Share of employees per listed skill as a percent, keyed by skill name.",
    )
    headquarters: str | None = Field(default=None, description="Headquarters location.")
    hq_country: str | None = Field(
        default=None, alias="hqCountry", description="Country of the headquarters."
    )
    hq_location_address_components: list[str] | None = Field(
        default=None,
        alias="hqLocationAddressComponents",
        description="The headquarters location split into address components (city, state, country). Restates headquarters in parts.",
    )
    hq_street_address_and_city: str | None = Field(
        default=None,
        alias="hqStreetAddressAndCity",
        description="Headquarters street address and city. Crustdata returns the same string as headquarters for most companies.",
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    indexed_utc: int | None = Field(
        default=None,
        alias="indexedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When Crustdata last indexed the record for search, which is usually just after updatedUtc.",
    )
    industries: list[str] | None = Field(
        default=None, description="All LinkedIn industries listed for the company."
    )
    industry: str | None = Field(default=None, description="Primary LinkedIn industry.")
    investors: list[str] | None = Field(
        default=None, description="Investors named on the Crunchbase profile."
    )
    is_investor: bool | None = Field(
        default=None,
        alias="isInvestor",
        description="True when the company itself invests in other companies.",
    )
    largest_headcount_country: str | None = Field(
        default=None,
        alias="largestHeadcountCountry",
        description="Country holding the largest share of employees.",
    )
    last_funding_type: str | None = Field(
        default=None,
        alias="lastFundingType",
        description="Type of the most recent funding round, e.g. series_e.",
    )
    last_funding_usd: int | None = Field(
        default=None,
        alias="lastFundingUsd",
        description="Amount raised in the most recent funding round, in USD.",
    )
    last_funding_utc: int | None = Field(
        default=None,
        alias="lastFundingUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Date of the most recent funding round.",
    )
    linkedin_categories: list[str] | None = Field(
        default=None,
        alias="linkedinCategories",
        description="LinkedIn speciality tags listed by the company.",
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
    markets: list[str] | None = Field(
        default=None,
        description="Markets the company trades in, e.g. PRIVATE or NASDAQ.",
    )
    name: str | None = Field(description="Company name.")
    office_addresses: Any | None = Field(
        default=None,
        alias="officeAddresses",
        description="Office addresses exactly as Crustdata returns them. Untyped passthrough: the structure ships verbatim and is not validated, because it was empty for every company we captured.",
    )
    phone: str | None = Field(default=None, description="Publicly listed phone number.")
    role_growth6m_percent: CompanySearchCrustdataV3RoleGrowth6mPercent | None = Field(
        default=None,
        alias="roleGrowth6mPercent",
        description="Six-month percent headcount change per job function, keyed by LinkedIn function name.",
    )
    role_growth_yoy_percent: CompanySearchCrustdataV3RoleGrowthYoyPercent | None = (
        Field(
            default=None,
            alias="roleGrowthYoyPercent",
            description="Year-over-year percent headcount change per job function, keyed by LinkedIn function name.",
        )
    )
    stock_symbols: list[str] | None = Field(
        default=None, alias="stockSymbols", description="Stock ticker symbols."
    )
    total_funding_usd: int | None = Field(
        default=None,
        alias="totalFundingUsd",
        description="Total investment raised to date, in USD.",
    )
    tracxn_investors: Any | None = Field(
        default=None,
        alias="tracxnInvestors",
        description="Investors sourced from Tracxn, exactly as Crustdata returns them. Untyped passthrough: the structure ships verbatim and is not validated, because it was empty for every company we captured.",
    )
    twitter_url: str | None = Field(
        default=None, alias="twitterUrl", description="X (Twitter) profile URL."
    )
    updated_utc: int | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When this company record was last refreshed.",
    )
    valuation_lower_usd: int | None = Field(
        default=None,
        alias="valuationLowerUsd",
        description="Lower bound of the reported valuation in USD.",
    )
    valuation_usd: int | None = Field(
        default=None, alias="valuationUsd", description="Reported valuation in USD."
    )
    website: str | None = Field(default=None, description="Company website URL.")


class CompanySearchCrustdataV3EmployeeGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    absolute12m: int | None = Field(
        default=None, description="Net change over the last twelve months."
    )
    absolute1m: int | None = Field(
        default=None, description="Net change over the last month."
    )
    absolute3m: int | None = Field(
        default=None, description="Net change over the last three months."
    )
    absolute6m: int | None = Field(
        default=None, description="Net change over the last six months."
    )
    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent1m: float | None = Field(
        default=None, description="Percent change over the last month."
    )
    percent3m: float | None = Field(
        default=None, description="Percent change over the last three months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class CompanySearchCrustdataV3FollowerGrowth(BaseModel):
    model_config = ConfigDict(extra="allow")

    absolute12m: int | None = Field(
        default=None, description="Net change over the last twelve months."
    )
    absolute1m: int | None = Field(
        default=None, description="Net change over the last month."
    )
    absolute3m: int | None = Field(
        default=None, description="Net change over the last three months."
    )
    absolute6m: int | None = Field(
        default=None, description="Net change over the last six months."
    )
    percent12m: float | None = Field(
        default=None, description="Percent change over the last twelve months."
    )
    percent1m: float | None = Field(
        default=None, description="Percent change over the last month."
    )
    percent3m: float | None = Field(
        default=None, description="Percent change over the last three months."
    )
    percent6m: float | None = Field(
        default=None, description="Percent change over the last six months."
    )


class CompanySearchCrustdataV3HeadcountByRegion(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchCrustdataV3HeadcountByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchCrustdataV3HeadcountByRolePercent(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchCrustdataV3HeadcountBySkill(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchCrustdataV3HeadcountBySkillPercent(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchCrustdataV3RoleGrowth6mPercent(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchCrustdataV3RoleGrowthYoyPercent(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchFullenrichData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchFullenrichCompanie] = Field(
        description="Matching companies with FullEnrich's firmographic record."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Cursor for the next page, or null when this lane is complete. Send it back as cursor.",
    )
    offset: int | None = Field(
        default=None, description="Rows skipped before this page."
    )
    total: int | None = Field(
        default=None, description="Rows matching the filters across all pages."
    )


class CompanySearchFullenrichCompanie(BaseModel):
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
    headquarters: CompanySearchFullenrichHeadquarter | None = Field(
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
    name: str | None = Field(description="Company name.")
    offices: list[CompanySearchFullenrichOffice] | None = Field(
        default=None, description="Every other office FullEnrich holds for the company."
    )
    specialties: list[str] | None = Field(
        default=None, description="Specialties the company lists for itself."
    )
    website: str | None = Field(default=None, description="Company website URL.")


class CompanySearchFullenrichHeadquarter(BaseModel):
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


class CompanySearchFullenrichOffice(BaseModel):
    model_config = ConfigDict(extra="allow")

    line1: str | None = Field(default=None, description="First address line.")
    line2: str | None = Field(
        default=None,
        description="Second address line, carrying city, region, postal code and country.",
    )


class CompanySearchPeopledatalabsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchPeopledatalabsCompanie] = Field(
        description="Matching company records, up to limit."
    )
    dataset_version: str | None = Field(
        default=None,
        alias="datasetVersion",
        description="Version of the People Data Labs dataset these records came from.",
    )
    total: int | None = Field(
        default=None,
        description="Companies matching the query across the whole dataset, not just this page.",
    )


class CompanySearchPeopledatalabsCompanie(BaseModel):
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
    average_tenure_by_level: CompanySearchPeopledatalabsAverageTenureByLevel | None = (
        Field(
            default=None,
            alias="averageTenureByLevel",
            description="Average tenure in years, keyed by seniority level.",
        )
    )
    average_tenure_by_role: CompanySearchPeopledatalabsAverageTenureByRole | None = (
        Field(
            default=None,
            alias="averageTenureByRole",
            description="Average tenure in years, keyed by role.",
        )
    )
    direct_subsidiaries: list[str] | None = Field(
        default=None,
        alias="directSubsidiaries",
        description="People Data Labs company ids of direct subsidiaries.",
    )
    employee_churn_rate: CompanySearchPeopledatalabsEmployeeChurnRate | None = Field(
        default=None,
        alias="employeeChurnRate",
        description="Churn rate keyed by window, e.g. 12_month.",
    )
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Employees People Data Labs currently counts.",
    )
    employee_count_by_class: CompanySearchPeopledatalabsEmployeeCountByClas | None = (
        Field(
            default=None,
            alias="employeeCountByClass",
            description="Headcount keyed by job class.",
        )
    )
    employee_count_by_country: (
        CompanySearchPeopledatalabsEmployeeCountByCountry | None
    ) = Field(
        default=None,
        alias="employeeCountByCountry",
        description="Headcount keyed by country.",
    )
    employee_count_by_month: CompanySearchPeopledatalabsEmployeeCountByMonth | None = (
        Field(
            default=None,
            alias="employeeCountByMonth",
            description="Headcount keyed by YYYY-MM month.",
        )
    )
    employee_count_by_role: CompanySearchPeopledatalabsEmployeeCountByRole | None = (
        Field(
            default=None,
            alias="employeeCountByRole",
            description="Headcount keyed by role.",
        )
    )
    employee_count_by_sub_role: (
        CompanySearchPeopledatalabsEmployeeCountBySubRole | None
    ) = Field(
        default=None,
        alias="employeeCountBySubRole",
        description="Headcount keyed by sub-role.",
    )
    employee_growth_rate: CompanySearchPeopledatalabsEmployeeGrowthRate | None = Field(
        default=None,
        alias="employeeGrowthRate",
        description="Headcount growth rate keyed by window.",
    )
    employee_growth_rate12_month_by_class: (
        CompanySearchPeopledatalabsEmployeeGrowthRate12MonthByClas | None
    ) = Field(
        default=None,
        alias="employeeGrowthRate12MonthByClass",
        description="Twelve-month headcount growth rate keyed by job class.",
    )
    employee_growth_rate12_month_by_country: (
        CompanySearchPeopledatalabsEmployeeGrowthRate12MonthByCountry | None
    ) = Field(
        default=None,
        alias="employeeGrowthRate12MonthByCountry",
        description="Twelve-month headcount growth keyed by country, each entry carrying current and prior headcount.",
    )
    employee_growth_rate12_month_by_role: (
        CompanySearchPeopledatalabsEmployeeGrowthRate12MonthByRole | None
    ) = Field(
        default=None,
        alias="employeeGrowthRate12MonthByRole",
        description="Twelve-month headcount growth rate keyed by role.",
    )
    employee_turnover_rate: CompanySearchPeopledatalabsEmployeeTurnoverRate | None = (
        Field(
            default=None,
            alias="employeeTurnoverRate",
            description="Turnover rate keyed by window, e.g. 3_month, 12_month.",
        )
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
        CompanySearchPeopledatalabsGrossAdditionsByMonth | None
    ) = Field(
        default=None,
        alias="grossAdditionsByMonth",
        description="Employees joined, keyed by YYYY-MM month.",
    )
    gross_departures_by_month: (
        CompanySearchPeopledatalabsGrossDeparturesByMonth | None
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
    location: CompanySearchPeopledatalabsLocation | None = Field(
        default=None, description="Company headquarters."
    )
    median_employee_tenure: float | None = Field(
        default=None,
        alias="medianEmployeeTenure",
        description="Median employee tenure in years.",
    )
    median_tenure_by_level: CompanySearchPeopledatalabsMedianTenureByLevel | None = (
        Field(
            default=None,
            alias="medianTenureByLevel",
            description="Median tenure in years, keyed by seniority level.",
        )
    )
    median_tenure_by_role: CompanySearchPeopledatalabsMedianTenureByRole | None = Field(
        default=None,
        alias="medianTenureByRole",
        description="Median tenure in years, keyed by role.",
    )
    mic_exchange: str | None = Field(
        default=None,
        alias="micExchange",
        description="MIC code of the exchange the company lists on.",
    )
    naics_codes: list[CompanySearchPeopledatalabsNaicsCode] | None = Field(
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
    sic_codes: list[CompanySearchPeopledatalabsSicCode] | None = Field(
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


class CompanySearchPeopledatalabsAverageTenureByLevel(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsAverageTenureByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeChurnRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeCountByClas(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeCountByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeCountByMonth(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeCountByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeCountBySubRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeGrowthRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeGrowthRate12MonthByClas(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeGrowthRate12MonthByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeGrowthRate12MonthByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsEmployeeTurnoverRate(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsGrossAdditionsByMonth(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsGrossDeparturesByMonth(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsLocation(BaseModel):
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


class CompanySearchPeopledatalabsMedianTenureByLevel(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsMedianTenureByRole(BaseModel):
    model_config = ConfigDict(extra="allow")


class CompanySearchPeopledatalabsNaicsCode(BaseModel):
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


class CompanySearchPeopledatalabsSicCode(BaseModel):
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


class CompanySearchProspeoData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchProspeoCompanie] = Field(
        description="Matching companies with Prospeo's full firmographic record."
    )
    current_page: int | None = Field(
        default=None,
        alias="currentPage",
        description="Page number this response holds, one-based.",
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


class CompanySearchProspeoCompanie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attributes: CompanySearchProspeoAttribute | None = Field(
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
    email_tech: CompanySearchProspeoEmailTech | None = Field(
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
    funding: CompanySearchProspeoFunding | None = Field(
        default=None, description="Funding history."
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    industry: str | None = Field(default=None, description="Company industry.")
    instagram_url: str | None = Field(
        default=None, alias="instagramUrl", description="Company Instagram profile URL."
    )
    job_postings: CompanySearchProspeoJobPosting | None = Field(
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
    location: CompanySearchProspeoLocation | None = Field(
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
    phone_hq: CompanySearchProspeoPhoneHq | None = Field(
        default=None, alias="phoneHq", description="Headquarters switchboard number."
    )
    revenue_range: CompanySearchProspeoRevenueRange | None = Field(
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


class CompanySearchProspeoAttribute(BaseModel):
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


class CompanySearchProspeoEmailTech(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str | None = Field(
        default=None, description="Domain the company's email addresses use."
    )
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider behind the domain's MX records.",
    )


class CompanySearchProspeoFunding(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    events: list[CompanySearchProspeoEvent] | None = Field(
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


class CompanySearchProspeoEvent(BaseModel):
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


class CompanySearchProspeoJobPosting(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active_count: int | None = Field(
        default=None, alias="activeCount", description="Open roles currently posted."
    )
    active_titles: list[str] | None = Field(
        default=None, alias="activeTitles", description="Titles of the open roles."
    )


class CompanySearchProspeoLocation(BaseModel):
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


class CompanySearchProspeoPhoneHq(BaseModel):
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


class CompanySearchProspeoRevenueRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    max: float | None = Field(default=None, description="Upper bound in USD.")
    min: float | None = Field(default=None, description="Lower bound in USD.")


class CompanySearchQuickenrichData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchQuickenrichCompanie] = Field(
        description="Companies on this page."
    )
    has_more: bool = Field(
        alias="hasMore",
        description="Whether the upstream reports further pages beyond this one.",
    )
    page: int = Field(description="One-based page this response covers.")
    page_size: int = Field(
        alias="pageSize", description="Records per page upstream applied."
    )
    total: int = Field(description="Total records matching the request.")
    total_pages: int = Field(alias="totalPages", description="Total pages available.")


class CompanySearchQuickenrichCompanie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City on the employer record.")
    country: str | None = Field(
        default=None,
        description="ISO 3166-1 alpha-2 country code on the employer record.",
    )
    domain: str | None = Field(default=None, description="Company website domain.")
    email: str | None = Field(default=None, description="Work email address.")
    email_domain: str | None = Field(
        default=None,
        alias="emailDomain",
        description="Domain the work email resolves to.",
    )
    employee_count: str | None = Field(
        default=None,
        alias="employeeCount",
        description='Headcount band, e.g. "20 - 99". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    final_email_domain: str | None = Field(
        default=None,
        alias="finalEmailDomain",
        description="Domain the company's email addresses finally resolve to after redirects.",
    )
    home_page_text: str | None = Field(
        default=None,
        alias="homePageText",
        description="Home page text. A snippet unless includeFullText was set.",
    )
    industry: str | None = Field(default=None, description="Industry label.")
    linkedin_bio: str | None = Field(
        default=None, alias="linkedinBio", description="Company LinkedIn bio snippet."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Person's LinkedIn profile URL."
    )
    name: str | None = Field(description="Company name.")
    phone: str | None = Field(
        default=None,
        description="Direct business phone line held for the person. Mostly desk lines; read phoneType before treating it as a mobile.",
    )
    region: str | None = Field(
        default=None, description="State or region code on the employer record."
    )
    revenue: str | None = Field(
        default=None,
        description='Revenue band, e.g. "1 - 2.5 Million". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    service_count: int | None = Field(
        default=None,
        alias="serviceCount",
        description="How many services the company lists.",
    )
    services: Any | None = Field(
        default=None,
        description="Services the company lists. Passed through untyped: every captured response so far has this empty, so the element shape is unverified.",
    )


class CompanySearchTheirstackData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    companies: list[CompanySearchTheirstackCompanie] = Field(
        description="Matching companies with TheirStack's firmographic record and the technology and keyword slugs found in their job posts."
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


class CompanySearchTheirstackCompanie(BaseModel):
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
    name: str | None = Field(description="Company name.")
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
    num_jobs_found: int | None = Field(
        default=None,
        alias="numJobsFound",
        description="Job posts of this company that matched your job filters, when you sent any.",
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
    technologies_found: list[CompanySearchTheirstackTechnologiesFound] | None = Field(
        default=None,
        alias="technologiesFound",
        description="The technologies from your technology filters that this company was matched on. Empty unless you filtered by technology.",
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
    url_source: str | None = Field(
        default=None,
        alias="urlSource",
        description="Where TheirStack sourced the company website URL.",
    )
    yc_batch: str | None = Field(
        default=None,
        alias="ycBatch",
        description="Y Combinator batch, e.g. W20, for companies that went through it.",
    )


class CompanySearchTheirstackTechnologiesFound(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category: str | None = Field(
        default=None, description="Category the technology sits in."
    )
    category_slug: str | None = Field(
        default=None, alias="categorySlug", description="Slug for that category."
    )
    confidence: str | None = Field(
        default=None,
        description="How sure TheirStack is that the company uses it: high, medium or low.",
    )
    first_found_utc: float | None = Field(
        default=None,
        alias="firstFoundUtc",
        description="UTC epoch timestamp in seconds (Unix time) the technology was first seen. Multiply by 1000 for a JS Date in milliseconds.",
    )
    image: str | None = Field(default=None, description="Technology logo URL.")
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
    name: str | None = Field(description="Technology name.")
    parent_category: str | None = Field(
        default=None, alias="parentCategory", description="Parent category."
    )
    parent_category_slug: str | None = Field(
        default=None,
        alias="parentCategorySlug",
        description="Slug for that parent category.",
    )
    rank_within_category: int | None = Field(
        default=None,
        alias="rankWithinCategory",
        description="Rank among the company's technologies in the same category, 1 being the most used.",
    )
    relative_occurrence_within_category: float | None = Field(
        default=None,
        alias="relativeOccurrenceWithinCategory",
        description="Share of the company's mentions within this category that are of this technology, 0 to 1.",
    )
    score: float | None = Field(
        default=None, description="TheirStack's own relevance score for the match."
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


class CompanySearchNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ai_ark(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchAiArkInput],
    ) -> RunResult[CompanySearchAiArkData]:
        """Company Search - AI Ark

        Search companies by name, lookalike domains, account filters, and saved-list
        filters.

        Price: $0 per request plus $0.0024 per result (maximum $0.24).

        Example:
            res = client.company_search.ai_ark(name="OpenAI", page=0, size=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.ai_ark", dict(input), options
        )
        return RunResult[CompanySearchAiArkData].model_validate(raw)

    def crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataInput],
    ) -> RunResult[CompanySearchCrustdataData]:
        """Company Search - Crustdata

        Search companies by structured filters with cursor pagination.

        Price: $0.0012 per request plus $0.00144 per result (maximum $0.3612).

        Example:
            res = client.company_search.crustdata(filters={"field": "basic_info.primary_domain", "type": "=", "value": "posthog.com"}, limit=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.crustdata", dict(input), options
        )
        return RunResult[CompanySearchCrustdataData].model_validate(raw)

    def iter_crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataInput],
    ) -> Paginator[CompanySearchCrustdataCompanie, CompanySearchCrustdataData]:
        """Iterate Company Search - Crustdata results, following pagination cursors.

        Yields validated `CompanySearchCrustdataCompanie` items from the `companies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "company_search.crustdata",
            dict(input),
            "companies",
            item_model=CompanySearchCrustdataCompanie,
            data_model=CompanySearchCrustdataData,
            bare=False,
            options=options,
        )

    def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataV3Input],
    ) -> RunResult[CompanySearchCrustdataV3Data]:
        """Company Search - Crustdata v3 (legacy)

        Search companies by structured filters with cursor pagination.

        Price: $0 per request plus $0.048 per result (maximum $12).

        Example:
            res = client.company_search.crustdata_v3(filters=[{"filter_type": "company_website_domain", "type": "(.)", "value": "posthog.com"}], limit=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.crustdata_v3", dict(input), options
        )
        return RunResult[CompanySearchCrustdataV3Data].model_validate(raw)

    def iter_crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataV3Input],
    ) -> Paginator[CompanySearchCrustdataV3Companie, CompanySearchCrustdataV3Data]:
        """Iterate Company Search - Crustdata v3 (legacy) results, following pagination cursors.

        Yields validated `CompanySearchCrustdataV3Companie` items from the `companies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "company_search.crustdata_v3",
            dict(input),
            "companies",
            item_model=CompanySearchCrustdataV3Companie,
            data_model=CompanySearchCrustdataV3Data,
            bare=False,
            options=options,
        )

    def fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchFullenrichInput],
    ) -> RunResult[CompanySearchFullenrichData]:
        """Company Search - FullEnrich

        Build an account list from FullEnrich by name, domain, industry, specialty,
        ownership type, headcount, founding year and headquarters, with full
        firmographics and every office on each row. Billed per company returned.

        Price: $0 per request plus $0.0252 per result (maximum $2.52).

        Example:
            res = client.company_search.fullenrich(domains=[{"exact_match": True, "value": "stripe.com"}], limit=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.fullenrich", dict(input), options
        )
        return RunResult[CompanySearchFullenrichData].model_validate(raw)

    def iter_fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchFullenrichInput],
    ) -> Paginator[CompanySearchFullenrichCompanie, CompanySearchFullenrichData]:
        """Iterate Company Search - FullEnrich results, following pagination cursors.

        Yields validated `CompanySearchFullenrichCompanie` items from the `companies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "company_search.fullenrich",
            dict(input),
            "companies",
            item_model=CompanySearchFullenrichCompanie,
            data_model=CompanySearchFullenrichData,
            bare=False,
            options=options,
        )

    def peopledatalabs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchPeopledatalabsInput],
    ) -> RunResult[CompanySearchPeopledatalabsData]:
        """Company Search - People Data Labs

        Search People Data Labs' company dataset with SQL or an Elasticsearch query
        and get the full firmographic record back, including funding history and the
        headcount growth, tenure and churn series. Billed per company returned.

        Price: $0 per request plus $0.12 per result (maximum $9.96).

        Example:
            res = client.company_search.peopledatalabs(limit=1, sql="SELECT * FROM company WHERE website = 'posthog.com'")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.peopledatalabs", dict(input), options
        )
        return RunResult[CompanySearchPeopledatalabsData].model_validate(raw)

    def prospeo(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchProspeoInput],
    ) -> RunResult[CompanySearchProspeoData]:
        """Company Search - Prospeo

        Build an account list from Prospeo by industry, headcount, revenue,
        location, technology, funding and hiring activity. One flat price per page
        of 25.

        Price: $0.066 per request.

        Example:
            res = client.company_search.prospeo(company={"websites": {"include": ["stripe.com"]}}, page=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.prospeo", dict(input), options
        )
        return RunResult[CompanySearchProspeoData].model_validate(raw)

    def quickenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchQuickenrichInput],
    ) -> RunResult[CompanySearchQuickenrichData]:
        """Company Search - QuickEnrich

        Find companies by name, domain, industry, headcount, revenue, services, or
        location, and get back their site, LinkedIn, and contact details. Billed per
        company returned.

        Price: $0 per request plus $0.0072 per result (maximum $0.72).

        Example:
            res = client.company_search.quickenrich(country={"include": ["US"]}, employeeCount={"include": ["20 - 99"]}, limit=2)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.quickenrich", dict(input), options
        )
        return RunResult[CompanySearchQuickenrichData].model_validate(raw)

    def theirstack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchTheirstackInput],
    ) -> RunResult[CompanySearchTheirstackData]:
        """Company Search - TheirStack

        Build an account list from TheirStack by the technologies, keywords and
        buying-intent topics a company mentions in its job posts, plus headcount,
        revenue, funding, industry and location. Billed per company returned.

        Price: $0 per request plus $0.1992 per result (maximum $9.96).

        Example:
            res = client.company_search.theirstack(companyDomainOr=["posthog.com"], limit=1)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.theirstack", dict(input), options
        )
        return RunResult[CompanySearchTheirstackData].model_validate(raw)


class AsyncCompanySearchNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ai_ark(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchAiArkInput],
    ) -> RunResult[CompanySearchAiArkData]:
        """Company Search - AI Ark

        Search companies by name, lookalike domains, account filters, and saved-list
        filters.

        Price: $0 per request plus $0.0024 per result (maximum $0.24).

        Example:
            res = client.company_search.ai_ark(name="OpenAI", page=0, size=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.ai_ark", dict(input), options
        )
        return RunResult[CompanySearchAiArkData].model_validate(raw)

    async def crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataInput],
    ) -> RunResult[CompanySearchCrustdataData]:
        """Company Search - Crustdata

        Search companies by structured filters with cursor pagination.

        Price: $0.0012 per request plus $0.00144 per result (maximum $0.3612).

        Example:
            res = client.company_search.crustdata(filters={"field": "basic_info.primary_domain", "type": "=", "value": "posthog.com"}, limit=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.crustdata", dict(input), options
        )
        return RunResult[CompanySearchCrustdataData].model_validate(raw)

    def iter_crustdata(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataInput],
    ) -> AsyncPaginator[CompanySearchCrustdataCompanie, CompanySearchCrustdataData]:
        """Iterate Company Search - Crustdata results, following pagination cursors.

        Yields validated `CompanySearchCrustdataCompanie` items from the `companies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "company_search.crustdata",
            dict(input),
            "companies",
            item_model=CompanySearchCrustdataCompanie,
            data_model=CompanySearchCrustdataData,
            bare=False,
            options=options,
        )

    async def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataV3Input],
    ) -> RunResult[CompanySearchCrustdataV3Data]:
        """Company Search - Crustdata v3 (legacy)

        Search companies by structured filters with cursor pagination.

        Price: $0 per request plus $0.048 per result (maximum $12).

        Example:
            res = client.company_search.crustdata_v3(filters=[{"filter_type": "company_website_domain", "type": "(.)", "value": "posthog.com"}], limit=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.crustdata_v3", dict(input), options
        )
        return RunResult[CompanySearchCrustdataV3Data].model_validate(raw)

    def iter_crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchCrustdataV3Input],
    ) -> AsyncPaginator[CompanySearchCrustdataV3Companie, CompanySearchCrustdataV3Data]:
        """Iterate Company Search - Crustdata v3 (legacy) results, following pagination cursors.

        Yields validated `CompanySearchCrustdataV3Companie` items from the `companies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "company_search.crustdata_v3",
            dict(input),
            "companies",
            item_model=CompanySearchCrustdataV3Companie,
            data_model=CompanySearchCrustdataV3Data,
            bare=False,
            options=options,
        )

    async def fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchFullenrichInput],
    ) -> RunResult[CompanySearchFullenrichData]:
        """Company Search - FullEnrich

        Build an account list from FullEnrich by name, domain, industry, specialty,
        ownership type, headcount, founding year and headquarters, with full
        firmographics and every office on each row. Billed per company returned.

        Price: $0 per request plus $0.0252 per result (maximum $2.52).

        Example:
            res = client.company_search.fullenrich(domains=[{"exact_match": True, "value": "stripe.com"}], limit=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.fullenrich", dict(input), options
        )
        return RunResult[CompanySearchFullenrichData].model_validate(raw)

    def iter_fullenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchFullenrichInput],
    ) -> AsyncPaginator[CompanySearchFullenrichCompanie, CompanySearchFullenrichData]:
        """Iterate Company Search - FullEnrich results, following pagination cursors.

        Yields validated `CompanySearchFullenrichCompanie` items from the `companies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "company_search.fullenrich",
            dict(input),
            "companies",
            item_model=CompanySearchFullenrichCompanie,
            data_model=CompanySearchFullenrichData,
            bare=False,
            options=options,
        )

    async def peopledatalabs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchPeopledatalabsInput],
    ) -> RunResult[CompanySearchPeopledatalabsData]:
        """Company Search - People Data Labs

        Search People Data Labs' company dataset with SQL or an Elasticsearch query
        and get the full firmographic record back, including funding history and the
        headcount growth, tenure and churn series. Billed per company returned.

        Price: $0 per request plus $0.12 per result (maximum $9.96).

        Example:
            res = client.company_search.peopledatalabs(limit=1, sql="SELECT * FROM company WHERE website = 'posthog.com'")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.peopledatalabs", dict(input), options
        )
        return RunResult[CompanySearchPeopledatalabsData].model_validate(raw)

    async def prospeo(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchProspeoInput],
    ) -> RunResult[CompanySearchProspeoData]:
        """Company Search - Prospeo

        Build an account list from Prospeo by industry, headcount, revenue,
        location, technology, funding and hiring activity. One flat price per page
        of 25.

        Price: $0.066 per request.

        Example:
            res = client.company_search.prospeo(company={"websites": {"include": ["stripe.com"]}}, page=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.prospeo", dict(input), options
        )
        return RunResult[CompanySearchProspeoData].model_validate(raw)

    async def quickenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchQuickenrichInput],
    ) -> RunResult[CompanySearchQuickenrichData]:
        """Company Search - QuickEnrich

        Find companies by name, domain, industry, headcount, revenue, services, or
        location, and get back their site, LinkedIn, and contact details. Billed per
        company returned.

        Price: $0 per request plus $0.0072 per result (maximum $0.72).

        Example:
            res = client.company_search.quickenrich(country={"include": ["US"]}, employeeCount={"include": ["20 - 99"]}, limit=2)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.quickenrich", dict(input), options
        )
        return RunResult[CompanySearchQuickenrichData].model_validate(raw)

    async def theirstack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanySearchTheirstackInput],
    ) -> RunResult[CompanySearchTheirstackData]:
        """Company Search - TheirStack

        Build an account list from TheirStack by the technologies, keywords and
        buying-intent topics a company mentions in its job posts, plus headcount,
        revenue, funding, industry and location. Billed per company returned.

        Price: $0 per request plus $0.1992 per result (maximum $9.96).

        Example:
            res = client.company_search.theirstack(companyDomainOr=["posthog.com"], limit=1)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_search.theirstack", dict(input), options
        )
        return RunResult[CompanySearchTheirstackData].model_validate(raw)
