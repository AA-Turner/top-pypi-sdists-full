# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the seo platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

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


class SeoBacklinkAnchorsInput(TypedDict, total=False):
    """Input for SEO Backlink Anchors."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeSubdomains: NotRequired[bool]
    """Count links pointing at the target's subdomains as well as the target itself. Default: true."""
    limit: NotRequired[int]
    """Maximum number of anchor texts to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    status: NotRequired[Literal["live", "lost", "all"]]
    """Count backlinks that are live now, ones that have been lost, or both. Default: live."""
    target: Required[str]
    """Domain, subdomain, or full page URL to analyze. Send a domain without a protocol or leading www."""


class SeoBacklinkCompetitorsInput(TypedDict, total=False):
    """Input for SEO Backlink Competitors."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    excludeLargeDomains: NotRequired[bool]
    """Leave out very large sites (such as google.com or wikipedia.org) that share backlinks with almost everyone. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of competing domains to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    mainDomainOnly: NotRequired[bool]
    """Group results by registrable domain rather than listing subdomains separately. Default: true."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    target: Required[str]
    """Domain, subdomain, or full page URL to analyze. Send a domain without a protocol or leading www."""


class SeoBacklinksInput(TypedDict, total=False):
    """Input for SEO Backlinks."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeSubdomains: NotRequired[bool]
    """Count links pointing at the target's subdomains as well as the target itself. Default: true."""
    limit: NotRequired[int]
    """Maximum number of backlinks to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    mode: NotRequired[Literal["as_is", "one_per_domain", "one_per_anchor"]]
    """as_is returns every backlink; one_per_domain keeps one backlink per linking domain; one_per_anchor keeps one per anchor text. Default: as_is."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    status: NotRequired[Literal["live", "lost", "all"]]
    """Return backlinks that are live now, ones that have been lost, or both. Default: live."""
    target: Required[str]
    """Domain, subdomain, or full page URL to analyze. Send a domain without a protocol or leading www."""


class SeoBacklinksSummaryInput(TypedDict, total=False):
    """Input for SEO Backlinks Summary."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeSubdomains: NotRequired[bool]
    """Count links pointing at the target's subdomains as well as the target itself. Default: true."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    target: Required[str]
    """Domain, subdomain, or full page URL to analyze. Send a domain without a protocol or leading www."""


