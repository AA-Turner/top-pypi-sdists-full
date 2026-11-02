# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the linkedin platform."""

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


class LinkedinAdInput(TypedDict, total=False):
    """Input for LinkedIn Ad Details."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """LinkedIn Ad Library ad URL (e.g. "https://www.linkedin.com/ad-library/detail/666281156")."""


class LinkedinAdsInput(TypedDict, total=False):
    """Input for LinkedIn Ads Library."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). You are billed per result returned, so a lower limit costs less. Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """LinkedIn Ad Library search URL or a LinkedIn company URL (e.g. https://www.linkedin.com/ad-library/search?companyIds=1035)."""


class LinkedinAdsSearchInput(TypedDict, total=False):
    """Input for LinkedIn Ad Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    company: NotRequired[str]
    """Company name to search (e.g. "microsoft")."""
    companyId: NotRequired[str]
    """LinkedIn company identifier."""
    countries: NotRequired[str]
    """Comma-separated two-letter country codes (e.g. "US,CA,MX")."""
    endDate: NotRequired[str]
    """Search end date in YYYY-MM-DD format. Today or a later date is moved back to yesterday in UTC when your range overlaps LinkedIn's accepted dates. When you send startDate without endDate, the search ends yesterday in UTC, the latest day LinkedIn accepts."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keyword: NotRequired[str]
    """Keyword term for the ad search."""
    paginationToken: NotRequired[str]
    """Opaque pagination token from a previous response's nextCursor."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Search start date in YYYY-MM-DD format. An earlier date is moved up to one year ago in UTC when your range overlaps LinkedIn's accepted dates."""


class LinkedinArticleInput(TypedDict, total=False):
    """Input for LinkedIn Article."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Public LinkedIn article or newsletter issue URL, e.g. https://www.linkedin.com/pulse/your-article-slug. Pair it with the attachmentUrl returned by linkedin.search_posts_full to read the article behind a post."""


class LinkedinCommentReactionsInput(TypedDict, total=False):
    """Input for LinkedIn Comment Reactions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """Which page of up to 100 reactions to return, starting at 1 (default 1). Each page is billed as one request; totalPages in the response says how many there are. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """LinkedIn comment URL, as returned in the url field of linkedin.post_comments or copied with "Copy link to comment" (a /feed/update/... link carrying commentUrn and dashCommentUrn). A post URL without dashCommentUrn, or a reply's URL (carrying replyUrn), is refused as invalid input, with no charge."""


class LinkedinCommentRepliesInput(TypedDict, total=False):
    """Input for LinkedIn Comment Replies."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """LinkedIn comment URL, as returned in the url field of linkedin.post_comments or copied with "Copy link to comment" (a /feed/update/... link carrying commentUrn and dashCommentUrn). A reply's URL returns the thread it belongs to. A post URL without dashCommentUrn is refused as invalid input, with no charge."""


class LinkedinCompanyInput(TypedDict, total=False):
    """Input for LinkedIn Company."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "city",
                "companyType",
                "foundedOn",
                "fundingData",
                "line1",
                "pageVerified",
                "postalCode",
                "similarOrganizations",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `city` or `postalCode`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn company page URL."""


class LinkedinCompanyEmployeesInput(TypedDict, total=False):
    """Input for LinkedIn Company Employees."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    company: Required[str]
    """Company name or LinkedIn company URL (e.g. google or https://www.linkedin.com/company/google/)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    jobTitle: NotRequired[str]
    """Optional job-title filter supporting boolean operators (e.g. CEO OR CTO)."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-10, default 10). Range: 1 to 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "companyId",
                "companyUrl",
                "countryCode",
                "createdUtc",
                "creator",
                "firstName",
                "influencer",
                "lastName",
                "openToWork",
                "premium",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `openToWork` or `premium`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an employee who genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LinkedinCompanyPostsInput(TypedDict, total=False):
    """Input for LinkedIn Company Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeQuotePosts: NotRequired[bool]
    """Include quote posts (posts shared with an added comment). Defaults to true; set false to exclude them."""
    includeReposts: NotRequired[bool]
    """Include reposts (posts shared without an added comment). Defaults to true; set false to exclude them."""
    limit: NotRequired[int]
    """Maximum number of posts to return. Range: 1 to 50. Default: 10."""
    postedLimit: NotRequired[
        Literal["any", "1h", "24h", "week", "month", "3months", "6months", "year"]
    ]
    """Only return posts published within this window (default any)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn company page URL."""


class LinkedinCompanyPostsThinInput(TypedDict, total=False):
    """Input for LinkedIn Company Posts (basic)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """Page number for pagination. Minimum: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn company page URL."""


class LinkedinCompanyThinInput(TypedDict, total=False):
    """Input for LinkedIn Company (basic)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["companyType", "coverImage"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `companyType` or `coverImage`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a company page that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn company page URL."""


class LinkedinEmailInput(TypedDict, total=False):
    """Input for LinkedIn Email Finder."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileUrl: Required[str]
    """LinkedIn profile URL or public identifier (the last part of the URL) to find the deliverability-validated work email for."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LinkedinGroupInput(TypedDict, total=False):
    """Input for LinkedIn Group."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    groupId: NotRequired[str]
    """Numeric LinkedIn group id (e.g. 1898033), the number in the group URL. Send this or url."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """LinkedIn group URL (e.g. https://www.linkedin.com/groups/1898033). Send this or groupId."""


class LinkedinGroupPostsInput(TypedDict, total=False):
    """Input for LinkedIn Group Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """Which page of about 100 posts to return, starting at 1 (default 1). Page 2 continues where page 1 ended, going further back in time. Each page is billed as one request. Minimum: 1. Default: 1."""
    postedLimit: NotRequired[
        Literal["any", "1h", "24h", "week", "month", "3months", "6months", "year"]
    ]
    """Only return posts published within this window (default any). The window is applied to the page, so a page can come back with fewer posts or none."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn group URL (e.g. https://www.linkedin.com/groups/1898033)."""


class LinkedinJobInput(TypedDict, total=False):
    """Input for LinkedIn Job."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn job posting URL, e.g. https://www.linkedin.com/jobs/view/4431721875/."""


class LinkedinJobsInput(TypedDict, total=False):
    """Input for LinkedIn Jobs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    company: NotRequired[str]
    """Filter to a specific company by name (e.g. Google)."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of job listings."""
    easyApply: NotRequired[bool]
    """When true, only return jobs offering LinkedIn Easy Apply."""
    employmentType: NotRequired[
        Literal["full-time", "part-time", "contract", "internship", "temporary"]
    ]
    """Filter by employment type."""
    experienceLevel: NotRequired[
        Literal[
            "internship", "entry", "associate", "mid-senior", "director", "executive"
        ]
    ]
    """Filter by required seniority/experience level."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Accepted for compatibility and ignored: each call returns one full page of up to 25 jobs at one flat price per call; follow nextCursor for more. Range: 1 to 25."""
    location: NotRequired[str]
    """City, region, or country to search within (e.g. United States, San Francisco)."""
    postedLimit: NotRequired[Literal["1h", "24h", "week", "month"]]
    """Only jobs posted within this window (past hour, 24 hours, week, or month)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Job title or keywords to search. Supports LinkedIn boolean operators."""
    salary: NotRequired[
        Literal[
            "40k+", "60k+", "80k+", "100k+", "120k+", "140k+", "160k+", "180k+", "200k+"
        ]
    ]
    """Filter by minimum base salary band (US dollars)."""
    sortBy: NotRequired[Literal["date", "relevance"]]
    """Sort order: most recent (date) or best match (relevance)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    under10Applicants: NotRequired[bool]
    """When true, only return jobs with fewer than 10 applicants (lower competition)."""
    workplaceType: NotRequired[Literal["remote", "hybrid", "onsite"]]
    """Filter by workplace type (remote, hybrid, or onsite)."""


class LinkedinJobsThinInput(TypedDict, total=False):
    """Input for LinkedIn Jobs (index)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyId: NotRequired[str]
    """Filter to a specific company by its LinkedIn numeric company id."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of job listings."""
    employmentType: NotRequired[
        Literal["full-time", "part-time", "contract", "internship", "temporary"]
    ]
    """Filter by employment type."""
    experienceLevel: NotRequired[
        Literal[
            "internship", "entry", "associate", "mid-senior", "director", "executive"
        ]
    ]
    """Filter by required seniority/experience level."""
    geoId: NotRequired[str]
    """LinkedIn geo id to target a precise location (e.g. 103644278 for the United States); more exact than the free-text location."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Accepted for compatibility and ignored: each call returns one full source page (10 or 25 jobs depending on source); follow nextCursor for more. Range: 1 to 25."""
    location: NotRequired[str]
    """City, region, or country to search within."""
    postedLimit: NotRequired[Literal["24h", "week", "month"]]
    """Only jobs posted within this window (past 24 hours, week, or month)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Job title or keywords to search."""
    requireFields: NotRequired[list[Literal["logoUrl"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `logoUrl`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a listing that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    workplaceType: NotRequired[Literal["remote", "hybrid", "onsite"]]
    """Filter by workplace type (remote, hybrid, or onsite)."""


class LinkedinPostInput(TypedDict, total=False):
    """Input for LinkedIn Post."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["authorImage", "image"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `image`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn post or article URL."""


class LinkedinPostCommentsInput(TypedDict, total=False):
    """Input for LinkedIn Post Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of comments to return. Range: 1 to 100. Default: 100."""
    postedLimit: NotRequired[
        Literal["any", "24h", "week", "month", "3months", "6months", "year"]
    ]
    """Only return comments posted within this window (default any)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full URL of the LinkedIn post to list comments for."""


class LinkedinPostReactionsInput(TypedDict, total=False):
    """Input for LinkedIn Post Reactions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of reactions to return (1-100, default 100). Range: 1 to 100."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["postId"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `postId`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """URL of the LinkedIn post to list reactions for (a /posts/...-activity-... or /feed/update/urn:li:activity:... link)."""


class LinkedinPostTranscriptInput(TypedDict, total=False):
    """Input for LinkedIn Post Transcript."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The full URL of the LinkedIn post to get the video transcript from."""


class LinkedinProfileInput(TypedDict, total=False):
    """Input for LinkedIn Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "endorsements", "positions", "schoolId", "topSkills", "workplaceType"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `topSkills` or `workplaceType`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn profile URL."""


class LinkedinProfileCommentsInput(TypedDict, total=False):
    """Input for LinkedIn Profile Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of comments to return. Range: 1 to 100. Default: 100."""
    postedLimit: NotRequired[Literal["any", "24h", "week", "month"]]
    """Only return comments posted within this window (default any)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["edited", "isAuthor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `edited` or `isAuthor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a comment that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full URL of the LinkedIn member profile whose comments on other people's posts should be listed."""


class LinkedinProfilePostsFullInput(TypedDict, total=False):
    """Input for LinkedIn Profile Posts (full)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    contextCountry: NotRequired[Literal["any", "US", "GB", "DE", "FR"]]
    """Regional LinkedIn context used when retrieving posts."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeQuotePosts: NotRequired[bool]
    """Whether to include quote posts that add commentary to shared content. Default: true."""
    includeReposts: NotRequired[bool]
    """Whether to include reposts that share content without added commentary. Default: true."""
    limit: NotRequired[int]
    """Most posts to return (1-100, default 10). Ignored on sources that page: each call returns one full page of 50 posts; follow nextCursor for more. Sources that cannot page return up to `limit` posts in one call with no nextCursor. Range: 1 to 100. Default: 10."""
    postedLimit: NotRequired[
        Literal["any", "1h", "24h", "week", "month", "3months", "6months", "year"]
    ]
    """Only return posts published within this relative time window."""
    postedLimitDate: NotRequired[str]
    """Only return posts published on or after this date or timestamp, using a JavaScript-compatible date-time string."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["nextCursor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full URL of the public LinkedIn profile whose posts should be returned."""


class LinkedinProfilePostsThinInput(TypedDict, total=False):
    """Input for LinkedIn Profile Posts (basic)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Most posts to return (10-100, default 10). Ignored on sources that page: each call returns one full page of 50 posts; follow nextCursor for more. Sources that cannot page return up to `limit` posts in one call with no nextCursor. Range: 10 to 100. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["nextCursor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full URL of the public LinkedIn profile whose posts should be returned."""


class LinkedinProfileReactionsInput(TypedDict, total=False):
    """Input for LinkedIn Profile Reactions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of reactions to return. One upstream page holds 100. Range: 1 to 100. Default: 100."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full URL of the LinkedIn member profile whose reactions to list, for example https://www.linkedin.com/in/williamhgates."""


class LinkedinProfileThinInput(TypedDict, total=False):
    """Input for LinkedIn Profile (basic)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "activityType",
                "articles",
                "companyLinkedinUrl",
                "companyName",
                "connections",
                "createdUtc",
                "current",
                "currentPosition",
                "headline",
                "id",
                "position",
                "publicIdentifier",
                "recentPosts",
                "text",
                "url",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `headline` or `recentPosts`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full LinkedIn person profile URL, carrying the profile id after /in/, for example https://www.linkedin.com/in/williamhgates. Any other LinkedIn URL names no person, so it is rejected instead of charged: send a company page to linkedin.company_thin or linkedin.company, and a post to linkedin.post."""


class LinkedinSearchCompaniesInput(TypedDict, total=False):
    """Input for LinkedIn Company Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). Range: 1 to 20. Default: 20."""
    location: NotRequired[str]
    """Optional location filter, written out in full (e.g. United Kingdom or San Francisco)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search LinkedIn companies for (e.g. marketing agency)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LinkedinSearchGroupsInput(TypedDict, total=False):
    """Input for LinkedIn Group Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """Which page of up to 10 groups to return, starting at 1 (1-100, default 1). Each page is billed as one request. Range: 1 to 100. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search LinkedIn groups for (e.g. python or sales)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LinkedinSearchLeadsInput(TypedDict, total=False):
    """Input for LinkedIn Sales Navigator Lead Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyHeadcount: NotRequired[
        list[Literal["A", "B", "C", "D", "E", "F", "G", "H", "I"]]
    ]
    """Filter by current company size (employee count). Codes: A=Self-Employed, B=1-10, C=11-50, D=51-200, E=201-500, F=501-1,000, G=1,001-5,000, H=5,001-10,000, I=10,001+."""
    companyHeadquarterLocations: NotRequired[list[str]]
    """Filter by the location of the person's current company headquarters, by place name (e.g. ['United States']). Commas are not allowed in a value. Up to 70 values."""
    currentCompanies: NotRequired[list[str]]
    """Filter to people who currently work at any of these companies, by name (e.g. ['Google','Meta']). Multiple names widen the match (OR). Commas are not allowed in a value. Up to 50 values."""
    excludeCompanyHeadquarterLocations: NotRequired[list[str]]
    """Exclude people whose current company is headquartered in any of these locations. Commas are not allowed in a value. Up to 70 values."""
    excludeCurrentCompanies: NotRequired[list[str]]
    """Exclude people who currently work at any of these companies, by name. Commas are not allowed in a value. Up to 50 values."""
    excludeCurrentJobTitles: NotRequired[list[str]]
    """Exclude people whose current job title matches any of these. Commas are not allowed in a value. Up to 70 values."""
    excludeFunctionIds: NotRequired[
        list[
            Literal[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            ]
        ]
    ]
    """Exclude these job functions (same codes as functionIds). Up to 30 values."""
    excludeLocations: NotRequired[list[str]]
    """Exclude people in any of these locations, by place name. Commas are not allowed in a value. Up to 70 values."""
    excludePastCompanies: NotRequired[list[str]]
    """Exclude people who previously worked at any of these companies, by name. Commas are not allowed in a value. Up to 50 values."""
    excludePastJobTitles: NotRequired[list[str]]
    """Exclude people who held any of these past job titles. Commas are not allowed in a value. Up to 70 values."""
    excludeSchools: NotRequired[list[str]]
    """Exclude people who attended any of these schools, by name. Commas are not allowed in a value. Up to 50 values."""
    excludeSeniorityLevelIds: NotRequired[
        list[
            Literal[
                "100", "110", "120", "130", "200", "210", "220", "300", "310", "320"
            ]
        ]
    ]
    """Exclude these seniority levels (same codes as seniorityLevelIds). Up to 20 values."""
    firstNames: NotRequired[list[str]]
    """Filter to people whose first name matches any of these. Commas are not allowed in a value. Up to 70 values."""
    functionIds: NotRequired[
        list[
            Literal[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            ]
        ]
    ]
    """Filter by job function. Codes: 1=Accounting, 2=Administrative, 3=Arts and Design, 4=Business Development, 5=Community and Social Services, 6=Consulting, 7=Education, 8=Engineering, 9=Entrepreneurship, 10=Finance, 11=Healthcare Services, 12=Human Resources, 13=Information Technology, 14=Legal, 15=Marketing, 16=Media and Communication, 17=Military and Protective Services, 18=Operations, 19=Product Management, 20=Program and Project Management, 21=Purchasing, 22=Quality Assurance, 23=Real Estate, 24=Research, 25=Sales, 26=Customer Success and Support."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    jobTitle: NotRequired[str]
    """Optional current job title filter (e.g. 'Software Engineer'). Commas are not allowed in a value."""
    lastNames: NotRequired[list[str]]
    """Filter to people whose last name matches any of these. Commas are not allowed in a value. Up to 70 values."""
    location: NotRequired[str]
    """Optional location filter (e.g. 'San Francisco'). Commas are not allowed in a value."""
    page: NotRequired[int]
    """Which page of up to 25 leads to return, starting at 1 (1-100, default 1). Also pages through a salesNavUrl search. Each page is billed as one request. Range: 1 to 100. Default: 1."""
    pastCompanies: NotRequired[list[str]]
    """Filter to people who previously worked at any of these companies, by name. Commas are not allowed in a value. Up to 50 values."""
    pastJobTitles: NotRequired[list[str]]
    """Filter by a past job title the person held (e.g. ['Product Manager']). Commas are not allowed in a value. Up to 70 values."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileLanguages: NotRequired[
        list[
            Literal[
                "Arabic",
                "English",
                "Spanish",
                "Portuguese",
                "Chinese",
                "French",
                "Italian",
                "Russian",
                "German",
                "Dutch",
                "Turkish",
                "Tagalog",
                "Polish",
                "Korean",
                "Japanese",
                "Malay",
                "Norwegian",
                "Danish",
                "Romanian",
                "Swedish",
                "Bahasa Indonesia",
                "Czech",
            ]
        ]
    ]
    """Filter by the profile's primary language."""
    query: NotRequired[str]
    """Search keywords for LinkedIn leads: a role, name, or keywords (e.g. 'Marketing Manager'). Provide this or salesNavUrl."""
    recentlyChangedJobs: NotRequired[bool]
    """When true, only return people who recently changed jobs (a strong sales/recruiting signal)."""
    recentlyPostedOnLinkedIn: NotRequired[bool]
    """When true, only return people who recently posted on LinkedIn (an activity signal)."""
    salesNavUrl: NotRequired[str]
    """Alternatively, a LinkedIn Sales Navigator lead-search URL you built in Sales Navigator (e.g. https://www.linkedin.com/sales/search/people?query=(keywords%3Aengineer)). When set it overrides query and every other filter on this request; only page still applies."""
    schools: NotRequired[list[str]]
    """Filter to people who attended any of these schools, by name. Commas are not allowed in a value. Up to 50 values."""
    seniorityLevelIds: NotRequired[
        list[
            Literal[
                "100", "110", "120", "130", "200", "210", "220", "300", "310", "320"
            ]
        ]
    ]
    """Filter by seniority level. Codes: 100=In Training, 110=Entry Level, 120=Senior, 130=Strategic, 200=Entry Level Manager, 210=Experienced Manager, 220=Director, 300=Vice President, 310=CXO, 320=Owner/Partner."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    yearsAtCurrentCompanyIds: NotRequired[list[Literal["1", "2", "3", "4", "5"]]]
    """Filter by tenure at the current company. Codes: 1=Less than 1 year, 2=1 to 2 years, 3=3 to 5 years, 4=6 to 10 years, 5=More than 10 years."""
    yearsOfExperienceIds: NotRequired[list[Literal["1", "2", "3", "4", "5"]]]
    """Filter by total years of experience. Codes: 1=Less than 1 year, 2=1 to 2 years, 3=3 to 5 years, 4=6 to 10 years, 5=More than 10 years."""


class LinkedinSearchPostsInput(TypedDict, total=False):
    """Input for LinkedIn Post Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    datePosted: NotRequired[
        Literal["last-hour", "last-day", "last-week", "last-month", "last-year"]
    ]
    """Filter by recency. One of last-hour, last-day, last-week, last-month, last-year."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The post search query."""
    requireCursor: NotRequired[bool]
    """Deprecated. Every source for this search returns a nextCursor, so this changes nothing about the price or which source serves you; it stays accepted so callers that already send it keep working."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LinkedinSearchPostsFullInput(TypedDict, total=False):
    """Input for LinkedIn Post Search (full)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    authorCompanyNames: NotRequired[list[str]]
    """Only return posts by people associated with these company names."""
    authorIndustryIds: NotRequired[list[str]]
    """Only return posts by authors associated with these LinkedIn industry IDs."""
    authorKeywords: NotRequired[str]
    """Only return posts whose author profile headline or job title contains at least one of these keywords."""
    authorUrls: NotRequired[list[str]]
    """Only return posts authored by these LinkedIn profile or company URLs."""
    contentType: NotRequired[
        Literal[
            "all",
            "videos",
            "images",
            "jobs",
            "live-videos",
            "documents",
            "collaborative-articles",
        ]
    ]
    """Only return posts carrying this content type."""
    datePosted: NotRequired[
        Literal[
            "last-hour",
            "last-day",
            "last-week",
            "last-month",
            "last-three-months",
            "last-six-months",
            "last-year",
        ]
    ]
    """Only return posts published within this relative time window. Last-hour and windows beyond one month route to the provider that supports them. Default: last-day."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of posts to return (1-100, default 10). The upper bound is one LinkedIn search page. Range: 1 to 100. Default: 10."""
    mentioningMemberUrls: NotRequired[list[str]]
    """Only return posts mentioning these LinkedIn member profile URLs."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """LinkedIn post search query, including quoted terms or Boolean operators accepted by LinkedIn search."""
    requireFields: NotRequired[
        list[
            Literal[
                "attachmentDescription",
                "attachmentImage",
                "attachmentSubtitle",
                "attachmentTitle",
                "attachmentType",
                "attachmentUrl",
                "pollClosed",
                "pollOptions",
                "pollQuestion",
                "pollTotalVotes",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `attachmentType` or `pollOptions`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sort: NotRequired[Literal["relevance", "date"]]
    """Order results by search relevance or publication date. Default: relevance."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LinkedinSearchProfilesInput(TypedDict, total=False):
    """Input for LinkedIn Profile Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyHeadcount: NotRequired[
        list[Literal["A", "B", "C", "D", "E", "F", "G", "H", "I"]]
    ]
    """Filter by current company size (employee count). Codes: A=Self-Employed, B=1-10, C=11-50, D=51-200, E=201-500, F=501-1,000, G=1,001-5,000, H=5,001-10,000, I=10,001+."""
    companyHeadquarterLocations: NotRequired[list[str]]
    """Filter by the location of the person's current company headquarters, by place name (e.g. ['United States'])."""
    currentCompanies: NotRequired[list[str]]
    """Filter to people who currently work at any of these companies, by name (e.g. ['Google','Meta']). Multiple names widen the match (OR)."""
    excludeCompanyHeadquarterLocations: NotRequired[list[str]]
    """Exclude people whose current company is headquartered in any of these locations."""
    excludeCurrentCompanies: NotRequired[list[str]]
    """Exclude people who currently work at any of these companies, by name."""
    excludeCurrentJobTitles: NotRequired[list[str]]
    """Exclude people whose current job title matches any of these."""
    excludeFunctionIds: NotRequired[
        list[
            Literal[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            ]
        ]
    ]
    """Exclude these job functions (same codes as functionIds)."""
    excludeLocations: NotRequired[list[str]]
    """Exclude people in any of these locations, by place name."""
    excludePastCompanies: NotRequired[list[str]]
    """Exclude people who previously worked at any of these companies, by name."""
    excludePastJobTitles: NotRequired[list[str]]
    """Exclude people who held any of these past job titles."""
    excludeSchools: NotRequired[list[str]]
    """Exclude people who attended any of these schools, by name."""
    excludeSeniorityLevelIds: NotRequired[
        list[
            Literal[
                "100", "110", "120", "130", "200", "210", "220", "300", "310", "320"
            ]
        ]
    ]
    """Exclude these seniority levels (same codes as seniorityLevelIds)."""
    firstNames: NotRequired[list[str]]
    """Filter to people whose first name matches any of these."""
    functionIds: NotRequired[
        list[
            Literal[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            ]
        ]
    ]
    """Filter by job function. Codes: 1=Accounting, 2=Administrative, 3=Arts and Design, 4=Business Development, 5=Community and Social Services, 6=Consulting, 7=Education, 8=Engineering, 9=Entrepreneurship, 10=Finance, 11=Healthcare Services, 12=Human Resources, 13=Information Technology, 14=Legal, 15=Marketing, 16=Media and Communication, 17=Military and Protective Services, 18=Operations, 19=Product Management, 20=Program and Project Management, 21=Purchasing, 22=Quality Assurance, 23=Real Estate, 24=Research, 25=Sales, 26=Customer Success and Support."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    jobTitle: NotRequired[str]
    """Optional current job title filter (e.g. 'Software Engineer')."""
    lastNames: NotRequired[list[str]]
    """Filter to people whose last name matches any of these."""
    limit: NotRequired[int]
    """Maximum number of full profiles to return (1-25, default 10). You are billed per profile returned, so a lower limit costs less. Range: 1 to 25."""
    location: NotRequired[str]
    """Optional location filter (e.g. 'San Francisco')."""
    pastCompanies: NotRequired[list[str]]
    """Filter to people who previously worked at any of these companies, by name."""
    pastJobTitles: NotRequired[list[str]]
    """Filter by a past job title the person held (e.g. ['Product Manager'])."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileLanguages: NotRequired[
        list[
            Literal[
                "Arabic",
                "English",
                "Spanish",
                "Portuguese",
                "Chinese",
                "French",
                "Italian",
                "Russian",
                "German",
                "Dutch",
                "Turkish",
                "Tagalog",
                "Polish",
                "Korean",
                "Japanese",
                "Malay",
                "Norwegian",
                "Danish",
                "Romanian",
                "Swedish",
                "Bahasa Indonesia",
                "Czech",
            ]
        ]
    ]
    """Filter by the profile's primary language."""
    query: Required[str]
    """Search query for LinkedIn profiles: a role, name, or keywords (e.g. 'Marketing Manager')."""
    recentlyChangedJobs: NotRequired[bool]
    """When true, only return people who recently changed jobs (a strong sales/recruiting signal)."""
    recentlyPostedOnLinkedIn: NotRequired[bool]
    """When true, only return people who recently posted on LinkedIn (an activity signal)."""
    schools: NotRequired[list[str]]
    """Filter to people who attended any of these schools, by name."""
    seniorityLevelIds: NotRequired[
        list[
            Literal[
                "100", "110", "120", "130", "200", "210", "220", "300", "310", "320"
            ]
        ]
    ]
    """Filter by seniority level. Codes: 100=In Training, 110=Entry Level, 120=Senior, 130=Strategic, 200=Entry Level Manager, 210=Experienced Manager, 220=Director, 300=Vice President, 310=CXO, 320=Owner/Partner."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    yearsAtCurrentCompanyIds: NotRequired[list[Literal["1", "2", "3", "4", "5"]]]
    """Filter by tenure at the current company. Codes: 1=Less than 1 year, 2=1 to 2 years, 3=3 to 5 years, 4=6 to 10 years, 5=More than 10 years."""
    yearsOfExperienceIds: NotRequired[list[Literal["1", "2", "3", "4", "5"]]]
    """Filter by total years of experience. Codes: 1=Less than 1 year, 2=1 to 2 years, 3=3 to 5 years, 4=6 to 10 years, 5=More than 10 years."""


class LinkedinSearchProfilesEmailInput(TypedDict, total=False):
    """Input for LinkedIn Profile Search + Email."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyHeadcount: NotRequired[
        list[Literal["A", "B", "C", "D", "E", "F", "G", "H", "I"]]
    ]
    """Filter by current company size (employee count). Codes: A=Self-Employed, B=1-10, C=11-50, D=51-200, E=201-500, F=501-1,000, G=1,001-5,000, H=5,001-10,000, I=10,001+."""
    companyHeadquarterLocations: NotRequired[list[str]]
    """Filter by the location of the person's current company headquarters, by place name (e.g. ['United States'])."""
    currentCompanies: NotRequired[list[str]]
    """Filter to people who currently work at any of these companies, by name (e.g. ['Google','Meta']). Multiple names widen the match (OR)."""
    excludeCompanyHeadquarterLocations: NotRequired[list[str]]
    """Exclude people whose current company is headquartered in any of these locations."""
    excludeCurrentCompanies: NotRequired[list[str]]
    """Exclude people who currently work at any of these companies, by name."""
    excludeCurrentJobTitles: NotRequired[list[str]]
    """Exclude people whose current job title matches any of these."""
    excludeFunctionIds: NotRequired[
        list[
            Literal[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            ]
        ]
    ]
    """Exclude these job functions (same codes as functionIds)."""
    excludeLocations: NotRequired[list[str]]
    """Exclude people in any of these locations, by place name."""
    excludePastCompanies: NotRequired[list[str]]
    """Exclude people who previously worked at any of these companies, by name."""
    excludePastJobTitles: NotRequired[list[str]]
    """Exclude people who held any of these past job titles."""
    excludeSchools: NotRequired[list[str]]
    """Exclude people who attended any of these schools, by name."""
    excludeSeniorityLevelIds: NotRequired[
        list[
            Literal[
                "100", "110", "120", "130", "200", "210", "220", "300", "310", "320"
            ]
        ]
    ]
    """Exclude these seniority levels (same codes as seniorityLevelIds)."""
    firstNames: NotRequired[list[str]]
    """Filter to people whose first name matches any of these."""
    functionIds: NotRequired[
        list[
            Literal[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            ]
        ]
    ]
    """Filter by job function. Codes: 1=Accounting, 2=Administrative, 3=Arts and Design, 4=Business Development, 5=Community and Social Services, 6=Consulting, 7=Education, 8=Engineering, 9=Entrepreneurship, 10=Finance, 11=Healthcare Services, 12=Human Resources, 13=Information Technology, 14=Legal, 15=Marketing, 16=Media and Communication, 17=Military and Protective Services, 18=Operations, 19=Product Management, 20=Program and Project Management, 21=Purchasing, 22=Quality Assurance, 23=Real Estate, 24=Research, 25=Sales, 26=Customer Success and Support."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    jobTitle: NotRequired[str]
    """Optional current job title filter (e.g. 'Software Engineer')."""
    lastNames: NotRequired[list[str]]
    """Filter to people whose last name matches any of these."""
    limit: NotRequired[int]
    """Maximum number of full profiles (with email) to return (1-25, default 10). You are billed per profile returned, so a lower limit costs less. Range: 1 to 25."""
    location: NotRequired[str]
    """Optional location filter (e.g. 'San Francisco')."""
    pastCompanies: NotRequired[list[str]]
    """Filter to people who previously worked at any of these companies, by name."""
    pastJobTitles: NotRequired[list[str]]
    """Filter by a past job title the person held (e.g. ['Product Manager'])."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileLanguages: NotRequired[
        list[
            Literal[
                "Arabic",
                "English",
                "Spanish",
                "Portuguese",
                "Chinese",
                "French",
                "Italian",
                "Russian",
                "German",
                "Dutch",
                "Turkish",
                "Tagalog",
                "Polish",
                "Korean",
                "Japanese",
                "Malay",
                "Norwegian",
                "Danish",
                "Romanian",
                "Swedish",
                "Bahasa Indonesia",
                "Czech",
            ]
        ]
    ]
    """Filter by the profile's primary language."""
    query: Required[str]
    """Search query for LinkedIn profiles: a role, name, or keywords (e.g. 'Marketing Manager')."""
    recentlyChangedJobs: NotRequired[bool]
    """When true, only return people who recently changed jobs (a strong sales/recruiting signal)."""
    recentlyPostedOnLinkedIn: NotRequired[bool]
    """When true, only return people who recently posted on LinkedIn (an activity signal)."""
    schools: NotRequired[list[str]]
    """Filter to people who attended any of these schools, by name."""
    seniorityLevelIds: NotRequired[
        list[
            Literal[
                "100", "110", "120", "130", "200", "210", "220", "300", "310", "320"
            ]
        ]
    ]
    """Filter by seniority level. Codes: 100=In Training, 110=Entry Level, 120=Senior, 130=Strategic, 200=Entry Level Manager, 210=Experienced Manager, 220=Director, 300=Vice President, 310=CXO, 320=Owner/Partner."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    yearsAtCurrentCompanyIds: NotRequired[list[Literal["1", "2", "3", "4", "5"]]]
    """Filter by tenure at the current company. Codes: 1=Less than 1 year, 2=1 to 2 years, 3=3 to 5 years, 4=6 to 10 years, 5=More than 10 years."""
    yearsOfExperienceIds: NotRequired[list[Literal["1", "2", "3", "4", "5"]]]
    """Filter by total years of experience. Codes: 1=Less than 1 year, 2=1 to 2 years, 3=3 to 5 years, 4=6 to 10 years, 5=More than 10 years."""


class LinkedinSearchProfilesThinInput(TypedDict, total=False):
    """Input for LinkedIn Profile Search (basic)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    currentCompanyId: NotRequired[str]
    """Filter by current employer, using a numeric LinkedIn company id. Comma-separate for several."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; a page holds 10 profiles."""
    firstName: NotRequired[str]
    """Filter by first name (e.g. Jane)."""
    followerOfUrn: NotRequired[str]
    """Return only people who follow this member, given the member's LinkedIn URN."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    industryId: NotRequired[str]
    """Filter by industry, using a LinkedIn industry id."""
    lastName: NotRequired[str]
    """Filter by last name (e.g. Okafor)."""
    locationId: NotRequired[str]
    """Filter by location, using a LinkedIn geocode id."""
    pastCompanyId: NotRequired[str]
    """Filter by a previous employer, using a numeric LinkedIn company id."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileLanguage: NotRequired[str]
    """Filter by the language the profile is written in (ISO 2-letter code, e.g. en)."""
    query: Required[str]
    """Search query for LinkedIn profiles - a role, name, or keywords (e.g. 'Marketing Manager')."""
    schoolId: NotRequired[str]
    """Filter by school, using a LinkedIn school id."""
    serviceCategoryId: NotRequired[str]
    """Filter by service category, using a numeric service-category id."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    title: NotRequired[str]
    """Filter by job title or headline (e.g. Head of Talent)."""


class LinkedinSearchServicesInput(TypedDict, total=False):
    """Input for LinkedIn Service Provider Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    geoId: NotRequired[str]
    """LinkedIn geo id to target a precise location (e.g. 103644278 for the United States); more exact than the free-text location, and overrides it when both are sent."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    location: NotRequired[str]
    """Optional location filter as a place name (e.g. 'Australia', 'New York'). LinkedIn picks its closest location match, so a short or ambiguous name can land elsewhere; use geoId for an exact place."""
    page: NotRequired[int]
    """Which page of up to 10 people to return, starting at 1 (1-100, default 1). Each page is billed as one request. Range: 1 to 100. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The service to search for, as keywords (e.g. 'Web Development', 'Accounting', 'Photography')."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class LinkedinAdData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_type: str = Field(
        alias="adType",
        description="Populated whenever the provider has data for the entity.",
    )
    advertiser: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    advertiser_linkedin_page: str = Field(
        alias="advertiserLinkedinPage",
        description="Populated whenever the provider has data for the entity.",
    )
    advertiser_logo: str | None = Field(
        default=None,
        alias="advertiserLogo",
        description="Advertiser logo image URL. The query string is a signed token, so keep the URL intact.",
    )
    cta: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    description: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    destination_url: str = Field(alias="destinationUrl")
    end_date: str = Field(alias="endDate", description="ISO 8601 date.")
    headline: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    id: str
    image: str
    start_date: str = Field(alias="startDate", description="ISO 8601 date.")
    total_impressions: str = Field(alias="totalImpressions")
    url: str | None = Field(
        default=None, description="Canonical LinkedIn Ad Library URL for this ad."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL for a video ad, or empty string. The query string is a signed token, so keep the URL intact.",
    )


class LinkedinAdsData(BaseModel):
    items: list[LinkedinAdsItem] = Field(
        description="Ad records from the LinkedIn Ad Library. Populated whenever the provider has data for the entity."
    )


class LinkedinAdsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    advertiser: str | None = Field(
        default=None,
        description="Advertiser (company) name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    advertiser_logo: str | None = Field(
        default=None, alias="advertiserLogo", description="Advertiser logo image URL."
    )
    format: str | None = Field(
        default=None, description="Ad format (e.g. SINGLE_IMAGE, VIDEO)."
    )
    id: str = Field(
        description="LinkedIn ad id. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="Ad creative image URL.")
    text: str | None = Field(default=None, description="Ad creative body text.")
    url: str = Field(
        description="Canonical LinkedIn Ad Library detail URL. Populated whenever the provider has data for the entity."
    )


class LinkedinAdsSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[LinkedinAdsSearchAd] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    next_cursor: str = Field(alias="nextCursor")
    total_ads: int = Field(alias="totalAds")


class LinkedinAdsSearchAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_type: str = Field(
        alias="adType",
        description="Populated whenever the provider has data for the entity.",
    )
    advertiser: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    advertiser_linkedin_page: str = Field(alias="advertiserLinkedinPage")
    advertiser_logo: str | None = Field(
        default=None,
        alias="advertiserLogo",
        description="Advertiser logo image URL. The query string is a signed token, so keep the URL intact.",
    )
    cta: str
    description: str
    destination_url: str = Field(alias="destinationUrl")
    end_date: str = Field(alias="endDate")
    headline: str
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    start_date: str = Field(alias="startDate")
    total_impressions: str = Field(alias="totalImpressions")
    url: str | None = Field(
        default=None, description="Canonical LinkedIn Ad Library URL for this ad."
    )


class LinkedinArticleData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None,
        description="Display name of the person or organization that published the article. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="Follower count of the author at capture time.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical LinkedIn profile or company URL of the author.",
    )
    body: str = Field(
        description="Full body text of the article as plain text. Populated whenever the provider has data for the entity."
    )
    comments: int | None = Field(
        default=None, description="Total comments on the article."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None,
        description="Short summary of the article, as LinkedIn presents it in previews.",
    )
    image: str | None = Field(
        default=None, description="Cover image URL of the article."
    )
    reactions: int | None = Field(
        default=None, description="Total reactions on the article."
    )
    title: str = Field(
        description="Title of the article. Populated whenever the provider has data for the entity."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Kind of LinkedIn publication, e.g. article or issue (a newsletter edition).",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical URL of the article. Populated whenever the provider has data for the entity."
    )


class LinkedinCommentReactionsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinCommentReactionsItem] = Field(
        description="Reactions on the comment, one record per reactor, newest first."
    )
    page: int | None = Field(
        default=None, description="The page this response holds, starting at 1."
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="How many pages of up to 100 reactions the comment has.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="How many reactions the comment has in total, across every page.",
    )


class LinkedinCommentReactionsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    actor: LinkedinCommentReactionsActor = Field(
        description="The reactor - the person or company that reacted."
    )
    comment_urn: str | None = Field(
        default=None,
        alias="commentUrn",
        description="LinkedIn URN of the comment that was reacted to, naming its post and the comment id (e.g. urn:li:comment:(activity:7510715600319467520,7510768837462745088)).",
    )
    id: str | None = Field(
        default=None, description="LinkedIn identifier of the reaction."
    )
    reaction_type: str = Field(
        alias="reactionType",
        description="Reaction kind (e.g. LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION, ENTERTAINMENT).",
    )


class LinkedinCommentReactionsActor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None,
        description="LinkedIn member or company id of the reactor. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None, description="Profile picture URL of the reactor."
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn profile or company URL of the reactor. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(
        description="Full name of the reactor (or company name). Populated whenever the provider has data for the entity."
    )
    position: str | None = Field(
        default=None,
        description="Reactor's current job title / headline (or follower count for a company). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinCommentRepliesData(BaseModel):
    items: list[LinkedinCommentRepliesItem] = Field(
        description="Up to the 10 newest replies to the comment, newest first. Populated whenever the provider has data for the entity."
    )


class LinkedinCommentRepliesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    actor: LinkedinCommentRepliesActor | None = Field(
        default=None, description="The person or company that replied."
    )
    commentary: str = Field(
        description="Full text of the reply. Populated whenever the provider has data for the entity."
    )
    content_annotations: list[LinkedinCommentRepliesContentAnnotation] | None = Field(
        default=None,
        alias="contentAnnotations",
        description="Structured mentions and links embedded in the reply text.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    edited: bool | None = Field(
        default=None, description="Whether the reply has been edited."
    )
    engagement: LinkedinCommentRepliesEngagement | None = Field(
        default=None, description="Engagement metrics for the reply."
    )
    id: str = Field(
        description="Unique identifier of the reply. Populated whenever the provider has data for the entity."
    )
    post_id: str | None = Field(
        default=None,
        alias="postId",
        description="Identifier of the post the comment belongs to (e.g. activity:7510715600319467520).",
    )
    url: str | None = Field(
        default=None,
        description="Canonical permalink URL of the reply. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinCommentRepliesActor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None, description="LinkedIn identifier of the replier."
    )
    image: str | None = Field(
        default=None,
        description="Profile picture URL of the replier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn URL of the replier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Display name of the replier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    position: str | None = Field(
        default=None,
        description="Replier's headline or job title as displayed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Replier kind, e.g. 'profile' or 'company'.",
    )


class LinkedinCommentRepliesContentAnnotation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    hyperlink: str | None = Field(
        default=None,
        description="Canonical hyperlink attached to the annotation, when present.",
    )
    length: int | None = Field(
        default=None, description="Length of the annotated text span. Minimum: 0."
    )
    profile_first_name: str | None = Field(
        default=None,
        alias="profileFirstName",
        description="First name of a mentioned profile, when present.",
    )
    profile_handle: str | None = Field(
        default=None,
        alias="profileHandle",
        description="Public LinkedIn handle of a mentioned profile, when present.",
    )
    profile_id: str | None = Field(
        default=None,
        alias="profileId",
        description="LinkedIn identifier of a mentioned profile, when present.",
    )
    profile_last_name: str | None = Field(
        default=None,
        alias="profileLastName",
        description="Last name of a mentioned profile, when present.",
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical LinkedIn URL of a mentioned profile, when present.",
    )
    start: int | None = Field(
        default=None,
        description="Zero-based start offset of the annotation in the reply text. Minimum: 0.",
    )
    text_link: str | None = Field(
        default=None,
        alias="textLink",
        description="Canonical text link attached to the annotation, when present.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Kind of content annotation."
    )


class LinkedinCommentRepliesEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    likes: int | None = Field(
        default=None, description="Number of reactions on the reply."
    )
    reactions: list[LinkedinCommentRepliesReaction] | None = Field(
        default=None,
        description="Per-reaction-type breakdown of the reactions on the reply.",
    )


class LinkedinCommentRepliesReaction(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int | None = Field(
        default=None, description="Number of reactions of this type."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Reaction type, e.g. LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION.",
    )


class LinkedinCompanyData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Company type, e.g. Privately Held, Public Company.",
    )
    description: str = Field(
        description="Company about/description text. Populated whenever the provider has data for the entity."
    )
    employee_count: int = Field(
        alias="employeeCount",
        description="Reported total employee count. Populated whenever the provider has data for the entity.",
    )
    employee_count_range: LinkedinCompanyEmployeeCountRange | None = Field(
        default=None,
        alias="employeeCountRange",
        description="LinkedIn size bucket the company falls in.",
    )
    follower_count: int = Field(
        alias="followerCount",
        description="LinkedIn page follower count. Populated whenever the provider has data for the entity.",
    )
    founded_on: LinkedinCompanyFoundedOn | None = Field(
        default=None,
        alias="foundedOn",
        description="Founding date (year populated when known).",
    )
    funding_data: LinkedinCompanyFundingData | None = Field(
        default=None,
        alias="fundingData",
        description="Funding summary sourced from Crunchbase, when available.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn's numeric company id, as a string."
    )
    industry: str = Field(description="Primary industry.")
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn company page URL.",
    )
    locations: list[LinkedinCompanyLocation] | None = Field(
        default=None, description="Company office locations, including headquarters."
    )
    logo_url: str = Field(alias="logoUrl", description="Company logo image URL.")
    name: str = Field(description="Company name.")
    page_verified: bool | None = Field(
        default=None,
        alias="pageVerified",
        description="Whether LinkedIn has verified the company page.",
    )
    similar_organizations: list[Any] | None = Field(
        default=None,
        alias="similarOrganizations",
        description="Similar organizations surfaced by LinkedIn.",
    )
    specialities: list[Any] | None = Field(
        default=None, description="Company-declared specialities."
    )
    tagline: str = Field(description="Company tagline/slogan.")
    universal_name: str | None = Field(
        default=None,
        alias="universalName",
        description="LinkedIn universal (vanity) name for the company.",
    )
    website: str = Field(description="Company website URL.")


class LinkedinCompanyEmployeeCountRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    end: int | None = Field(
        default=None,
        description="Upper bound of the employee-count bucket; null when the source does not report it.",
    )
    start: int | None = Field(
        default=None,
        description="Lower bound of the employee-count bucket; null when the source does not report it.",
    )


class LinkedinCompanyFoundedOn(BaseModel):
    model_config = ConfigDict(extra="allow")

    year: int | None = Field(default=None, description="Year the company was founded.")


class LinkedinCompanyFundingData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_crunchbase_url: str | None = Field(
        default=None,
        alias="companyCrunchbaseUrl",
        description="Crunchbase profile URL for the company.",
    )
    last_funding_type: str | None = Field(
        default=None,
        alias="lastFundingType",
        description="Type of the most recent funding round.",
    )
    num_funding_rounds: int | None = Field(
        default=None,
        alias="numFundingRounds",
        description="Total number of funding rounds; null when the source does not report it.",
    )


class LinkedinCompanyLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(default=None, description="City.")
    country: str | None = Field(default=None, description="ISO country code.")
    headquarter: bool | None = Field(
        default=None, description="True when this location is the headquarters."
    )
    line1: str | None = Field(default=None, description="Street address line.")
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Postal code."
    )