class SeoCompetitorsDomainInput(TypedDict, total=False):
    """Input for SEO Competitor Domains."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Language code for SEO competitor metrics. Default: en."""
    limit: NotRequired[int]
    """Maximum number of competitor domains to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code for SEO competitor metrics. The default is the United States. Default: 2840."""
    orderBy: NotRequired[
        Literal[
            "intersections_desc",
            "organic_keywords_desc",
            "organic_etv_desc",
            "avg_position_asc",
        ]
    ]
    """Sort order for the returned competitors: by shared keyword count (intersections), organic keyword count, organic traffic value (etv), or average position. Omit for the default order."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    target: Required[str]
    """Domain to analyze, without a protocol or leading www."""


class SeoDomainIntersectionInput(TypedDict, total=False):
    """Input for SEO Domain Intersection."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    intersections: NotRequired[bool]
    """When true (the default), return keywords both domains rank for (overlap). When false, return keywords the first domain ranks for that the second domain does NOT (the content-gap query); in that mode secondRank and secondUrl are absent."""
    language: NotRequired[str]
    """Language code for SEO overlap metrics. Default: en."""
    limit: NotRequired[int]
    """Maximum number of keywords to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code for SEO overlap metrics. The default is the United States. Default: 2840."""
    orderBy: NotRequired[
        Literal[
            "volume_desc", "volume_asc", "cpc_desc", "difficulty_asc", "difficulty_desc"
        ]
    ]
    """Sort order for the returned keywords: by search volume, cost per click, or keyword difficulty, ascending or descending. Omit for the default order."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    target1: Required[str]
    """First domain to compare, without a protocol or leading www."""
    target2: Required[str]
    """Second domain to compare, without a protocol or leading www."""


class SeoDomainPagesInput(TypedDict, total=False):
    """Input for SEO Domain Pages."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeSubdomains: NotRequired[bool]
    """Count links pointing at the target's subdomains as well as the target itself. Default: true."""
    limit: NotRequired[int]
    """Maximum number of pages to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    status: NotRequired[Literal["live", "lost", "all"]]
    """Count backlinks that are live now, ones that have been lost, or both. Default: live."""
    target: Required[str]
    """Domain or subdomain to list pages for, without a protocol or leading www."""


class SeoDomainRankOverviewInput(TypedDict, total=False):
    """Input for SEO Domain Rank Overview."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Language code for SEO domain metrics. Default: en."""
    location: NotRequired[int]
    """Location code for SEO domain metrics. The default is the United States. Default: 2840."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    target: Required[str]
    """Domain to analyze, without a protocol or leading www."""


class SeoDomainTechnologiesInput(TypedDict, total=False):
    """Input for SEO Domain Technologies."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: Required[str]
    """Domain to analyze, without a protocol or leading www. Billing is flat per request."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoDomainsByTechnologyInput(TypedDict, total=False):
    """Input for SEO Domains By Technology."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    category: NotRequired[str]
    """Technology category to match, for example marketing_automation. Broader than technology: it returns every domain running anything in that category."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor. Omit for the first page."""
    group: NotRequired[str]
    """Top-level technology group to match, for example marketing or servers. The broadest selector."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: NotRequired[str]
    """On-page term to match in the site's HTML, for example highlevel. Use this to find sites running a product that the technology index does not detect by name."""
    limit: NotRequired[int]
    """Maximum number of domains to return in this response. You are billed per returned result, so a lower limit costs less. Range: 1 to 100. Default: 20."""
    orderBy: NotRequired[
        Literal["rank_desc", "rank_asc", "last_visited_desc", "country_asc"]
    ]
    """Sort order for the returned domains: by domain rank descending or ascending, by most recently crawled, or by country code. Omit for the default order."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    technology: NotRequired[str]
    """Exact technology name to match, for example Nginx or HubSpot. Only technologies present in the detection index are accepted; any other name is rejected with a 400 error and no charge, so use keyword instead when a product is not matched by name."""


class SeoKeywordDifficultyInput(TypedDict, total=False):
    """Input for SEO Keyword Difficulty."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: Required[list[str]]
    """SEO keywords to score for organic ranking difficulty."""
    language: NotRequired[str]
    """Language code for SEO keyword difficulty metrics. Default: en."""
    location: NotRequired[int]
    """Location code for SEO keyword difficulty metrics. The default is the United States. Default: 2840."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoKeywordIdeasInput(TypedDict, total=False):
    """Input for SEO Keyword Ideas."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    closelyVariants: NotRequired[bool]
    """When true, generate only close variants of the seed keywords; when false (the default), generate a broader set of related ideas."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: Required[list[str]]
    """Seed SEO keywords used to generate related keyword ideas."""
    language: NotRequired[str]
    """Language code for SEO metrics. Default: en."""
    limit: NotRequired[int]
    """Maximum number of keyword ideas to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 5."""
    location: NotRequired[int]
    """Location code for SEO metrics. The default is the United States. Default: 2840."""
    orderBy: NotRequired[
        Literal[
            "volume_desc", "volume_asc", "cpc_desc", "difficulty_asc", "difficulty_desc"
        ]
    ]
    """Sort order for the returned ideas: by search volume, cost per click, or keyword difficulty, ascending or descending. Omit for the default order."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoKeywordOverviewInput(TypedDict, total=False):
    """Input for SEO Keyword Overview."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: Required[list[str]]
    """SEO keywords to analyze."""
    language: NotRequired[str]
    """Language code for SEO metrics. Default: en."""
    location: NotRequired[int]
    """Location code for SEO metrics. The default is the United States. Default: 2840."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoKeywordSuggestionsInput(TypedDict, total=False):
    """Input for SEO Keyword Suggestions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    exactMatch: NotRequired[bool]
    """When true, only return suggestions that contain the exact seed phrase; when false (the default), allow reordered and partial-match suggestions."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: Required[str]
    """Seed SEO keyword used to generate keyword suggestions."""
    language: NotRequired[str]
    """Language code for SEO metrics. Default: en."""
    limit: NotRequired[int]
    """Maximum number of keyword suggestions to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 5."""
    location: NotRequired[int]
    """Location code for SEO metrics. The default is the United States. Default: 2840."""
    orderBy: NotRequired[
        Literal[
            "volume_desc", "volume_asc", "cpc_desc", "difficulty_asc", "difficulty_desc"
        ]
    ]
    """Sort order for the returned suggestions: by search volume, cost per click, or keyword difficulty, ascending or descending. Omit for the default order."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoLlmMentionsInput(TypedDict, total=False):
    """Input for SEO LLM Mentions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: NotRequired[str]
    """Domain whose mentions to find, without a protocol or leading www. Send domain or keyword, not both."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: NotRequired[str]
    """Brand name or phrase whose mentions to find. Send domain or keyword, not both."""
    language: NotRequired[str]
    """Language code to restrict answers to, for example en. Omit for every language."""
    limit: NotRequired[int]
    """Maximum number of AI answers to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code to restrict answers to, for example 2840 for the United States. Omit for every location."""
    platform: NotRequired[Literal["google", "chat_gpt"]]
    """AI surface to search: google for Google AI Overviews, chat_gpt for ChatGPT. Default: google."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoLlmTopBrandsInput(TypedDict, total=False):
    """Input for SEO LLM Top Brands."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    breakdownLimit: NotRequired[int]
    """How many entries each breakdown list (cited domains, brands, locations, and so on) carries. Range: 1 to 10. Default: 5."""
    domain: NotRequired[str]
    """Only count AI answers that mention or cite this domain, without a protocol or leading www. Send domain or keyword, not both."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: NotRequired[str]
    """Only count AI answers that contain this word or phrase. Send domain or keyword, not both."""
    language: NotRequired[str]
    """Language code to restrict answers to, for example en. Omit for every language."""
    limit: NotRequired[int]
    """Maximum number of brands to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code to restrict answers to, for example 2840 for the United States. Omit for every location."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoLlmTopDomainsInput(TypedDict, total=False):
    """Input for SEO LLM Top Domains."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    breakdownLimit: NotRequired[int]
    """How many entries each breakdown list (cited domains, brands, locations, and so on) carries. Range: 1 to 10. Default: 5."""
    domain: NotRequired[str]
    """Only count AI answers that mention or cite this domain, without a protocol or leading www. Send domain or keyword, not both."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: NotRequired[str]
    """Only count AI answers that contain this word or phrase. Send domain or keyword, not both."""
    language: NotRequired[str]
    """Language code to restrict answers to, for example en. Omit for every language."""
    limit: NotRequired[int]
    """Maximum number of domains to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code to restrict answers to, for example 2840 for the United States. Omit for every location."""
    platform: NotRequired[Literal["google", "chat_gpt"]]
    """AI surface to count: google for Google AI Overviews, chat_gpt for ChatGPT. Omit for both."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoLlmTopPagesInput(TypedDict, total=False):
    """Input for SEO LLM Top Pages."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    breakdownLimit: NotRequired[int]
    """How many entries each breakdown list (cited domains, brands, locations, and so on) carries. Range: 1 to 10. Default: 5."""
    domain: NotRequired[str]
    """Only count AI answers that mention or cite this domain, without a protocol or leading www. Send domain or keyword, not both."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: NotRequired[str]
    """Only count AI answers that contain this word or phrase. Send domain or keyword, not both."""
    language: NotRequired[str]
    """Language code to restrict answers to, for example en. Omit for every language."""
    limit: NotRequired[int]
    """Maximum number of pages to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code to restrict answers to, for example 2840 for the United States. Omit for every location."""
    platform: NotRequired[Literal["google", "chat_gpt"]]
    """AI surface to count: google for Google AI Overviews, chat_gpt for ChatGPT. Omit for both."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoLocalPackInput(TypedDict, total=False):
    """Input for Google Local Pack."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: Required[str]
    """Search keyword, for example coffee shop or plumber."""
    language: NotRequired[str]
    """Language code for the search results. Default: en."""
    limit: NotRequired[int]
    """Maximum number of local pack businesses to return. Google usually shows three. Billing is flat per request. Range: 1 to 100."""
    location: Required[str]
    """Location to search from, formatted like City,Region,Country; for example, New York,New York,United States."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "address",
                "bookingUrl",
                "category",
                "cid",
                "description",
                "directionsUrl",
                "hours",
                "image",
                "knowledgeGraphId",
                "priceLevel",
                "rankGroup",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `address` or `cid`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a business that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoRankedKeywordsInput(TypedDict, total=False):
    """Input for SEO Ranked Keywords."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Language code for SEO ranking metrics. Default: en."""
    limit: NotRequired[int]
    """Maximum number of ranked keywords to return. 1,000 is the per-call maximum; use offset to fetch more. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code for SEO ranking metrics. The default is the United States. Default: 2840."""
    offset: NotRequired[int]
    """Number of ranked keywords to skip in the chosen sort order. To fetch the next page, set offset to the previous offset plus limit, and keep the same orderBy, location, and language across pages. You are billed only for the keywords returned. Minimum: 0. Default: 0."""
    orderBy: NotRequired[
        Literal["position_asc", "position_desc", "volume_desc", "etv_desc"]
    ]
    """Sort order for the returned ranked keywords: by SERP position (ascending for best rankings first), search volume, or estimated traffic value (etv). Omit for the default order."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    target: Required[str]
    """Domain to analyze, without a protocol or leading www."""


class SeoReferringDomainsInput(TypedDict, total=False):
    """Input for SEO Referring Domains."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeSubdomains: NotRequired[bool]
    """Count links pointing at the target's subdomains as well as the target itself. Default: true."""
    limit: NotRequired[int]
    """Maximum number of referring domains to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    target: Required[str]
    """Domain, subdomain, or full page URL to analyze. Send a domain without a protocol or leading www."""


class SeoRelatedKeywordsInput(TypedDict, total=False):
    """Input for SEO Related Keywords."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    depth: NotRequired[int]
    """Depth of the related-keyword expansion (0-4). Higher depth explores a broader keyword tree; the number of returned results, and therefore the price, is still capped by limit. Range: 0 to 4."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: Required[str]
    """Seed SEO keyword used to find related keywords."""
    language: NotRequired[str]
    """Language code for SEO metrics. Default: en."""
    limit: NotRequired[int]
    """Maximum number of related keywords to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 5."""
    location: NotRequired[int]
    """Location code for SEO metrics. The default is the United States. Default: 2840."""
    orderBy: NotRequired[
        Literal[
            "volume_desc", "volume_asc", "cpc_desc", "difficulty_asc", "difficulty_desc"
        ]
    ]
    """Sort order for the returned related keywords: by search volume, cost per click, or keyword difficulty, ascending or descending. Omit for the default order."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoSearchIntentInput(TypedDict, total=False):
    """Input for SEO Search Intent."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: Required[list[str]]
    """SEO keywords to classify by search intent."""
    language: NotRequired[str]
    """Language code for search intent classification. Default: en."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoSearchVolumeInput(TypedDict, total=False):
    """Input for SEO Search Volume."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    dateFrom: NotRequired[str]
    """Start of the historical monthly-searches window, formatted YYYY-MM-DD. Cannot be more than four years before today. Omit for the default trailing window."""
    dateTo: NotRequired[str]
    """End of the historical monthly-searches window, formatted YYYY-MM-DD. Omit for the default trailing window."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: Required[list[str]]
    """SEO keyword phrases to retrieve search-volume metrics for."""
    language: NotRequired[str]
    """Language code for SEO search-volume metrics. Default: en."""
    location: NotRequired[int]
    """Location code for SEO search-volume metrics. The default is the United States. Default: 2840."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    searchPartners: NotRequired[bool]
    """When true, include Google search-partner network volume in the reported numbers; when false (the default), count Google search only."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SeoTopPagesInput(TypedDict, total=False):
    """Input for SEO Top Pages."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Language code for search metrics. Default: en."""
    limit: NotRequired[int]
    """Maximum number of pages to return. You are billed per returned result, so a lower limit costs less. Range: 1 to 1000. Default: 10."""
    location: NotRequired[int]
    """Location code for search metrics. The default is the United States. Default: 2840."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    status: NotRequired[Literal["live", "lost", "all"]]
    """Count rankings the page holds now, rankings it has lost, or both. Default: live."""
    target: Required[str]
    """Domain to analyze, without a protocol or leading www."""


class SeoBacklinkAnchorsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    anchors: list[SeoBacklinkAnchorsAnchor] = Field(
        description="Anchor texts of backlinks to the target. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total anchor texts, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoBacklinkAnchorsAnchor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor: str | None = Field(
        default=None,
        description="Anchor text. Absent for links without text, such as image links. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    backlinks: int | None = Field(
        default=None,
        description="Backlinks counted. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    broken_backlinks: int | None = Field(
        default=None,
        alias="brokenBacklinks",
        description="Backlinks pointing at pages that no longer resolve.",
    )
    broken_pages: int | None = Field(
        default=None,
        alias="brokenPages",
        description="Linked pages with an error status.",
    )
    first_seen_utc: float | None = Field(
        default=None,
        alias="firstSeenUtc",
        description="When the first of these backlinks was seen. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    links_by_attribute: SeoBacklinkAnchorsLinksByAttribute | None = Field(
        default=None,
        alias="linksByAttribute",
        description="Count of these backlinks, by rel attribute (nofollow, sponsored, ugc, noopener, and so on).",
    )
    links_by_country: SeoBacklinkAnchorsLinksByCountry | None = Field(
        default=None,
        alias="linksByCountry",
        description="Count of these backlinks, by country code of the linking domain. An empty key means the country is unknown.",
    )
    links_by_platform_type: SeoBacklinkAnchorsLinksByPlatformType | None = Field(
        default=None,
        alias="linksByPlatformType",
        description="Count of these backlinks, by type of linking site (blogs, news, ecommerce, and so on).",
    )
    links_by_semantic_location: SeoBacklinkAnchorsLinksBySemanticLocation | None = (
        Field(
            default=None,
            alias="linksBySemanticLocation",
            description="Count of these backlinks, by the page section holding the link (article, footer, nav, and so on). An empty key means no section was detected.",
        )
    )
    links_by_tld: SeoBacklinkAnchorsLinksByTld | None = Field(
        default=None,
        alias="linksByTld",
        description="Count of these backlinks, by top-level domain of the linking page.",
    )
    links_by_type: SeoBacklinkAnchorsLinksByType | None = Field(
        default=None,
        alias="linksByType",
        description="Count of these backlinks, by link type (anchor, image, redirect, canonical, alternate).",
    )
    lost_utc: float | None = Field(
        default=None,
        alias="lostUtc",
        description="When the last of these backlinks was lost, if they were. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    rank: int | None = Field(
        default=None,
        description="Authority rank on a 0-1000 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    referring_domains: int | None = Field(
        default=None, alias="referringDomains", description="Distinct linking domains."
    )
    referring_domains_nofollow: int | None = Field(
        default=None,
        alias="referringDomainsNofollow",
        description="Linking domains whose every link is nofollow.",
    )
    referring_ips: int | None = Field(
        default=None,
        alias="referringIps",
        description="Distinct IP addresses of linking pages.",
    )
    referring_main_domains: int | None = Field(
        default=None,
        alias="referringMainDomains",
        description="Distinct linking registrable domains.",
    )
    referring_main_domains_nofollow: int | None = Field(
        default=None,
        alias="referringMainDomainsNofollow",
        description="Linking registrable domains whose every link is nofollow.",
    )
    referring_pages: int | None = Field(
        default=None, alias="referringPages", description="Distinct linking pages."
    )
    referring_pages_nofollow: int | None = Field(
        default=None,
        alias="referringPagesNofollow",
        description="Linking pages whose links are all nofollow.",
    )
    referring_subnets: int | None = Field(
        default=None,
        alias="referringSubnets",
        description="Distinct subnets of linking pages.",
    )
    spam_score: int | None = Field(
        default=None,
        alias="spamScore",
        description="Average spam score of those backlinks on a 0-100 scale.",
    )


class SeoBacklinkAnchorsLinksByAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinkAnchorsLinksByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinkAnchorsLinksByPlatformType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinkAnchorsLinksBySemanticLocation(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinkAnchorsLinksByTld(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinkAnchorsLinksByType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinkCompetitorsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    competitors: list[SeoBacklinkCompetitorsCompetitor] = Field(
        description="Domains sharing backlinks with the target, most shared first. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total competing domains, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoBacklinkCompetitorsCompetitor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str = Field(
        description="Competing domain. Populated whenever the provider has data for the entity."
    )
    rank: int | None = Field(
        default=None,
        description="Authority rank of the competing domain on a 0-1000 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    shared_backlinks: int | None = Field(
        default=None,
        alias="sharedBacklinks",
        description="Backlinks the competing domain shares with the target. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoBacklinksData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    backlinks: list[SeoBacklinksBacklink] = Field(
        description="Backlinks pointing at the target. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total backlinks matching the request, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoBacklinksBacklink(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor: str | None = Field(default=None, description="Anchor text of the link.")
    attributes: list[str] | None = Field(
        default=None,
        description="rel attributes on the link, such as nofollow, sponsored, ugc, or noopener.",
    )
    dofollow: bool | None = Field(
        default=None,
        description="True when the link passes ranking value (no nofollow attribute). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    domain_from: str | None = Field(
        default=None,
        alias="domainFrom",
        description="Domain of the linking page. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    domain_from_country: str | None = Field(
        default=None,
        alias="domainFromCountry",
        description="Country code of the linking domain.",
    )
    domain_from_ip: str | None = Field(
        default=None,
        alias="domainFromIp",
        description="IP address of the linking domain.",
    )
    domain_from_is_ip: bool | None = Field(
        default=None,
        alias="domainFromIsIp",
        description="True when the linking host is a bare IP address.",
    )
    domain_from_platform_types: list[str] | None = Field(
        default=None,
        alias="domainFromPlatformTypes",
        description="Site types of the linking domain, such as blogs, news, or ecommerce.",
    )
    domain_from_rank: int | None = Field(
        default=None,
        alias="domainFromRank",
        description="Authority rank of the linking domain on a 0-1000 scale.",
    )
    domain_to: str | None = Field(
        default=None, alias="domainTo", description="Domain of the target URL."
    )
    first_seen_utc: float | None = Field(
        default=None,
        alias="firstSeenUtc",
        description="When the backlink was first seen. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    group_count: int | None = Field(
        default=None,
        alias="groupCount",
        description="Backlinks grouped into this one by the requested mode.",
    )
    image_alt: str | None = Field(
        default=None,
        alias="imageAlt",
        description="Alt text of the linked image, for image links.",
    )
    image_url: str | None = Field(
        default=None,
        alias="imageUrl",
        description="URL of the linked image, for image links.",
    )
    is_broken: bool | None = Field(
        default=None,
        alias="isBroken",
        description="True when the target URL no longer resolves.",
    )
    is_indirect: bool | None = Field(
        default=None,
        alias="isIndirect",
        description="True when the link reaches the target through a redirect or canonical.",
    )
    is_lost: bool | None = Field(
        default=None,
        alias="isLost",
        description="True when the backlink has been removed.",
    )
    is_new: bool | None = Field(
        default=None,
        alias="isNew",
        description="True when the backlink appeared since the previous crawl.",
    )
    is_original: bool | None = Field(
        default=None,
        alias="isOriginal",
        description="True when the link was present on the first crawl of the linking page.",
    )
    last_seen_utc: float | None = Field(
        default=None,
        alias="lastSeenUtc",
        description="When the backlink was last seen. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    link_type: str | None = Field(
        default=None,
        alias="linkType",
        description="How the link is placed: anchor, image, redirect, canonical, alternate, and so on.",
    )
    links_count: int | None = Field(
        default=None,
        alias="linksCount",
        description="Identical links from the linking page to the target.",
    )
    page_from_encoding: str | None = Field(
        default=None,
        alias="pageFromEncoding",
        description="Character encoding of the linking page.",
    )
    page_from_external_links: int | None = Field(
        default=None,
        alias="pageFromExternalLinks",
        description="Outbound links on the linking page.",
    )
    page_from_internal_links: int | None = Field(
        default=None,
        alias="pageFromInternalLinks",
        description="Internal links on the linking page.",
    )
    page_from_keywords_top10: int | None = Field(
        default=None,
        alias="pageFromKeywordsTop10",
        description="Keywords the linking page ranks in the top 10 for.",
    )
    page_from_keywords_top100: int | None = Field(
        default=None,
        alias="pageFromKeywordsTop100",
        description="Keywords the linking page ranks in the top 100 for.",
    )
    page_from_keywords_top3: int | None = Field(
        default=None,
        alias="pageFromKeywordsTop3",
        description="Keywords the linking page ranks in the top 3 for.",
    )
    page_from_language: str | None = Field(
        default=None,
        alias="pageFromLanguage",
        description="Language code of the linking page.",
    )
    page_from_rank: int | None = Field(
        default=None,
        alias="pageFromRank",
        description="Authority rank of the linking page on a 0-1000 scale.",
    )
    page_from_size: int | None = Field(
        default=None,
        alias="pageFromSize",
        description="Size of the linking page in bytes.",
    )
    page_from_status_code: int | None = Field(
        default=None,
        alias="pageFromStatusCode",
        description="HTTP status the linking page returned.",
    )
    page_from_title: str | None = Field(
        default=None, alias="pageFromTitle", description="Title of the linking page."
    )
    previous_seen_utc: float | None = Field(
        default=None,
        alias="previousSeenUtc",
        description="When the backlink was seen on the crawl before the last one. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    rank: int | None = Field(
        default=None, description="Authority rank of the backlink on a 0-1000 scale."
    )
    semantic_location: str | None = Field(
        default=None,
        alias="semanticLocation",
        description="Page section holding the link, such as article, footer, or nav.",
    )
    spam_score: int | None = Field(
        default=None,
        alias="spamScore",
        description="Spam score of the backlink on a 0-100 scale.",
    )
    text_after: str | None = Field(
        default=None,
        alias="textAfter",
        description="Text right after the link on the linking page.",
    )
    text_before: str | None = Field(
        default=None,
        alias="textBefore",
        description="Text right before the link on the linking page.",
    )
    tld_from: str | None = Field(
        default=None,
        alias="tldFrom",
        description="Top-level domain of the linking page.",
    )
    url_from: str = Field(
        alias="urlFrom",
        description="URL of the page carrying the link. Populated whenever the provider has data for the entity.",
    )
    url_to: str | None = Field(
        default=None,
        alias="urlTo",
        description="Target URL the link points at. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url_to_redirect_target: str | None = Field(
        default=None,
        alias="urlToRedirectTarget",
        description="Where the target URL redirects, if it does.",
    )
    url_to_spam_score: int | None = Field(
        default=None,
        alias="urlToSpamScore",
        description="Spam score of the target URL on a 0-100 scale.",
    )
    url_to_status_code: int | None = Field(
        default=None,
        alias="urlToStatusCode",
        description="HTTP status the target URL returned.",
    )


class SeoBacklinksSummaryData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    backlinks: int | None = Field(
        default=None,
        description="Total live backlinks pointing at the target. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    backlinks_spam_score: int | None = Field(
        default=None,
        alias="backlinksSpamScore",
        description="Average spam score of the backlinks on a 0-100 scale.",
    )
    broken_backlinks: int | None = Field(
        default=None,
        alias="brokenBacklinks",
        description="Backlinks pointing at target pages that no longer resolve.",
    )
    broken_pages: int | None = Field(
        default=None,
        alias="brokenPages",
        description="Target pages with an error status that still receive backlinks.",
    )
    cms: str | None = Field(
        default=None, description="Content management system detected on the target."
    )
    country: str | None = Field(
        default=None, description="Country code of the target's server."
    )
    crawled_pages: int | None = Field(
        default=None, alias="crawledPages", description="Target pages crawled."
    )
    external_links: int | None = Field(
        default=None,
        alias="externalLinks",
        description="Outbound links from the target to other domains.",
    )
    first_seen_utc: float | None = Field(
        default=None,
        alias="firstSeenUtc",
        description="When a backlink to the target was first seen. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    internal_links: int | None = Field(
        default=None,
        alias="internalLinks",
        description="Links between pages of the target.",
    )
    ip_address: str | None = Field(
        default=None,
        alias="ipAddress",
        description="IP address the target resolves to.",
    )
    is_ip: bool | None = Field(
        default=None,
        alias="isIp",
        description="True when the target is a bare IP address.",
    )
    links_by_attribute: SeoBacklinksSummaryLinksByAttribute | None = Field(
        default=None,
        alias="linksByAttribute",
        description="Count of referring links to the target, by rel attribute (nofollow, sponsored, ugc, noopener, and so on).",
    )
    links_by_country: SeoBacklinksSummaryLinksByCountry | None = Field(
        default=None,
        alias="linksByCountry",
        description="Count of referring links to the target, by country code of the linking domain. An empty key means the country is unknown.",
    )
    links_by_platform_type: SeoBacklinksSummaryLinksByPlatformType | None = Field(
        default=None,
        alias="linksByPlatformType",
        description="Count of referring links to the target, by type of linking site (blogs, news, ecommerce, and so on).",
    )
    links_by_semantic_location: SeoBacklinksSummaryLinksBySemanticLocation | None = (
        Field(
            default=None,
            alias="linksBySemanticLocation",
            description="Count of referring links to the target, by the page section holding the link (article, footer, nav, and so on). An empty key means no section was detected.",
        )
    )
    links_by_tld: SeoBacklinksSummaryLinksByTld | None = Field(
        default=None,
        alias="linksByTld",
        description="Count of referring links to the target, by top-level domain of the linking page.",
    )
    links_by_type: SeoBacklinksSummaryLinksByType | None = Field(
        default=None,
        alias="linksByType",
        description="Count of referring links to the target, by link type (anchor, image, redirect, canonical, alternate).",
    )
    lost_utc: float | None = Field(
        default=None,
        alias="lostUtc",
        description="When the target lost its last backlink, if it has. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    platform_types: list[str] | None = Field(
        default=None,
        alias="platformTypes",
        description="Site types detected for the target, such as blogs, news, or ecommerce.",
    )
    rank: int | None = Field(
        default=None,
        description="Authority rank of the target on a 0-1000 scale, derived from its backlink profile. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    referring_domains: int | None = Field(
        default=None,
        alias="referringDomains",
        description="Distinct domains linking to the target. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    referring_domains_nofollow: int | None = Field(
        default=None,
        alias="referringDomainsNofollow",
        description="Referring domains whose every link is nofollow.",
    )
    referring_ips: int | None = Field(
        default=None,
        alias="referringIps",
        description="Distinct IP addresses hosting referring pages.",
    )
    referring_main_domains: int | None = Field(
        default=None,
        alias="referringMainDomains",
        description="Distinct registrable domains linking to the target.",
    )
    referring_main_domains_nofollow: int | None = Field(
        default=None,
        alias="referringMainDomainsNofollow",
        description="Referring registrable domains whose every link is nofollow.",
    )
    referring_pages: int | None = Field(
        default=None,
        alias="referringPages",
        description="Distinct pages linking to the target.",
    )
    referring_pages_nofollow: int | None = Field(
        default=None,
        alias="referringPagesNofollow",
        description="Referring pages whose links are all nofollow.",
    )
    referring_subnets: int | None = Field(
        default=None,
        alias="referringSubnets",
        description="Distinct subnets hosting referring pages.",
    )
    server: str | None = Field(
        default=None, description="Web server or CDN serving the target."
    )
    target: str = Field(
        description="Domain or URL the totals describe. Populated whenever the provider has data for the entity."
    )
    target_spam_score: int | None = Field(
        default=None,
        alias="targetSpamScore",
        description="Spam score of the target itself on a 0-100 scale.",
    )


class SeoBacklinksSummaryLinksByAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinksSummaryLinksByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinksSummaryLinksByPlatformType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinksSummaryLinksBySemanticLocation(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinksSummaryLinksByTld(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoBacklinksSummaryLinksByType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoCompetitorsDomainData(BaseModel):
    competitors: list[SeoCompetitorsDomainCompetitor] = Field(
        description="SEO competitor domain records. Populated whenever the provider has data for the entity."
    )


class SeoCompetitorsDomainCompetitor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avg_position: float | None = Field(
        default=None,
        alias="avgPosition",
        description="Average ranking position across shared keywords. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    domain: str = Field(
        description="Competing domain. Populated whenever the provider has data for the entity."
    )
    intersections: int = Field(
        description="Number of keywords shared with the target domain. Populated whenever the provider has data for the entity."
    )
    organic_etv: float | None = Field(
        default=None,
        alias="organicEtv",
        description="Estimated monthly organic search traffic for the competitor domain.",
    )
    organic_keywords: int | None = Field(
        default=None,
        alias="organicKeywords",
        description="Number of organic search results where the competitor domain appears.",
    )
    sum_position: int | None = Field(
        default=None,
        alias="sumPosition",
        description="Sum of ranking positions across shared keywords. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoDomainIntersectionData(BaseModel):
    keywords: list[SeoDomainIntersectionKeyword] = Field(
        description="SEO keyword records both domains rank for. Populated whenever the provider has data for the entity."
    )


class SeoDomainIntersectionKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid_high: float | None = Field(
        default=None,
        alias="bidHigh",
        description="Upper bound of the estimated paid-search top-of-page bid in USD.",
    )
    bid_low: float | None = Field(
        default=None,
        alias="bidLow",
        description="Lower bound of the estimated paid-search top-of-page bid in USD.",
    )
    competition: str | None = Field(
        default=None,
        description="Paid-search competition level for the keyword (LOW, MEDIUM, HIGH).",
    )
    cpc: float | None = Field(
        default=None, description="Average paid-search cost per click in USD."
    )
    first_rank: int = Field(
        alias="firstRank",
        description="Absolute organic ranking position for the first domain. Populated whenever the provider has data for the entity.",
    )
    first_title: str | None = Field(
        default=None,
        alias="firstTitle",
        description="Search-result title of the first domain's ranking page.",
    )
    first_url: str | None = Field(
        default=None, alias="firstUrl", description="Ranking URL for the first domain."
    )
    keyword: str = Field(
        description="Keyword phrase both domains rank for. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Estimated organic ranking difficulty on a 0-100 scale.",
    )
    search_intent: str | None = Field(
        default=None,
        alias="searchIntent",
        description="Primary SEO search intent for the keyword.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the keyword.",
    )
    second_rank: int | None = Field(
        default=None,
        alias="secondRank",
        description="Absolute organic ranking position for the second domain. Absent when intersections is false (the second domain does not rank for this keyword).",
    )
    second_title: str | None = Field(
        default=None,
        alias="secondTitle",
        description="Search-result title of the second domain's ranking page. Absent when the second domain does not rank for this keyword.",
    )
    second_url: str | None = Field(
        default=None,
        alias="secondUrl",
        description="Ranking URL for the second domain. Absent when intersections is false.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class SeoDomainPagesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pages: list[SeoDomainPagesPage] = Field(
        description="Pages of the domain with their backlink and on-page data. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total pages, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoDomainPagesPage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    backlinks: int | None = Field(
        default=None,
        description="Backlinks counted. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    broken_backlinks: int | None = Field(
        default=None,
        alias="brokenBacklinks",
        description="Backlinks pointing at pages that no longer resolve.",
    )
    broken_pages: int | None = Field(
        default=None,
        alias="brokenPages",
        description="Linked pages with an error status.",
    )
    canonical: str | None = Field(
        default=None, description="Canonical URL declared by the page."
    )
    charset: str | None = Field(default=None, description="Character set of the page.")
    content_encoding: str | None = Field(
        default=None,
        alias="contentEncoding",
        description="Content encoding of the response.",
    )
    domain: str | None = Field(
        default=None,
        description="Host of the page. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    encoded_size: int | None = Field(
        default=None, alias="encodedSize", description="Encoded page size in bytes."
    )
    external_links: int | None = Field(
        default=None, alias="externalLinks", description="Outbound links on the page."
    )
    fetched_utc: float | None = Field(
        default=None,
        alias="fetchedUtc",
        description="When the page was last crawled. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    first_seen_utc: float | None = Field(
        default=None,
        alias="firstSeenUtc",
        description="When the first of these backlinks was seen. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    first_visited_utc: float | None = Field(
        default=None,
        alias="firstVisitedUtc",
        description="When the page was first crawled. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    h1: list[str] | None = Field(default=None, description="H1 headings on the page.")
    h2: list[str] | None = Field(default=None, description="H2 headings on the page.")
    h3: list[str] | None = Field(default=None, description="H3 headings on the page.")
    images_count: int | None = Field(
        default=None, alias="imagesCount", description="Images on the page."
    )
    internal_links: int | None = Field(
        default=None, alias="internalLinks", description="Internal links on the page."
    )
    ip: str | None = Field(
        default=None, description="IP address the page was fetched from."
    )
    language: str | None = Field(default=None, description="Language code of the page.")
    links_by_attribute: SeoDomainPagesLinksByAttribute | None = Field(
        default=None,
        alias="linksByAttribute",
        description="Count of these backlinks, by rel attribute (nofollow, sponsored, ugc, noopener, and so on).",
    )
    links_by_country: SeoDomainPagesLinksByCountry | None = Field(
        default=None,
        alias="linksByCountry",
        description="Count of these backlinks, by country code of the linking domain. An empty key means the country is unknown.",
    )
    links_by_platform_type: SeoDomainPagesLinksByPlatformType | None = Field(
        default=None,
        alias="linksByPlatformType",
        description="Count of these backlinks, by type of linking site (blogs, news, ecommerce, and so on).",
    )
    links_by_semantic_location: SeoDomainPagesLinksBySemanticLocation | None = Field(
        default=None,
        alias="linksBySemanticLocation",
        description="Count of these backlinks, by the page section holding the link (article, footer, nav, and so on). An empty key means no section was detected.",
    )
    links_by_tld: SeoDomainPagesLinksByTld | None = Field(
        default=None,
        alias="linksByTld",
        description="Count of these backlinks, by top-level domain of the linking page.",
    )
    links_by_type: SeoDomainPagesLinksByType | None = Field(
        default=None,
        alias="linksByType",
        description="Count of these backlinks, by link type (anchor, image, redirect, canonical, alternate).",
    )
    lost_utc: float | None = Field(
        default=None,
        alias="lostUtc",
        description="When the last of these backlinks was lost, if they were. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    main_domain: str | None = Field(
        default=None, alias="mainDomain", description="Registrable domain of the page."
    )
    media_type: str | None = Field(
        default=None, alias="mediaType", description="Media type of the page."
    )
    page_spam_score: int | None = Field(
        default=None,
        alias="pageSpamScore",
        description="Spam score of the page on a 0-100 scale.",
    )
    platform_types: list[str] | None = Field(
        default=None,
        alias="platformTypes",
        description="Site types detected, such as blogs, news, or ecommerce.",
    )
    previous_visited_utc: float | None = Field(
        default=None,
        alias="previousVisitedUtc",
        description="When the page was crawled before the last time. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    rank: int | None = Field(
        default=None,
        description="Authority rank on a 0-1000 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    referring_domains: int | None = Field(
        default=None, alias="referringDomains", description="Distinct linking domains."
    )
    referring_domains_nofollow: int | None = Field(
        default=None,
        alias="referringDomainsNofollow",
        description="Linking domains whose every link is nofollow.",
    )
    referring_ips: int | None = Field(
        default=None,
        alias="referringIps",
        description="Distinct IP addresses of linking pages.",
    )
    referring_main_domains: int | None = Field(
        default=None,
        alias="referringMainDomains",
        description="Distinct linking registrable domains.",
    )
    referring_main_domains_nofollow: int | None = Field(
        default=None,
        alias="referringMainDomainsNofollow",
        description="Linking registrable domains whose every link is nofollow.",
    )
    referring_pages: int | None = Field(
        default=None, alias="referringPages", description="Distinct linking pages."
    )
    referring_pages_nofollow: int | None = Field(
        default=None,
        alias="referringPagesNofollow",
        description="Linking pages whose links are all nofollow.",
    )
    referring_subnets: int | None = Field(
        default=None,
        alias="referringSubnets",
        description="Distinct subnets of linking pages.",
    )
    server: str | None = Field(
        default=None, description="Web server or CDN serving the page."
    )
    size: int | None = Field(default=None, description="Page size in bytes.")
    social_tags: SeoDomainPagesSocialTag | None = Field(
        default=None,
        alias="socialTags",
        description="Open Graph and Twitter card tags, by tag name.",
    )
    spam_score: int | None = Field(
        default=None,
        alias="spamScore",
        description="Average spam score of those backlinks on a 0-100 scale.",
    )
    status_code: int | None = Field(
        default=None,
        alias="statusCode",
        description="HTTP status of the page on the last crawl.",
    )
    technologies: SeoDomainPagesTechnologie | None = Field(
        default=None, description="Technologies detected on the page, by category."
    )
    title: str | None = Field(default=None, description="Page title.")
    tld: str | None = Field(default=None, description="Top-level domain of the page.")
    url: str = Field(
        description="Page URL. Populated whenever the provider has data for the entity."
    )
    words_count: int | None = Field(
        default=None, alias="wordsCount", description="Words on the page."
    )


class SeoDomainPagesLinksByAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainPagesLinksByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainPagesLinksByPlatformType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainPagesLinksBySemanticLocation(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainPagesLinksByTld(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainPagesLinksByType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainPagesSocialTag(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainPagesTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainRankOverviewData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str = Field(
        description="Analyzed domain. Populated whenever the provider has data for the entity."
    )
    language: str | None = Field(
        default=None, description="Language code the metrics are scoped to."
    )
    location: int | None = Field(
        default=None, description="Location code the metrics are scoped to."
    )
    organic_keywords: int | None = Field(
        default=None,
        alias="organicKeywords",
        description="Number of organic search results where the domain appears. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organic_pos1: int | None = Field(
        default=None,
        alias="organicPos1",
        description="Number of organic search results where the domain ranks first. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organic_pos2_to3: int | None = Field(
        default=None,
        alias="organicPos2To3",
        description="Number of organic search results where the domain ranks second or third. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organic_pos4_to10: int | None = Field(
        default=None,
        alias="organicPos4To10",
        description="Number of organic search results where the domain ranks fourth through tenth. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organic_traffic: float | None = Field(
        default=None,
        alias="organicTraffic",
        description="Estimated monthly organic search traffic. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organic_traffic_cost_usd: float | None = Field(
        default=None,
        alias="organicTrafficCostUsd",
        description="Estimated USD value of the organic search traffic. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    paid_keywords: int | None = Field(
        default=None,
        alias="paidKeywords",
        description="Number of paid search results where the domain appears.",
    )
    paid_pos1: int | None = Field(
        default=None,
        alias="paidPos1",
        description="Number of paid search results where the domain ranks first.",
    )
    paid_pos2_to3: int | None = Field(
        default=None,
        alias="paidPos2To3",
        description="Number of paid search results where the domain ranks second or third.",
    )
    paid_pos4_to10: int | None = Field(
        default=None,
        alias="paidPos4To10",
        description="Number of paid search results where the domain ranks fourth through tenth.",
    )
    paid_traffic: float | None = Field(
        default=None,
        alias="paidTraffic",
        description="Estimated monthly paid search traffic.",
    )
    paid_traffic_cost_usd: float | None = Field(
        default=None,
        alias="paidTrafficCostUsd",
        description="Estimated USD value of the paid search traffic.",
    )


class SeoDomainTechnologiesData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    content_language_code: str | None = Field(
        default=None,
        alias="contentLanguageCode",
        description="Language code detected from the domain's page content.",
    )
    country_iso_code: str | None = Field(
        default=None,
        alias="countryIsoCode",
        description="Two-letter ISO country code the domain is associated with.",
    )
    description: str | None = Field(
        default=None, description="Meta description of the domain's homepage."
    )
    domain: str = Field(
        description="Domain name that was analyzed, as the detection index stores it. Populated whenever the provider has data for the entity."
    )
    domain_rank: int | None = Field(
        default=None,
        alias="domainRank",
        description="Relative authority rank of the domain. Higher is stronger. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    emails: list[str] | None = Field(
        default=None, description="Contact email addresses published on the domain."
    )
    language_code: str | None = Field(
        default=None,
        alias="languageCode",
        description="Language code declared by the domain.",
    )
    last_visited_utc: float | None = Field(
        default=None,
        alias="lastVisitedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    phone_numbers: list[str] | None = Field(
        default=None,
        alias="phoneNumbers",
        description="Contact phone numbers published on the domain.",
    )
    social_graph_urls: list[str] | None = Field(
        default=None,
        alias="socialGraphUrls",
        description="Social profile URLs linked from the domain.",
    )
    technologies: SeoDomainTechnologiesTechnologie | None = Field(
        default=None,
        description="Technologies detected on the domain, nested by group and then by category, with an array of technology names at each leaf. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str | None = Field(
        default=None, description="Title of the domain's homepage."
    )


class SeoDomainTechnologiesTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoDomainsByTechnologyData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    domains: list[SeoDomainsByTechnologyDomain] = Field(
        description="Domains detected running the requested technology, category, group, or on-page term. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Cursor for the next page. Null or empty when there are no further results.",
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total number of domains matching the request across all pages.",
    )


class SeoDomainsByTechnologyDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    content_language_code: str | None = Field(
        default=None,
        alias="contentLanguageCode",
        description="Language code detected from the domain's page content.",
    )
    country_iso_code: str | None = Field(
        default=None,
        alias="countryIsoCode",
        description="Two-letter ISO country code the domain is associated with.",
    )
    description: str | None = Field(
        default=None, description="Meta description of the domain's homepage."
    )
    domain: str = Field(
        description="Domain name of the detected website. Populated whenever the provider has data for the entity."
    )
    domain_rank: int | None = Field(
        default=None,
        alias="domainRank",
        description="Relative authority rank of the domain. Higher is stronger. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    emails: list[str] | None = Field(
        default=None, description="Contact email addresses published on the domain."
    )
    keywords: list[str] | None = Field(
        default=None, description="Meta keywords declared on the domain's home page."
    )
    language_code: str | None = Field(
        default=None,
        alias="languageCode",
        description="Language code declared by the domain.",
    )
    last_visited_utc: float | None = Field(
        default=None,
        alias="lastVisitedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    phone_numbers: list[str] | None = Field(
        default=None,
        alias="phoneNumbers",
        description="Contact phone numbers published on the domain.",
    )
    social_graph_urls: list[str] | None = Field(
        default=None,
        alias="socialGraphUrls",
        description="Social profile URLs linked from the domain.",
    )
    technologies: SeoDomainsByTechnologyTechnologie | None = Field(
        default=None,
        description="Technologies detected on the domain, nested by group and then by category, with an array of technology names at each leaf. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str | None = Field(
        default=None, description="Title of the domain's homepage."
    )


class SeoDomainsByTechnologyTechnologie(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoKeywordDifficultyData(BaseModel):
    difficulties: list[SeoKeywordDifficultyDifficultie] = Field(
        description="SEO keyword difficulty records. Populated whenever the provider has data for the entity."
    )


class SeoKeywordDifficultyDifficultie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    keyword: str = Field(
        description="Keyword phrase. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Estimated organic ranking difficulty on a 0-100 scale. Omitted when the upstream has no difficulty for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoKeywordIdeasData(BaseModel):
    ideas: list[SeoKeywordIdeasIdea] = Field(
        description="SEO keyword idea records. Populated whenever the provider has data for the entity."
    )


class SeoKeywordIdeasIdea(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid_high: float | None = Field(
        default=None,
        alias="bidHigh",
        description="Upper bound of the estimated paid-search top-of-page bid in USD.",
    )
    bid_low: float | None = Field(
        default=None,
        alias="bidLow",
        description="Lower bound of the estimated paid-search top-of-page bid in USD.",
    )
    competition: str | None = Field(
        default=None,
        description="Paid-search competition level for the keyword idea. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cpc: float | None = Field(
        default=None,
        description="Average paid-search cost per click in USD. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    keyword: str = Field(
        description="Keyword idea phrase. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Estimated organic ranking difficulty on a 0-100 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    monthly_searches: list[SeoKeywordIdeasMonthlySearche] | None = Field(
        default=None,
        alias="monthlySearches",
        description="Monthly search-volume history for the keyword.",
    )
    search_intent: str | None = Field(
        default=None,
        alias="searchIntent",
        description="Primary SEO search intent for the keyword idea. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the keyword idea. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class SeoKeywordIdeasMonthlySearche(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month: int | None = Field(
        default=None,
        description="Calendar month number for the monthly search-volume record.",
    )
    search_volume: int | None = Field(
        default=None, alias="searchVolume", description="Search volume for the month."
    )
    year: int | None = Field(
        default=None, description="Calendar year for the monthly search-volume record."
    )


class SeoKeywordOverviewData(BaseModel):
    keywords: list[SeoKeywordOverviewKeyword] = Field(
        description="SEO keyword metric records. Populated whenever the provider has data for the entity."
    )


class SeoKeywordOverviewKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid_high: float | None = Field(
        default=None,
        alias="bidHigh",
        description="Upper bound of the estimated paid-search top-of-page bid in USD.",
    )
    bid_low: float | None = Field(
        default=None,
        alias="bidLow",
        description="Lower bound of the estimated paid-search top-of-page bid in USD.",
    )
    competition: str | None = Field(
        default=None,
        description="Paid-search competition level for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cpc: float | None = Field(
        default=None,
        description="Average paid-search cost per click in USD. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    keyword: str = Field(
        description="Keyword phrase. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Estimated organic ranking difficulty on a 0-100 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    monthly_searches: list[SeoKeywordOverviewMonthlySearche] | None = Field(
        default=None,
        alias="monthlySearches",
        description="Monthly search-volume history for the keyword.",
    )
    search_intent: str | None = Field(
        default=None,
        alias="searchIntent",
        description="Primary SEO search intent for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class SeoKeywordOverviewMonthlySearche(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month: int | None = Field(
        default=None,
        description="Calendar month number for the monthly search-volume record.",
    )
    search_volume: int | None = Field(
        default=None, alias="searchVolume", description="Search volume for the month."
    )
    year: int | None = Field(
        default=None, description="Calendar year for the monthly search-volume record."
    )


class SeoKeywordSuggestionsData(BaseModel):
    suggestions: list[SeoKeywordSuggestionsSuggestion] = Field(
        description="SEO keyword suggestion records. Populated whenever the provider has data for the entity."
    )


class SeoKeywordSuggestionsSuggestion(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid_high: float | None = Field(
        default=None,
        alias="bidHigh",
        description="Upper bound of the estimated paid-search top-of-page bid in USD.",
    )
    bid_low: float | None = Field(
        default=None,
        alias="bidLow",
        description="Lower bound of the estimated paid-search top-of-page bid in USD.",
    )
    competition: str | None = Field(
        default=None,
        description="Paid-search competition level for the keyword suggestion. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cpc: float | None = Field(
        default=None,
        description="Average paid-search cost per click in USD. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    keyword: str = Field(
        description="Keyword suggestion phrase. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Estimated organic ranking difficulty on a 0-100 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    monthly_searches: list[SeoKeywordSuggestionsMonthlySearche] | None = Field(
        default=None,
        alias="monthlySearches",
        description="Monthly search-volume history for the keyword.",
    )
    search_intent: str | None = Field(
        default=None,
        alias="searchIntent",
        description="Primary SEO search intent for the keyword suggestion. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the keyword suggestion. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class SeoKeywordSuggestionsMonthlySearche(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month: int | None = Field(
        default=None,
        description="Calendar month number for the monthly search-volume record.",
    )
    search_volume: int | None = Field(
        default=None, alias="searchVolume", description="Search volume for the month."
    )
    year: int | None = Field(
        default=None, description="Calendar year for the monthly search-volume record."
    )


class SeoLlmMentionsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mentions: list[SeoLlmMentionsMention] = Field(
        description="AI answers that mention the target. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total AI answers mentioning the target, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoLlmMentionsMention(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume for the question.",
    )
    answer: str | None = Field(
        default=None,
        description="The AI answer in markdown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    first_response_utc: float | None = Field(
        default=None,
        alias="firstResponseUtc",
        description="When this answer was first recorded. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    language: str | None = Field(
        default=None, description="Language code of the answer."
    )
    last_response_utc: float | None = Field(
        default=None,
        alias="lastResponseUtc",
        description="When this answer was last recorded. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    location: int | None = Field(
        default=None, description="Location code of the answer."
    )
    model: str | None = Field(
        default=None, description="Model that produced the answer."
    )
    monthly_searches: list[SeoLlmMentionsMonthlySearche] | None = Field(
        default=None,
        alias="monthlySearches",
        description="Monthly AI search-volume history for the question.",
    )
    platform: str | None = Field(
        default=None,
        description="AI surface that answered: google or chat_gpt. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    question: str = Field(
        description="Question the AI answered. Populated whenever the provider has data for the entity."
    )
    sources: list[SeoLlmMentionsSource] | None = Field(
        default=None, description="Sources the answer cites."
    )


class SeoLlmMentionsMonthlySearche(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month: int | None = Field(
        default=None,
        description="Calendar month number for the monthly search-volume record.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="AI search volume for the month.",
    )
    year: int | None = Field(
        default=None, description="Calendar year for the monthly search-volume record."
    )


class SeoLlmMentionsSource(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str | None = Field(default=None, description="Source domain.")
    position: int | None = Field(
        default=None, description="1-based position of the source in the answer."
    )
    snippet: str | None = Field(
        default=None, description="Text excerpt from the source."
    )
    source_name: str | None = Field(
        default=None, alias="sourceName", description="Publisher name."
    )
    title: str | None = Field(default=None, description="Source page title.")
    url: str = Field(description="Source URL.")


class SeoLlmTopBrandsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    brands: list[SeoLlmTopBrandsBrand] = Field(
        description="Brands named in matching AI answers, most mentioned first. Populated whenever the provider has data for the entity."
    )
    mentions: int | None = Field(
        default=None, description="AI answers matching the request."
    )
    overall_brand_categories: list[SeoLlmTopBrandsOverallBrandCategorie] | None = Field(
        default=None,
        alias="overallBrandCategories",
        description="Categories of the brands named in answers mentioning the target.",
    )
    overall_brands: list[SeoLlmTopBrandsOverallBrand] | None = Field(
        default=None,
        alias="overallBrands",
        description="Brands most often named in answers mentioning the target.",
    )
    overall_cited_domains: list[SeoLlmTopBrandsOverallCitedDomain] | None = Field(
        default=None,
        alias="overallCitedDomains",
        description="Domains most often cited as sources in answers mentioning the target.",
    )
    overall_languages: list[SeoLlmTopBrandsOverallLanguage] | None = Field(
        default=None,
        alias="overallLanguages",
        description="Mentions of the target, by language.",
    )
    overall_locations: list[SeoLlmTopBrandsOverallLocation] | None = Field(
        default=None,
        alias="overallLocations",
        description="Mentions of the target, by location.",
    )
    overall_platforms: list[SeoLlmTopBrandsOverallPlatform] | None = Field(
        default=None,
        alias="overallPlatforms",
        description="Mentions of the target, by AI surface.",
    )
    overall_search_result_domains: (
        list[SeoLlmTopBrandsOverallSearchResultDomain] | None
    ) = Field(
        default=None,
        alias="overallSearchResultDomains",
        description="Domains most often in the web results behind answers mentioning the target.",
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total brands matching the request, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoLlmTopBrandsBrand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    brand: str = Field(
        description="Brand name. Populated whenever the provider has data for the entity."
    )
    brand_categories: list[SeoLlmTopBrandsBrandCategorie] | None = Field(
        default=None,
        alias="brandCategories",
        description="Categories of the brands named in answers mentioning this brand.",
    )
    brands: list[SeoLlmTopBrandsBrand2] | None = Field(
        default=None,
        description="Brands most often named in answers mentioning this brand.",
    )
    cited_domains: list[SeoLlmTopBrandsCitedDomain] | None = Field(
        default=None,
        alias="citedDomains",
        description="Domains most often cited as sources in answers mentioning this brand.",
    )
    languages: list[SeoLlmTopBrandsLanguage] | None = Field(
        default=None, description="Mentions of this brand, by language."
    )
    locations: list[SeoLlmTopBrandsLocation] | None = Field(
        default=None, description="Mentions of this brand, by location."
    )
    mentions: int | None = Field(
        default=None,
        description="AI answers that mention this brand. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    platforms: list[SeoLlmTopBrandsPlatform] | None = Field(
        default=None, description="Mentions of this brand, by AI surface."
    )
    search_result_domains: list[SeoLlmTopBrandsSearchResultDomain] | None = Field(
        default=None,
        alias="searchResultDomains",
        description="Domains most often in the web results behind answers mentioning this brand.",
    )


class SeoLlmTopBrandsBrandCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    category: str = Field(description="Category of the named brand.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsBrand2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    brand: str = Field(description="Brand named in the answer.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsCitedDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain cited as a source.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsLanguage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    language: str = Field(description="Language code.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    location: int = Field(
        description="Location code, for example 2840 for the United States."
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsPlatform(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )
    platform: str = Field(description="AI surface: google (AI Overviews) or chat_gpt.")


class SeoLlmTopBrandsSearchResultDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain in the web results the AI consulted.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsOverallBrandCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    category: str = Field(description="Category of the named brand.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsOverallBrand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    brand: str = Field(description="Brand named in the answer.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsOverallCitedDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain cited as a source.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsOverallLanguage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    language: str = Field(description="Language code.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsOverallLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    location: int = Field(
        description="Location code, for example 2840 for the United States."
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopBrandsOverallPlatform(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )
    platform: str = Field(description="AI surface: google (AI Overviews) or chat_gpt.")


class SeoLlmTopBrandsOverallSearchResultDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain in the web results the AI consulted.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domains: list[SeoLlmTopDomainsDomain] = Field(
        description="Domains cited in matching AI answers, most mentioned first. Populated whenever the provider has data for the entity."
    )
    mentions: int | None = Field(
        default=None, description="AI answers matching the request."
    )
    overall_brand_categories: list[SeoLlmTopDomainsOverallBrandCategorie] | None = (
        Field(
            default=None,
            alias="overallBrandCategories",
            description="Categories of the brands named in answers mentioning the target.",
        )
    )
    overall_brands: list[SeoLlmTopDomainsOverallBrand] | None = Field(
        default=None,
        alias="overallBrands",
        description="Brands most often named in answers mentioning the target.",
    )
    overall_cited_domains: list[SeoLlmTopDomainsOverallCitedDomain] | None = Field(
        default=None,
        alias="overallCitedDomains",
        description="Domains most often cited as sources in answers mentioning the target.",
    )
    overall_languages: list[SeoLlmTopDomainsOverallLanguage] | None = Field(
        default=None,
        alias="overallLanguages",
        description="Mentions of the target, by language.",
    )
    overall_locations: list[SeoLlmTopDomainsOverallLocation] | None = Field(
        default=None,
        alias="overallLocations",
        description="Mentions of the target, by location.",
    )
    overall_platforms: list[SeoLlmTopDomainsOverallPlatform] | None = Field(
        default=None,
        alias="overallPlatforms",
        description="Mentions of the target, by AI surface.",
    )
    overall_search_result_domains: (
        list[SeoLlmTopDomainsOverallSearchResultDomain] | None
    ) = Field(
        default=None,
        alias="overallSearchResultDomains",
        description="Domains most often in the web results behind answers mentioning the target.",
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total domains matching the request, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoLlmTopDomainsDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    brand_categories: list[SeoLlmTopDomainsBrandCategorie] | None = Field(
        default=None,
        alias="brandCategories",
        description="Categories of the brands named in answers mentioning this domain.",
    )
    brands: list[SeoLlmTopDomainsBrand] | None = Field(
        default=None,
        description="Brands most often named in answers mentioning this domain.",
    )
    cited_domains: list[SeoLlmTopDomainsCitedDomain] | None = Field(
        default=None,
        alias="citedDomains",
        description="Domains most often cited as sources in answers mentioning this domain.",
    )
    domain: str = Field(
        description="Cited domain. Populated whenever the provider has data for the entity."
    )
    languages: list[SeoLlmTopDomainsLanguage] | None = Field(
        default=None, description="Mentions of this domain, by language."
    )
    locations: list[SeoLlmTopDomainsLocation] | None = Field(
        default=None, description="Mentions of this domain, by location."
    )
    mentions: int | None = Field(
        default=None,
        description="AI answers that mention this domain. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    platforms: list[SeoLlmTopDomainsPlatform] | None = Field(
        default=None, description="Mentions of this domain, by AI surface."
    )
    search_result_domains: list[SeoLlmTopDomainsSearchResultDomain] | None = Field(
        default=None,
        alias="searchResultDomains",
        description="Domains most often in the web results behind answers mentioning this domain.",
    )


class SeoLlmTopDomainsBrandCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    category: str = Field(description="Category of the named brand.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsBrand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    brand: str = Field(description="Brand named in the answer.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsCitedDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain cited as a source.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsLanguage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    language: str = Field(description="Language code.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    location: int = Field(
        description="Location code, for example 2840 for the United States."
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsPlatform(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )
    platform: str = Field(description="AI surface: google (AI Overviews) or chat_gpt.")


class SeoLlmTopDomainsSearchResultDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain in the web results the AI consulted.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsOverallBrandCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    category: str = Field(description="Category of the named brand.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsOverallBrand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    brand: str = Field(description="Brand named in the answer.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsOverallCitedDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain cited as a source.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsOverallLanguage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    language: str = Field(description="Language code.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsOverallLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    location: int = Field(
        description="Location code, for example 2840 for the United States."
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopDomainsOverallPlatform(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )
    platform: str = Field(description="AI surface: google (AI Overviews) or chat_gpt.")


class SeoLlmTopDomainsOverallSearchResultDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain in the web results the AI consulted.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    mentions: int | None = Field(
        default=None, description="AI answers matching the request."
    )
    overall_brand_categories: list[SeoLlmTopPagesOverallBrandCategorie] | None = Field(
        default=None,
        alias="overallBrandCategories",
        description="Categories of the brands named in answers mentioning the target.",
    )
    overall_brands: list[SeoLlmTopPagesOverallBrand] | None = Field(
        default=None,
        alias="overallBrands",
        description="Brands most often named in answers mentioning the target.",
    )
    overall_cited_domains: list[SeoLlmTopPagesOverallCitedDomain] | None = Field(
        default=None,
        alias="overallCitedDomains",
        description="Domains most often cited as sources in answers mentioning the target.",
    )
    overall_languages: list[SeoLlmTopPagesOverallLanguage] | None = Field(
        default=None,
        alias="overallLanguages",
        description="Mentions of the target, by language.",
    )
    overall_locations: list[SeoLlmTopPagesOverallLocation] | None = Field(
        default=None,
        alias="overallLocations",
        description="Mentions of the target, by location.",
    )
    overall_platforms: list[SeoLlmTopPagesOverallPlatform] | None = Field(
        default=None,
        alias="overallPlatforms",
        description="Mentions of the target, by AI surface.",
    )
    overall_search_result_domains: (
        list[SeoLlmTopPagesOverallSearchResultDomain] | None
    ) = Field(
        default=None,
        alias="overallSearchResultDomains",
        description="Domains most often in the web results behind answers mentioning the target.",
    )
    pages: list[SeoLlmTopPagesPage] = Field(
        description="Pages cited in matching AI answers, most mentioned first. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total pages matching the request, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoLlmTopPagesOverallBrandCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    category: str = Field(description="Category of the named brand.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesOverallBrand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    brand: str = Field(description="Brand named in the answer.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesOverallCitedDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain cited as a source.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesOverallLanguage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    language: str = Field(description="Language code.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesOverallLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    location: int = Field(
        description="Location code, for example 2840 for the United States."
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesOverallPlatform(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )
    platform: str = Field(description="AI surface: google (AI Overviews) or chat_gpt.")


class SeoLlmTopPagesOverallSearchResultDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain in the web results the AI consulted.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesPage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    brand_categories: list[SeoLlmTopPagesBrandCategorie] | None = Field(
        default=None,
        alias="brandCategories",
        description="Categories of the brands named in answers mentioning this page.",
    )
    brands: list[SeoLlmTopPagesBrand] | None = Field(
        default=None,
        description="Brands most often named in answers mentioning this page.",
    )
    cited_domains: list[SeoLlmTopPagesCitedDomain] | None = Field(
        default=None,
        alias="citedDomains",
        description="Domains most often cited as sources in answers mentioning this page.",
    )
    languages: list[SeoLlmTopPagesLanguage] | None = Field(
        default=None, description="Mentions of this page, by language."
    )
    locations: list[SeoLlmTopPagesLocation] | None = Field(
        default=None, description="Mentions of this page, by location."
    )
    mentions: int | None = Field(
        default=None,
        description="AI answers that mention this page. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    page: str = Field(
        description="Cited page URL. Populated whenever the provider has data for the entity."
    )
    platforms: list[SeoLlmTopPagesPlatform] | None = Field(
        default=None, description="Mentions of this page, by AI surface."
    )
    search_result_domains: list[SeoLlmTopPagesSearchResultDomain] | None = Field(
        default=None,
        alias="searchResultDomains",
        description="Domains most often in the web results behind answers mentioning this page.",
    )


class SeoLlmTopPagesBrandCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    category: str = Field(description="Category of the named brand.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesBrand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    brand: str = Field(description="Brand named in the answer.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesCitedDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain cited as a source.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesLanguage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    language: str = Field(description="Language code.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    location: int = Field(
        description="Location code, for example 2840 for the United States."
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLlmTopPagesPlatform(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )
    platform: str = Field(description="AI surface: google (AI Overviews) or chat_gpt.")


class SeoLlmTopPagesSearchResultDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ai_search_volume: int | None = Field(
        default=None,
        alias="aiSearchVolume",
        description="Estimated monthly AI search volume of those answers.",
    )
    domain: str = Field(description="Domain in the web results the AI consulted.")
    mentions: int | None = Field(
        default=None, description="AI answers counted in this group."
    )


class SeoLocalPackData(BaseModel):
    places: list[SeoLocalPackPlace] = Field(
        description="Businesses in the Google local pack, in the order Google shows them. Populated whenever the provider has data for the entity."
    )


class SeoLocalPackPlace(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None,
        description="The address line Google shows for the business in the pack. For a business that serves an area rather than a storefront, Google shows years in business and the city here instead.",
    )
    booking_url: str | None = Field(
        default=None,
        alias="bookingUrl",
        description="Booking link Google shows for the business, when it has one. The query string carries the booking session, so it is kept.",
    )
    category: str | None = Field(
        default=None,
        description="Business category Google shows, such as Coffee shop or Plumber.",
    )
    cid: str | None = Field(
        default=None, description="Google customer id (CID) of the business listing."
    )
    description: str | None = Field(
        default=None,
        description="The text Google prints under the business name in the pack. Usually it is every line: the street address or years in business, opening hours, and a review quote. On some responses it is only the review quote, with the address and hours in their own fields.",
    )
    directions_url: str | None = Field(
        default=None,
        alias="directionsUrl",
        description="Google Maps directions link to the business, with tracking query parameters removed.",
    )
    domain: str | None = Field(
        default=None,
        description="Host name of the business website, such as www.example.com.",
    )
    hours: str | None = Field(
        default=None,
        description="Opening hours text Google shows, such as Open 24 hours or Closed - Opens 7 AM.",
    )
    image: str | None = Field(
        default=None, description="Thumbnail photo URL Google shows for the business."
    )
    knowledge_graph_id: str | None = Field(
        default=None,
        alias="knowledgeGraphId",
        description="Google Knowledge Graph id of the business, such as /g/11vb1r7rlr.",
    )
    name: str = Field(
        description="Business name. Populated whenever the provider has data for the entity."
    )
    phone: str | None = Field(
        default=None,
        description="Business phone number, when Google shows one, as Google prints it: national format such as (512) 890-2933 or international format such as +1 512-890-2933.",
    )
    position: int = Field(
        description="One-based position of the business in the local pack, counting only unpaid listings. Populated whenever the provider has data for the entity."
    )
    price_level: str | None = Field(
        default=None,
        alias="priceLevel",
        description="Price range Google shows for the business, such as $10-20.",
    )
    rank_absolute: int | None = Field(
        default=None,
        alias="rankAbsolute",
        description="Position of the business among every element of the Google results page, counting from the top.",
    )
    rank_group: int | None = Field(
        default=None,
        alias="rankGroup",
        description="Position Google gives the business inside the local pack, counting sponsored listings, so it can be higher than position when an ad sits above it.",
    )
    rating: float | None = Field(
        default=None,
        description="Average Google star rating out of 5. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reviews_count: int | None = Field(
        default=None,
        alias="reviewsCount",
        description="Number of Google reviews behind the rating. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Business website URL, when listed, with tracking query parameters removed.",
    )


class SeoRankedKeywordsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ranked_keywords: list[SeoRankedKeywordsRankedKeyword] = Field(
        alias="rankedKeywords",
        description="SEO ranked keyword records for the domain. Populated whenever the provider has data for the entity.",
    )


class SeoRankedKeywordsRankedKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    competition: str | None = Field(
        default=None,
        description="Paid-search competition level for the keyword (LOW, MEDIUM, HIGH).",
    )
    cpc: float | None = Field(
        default=None, description="Average paid-search cost per click in USD."
    )
    description: str | None = Field(
        default=None, description="Search-result snippet of the ranking page."
    )
    domain: str | None = Field(default=None, description="Domain of the ranking page.")
    etv: float | None = Field(
        default=None,
        description="Estimated organic search traffic for the ranking URL.",
    )
    keyword: str = Field(
        description="Keyword phrase the domain ranks for. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Estimated organic ranking difficulty on a 0-100 scale.",
    )
    rank_absolute: int = Field(
        alias="rankAbsolute",
        description="Absolute organic ranking position for the keyword. Populated whenever the provider has data for the entity.",
    )
    rank_group: int | None = Field(
        default=None,
        alias="rankGroup",
        description="Grouped organic ranking position for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    search_intent: str | None = Field(
        default=None,
        alias="searchIntent",
        description="Primary SEO search intent for the keyword.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str | None = Field(
        default=None, description="Search-result title of the ranking page."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="SERP element type the ranking appeared as (e.g. organic, featured_snippet).",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str | None = Field(default=None, description="Ranking URL for the domain.")


class SeoReferringDomainsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    referring_domains: list[SeoReferringDomainsReferringDomain] = Field(
        alias="referringDomains",
        description="Domains linking to the target. Populated whenever the provider has data for the entity.",
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total referring domains, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoReferringDomainsReferringDomain(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    backlinks: int | None = Field(
        default=None,
        description="Backlinks from this domain to the target. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    broken_backlinks: int | None = Field(
        default=None,
        alias="brokenBacklinks",
        description="Backlinks from this domain to target pages that no longer resolve.",
    )
    broken_pages: int | None = Field(
        default=None,
        alias="brokenPages",
        description="Target pages with an error status that this domain still links to.",
    )
    domain: str = Field(
        description="Referring domain. Populated whenever the provider has data for the entity."
    )
    first_seen_utc: float | None = Field(
        default=None,
        alias="firstSeenUtc",
        description="When a link from this domain was first seen. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    links_by_attribute: SeoReferringDomainsLinksByAttribute | None = Field(
        default=None,
        alias="linksByAttribute",
        description="Count of this domain's links to the target, by rel attribute (nofollow, sponsored, ugc, noopener, and so on).",
    )
    links_by_country: SeoReferringDomainsLinksByCountry | None = Field(
        default=None,
        alias="linksByCountry",
        description="Count of this domain's links to the target, by country code of the linking domain. An empty key means the country is unknown.",
    )
    links_by_platform_type: SeoReferringDomainsLinksByPlatformType | None = Field(
        default=None,
        alias="linksByPlatformType",
        description="Count of this domain's links to the target, by type of linking site (blogs, news, ecommerce, and so on).",
    )
    links_by_semantic_location: SeoReferringDomainsLinksBySemanticLocation | None = (
        Field(
            default=None,
            alias="linksBySemanticLocation",
            description="Count of this domain's links to the target, by the page section holding the link (article, footer, nav, and so on). An empty key means no section was detected.",
        )
    )
    links_by_tld: SeoReferringDomainsLinksByTld | None = Field(
        default=None,
        alias="linksByTld",
        description="Count of this domain's links to the target, by top-level domain of the linking page.",
    )
    links_by_type: SeoReferringDomainsLinksByType | None = Field(
        default=None,
        alias="linksByType",
        description="Count of this domain's links to the target, by link type (anchor, image, redirect, canonical, alternate).",
    )
    lost_utc: float | None = Field(
        default=None,
        alias="lostUtc",
        description="When this domain's last link to the target was lost, if it was. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    rank: int | None = Field(
        default=None,
        description="Authority rank of the referring domain on a 0-1000 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    referring_domains: int | None = Field(
        default=None,
        alias="referringDomains",
        description="Distinct domains linking to this referring domain.",
    )
    referring_domains_nofollow: int | None = Field(
        default=None,
        alias="referringDomainsNofollow",
        description="Domains whose every link to this referring domain is nofollow.",
    )
    referring_ips: int | None = Field(
        default=None,
        alias="referringIps",
        description="Distinct IP addresses among this domain's linking pages.",
    )
    referring_main_domains: int | None = Field(
        default=None,
        alias="referringMainDomains",
        description="Distinct registrable domains linking to this referring domain.",
    )
    referring_main_domains_nofollow: int | None = Field(
        default=None,
        alias="referringMainDomainsNofollow",
        description="Registrable domains whose every link to this referring domain is nofollow.",
    )
    referring_pages: int | None = Field(
        default=None,
        alias="referringPages",
        description="Pages on this domain linking to the target.",
    )
    referring_pages_nofollow: int | None = Field(
        default=None,
        alias="referringPagesNofollow",
        description="Pages on this domain whose links to the target are all nofollow.",
    )
    referring_subnets: int | None = Field(
        default=None,
        alias="referringSubnets",
        description="Distinct subnets among this domain's linking pages.",
    )
    spam_score: int | None = Field(
        default=None,
        alias="spamScore",
        description="Average spam score of this domain's backlinks on a 0-100 scale.",
    )


class SeoReferringDomainsLinksByAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoReferringDomainsLinksByCountry(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoReferringDomainsLinksByPlatformType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoReferringDomainsLinksBySemanticLocation(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoReferringDomainsLinksByTld(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoReferringDomainsLinksByType(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeoRelatedKeywordsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    related_keywords: list[SeoRelatedKeywordsRelatedKeyword] = Field(
        alias="relatedKeywords",
        description="SEO related keyword records. Populated whenever the provider has data for the entity.",
    )


class SeoRelatedKeywordsRelatedKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid_high: float | None = Field(
        default=None,
        alias="bidHigh",
        description="Upper bound of the estimated paid-search top-of-page bid in USD.",
    )
    bid_low: float | None = Field(
        default=None,
        alias="bidLow",
        description="Lower bound of the estimated paid-search top-of-page bid in USD.",
    )
    competition: str | None = Field(
        default=None,
        description="Paid-search competition level for the related keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cpc: float | None = Field(
        default=None,
        description="Average paid-search cost per click in USD. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    depth: int | None = Field(
        default=None,
        description="Related-keyword graph depth from the seed keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    keyword: str = Field(
        description="Related keyword phrase. Populated whenever the provider has data for the entity."
    )
    keyword_difficulty: int | None = Field(
        default=None,
        alias="keywordDifficulty",
        description="Estimated organic ranking difficulty on a 0-100 scale. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    keywords: list[str] | None = Field(
        default=None, description="Further keywords DataForSEO relates to this one."
    )
    monthly_searches: list[SeoRelatedKeywordsMonthlySearche] | None = Field(
        default=None,
        alias="monthlySearches",
        description="Monthly search-volume history for the keyword.",
    )
    search_intent: str | None = Field(
        default=None,
        alias="searchIntent",
        description="Primary SEO search intent for the related keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the related keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class SeoRelatedKeywordsMonthlySearche(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month: int | None = Field(
        default=None,
        description="Calendar month number for the monthly search-volume record.",
    )
    search_volume: int | None = Field(
        default=None, alias="searchVolume", description="Search volume for the month."
    )
    year: int | None = Field(
        default=None, description="Calendar year for the monthly search-volume record."
    )


class SeoSearchIntentData(BaseModel):
    intents: list[SeoSearchIntentIntent] = Field(
        description="SEO keyword search intent records. Populated whenever the provider has data for the entity."
    )


class SeoSearchIntentIntent(BaseModel):
    model_config = ConfigDict(extra="allow")

    intent: str = Field(
        description="Primary SEO search intent for the keyword. Populated whenever the provider has data for the entity."
    )
    keyword: str = Field(
        description="Keyword phrase. Populated whenever the provider has data for the entity."
    )


class SeoSearchVolumeData(BaseModel):
    keywords: list[SeoSearchVolumeKeyword] = Field(
        description="SEO keyword search-volume records. Populated whenever the provider has data for the entity."
    )


class SeoSearchVolumeKeyword(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid_high: float | None = Field(
        default=None,
        alias="bidHigh",
        description="Upper bound of the estimated paid-search top-of-page bid in USD.",
    )
    bid_low: float | None = Field(
        default=None,
        alias="bidLow",
        description="Lower bound of the estimated paid-search top-of-page bid in USD.",
    )
    competition: str | None = Field(
        default=None,
        description="Paid-search competition level for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    competition_index: int | None = Field(
        default=None,
        alias="competitionIndex",
        description="Paid-search competition index for the keyword.",
    )
    cpc: float | None = Field(
        default=None,
        description="Average paid-search cost per click in USD. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    keyword: str = Field(
        description="Keyword phrase. Populated whenever the provider has data for the entity."
    )
    monthly_searches: list[SeoSearchVolumeMonthlySearche] | None = Field(
        default=None,
        alias="monthlySearches",
        description="Monthly search-volume history for the keyword.",
    )
    search_volume: int | None = Field(
        default=None,
        alias="searchVolume",
        description="Average monthly search volume for the keyword. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoSearchVolumeMonthlySearche(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    month: int | None = Field(
        default=None,
        description="Calendar month number for the monthly search-volume record.",
    )
    search_volume: int | None = Field(
        default=None, alias="searchVolume", description="Search volume for the month."
    )
    year: int | None = Field(
        default=None, description="Calendar year for the monthly search-volume record."
    )


class SeoTopPagesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pages: list[SeoTopPagesPage] = Field(
        description="Pages of the domain ranked by organic search traffic. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="Total ranking pages, before the limit. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class SeoTopPagesPage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    organic_down: int | None = Field(
        default=None,
        alias="organicDown",
        description="Organic keywords that moved down since the previous update.",
    )
    organic_keywords: int | None = Field(
        default=None,
        alias="organicKeywords",
        description="Keywords the page ranks for in organic results. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organic_lost: int | None = Field(
        default=None,
        alias="organicLost",
        description="Organic keywords no longer ranking since the previous update.",
    )
    organic_new: int | None = Field(
        default=None,
        alias="organicNew",
        description="Organic keywords newly ranking since the previous update.",
    )
    organic_pos1: int | None = Field(
        default=None,
        alias="organicPos1",
        description="Organic keywords ranking the page at positions 1.",
    )
    organic_pos11_to20: int | None = Field(
        default=None,
        alias="organicPos11To20",
        description="Organic keywords ranking the page at positions 11-20.",
    )
    organic_pos21_to30: int | None = Field(
        default=None,
        alias="organicPos21To30",
        description="Organic keywords ranking the page at positions 21-30.",
    )
    organic_pos2_to3: int | None = Field(
        default=None,
        alias="organicPos2To3",
        description="Organic keywords ranking the page at positions 2-3.",
    )
    organic_pos31_to40: int | None = Field(
        default=None,
        alias="organicPos31To40",
        description="Organic keywords ranking the page at positions 31-40.",
    )
    organic_pos41_to50: int | None = Field(
        default=None,
        alias="organicPos41To50",
        description="Organic keywords ranking the page at positions 41-50.",
    )
    organic_pos4_to10: int | None = Field(
        default=None,
        alias="organicPos4To10",
        description="Organic keywords ranking the page at positions 4-10.",
    )
    organic_pos51_to60: int | None = Field(
        default=None,
        alias="organicPos51To60",
        description="Organic keywords ranking the page at positions 51-60.",
    )
    organic_pos61_to70: int | None = Field(
        default=None,
        alias="organicPos61To70",
        description="Organic keywords ranking the page at positions 61-70.",
    )
    organic_pos71_to80: int | None = Field(
        default=None,
        alias="organicPos71To80",
        description="Organic keywords ranking the page at positions 71-80.",
    )
    organic_pos81_to90: int | None = Field(
        default=None,
        alias="organicPos81To90",
        description="Organic keywords ranking the page at positions 81-90.",
    )
    organic_pos91_to100: int | None = Field(
        default=None,
        alias="organicPos91To100",
        description="Organic keywords ranking the page at positions 91-100.",
    )
    organic_traffic: float | None = Field(
        default=None,
        alias="organicTraffic",
        description="Estimated monthly organic traffic to the page. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organic_traffic_cost_usd: float | None = Field(
        default=None,
        alias="organicTrafficCostUsd",
        description="Estimated monthly cost in USD of buying the page's organic traffic as ads.",
    )
    organic_up: int | None = Field(
        default=None,
        alias="organicUp",
        description="Organic keywords that moved up since the previous update.",
    )
    paid_down: int | None = Field(
        default=None,
        alias="paidDown",
        description="Paid keywords that moved down since the previous update.",
    )
    paid_keywords: int | None = Field(
        default=None,
        alias="paidKeywords",
        description="Keywords the page ranks for in paid results.",
    )
    paid_lost: int | None = Field(
        default=None,
        alias="paidLost",
        description="Paid keywords no longer ranking since the previous update.",
    )
    paid_new: int | None = Field(
        default=None,
        alias="paidNew",
        description="Paid keywords newly ranking since the previous update.",
    )
    paid_pos1: int | None = Field(
        default=None,
        alias="paidPos1",
        description="Paid keywords ranking the page at positions 1.",
    )
    paid_pos11_to20: int | None = Field(
        default=None,
        alias="paidPos11To20",
        description="Paid keywords ranking the page at positions 11-20.",
    )
    paid_pos21_to30: int | None = Field(
        default=None,
        alias="paidPos21To30",
        description="Paid keywords ranking the page at positions 21-30.",
    )
    paid_pos2_to3: int | None = Field(
        default=None,
        alias="paidPos2To3",
        description="Paid keywords ranking the page at positions 2-3.",
    )
    paid_pos31_to40: int | None = Field(
        default=None,
        alias="paidPos31To40",
        description="Paid keywords ranking the page at positions 31-40.",
    )
    paid_pos41_to50: int | None = Field(
        default=None,
        alias="paidPos41To50",
        description="Paid keywords ranking the page at positions 41-50.",
    )
    paid_pos4_to10: int | None = Field(
        default=None,
        alias="paidPos4To10",
        description="Paid keywords ranking the page at positions 4-10.",
    )
    paid_pos51_to60: int | None = Field(
        default=None,
        alias="paidPos51To60",
        description="Paid keywords ranking the page at positions 51-60.",
    )
    paid_pos61_to70: int | None = Field(
        default=None,
        alias="paidPos61To70",
        description="Paid keywords ranking the page at positions 61-70.",
    )
    paid_pos71_to80: int | None = Field(
        default=None,
        alias="paidPos71To80",
        description="Paid keywords ranking the page at positions 71-80.",
    )
    paid_pos81_to90: int | None = Field(
        default=None,
        alias="paidPos81To90",
        description="Paid keywords ranking the page at positions 81-90.",
    )
    paid_pos91_to100: int | None = Field(
        default=None,
        alias="paidPos91To100",
        description="Paid keywords ranking the page at positions 91-100.",
    )
    paid_traffic: float | None = Field(
        default=None,
        alias="paidTraffic",
        description="Estimated monthly paid traffic to the page.",
    )
    paid_traffic_cost_usd: float | None = Field(
        default=None,
        alias="paidTrafficCostUsd",
        description="Estimated monthly cost in USD of buying the page's paid traffic as ads.",
    )
    paid_up: int | None = Field(
        default=None,
        alias="paidUp",
        description="Paid keywords that moved up since the previous update.",
    )
    url: str = Field(
        description="Page URL. Populated whenever the provider has data for the entity."
    )


class SeoNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def backlink_anchors(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinkAnchorsInput],
    ) -> RunResult[SeoBacklinkAnchorsData]:
        """SEO Backlink Anchors

        Get AnyAPI SEO anchor texts of the backlinks pointing at a domain or URL,
        each with backlink and referring domain counts, authority rank, and spam
        score as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.backlink_anchors(limit=10, target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlink_anchors", dict(input), options
        )
        return RunResult[SeoBacklinkAnchorsData].model_validate(raw)

    def backlink_competitors(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinkCompetitorsInput],
    ) -> RunResult[SeoBacklinkCompetitorsData]:
        """SEO Backlink Competitors

        Find the domains that share the most backlinks with a domain or URL, each
        with its authority rank and shared backlink count as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.backlink_competitors(limit=10, target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlink_competitors", dict(input), options
        )
        return RunResult[SeoBacklinkCompetitorsData].model_validate(raw)

    def backlinks(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinksInput],
    ) -> RunResult[SeoBacklinksData]:
        """SEO Backlinks

        Get AnyAPI SEO backlinks for a domain or URL, each with the linking page,
        anchor text, dofollow flag, authority rank, spam score, and first and last
        seen dates as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.backlinks(limit=10, target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlinks", dict(input), options
        )
        return RunResult[SeoBacklinksData].model_validate(raw)

    def backlinks_summary(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinksSummaryInput],
    ) -> RunResult[SeoBacklinksSummaryData]:
        """SEO Backlinks Summary

        Get AnyAPI SEO backlink profile totals for a domain or URL: backlinks,
        referring domains, authority rank, spam score, and broken links as
        normalized JSON.

        Price: $0.02885 per request plus $0 per result (maximum $0.02885).

        Example:
            res = client.seo.backlinks_summary(target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlinks_summary", dict(input), options
        )
        return RunResult[SeoBacklinksSummaryData].model_validate(raw)

    def competitors_domain(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoCompetitorsDomainInput],
    ) -> RunResult[SeoCompetitorsDomainData]:
        """SEO Competitor Domains

        Get AnyAPI SEO competitor domains for a target domain with shared keyword
        counts and organic metrics as normalized JSON.

        Price: $0.02864 per request plus $0.00016 per result (maximum $0.18864).

        Example:
            res = client.seo.competitors_domain(language="en", limit=10, location=2840, target="github.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.competitors_domain", dict(input), options
        )
        return RunResult[SeoCompetitorsDomainData].model_validate(raw)

    def domain_intersection(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainIntersectionInput],
    ) -> RunResult[SeoDomainIntersectionData]:
        """SEO Domain Intersection

        Get AnyAPI SEO keyword overlap for two domains with each domain's rankings,
        URLs, volume, CPC, and difficulty as normalized JSON.

        Price: $0.02864 per request plus $0.00016 per result (maximum $0.18864).

        Example:
            res = client.seo.domain_intersection(language="en", limit=10, location=2840, target1="github.com", target2="gitlab.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_intersection", dict(input), options
        )
        return RunResult[SeoDomainIntersectionData].model_validate(raw)

    def domain_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainPagesInput],
    ) -> RunResult[SeoDomainPagesData]:
        """SEO Domain Pages

        Get AnyAPI SEO pages of a domain with their backlink profile (rank,
        backlinks, referring domains) and on-page data (title, headings, word count,
        status, technologies) as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.domain_pages(limit=10, target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_pages", dict(input), options
        )
        return RunResult[SeoDomainPagesData].model_validate(raw)

    def domain_rank_overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainRankOverviewInput],
    ) -> RunResult[SeoDomainRankOverviewData]:
        """SEO Domain Rank Overview

        Get AnyAPI SEO domain ranking, organic traffic, and paid traffic metrics as
        normalized JSON.

        Price: $0.01455 per request plus $0 per result (maximum $0.01455).

        Example:
            res = client.seo.domain_rank_overview(language="en", location=2840, target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_rank_overview", dict(input), options
        )
        return RunResult[SeoDomainRankOverviewData].model_validate(raw)

    def domain_technologies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainTechnologiesInput],
    ) -> RunResult[SeoDomainTechnologiesData]:
        """SEO Domain Technologies

        Detect the technology stack a website runs: CMS, analytics, marketing,
        hosting, and security, plus contacts and social profiles as normalized JSON.

        Price: $0.0144 per request.

        Example:
            res = client.seo.domain_technologies(domain="hubspot.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_technologies", dict(input), options
        )
        return RunResult[SeoDomainTechnologiesData].model_validate(raw)

    def domains_by_technology(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainsByTechnologyInput],
    ) -> RunResult[SeoDomainsByTechnologyData]:
        """SEO Domains By Technology

        Find websites running a given technology, category, or on-page term: domain,
        rank, detected stack, contacts, and social profiles as normalized JSON.

        Price: $0.01464 per request plus $0.0012 per result (maximum $0.13464).

        Example:
            res = client.seo.domains_by_technology(keyword="highlevel", limit=10, orderBy="rank_desc")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domains_by_technology", dict(input), options
        )
        return RunResult[SeoDomainsByTechnologyData].model_validate(raw)

    def iter_domains_by_technology(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainsByTechnologyInput],
    ) -> Paginator[SeoDomainsByTechnologyDomain, SeoDomainsByTechnologyData]:
        """Iterate SEO Domains By Technology results, following pagination cursors.

        Yields validated `SeoDomainsByTechnologyDomain` items from the `domains` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "seo.domains_by_technology",
            dict(input),
            "domains",
            item_model=SeoDomainsByTechnologyDomain,
            data_model=SeoDomainsByTechnologyData,
            bare=False,
            options=options,
        )

    def keyword_difficulty(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordDifficultyInput],
    ) -> RunResult[SeoKeywordDifficultyData]:
        """SEO Keyword Difficulty

        Get AnyAPI SEO keyword difficulty scores for one or more keywords as
        normalized JSON.

        Price: $0.01438 per request plus $0.00016 per keyword (maximum $0.17438).

        Example:
            res = client.seo.keyword_difficulty(keywords=["seo tools"], language="en", location=2840)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_difficulty", dict(input), options
        )
        return RunResult[SeoKeywordDifficultyData].model_validate(raw)

    def keyword_ideas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordIdeasInput],
    ) -> RunResult[SeoKeywordIdeasData]:
        """SEO Keyword Ideas

        Find AnyAPI SEO keyword ideas from seed terms with volume, CPC, competition,
        difficulty, and intent as normalized JSON.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.keyword_ideas(keywords=["project management software"], language="en", limit=5, location=2840)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_ideas", dict(input), options
        )
        return RunResult[SeoKeywordIdeasData].model_validate(raw)

    def keyword_overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordOverviewInput],
    ) -> RunResult[SeoKeywordOverviewData]:
        """SEO Keyword Overview

        Get AnyAPI SEO keyword metrics including search volume, CPC, competition,
        difficulty, and search intent as normalized JSON.

        Price: $0.01438 per request plus $0.00016 per keyword (maximum $0.12638).

        Example:
            res = client.seo.keyword_overview(keywords=["project management software"], language="en", location=2840)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_overview", dict(input), options
        )
        return RunResult[SeoKeywordOverviewData].model_validate(raw)

    def keyword_suggestions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordSuggestionsInput],
    ) -> RunResult[SeoKeywordSuggestionsData]:
        """SEO Keyword Suggestions

        Find AnyAPI SEO keyword suggestions from a seed term with volume, CPC,
        competition, difficulty, and intent as normalized JSON.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.keyword_suggestions(keyword="project management software", language="en", limit=5, location=2840)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_suggestions", dict(input), options
        )
        return RunResult[SeoKeywordSuggestionsData].model_validate(raw)

    def llm_mentions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmMentionsInput],
    ) -> RunResult[SeoLlmMentionsData]:
        """SEO LLM Mentions

        Find AI answers that mention a domain or keyword, from Google AI Overviews
        or ChatGPT, each with the question asked, the answer, its cited sources, and
        AI search volume as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_mentions(domain="ahrefs.com", limit=5, platform="google")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_mentions", dict(input), options
        )
        return RunResult[SeoLlmMentionsData].model_validate(raw)

    def llm_top_brands(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmTopBrandsInput],
    ) -> RunResult[SeoLlmTopBrandsData]:
        """SEO LLM Top Brands

        Rank the brands ChatGPT names most often in answers about a keyword or
        domain, each with mention count, AI search volume, and the sources and
        categories behind them as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_top_brands(keyword="seo tools", limit=5)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_top_brands", dict(input), options
        )
        return RunResult[SeoLlmTopBrandsData].model_validate(raw)

    def llm_top_domains(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmTopDomainsInput],
    ) -> RunResult[SeoLlmTopDomainsData]:
        """SEO LLM Top Domains

        Rank the domains Google AI Overviews and ChatGPT cite most often in answers
        about a keyword or domain, each with mention count, AI search volume, and
        breakdowns by platform, location, and co-cited sources as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_top_domains(keyword="seo tools", limit=5)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_top_domains", dict(input), options
        )
        return RunResult[SeoLlmTopDomainsData].model_validate(raw)

    def llm_top_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmTopPagesInput],
    ) -> RunResult[SeoLlmTopPagesData]:
        """SEO LLM Top Pages

        Rank the pages Google AI Overviews and ChatGPT cite most often in answers
        about a keyword or domain, each with mention count, AI search volume, and
        breakdowns by platform, location, and co-cited sources as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_top_pages(keyword="seo tools", limit=5)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_top_pages", dict(input), options
        )
        return RunResult[SeoLlmTopPagesData].model_validate(raw)

    def local_pack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLocalPackInput],
    ) -> RunResult[SeoLocalPackData]:
        """Google Local Pack

        Get the Google local pack for a keyword in a city: the short list of
        businesses Google shows in the map box on its normal search results page, in
        pack order, with rating, review count, address, category, opening hours,
        phone, website, booking link, and Google listing ids. Sponsored listings are
        left out. For the full Google Maps results list, use maps.search.

        Price: $0.0015 per request.

        Example:
            res = client.seo.local_pack(keyword="coffee shop", language="en", location="New York,New York,United States")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.local_pack", dict(input), options
        )
        return RunResult[SeoLocalPackData].model_validate(raw)

    def ranked_keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoRankedKeywordsInput],
    ) -> RunResult[SeoRankedKeywordsData]:
        """SEO Ranked Keywords

        Get AnyAPI SEO ranked keywords for a domain with rankings, traffic
        estimates, volume, CPC, difficulty, and intent as normalized JSON. One call
        returns up to 1,000 keywords; use offset to page further.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.ranked_keywords(language="en", limit=10, location=2840, target="github.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.ranked_keywords", dict(input), options
        )
        return RunResult[SeoRankedKeywordsData].model_validate(raw)

    def referring_domains(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoReferringDomainsInput],
    ) -> RunResult[SeoReferringDomainsData]:
        """SEO Referring Domains

        Get AnyAPI SEO referring domains for a domain or URL, each with its backlink
        count, authority rank, spam score, and first seen date as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.referring_domains(limit=10, target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.referring_domains", dict(input), options
        )
        return RunResult[SeoReferringDomainsData].model_validate(raw)

    def related_keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoRelatedKeywordsInput],
    ) -> RunResult[SeoRelatedKeywordsData]:
        """SEO Related Keywords

        Find AnyAPI SEO related keywords from a seed term with volume, CPC,
        competition, difficulty, and intent as normalized JSON.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.related_keywords(keyword="project management software", language="en", limit=5, location=2840)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.related_keywords", dict(input), options
        )
        return RunResult[SeoRelatedKeywordsData].model_validate(raw)

    def search_intent(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoSearchIntentInput],
    ) -> RunResult[SeoSearchIntentData]:
        """SEO Search Intent

        Classify AnyAPI SEO keyword search intent as normalized JSON.

        Price: $0.01438 per request plus $0.00016 per keyword (maximum $0.17438).

        Example:
            res = client.seo.search_intent(keywords=["seo tools"], language="en")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.search_intent", dict(input), options
        )
        return RunResult[SeoSearchIntentData].model_validate(raw)

    def search_volume(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoSearchVolumeInput],
    ) -> RunResult[SeoSearchVolumeData]:
        """SEO Search Volume

        Get AnyAPI SEO keyword search volume, CPC, competition, bid estimates, and
        monthly history as normalized JSON.

        Price: $0.108 per request plus $0 per result (maximum $0.108).

        Example:
            res = client.seo.search_volume(keywords=["seo tools"], language="en", location=2840)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.search_volume", dict(input), options
        )
        return RunResult[SeoSearchVolumeData].model_validate(raw)

    def top_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoTopPagesInput],
    ) -> RunResult[SeoTopPagesData]:
        """SEO Top Pages

        Get AnyAPI SEO top pages of a domain by organic search, each with ranking
        keyword counts, estimated traffic and its ad value, and position
        distribution as normalized JSON.

        Price: $0.0144 per request plus $0.00015 per result (maximum $0.1584).

        Example:
            res = client.seo.top_pages(limit=10, target="ahrefs.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.top_pages", dict(input), options
        )
        return RunResult[SeoTopPagesData].model_validate(raw)


class AsyncSeoNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def backlink_anchors(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinkAnchorsInput],
    ) -> RunResult[SeoBacklinkAnchorsData]:
        """SEO Backlink Anchors

        Get AnyAPI SEO anchor texts of the backlinks pointing at a domain or URL,
        each with backlink and referring domain counts, authority rank, and spam
        score as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.backlink_anchors(limit=10, target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlink_anchors", dict(input), options
        )
        return RunResult[SeoBacklinkAnchorsData].model_validate(raw)

    async def backlink_competitors(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinkCompetitorsInput],
    ) -> RunResult[SeoBacklinkCompetitorsData]:
        """SEO Backlink Competitors

        Find the domains that share the most backlinks with a domain or URL, each
        with its authority rank and shared backlink count as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.backlink_competitors(limit=10, target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlink_competitors", dict(input), options
        )
        return RunResult[SeoBacklinkCompetitorsData].model_validate(raw)

    async def backlinks(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinksInput],
    ) -> RunResult[SeoBacklinksData]:
        """SEO Backlinks

        Get AnyAPI SEO backlinks for a domain or URL, each with the linking page,
        anchor text, dofollow flag, authority rank, spam score, and first and last
        seen dates as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.backlinks(limit=10, target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlinks", dict(input), options
        )
        return RunResult[SeoBacklinksData].model_validate(raw)

    async def backlinks_summary(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoBacklinksSummaryInput],
    ) -> RunResult[SeoBacklinksSummaryData]:
        """SEO Backlinks Summary

        Get AnyAPI SEO backlink profile totals for a domain or URL: backlinks,
        referring domains, authority rank, spam score, and broken links as
        normalized JSON.

        Price: $0.02885 per request plus $0 per result (maximum $0.02885).

        Example:
            res = client.seo.backlinks_summary(target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.backlinks_summary", dict(input), options
        )
        return RunResult[SeoBacklinksSummaryData].model_validate(raw)

    async def competitors_domain(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoCompetitorsDomainInput],
    ) -> RunResult[SeoCompetitorsDomainData]:
        """SEO Competitor Domains

        Get AnyAPI SEO competitor domains for a target domain with shared keyword
        counts and organic metrics as normalized JSON.

        Price: $0.02864 per request plus $0.00016 per result (maximum $0.18864).

        Example:
            res = client.seo.competitors_domain(language="en", limit=10, location=2840, target="github.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.competitors_domain", dict(input), options
        )
        return RunResult[SeoCompetitorsDomainData].model_validate(raw)

    async def domain_intersection(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainIntersectionInput],
    ) -> RunResult[SeoDomainIntersectionData]:
        """SEO Domain Intersection

        Get AnyAPI SEO keyword overlap for two domains with each domain's rankings,
        URLs, volume, CPC, and difficulty as normalized JSON.

        Price: $0.02864 per request plus $0.00016 per result (maximum $0.18864).

        Example:
            res = client.seo.domain_intersection(language="en", limit=10, location=2840, target1="github.com", target2="gitlab.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_intersection", dict(input), options
        )
        return RunResult[SeoDomainIntersectionData].model_validate(raw)

    async def domain_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainPagesInput],
    ) -> RunResult[SeoDomainPagesData]:
        """SEO Domain Pages

        Get AnyAPI SEO pages of a domain with their backlink profile (rank,
        backlinks, referring domains) and on-page data (title, headings, word count,
        status, technologies) as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.domain_pages(limit=10, target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_pages", dict(input), options
        )
        return RunResult[SeoDomainPagesData].model_validate(raw)

    async def domain_rank_overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainRankOverviewInput],
    ) -> RunResult[SeoDomainRankOverviewData]:
        """SEO Domain Rank Overview

        Get AnyAPI SEO domain ranking, organic traffic, and paid traffic metrics as
        normalized JSON.

        Price: $0.01455 per request plus $0 per result (maximum $0.01455).

        Example:
            res = client.seo.domain_rank_overview(language="en", location=2840, target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_rank_overview", dict(input), options
        )
        return RunResult[SeoDomainRankOverviewData].model_validate(raw)

    async def domain_technologies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainTechnologiesInput],
    ) -> RunResult[SeoDomainTechnologiesData]:
        """SEO Domain Technologies

        Detect the technology stack a website runs: CMS, analytics, marketing,
        hosting, and security, plus contacts and social profiles as normalized JSON.

        Price: $0.0144 per request.

        Example:
            res = client.seo.domain_technologies(domain="hubspot.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domain_technologies", dict(input), options
        )
        return RunResult[SeoDomainTechnologiesData].model_validate(raw)

    async def domains_by_technology(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainsByTechnologyInput],
    ) -> RunResult[SeoDomainsByTechnologyData]:
        """SEO Domains By Technology

        Find websites running a given technology, category, or on-page term: domain,
        rank, detected stack, contacts, and social profiles as normalized JSON.

        Price: $0.01464 per request plus $0.0012 per result (maximum $0.13464).

        Example:
            res = client.seo.domains_by_technology(keyword="highlevel", limit=10, orderBy="rank_desc")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.domains_by_technology", dict(input), options
        )
        return RunResult[SeoDomainsByTechnologyData].model_validate(raw)

    def iter_domains_by_technology(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoDomainsByTechnologyInput],
    ) -> AsyncPaginator[SeoDomainsByTechnologyDomain, SeoDomainsByTechnologyData]:
        """Iterate SEO Domains By Technology results, following pagination cursors.

        Yields validated `SeoDomainsByTechnologyDomain` items from the `domains` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "seo.domains_by_technology",
            dict(input),
            "domains",
            item_model=SeoDomainsByTechnologyDomain,
            data_model=SeoDomainsByTechnologyData,
            bare=False,
            options=options,
        )

    async def keyword_difficulty(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordDifficultyInput],
    ) -> RunResult[SeoKeywordDifficultyData]:
        """SEO Keyword Difficulty

        Get AnyAPI SEO keyword difficulty scores for one or more keywords as
        normalized JSON.

        Price: $0.01438 per request plus $0.00016 per keyword (maximum $0.17438).

        Example:
            res = client.seo.keyword_difficulty(keywords=["seo tools"], language="en", location=2840)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_difficulty", dict(input), options
        )
        return RunResult[SeoKeywordDifficultyData].model_validate(raw)

    async def keyword_ideas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordIdeasInput],
    ) -> RunResult[SeoKeywordIdeasData]:
        """SEO Keyword Ideas

        Find AnyAPI SEO keyword ideas from seed terms with volume, CPC, competition,
        difficulty, and intent as normalized JSON.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.keyword_ideas(keywords=["project management software"], language="en", limit=5, location=2840)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_ideas", dict(input), options
        )
        return RunResult[SeoKeywordIdeasData].model_validate(raw)

    async def keyword_overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordOverviewInput],
    ) -> RunResult[SeoKeywordOverviewData]:
        """SEO Keyword Overview

        Get AnyAPI SEO keyword metrics including search volume, CPC, competition,
        difficulty, and search intent as normalized JSON.

        Price: $0.01438 per request plus $0.00016 per keyword (maximum $0.12638).

        Example:
            res = client.seo.keyword_overview(keywords=["project management software"], language="en", location=2840)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_overview", dict(input), options
        )
        return RunResult[SeoKeywordOverviewData].model_validate(raw)

    async def keyword_suggestions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoKeywordSuggestionsInput],
    ) -> RunResult[SeoKeywordSuggestionsData]:
        """SEO Keyword Suggestions

        Find AnyAPI SEO keyword suggestions from a seed term with volume, CPC,
        competition, difficulty, and intent as normalized JSON.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.keyword_suggestions(keyword="project management software", language="en", limit=5, location=2840)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.keyword_suggestions", dict(input), options
        )
        return RunResult[SeoKeywordSuggestionsData].model_validate(raw)

    async def llm_mentions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmMentionsInput],
    ) -> RunResult[SeoLlmMentionsData]:
        """SEO LLM Mentions

        Find AI answers that mention a domain or keyword, from Google AI Overviews
        or ChatGPT, each with the question asked, the answer, its cited sources, and
        AI search volume as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_mentions(domain="ahrefs.com", limit=5, platform="google")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_mentions", dict(input), options
        )
        return RunResult[SeoLlmMentionsData].model_validate(raw)

    async def llm_top_brands(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmTopBrandsInput],
    ) -> RunResult[SeoLlmTopBrandsData]:
        """SEO LLM Top Brands

        Rank the brands ChatGPT names most often in answers about a keyword or
        domain, each with mention count, AI search volume, and the sources and
        categories behind them as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_top_brands(keyword="seo tools", limit=5)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_top_brands", dict(input), options
        )
        return RunResult[SeoLlmTopBrandsData].model_validate(raw)

    async def llm_top_domains(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmTopDomainsInput],
    ) -> RunResult[SeoLlmTopDomainsData]:
        """SEO LLM Top Domains

        Rank the domains Google AI Overviews and ChatGPT cite most often in answers
        about a keyword or domain, each with mention count, AI search volume, and
        breakdowns by platform, location, and co-cited sources as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_top_domains(keyword="seo tools", limit=5)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_top_domains", dict(input), options
        )
        return RunResult[SeoLlmTopDomainsData].model_validate(raw)

    async def llm_top_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLlmTopPagesInput],
    ) -> RunResult[SeoLlmTopPagesData]:
        """SEO LLM Top Pages

        Rank the pages Google AI Overviews and ChatGPT cite most often in answers
        about a keyword or domain, each with mention count, AI search volume, and
        breakdowns by platform, location, and co-cited sources as normalized JSON.

        Price: $0.12 per request plus $0.0012 per result (maximum $1.32).

        Example:
            res = client.seo.llm_top_pages(keyword="seo tools", limit=5)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.llm_top_pages", dict(input), options
        )
        return RunResult[SeoLlmTopPagesData].model_validate(raw)

    async def local_pack(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoLocalPackInput],
    ) -> RunResult[SeoLocalPackData]:
        """Google Local Pack

        Get the Google local pack for a keyword in a city: the short list of
        businesses Google shows in the map box on its normal search results page, in
        pack order, with rating, review count, address, category, opening hours,
        phone, website, booking link, and Google listing ids. Sponsored listings are
        left out. For the full Google Maps results list, use maps.search.

        Price: $0.0015 per request.

        Example:
            res = client.seo.local_pack(keyword="coffee shop", language="en", location="New York,New York,United States")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.local_pack", dict(input), options
        )
        return RunResult[SeoLocalPackData].model_validate(raw)

    async def ranked_keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoRankedKeywordsInput],
    ) -> RunResult[SeoRankedKeywordsData]:
        """SEO Ranked Keywords

        Get AnyAPI SEO ranked keywords for a domain with rankings, traffic
        estimates, volume, CPC, difficulty, and intent as normalized JSON. One call
        returns up to 1,000 keywords; use offset to page further.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.ranked_keywords(language="en", limit=10, location=2840, target="github.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.ranked_keywords", dict(input), options
        )
        return RunResult[SeoRankedKeywordsData].model_validate(raw)

    async def referring_domains(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoReferringDomainsInput],
    ) -> RunResult[SeoReferringDomainsData]:
        """SEO Referring Domains

        Get AnyAPI SEO referring domains for a domain or URL, each with its backlink
        count, authority rank, spam score, and first seen date as normalized JSON.

        Price: $0.0288 per request plus $0.00005 per result (maximum $0.0768).

        Example:
            res = client.seo.referring_domains(limit=10, target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.referring_domains", dict(input), options
        )
        return RunResult[SeoReferringDomainsData].model_validate(raw)

    async def related_keywords(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoRelatedKeywordsInput],
    ) -> RunResult[SeoRelatedKeywordsData]:
        """SEO Related Keywords

        Find AnyAPI SEO related keywords from a seed term with volume, CPC,
        competition, difficulty, and intent as normalized JSON.

        Price: $0.01496 per request plus $0.00016 per result (maximum $0.17496).

        Example:
            res = client.seo.related_keywords(keyword="project management software", language="en", limit=5, location=2840)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.related_keywords", dict(input), options
        )
        return RunResult[SeoRelatedKeywordsData].model_validate(raw)

    async def search_intent(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoSearchIntentInput],
    ) -> RunResult[SeoSearchIntentData]:
        """SEO Search Intent

        Classify AnyAPI SEO keyword search intent as normalized JSON.

        Price: $0.01438 per request plus $0.00016 per keyword (maximum $0.17438).

        Example:
            res = client.seo.search_intent(keywords=["seo tools"], language="en")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.search_intent", dict(input), options
        )
        return RunResult[SeoSearchIntentData].model_validate(raw)

    async def search_volume(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoSearchVolumeInput],
    ) -> RunResult[SeoSearchVolumeData]:
        """SEO Search Volume

        Get AnyAPI SEO keyword search volume, CPC, competition, bid estimates, and
        monthly history as normalized JSON.

        Price: $0.108 per request plus $0 per result (maximum $0.108).

        Example:
            res = client.seo.search_volume(keywords=["seo tools"], language="en", location=2840)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.search_volume", dict(input), options
        )
        return RunResult[SeoSearchVolumeData].model_validate(raw)

    async def top_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SeoTopPagesInput],
    ) -> RunResult[SeoTopPagesData]:
        """SEO Top Pages

        Get AnyAPI SEO top pages of a domain by organic search, each with ranking
        keyword counts, estimated traffic and its ad value, and position
        distribution as normalized JSON.

        Price: $0.0144 per request plus $0.00015 per result (maximum $0.1584).

        Example:
            res = client.seo.top_pages(limit=10, target="ahrefs.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "seo.top_pages", dict(input), options
        )
        return RunResult[SeoTopPagesData].model_validate(raw)