class LinkedinCompanyEmployeesData(BaseModel):
    items: list[LinkedinCompanyEmployeesItem] = Field(
        description="Employee records for the company. Populated whenever the provider has data for the entity."
    )


class LinkedinCompanyEmployeesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str | None = Field(
        default=None, description="City of the member, as LinkedIn words it."
    )
    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="LinkedIn's numeric id of the member's current company, as a string.",
    )
    company_url: str | None = Field(
        default=None,
        alias="companyUrl",
        description="Canonical LinkedIn URL of the member's current company.",
    )
    country: str | None = Field(default=None, description="Country name of the member.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code of the member.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the profile was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    creator: bool | None = Field(
        default=None, description="Whether the member is in LinkedIn creator mode."
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="First name."
    )
    handle: str | None = Field(
        default=None,
        description="Public profile identifier (the vanity slug in the URL). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(default=None, description="Profile picture URL.")
    influencer: bool | None = Field(
        default=None, description="Whether LinkedIn marks the member as an influencer."
    )
    job_title: str | None = Field(
        default=None,
        alias="jobTitle",
        description="The employee's current role or headline.",
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Last name."
    )
    location: str | None = Field(
        default=None,
        description="The employee's location as a single string (city, region, country).",
    )
    name: str | None = Field(
        default=None,
        description="Full name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    open_to_work: bool | None = Field(
        default=None,
        alias="openToWork",
        description="Whether the member shows the Open To Work badge.",
    )
    premium: bool | None = Field(
        default=None, description="Whether the member has LinkedIn Premium."
    )
    url: str = Field(
        description="Canonical LinkedIn profile URL. Populated whenever the provider has data for the entity."
    )


class LinkedinCompanyPostsData(BaseModel):
    items: list[LinkedinCompanyPostsItem] = Field(
        description="The company's recent posts. Populated whenever the provider has data for the entity."
    )


class LinkedinCompanyPostsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    article_image: str | None = Field(
        default=None,
        alias="articleImage",
        description="Cover image URL of the attached article. The query string is a signed token, so keep the URL intact.",
    )
    article_link_label: str | None = Field(
        default=None,
        alias="articleLinkLabel",
        description="Accessible link label LinkedIn renders for the attached article.",
    )
    article_subtitle: str | None = Field(
        default=None,
        alias="articleSubtitle",
        description="Subtitle or source domain of the attached article.",
    )
    article_title: str | None = Field(
        default=None,
        alias="articleTitle",
        description="Title of the article attached to the post.",
    )
    article_url: str | None = Field(
        default=None,
        alias="articleUrl",
        description="Destination URL of the attached article.",
    )
    author: LinkedinCompanyPostsAuthor | None = Field(
        default=None, description="The post author (a company or a profile)."
    )
    content_attributes: list[LinkedinCompanyPostsContentAttribute] | None = Field(
        default=None,
        alias="contentAttributes",
        description="Inline mentions and entity references in the post text.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    engagement: LinkedinCompanyPostsEngagement | None = Field(
        default=None, description="Engagement metrics for the post."
    )
    id: str = Field(
        description="Unique identifier of the post. Populated whenever the provider has data for the entity."
    )
    post_images: list[LinkedinCompanyPostsPostImage] | None = Field(
        default=None, alias="postImages", description="Images attached to the post."
    )
    post_video: LinkedinCompanyPostsPostVideo | None = Field(
        default=None,
        alias="postVideo",
        description="Video attached to the post, or null when absent.",
    )
    repost_author_name: str | None = Field(
        default=None,
        alias="repostAuthorName",
        description="Display name of the account that reposted this post.",
    )
    repost_author_universal_name: str | None = Field(
        default=None,
        alias="repostAuthorUniversalName",
        description="URL-safe handle of the account that reposted this post.",
    )
    repost_author_url: str | None = Field(
        default=None,
        alias="repostAuthorUrl",
        description="Canonical LinkedIn URL of the account that reposted this post.",
    )
    repost_created_utc: float | None = Field(
        default=None,
        alias="repostCreatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) of the repost. Multiply by 1000 for a JS Date in milliseconds.",
    )
    share_url: str | None = Field(
        default=None,
        alias="shareUrl",
        description="Shareable LinkedIn URL for the post.",
    )
    text: str = Field(
        description="Full text content of the post. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )


class LinkedinCompanyPostsAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    followers: str | None = Field(
        default=None,
        description="Author follower count as displayed text (e.g. '1,543,793 followers'). Absent when the author is a person, whose card shows a headline instead.",
    )
    handle: str | None = Field(
        default=None, description="Public identifier (vanity handle) of the author."
    )
    id: str | None = Field(
        default=None, description="LinkedIn identifier of the author."
    )
    image: str | None = Field(
        default=None,
        description="Author avatar or company logo image URL. The query string is a signed token, so keep the URL intact.",
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn URL of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Display name of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Author kind, e.g. 'company' or 'profile'.",
    )
    universal_name: str | None = Field(
        default=None,
        alias="universalName",
        description="URL-safe company/profile handle, when present. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinCompanyPostsContentAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinCompanyPostsEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    comments: int | None = Field(
        default=None, description="Number of comments on the post."
    )
    likes: int | None = Field(
        default=None,
        description="Total reaction count on the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reactions: list[LinkedinCompanyPostsReaction] | None = Field(
        default=None, description="Per-reaction-type breakdown of the reaction total."
    )
    shares: int | None = Field(
        default=None, description="Number of shares/reposts of the post."
    )


class LinkedinCompanyPostsReaction(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int | None = Field(
        default=None, description="Number of reactions of this type."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Reaction type, e.g. LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION.",
    )


class LinkedinCompanyPostsPostImage(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinCompanyPostsPostVideo(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinCompanyPostsThinData(BaseModel):
    items: list[LinkedinCompanyPostsThinItem] = Field(
        description="The company's recent posts. Populated whenever the provider has data for the entity."
    )


class LinkedinCompanyPostsThinItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Unique identifier of the post. Populated whenever the provider has data for the entity."
    )
    text: str = Field(
        description="Text content of the post. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )


class LinkedinCompanyThinData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Company type, e.g. Privately Held, Public Company.",
    )
    cover_image: str | None = Field(
        default=None,
        alias="coverImage",
        description="Company page cover image URL. The query string is a signed token, so keep the URL intact.",
    )
    description: str = Field(
        description="Company about/description text. Populated whenever the provider has data for the entity."
    )
    employee_count: int = Field(
        alias="employeeCount", description="Reported employee count."
    )
    follower_count: int | None = Field(
        default=None, alias="followerCount", description="LinkedIn page follower count."
    )
    founded_year: int | None = Field(
        default=None,
        alias="foundedYear",
        description="Year the company was founded, or 0 when unknown.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn's numeric company id, as a string."
    )
    industry: str = Field(
        description="Primary industry. Populated whenever the provider has data for the entity."
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn company page URL.",
    )
    logo_url: str = Field(
        alias="logoUrl",
        description="Company logo image URL. Populated whenever the provider has data for the entity.",
    )
    name: str = Field(description="Company name.")
    tagline: str = Field(
        description="Company tagline/slogan. Populated whenever the provider has data for the entity."
    )
    universal_name: str | None = Field(
        default=None,
        alias="universalName",
        description="LinkedIn universal (vanity) name for the company.",
    )
    website: str = Field(
        description="Company website URL. Populated whenever the provider has data for the entity."
    )


class LinkedinEmailData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    about: str | None = Field(
        default=None, description="About/summary text of the profile."
    )
    avatar_url: str | None = Field(
        default=None, alias="avatarUrl", description="URL of the profile avatar image."
    )
    city: str | None = Field(default=None, description="City of the profile owner.")
    connections_count: int | None = Field(
        default=None,
        alias="connectionsCount",
        description="Number of connections on the profile.",
    )
    country: str | None = Field(
        default=None, description="Country of the profile owner."
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code of the profile owner.",
    )
    cover_image: str | None = Field(
        default=None,
        alias="coverImage",
        description="Profile cover (banner) image URL. The query string is a signed token, so keep the URL intact.",
    )
    creator: bool | None = Field(
        default=None, description="Whether the member is in LinkedIn creator mode."
    )
    emails: list[LinkedinEmailEmail] = Field(
        description="Deliverability-validated work emails discovered for the profile. Populated whenever the provider has data for the entity."
    )
    first_name: str | None = Field(
        default=None,
        alias="firstName",
        description="First name on the LinkedIn profile.",
    )
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="Number of followers of the profile.",
    )
    handle: str | None = Field(
        default=None, description="Public identifier (vanity handle) of the profile."
    )
    headline: str | None = Field(default=None, description="Profile headline.")
    hiring: bool | None = Field(
        default=None, description="Whether the member shows the Hiring badge."
    )
    id: str | None = Field(default=None, description="LinkedIn member identifier.")
    influencer: bool | None = Field(
        default=None, description="Whether LinkedIn marks the member as an influencer."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Last name on the LinkedIn profile."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn profile URL."
    )
    location: str | None = Field(
        default=None, description="Location as LinkedIn displays it."
    )
    open_to_work: bool | None = Field(
        default=None,
        alias="openToWork",
        description="Whether the member shows the Open To Work badge.",
    )
    premium: bool | None = Field(
        default=None, description="Whether the member has LinkedIn Premium."
    )
    state: str | None = Field(
        default=None, description="State or region of the profile owner."
    )
    verified: bool | None = Field(
        default=None, description="Whether LinkedIn has verified the member's identity."
    )


class LinkedinEmailEmail(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    deliverable: bool | None = Field(
        default=None,
        description="True when the email passed deliverability checks (including SMTP).",
    )
    email: str = Field(
        description="Discovered work email address. Populated whenever the provider has data for the entity."
    )
    quality_score: int | None = Field(
        default=None,
        alias="qualityScore",
        description="Confidence score for the email, 0-100.",
    )
    status: str | None = Field(
        default=None,
        description="Validation status of the email (e.g. valid). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    valid_email_server: bool | None = Field(
        default=None,
        alias="validEmailServer",
        description="True when the domain has a valid mail server.",
    )


class LinkedinGroupData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    admin_count: int | None = Field(
        alias="adminCount", description="Total number of group admins."
    )
    admins: list[LinkedinGroupAdmin] = Field(
        description="Group admins LinkedIn shows on the group page."
    )
    cover_image: str | None = Field(
        alias="coverImage",
        description="Group cover (hero) image URL. The query string is a signed token, so keep the URL intact.",
    )
    created_utc: float | None = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    description: str | None = Field(description="Group about text.")
    id: str = Field(description="Numeric LinkedIn group id, as a string.")
    image: str | None = Field(
        description="Group logo image URL. The query string is a signed token, so keep the URL intact."
    )
    invitation_level: str | None = Field(
        alias="invitationLevel",
        description="Who may invite new members, as LinkedIn reports it (e.g. ADMIN, ALL).",
    )
    member_count: int | None = Field(
        alias="memberCount", description="Number of group members."
    )
    name: str = Field(description="Group name.")
    post_approval_enabled: bool | None = Field(
        alias="postApprovalEnabled",
        description="True when admins must approve posts before they appear.",
    )
    public_visibility: bool | None = Field(
        alias="publicVisibility",
        description="True when the group is publicly visible (listed in search), false when unlisted.",
    )
    rules: str | None = Field(description="Group rules as written by its admins.")
    url: str = Field(description="Canonical LinkedIn group URL.")


class LinkedinGroupAdmin(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    first_name: str | None = Field(
        default=None, alias="firstName", description="Admin first name."
    )
    headline: str | None = Field(default=None, description="Admin profile headline.")
    id: str | None = Field(default=None, description="LinkedIn member id of the admin.")
    image: str | None = Field(
        default=None,
        description="Admin profile picture URL. The query string is a signed token, so keep the URL intact.",
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Admin last name."
    )
    url: str | None = Field(
        default=None, description="Canonical LinkedIn profile URL of the admin."
    )


class LinkedinGroupPostsData(BaseModel):
    items: list[LinkedinGroupPostsItem] = Field(
        description="Posts in the group, newest first. A post the group admins pinned can come first on page 1. Populated whenever the provider has data for the entity."
    )


class LinkedinGroupPostsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    article_description: str | None = Field(
        default=None,
        alias="articleDescription",
        description="Description excerpt of the attached article, when present.",
    )
    article_image: str | None = Field(
        default=None,
        alias="articleImage",
        description="Cover image URL of the attached article. The query string is a signed token, so keep the URL intact.",
    )
    article_link_label: str | None = Field(
        default=None,
        alias="articleLinkLabel",
        description="Accessible link label LinkedIn renders for the attached article.",
    )
    article_subtitle: str | None = Field(
        default=None,
        alias="articleSubtitle",
        description="Subtitle or source domain of the attached article.",
    )
    article_title: str | None = Field(
        default=None,
        alias="articleTitle",
        description="Title of the article attached to the post.",
    )
    article_url: str | None = Field(
        default=None,
        alias="articleUrl",
        description="Destination URL of the attached article.",
    )
    author: LinkedinGroupPostsAuthor | None = Field(
        default=None, description="The member who posted in the group."
    )
    content_attributes: list[LinkedinGroupPostsContentAttribute] | None = Field(
        default=None,
        alias="contentAttributes",
        description="Inline links, mentions and entity references in the post text, each with its character offset.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    document_image: str | None = Field(
        default=None,
        alias="documentImage",
        description="Cover image URL of the attached document's first page, when present. The query string is a signed token, so keep the URL intact.",
    )
    document_page_count: int | None = Field(
        default=None,
        alias="documentPageCount",
        description="Number of pages in the attached document, when present. Minimum: 0.",
    )
    document_title: str | None = Field(
        default=None,
        alias="documentTitle",
        description="Title of the document (PDF carousel) attached to the post, when present.",
    )
    document_url: str | None = Field(
        default=None,
        alias="documentUrl",
        description="Download URL of the attached document as a PDF, when present. The query string is a signed token that expires, so keep the URL intact.",
    )
    edited: bool | None = Field(
        default=None, description="Whether the post was edited after it was published."
    )
    engagement: LinkedinGroupPostsEngagement | None = Field(
        default=None, description="Engagement metrics for the post."
    )
    id: str = Field(
        description="Unique identifier of the post. Populated whenever the provider has data for the entity."
    )
    newsletter_title: str | None = Field(
        default=None,
        alias="newsletterTitle",
        description="Title of the LinkedIn newsletter associated with the post, when present.",
    )
    newsletter_url: str | None = Field(
        default=None,
        alias="newsletterUrl",
        description="Canonical URL of the LinkedIn newsletter associated with the post, when present.",
    )
    pinned: bool | None = Field(
        default=None,
        description="Whether the group admins pinned the post to the top of the group.",
    )
    poll_closed: bool | None = Field(
        default=None,
        alias="pollClosed",
        description="Whether the attached poll is closed.",
    )
    poll_options: list[LinkedinGroupPostsPollOption] | None = Field(
        default=None,
        alias="pollOptions",
        description="Options and public vote counts for an attached poll.",
    )
    poll_question: str | None = Field(
        default=None,
        alias="pollQuestion",
        description="Question asked by an attached LinkedIn poll.",
    )
    poll_total_votes: int | None = Field(
        default=None,
        alias="pollTotalVotes",
        description="Total votes recorded by the attached poll. Minimum: 0.",
    )
    post_images: list[LinkedinGroupPostsPostImage] | None = Field(
        default=None, alias="postImages", description="Images attached to the post."
    )
    post_video: LinkedinGroupPostsPostVideo | None = Field(
        default=None,
        alias="postVideo",
        description="Video attached to the post, or null when absent.",
    )
    repost_article_description: str | None = Field(
        default=None,
        alias="repostArticleDescription",
        description="Description excerpt of the reposted post's article, when present.",
    )
    repost_article_image: str | None = Field(
        default=None,
        alias="repostArticleImage",
        description="Image URL of the reposted post's article, when present.",
    )
    repost_article_link_label: str | None = Field(
        default=None,
        alias="repostArticleLinkLabel",
        description="Accessible display label for the reposted post's article link, when present.",
    )
    repost_article_subtitle: str | None = Field(
        default=None,
        alias="repostArticleSubtitle",
        description="Subtitle or publisher label of the reposted post's article, when present.",
    )
    repost_article_title: str | None = Field(
        default=None,
        alias="repostArticleTitle",
        description="Title of the article attached to the reposted post, when present.",
    )
    repost_article_url: str | None = Field(
        default=None,
        alias="repostArticleUrl",
        description="Canonical URL of the reposted post's article, when present.",
    )
    repost_author_handle: str | None = Field(
        default=None,
        alias="repostAuthorHandle",
        description="Public LinkedIn profile handle of the reposted post's author, when present.",
    )
    repost_author_headline: str | None = Field(
        default=None,
        alias="repostAuthorHeadline",
        description="Headline or follower summary of the reposted post's author, when present.",
    )
    repost_author_id: str | None = Field(
        default=None,
        alias="repostAuthorId",
        description="Stable LinkedIn identifier of the reposted post's author, when present.",
    )
    repost_author_image: str | None = Field(
        default=None,
        alias="repostAuthorImage",
        description="Image URL of the reposted post's author, when present.",
    )
    repost_author_name: str | None = Field(
        default=None,
        alias="repostAuthorName",
        description="Display name of the reposted post's author, when present.",
    )
    repost_author_type: str | None = Field(
        default=None,
        alias="repostAuthorType",
        description="Author kind for the reposted post, when present.",
    )
    repost_author_universal_name: str | None = Field(
        default=None,
        alias="repostAuthorUniversalName",
        description="Universal LinkedIn name of the reposted post's company author, when present.",
    )
    repost_author_url: str | None = Field(
        default=None,
        alias="repostAuthorUrl",
        description="Canonical LinkedIn URL of the reposted post's author, when present.",
    )
    repost_created_utc: float | None = Field(
        default=None,
        alias="repostCreatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the reposted post was published. Multiply by 1000 for a JS Date in milliseconds.",
    )
    repost_engagement: LinkedinGroupPostsRepostEngagement | None = Field(
        default=None,
        alias="repostEngagement",
        description="Engagement metrics for the reposted post, when present.",
    )
    repost_id: str | None = Field(
        default=None,
        alias="repostId",
        description="Unique identifier of the reposted post, when present.",
    )
    repost_images: list[LinkedinGroupPostsRepostImage] | None = Field(
        default=None,
        alias="repostImages",
        description="Images attached to the reposted post.",
    )
    repost_text: str | None = Field(
        default=None,
        alias="repostText",
        description="Text content of the reposted post, when present.",
    )
    repost_url: str | None = Field(
        default=None,
        alias="repostUrl",
        description="Canonical URL of the reposted post, when present.",
    )
    repost_video_thumbnail: str | None = Field(
        default=None,
        alias="repostVideoThumbnail",
        description="Video thumbnail image URL of the reposted post, when present.",
    )
    repost_video_url: str | None = Field(
        default=None,
        alias="repostVideoUrl",
        description="Video stream URL of the reposted post, when present. The query string is a signed token, so keep the URL intact.",
    )
    share_url: str | None = Field(
        default=None,
        alias="shareUrl",
        description="Shareable LinkedIn URL for the post.",
    )
    text: str = Field(
        description="Full text content of the post. Empty for a repost shared without added text. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )


class LinkedinGroupPostsAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    group_admin: bool | None = Field(
        default=None,
        alias="groupAdmin",
        description="Whether LinkedIn labels the author as an admin of this group.",
    )
    handle: str | None = Field(
        default=None, description="Public identifier (vanity handle) of the author."
    )
    headline: str | None = Field(
        default=None,
        description="Profile headline of the author (the tagline under the name).",
    )
    id: str | None = Field(
        default=None, description="LinkedIn identifier of the author."
    )
    image: str | None = Field(
        default=None,
        description="Author profile picture URL. The query string is a signed token, so keep the URL intact.",
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="LinkedIn profile URL of the author, with tracking query params stripped. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Display name of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Author kind, e.g. profile."
    )
    website: str | None = Field(
        default=None,
        description="Website URL the author shows on their profile, when present.",
    )


class LinkedinGroupPostsContentAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinGroupPostsEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    comments: int | None = Field(
        default=None, description="Number of comments on the post."
    )
    likes: int | None = Field(
        default=None,
        description="Total reaction count on the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reactions: list[LinkedinGroupPostsReaction] | None = Field(
        default=None, description="Per-reaction-type breakdown of the reaction total."
    )
    shares: int | None = Field(
        default=None, description="Number of shares/reposts of the post."
    )


class LinkedinGroupPostsReaction(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int | None = Field(
        default=None, description="Number of reactions of this type."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Reaction type, e.g. LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION.",
    )


class LinkedinGroupPostsPollOption(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str = Field(description="Poll option text.")
    votes: int = Field(description="Votes recorded for this option. Minimum: 0.")


class LinkedinGroupPostsPostImage(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinGroupPostsPostVideo(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinGroupPostsRepostEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    comments: int | None = Field(
        default=None, description="Number of comments on the reposted post."
    )
    likes: int | None = Field(
        default=None, description="Total reaction count on the reposted post."
    )
    shares: int | None = Field(
        default=None, description="Number of shares/reposts of the reposted post."
    )


class LinkedinGroupPostsRepostImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    height: int | None = Field(
        default=None, description="Height of the reposted image in pixels. Minimum: 0."
    )
    url: str = Field(description="URL of an image attached to the reposted post.")
    width: int | None = Field(
        default=None, description="Width of the reposted image in pixels. Minimum: 0."
    )


class LinkedinJobData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    applicant_tracking_system: str | None = Field(
        default=None,
        alias="applicantTrackingSystem",
        description="Applicant tracking system behind the posting (e.g. Workday, Lever, Greenhouse), when LinkedIn reports one.",
    )
    applicants: int | None = Field(
        default=None,
        description="Number of applicants reported by LinkedIn. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    apply_url: str | None = Field(
        default=None,
        alias="applyUrl",
        description="External company apply URL when the job applies off-site.",
    )
    benefits: list[str] | None = Field(default=None, description="Listed benefits.")
    city: str | None = Field(default=None, description="City of the job location.")
    company: LinkedinJobCompany | None = Field(
        default=None, description="Hiring company details."
    )
    country: str | None = Field(
        default=None, description="Country of the job location."
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code of the job location.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the job was posted. Multiply by 1000 for a JS Date in milliseconds.",
    )
    description_text: str | None = Field(
        default=None,
        alias="descriptionText",
        description="Full job description as plain text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    easy_apply_url: str | None = Field(
        default=None,
        alias="easyApplyUrl",
        description="LinkedIn Easy Apply URL when available.",
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type (e.g. full_time, contract, part_time).",
    )
    experience_level: str | None = Field(
        default=None,
        alias="experienceLevel",
        description="Seniority / experience level (e.g. Mid-Senior level, Entry level).",
    )
    expire_utc: float | None = Field(
        default=None,
        alias="expireUtc",
        description="UTC epoch timestamp in seconds (Unix time) the posting expires. Multiply by 1000 for a JS Date in milliseconds.",
    )
    hiring_team: list[LinkedinJobHiringTeam] | None = Field(
        default=None,
        alias="hiringTeam",
        description="LinkedIn members named on the posting as the hiring contacts.",
    )
    id: str | None = Field(default=None, description="LinkedIn job posting id.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the role."
    )
    job_state: str | None = Field(
        default=None,
        alias="jobState",
        description="Posting state reported by LinkedIn (e.g. LISTED, CLOSED).",
    )
    location: str | None = Field(
        default=None, description="Job location (city, region, or country)."
    )
    remote: bool | None = Field(
        default=None, description="Whether LinkedIn flags the role as remote-allowed."
    )
    salary: LinkedinJobSalary | None = Field(
        default=None, description="Salary range when disclosed by the poster."
    )
    state: str | None = Field(
        default=None, description="State or region of the job location."
    )
    title: str = Field(
        description="Job title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(description="Canonical LinkedIn job posting URL.")
    views: int | None = Field(
        default=None, description="Number of views LinkedIn reports for the posting."
    )
    workplace_type: str | None = Field(
        default=None,
        alias="workplaceType",
        description="Workplace type (e.g. remote, on_site, hybrid).",
    )


class LinkedinJobCompany(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(default=None, description="Company About text.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Number of employees LinkedIn reports for the company.",
    )
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="Number of followers of the company page.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn's numeric company id, as a string."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn company URL."
    )
    logo: str | None = Field(default=None, description="Company logo image URL.")
    name: str | None = Field(
        default=None,
        description="Company name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    universal_name: str | None = Field(
        default=None,
        alias="universalName",
        description="Company LinkedIn universal (vanity) name.",
    )
    website: str | None = Field(default=None, description="Company website.")


class LinkedinJobHiringTeam(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn profile URL."
    )
    name: str | None = Field(default=None, description="Member name.")
    position: str | None = Field(
        default=None, description="Member headline or job title."
    )


class LinkedinJobSalary(BaseModel):
    model_config = ConfigDict(extra="allow")

    max: float | None = Field(default=None, description="Maximum salary.")
    min: float | None = Field(default=None, description="Minimum salary.")
    text: str | None = Field(
        default=None, description="Salary as displayed (e.g. '300,000 - 330,000 USD')."
    )


class LinkedinJobsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinJobsItem] = Field(
        description="Full job listing records for the search. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of job listings, or null when there are no more. Pass it back as cursor to continue.",
    )


class LinkedinJobsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    applicant_tracking_system: str | None = Field(
        default=None,
        alias="applicantTrackingSystem",
        description="Applicant tracking system behind the external apply link (e.g. Greenhouse).",
    )
    applicants: int | None = Field(
        default=None,
        description="Number of applicants reported by LinkedIn. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    apply_url: str | None = Field(
        default=None,
        alias="applyUrl",
        description="External company apply URL when the job applies off-site.",
    )
    benefits: list[str] | None = Field(default=None, description="Listed benefits.")
    city: str | None = Field(default=None, description="City of the job location.")
    company: LinkedinJobsCompany | None = Field(
        default=None, description="Hiring company details."
    )
    country: str | None = Field(
        default=None, description="Country of the job location."
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code of the job location.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the job was posted. Multiply by 1000 for a JS Date in milliseconds.",
    )
    description_text: str | None = Field(
        default=None,
        alias="descriptionText",
        description="Full job description as plain text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    easy_apply_url: str | None = Field(
        default=None,
        alias="easyApplyUrl",
        description="LinkedIn Easy Apply URL when available.",
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type (e.g. full_time, contract, part_time).",
    )
    experience_level: str | None = Field(
        default=None,
        alias="experienceLevel",
        description="Seniority / experience level (e.g. Mid-Senior level, Entry level).",
    )
    expire_utc: float | None = Field(
        default=None,
        alias="expireUtc",
        description="UTC epoch timestamp in seconds (Unix time) the posting expires. Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(default=None, description="LinkedIn job listing id.")
    industries: list[str] | None = Field(
        default=None, description="Industries associated with the role."
    )
    job_state: str | None = Field(
        default=None,
        alias="jobState",
        description="Posting state reported by LinkedIn (e.g. LISTED, CLOSED).",
    )
    location: str | None = Field(
        default=None, description="Job location (city, region, or country)."
    )
    remote: bool | None = Field(
        default=None, description="Whether LinkedIn flags the role as remote-allowed."
    )
    salary: LinkedinJobsSalary | None = Field(
        default=None, description="Salary range when disclosed by the poster."
    )
    state: str | None = Field(
        default=None, description="State or region of the job location."
    )
    title: str = Field(description="Job title.")
    url: str = Field(description="Canonical LinkedIn job listing URL.")
    views: int | None = Field(
        default=None, description="Number of views LinkedIn reports for the posting."
    )
    workplace_type: str | None = Field(
        default=None,
        alias="workplaceType",
        description="Workplace type (e.g. remote, on_site, hybrid).",
    )


class LinkedinJobsCompany(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(default=None, description="Company About text.")
    employee_count: int | None = Field(
        default=None,
        alias="employeeCount",
        description="Number of employees LinkedIn reports for the company.",
    )
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="Number of followers of the company page.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn's numeric company id, as a string."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Canonical LinkedIn company URL."
    )
    logo: str | None = Field(default=None, description="Company logo image URL.")
    name: str | None = Field(default=None, description="Company name.")
    universal_name: str | None = Field(
        default=None,
        alias="universalName",
        description="Company LinkedIn universal (vanity) name.",
    )
    website: str | None = Field(default=None, description="Company website.")


class LinkedinJobsSalary(BaseModel):
    model_config = ConfigDict(extra="allow")

    max: float | None = Field(
        default=None, description="Maximum salary; null when the posting shows none."
    )
    min: float | None = Field(
        default=None, description="Minimum salary; null when the posting shows none."
    )
    text: str | None = Field(
        default=None, description="Salary as displayed (e.g. '300,000 - 330,000 USD')."
    )


class LinkedinJobsThinData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinJobsThinItem] = Field(
        description="Job listing index records for the search. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of job listings, or null when there are no more. Pass it back as cursor to continue.",
    )


class LinkedinJobsThinItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company: str | None = Field(
        default=None,
        description="Hiring company name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_url: str | None = Field(
        default=None, alias="companyUrl", description="Canonical LinkedIn company URL."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(default=None, description="LinkedIn job listing id.")
    location: str | None = Field(
        default=None,
        description="Job location (city, region). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    logo_url: str | None = Field(
        default=None, alias="logoUrl", description="Hiring company logo image URL."
    )
    title: str = Field(
        description="Job title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical LinkedIn job listing URL. Populated whenever the provider has data for the entity."
    )


class LinkedinPostData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Name of the post author. Populated whenever the provider has data for the entity."
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author avatar or company logo image URL, or null when the serving source does not carry one. The query string is a signed token, so keep the URL intact.",
    )
    author_url: str | None = Field(
        default=None, alias="authorUrl", description="LinkedIn URL of the post author."
    )
    comments: int = Field(description="Number of comments on the post.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    image: str | None = Field(
        default=None,
        description="First image attached to the post, or null when the serving source does not carry one. The query string is a signed token, so keep the URL intact.",
    )
    likes: int = Field(description="Number of likes on the post.")
    text: str = Field(
        description="Text content of the post. Populated whenever the provider has data for the entity."
    )
    title: str = Field(description="Title of the post.")
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )


class LinkedinPostCommentsData(BaseModel):
    items: list[LinkedinPostCommentsItem] = Field(
        description="The post's comments. Populated whenever the provider has data for the entity."
    )


class LinkedinPostCommentsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    actor: LinkedinPostCommentsActor | None = Field(
        default=None, description="The commenter (a profile or a company)."
    )
    commentary: str = Field(
        description="Full text of the comment. Populated whenever the provider has data for the entity."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    edited: bool | None = Field(
        default=None, description="Whether the comment has been edited."
    )
    engagement: LinkedinPostCommentsEngagement | None = Field(
        default=None, description="Engagement metrics for the comment."
    )
    id: str = Field(
        description="Unique identifier of the comment. Populated whenever the provider has data for the entity."
    )
    pinned: bool | None = Field(
        default=None, description="Whether the comment is pinned on the post."
    )
    url: str | None = Field(
        default=None,
        description="Canonical permalink URL of the comment. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinPostCommentsActor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None, description="LinkedIn identifier of the commenter."
    )
    image: str | None = Field(
        default=None,
        description="Profile picture URL of the commenter. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn URL of the commenter. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Display name of the commenter. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    position: str | None = Field(
        default=None,
        description="Commenter's headline or job title as displayed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Commenter kind, e.g. 'profile' or 'company'.",
    )


class LinkedinPostCommentsEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    comments: int | None = Field(
        default=None, description="Number of replies to the comment."
    )
    likes: int | None = Field(
        default=None, description="Number of likes on the comment."
    )


class LinkedinPostReactionsData(BaseModel):
    items: list[LinkedinPostReactionsItem] = Field(
        description="Reactions on the post, one record per reactor."
    )


class LinkedinPostReactionsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    actor: LinkedinPostReactionsActor = Field(
        description="The reactor - the person or company that reacted."
    )
    id: str | None = Field(
        default=None, description="LinkedIn identifier of the reaction."
    )
    post_id: str | None = Field(
        default=None,
        alias="postId",
        description="LinkedIn URN of the post that was reacted to.",
    )
    reaction_type: str = Field(
        alias="reactionType",
        description="Reaction kind (e.g. LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION, ENTERTAINMENT).",
    )


class LinkedinPostReactionsActor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None,
        description="LinkedIn member or company id of the reactor. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn profile or company URL of the reactor. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(
        description="Full name of the reactor (or company name). Populated whenever the provider has data for the entity."
    )
    picture_url: str | None = Field(
        default=None,
        alias="pictureUrl",
        description="Profile picture URL of the reactor.",
    )
    position: str | None = Field(
        default=None,
        description="Reactor's current job title / headline (or follower count for a company). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinPostTranscriptData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    transcript: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    transcript_not_available: bool = Field(alias="transcriptNotAvailable")
    url: str


class LinkedinProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str | None = Field(
        default=None, description="About/summary text of the profile."
    )
    certifications: list[LinkedinProfileCertification] | None = Field(
        default=None, description="Licenses and certifications."
    )
    city: str | None = Field(default=None, description="City of the profile owner.")
    connections_count: int | None = Field(
        default=None, alias="connectionsCount", description="Number of connections."
    )
    country: str | None = Field(
        default=None, description="Country of the profile owner."
    )
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code of the profile owner.",
    )
    cover_image: str | None = Field(
        default=None,
        alias="coverImage",
        description="Profile cover (banner) image URL. The query string is a signed token, so keep the URL intact.",
    )
    creator: bool | None = Field(
        default=None, description="Whether the member is in LinkedIn creator mode."
    )
    current_position: list[LinkedinProfileCurrentPosition] | None = Field(
        default=None,
        alias="currentPosition",
        description="The member's current role(s).",
    )
    education: list[LinkedinProfileEducation] | None = Field(
        default=None, description="Education entries."
    )
    experience: list[LinkedinProfileExperience] | None = Field(
        default=None,
        description="Full work experience with titles, descriptions, dates, and per-role skills. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    first_name: str = Field(
        alias="firstName", description="First name of the profile owner."
    )
    follower_count: int | None = Field(
        default=None, alias="followerCount", description="Number of followers."
    )
    headline: str = Field(
        description="Professional headline shown under the name. Populated whenever the provider has data for the entity."
    )
    hiring: bool | None = Field(
        default=None, description="Whether the member shows the Hiring badge."
    )
    honors_and_awards: list[LinkedinProfileHonorsAndAward] | None = Field(
        default=None, alias="honorsAndAwards", description="Honors and awards."
    )
    id: str | None = Field(default=None, description="LinkedIn member identifier.")
    influencer: bool | None = Field(
        default=None, description="Whether LinkedIn marks the member as an influencer."
    )
    languages: list[Any] | None = Field(
        default=None, description="Languages, as returned by LinkedIn when present."
    )
    last_name: str = Field(
        alias="lastName", description="Last name of the profile owner."
    )
    location: str | None = Field(
        default=None, description="Location of the profile owner."
    )
    open_to_work: bool | None = Field(
        default=None,
        alias="openToWork",
        description="Whether the member is open to work.",
    )
    photo: str | None = Field(default=None, description="URL of the profile photo.")
    premium: bool | None = Field(
        default=None, description="Whether the member has LinkedIn Premium."
    )
    projects: list[Any] | None = Field(
        default=None, description="Projects, as returned by LinkedIn when present."
    )
    public_identifier: str | None = Field(
        default=None,
        alias="publicIdentifier",
        description="LinkedIn public identifier (the /in/ handle).",
    )
    publications: list[LinkedinProfilePublication] | None = Field(
        default=None, description="Publications."
    )
    skills: list[LinkedinProfileSkill] | None = Field(
        default=None,
        description="The member's skills: an object per skill, or a bare skill name when LinkedIn shows no endorsed-skills section.",
    )
    state: str | None = Field(
        default=None, description="State or region of the profile owner."
    )
    top_skills: list[Any] | None = Field(
        default=None,
        alias="topSkills",
        description="The member's top skills, as free-form strings when present.",
    )
    url: str = Field(description="Canonical LinkedIn profile URL.")
    verified: bool | None = Field(
        default=None, description="Whether the profile is identity-verified."
    )


class LinkedinProfileCertification(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    issued_at: str | None = Field(
        default=None, alias="issuedAt", description="Issue date text."
    )
    issued_by: str | None = Field(
        default=None, alias="issuedBy", description="Issuing organization."
    )
    title: str | None = Field(default=None, description="Certification title.")


class LinkedinProfileCurrentPosition(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="LinkedIn's numeric company id, as a string.",
    )
    company_linkedin_url: str | None = Field(
        default=None, alias="companyLinkedinUrl", description="Company LinkedIn URL."
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Company name."
    )
    duration: str | None = Field(
        default=None, description="Human-readable tenure, e.g. '12 yrs 6 mos'."
    )
    location: str | None = Field(default=None, description="Role location.")
    position: str | None = Field(default=None, description="Job title.")


class LinkedinProfileEducation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    degree: str | None = Field(default=None, description="Degree earned.")
    end_date: str | None = Field(
        default=None, alias="endDate", description="End date text."
    )
    field_of_study: str | None = Field(
        default=None, alias="fieldOfStudy", description="Field of study."
    )
    school: str = Field(description="School name.")
    school_id: str | None = Field(
        default=None,
        alias="schoolId",
        description="LinkedIn's numeric school id, as a string.",
    )
    school_url: str | None = Field(
        default=None, alias="schoolUrl", description="School LinkedIn URL."
    )
    start_date: str | None = Field(
        default=None, alias="startDate", description="Start date text."
    )


class LinkedinProfileExperience(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="LinkedIn's numeric company id, as a string.",
    )
    company_linkedin_url: str | None = Field(
        default=None, alias="companyLinkedinUrl", description="Company LinkedIn URL."
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Company name."
    )
    description: str | None = Field(default=None, description="Role description.")
    duration: str | None = Field(
        default=None, description="Human-readable tenure, e.g. '3 yrs 2 mos'."
    )
    employment_type: str | None = Field(
        default=None,
        alias="employmentType",
        description="Employment type, e.g. 'Full-time'.",
    )
    end_date: str | None = Field(
        default=None, alias="endDate", description="End date text, e.g. 'Present'."
    )
    location: str | None = Field(default=None, description="Role location.")
    position: str = Field(
        description="Job title. Populated whenever the provider has data for the entity."
    )
    skills: list[Any] | None = Field(
        default=None, description="Skills associated with this role."
    )
    start_date: str | None = Field(
        default=None, alias="startDate", description="Start date text, e.g. 'Feb 2014'."
    )
    workplace_type: str | None = Field(
        default=None,
        alias="workplaceType",
        description="Workplace type, e.g. 'Remote' or 'On-site'.",
    )


class LinkedinProfileHonorsAndAward(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(default=None, description="Award description.")
    issued_at: str | None = Field(
        default=None, alias="issuedAt", description="Issue date text."
    )
    issued_by: str | None = Field(
        default=None, alias="issuedBy", description="Issuing organization."
    )
    title: str | None = Field(default=None, description="Award title.")


class LinkedinProfilePublication(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(
        default=None, description="Publication description."
    )
    published_text: str | None = Field(
        default=None,
        alias="publishedText",
        description="Publisher and/or date text as shown on LinkedIn.",
    )
    title: str | None = Field(default=None, description="Publication title.")


class LinkedinProfileSkill(BaseModel):
    model_config = ConfigDict(extra="allow")

    endorsements: str | None = Field(
        default=None,
        description="Endorsement count as LinkedIn shows it, e.g. '23 endorsements'. Null from a source that does not read endorsements; name it in requireFields to be served by one that does.",
    )
    name: str | None = Field(default=None, description="Skill name.")
    positions: list[str] | None = Field(
        default=None,
        description="Where the skill was used or who endorsed it, as LinkedIn shows it, e.g. 'Endorsed by 3 colleagues at Rippling'. Null from a source that does not read them; name it in requireFields to be served by one that does.",
    )


class LinkedinProfileCommentsData(BaseModel):
    items: list[LinkedinProfileCommentsItem] = Field(
        description="Comments this member left on other people's posts, newest first, each with the post it was left on. Populated whenever the provider has data for the entity."
    )


class LinkedinProfileCommentsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    actor: LinkedinProfileCommentsActor | None = Field(
        default=None,
        description="The member who left the comment (a profile or a company).",
    )
    commentary: str = Field(
        description="Full text of the comment the member left. Populated whenever the provider has data for the entity."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    edited: bool | None = Field(
        default=None,
        description="Whether the comment has been edited. Null when the serving source does not report it.",
    )
    engagement: LinkedinProfileCommentsEngagement | None = Field(
        default=None, description="Engagement metrics for the comment."
    )
    id: str = Field(
        description="Unique identifier of the comment. Populated whenever the provider has data for the entity."
    )
    is_author: bool | None = Field(
        default=None,
        alias="isAuthor",
        description="Whether the commenter is also the author of the post. Null when the serving source does not report it.",
    )
    post: LinkedinProfileCommentsPost | None = Field(
        default=None,
        description="The post the comment was left on, so the comment can be read in context. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical permalink URL of the comment. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinProfileCommentsActor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None, description="LinkedIn identifier of the commenter."
    )
    image: str | None = Field(
        default=None,
        description="Profile picture URL of the commenter. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn URL of the commenter. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Display name of the commenter. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    position: str | None = Field(
        default=None,
        description="Commenter's headline or job title as displayed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Commenter kind, e.g. 'profile' or 'company'.",
    )


class LinkedinProfileCommentsEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    comments: int | None = Field(
        default=None, description="Number of replies to the comment. Minimum: 0."
    )
    likes: int | None = Field(
        default=None, description="Number of likes on the comment. Minimum: 0."
    )
    shares: int | None = Field(
        default=None, description="Number of shares of the comment. Minimum: 0."
    )


class LinkedinProfileCommentsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: LinkedinProfileCommentsAuthor | None = Field(
        default=None, description="Author of the post that was commented on."
    )
    engagement: LinkedinProfileCommentsEngagement2 | None = Field(
        default=None,
        description="Public engagement totals on the post that was commented on.",
    )
    id: str | None = Field(
        default=None,
        description="Unique identifier of the LinkedIn post that was commented on.",
    )
    posted_utc: float | None = Field(
        default=None,
        alias="postedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the post was published. Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    text: str | None = Field(
        default=None,
        description="Text content of the post that was commented on. Empty when the post carries no commentary of its own, such as a bare reshare or an image-only post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical LinkedIn URL of the post that was commented on. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinProfileCommentsAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    headline: str | None = Field(
        default=None,
        description="Public headline or company follower summary for the post author.",
    )
    image: str | None = Field(
        default=None,
        description="Profile or company image URL of the post author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Display name of the post author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical LinkedIn profile or company URL of the post author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    public_identifier: str | None = Field(
        default=None,
        alias="publicIdentifier",
        description='LinkedIn public identifier (vanity slug) of the post author, for example "williamhgates". Stable across lanes, unlike the raw id.',
    )


class LinkedinProfileCommentsEngagement2(BaseModel):
    model_config = ConfigDict(extra="allow")

    comments: int | None = Field(
        default=None, description="Total comment count on the post. Minimum: 0."
    )
    reactions: int | None = Field(
        default=None, description="Total reaction count on the post. Minimum: 0."
    )
    reposts: int | None = Field(
        default=None, description="Total repost or share count on the post. Minimum: 0."
    )


class LinkedinProfilePostsFullData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinProfilePostsFullItem] = Field(
        description="Recent enriched posts published by the profile. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when there are no more. Pass it back as cursor to continue.",
    )


class LinkedinProfilePostsFullItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    article_description: str | None = Field(
        default=None,
        alias="articleDescription",
        description="Description excerpt of the attached article, when present.",
    )
    article_image: str | None = Field(
        default=None,
        alias="articleImage",
        description="Image URL of the attached article, when present.",
    )
    article_image_height: int | None = Field(
        default=None,
        alias="articleImageHeight",
        description="Height of the attached article image in pixels. Minimum: 0.",
    )
    article_image_width: int | None = Field(
        default=None,
        alias="articleImageWidth",
        description="Width of the attached article image in pixels. Minimum: 0.",
    )
    article_link_label: str | None = Field(
        default=None,
        alias="articleLinkLabel",
        description="Accessible display label for the attached article link, when present.",
    )
    article_subtitle: str | None = Field(
        default=None,
        alias="articleSubtitle",
        description="Subtitle or publisher label of the attached article, when present.",
    )
    article_title: str | None = Field(
        default=None,
        alias="articleTitle",
        description="Title of the attached article, when present.",
    )
    article_url: str | None = Field(
        default=None,
        alias="articleUrl",
        description="Canonical URL of the attached article, when present.",
    )
    author: LinkedinProfilePostsFullAuthor | None = Field(
        default=None,
        description="Detailed identity and publication information for the post author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    content_annotations: list[LinkedinProfilePostsFullContentAnnotation] | None = Field(
        default=None,
        alias="contentAnnotations",
        description="Structured mentions and links embedded in the post text.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    engagement: LinkedinProfilePostsFullEngagement | None = Field(
        default=None,
        description="Engagement totals and reaction breakdown for the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Unique identifier of the LinkedIn post. Populated whenever the provider has data for the entity."
    )
    images: list[LinkedinProfilePostsFullImage] | None = Field(
        default=None, description="Images attached to the post."
    )
    newsletter_title: str | None = Field(
        default=None,
        alias="newsletterTitle",
        description="Title of the LinkedIn newsletter associated with the post, when present.",
    )
    newsletter_url: str | None = Field(
        default=None,
        alias="newsletterUrl",
        description="Canonical URL of the LinkedIn newsletter associated with the post, when present.",
    )
    publication_url: str | None = Field(
        default=None,
        alias="publicationUrl",
        description="Canonical LinkedIn feed publication URL for the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    repost_article_description: str | None = Field(
        default=None,
        alias="repostArticleDescription",
        description="Description excerpt of the reposted post's article, when present.",
    )
    repost_article_image: str | None = Field(
        default=None,
        alias="repostArticleImage",
        description="Image URL of the reposted post's article, when present.",
    )
    repost_article_image_height: int | None = Field(
        default=None,
        alias="repostArticleImageHeight",
        description="Height of the reposted post's article image in pixels. Minimum: 0.",
    )
    repost_article_image_width: int | None = Field(
        default=None,
        alias="repostArticleImageWidth",
        description="Width of the reposted post's article image in pixels. Minimum: 0.",
    )
    repost_article_link_label: str | None = Field(
        default=None,
        alias="repostArticleLinkLabel",
        description="Accessible display label for the reposted post's article link, when present.",
    )
    repost_article_subtitle: str | None = Field(
        default=None,
        alias="repostArticleSubtitle",
        description="Subtitle or publisher label of the reposted post's article, when present.",
    )
    repost_article_title: str | None = Field(
        default=None,
        alias="repostArticleTitle",
        description="Title of the article attached to the reposted post, when present.",
    )
    repost_article_url: str | None = Field(
        default=None,
        alias="repostArticleUrl",
        description="Canonical URL of the reposted post's article, when present.",
    )
    repost_author_handle: str | None = Field(
        default=None,
        alias="repostAuthorHandle",
        description="Public LinkedIn profile handle of the reposted post's author, when present.",
    )
    repost_author_headline: str | None = Field(
        default=None,
        alias="repostAuthorHeadline",
        description="Headline or follower summary of the reposted post's author, when present.",
    )
    repost_author_id: str | None = Field(
        default=None,
        alias="repostAuthorId",
        description="Stable LinkedIn identifier of the reposted post's author, when present.",
    )
    repost_author_image: str | None = Field(
        default=None,
        alias="repostAuthorImage",
        description="Image URL of the reposted post's author, when present.",
    )
    repost_author_name: str | None = Field(
        default=None,
        alias="repostAuthorName",
        description="Display name of the reposted post's author, when present.",
    )
    repost_author_type: str | None = Field(
        default=None,
        alias="repostAuthorType",
        description="Author kind for the reposted post, when present.",
    )
    repost_author_universal_name: str | None = Field(
        default=None,
        alias="repostAuthorUniversalName",
        description="Universal LinkedIn name of the reposted post's company author, when present.",
    )
    repost_author_url: str | None = Field(
        default=None,
        alias="repostAuthorUrl",
        description="Canonical LinkedIn URL of the reposted post's author, when present.",
    )
    repost_created_utc: float | None = Field(
        default=None,
        alias="repostCreatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the reposted post was published. Multiply by 1000 for a JS Date in milliseconds.",
    )
    repost_id: str | None = Field(
        default=None,
        alias="repostId",
        description="Unique identifier of the reposted post, when present.",
    )
    repost_images: list[LinkedinProfilePostsFullRepostImage] | None = Field(
        default=None,
        alias="repostImages",
        description="Images attached to the reposted post.",
    )
    repost_text: str | None = Field(
        default=None,
        alias="repostText",
        description="Text content of the reposted post, when present.",
    )
    repost_url: str | None = Field(
        default=None,
        alias="repostUrl",
        description="Canonical URL of the reposted post, when present.",
    )
    social_content: LinkedinProfilePostsFullSocialContent | None = Field(
        default=None,
        alias="socialContent",
        description="LinkedIn visibility and action flags for the post.",
    )
    text: str = Field(
        description="Text content of the post. Populated whenever the provider has data for the entity."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="LinkedIn record type reported for the post.",
    )
    url: str = Field(
        description="Canonical LinkedIn URL of the post. Populated whenever the provider has data for the entity."
    )
    video_thumbnail: str | None = Field(
        default=None,
        alias="videoThumbnail",
        description="Thumbnail URL of the attached video, when present.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="URL of the attached video, when present.",
    )


class LinkedinProfilePostsFullAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    handle: str | None = Field(
        default=None,
        description="Public LinkedIn profile handle of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    headline: str | None = Field(
        default=None,
        description="Professional headline or follower summary displayed for the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str | None = Field(
        default=None,
        description="Stable LinkedIn identifier of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Profile or company image URL of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image_height: int | None = Field(
        default=None,
        alias="imageHeight",
        description="Height of the author image in pixels. Minimum: 0.",
    )
    image_width: int | None = Field(
        default=None,
        alias="imageWidth",
        description="Width of the author image in pixels. Minimum: 0.",
    )
    name: str | None = Field(
        default=None,
        description="Display name of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical LinkedIn profile or company URL of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Author kind, such as profile or company. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    universal_name: str | None = Field(
        default=None,
        alias="universalName",
        description="Universal LinkedIn name used for company authors, when present.",
    )
    website: str | None = Field(
        default=None, description="Publication or website URL displayed by the author."
    )
    website_label: str | None = Field(
        default=None,
        alias="websiteLabel",
        description="Display label for the author's publication or website link.",
    )


class LinkedinProfilePostsFullContentAnnotation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        default=None,
        alias="companyId",
        description="LinkedIn identifier of a mentioned company, when present.",
    )
    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Display name of a mentioned company, when present.",
    )
    company_url: str | None = Field(
        default=None,
        alias="companyUrl",
        description="Canonical LinkedIn URL of a mentioned company, when present.",
    )
    hyperlink: str | None = Field(
        default=None,
        description="Canonical hyperlink attached to the annotation, when present.",
    )
    length: int | None = Field(
        default=None, description="Length of the annotated text span. Minimum: 0."
    )
    profile_first_name: str | None = Field(
        default=None,
        alias="profileFirstName",
        description="First name of a mentioned profile, when present.",
    )
    profile_handle: str | None = Field(
        default=None,
        alias="profileHandle",
        description="Public LinkedIn handle of a mentioned profile, when present.",
    )
    profile_id: str | None = Field(
        default=None,
        alias="profileId",
        description="LinkedIn identifier of a mentioned profile, when present.",
    )
    profile_last_name: str | None = Field(
        default=None,
        alias="profileLastName",
        description="Last name of a mentioned profile, when present.",
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical LinkedIn URL of a mentioned profile, when present.",
    )
    start: int | None = Field(
        default=None,
        description="Zero-based start offset of the annotation in the post text. Minimum: 0.",
    )
    text_link: str | None = Field(
        default=None,
        alias="textLink",
        description="Canonical text link attached to the annotation, when present.",
    )
    type_: str | None = Field(
        default=None, alias="type", description="Kind of content annotation."
    )


class LinkedinProfilePostsFullEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    breakdown: list[LinkedinProfilePostsFullBreakdown] | None = Field(
        default=None, description="Counts grouped by LinkedIn reaction type."
    )
    comments: int | None = Field(
        default=None,
        description="Total number of comments on the post. Populated whenever the provider has data for the entity. Minimum: 0. Present whenever the upstream returns this record.",
    )
    reactions: int | None = Field(
        default=None,
        description="Total number of reactions on the post. Populated whenever the provider has data for the entity. Minimum: 0. Present whenever the upstream returns this record.",
    )
    reposts: int | None = Field(
        default=None,
        description="Total number of reposts or shares of the post. Populated whenever the provider has data for the entity. Minimum: 0. Present whenever the upstream returns this record.",
    )


class LinkedinProfilePostsFullBreakdown(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int = Field(description="Number of reactions of this type. Minimum: 0.")
    type_: str = Field(alias="type", description="LinkedIn reaction type.")


class LinkedinProfilePostsFullImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    height: int | None = Field(
        default=None, description="Height of the image in pixels. Minimum: 0."
    )
    url: str = Field(description="URL of the attached image.")
    width: int | None = Field(
        default=None, description="Width of the image in pixels. Minimum: 0."
    )


class LinkedinProfilePostsFullRepostImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    height: int | None = Field(
        default=None, description="Height of the reposted image in pixels. Minimum: 0."
    )
    url: str = Field(description="URL of an image attached to the reposted post.")
    width: int | None = Field(
        default=None, description="Width of the reposted image in pixels. Minimum: 0."
    )


class LinkedinProfilePostsFullSocialContent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    hide_comment_action: bool | None = Field(
        default=None,
        alias="hideCommentAction",
        description="Whether LinkedIn hides the comment action.",
    )
    hide_comments_count: bool | None = Field(
        default=None,
        alias="hideCommentsCount",
        description="Whether LinkedIn hides the comment count.",
    )
    hide_react_action: bool | None = Field(
        default=None,
        alias="hideReactAction",
        description="Whether LinkedIn hides the react action.",
    )
    hide_reactions_count: bool | None = Field(
        default=None,
        alias="hideReactionsCount",
        description="Whether LinkedIn hides the reaction count.",
    )
    hide_reposts_count: bool | None = Field(
        default=None,
        alias="hideRepostsCount",
        description="Whether LinkedIn hides the repost count.",
    )
    hide_send_action: bool | None = Field(
        default=None,
        alias="hideSendAction",
        description="Whether LinkedIn hides the send action.",
    )
    hide_share_action: bool | None = Field(
        default=None,
        alias="hideShareAction",
        description="Whether LinkedIn hides the share action.",
    )
    hide_social_activity_counts: bool | None = Field(
        default=None,
        alias="hideSocialActivityCounts",
        description="Whether LinkedIn hides social activity counts.",
    )
    hide_views_count: bool | None = Field(
        default=None,
        alias="hideViewsCount",
        description="Whether LinkedIn hides the view count.",
    )
    share_url: str | None = Field(
        default=None,
        alias="shareUrl",
        description="Canonical LinkedIn share URL for the post.",
    )
    show_contribution_experience: bool | None = Field(
        default=None,
        alias="showContributionExperience",
        description="Whether LinkedIn enables the contribution experience.",
    )
    show_social_detail: bool | None = Field(
        default=None,
        alias="showSocialDetail",
        description="Whether LinkedIn shows social detail.",
    )


class LinkedinProfilePostsThinData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinProfilePostsThinItem] = Field(
        description="Recent posts published by the profile. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when there are no more. Pass it back as cursor to continue.",
    )


class LinkedinProfilePostsThinItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    article_image: str | None = Field(
        default=None,
        alias="articleImage",
        description="Image URL of the attached article, when present.",
    )
    article_subtitle: str | None = Field(
        default=None,
        alias="articleSubtitle",
        description="Subtitle or publisher label of the attached article, when present.",
    )
    article_title: str | None = Field(
        default=None,
        alias="articleTitle",
        description="Title of the attached article, when present.",
    )
    article_url: str | None = Field(
        default=None,
        alias="articleUrl",
        description="Canonical URL of the attached article, when present.",
    )
    author: LinkedinProfilePostsThinAuthor | None = Field(
        default=None,
        description="Portable details about the post author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    engagement: LinkedinProfilePostsThinEngagement | None = Field(
        default=None,
        description="Portable engagement totals for the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Unique identifier of the LinkedIn post. Populated whenever the provider has data for the entity."
    )
    images: list[LinkedinProfilePostsThinImage] | None = Field(
        default=None, description="Images attached to the post."
    )
    repost_article_image: str | None = Field(
        default=None,
        alias="repostArticleImage",
        description="Cover image URL of the article attached to the reposted post. The query string is a signed token, so keep the URL intact.",
    )
    repost_article_subtitle: str | None = Field(
        default=None,
        alias="repostArticleSubtitle",
        description="Subtitle or source domain of the article attached to the reposted post.",
    )
    repost_article_title: str | None = Field(
        default=None,
        alias="repostArticleTitle",
        description="Title of the article attached to the reposted post, when present.",
    )
    repost_article_url: str | None = Field(
        default=None,
        alias="repostArticleUrl",
        description="Canonical URL of the article attached to the reposted post, when present.",
    )
    repost_author_headline: str | None = Field(
        default=None,
        alias="repostAuthorHeadline",
        description="Headline or follower line of the author of the reposted post.",
    )
    repost_author_image: str | None = Field(
        default=None,
        alias="repostAuthorImage",
        description="Avatar or logo image URL of the author of the reposted post. The query string is a signed token, so keep the URL intact.",
    )
    repost_author_url: str | None = Field(
        default=None,
        alias="repostAuthorUrl",
        description="Canonical LinkedIn URL of the author of the reposted post.",
    )
    repost_created_utc: float | None = Field(
        default=None,
        alias="repostCreatedUtc",
        description="UTC epoch timestamp in seconds (Unix time) when the reposted post was published. Multiply by 1000 for a JS Date in milliseconds.",
    )
    repost_id: str | None = Field(
        default=None,
        alias="repostId",
        description="Unique identifier of the reposted post, when present.",
    )
    repost_text: str | None = Field(
        default=None,
        alias="repostText",
        description="Text content of the reposted post, when present.",
    )
    repost_url: str | None = Field(
        default=None,
        alias="repostUrl",
        description="Canonical URL of the reposted post, when present.",
    )
    text: str = Field(
        description="Text content of the post. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical LinkedIn URL of the post. Populated whenever the provider has data for the entity."
    )
    video_thumbnail: str | None = Field(
        default=None,
        alias="videoThumbnail",
        description="Thumbnail URL of the attached video, when present.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="URL of the attached video, when present.",
    )


class LinkedinProfilePostsThinAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    handle: str | None = Field(
        default=None,
        description="Public LinkedIn handle of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    headline: str | None = Field(
        default=None,
        description="Professional headline displayed for the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Profile image URL of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical LinkedIn profile URL of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinProfilePostsThinEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    comments: int | None = Field(
        default=None,
        description="Total number of comments on the post. Populated whenever the provider has data for the entity. Minimum: 0. Present whenever the upstream returns this record.",
    )
    reactions: int | None = Field(
        default=None,
        description="Total number of reactions on the post. Populated whenever the provider has data for the entity. Minimum: 0. Present whenever the upstream returns this record.",
    )
    reposts: int | None = Field(
        default=None,
        description="Total number of reposts or shares of the post. Populated whenever the provider has data for the entity. Minimum: 0. Present whenever the upstream returns this record.",
    )


class LinkedinProfilePostsThinImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str = Field(description="URL of an attached image.")


class LinkedinProfileReactionsData(BaseModel):
    items: list[LinkedinProfileReactionsItem] = Field(
        description="Posts the member has reacted to, newest first. One record per reaction, carrying both the reaction itself and the post it was made on. Populated whenever the provider has data for the entity."
    )


class LinkedinProfileReactionsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    action: str = Field(
        description='LinkedIn\'s own display sentence for the reaction, for example "Bill Gates likes this" or "Ali Abdaal liked Tobi Odutola\'s comment on this". It is the only place the reaction kind appears on this endpoint, it names the member and sometimes a third party, and it distinguishes a reaction on the post from a reaction on a comment. It is free English text, not an enum: parse it only if you accept that LinkedIn may reword it. Populated whenever the provider has data for the entity.'
    )
    actor: LinkedinProfileReactionsActor | None = Field(
        default=None,
        description="The member who reacted - the profile that was asked about. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="LinkedIn activity identifier of the reaction event itself. This is not the identifier of the post that was reacted to - that is post.id. Populated whenever the provider has data for the entity."
    )
    post: LinkedinProfileReactionsPost | None = Field(
        default=None,
        description="The post the member reacted to. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical LinkedIn feed URL of the reaction event. Use post.url for the post itself. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinProfileReactionsActor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None, description="LinkedIn member identifier of the reactor."
    )
    image: str | None = Field(
        default=None, description="Profile picture URL of the reactor."
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn profile URL of the reactor. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinProfileReactionsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: LinkedinProfileReactionsAuthor | None = Field(
        default=None,
        description="Public author identity attached to the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    engagement: LinkedinProfileReactionsEngagement | None = Field(
        default=None,
        description="Public engagement totals attached to the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str | None = Field(
        default=None,
        description="LinkedIn activity identifier of the post that was reacted to. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    posted_utc: float | None = Field(
        default=None,
        alias="postedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the post was published. Multiply by 1000 for a JS Date in milliseconds.",
    )
    repost_id: str | None = Field(
        default=None,
        alias="repostId",
        description="Unique identifier of the post this one reshares, when it is a reshare.",
    )
    text: str | None = Field(
        default=None,
        description="Text content of the post. Empty string when the post carries no commentary of its own, such as a bare reshare or an image-only post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical LinkedIn URL of the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinkedinProfileReactionsAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    headline: str | None = Field(
        default=None,
        description="Public headline for a person, or the follower summary for a company. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn identifier for the author."
    )
    image: str | None = Field(
        default=None, description="Public profile or company image URL for the author."
    )
    name: str | None = Field(
        default=None,
        description="Display name of the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical LinkedIn profile or company URL for the author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    public_identifier: str | None = Field(
        default=None,
        alias="publicIdentifier",
        description='LinkedIn public identifier (vanity slug) for the author, for example "williamhgates". Absent for company authors, which carry universalName instead.',
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Author kind, such as profile or company.",
    )
    universal_name: str | None = Field(
        default=None,
        alias="universalName",
        description="Universal LinkedIn name used for company authors, when present.",
    )


class LinkedinProfileReactionsEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    breakdown: list[LinkedinProfileReactionsBreakdown] | None = Field(
        default=None,
        description="Reaction counts on the post grouped by LinkedIn reaction type.",
    )
    comments: int | None = Field(
        default=None, description="Total comment count. Minimum: 0."
    )
    reactions: int | None = Field(
        default=None, description="Total reaction count. Minimum: 0."
    )
    reposts: int | None = Field(
        default=None, description="Total repost or share count. Minimum: 0."
    )


class LinkedinProfileReactionsBreakdown(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int = Field(description="Number of reactions of this type. Minimum: 0.")
    type_: str = Field(alias="type", description="LinkedIn reaction type.")


class LinkedinProfileThinData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str | None = Field(
        default=None, description="About/summary text of the profile."
    )
    articles: list[LinkedinProfileThinArticle] | None = Field(
        default=None,
        description="The profile's published articles, or null when the serving source does not publish them.",
    )
    avatar_url: str | None = Field(
        default=None, alias="avatarUrl", description="URL of the profile avatar image."
    )
    connections: str | None = Field(
        default=None,
        description='Connections count as LinkedIn\'s public label shows it, capped at "500+" (for example "8" or "500+"). Null when the serving source does not publish it.',
    )
    current_position: list[LinkedinProfileThinCurrentPosition] | None = Field(
        default=None,
        alias="currentPosition",
        description="The member's current role as the serving source reports it: one entry, or an empty list when the profile shows no current employer. Null when the serving source does not publish it.",
    )
    education: list[LinkedinProfileThinEducation] | None = Field(
        default=None, description="Education entries."
    )
    experience: list[LinkedinProfileThinExperience] | None = Field(
        default=None,
        description="Work experience entries: company and dates, plus the job title and whether the role is current when the serving source publishes them. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    followers: int | None = Field(default=None, description="Number of followers.")
    headline: str | None = Field(
        default=None,
        description="Profile headline, or null when the serving source does not publish it.",
    )
    location: str | None = Field(
        default=None, description="Location of the profile owner."
    )
    name: str = Field(description="Full name of the profile owner.")
    public_identifier: str | None = Field(
        default=None,
        alias="publicIdentifier",
        description="LinkedIn public identifier (the /in/ handle), or null when the serving source does not publish it.",
    )
    recent_posts: list[LinkedinProfileThinRecentPost] | None = Field(
        default=None,
        alias="recentPosts",
        description="The profile's recent posts, or null when the serving source does not publish them.",
    )


class LinkedinProfileThinArticle(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    headline: str = Field(description="Headline of the article.")
    url: str | None = Field(default=None, description="Canonical URL of the article.")


class LinkedinProfileThinCurrentPosition(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Company LinkedIn URL, or null when the serving source does not publish it.",
    )
    company_name: str = Field(alias="companyName", description="Company name.")
    position: str | None = Field(
        default=None,
        description="Job title, or null when the serving source does not publish it or the profile hides it.",
    )


class LinkedinProfileThinEducation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    end_date: str | None = Field(
        default=None, alias="endDate", description="End date of study."
    )
    school: str = Field(description="Name of the school.")
    school_url: str | None = Field(
        default=None, alias="schoolUrl", description="URL of the school page."
    )
    start_date: str | None = Field(
        default=None, alias="startDate", description="Start date of study."
    )


class LinkedinProfileThinExperience(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company: str = Field(description="Name of the company.")
    company_url: str | None = Field(
        default=None, alias="companyUrl", description="URL of the company page."
    )
    current: bool | None = Field(
        default=None,
        description="Whether this is a current role, or null when the serving source does not say.",
    )
    end_date: str | None = Field(
        default=None, alias="endDate", description="End date of the role."
    )
    position: str | None = Field(
        default=None,
        description="Job title, or null when the serving source does not publish it or the profile hides it.",
    )
    start_date: str | None = Field(
        default=None, alias="startDate", description="Start date of the role."
    )


class LinkedinProfileThinRecentPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    activity_type: str | None = Field(
        default=None, alias="activityType", description="Type of activity for the post."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(description="Unique identifier of the post.")
    text: str | None = Field(default=None, description="Text content of the post.")
    url: str | None = Field(default=None, description="Canonical URL of the post.")


class LinkedinSearchCompaniesData(BaseModel):
    items: list[LinkedinSearchCompaniesItem] = Field(
        description="Matching company records. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchCompaniesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(
        default=None,
        description="Company summary / about text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    followers_text: str | None = Field(
        default=None,
        alias="followersText",
        description="Follower count as a display string (e.g. 105K followers). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    handle: str | None = Field(
        default=None,
        description="Company universal name (the vanity slug in the URL). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="LinkedIn company id. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Company logo image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    industry: str | None = Field(
        default=None,
        description="Company industry. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    location: str | None = Field(
        default=None,
        description="Company location as a single string (city, region). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str = Field(
        description="Company name. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical LinkedIn company URL. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchGroupsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinSearchGroupsItem] = Field(
        description="Matching group records. Populated whenever the provider has data for the entity."
    )
    page: int | None = Field(description="The page this response holds, starting at 1.")
    total_pages: int | None = Field(
        alias="totalPages",
        description="How many pages of up to 10 groups the search can reach.",
    )
    total_results: int | None = Field(
        alias="totalResults",
        description="How many groups match the search in total, including those past the last reachable page.",
    )


class LinkedinSearchGroupsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(default=None, description="Group summary text.")
    id: str = Field(
        description="Numeric LinkedIn group id, as a string. Pass it to the LinkedIn Group API as groupId for the full record. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Group logo image URL. The query string is a signed token, so keep the URL intact.",
    )
    members_text: str | None = Field(
        default=None,
        alias="membersText",
        description="Member count as a display string (e.g. 648K members).",
    )
    name: str = Field(
        description="Group name. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical LinkedIn group URL. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchLeadsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinSearchLeadsItem] = Field(
        description="Matching leads, up to 25 per page. Populated whenever the provider has data for the entity."
    )
    page: int | None = Field(
        default=None, description="The page this response holds, starting at 1."
    )
    total_pages: int | None = Field(
        default=None,
        alias="totalPages",
        description="How many pages of up to 25 leads the search has.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="How many leads match the search in total, across every page.",
    )


class LinkedinSearchLeadsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str | None = Field(
        default=None, description="Profile summary text, when the member wrote one."
    )
    current_positions: list[LinkedinSearchLeadsCurrentPosition] | None = Field(
        default=None,
        alias="currentPositions",
        description="Current roles. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    first_name: str | None = Field(
        default=None,
        alias="firstName",
        description="Member's first name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn member id, the last segment of `url`."
    )
    image: str | None = Field(
        default=None,
        description="Profile picture URL. The query string is a signed token, so keep the URL intact. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    last_name: str | None = Field(
        default=None,
        alias="lastName",
        description="Member's last name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    location: str | None = Field(
        default=None,
        description="Member's location as a single string (city, region, country). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    open_profile: bool | None = Field(
        default=None,
        alias="openProfile",
        description="Whether the member accepts messages from people outside their network.",
    )
    premium: bool | None = Field(
        default=None,
        description="Whether the member has a LinkedIn Premium subscription.",
    )
    url: str = Field(
        description="LinkedIn profile URL in its member-id form (https://www.linkedin.com/in/ACwAAA...). It opens the profile on LinkedIn, and passing it as `url` to linkedin.profile returns the full record. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchLeadsCurrentPosition(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        default=None, alias="companyId", description="LinkedIn company id."
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="LinkedIn company page URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Company name."
    )
    started_on: LinkedinSearchLeadsStartedOn | None = Field(
        default=None,
        alias="startedOn",
        description="When the role started, as `month` (1-12, when shown) and `year`.",
    )
    tenure_at_company: LinkedinSearchLeadsTenureAtCompany | None = Field(
        default=None,
        alias="tenureAtCompany",
        description="Time at this company, as `numYears` and `numMonths`.",
    )
    tenure_at_position: LinkedinSearchLeadsTenureAtPosition | None = Field(
        default=None,
        alias="tenureAtPosition",
        description="Time in this role, as `numYears` and `numMonths`.",
    )
    title: str | None = Field(default=None, description="Job title.")


class LinkedinSearchLeadsStartedOn(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchLeadsTenureAtCompany(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchLeadsTenureAtPosition(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    posts: list[LinkedinSearchPostsPost] = Field(
        description="Posts matching the search query. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the post's author. Empty when the upstream omits it.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical profile URL of the post's author, with tracking query params stripped. Empty when the upstream omits it.",
    )
    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="URL of the post author's profile avatar image.",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Total number of comments on the post.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="The post's LinkedIn activity ID, as a string. Populated whenever the provider has data for the entity."
    )
    reaction_count: int | None = Field(
        default=None,
        alias="reactionCount",
        description="Total number of reactions on the post.",
    )
    text: str = Field(
        description="Text content of the post. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchPostsFullData(BaseModel):
    posts: list[LinkedinSearchPostsFullPost] = Field(
        description="LinkedIn posts matching the search query. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchPostsFullPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attachment_description: str | None = Field(
        default=None,
        alias="attachmentDescription",
        description="Short description of the attached content, as LinkedIn shows it on the preview card. Best effort on article attachments: depending on the search it may be absent, so treat it as optional. To read an article's content reliably, pass attachmentUrl to the linkedin.article endpoint.",
    )
    attachment_image: str | None = Field(
        default=None,
        alias="attachmentImage",
        description="Image URL associated with the attachment.",
    )
    attachment_subtitle: str | None = Field(
        default=None,
        alias="attachmentSubtitle",
        description="Subtitle of the attached structured content.",
    )
    attachment_title: str | None = Field(
        default=None,
        alias="attachmentTitle",
        description="Title of the attached article, job, or other structured content.",
    )
    attachment_type: str | None = Field(
        default=None,
        alias="attachmentType",
        description="Kind of structured content attached to the post, such as article, job, poll, video, or document.",
    )
    attachment_url: str | None = Field(
        default=None,
        alias="attachmentUrl",
        description="Destination URL of the attachment with tracking parameters removed; a video keeps the signed query it needs to play, and a YouTube link keeps its video id. When attachmentType is article, pass this URL to the linkedin.article endpoint to read the article's full body text.",
    )
    author: LinkedinSearchPostsFullAuthor = Field(
        description="Public author identity attached to the post. Populated whenever the provider has data for the entity."
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    engagement: LinkedinSearchPostsFullEngagement = Field(
        description="Public engagement totals attached to the post. Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Stable LinkedIn activity identifier for the post. Populated whenever the provider has data for the entity."
    )
    poll_closed: bool | None = Field(
        default=None,
        alias="pollClosed",
        description="Whether the attached poll is closed.",
    )
    poll_options: list[LinkedinSearchPostsFullPollOption] | None = Field(
        default=None,
        alias="pollOptions",
        description="Options and public vote counts for an attached poll.",
    )
    poll_question: str | None = Field(
        default=None,
        alias="pollQuestion",
        description="Question asked by an attached LinkedIn poll.",
    )
    poll_total_votes: int | None = Field(
        default=None,
        alias="pollTotalVotes",
        description="Total votes recorded by the attached poll. Minimum: 0.",
    )
    text: str = Field(
        description="Text content of the post. Empty string when the post carries no commentary of its own, such as a bare article share or an image-only post. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the LinkedIn post. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchPostsFullAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    headline: str | None = Field(
        default=None,
        description="Public headline or company follower summary for the author.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn identifier for the author."
    )
    image: str | None = Field(
        default=None, description="Public profile or company image URL for the author."
    )
    name: str | None = Field(default=None, description="Display name of the author.")
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical LinkedIn profile or company URL for the author.",
    )
    public_identifier: str | None = Field(
        default=None,
        alias="publicIdentifier",
        description='LinkedIn public identifier (vanity slug) for the author, for example "williamhgates". Stable across lanes, unlike the raw id.',
    )
    type_: Literal["person", "company", "showcase"] | None = Field(
        default=None,
        alias="type",
        description="Kind of LinkedIn entity that authored the post, derived from the author URL.",
    )


class LinkedinSearchPostsFullEngagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    breakdown: list[LinkedinSearchPostsFullBreakdown] | None = Field(
        default=None, description="Reaction counts grouped by LinkedIn reaction type."
    )
    comments: int | None = Field(
        default=None, description="Total comment count. Minimum: 0."
    )
    reactions: int | None = Field(
        default=None, description="Total reaction count. Minimum: 0."
    )
    reposts: int | None = Field(
        default=None, description="Total repost or share count. Minimum: 0."
    )


class LinkedinSearchPostsFullBreakdown(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int = Field(description="Number of reactions of this type. Minimum: 0.")
    type_: str = Field(alias="type", description="LinkedIn reaction type.")


class LinkedinSearchPostsFullPollOption(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str = Field(description="Poll option text.")
    votes: int = Field(description="Votes recorded for this option. Minimum: 0.")


class LinkedinSearchProfilesData(BaseModel):
    items: list[LinkedinSearchProfilesItem] = Field(
        description="Matched profile records. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchProfilesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str | None = Field(
        default=None,
        description="Profile about / summary text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    city: str | None = Field(default=None, description="City of the member.")
    connections_count: int | None = Field(
        default=None,
        alias="connectionsCount",
        description="Number of connections on the profile.",
    )
    country: str | None = Field(default=None, description="Country of the member.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code of the member.",
    )
    cover_image: str | None = Field(
        default=None,
        alias="coverImage",
        description="Profile cover (banner) image URL. The query string is a signed token, so keep the URL intact.",
    )
    creator: bool | None = Field(
        default=None, description="Whether the member is in LinkedIn creator mode."
    )
    current_position: list[LinkedinSearchProfilesCurrentPosition] | None = Field(
        default=None,
        alias="currentPosition",
        description="Current role(s). Each entry is an open object with the position title, company, dates, and location; shape can vary by profile.",
    )
    education: list[LinkedinSearchProfilesEducation] | None = Field(
        default=None,
        description="Education history. Each entry is an open object with school, degree, and field of study; shape can vary by profile.",
    )
    experience: list[LinkedinSearchProfilesExperience] | None = Field(
        default=None,
        description="Full work history. Each entry is an open object with the position title, company, dates, and location; shape can vary by profile. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    first_name: str | None = Field(
        default=None,
        alias="firstName",
        description="Member's first name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="Number of followers of the profile.",
    )
    handle: str | None = Field(
        default=None,
        description="Public profile identifier (the vanity slug in the URL). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    headline: str | None = Field(
        default=None,
        description="Profile headline (the tagline under the name). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    hiring: bool | None = Field(
        default=None, description="Whether the member shows the Hiring badge."
    )
    id: str = Field(description="LinkedIn member URN id for the profile.")
    image: str | None = Field(
        default=None,
        description="Profile picture URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    influencer: bool | None = Field(
        default=None, description="Whether LinkedIn marks the member as an influencer."
    )
    last_name: str | None = Field(
        default=None,
        alias="lastName",
        description="Member's last name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    location: str | None = Field(
        default=None,
        description="Member's location as a single string (city, region, country). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    open_to_work: bool | None = Field(
        default=None,
        alias="openToWork",
        description="Whether the member has the Open to Work flag set.",
    )
    premium: bool | None = Field(
        default=None,
        description="Whether the member has a LinkedIn Premium subscription.",
    )
    skills: list[Any] | None = Field(
        default=None,
        description="Listed skills, one object per skill with its name and, when the source has them, the endorsements label and related positions.",
    )
    state: str | None = Field(
        default=None, description="State or region of the member."
    )
    url: str = Field(
        description="Canonical LinkedIn profile URL. Populated whenever the provider has data for the entity."
    )
    verified: bool | None = Field(
        default=None, description="Whether LinkedIn has verified the member's identity."
    )


class LinkedinSearchProfilesCurrentPosition(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchProfilesEducation(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchProfilesExperience(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchProfilesEmailData(BaseModel):
    items: list[LinkedinSearchProfilesEmailItem] = Field(
        description="Matched profile records, each with a discovered work email. Populated whenever the provider has data for the entity."
    )


class LinkedinSearchProfilesEmailItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str | None = Field(
        default=None,
        description="Profile about / summary text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    city: str | None = Field(default=None, description="City of the member.")
    connections_count: int | None = Field(
        default=None,
        alias="connectionsCount",
        description="Number of connections on the profile.",
    )
    country: str | None = Field(default=None, description="Country of the member.")
    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code of the member.",
    )
    cover_image: str | None = Field(
        default=None,
        alias="coverImage",
        description="Profile cover (banner) image URL. The query string is a signed token, so keep the URL intact.",
    )
    creator: bool | None = Field(
        default=None, description="Whether the member is in LinkedIn creator mode."
    )
    current_position: list[LinkedinSearchProfilesEmailCurrentPosition] | None = Field(
        default=None,
        alias="currentPosition",
        description="Current role(s). Each entry is an open object with the position title, company, dates, and location; shape can vary by profile.",
    )
    education: list[LinkedinSearchProfilesEmailEducation] | None = Field(
        default=None,
        description="Education history. Each entry is an open object with school, degree, and field of study; shape can vary by profile.",
    )
    emails: list[LinkedinSearchProfilesEmailEmail] | None = Field(
        default=None,
        description="Discovered work email(s) for the member. Each entry is an open object with the email address plus deliverability signals (deliverable, disposable, catchAllDomain, validEmailServer, qualityScore, status); may be empty when no email could be verified. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    experience: list[LinkedinSearchProfilesEmailExperience] | None = Field(
        default=None,
        description="Full work history. Each entry is an open object with the position title, company, dates, and location; shape can vary by profile. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    first_name: str | None = Field(
        default=None,
        alias="firstName",
        description="Member's first name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    follower_count: int | None = Field(
        default=None,
        alias="followerCount",
        description="Number of followers of the profile; null when the source does not report it.",
    )
    handle: str | None = Field(
        default=None,
        description="Public profile identifier (the vanity slug in the URL). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    headline: str | None = Field(
        default=None,
        description="Profile headline (the tagline under the name). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    hiring: bool | None = Field(
        default=None, description="Whether the member shows the Hiring badge."
    )
    id: str = Field(description="LinkedIn member URN id for the profile.")
    image: str | None = Field(
        default=None,
        description="Profile picture URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    influencer: bool | None = Field(
        default=None, description="Whether LinkedIn marks the member as an influencer."
    )
    last_name: str | None = Field(
        default=None,
        alias="lastName",
        description="Member's last name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    location: str | None = Field(
        default=None,
        description="Member's location as a single string (city, region, country). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    open_to_work: bool | None = Field(
        default=None,
        alias="openToWork",
        description="Whether the member has the Open to Work flag set.",
    )
    premium: bool | None = Field(
        default=None,
        description="Whether the member has a LinkedIn Premium subscription.",
    )
    skills: list[Any] | None = Field(
        default=None, description="Listed skills, as free-form strings when present."
    )
    state: str | None = Field(
        default=None, description="State or region of the member."
    )
    url: str = Field(
        description="Canonical LinkedIn profile URL. Populated whenever the provider has data for the entity."
    )
    verified: bool | None = Field(
        default=None, description="Whether LinkedIn has verified the member's identity."
    )


class LinkedinSearchProfilesEmailCurrentPosition(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchProfilesEmailEducation(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchProfilesEmailEmail(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchProfilesEmailExperience(BaseModel):
    model_config = ConfigDict(extra="allow")


class LinkedinSearchProfilesThinData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinSearchProfilesThinItem] = Field(
        description="Matched profile records (basic fields only). Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of profiles, or null/empty when there are no more. Pass it back as cursor to continue.",
    )


class LinkedinSearchProfilesThinItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    handle: str | None = Field(
        default=None,
        description="Public profile identifier (the vanity slug in the URL). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    headline: str | None = Field(
        default=None,
        description="Profile headline (the tagline under the name). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str | None = Field(
        default=None, description="LinkedIn member URN id for the profile."
    )
    image: str | None = Field(default=None, description="Profile picture URL.")
    location: str | None = Field(
        default=None,
        description="Member's location as a single string (city, region, country).",
    )
    name: str | None = Field(default=None, description="Member's display name.")
    premium: bool | None = Field(
        default=None, description="Whether the member has LinkedIn Premium."
    )
    url: str = Field(
        description="Canonical LinkedIn vanity profile URL. Populated whenever the provider has data for the entity."
    )
    verified: bool | None = Field(
        default=None, description="Whether LinkedIn has verified the member's identity."
    )


class LinkedinSearchServicesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[LinkedinSearchServicesItem] = Field(
        description="People offering a matching service, in LinkedIn's order. Populated whenever the provider has data for the entity."
    )
    page: int | None = Field(
        description="The page this response holds, starting at 1, or null when not reported."
    )
    total_pages: int | None = Field(
        alias="totalPages",
        description="Number of result pages LinkedIn will serve for this search (at most 100), or null when not reported. Stop paging after this page.",
    )
    total_results: int | None = Field(
        alias="totalResults",
        description="How many people match the search in total, including those past the last reachable page, or null when not reported.",
    )


class LinkedinSearchServicesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str | None = Field(
        default=None,
        description="Profile about / summary text, when the member has one.",
    )
    headline: str | None = Field(
        default=None,
        description="Profile headline (the tagline under the name). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="LinkedIn member URN id for the profile. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Profile picture URL. The query string is a signed token, so keep the URL intact.",
    )
    location: str | None = Field(
        default=None,
        description="Member's location as a single string (city, region, country). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Member's display name. Some members show only a last-name initial (e.g. 'Chris S.'). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    service_url: str | None = Field(
        default=None,
        alias="serviceUrl",
        description="URL of the member's LinkedIn service page. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    services: list[str] | None = Field(
        default=None,
        description="Names of the services the member offers (e.g. 'Web Development', 'Web Design'). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str = Field(
        description="LinkedIn profile URL built from the member id (https://www.linkedin.com/in/<id>). It opens the profile and can be passed to linkedin.profile. Populated whenever the provider has data for the entity."
    )


class LinkedinNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ad(
        self, *, options: RequestOptions | None = None, **input: Unpack[LinkedinAdInput]
    ) -> RunResult[LinkedinAdData]:
        """LinkedIn Ad Details

        Look up a single LinkedIn Ad Library ad by URL and get the advertiser,
        headline, creative text, format, CTA, targeting, run dates, and impressions
        as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.ad(url="https://www.linkedin.com/ad-library/detail/1487405616")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.ad", dict(input), options
        )
        return RunResult[LinkedinAdData].model_validate(raw)

    def ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinAdsInput],
    ) -> RunResult[LinkedinAdsData]:
        """LinkedIn Ads Library

        Search the LinkedIn Ad Library by search URL and list the matching ads
        (advertiser, creative text, format).

        Price: $0.00006 per request plus $0.00165 per result (maximum $0.0331).

        Example:
            res = client.linkedin.ads(limit=3, url="https://www.linkedin.com/company/stripe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.ads", dict(input), options
        )
        return RunResult[LinkedinAdsData].model_validate(raw)

    def ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinAdsSearchInput],
    ) -> RunResult[LinkedinAdsSearchData]:
        """LinkedIn Ad Search

        Search the LinkedIn Ad Library by company or keyword and list matching ads
        (advertiser, headline, creative text, format, CTA, and run dates) with
        pagination.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.ads_search(company="microsoft")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.ads_search", dict(input), options
        )
        return RunResult[LinkedinAdsSearchData].model_validate(raw)

    def article(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinArticleInput],
    ) -> RunResult[LinkedinArticleData]:
        """LinkedIn Article

        Read a public LinkedIn article or newsletter issue by URL, including its
        full body text, author, publication time, and engagement counts.

        Price: $0.00569 per request plus $0 per result (maximum $0.00569).

        Example:
            res = client.linkedin.article(url="https://www.linkedin.com/pulse/artificial-intelligence-primer-stephen-dover")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.article", dict(input), options
        )
        return RunResult[LinkedinArticleData].model_validate(raw)

    def comment_reactions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCommentReactionsInput],
    ) -> RunResult[LinkedinCommentReactionsData]:
        """LinkedIn Comment Reactions

        List who reacted to a comment on a LinkedIn post - reactor name, profile
        URL, job title, and reaction type, 100 per page.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.comment_reactions(url="https://www.linkedin.com/feed/update/urn:li:activity:7510715600319467520?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7510715600319467520%2C7510768837462745088%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287510768837462745088%2Curn%3Ali%3Aactivity%3A7510715600319467520%29")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.comment_reactions", dict(input), options
        )
        return RunResult[LinkedinCommentReactionsData].model_validate(raw)

    def comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCommentRepliesInput],
    ) -> RunResult[LinkedinCommentRepliesData]:
        """LinkedIn Comment Replies

        List up to the 10 newest replies to a comment on a LinkedIn post - reply
        text, replier name/URL/job title, timestamps, and likes.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.comment_replies(url="https://www.linkedin.com/feed/update/urn:li:activity:7510715600319467520?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7510715600319467520%2C7510749329649725442%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287510749329649725442%2Curn%3Ali%3Aactivity%3A7510715600319467520%29")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.comment_replies", dict(input), options
        )
        return RunResult[LinkedinCommentRepliesData].model_validate(raw)

    def company(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyInput],
    ) -> RunResult[LinkedinCompanyData]:
        """LinkedIn Company

        Fetch a full LinkedIn company page by URL: name, description, industry,
        employee count and range, follower count, founded year, headquarters and
        office locations, funding data, tagline, logo, website, and specialities.

        Price: $0.0011 per request.

        Example:
            res = client.linkedin.company(url="https://www.linkedin.com/company/stripe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company", dict(input), options
        )
        return RunResult[LinkedinCompanyData].model_validate(raw)

    def company_employees(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyEmployeesInput],
    ) -> RunResult[LinkedinCompanyEmployeesData]:
        """LinkedIn Company Employees

        List the employees of a LinkedIn company by name or company URL, with
        optional job-title filtering.

        Price: $0.006 per request.

        Example:
            res = client.linkedin.company_employees(company="stripe", limit=3)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_employees", dict(input), options
        )
        return RunResult[LinkedinCompanyEmployeesData].model_validate(raw)

    def company_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyPostsInput],
    ) -> RunResult[LinkedinCompanyPostsData]:
        """LinkedIn Company Posts

        List a LinkedIn company page's recent posts by URL: full text, canonical
        link, publish date, author, engagement counts with a per-reaction breakdown,
        and attached media.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.company_posts(limit=10, url="https://www.linkedin.com/company/stripe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_posts", dict(input), options
        )
        return RunResult[LinkedinCompanyPostsData].model_validate(raw)

    def company_posts_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyPostsThinInput],
    ) -> RunResult[LinkedinCompanyPostsThinData]:
        """LinkedIn Company Posts (basic)

        Post text and link only. No engagement counts, author details, media, or
        reaction breakdown - for those use linkedin.company_posts.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.company_posts_thin(url="https://www.linkedin.com/company/stripe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_posts_thin", dict(input), options
        )
        return RunResult[LinkedinCompanyPostsThinData].model_validate(raw)

    def company_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyThinInput],
    ) -> RunResult[LinkedinCompanyThinData]:
        """LinkedIn Company (basic)

        Basic company: name, description, employee count, industry, logo, website,
        tagline. No follower count, founded year, office locations, or funding data
        - for those use linkedin.company.

        Price: $0.001 per request.

        Example:
            res = client.linkedin.company_thin(url="https://www.linkedin.com/company/stripe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_thin", dict(input), options
        )
        return RunResult[LinkedinCompanyThinData].model_validate(raw)

    def email(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinEmailInput],
    ) -> RunResult[LinkedinEmailData]:
        """LinkedIn Email Finder

        Find the deliverability-validated work email behind a LinkedIn profile URL
        or public ID. Returns each discovered email with its deliverability,
        validation status, and quality score, plus the person's name and headline.

        Price: $0.011 per request plus $0 per result (maximum $0.011).

        Example:
            res = client.linkedin.email(profileUrl="https://www.linkedin.com/in/satyanadella")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.email", dict(input), options
        )
        return RunResult[LinkedinEmailData].model_validate(raw)

    def group(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinGroupInput],
    ) -> RunResult[LinkedinGroupData]:
        """LinkedIn Group

        Fetch one LinkedIn group by URL or id: name, description, rules, member
        count, logo and cover image, creation date, visibility and join settings,
        and its admins.

        Price: $0.0013 per request.

        Example:
            res = client.linkedin.group(url="https://www.linkedin.com/groups/1898033")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.group", dict(input), options
        )
        return RunResult[LinkedinGroupData].model_validate(raw)

    def group_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinGroupPostsInput],
    ) -> RunResult[LinkedinGroupPostsData]:
        """LinkedIn Group Posts

        List the posts in a LinkedIn group by group URL, newest first: full text,
        canonical link, publish date, author, engagement counts with a per-reaction
        breakdown, and attached media. One call returns a page of about 100 posts;
        pass page to go further back.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.group_posts(url="https://www.linkedin.com/groups/1898033")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.group_posts", dict(input), options
        )
        return RunResult[LinkedinGroupPostsData].model_validate(raw)

    def job(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobInput],
    ) -> RunResult[LinkedinJobData]:
        """LinkedIn Job

        Fetch one LinkedIn job posting by URL: title, full description, location,
        salary when disclosed, applicant count, employment and workplace type,
        seniority, benefits, industries, apply links, posting and expiry dates, the
        hiring team, the applicant tracking system behind it, and the hiring company
        with its size, follower count, website and description.

        Price: $0.0015 per request.

        Example:
            res = client.linkedin.job(url="https://www.linkedin.com/jobs/view/4431721875/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.job", dict(input), options
        )
        return RunResult[LinkedinJobData].model_validate(raw)

    def jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsInput],
    ) -> RunResult[LinkedinJobsData]:
        """LinkedIn Jobs

        Search LinkedIn job listings by title and location - full records with
        description, salary, applicant count, seniority, company details, and
        benefits. Up to 25 jobs per request.

        Price: $0.0195 per request.

        Example:
            res = client.linkedin.jobs(limit=3, location="United States", query="software engineer", workplaceType="remote")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.jobs", dict(input), options
        )
        return RunResult[LinkedinJobsData].model_validate(raw)

    def iter_jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsInput],
    ) -> Paginator[LinkedinJobsItem, LinkedinJobsData]:
        """Iterate LinkedIn Jobs results, following pagination cursors.

        Yields validated `LinkedinJobsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "linkedin.jobs",
            dict(input),
            "items",
            item_model=LinkedinJobsItem,
            data_model=LinkedinJobsData,
            bare=False,
            options=options,
        )

    def jobs_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsThinInput],
    ) -> RunResult[LinkedinJobsThinData]:
        """LinkedIn Jobs (index)

        Cheap job index: title, company, location, posted date, URL. No description,
        salary, applicant counts, or seniority - for those use linkedin.jobs.

        Price: $0.00066 per request.

        Example:
            res = client.linkedin.jobs_thin(limit=3, location="United States", query="software engineer", workplaceType="remote")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.jobs_thin", dict(input), options
        )
        return RunResult[LinkedinJobsThinData].model_validate(raw)

    def iter_jobs_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsThinInput],
    ) -> Paginator[LinkedinJobsThinItem, LinkedinJobsThinData]:
        """Iterate LinkedIn Jobs (index) results, following pagination cursors.

        Yields validated `LinkedinJobsThinItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "linkedin.jobs_thin",
            dict(input),
            "items",
            item_model=LinkedinJobsThinItem,
            data_model=LinkedinJobsThinData,
            bare=False,
            options=options,
        )

    def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostInput],
    ) -> RunResult[LinkedinPostData]:
        """LinkedIn Post

        Fetch a single LinkedIn post or article by URL (title, text, author, like
        and comment counts, publish date).

        Price: $0.0008 per request.

        Example:
            res = client.linkedin.post(url="https://www.linkedin.com/posts/stripe_last-week-agent-traffic-surpassed-human-activity-7470882737390940160-2Nxs")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post", dict(input), options
        )
        return RunResult[LinkedinPostData].model_validate(raw)

    def post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostCommentsInput],
    ) -> RunResult[LinkedinPostCommentsData]:
        """LinkedIn Post Comments

        List comments on a LinkedIn post - full text, commenter name/URL/job title,
        timestamps, and engagement.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.post_comments(limit=10, url="https://www.linkedin.com/posts/stripe_philip-kl%C3%B6ckner-in-conversation-with-conor-activity-7477791740645564416-tIbZ")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post_comments", dict(input), options
        )
        return RunResult[LinkedinPostCommentsData].model_validate(raw)

    def post_reactions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostReactionsInput],
    ) -> RunResult[LinkedinPostReactionsData]:
        """LinkedIn Post Reactions

        List who reacted to a LinkedIn post - reactor name, profile URL, job title,
        and reaction type. Lead-gen grade.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.post_reactions(limit=5, url="https://www.linkedin.com/posts/satyanadella_today-were-bringing-skills-to-copilot-for-activity-7475945433668694017--kvG")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post_reactions", dict(input), options
        )
        return RunResult[LinkedinPostReactionsData].model_validate(raw)

    def post_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostTranscriptInput],
    ) -> RunResult[LinkedinPostTranscriptData]:
        """LinkedIn Post Transcript

        Get the spoken transcript of a LinkedIn video post by URL.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.post_transcript(url="https://www.linkedin.com/posts/artificial-analysis_gemini-35-flash-is-a-step-forward-for-google-activity-7465082408409870337-4Pm-")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post_transcript", dict(input), options
        )
        return RunResult[LinkedinPostTranscriptData].model_validate(raw)

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileInput],
    ) -> RunResult[LinkedinProfileData]:
        """LinkedIn Profile

        Fetch a rich LinkedIn member profile by URL: name, headline, avatar,
        location, connections and followers, current position, and full work
        experience with job titles, descriptions, dates, employment/workplace type,
        and per-role skills, plus education, skills, certifications, honors and
        awards, languages, projects, publications, and verified/premium/open-to-work
        flags.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.profile(url="https://www.linkedin.com/in/patrickcollison")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile", dict(input), options
        )
        return RunResult[LinkedinProfileData].model_validate(raw)

    def profile_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileCommentsInput],
    ) -> RunResult[LinkedinProfileCommentsData]:
        """LinkedIn Profile Comments

        List the comments a LinkedIn member has left on other people's posts - the
        comment text, its permalink and timestamp, plus the post it was left on and
        that post's author and engagement.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.profile_comments(limit=10, url="https://www.linkedin.com/in/jeffweiner08")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_comments", dict(input), options
        )
        return RunResult[LinkedinProfileCommentsData].model_validate(raw)

    def profile_posts_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsFullInput],
    ) -> RunResult[LinkedinProfilePostsFullData]:
        """LinkedIn Profile Posts (full)

        Fetch recent public LinkedIn profile posts with enriched author, engagement,
        article, newsletter, media, annotation, repost, and social activity details.

        Price: $0.005 per request.

        Example:
            res = client.linkedin.profile_posts_full(limit=10, url="https://www.linkedin.com/in/williamhgates/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_posts_full", dict(input), options
        )
        return RunResult[LinkedinProfilePostsFullData].model_validate(raw)

    def iter_profile_posts_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsFullInput],
    ) -> Paginator[LinkedinProfilePostsFullItem, LinkedinProfilePostsFullData]:
        """Iterate LinkedIn Profile Posts (full) results, following pagination cursors.

        Yields validated `LinkedinProfilePostsFullItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "linkedin.profile_posts_full",
            dict(input),
            "items",
            item_model=LinkedinProfilePostsFullItem,
            data_model=LinkedinProfilePostsFullData,
            bare=False,
            options=options,
        )

    def profile_posts_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsThinInput],
    ) -> RunResult[LinkedinProfilePostsThinData]:
        """LinkedIn Profile Posts (basic)

        Fetch recent public LinkedIn profile posts with portable identity, author,
        engagement, article, image, video, and repost fields.

        Price: $0.005 per request.

        Example:
            res = client.linkedin.profile_posts_thin(limit=10, url="https://www.linkedin.com/in/williamhgates/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_posts_thin", dict(input), options
        )
        return RunResult[LinkedinProfilePostsThinData].model_validate(raw)

    def iter_profile_posts_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsThinInput],
    ) -> Paginator[LinkedinProfilePostsThinItem, LinkedinProfilePostsThinData]:
        """Iterate LinkedIn Profile Posts (basic) results, following pagination cursors.

        Yields validated `LinkedinProfilePostsThinItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "linkedin.profile_posts_thin",
            dict(input),
            "items",
            item_model=LinkedinProfilePostsThinItem,
            data_model=LinkedinProfilePostsThinData,
            bare=False,
            options=options,
        )

    def profile_reactions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileReactionsInput],
    ) -> RunResult[LinkedinProfileReactionsData]:
        """LinkedIn Profile Reactions

        List the posts a LinkedIn member has reacted to - the reaction, its
        timestamp, and the full post it was made on with author and engagement.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.profile_reactions(limit=10, url="https://www.linkedin.com/in/williamhgates")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_reactions", dict(input), options
        )
        return RunResult[LinkedinProfileReactionsData].model_validate(raw)

    def profile_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileThinInput],
    ) -> RunResult[LinkedinProfileThinData]:
        """LinkedIn Profile (basic)

        Lightweight profile: name, avatar, location, followers, public id, current
        company, and a basic experience/education list (company + dates; job titles,
        the current-role flag and the connections label only where the source and
        the profile show them; no descriptions or skills; past companies may be
        redacted). For full experience detail, skills, certifications, and verified
        flags use linkedin.profile.

        Price: $0.0008 per request.

        Example:
            res = client.linkedin.profile_thin(url="https://www.linkedin.com/in/williamhgates")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_thin", dict(input), options
        )
        return RunResult[LinkedinProfileThinData].model_validate(raw)

    def search_companies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchCompaniesInput],
    ) -> RunResult[LinkedinSearchCompaniesData]:
        """LinkedIn Company Search

        Search LinkedIn companies by keyword with optional location filtering,
        returning normalized company records.

        Price: $0.005 per request.

        Example:
            res = client.linkedin.search_companies(limit=3, query="fintech")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_companies", dict(input), options
        )
        return RunResult[LinkedinSearchCompaniesData].model_validate(raw)

    def search_groups(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchGroupsInput],
    ) -> RunResult[LinkedinSearchGroupsData]:
        """LinkedIn Group Search

        Search LinkedIn groups by keyword, 10 per page: group name, URL, member
        count, summary, and logo.

        Price: $0.0013 per request.

        Example:
            res = client.linkedin.search_groups(query="python")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_groups", dict(input), options
        )
        return RunResult[LinkedinSearchGroupsData].model_validate(raw)

    def search_leads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchLeadsInput],
    ) -> RunResult[LinkedinSearchLeadsData]:
        """LinkedIn Sales Navigator Lead Search

        LinkedIn lead search with Sales Navigator's search and filters: one call
        returns a page of up to 25 people matching a keyword and Sales Navigator
        lead filters (location, job title, current and past company, school,
        seniority, function, company size, and more), or the results of a Sales
        Navigator lead-search URL you built yourself. Each lead comes with name,
        current positions, location, summary, and photo, and its url opens the
        profile and can be passed to linkedin.profile for the full record. For full
        profiles in one call use linkedin.search_profiles.

        Price: $0.07 per request.

        Example:
            res = client.linkedin.search_leads(currentCompanies=["Google"], query="engineer")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_leads", dict(input), options
        )
        return RunResult[LinkedinSearchLeadsData].model_validate(raw)

    def search_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchPostsInput],
    ) -> RunResult[LinkedinSearchPostsData]:
        """LinkedIn Post Search

        Search public LinkedIn posts by keyword (text, link, publish date). Results
        come from search-engine matches over public LinkedIn posts and work best
        with English keywords.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.search_posts(datePosted="last-week", query="hiring")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_posts", dict(input), options
        )
        return RunResult[LinkedinSearchPostsData].model_validate(raw)

    def iter_search_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchPostsInput],
    ) -> Paginator[LinkedinSearchPostsPost, LinkedinSearchPostsData]:
        """Iterate LinkedIn Post Search results, following pagination cursors.

        Yields validated `LinkedinSearchPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "linkedin.search_posts",
            dict(input),
            "posts",
            item_model=LinkedinSearchPostsPost,
            data_model=LinkedinSearchPostsData,
            bare=False,
            options=options,
        )

    def search_posts_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchPostsFullInput],
    ) -> RunResult[LinkedinSearchPostsFullData]:
        """LinkedIn Post Search (full)

        Search public LinkedIn posts with rich author, engagement, attachment, and
        poll details.

        Price: $0.004 per request.

        Example:
            res = client.linkedin.search_posts_full(datePosted="last-week", limit=10, query="artificial intelligence", sort="relevance")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_posts_full", dict(input), options
        )
        return RunResult[LinkedinSearchPostsFullData].model_validate(raw)

    def search_profiles(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesInput],
    ) -> RunResult[LinkedinSearchProfilesData]:
        """LinkedIn Profile Search

        Search LinkedIn profiles by keyword with optional location and job-title
        filters. Each match returns a full profile record: name, headline, location,
        current position, work experience, education, and skills, plus the profile
        URL, handle, and id. For a cheaper name/headline/URL-only search use
        linkedin.search_profiles_thin; add emails with
        linkedin.search_profiles_email.

        Price: $0.088 per request plus $0.0044 per result (maximum $0.198).

        Example:
            res = client.linkedin.search_profiles(currentCompanies=["Google"], limit=3, query="engineer")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_profiles", dict(input), options
        )
        return RunResult[LinkedinSearchProfilesData].model_validate(raw)

    def search_profiles_email(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesEmailInput],
    ) -> RunResult[LinkedinSearchProfilesEmailData]:
        """LinkedIn Profile Search + Email

        People search returning a full profile AND a verified work email for each
        hit. Search LinkedIn profiles by keyword with optional location and
        job-title filters; each match returns the full profile record (name,
        headline, location, current position, work experience, education, and
        skills, plus the profile URL, handle, and id) together with an emails array
        carrying the discovered work email and its deliverability. Email discovery
        is best effort and needs the profile to expose a resolvable company domain,
        so on a broad search many matches return an empty emails array while still
        billing the email rate. If you already have names and company domains,
        email.find, email_finding.icypeas, and email_finding.dropleads resolve
        addresses directly for less, and linkedin.email enriches a single known
        profile URL. For a full profile without email use linkedin.search_profiles;
        for a cheaper name/headline/URL-only search use
        linkedin.search_profiles_thin.

        Price: $0.088 per request plus $0.0099 per result (maximum $0.336).

        Example:
            res = client.linkedin.search_profiles_email(companyHeadcount=["B"], limit=5, query="founder")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_profiles_email", dict(input), options
        )
        return RunResult[LinkedinSearchProfilesEmailData].model_validate(raw)

    def search_profiles_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesThinInput],
    ) -> RunResult[LinkedinSearchProfilesThinData]:
        """LinkedIn Profile Search (basic)

        Cheap people search: name/handle, headline, VANITY profile URL, location. No
        full profile or email - for full profiles per hit use
        linkedin.search_profiles, add emails with linkedin.search_profiles_email.

        Price: $0.036 per request.

        Example:
            res = client.linkedin.search_profiles_thin(query="recruiter")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_profiles_thin", dict(input), options
        )
        return RunResult[LinkedinSearchProfilesThinData].model_validate(raw)

    def iter_search_profiles_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesThinInput],
    ) -> Paginator[LinkedinSearchProfilesThinItem, LinkedinSearchProfilesThinData]:
        """Iterate LinkedIn Profile Search (basic) results, following pagination cursors.

        Yields validated `LinkedinSearchProfilesThinItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "linkedin.search_profiles_thin",
            dict(input),
            "items",
            item_model=LinkedinSearchProfilesThinItem,
            data_model=LinkedinSearchProfilesThinData,
            bare=False,
            options=options,
        )

    def search_services(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchServicesInput],
    ) -> RunResult[LinkedinSearchServicesData]:
        """LinkedIn Service Provider Search

        Find freelancers and service providers on LinkedIn by the service they offer
        (e.g. 'Web Development'), optionally in a location. One call returns a page
        of up to 10 people, each with name, headline, location, about text, photo,
        profile URL, service page URL, and the list of services they offer. The
        profile URL can be passed to linkedin.profile for the full record.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.search_services(location="Australia", query="Web Development")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_services", dict(input), options
        )
        return RunResult[LinkedinSearchServicesData].model_validate(raw)


class AsyncLinkedinNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ad(
        self, *, options: RequestOptions | None = None, **input: Unpack[LinkedinAdInput]
    ) -> RunResult[LinkedinAdData]:
        """LinkedIn Ad Details

        Look up a single LinkedIn Ad Library ad by URL and get the advertiser,
        headline, creative text, format, CTA, targeting, run dates, and impressions
        as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.ad(url="https://www.linkedin.com/ad-library/detail/1487405616")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.ad", dict(input), options
        )
        return RunResult[LinkedinAdData].model_validate(raw)

    async def ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinAdsInput],
    ) -> RunResult[LinkedinAdsData]:
        """LinkedIn Ads Library

        Search the LinkedIn Ad Library by search URL and list the matching ads
        (advertiser, creative text, format).

        Price: $0.00006 per request plus $0.00165 per result (maximum $0.0331).

        Example:
            res = client.linkedin.ads(limit=3, url="https://www.linkedin.com/company/stripe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.ads", dict(input), options
        )
        return RunResult[LinkedinAdsData].model_validate(raw)

    async def ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinAdsSearchInput],
    ) -> RunResult[LinkedinAdsSearchData]:
        """LinkedIn Ad Search

        Search the LinkedIn Ad Library by company or keyword and list matching ads
        (advertiser, headline, creative text, format, CTA, and run dates) with
        pagination.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.ads_search(company="microsoft")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.ads_search", dict(input), options
        )
        return RunResult[LinkedinAdsSearchData].model_validate(raw)

    async def article(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinArticleInput],
    ) -> RunResult[LinkedinArticleData]:
        """LinkedIn Article

        Read a public LinkedIn article or newsletter issue by URL, including its
        full body text, author, publication time, and engagement counts.

        Price: $0.00569 per request plus $0 per result (maximum $0.00569).

        Example:
            res = client.linkedin.article(url="https://www.linkedin.com/pulse/artificial-intelligence-primer-stephen-dover")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.article", dict(input), options
        )
        return RunResult[LinkedinArticleData].model_validate(raw)

    async def comment_reactions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCommentReactionsInput],
    ) -> RunResult[LinkedinCommentReactionsData]:
        """LinkedIn Comment Reactions

        List who reacted to a comment on a LinkedIn post - reactor name, profile
        URL, job title, and reaction type, 100 per page.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.comment_reactions(url="https://www.linkedin.com/feed/update/urn:li:activity:7510715600319467520?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7510715600319467520%2C7510768837462745088%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287510768837462745088%2Curn%3Ali%3Aactivity%3A7510715600319467520%29")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.comment_reactions", dict(input), options
        )
        return RunResult[LinkedinCommentReactionsData].model_validate(raw)

    async def comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCommentRepliesInput],
    ) -> RunResult[LinkedinCommentRepliesData]:
        """LinkedIn Comment Replies

        List up to the 10 newest replies to a comment on a LinkedIn post - reply
        text, replier name/URL/job title, timestamps, and likes.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.comment_replies(url="https://www.linkedin.com/feed/update/urn:li:activity:7510715600319467520?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7510715600319467520%2C7510749329649725442%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287510749329649725442%2Curn%3Ali%3Aactivity%3A7510715600319467520%29")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.comment_replies", dict(input), options
        )
        return RunResult[LinkedinCommentRepliesData].model_validate(raw)

    async def company(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyInput],
    ) -> RunResult[LinkedinCompanyData]:
        """LinkedIn Company

        Fetch a full LinkedIn company page by URL: name, description, industry,
        employee count and range, follower count, founded year, headquarters and
        office locations, funding data, tagline, logo, website, and specialities.

        Price: $0.0011 per request.

        Example:
            res = client.linkedin.company(url="https://www.linkedin.com/company/stripe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company", dict(input), options
        )
        return RunResult[LinkedinCompanyData].model_validate(raw)

    async def company_employees(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyEmployeesInput],
    ) -> RunResult[LinkedinCompanyEmployeesData]:
        """LinkedIn Company Employees

        List the employees of a LinkedIn company by name or company URL, with
        optional job-title filtering.

        Price: $0.006 per request.

        Example:
            res = client.linkedin.company_employees(company="stripe", limit=3)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_employees", dict(input), options
        )
        return RunResult[LinkedinCompanyEmployeesData].model_validate(raw)

    async def company_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyPostsInput],
    ) -> RunResult[LinkedinCompanyPostsData]:
        """LinkedIn Company Posts

        List a LinkedIn company page's recent posts by URL: full text, canonical
        link, publish date, author, engagement counts with a per-reaction breakdown,
        and attached media.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.company_posts(limit=10, url="https://www.linkedin.com/company/stripe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_posts", dict(input), options
        )
        return RunResult[LinkedinCompanyPostsData].model_validate(raw)

    async def company_posts_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyPostsThinInput],
    ) -> RunResult[LinkedinCompanyPostsThinData]:
        """LinkedIn Company Posts (basic)

        Post text and link only. No engagement counts, author details, media, or
        reaction breakdown - for those use linkedin.company_posts.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.company_posts_thin(url="https://www.linkedin.com/company/stripe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_posts_thin", dict(input), options
        )
        return RunResult[LinkedinCompanyPostsThinData].model_validate(raw)

    async def company_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinCompanyThinInput],
    ) -> RunResult[LinkedinCompanyThinData]:
        """LinkedIn Company (basic)

        Basic company: name, description, employee count, industry, logo, website,
        tagline. No follower count, founded year, office locations, or funding data
        - for those use linkedin.company.

        Price: $0.001 per request.

        Example:
            res = client.linkedin.company_thin(url="https://www.linkedin.com/company/stripe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.company_thin", dict(input), options
        )
        return RunResult[LinkedinCompanyThinData].model_validate(raw)

    async def email(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinEmailInput],
    ) -> RunResult[LinkedinEmailData]:
        """LinkedIn Email Finder

        Find the deliverability-validated work email behind a LinkedIn profile URL
        or public ID. Returns each discovered email with its deliverability,
        validation status, and quality score, plus the person's name and headline.

        Price: $0.011 per request plus $0 per result (maximum $0.011).

        Example:
            res = client.linkedin.email(profileUrl="https://www.linkedin.com/in/satyanadella")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.email", dict(input), options
        )
        return RunResult[LinkedinEmailData].model_validate(raw)

    async def group(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinGroupInput],
    ) -> RunResult[LinkedinGroupData]:
        """LinkedIn Group

        Fetch one LinkedIn group by URL or id: name, description, rules, member
        count, logo and cover image, creation date, visibility and join settings,
        and its admins.

        Price: $0.0013 per request.

        Example:
            res = client.linkedin.group(url="https://www.linkedin.com/groups/1898033")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.group", dict(input), options
        )
        return RunResult[LinkedinGroupData].model_validate(raw)

    async def group_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinGroupPostsInput],
    ) -> RunResult[LinkedinGroupPostsData]:
        """LinkedIn Group Posts

        List the posts in a LinkedIn group by group URL, newest first: full text,
        canonical link, publish date, author, engagement counts with a per-reaction
        breakdown, and attached media. One call returns a page of about 100 posts;
        pass page to go further back.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.group_posts(url="https://www.linkedin.com/groups/1898033")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.group_posts", dict(input), options
        )
        return RunResult[LinkedinGroupPostsData].model_validate(raw)

    async def job(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobInput],
    ) -> RunResult[LinkedinJobData]:
        """LinkedIn Job

        Fetch one LinkedIn job posting by URL: title, full description, location,
        salary when disclosed, applicant count, employment and workplace type,
        seniority, benefits, industries, apply links, posting and expiry dates, the
        hiring team, the applicant tracking system behind it, and the hiring company
        with its size, follower count, website and description.

        Price: $0.0015 per request.

        Example:
            res = client.linkedin.job(url="https://www.linkedin.com/jobs/view/4431721875/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.job", dict(input), options
        )
        return RunResult[LinkedinJobData].model_validate(raw)

    async def jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsInput],
    ) -> RunResult[LinkedinJobsData]:
        """LinkedIn Jobs

        Search LinkedIn job listings by title and location - full records with
        description, salary, applicant count, seniority, company details, and
        benefits. Up to 25 jobs per request.

        Price: $0.0195 per request.

        Example:
            res = client.linkedin.jobs(limit=3, location="United States", query="software engineer", workplaceType="remote")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.jobs", dict(input), options
        )
        return RunResult[LinkedinJobsData].model_validate(raw)

    def iter_jobs(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsInput],
    ) -> AsyncPaginator[LinkedinJobsItem, LinkedinJobsData]:
        """Iterate LinkedIn Jobs results, following pagination cursors.

        Yields validated `LinkedinJobsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "linkedin.jobs",
            dict(input),
            "items",
            item_model=LinkedinJobsItem,
            data_model=LinkedinJobsData,
            bare=False,
            options=options,
        )

    async def jobs_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsThinInput],
    ) -> RunResult[LinkedinJobsThinData]:
        """LinkedIn Jobs (index)

        Cheap job index: title, company, location, posted date, URL. No description,
        salary, applicant counts, or seniority - for those use linkedin.jobs.

        Price: $0.00066 per request.

        Example:
            res = client.linkedin.jobs_thin(limit=3, location="United States", query="software engineer", workplaceType="remote")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.jobs_thin", dict(input), options
        )
        return RunResult[LinkedinJobsThinData].model_validate(raw)

    def iter_jobs_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinJobsThinInput],
    ) -> AsyncPaginator[LinkedinJobsThinItem, LinkedinJobsThinData]:
        """Iterate LinkedIn Jobs (index) results, following pagination cursors.

        Yields validated `LinkedinJobsThinItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "linkedin.jobs_thin",
            dict(input),
            "items",
            item_model=LinkedinJobsThinItem,
            data_model=LinkedinJobsThinData,
            bare=False,
            options=options,
        )

    async def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostInput],
    ) -> RunResult[LinkedinPostData]:
        """LinkedIn Post

        Fetch a single LinkedIn post or article by URL (title, text, author, like
        and comment counts, publish date).

        Price: $0.0008 per request.

        Example:
            res = client.linkedin.post(url="https://www.linkedin.com/posts/stripe_last-week-agent-traffic-surpassed-human-activity-7470882737390940160-2Nxs")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post", dict(input), options
        )
        return RunResult[LinkedinPostData].model_validate(raw)

    async def post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostCommentsInput],
    ) -> RunResult[LinkedinPostCommentsData]:
        """LinkedIn Post Comments

        List comments on a LinkedIn post - full text, commenter name/URL/job title,
        timestamps, and engagement.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.post_comments(limit=10, url="https://www.linkedin.com/posts/stripe_philip-kl%C3%B6ckner-in-conversation-with-conor-activity-7477791740645564416-tIbZ")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post_comments", dict(input), options
        )
        return RunResult[LinkedinPostCommentsData].model_validate(raw)

    async def post_reactions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostReactionsInput],
    ) -> RunResult[LinkedinPostReactionsData]:
        """LinkedIn Post Reactions

        List who reacted to a LinkedIn post - reactor name, profile URL, job title,
        and reaction type. Lead-gen grade.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.post_reactions(limit=5, url="https://www.linkedin.com/posts/satyanadella_today-were-bringing-skills-to-copilot-for-activity-7475945433668694017--kvG")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post_reactions", dict(input), options
        )
        return RunResult[LinkedinPostReactionsData].model_validate(raw)

    async def post_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinPostTranscriptInput],
    ) -> RunResult[LinkedinPostTranscriptData]:
        """LinkedIn Post Transcript

        Get the spoken transcript of a LinkedIn video post by URL.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.post_transcript(url="https://www.linkedin.com/posts/artificial-analysis_gemini-35-flash-is-a-step-forward-for-google-activity-7465082408409870337-4Pm-")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.post_transcript", dict(input), options
        )
        return RunResult[LinkedinPostTranscriptData].model_validate(raw)

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileInput],
    ) -> RunResult[LinkedinProfileData]:
        """LinkedIn Profile

        Fetch a rich LinkedIn member profile by URL: name, headline, avatar,
        location, connections and followers, current position, and full work
        experience with job titles, descriptions, dates, employment/workplace type,
        and per-role skills, plus education, skills, certifications, honors and
        awards, languages, projects, publications, and verified/premium/open-to-work
        flags.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.profile(url="https://www.linkedin.com/in/patrickcollison")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile", dict(input), options
        )
        return RunResult[LinkedinProfileData].model_validate(raw)

    async def profile_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileCommentsInput],
    ) -> RunResult[LinkedinProfileCommentsData]:
        """LinkedIn Profile Comments

        List the comments a LinkedIn member has left on other people's posts - the
        comment text, its permalink and timestamp, plus the post it was left on and
        that post's author and engagement.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.profile_comments(limit=10, url="https://www.linkedin.com/in/jeffweiner08")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_comments", dict(input), options
        )
        return RunResult[LinkedinProfileCommentsData].model_validate(raw)

    async def profile_posts_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsFullInput],
    ) -> RunResult[LinkedinProfilePostsFullData]:
        """LinkedIn Profile Posts (full)

        Fetch recent public LinkedIn profile posts with enriched author, engagement,
        article, newsletter, media, annotation, repost, and social activity details.

        Price: $0.005 per request.

        Example:
            res = client.linkedin.profile_posts_full(limit=10, url="https://www.linkedin.com/in/williamhgates/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_posts_full", dict(input), options
        )
        return RunResult[LinkedinProfilePostsFullData].model_validate(raw)

    def iter_profile_posts_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsFullInput],
    ) -> AsyncPaginator[LinkedinProfilePostsFullItem, LinkedinProfilePostsFullData]:
        """Iterate LinkedIn Profile Posts (full) results, following pagination cursors.

        Yields validated `LinkedinProfilePostsFullItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "linkedin.profile_posts_full",
            dict(input),
            "items",
            item_model=LinkedinProfilePostsFullItem,
            data_model=LinkedinProfilePostsFullData,
            bare=False,
            options=options,
        )

    async def profile_posts_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsThinInput],
    ) -> RunResult[LinkedinProfilePostsThinData]:
        """LinkedIn Profile Posts (basic)

        Fetch recent public LinkedIn profile posts with portable identity, author,
        engagement, article, image, video, and repost fields.

        Price: $0.005 per request.

        Example:
            res = client.linkedin.profile_posts_thin(limit=10, url="https://www.linkedin.com/in/williamhgates/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_posts_thin", dict(input), options
        )
        return RunResult[LinkedinProfilePostsThinData].model_validate(raw)

    def iter_profile_posts_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfilePostsThinInput],
    ) -> AsyncPaginator[LinkedinProfilePostsThinItem, LinkedinProfilePostsThinData]:
        """Iterate LinkedIn Profile Posts (basic) results, following pagination cursors.

        Yields validated `LinkedinProfilePostsThinItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "linkedin.profile_posts_thin",
            dict(input),
            "items",
            item_model=LinkedinProfilePostsThinItem,
            data_model=LinkedinProfilePostsThinData,
            bare=False,
            options=options,
        )

    async def profile_reactions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileReactionsInput],
    ) -> RunResult[LinkedinProfileReactionsData]:
        """LinkedIn Profile Reactions

        List the posts a LinkedIn member has reacted to - the reaction, its
        timestamp, and the full post it was made on with author and engagement.

        Price: $0.0029 per request.

        Example:
            res = client.linkedin.profile_reactions(limit=10, url="https://www.linkedin.com/in/williamhgates")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_reactions", dict(input), options
        )
        return RunResult[LinkedinProfileReactionsData].model_validate(raw)

    async def profile_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinProfileThinInput],
    ) -> RunResult[LinkedinProfileThinData]:
        """LinkedIn Profile (basic)

        Lightweight profile: name, avatar, location, followers, public id, current
        company, and a basic experience/education list (company + dates; job titles,
        the current-role flag and the connections label only where the source and
        the profile show them; no descriptions or skills; past companies may be
        redacted). For full experience detail, skills, certifications, and verified
        flags use linkedin.profile.

        Price: $0.0008 per request.

        Example:
            res = client.linkedin.profile_thin(url="https://www.linkedin.com/in/williamhgates")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.profile_thin", dict(input), options
        )
        return RunResult[LinkedinProfileThinData].model_validate(raw)

    async def search_companies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchCompaniesInput],
    ) -> RunResult[LinkedinSearchCompaniesData]:
        """LinkedIn Company Search

        Search LinkedIn companies by keyword with optional location filtering,
        returning normalized company records.

        Price: $0.005 per request.

        Example:
            res = client.linkedin.search_companies(limit=3, query="fintech")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_companies", dict(input), options
        )
        return RunResult[LinkedinSearchCompaniesData].model_validate(raw)

    async def search_groups(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchGroupsInput],
    ) -> RunResult[LinkedinSearchGroupsData]:
        """LinkedIn Group Search

        Search LinkedIn groups by keyword, 10 per page: group name, URL, member
        count, summary, and logo.

        Price: $0.0013 per request.

        Example:
            res = client.linkedin.search_groups(query="python")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_groups", dict(input), options
        )
        return RunResult[LinkedinSearchGroupsData].model_validate(raw)

    async def search_leads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchLeadsInput],
    ) -> RunResult[LinkedinSearchLeadsData]:
        """LinkedIn Sales Navigator Lead Search

        LinkedIn lead search with Sales Navigator's search and filters: one call
        returns a page of up to 25 people matching a keyword and Sales Navigator
        lead filters (location, job title, current and past company, school,
        seniority, function, company size, and more), or the results of a Sales
        Navigator lead-search URL you built yourself. Each lead comes with name,
        current positions, location, summary, and photo, and its url opens the
        profile and can be passed to linkedin.profile for the full record. For full
        profiles in one call use linkedin.search_profiles.

        Price: $0.07 per request.

        Example:
            res = client.linkedin.search_leads(currentCompanies=["Google"], query="engineer")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_leads", dict(input), options
        )
        return RunResult[LinkedinSearchLeadsData].model_validate(raw)

    async def search_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchPostsInput],
    ) -> RunResult[LinkedinSearchPostsData]:
        """LinkedIn Post Search

        Search public LinkedIn posts by keyword (text, link, publish date). Results
        come from search-engine matches over public LinkedIn posts and work best
        with English keywords.

        Price: $0.0012 per request.

        Example:
            res = client.linkedin.search_posts(datePosted="last-week", query="hiring")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_posts", dict(input), options
        )
        return RunResult[LinkedinSearchPostsData].model_validate(raw)

    def iter_search_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchPostsInput],
    ) -> AsyncPaginator[LinkedinSearchPostsPost, LinkedinSearchPostsData]:
        """Iterate LinkedIn Post Search results, following pagination cursors.

        Yields validated `LinkedinSearchPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "linkedin.search_posts",
            dict(input),
            "posts",
            item_model=LinkedinSearchPostsPost,
            data_model=LinkedinSearchPostsData,
            bare=False,
            options=options,
        )

    async def search_posts_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchPostsFullInput],
    ) -> RunResult[LinkedinSearchPostsFullData]:
        """LinkedIn Post Search (full)

        Search public LinkedIn posts with rich author, engagement, attachment, and
        poll details.

        Price: $0.004 per request.

        Example:
            res = client.linkedin.search_posts_full(datePosted="last-week", limit=10, query="artificial intelligence", sort="relevance")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_posts_full", dict(input), options
        )
        return RunResult[LinkedinSearchPostsFullData].model_validate(raw)

    async def search_profiles(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesInput],
    ) -> RunResult[LinkedinSearchProfilesData]:
        """LinkedIn Profile Search

        Search LinkedIn profiles by keyword with optional location and job-title
        filters. Each match returns a full profile record: name, headline, location,
        current position, work experience, education, and skills, plus the profile
        URL, handle, and id. For a cheaper name/headline/URL-only search use
        linkedin.search_profiles_thin; add emails with
        linkedin.search_profiles_email.

        Price: $0.088 per request plus $0.0044 per result (maximum $0.198).

        Example:
            res = client.linkedin.search_profiles(currentCompanies=["Google"], limit=3, query="engineer")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_profiles", dict(input), options
        )
        return RunResult[LinkedinSearchProfilesData].model_validate(raw)

    async def search_profiles_email(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesEmailInput],
    ) -> RunResult[LinkedinSearchProfilesEmailData]:
        """LinkedIn Profile Search + Email

        People search returning a full profile AND a verified work email for each
        hit. Search LinkedIn profiles by keyword with optional location and
        job-title filters; each match returns the full profile record (name,
        headline, location, current position, work experience, education, and
        skills, plus the profile URL, handle, and id) together with an emails array
        carrying the discovered work email and its deliverability. Email discovery
        is best effort and needs the profile to expose a resolvable company domain,
        so on a broad search many matches return an empty emails array while still
        billing the email rate. If you already have names and company domains,
        email.find, email_finding.icypeas, and email_finding.dropleads resolve
        addresses directly for less, and linkedin.email enriches a single known
        profile URL. For a full profile without email use linkedin.search_profiles;
        for a cheaper name/headline/URL-only search use
        linkedin.search_profiles_thin.

        Price: $0.088 per request plus $0.0099 per result (maximum $0.336).

        Example:
            res = client.linkedin.search_profiles_email(companyHeadcount=["B"], limit=5, query="founder")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_profiles_email", dict(input), options
        )
        return RunResult[LinkedinSearchProfilesEmailData].model_validate(raw)

    async def search_profiles_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesThinInput],
    ) -> RunResult[LinkedinSearchProfilesThinData]:
        """LinkedIn Profile Search (basic)

        Cheap people search: name/handle, headline, VANITY profile URL, location. No
        full profile or email - for full profiles per hit use
        linkedin.search_profiles, add emails with linkedin.search_profiles_email.

        Price: $0.036 per request.

        Example:
            res = client.linkedin.search_profiles_thin(query="recruiter")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_profiles_thin", dict(input), options
        )
        return RunResult[LinkedinSearchProfilesThinData].model_validate(raw)

    def iter_search_profiles_thin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchProfilesThinInput],
    ) -> AsyncPaginator[LinkedinSearchProfilesThinItem, LinkedinSearchProfilesThinData]:
        """Iterate LinkedIn Profile Search (basic) results, following pagination cursors.

        Yields validated `LinkedinSearchProfilesThinItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "linkedin.search_profiles_thin",
            dict(input),
            "items",
            item_model=LinkedinSearchProfilesThinItem,
            data_model=LinkedinSearchProfilesThinData,
            bare=False,
            options=options,
        )

    async def search_services(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinkedinSearchServicesInput],
    ) -> RunResult[LinkedinSearchServicesData]:
        """LinkedIn Service Provider Search

        Find freelancers and service providers on LinkedIn by the service they offer
        (e.g. 'Web Development'), optionally in a location. One call returns a page
        of up to 10 people, each with name, headline, location, about text, photo,
        profile URL, service page URL, and the list of services they offer. The
        profile URL can be passed to linkedin.profile for the full record.

        Price: $0.0026 per request.

        Example:
            res = client.linkedin.search_services(location="Australia", query="Web Development")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linkedin.search_services", dict(input), options
        )
        return RunResult[LinkedinSearchServicesData].model_validate(raw)
