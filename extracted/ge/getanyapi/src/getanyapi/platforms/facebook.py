# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the facebook platform."""

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


class FacebookAdDetailsInput(TypedDict, total=False):
    """Input for Facebook Ad Details."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """Meta Ad Library ad ID (e.g. "702369045530963"). Provide either id or url."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Meta Ad Library ad URL (e.g. "https://www.facebook.com/ads/library?id=1185617869915074"). Provide either id or url."""


class FacebookAdDetailsFullInput(TypedDict, total=False):
    """Input for Facebook Ad Creative Details."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: Required[str]
    """Meta Ad Library ad ID - the numeric id in an Ad Library URL (e.g. "962050096457659" from https://www.facebook.com/ads/library/?id=962050096457659)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookAdTranscriptInput(TypedDict, total=False):
    """Input for Facebook Ad Transcript."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """Meta Ad Library ad ID (e.g. "1020359190509080"). Provide either id or url."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Meta Ad Library ad URL (e.g. "https://www.facebook.com/ads/library?id=1020359190509080"). Provide either id or url."""


class FacebookAdsSearchInput(TypedDict, total=False):
    """Input for Facebook Ad Search."""

    adType: NotRequired[Literal["all", "political_and_issue_ads"]]
    """Restrict to all ads (default) or only political and issue ads."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Two-letter country code to scope results. Omit for all countries."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor."""
    endDate: NotRequired[str]
    """Filter to ads with impressions on or before this date, in YYYY-MM-DD format."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    mediaType: NotRequired[
        Literal["ALL", "IMAGE", "VIDEO", "MEME", "IMAGE_AND_MEME", "NONE"]
    ]
    """Creative media type filter."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search the Meta Ad Library for (e.g. "protein powder")."""
    requireFields: NotRequired[list[Literal["totalResults"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `totalResults`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an ad that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    searchType: NotRequired[Literal["keyword_unordered", "keyword_exact_phrase"]]
    """Match mode for the query: loose keyword match (keyword_unordered, the default) or exact phrase (keyword_exact_phrase)."""
    sortBy: NotRequired[Literal["impressions", "recent"]]
    """Sort order: impressions (highest first, the default) or recent (most recent)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Filter to ads with impressions on or after this date, in YYYY-MM-DD format."""
    status: NotRequired[Literal["ALL", "ACTIVE", "INACTIVE"]]
    """Ad status filter. Default: ACTIVE."""


class FacebookCommentRepliesInput(TypedDict, total=False):
    """Input for Facebook Comment Replies."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    expansionToken: Required[str]
    """The expansion_token of the comment, from the post comments endpoint."""
    feedbackId: Required[str]
    """The feedback_id of the comment (not the comment id)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookCompanyAdsInput(TypedDict, total=False):
    """Input for Facebook Company Ads."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyName: NotRequired[str]
    """Company name to search (e.g. "nike"). Exact-match and case-sensitive against the Meta Ad Library index; an advertiser with no indexed page returns found:false."""
    country: NotRequired[str]
    """Two-letter country code to scope results. Defaults to all countries."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor."""
    endDate: NotRequired[str]
    """Filter to ads with impressions on or before this date, in YYYY-MM-DD format."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Two-letter language code to filter ads (e.g. "EN", "ES", "FR")."""
    mediaType: NotRequired[
        Literal["ALL", "IMAGE", "VIDEO", "MEME", "IMAGE_AND_MEME", "NONE"]
    ]
    """Creative media type filter."""
    pageId: NotRequired[str]
    """Company's Ad Library page ID. Provide either pageId or companyName."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    sortBy: NotRequired[Literal["impressions", "recent"]]
    """Sort order: impressions (highest first, the default) or recent (most recent)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Filter to ads with impressions on or after this date, in YYYY-MM-DD format."""
    status: NotRequired[Literal["ALL", "ACTIVE", "INACTIVE"]]
    """Ad status filter. Defaults to ACTIVE."""


class FacebookEventDetailsInput(TypedDict, total=False):
    """Input for Facebook Event Details."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """The event's numeric identifier."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """The event's Facebook URL."""


class FacebookEventsInput(TypedDict, total=False):
    """Input for Facebook Events."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response to fetch the next page."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    time: NotRequired[Literal["today", "this_week", "next_week"]]
    """Timeframe filter for the returned events. Defaults to all time."""
    url: Required[str]
    """URL of a city's or place's Facebook Events page (e.g. https://www.facebook.com/events/explore/saint-petersburg-florida/111326725552547)."""


class FacebookEventsSearchInput(TypedDict, total=False):
    """Input for Facebook Events Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The query to search events for."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookFollowersInput(TypedDict, total=False):
    """Input for Facebook Followers."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    followType: NotRequired[str]
    """Which relation to fetch: 'follower' or 'following' (e.g. follower). Default: follower."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). You are billed per result returned, so a lower limit costs less. Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Facebook page or profile URL to list follows for (e.g. https://www.facebook.com/nasa)."""


class FacebookGroupPostsInput(TypedDict, total=False):
    """Input for Facebook Group Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response to fetch the next page."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    sort: NotRequired[
        Literal[
            "TOP_POSTS", "RECENT_ACTIVITY", "CHRONOLOGICAL", "CHRONOLOGICAL_LISTINGS"
        ]
    ]
    """Ordering for the returned posts (e.g. TOP_POSTS)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The URL of a public Facebook group to fetch posts from (e.g. https://www.facebook.com/groups/instantpotcommunity/)."""


class FacebookMarketplaceInput(TypedDict, total=False):
    """Input for Facebook Marketplace."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    availability: NotRequired[Literal["available", "sold", "all"]]
    """Filter by availability: available (default), sold, or all (e.g. sold)."""
    condition: NotRequired[Literal["new", "used_like_new", "used_good", "used_fair"]]
    """Only return listings in this condition (e.g. used_good)."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response to fetch the next page."""
    dateListed: NotRequired[
        Literal["all", "last_24_hours", "last_7_days", "last_30_days"]
    ]
    """Only return listings posted within this window (e.g. last_7_days)."""
    deliveryMethod: NotRequired[Literal["all", "local_pickup", "shipping"]]
    """Only return listings offering this delivery method (e.g. shipping)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lat: Required[str]
    """Latitude of the search location (e.g. '30.2677')."""
    lng: Required[str]
    """Longitude of the search location (e.g. '-97.7475')."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    priceMax: NotRequired[int]
    """Maximum listing price in whole currency units, e.g. 500 for $500. Facebook may mix in a few suggested listings outside the range. Minimum: 0."""
    priceMin: NotRequired[int]
    """Minimum listing price in whole currency units, e.g. 100 for $100. Facebook may mix in a few suggested listings outside the range. Minimum: 0."""
    query: Required[str]
    """Search keyword for Marketplace listings (e.g. 'bike')."""
    sort: NotRequired[
        Literal[
            "suggested",
            "distance_ascend",
            "creation_time_descend",
            "price_ascend",
            "price_descend",
        ]
    ]
    """Sort order for the returned listings (e.g. price_ascend)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookMarketplaceItemInput(TypedDict, total=False):
    """Input for Facebook Marketplace Item."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """Facebook Marketplace item ID."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Facebook Marketplace item URL."""


class FacebookMarketplaceLocationSearchInput(TypedDict, total=False):
    """Input for Facebook Marketplace Location Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Location search query (e.g. a city name)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookPageContactInput(TypedDict, total=False):
    """Input for Facebook Page Contact Info."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Locale code for the returned data (e.g. en-US). Default: en-US."""
    page: Required[str]
    """Facebook Page URL or page ID to look up (e.g. https://www.facebook.com/nasa)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["adStatus", "createdUtc", "followers"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `createdUtc` or `adStatus`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a page that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookPageLookupInput(TypedDict, total=False):
    """Input for Facebook Page Lookup."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of matches to return (1-7, default 7). Facebook's quick search answers a name with at most 7 matches. Range: 1 to 7. Default: 7."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Name to look up, as you would type it into Facebook's search box (e.g. NASA or plumber chicago)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookPhotosInput(TypedDict, total=False):
    """Input for Facebook Page Photos."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response to fetch the next page."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["imageHeight", "imageWidth", "nextPageId"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `imageWidth`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a photo that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """URL of the public Facebook page or profile to fetch photos from (e.g. https://www.facebook.com/Spurs)."""


class FacebookPostInput(TypedDict, total=False):
    """Input for Facebook Post."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "authorVerified",
                "feedbackId",
                "reactions",
                "videoId",
                "videoUrl",
                "views",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `videoId` or `views`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full Facebook post URL."""


class FacebookPostCommentsInput(TypedDict, total=False):
    """Input for Facebook Post Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    feedbackId: NotRequired[str]
    """Facebook feedback id for the post (alternative to url)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["feedbackId", "hasNextPage"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `feedbackId` or `hasNextPage`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a comment that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Full Facebook post URL."""


class FacebookPostTranscriptInput(TypedDict, total=False):
    """Input for Facebook Post Transcript."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The Facebook post or video URL."""


class FacebookProfileInput(TypedDict, total=False):
    """Input for Facebook Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: NotRequired[str]
    """Facebook page handle/username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Full Facebook page URL."""


class FacebookProfileEventsInput(TypedDict, total=False):
    """Input for Facebook Page Events."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The Facebook page link whose events to list, e.g. https://www.facebook.com/brickyardoldtown. Accepted: facebook.com/<name>, /p/<name>-<id>, /pages/<name>/<id>, /pg/<name>, /people/<name>/<id> and profile.php?id=<id>, on facebook.com or fb.com with or without www, m, mbasic, web, business or a language subdomain. Anything after the page, such as a tab, is fine: only the page is read. Any other Facebook link, such as a single event, group, share link, reel, video, hashtag, search or login page, is refused as invalid input, with no charge; facebook.event_details reads one event."""


class FacebookProfilePostsInput(TypedDict, total=False):
    """Input for Facebook Profile Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    pageId: NotRequired[str]
    """Facebook page id."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["shares"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `shares`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Facebook page or profile link, e.g. https://www.facebook.com/nike. Accepted: facebook.com/<name>, /p/<name>-<id>, /pages/<name>/<id>, /pg/<name>, /people/<name>/<id>, profile.php?id=<id>, and share links to a page (/share/<id> or /share/p/<id>), on facebook.com or fb.com with or without www, m, mbasic, web, business or a language subdomain. Anything after the page, such as a tab, is fine. Any other Facebook link, such as a single event, group, reel, video, video or reel share link (/share/v/ or /share/r/), hashtag, search or login page, is refused as invalid input, with no charge; facebook.event_details reads one event and facebook.post reads one post."""


class FacebookProfileReelsInput(TypedDict, total=False):
    """Input for Facebook Profile Reels."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "authorVerified",
                "comments",
                "feedbackId",
                "likes",
                "shares",
                "videoUrl",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `feedbackId` or `authorVerified`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a reel that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full Facebook page/profile URL."""


class FacebookSearchCompaniesInput(TypedDict, total=False):
    """Input for Facebook Company Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search advertiser pages for (e.g. "nike")."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookSearchPagesInput(TypedDict, total=False):
    """Input for Facebook Page Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-10, default 10). You are billed per result returned, so a lower limit costs less. Range: 1 to 10."""
    location: NotRequired[str]
    """Optional free-text location to narrow the search: a city, province, or country (e.g. 'Berlin')."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search Facebook Pages for (e.g. 'coffee roasters')."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class FacebookSearchPostsInput(TypedDict, total=False):
    """Input for Facebook Post Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    endDate: NotRequired[str]
    """Only return posts published on or before this date, format YYYY-MM-DD (e.g. 2024-12-31)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). Range: 1 to 20."""
    location: NotRequired[str]
    """Optional place name; include both city and country for best matches (e.g. 'Paris, France'). Uses Facebook's place filter, which favors posts tagged at that place rather than every post by people who live there, and can still return some posts from elsewhere."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword or phrase to search Facebook posts for (e.g. 'product launch')."""
    requireFields: NotRequired[list[Literal["albumPreview", "imagesCount", "type"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `imagesCount` or `albumPreview`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Only return posts published on or after this date, format YYYY-MM-DD (e.g. 2024-01-01)."""


class FacebookAdDetailsData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active: bool | None = Field(
        default=None, description="Whether the ad is currently running."
    )
    ad_archive_id: str = Field(
        alias="adArchiveId",
        description="Ad Library archive ID (stable identity). Populated whenever the provider has data for the entity.",
    )
    caption: str | None = Field(
        default=None,
        description="Caption line of the ad creative, usually the advertiser's display domain.",
    )
    categories: list[str] | None = Field(
        default=None, description="Ad Library categories the ad is filed under."
    )
    creatives: list[FacebookAdDetailsCreative] | None = Field(
        default=None,
        description="One entry per card of a carousel, dynamic-product, or dynamic-creative ad, in the order Meta returns them, each with its own text and destination. Single-creative ads return an empty array. The same card images and videos also appear in media. Meta CDN media URLs are signed and expire.",
    )
    cta_text: str | None = Field(
        default=None,
        alias="ctaText",
        description="Call-to-action label. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None, description="Spend currency, may be empty."
    )
    display_format: str | None = Field(
        default=None,
        alias="displayFormat",
        description="Ad creative format. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    end_date: int | None = Field(
        default=None, alias="endDate", description="Run end, epoch seconds."
    )
    is_reshared: bool | None = Field(
        default=None,
        alias="isReshared",
        description="Whether the ad creative is a reshare of another post.",
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Description text shown under the ad's link.",
    )
    link_url: str | None = Field(
        default=None,
        alias="linkUrl",
        description="Creative destination URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    media: list[FacebookAdDetailsMedia] | None = Field(
        default=None,
        description="Creative attached to the ad: one element per image, video, or carousel card, in the order the ad presents them. Empty when the ad has none.",
    )
    page_categories: list[str] | None = Field(
        default=None,
        alias="pageCategories",
        description="Categories Facebook lists the advertising page under.",
    )
    page_deleted: bool | None = Field(
        default=None,
        alias="pageDeleted",
        description="Whether the advertising page has been deleted.",
    )
    page_id: str = Field(
        alias="pageId",
        description="Advertiser page ID (stable identity). Populated whenever the provider has data for the entity.",
    )
    page_likes: int | None = Field(
        default=None,
        alias="pageLikes",
        description="Like count of the advertising page.",
    )
    page_name: str | None = Field(
        default=None,
        alias="pageName",
        description="Advertiser page name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    page_profile_picture: str | None = Field(
        default=None,
        alias="pageProfilePicture",
        description="Profile picture of the advertising page. This is the advertiser's identity image, not ad creative.",
    )
    page_url: str | None = Field(
        default=None,
        alias="pageUrl",
        description="Canonical Facebook URL of the advertising page.",
    )
    platforms: list[str] | None = Field(
        default=None,
        description="Publisher platforms the ad runs on. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    source_url: str = Field(
        alias="sourceUrl",
        description="Inspectable Meta Ad Library URL for this ad. Populated whenever the provider has data for the entity.",
    )
    start_date: int | None = Field(
        default=None,
        alias="startDate",
        description="Run start, epoch seconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    text: str | None = Field(
        default=None,
        description="Ad body text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str | None = Field(
        default=None,
        description="Creative title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class FacebookAdDetailsCreative(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    body: str | None = Field(default=None, description="Card body text.")
    caption: str | None = Field(
        default=None,
        description="Card display caption, usually the destination domain.",
    )
    cta_text: str | None = Field(
        default=None,
        alias="ctaText",
        description='Card call-to-action label (e.g. "Shop Now").',
    )
    cta_type: str | None = Field(
        default=None,
        alias="ctaType",
        description='Card call-to-action type (e.g. "SHOP_NOW").',
    )
    image: str | None = Field(
        default=None,
        description="Card image URL. For a video card this is the poster frame.",
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Card secondary description line.",
    )
    link_url: str | None = Field(
        default=None, alias="linkUrl", description="Card destination URL."
    )
    title: str | None = Field(default=None, description="Card headline.")
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Card video file URL (HD when supplied, otherwise SD). Present only on video cards.",
    )


class FacebookAdDetailsMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL. Present only for video and gif items.",
    )
    width: int | None = Field(
        default=None,
        description="Pixel width of the media item, when the lane reports it.",
    )


class FacebookAdDetailsFullData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active: bool | None = Field(
        default=None, description="Whether the ad is currently running."
    )
    ad_archive_id: str = Field(
        alias="adArchiveId",
        description="Ad Library archive ID (stable identity). Populated whenever the provider has data for the entity.",
    )
    body: str | None = Field(
        default=None,
        description="Ad body text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    caption: str | None = Field(
        default=None, description="Display caption, usually the destination domain."
    )
    categories: list[str] | None = Field(
        default=None, description="Ad Library categories the ad is filed under."
    )
    creatives: list[FacebookAdDetailsFullCreative] | None = Field(
        default=None,
        description="One entry per creative variant of a carousel or dynamic ad, in the order Meta returns them. Single-creative ads return an empty array and carry their media in images/videos. Meta CDN media URLs are signed and expire, so fetch what you need at read time.",
    )
    cta_text: str | None = Field(
        default=None,
        alias="ctaText",
        description='Call-to-action label (e.g. "Shop now").',
    )
    cta_type: str | None = Field(
        default=None,
        alias="ctaType",
        description='Call-to-action type (e.g. "SHOP_NOW").',
    )
    display_format: str | None = Field(
        default=None,
        alias="displayFormat",
        description='Ad creative format (e.g. "DPA", "VIDEO", "IMAGE"). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    ended_utc: float | None = Field(
        default=None,
        alias="endedUtc",
        description="Run end, or last-seen date while the ad is still running. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    images: list[FacebookAdDetailsFullImage] | None = Field(
        default=None,
        description="Standalone creative images for a single-image ad. Meta CDN media URLs are signed and expire.",
    )
    is_reshared: bool | None = Field(
        default=None,
        alias="isReshared",
        description="Whether the ad creative is a reshare of another post.",
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Secondary link description line.",
    )
    link_url: str | None = Field(
        default=None, alias="linkUrl", description="Creative destination URL."
    )
    page_categories: list[str] | None = Field(
        default=None,
        alias="pageCategories",
        description="Categories Facebook lists the advertising page under.",
    )
    page_deleted: bool | None = Field(
        default=None,
        alias="pageDeleted",
        description="Whether the advertising page has been deleted.",
    )
    page_id: str = Field(
        alias="pageId",
        description="Advertiser page ID (stable identity). Populated whenever the provider has data for the entity.",
    )
    page_image: str | None = Field(
        default=None,
        alias="pageImage",
        description="Advertiser page profile picture URL. Meta CDN URLs are signed and expire.",
    )
    page_likes: int | None = Field(
        default=None,
        alias="pageLikes",
        description="Like count of the advertising page.",
    )
    page_name: str | None = Field(
        default=None,
        alias="pageName",
        description="Advertiser page name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    page_url: str | None = Field(
        default=None, alias="pageUrl", description="Advertiser page URL."
    )
    platforms: list[str] | None = Field(
        default=None, description="Publisher platforms the ad runs on."
    )
    source_url: str = Field(
        alias="sourceUrl",
        description="Inspectable Meta Ad Library URL for this ad. Populated whenever the provider has data for the entity.",
    )
    started_utc: float | None = Field(
        default=None,
        alias="startedUtc",
        description="Run start. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str | None = Field(
        default=None,
        description='Creative headline. Dynamic-product ads return a template such as "{{product.name}}".',
    )
    videos: list[FacebookAdDetailsFullVideo] | None = Field(
        default=None,
        description="Standalone creative videos for a single-video ad. Meta CDN media URLs are signed and expire.",
    )


class FacebookAdDetailsFullCreative(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    body: str | None = Field(default=None, description="Variant body text.")
    caption: str | None = Field(default=None, description="Variant display caption.")
    cta_text: str | None = Field(
        default=None, alias="ctaText", description="Variant call-to-action label."
    )
    cta_type: str | None = Field(
        default=None, alias="ctaType", description="Variant call-to-action type."
    )
    image: str | None = Field(default=None, description="Original creative image URL.")
    image_resized: str | None = Field(
        default=None, alias="imageResized", description="Resized creative image URL."
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Variant secondary description.",
    )
    link_url: str | None = Field(
        default=None, alias="linkUrl", description="Variant destination URL."
    )
    title: str | None = Field(default=None, description="Variant headline.")
    video_preview_image: str | None = Field(
        default=None,
        alias="videoPreviewImage",
        description="Poster frame for the creative video.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Creative video URL (HD when supplied, otherwise SD).",
    )


class FacebookAdDetailsFullImage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    image: str | None = Field(default=None, description="Original creative image URL.")
    image_resized: str | None = Field(
        default=None, alias="imageResized", description="Resized creative image URL."
    )


class FacebookAdDetailsFullVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    video_preview_image: str | None = Field(
        default=None,
        alias="videoPreviewImage",
        description="Poster frame for the creative video.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Creative video URL (HD when supplied, otherwise SD).",
    )


class FacebookAdTranscriptData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_id: str = Field(
        alias="adId",
        description="Populated whenever the provider has data for the entity.",
    )
    transcript: str = Field(description="Transcribed ad audio text.")
    transcript_available: bool = Field(alias="transcriptAvailable")
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookAdsSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[FacebookAdsSearchAd]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of ads, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total_results: int | None = Field(
        alias="totalResults",
        description="Total number of ads matching the search. Null when the source cannot report an exact count.",
    )


class FacebookAdsSearchAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active: bool
    ad_count: int | None = Field(
        alias="adCount",
        description="Number of ads in this campaign (collation count). Null when the source does not report it.",
    )
    caption: str | None = Field(
        default=None,
        description="Caption line of the ad creative, usually the advertiser's display domain.",
    )
    categories: list[str] | None = Field(
        default=None, description="Ad Library categories the ad is filed under."
    )
    creatives: list[FacebookAdsSearchCreative] | None = Field(
        default=None,
        description="One entry per card of a carousel, dynamic-product, or dynamic-creative ad, in the order Meta returns them, each with its own text and destination. Single-creative ads return an empty array. The same card images and videos also appear in media. Meta CDN media URLs are signed and expire.",
    )
    cta_text: str = Field(
        alias="ctaText",
        description="Populated whenever the provider has data for the entity.",
    )
    cta_type: str = Field(
        alias="ctaType",
        description="Populated whenever the provider has data for the entity.",
    )
    display_format: str = Field(
        alias="displayFormat",
        description="Populated whenever the provider has data for the entity.",
    )
    end_date: int = Field(alias="endDate", description="Epoch seconds.")
    id: str = Field(
        description="Ad Library archive ID. Populated whenever the provider has data for the entity."
    )
    is_reshared: bool | None = Field(
        default=None,
        alias="isReshared",
        description="Whether the ad creative is a reshare of another post.",
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Description text shown under the ad's link.",
    )
    link_url: str = Field(
        alias="linkUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    media: list[FacebookAdsSearchMedia] | None = Field(
        default=None,
        description="Creative attached to the ad: one element per image, video, or carousel card, in the order the ad presents them. Empty when the ad has none.",
    )
    page_categories: list[str] | None = Field(
        default=None,
        alias="pageCategories",
        description="Categories Facebook lists the advertising page under.",
    )
    page_deleted: bool | None = Field(
        default=None,
        alias="pageDeleted",
        description="Whether the advertising page has been deleted.",
    )
    page_id: str = Field(
        alias="pageId",
        description="Populated whenever the provider has data for the entity.",
    )
    page_likes: int | None = Field(
        default=None,
        alias="pageLikes",
        description="Like count of the advertising page.",
    )
    page_name: str = Field(
        alias="pageName",
        description="Populated whenever the provider has data for the entity.",
    )
    page_profile_picture: str | None = Field(
        default=None,
        alias="pageProfilePicture",
        description="Profile picture of the advertising page. This is the advertiser's identity image, not ad creative.",
    )
    page_url: str | None = Field(
        default=None,
        alias="pageUrl",
        description="Canonical Facebook URL of the advertising page.",
    )
    platforms: list[str] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    source_url: str = Field(
        alias="sourceUrl",
        description="Inspectable Meta Ad Library URL for this ad. Populated whenever the provider has data for the entity.",
    )
    start_date: int = Field(
        alias="startDate",
        description="Epoch seconds. Populated whenever the provider has data for the entity.",
    )
    text: str = Field(
        description="Ad body text. Populated whenever the provider has data for the entity."
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookAdsSearchCreative(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    body: str | None = Field(default=None, description="Card body text.")
    caption: str | None = Field(
        default=None,
        description="Card display caption, usually the destination domain.",
    )
    cta_text: str | None = Field(
        default=None,
        alias="ctaText",
        description='Card call-to-action label (e.g. "Shop Now").',
    )
    cta_type: str | None = Field(
        default=None,
        alias="ctaType",
        description='Card call-to-action type (e.g. "SHOP_NOW").',
    )
    image: str | None = Field(
        default=None,
        description="Card image URL. For a video card this is the poster frame.",
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Card secondary description line.",
    )
    link_url: str | None = Field(
        default=None, alias="linkUrl", description="Card destination URL."
    )
    title: str | None = Field(default=None, description="Card headline.")
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Card video file URL (HD when supplied, otherwise SD). Present only on video cards.",
    )


class FacebookAdsSearchMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL. Present only for video and gif items.",
    )
    width: int | None = Field(
        default=None,
        description="Pixel width of the media item, when the lane reports it.",
    )


class FacebookCommentRepliesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_next_page: bool = Field(
        alias="hasNextPage",
        description="True when more replies are available beyond this page.",
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of replies, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    replies: list[FacebookCommentRepliesReplie] = Field(
        description="Replies to the comment. Populated whenever the provider has data for the entity."
    )


class FacebookCommentRepliesReplie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_id: str = Field(
        alias="authorId",
        description="Identifier of the reply author. Populated whenever the provider has data for the entity.",
    )
    author_name: str = Field(
        alias="authorName",
        description="Display name of the reply author. Populated whenever the provider has data for the entity.",
    )
    author_profile_picture: str = Field(
        alias="authorProfilePicture", description="URL of the author's profile picture."
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    expansion_token: str | None = Field(
        default=None,
        alias="expansionToken",
        description="Token used to expand nested replies, when present.",
    )
    feedback_id: str = Field(
        alias="feedbackId",
        description="Facebook feedback identifier for the reply. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Reply identifier. Populated whenever the provider has data for the entity."
    )
    reaction_count: int = Field(
        alias="reactionCount", description="Number of reactions on the reply."
    )
    reply_count: int = Field(
        alias="replyCount", description="Number of replies nested under this reply."
    )
    text: str = Field(
        description="Reply text content. Populated whenever the provider has data for the entity."
    )


class FacebookCompanyAdsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[FacebookCompanyAdsAd]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of ads, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total_results: int | None = Field(
        default=None,
        alias="totalResults",
        description="Total number of ads Facebook reports for the page.",
    )


class FacebookCompanyAdsAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active: bool
    ad_count: int | None = Field(
        alias="adCount",
        description="Number of ads in this campaign (collation count). Null when the source does not report it.",
    )
    caption: str | None = Field(
        default=None,
        description="Caption line of the ad creative, usually the advertiser's display domain.",
    )
    categories: list[str] | None = Field(
        default=None, description="Ad Library categories the ad is filed under."
    )
    creatives: list[FacebookCompanyAdsCreative] | None = Field(
        default=None,
        description="One entry per card of a carousel, dynamic-product, or dynamic-creative ad, in the order Meta returns them, each with its own text and destination. Single-creative ads return an empty array. The same card images and videos also appear in media. Meta CDN media URLs are signed and expire.",
    )
    cta_text: str | None = Field(
        default=None,
        alias="ctaText",
        description="Call-to-action button label on the ad.",
    )
    cta_type: str | None = Field(
        default=None,
        alias="ctaType",
        description='Call-to-action button type on the ad, e.g. "SHOP_NOW".',
    )
    currency: str
    display_format: str = Field(
        alias="displayFormat",
        description="Populated whenever the provider has data for the entity.",
    )
    end_date: int = Field(alias="endDate", description="Epoch seconds.")
    id: str = Field(
        description="Ad Library archive ID. Populated whenever the provider has data for the entity."
    )
    is_reshared: bool | None = Field(
        default=None,
        alias="isReshared",
        description="Whether the ad creative is a reshare of another post.",
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Description text shown under the ad's link.",
    )
    link_url: str | None = Field(
        default=None, alias="linkUrl", description="Destination URL the ad links to."
    )
    media: list[FacebookCompanyAdsMedia] | None = Field(
        default=None,
        description="Creative attached to the ad: one element per image, video, or carousel card, in the order the ad presents them. Empty when the ad has none.",
    )
    page_categories: list[str] | None = Field(
        default=None,
        alias="pageCategories",
        description="Categories Facebook lists the advertising page under.",
    )
    page_deleted: bool | None = Field(
        default=None,
        alias="pageDeleted",
        description="Whether the advertising page has been deleted.",
    )
    page_id: str = Field(
        alias="pageId",
        description="Populated whenever the provider has data for the entity.",
    )
    page_likes: int | None = Field(
        default=None,
        alias="pageLikes",
        description="Like count of the advertising page.",
    )
    page_name: str = Field(
        alias="pageName",
        description="Populated whenever the provider has data for the entity.",
    )
    page_profile_picture: str | None = Field(
        default=None,
        alias="pageProfilePicture",
        description="Profile picture of the advertising page. This is the advertiser's identity image, not ad creative.",
    )
    page_url: str | None = Field(
        default=None,
        alias="pageUrl",
        description="Canonical Facebook URL of the advertising page.",
    )
    platforms: list[str] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    start_date: int = Field(
        alias="startDate",
        description="Epoch seconds. Populated whenever the provider has data for the entity.",
    )
    text: str = Field(
        description="Ad body text. Populated whenever the provider has data for the entity."
    )
    title: str | None = Field(default=None, description="Headline of the ad creative.")


class FacebookCompanyAdsCreative(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    body: str | None = Field(default=None, description="Card body text.")
    caption: str | None = Field(
        default=None,
        description="Card display caption, usually the destination domain.",
    )
    cta_text: str | None = Field(
        default=None,
        alias="ctaText",
        description='Card call-to-action label (e.g. "Shop Now").',
    )
    cta_type: str | None = Field(
        default=None,
        alias="ctaType",
        description='Card call-to-action type (e.g. "SHOP_NOW").',
    )
    image: str | None = Field(
        default=None,
        description="Card image URL. For a video card this is the poster frame.",
    )
    link_description: str | None = Field(
        default=None,
        alias="linkDescription",
        description="Card secondary description line.",
    )
    link_url: str | None = Field(
        default=None, alias="linkUrl", description="Card destination URL."
    )
    title: str | None = Field(default=None, description="Card headline.")
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Card video file URL (HD when supplied, otherwise SD). Present only on video cards.",
    )


class FacebookCompanyAdsMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL. Present only for video and gif items.",
    )
    width: int | None = Field(
        default=None,
        description="Pixel width of the media item, when the lane reports it.",
    )


class FacebookEventDetailsData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Street address of the event venue."
    )
    attendance_count: int | None = Field(
        default=None,
        alias="attendanceCount",
        description="Number of people Facebook reports as attending.",
    )
    can_view_members: bool | None = Field(
        default=None,
        alias="canViewMembers",
        description="Whether the event's member list is publicly viewable.",
    )
    city: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    city_id: str | None = Field(
        default=None,
        alias="cityId",
        description="Numeric Facebook id of the event's city page, as a string.",
    )
    cover_photo_url: str = Field(
        alias="coverPhotoUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    creator_id: str | None = Field(
        default=None,
        alias="creatorId",
        description="Numeric Facebook id of the event's creator, as a string.",
    )
    creator_name: str | None = Field(
        default=None,
        alias="creatorName",
        description="Display name of the event's creator.",
    )
    day_time_sentence: str = Field(
        alias="dayTimeSentence",
        description="Populated whenever the provider has data for the entity.",
    )
    description: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    duration: str | None = Field(
        default=None, description='Human-readable event duration, e.g. "2 days".'
    )
    end_time: str = Field(alias="endTime")
    event_kind: str | None = Field(
        default=None,
        alias="eventKind",
        description='Event kind Facebook reports, e.g. "PUBLIC_TYPE".',
    )
    going_count: int = Field(alias="goingCount")
    host_context_text: str | None = Field(
        default=None,
        alias="hostContextText",
        description='Host line Facebook shows for the event, e.g. "Event by Kansas Comic Con".',
    )
    host_names: list[str] | None = Field(
        default=None, alias="hostNames", description="Names of the event's hosts."
    )
    hosts: list[FacebookEventDetailsHost] | None = Field(
        default=None, description="Pages or profiles hosting the event."
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    interested_count: int = Field(alias="interestedCount")
    is_canceled: bool = Field(alias="isCanceled")
    is_online: bool = Field(alias="isOnline")
    is_past: bool | None = Field(
        default=None,
        alias="isPast",
        description="Whether the event has already finished.",
    )
    latitude: float | None = Field(
        default=None, description="Latitude of the event venue."
    )
    location_name: str = Field(
        alias="locationName",
        description="Populated whenever the provider has data for the entity.",
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the event venue."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    place_id: str | None = Field(
        default=None,
        alias="placeId",
        description="Numeric Facebook id of the event's place, as a string.",
    )
    privacy: str | None = Field(
        default=None, description='Privacy setting of the event, e.g. "public".'
    )
    rsvp_style: str | None = Field(
        default=None,
        alias="rsvpStyle",
        description='RSVP style of the event, e.g. "PUBLIC_RSVP_STYLE".',
    )
    start_time: str = Field(alias="startTime")
    start_time_formatted: str | None = Field(
        default=None,
        alias="startTimeFormatted",
        description='Human-readable start time Facebook shows, e.g. "Sat, Oct 31 - Nov 1".',
    )
    start_timestamp: int | None = Field(
        default=None,
        alias="startTimestamp",
        description="UTC epoch timestamp in seconds (Unix time) the event starts. Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookEventDetailsHost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None, description="Numeric Facebook id of the host, as a string."
    )
    image: str | None = Field(
        default=None, description="Profile picture URL of the host."
    )
    name: str | None = Field(default=None, description="Display name of the host.")
    type_: str | None = Field(
        default=None,
        alias="type",
        description='Kind of Facebook entity the host is, e.g. "User" or "Page".',
    )
    url: str | None = Field(
        default=None, description="Canonical Facebook URL of the host."
    )
    verified: bool | None = Field(
        default=None,
        description="Whether the host carries a Facebook verification badge.",
    )


class FacebookEventsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: list[FacebookEventsEvent]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of events, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class FacebookEventsEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cover_image: str | None = Field(
        default=None,
        alias="coverImage",
        description="Cover photo image URL of the event.",
    )
    day_time_sentence: str = Field(
        alias="dayTimeSentence",
        description="Populated whenever the provider has data for the entity.",
    )
    event_kind: str | None = Field(
        default=None,
        alias="eventKind",
        description='Event kind Facebook reports, e.g. "PUBLIC_TYPE".',
    )
    going_count: int = Field(alias="goingCount")
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    interested_count: int = Field(alias="interestedCount")
    is_happening_now: bool | None = Field(
        default=None,
        alias="isHappeningNow",
        description="Whether the event is happening right now.",
    )
    is_online: bool = Field(alias="isOnline")
    is_past: bool | None = Field(
        default=None,
        alias="isPast",
        description="Whether the event has already finished.",
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    place_id: str | None = Field(
        default=None,
        alias="placeId",
        description="Numeric Facebook id of the event's place, as a string.",
    )
    place_name: str = Field(
        alias="placeName",
        description="Populated whenever the provider has data for the entity.",
    )
    start_timestamp: int = Field(
        alias="startTimestamp",
        description="Populated whenever the provider has data for the entity.",
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookEventsSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: list[FacebookEventsSearchEvent]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of events, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class FacebookEventsSearchEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cover_image: str = Field(
        alias="coverImage",
        description="Populated whenever the provider has data for the entity.",
    )
    day_time_sentence: str = Field(
        alias="dayTimeSentence",
        description="Populated whenever the provider has data for the entity.",
    )
    event_kind: str | None = Field(
        default=None,
        alias="eventKind",
        description='Event kind Facebook reports, e.g. "PUBLIC_TYPE".',
    )
    going_count: int = Field(alias="goingCount")
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    interested_count: int = Field(alias="interestedCount")
    is_online: bool = Field(alias="isOnline")
    is_past: bool = Field(alias="isPast")
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    place_id: str | None = Field(
        default=None,
        alias="placeId",
        description="Numeric Facebook id of the event's place, as a string.",
    )
    place_name: str = Field(
        alias="placeName",
        description="Populated whenever the provider has data for the entity.",
    )
    price_range_text: str = Field(alias="priceRangeText")
    start_timestamp: int = Field(
        alias="startTimestamp",
        description="Populated whenever the provider has data for the entity.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description='Entity type of the record, e.g. "Event".',
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookFollowersData(BaseModel):
    items: list[FacebookFollowersItem] = Field(
        description="Follower or following records for the target page/profile. Populated whenever the provider has data for the entity."
    )


class FacebookFollowersItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(
        description="The account's numeric Facebook ID, as a string. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the account's profile picture, a signed CDN URL whose query must be kept. Empty when the upstream omits it.",
    )
    name: str = Field(
        description="The account's public display name. Populated whenever the provider has data for the entity."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description='Kind of Facebook entity the record is, e.g. "User" or "Page".',
    )
    url: str = Field(
        description="Canonical URL of the account's Facebook profile, with tracking query params stripped. Populated whenever the provider has data for the entity."
    )


class FacebookGroupPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    posts: list[FacebookGroupPostsPost] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookGroupPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_id: str = Field(
        alias="authorId",
        description="Populated whenever the provider has data for the entity.",
    )
    author_name: str = Field(
        alias="authorName",
        description="Populated whenever the provider has data for the entity.",
    )
    comment_count: int = Field(alias="commentCount")
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the post's first image. Absent when the post has no image.",
    )
    publish_time: int = Field(
        alias="publishTime",
        description="Populated whenever the provider has data for the entity.",
    )
    reaction_count: int = Field(alias="reactionCount")
    reactions: FacebookGroupPostsReaction = Field(
        description="Reaction counts on the post, broken down by reaction type."
    )
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookGroupPostsReaction(BaseModel):
    model_config = ConfigDict(extra="allow")

    angry: int | None = Field(default=None, description="Angry reactions.")
    care: int | None = Field(default=None, description="Care reactions.")
    haha: int | None = Field(default=None, description="Haha reactions.")
    like: int | None = Field(default=None, description="Like reactions.")
    love: int | None = Field(default=None, description="Love reactions.")
    sad: int | None = Field(default=None, description="Sad reactions.")
    wow: int | None = Field(default=None, description="Wow reactions.")


class FacebookMarketplaceData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_next_page: bool = Field(alias="hasNextPage")
    listings: list[FacebookMarketplaceListing]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of listings, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class FacebookMarketplaceListing(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category_id: str | None = Field(
        default=None,
        alias="categoryId",
        description="Numeric Facebook Marketplace category id, as a string.",
    )
    city: str | None = Field(
        default=None, description="City the listing is located in."
    )
    city_page_id: str | None = Field(
        default=None,
        alias="cityPageId",
        description="Numeric Facebook id of the city page, as a string.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the listing was created. Multiply by 1000 for a JS Date in milliseconds. Null when the source does not report it.",
    )
    delivery_types: list[str] | None = Field(
        default=None,
        alias="deliveryTypes",
        description='Delivery options the seller offers, e.g. "IN_PERSON" or "SHIPPING".',
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    is_hidden: bool | None = Field(
        default=None, alias="isHidden", description="Whether the listing is hidden."
    )
    is_live: bool | None = Field(
        default=None,
        alias="isLive",
        description="Whether the listing is currently live.",
    )
    is_pending: bool | None = Field(
        default=None,
        alias="isPending",
        description="Whether the listing is marked pending.",
    )
    is_sold: bool = Field(alias="isSold")
    listing_date_text: str | None = Field(
        default=None,
        alias="listingDateText",
        description='Human-readable listing age Facebook shows, e.g. "Listed 2 weeks ago".',
    )
    location_name: str = Field(
        alias="locationName",
        description="Populated whenever the provider has data for the entity.",
    )
    photo_id: str | None = Field(
        default=None,
        alias="photoId",
        description="Numeric Facebook id of the listing's primary photo, as a string.",
    )
    photo_url: str = Field(
        alias="photoUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    price_amount: float = Field(
        alias="priceAmount",
        description="Populated whenever the provider has data for the entity.",
    )
    price_formatted: str = Field(
        alias="priceFormatted",
        description="Populated whenever the provider has data for the entity.",
    )
    state: str | None = Field(
        default=None, description="State or region the listing is located in."
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookMarketplaceItemData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attributes: list[FacebookMarketplaceItemAttribute] | None = Field(
        default=None, description="Item specifics Facebook publishes for the listing."
    )
    category_id: str = Field(
        alias="categoryId",
        description="Populated whenever the provider has data for the entity.",
    )
    creation_time: str = Field(
        alias="creationTime",
        description="Populated whenever the provider has data for the entity.",
    )
    currency: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    delivery_types: list[str] | None = Field(
        default=None,
        alias="deliveryTypes",
        description='Delivery options the seller offers, e.g. "IN_PERSON" or "SHIPPING".',
    )
    description: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    is_buy_now_enabled: bool | None = Field(
        default=None,
        alias="isBuyNowEnabled",
        description="Whether buy-now checkout is enabled on the listing.",
    )
    is_hidden: bool | None = Field(
        default=None, alias="isHidden", description="Whether the listing is hidden."
    )
    is_live: bool = Field(alias="isLive")
    is_pending: bool | None = Field(
        default=None,
        alias="isPending",
        description="Whether the listing is marked pending.",
    )
    is_shipping_offered: bool | None = Field(
        default=None,
        alias="isShippingOffered",
        description="Whether the seller offers shipping.",
    )
    is_sold: bool = Field(alias="isSold")
    latitude: float | None = Field(
        default=None, description="Latitude of the listing's location."
    )
    listing_date_text: str | None = Field(
        default=None,
        alias="listingDateText",
        description='Human-readable listing age Facebook shows, e.g. "Listed 4 months ago".',
    )
    location_text: str = Field(
        alias="locationText",
        description="Populated whenever the provider has data for the entity.",
    )
    longitude: float | None = Field(
        default=None, description="Longitude of the listing's location."
    )
    messaging_enabled: bool | None = Field(
        default=None,
        alias="messagingEnabled",
        description="Whether buyers can message the seller about the listing.",
    )
    photos: list[FacebookMarketplaceItemPhoto] | None = Field(
        default=None, description="Photos attached to the listing."
    )
    price_amount: float = Field(
        alias="priceAmount",
        description="Populated whenever the provider has data for the entity.",
    )
    price_formatted: str = Field(
        alias="priceFormatted",
        description="Populated whenever the provider has data for the entity.",
    )
    seller: FacebookMarketplaceItemSeller = Field(
        description="The person or business selling the item. Empty when Facebook does not show the seller on the listing."
    )
    share_url: str | None = Field(
        default=None,
        alias="shareUrl",
        description="Canonical shareable Marketplace URL of the listing.",
    )
    strikethrough_price_formatted: str | None = Field(
        default=None,
        alias="strikethroughPriceFormatted",
        description="Previous price shown struck through, formatted for display.",
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookMarketplaceItemAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: str | None = Field(
        default=None, description='Display label for the value, e.g. "Used - Good".'
    )
    name: str | None = Field(
        default=None, description='Attribute name, e.g. "Condition".'
    )
    value: str | None = Field(
        default=None, description='Raw attribute value, e.g. "used_good".'
    )


class FacebookMarketplaceItemPhoto(BaseModel):
    model_config = ConfigDict(extra="allow")

    caption: str | None = Field(
        default=None,
        description="Accessibility caption Facebook generated for the photo.",
    )
    height: int | None = Field(default=None, description="Pixel height of the photo.")
    id: str | None = Field(
        default=None, description="Numeric Facebook id of the photo, as a string."
    )
    url: str | None = Field(default=None, description="Image URL of the photo.")
    width: int | None = Field(default=None, description="Pixel width of the photo.")


class FacebookMarketplaceItemSeller(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None, description="Facebook id of the seller, as a string."
    )
    image: str | None = Field(
        default=None, description="URL of the seller's profile picture."
    )
    joined_utc: float | None = Field(
        default=None,
        alias="joinedUtc",
        description="UTC epoch timestamp in seconds (Unix time) the seller joined Facebook. Multiply by 1000 for a JS Date in milliseconds.",
    )
    name: str | None = Field(default=None, description="The seller's display name.")
    rating: float | None = Field(
        default=None,
        description="The seller's average rating as a seller, out of 5. Absent when the seller has no ratings or keeps them private.",
    )
    rating_count: int | None = Field(
        default=None,
        alias="ratingCount",
        description="Number of ratings the seller has received as a seller. Absent when the seller has no ratings or keeps them private.",
    )


class FacebookMarketplaceLocationSearchData(BaseModel):
    locations: list[FacebookMarketplaceLocationSearchLocation]


class FacebookMarketplaceLocationSearchLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    latitude: float = Field(
        description="Populated whenever the provider has data for the entity."
    )
    longitude: float = Field(
        description="Populated whenever the provider has data for the entity."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    page_id: str = Field(
        alias="pageId",
        description="Populated whenever the provider has data for the entity.",
    )
    postal_code: str = Field(
        alias="postalCode",
        description="Populated whenever the provider has data for the entity.",
    )
    subtitle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookPageContactData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    about: str | None = Field(default=None, description="The page's intro text.")
    ad_status: str | None = Field(
        default=None,
        alias="adStatus",
        description="Facebook Ad Library status sentence for the page.",
    )
    cover_photo_url: str | None = Field(
        default=None,
        alias="coverPhotoUrl",
        description="Cover photo image URL of the page.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the page was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str | None = Field(
        default=None, description="Numeric Facebook id of the page, as a string."
    )
    items: list[FacebookPageContactItem] = Field(
        description="Contact record for the requested Facebook Page (one item). Populated whenever the provider has data for the entity."
    )
    price_range: str | None = Field(
        default=None,
        alias="priceRange",
        description='Price range the page advertises, e.g. "$$".',
    )
    rating: str | None = Field(
        default=None,
        description='Recommendation summary Facebook shows for the page, e.g. "94% recommend (14,553 reviews)".',
    )
    services: str | None = Field(
        default=None,
        description="Services the page lists, e.g. dine-in or online booking.",
    )


class FacebookPageContactItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_library_page_id: str | None = Field(
        default=None,
        alias="adLibraryPageId",
        description="The page's Facebook Ad Library id, the `pageId` facebook.company_ads takes. It differs from `id`. Absent when Facebook shows none.",
    )
    address: str | None = Field(
        default=None,
        description="The page's public physical address. Empty when the page lists none.",
    )
    category: str | None = Field(
        default=None,
        description='The page\'s primary category (e.g. "Seafood Restaurant"). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    email: str | None = Field(
        default=None,
        description="The page's public contact email. Empty when the page lists none.",
    )
    followers: int | None = Field(
        default=None,
        description="The page's follower count. Some sources read it from Facebook's rounded label, so \"474K followers\" comes back as 474000; name it in requireFields for the exact count.",
    )
    image: str | None = Field(
        default=None,
        description="URL of the page's profile picture, a signed CDN URL whose query must be kept. Empty when the upstream omits it.",
    )
    links: list[str] | None = Field(
        default=None,
        description="Other social profiles the page links to, such as its Instagram account, as URLs. Empty when the page links none.",
    )
    phone: str | None = Field(
        default=None,
        description="The page's public phone number. Empty when the page lists none.",
    )
    title: str = Field(
        description="The page's public name. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the Facebook Page, with tracking query params stripped. Populated whenever the provider has data for the entity."
    )
    website: str | None = Field(
        default=None,
        description="The page's public website URL. Empty when the page lists none.",
    )


class FacebookPageLookupData(BaseModel):
    items: list[FacebookPageLookupItem] = Field(
        description="Pages and profiles whose name matches the query, in Facebook's order. Matches can include personal profiles as well as Pages."
    )


class FacebookPageLookupItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(
        description="Numeric Facebook id of the Page or profile, as a string. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Profile picture URL. Facebook signs it in the query string, so it works only as returned and expires. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    is_verified: bool | None = Field(
        default=None,
        alias="isVerified",
        description="Whether Facebook shows the verified badge on this Page or profile.",
    )
    name: str = Field(
        description="Display name of the Page or profile. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Facebook URL of the Page or profile. Populated whenever the provider has data for the entity."
    )


class FacebookPhotosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of photos, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    next_page_id: str | None = Field(
        alias="nextPageId",
        description="Facebook's own id for the next page of photos. Null when the serving source does not report it; pass nextCursor back as cursor to continue either way.",
    )
    photos: list[FacebookPhotosPhoto] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookPhotosPhoto(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image_height: int | None = Field(
        alias="imageHeight",
        description="Height of imageUrl in pixels. Null when the serving source does not report it.",
    )
    image_url: str = Field(
        alias="imageUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    image_width: int | None = Field(
        alias="imageWidth",
        description="Width of imageUrl in pixels. Null when the serving source does not report it.",
    )
    photo_id: str = Field(
        alias="photoId",
        description="Populated whenever the provider has data for the entity.",
    )
    thumbnail: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookPostData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric Facebook id of the page or profile that posted.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Profile picture URL of the page or profile that posted.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the page or profile that posted.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the posting page or profile carries a Facebook verification badge.",
    )
    comments: int
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Length of the post's video in seconds, 0 when the post carries no video.",
    )
    feedback_id: str | None = Field(
        default=None,
        alias="feedbackId",
        description="Facebook feedback id of the post; pass it to facebook.post_comments as feedbackId to fetch its comments. Null when this source cannot read it.",
    )
    id: str = Field(
        description="Facebook post id. For a reel or video post this is NOT the id in the /reel/ URL; that one is videoId. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None, description="Preview image or video thumbnail URL for the post."
    )
    likes: int
    reactions: FacebookPostReaction | None = Field(
        default=None,
        description="Reaction counts on the post, broken down by reaction type. Null when this source reports only the total.",
    )
    shares: int
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None, description="Canonical Facebook URL of the post."
    )
    video_id: str | None = Field(
        default=None,
        alias="videoId",
        description="Facebook video id of the post's reel or video, the id that appears in its /reel/<id> URL. Null when the post carries no video or this lane cannot read it.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL of the post's reel or video. Null when the post carries no video or this source cannot read it.",
    )
    views: int | None = Field(
        description="Number of views on the post's video. Null when the source cannot report an exact count, for example when it gives only a rounded figure such as 14K."
    )


class FacebookPostReaction(BaseModel):
    model_config = ConfigDict(extra="allow")

    angry: int | None = Field(default=None, description="Angry reactions.")
    care: int | None = Field(default=None, description="Care reactions.")
    haha: int | None = Field(default=None, description="Haha reactions.")
    like: int | None = Field(default=None, description="Like reactions.")
    love: int | None = Field(default=None, description="Love reactions.")
    sad: int | None = Field(default=None, description="Sad reactions.")
    wow: int | None = Field(default=None, description="Wow reactions.")


class FacebookPostCommentsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    comments: list[FacebookPostCommentsComment] = Field(
        description="Comments on the post. Populated whenever the provider has data for the entity."
    )
    has_next_page: bool | None = Field(
        default=None,
        alias="hasNextPage",
        description="Whether more comments are available after this page.",
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of comments, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class FacebookPostCommentsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Display name of the comment author. Populated whenever the provider has data for the entity."
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Facebook id of the commenter, as a string.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Profile picture URL of the commenter.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    expansion_token: str | None = Field(
        default=None,
        alias="expansionToken",
        description="Facebook expansion token for paging the comment's replies.",
    )
    feedback_id: str | None = Field(
        default=None,
        alias="feedbackId",
        description="Facebook feedback id of the comment, used to fetch its replies.",
    )
    id: str = Field(
        description="Comment identifier. Populated whenever the provider has data for the entity."
    )
    reactions: int = Field(description="Number of reactions on the comment.")
    replies: int = Field(description="Number of replies to the comment.")
    text: str = Field(
        description="Comment text content. Populated whenever the provider has data for the entity."
    )


class FacebookPostTranscriptData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Length of the video in seconds, with fractional seconds. Absent when the post has no transcribable video.",
    )
    post_id: str | None = Field(
        default=None,
        alias="postId",
        description="Numeric Facebook id of the transcribed post, as a string.",
    )
    transcript: str


class FacebookProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str
    ad_library_page_id: str | None = Field(
        default=None,
        alias="adLibraryPageId",
        description="The page's Facebook Ad Library id, the `pageId` facebook.company_ads takes. It differs from `id`. Absent when Facebook shows none.",
    )
    ad_status: str | None = Field(
        default=None,
        alias="adStatus",
        description="Facebook Ad Library status sentence for the page, e.g. whether it is currently running ads. Absent when Facebook shows none.",
    )
    avatar_url: str = Field(
        alias="avatarUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    category: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    cover_photo_url: str | None = Field(
        default=None,
        alias="coverPhotoUrl",
        description="Cover photo image URL of the page or profile.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the page was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    followers: int
    id: str | None = Field(
        default=None, description="Numeric Facebook id of the page or profile."
    )
    likes: int
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    page_active: bool | None = Field(
        default=None,
        alias="pageActive",
        description="Whether the page is an active business page.",
    )
    phone: str | None = Field(
        default=None, description="Public phone number listed on the page."
    )
    talking_about_count: int | None = Field(
        default=None,
        alias="talkingAboutCount",
        description="Number of people talking about the page.",
    )
    url: str | None = Field(
        default=None, description="Canonical Facebook URL of the page or profile."
    )
    website: str | None = Field(default=None, description="Website listed on the page.")


class FacebookProfileEventsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: list[FacebookProfileEventsEvent] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    has_next_page: bool = Field(alias="hasNextPage")
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of events, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total_count: int = Field(alias="totalCount")


class FacebookProfileEventsEvent(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    city: str
    creator_name: str = Field(
        alias="creatorName",
        description="Populated whenever the provider has data for the entity.",
    )
    day_time_sentence: str = Field(alias="dayTimeSentence")
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    is_canceled: bool = Field(alias="isCanceled")
    is_online: bool = Field(alias="isOnline")
    is_past: bool = Field(alias="isPast")
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    place_name: str = Field(alias="placeName")
    start_timestamp: int = Field(alias="startTimestamp")
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookProfilePostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    posts: list[FacebookProfilePostsPost] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookProfilePostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric Facebook id of the page or profile that posted, as a string.",
    )
    comments: int | None = Field(default=None, description="Comment count on the post.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None, description="Preview image or video thumbnail URL for the post."
    )
    likes: int | None = Field(
        default=None, description="Total reaction count on the post."
    )
    media: list[FacebookProfilePostsMedia] | None = Field(
        default=None,
        description="Photo, video, and GIF attachments on the post. Empty when the post has none.",
    )
    reactions: FacebookProfilePostsReaction = Field(
        description="Reaction counts on the post, broken down by reaction type."
    )
    shares: int | None = Field(
        default=None,
        description="Number of times the post was shared. Null when this source does not report it.",
    )
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookProfilePostsMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL. Present only for video and gif items.",
    )
    width: int | None = Field(
        default=None,
        description="Pixel width of the media item, when the lane reports it.",
    )


class FacebookProfilePostsReaction(BaseModel):
    model_config = ConfigDict(extra="allow")

    angry: int | None = Field(default=None, description="Angry reactions.")
    care: int | None = Field(default=None, description="Care reactions.")
    haha: int | None = Field(default=None, description="Haha reactions.")
    like: int | None = Field(default=None, description="Like reactions.")
    love: int | None = Field(default=None, description="Love reactions.")
    sad: int | None = Field(default=None, description="Sad reactions.")
    wow: int | None = Field(default=None, description="Wow reactions.")


class FacebookProfileReelsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of reels, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    reels: list[FacebookProfileReelsReel] = Field(
        description="The profile's reels. Populated whenever the provider has data for the entity."
    )


class FacebookProfileReelsReel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric Facebook id of the page or profile that posted the reel, as a string.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Profile picture URL of the page or profile that posted the reel.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the page or profile that posted the reel.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the posting page or profile carries a Facebook verification badge.",
    )
    caption: str = Field(
        description="Reel caption text. Populated whenever the provider has data for the entity."
    )
    comments: int | None = Field(
        default=None,
        description="Comment count on the reel. Null when this source does not report it.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Length of the reel in seconds.",
    )
    feedback_id: str | None = Field(
        default=None,
        alias="feedbackId",
        description="Facebook feedback id of the reel, used to fetch its comments.",
    )
    id: str = Field(
        description="Facebook post id of the reel, the same id facebook.post returns for it. This is NOT the id in the reel's /reel/ URL; that one is videoId. Populated whenever the provider has data for the entity."
    )
    likes: int | None = Field(
        default=None,
        description="Total reaction count on the reel. Null when this source does not report it.",
    )
    shares: int | None = Field(
        default=None,
        description="Number of times the reel was shared. Null when this source does not report it.",
    )
    thumbnail: str = Field(
        description="URL of the reel thumbnail image. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the reel. Populated whenever the provider has data for the entity."
    )
    video_id: str = Field(
        alias="videoId",
        description="Facebook video id of the reel, the id that appears in its /reel/<id> URL.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL of the reel. Null when this source cannot read it.",
    )
    views: int = Field(description="Number of views on the reel.")


class FacebookSearchCompaniesData(BaseModel):
    companies: list[FacebookSearchCompaniesCompanie]


class FacebookSearchCompaniesCompanie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    country: str
    entity_type: str = Field(
        alias="entityType",
        description="Populated whenever the provider has data for the entity.",
    )
    ig_followers: int = Field(
        alias="igFollowers",
        description="Populated whenever the provider has data for the entity.",
    )
    ig_username: str = Field(
        alias="igUsername",
        description="Populated whenever the provider has data for the entity.",
    )
    ig_verified: bool | None = Field(
        default=None,
        alias="igVerified",
        description="Whether the page's linked Instagram account is verified.",
    )
    image_url: str = Field(
        alias="imageUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    likes: int
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    page_alias: str = Field(
        alias="pageAlias",
        description="Populated whenever the provider has data for the entity.",
    )
    page_deleted: bool | None = Field(
        default=None,
        alias="pageDeleted",
        description="Whether the Facebook Page has been deleted.",
    )
    page_id: str = Field(
        alias="pageId",
        description="Populated whenever the provider has data for the entity.",
    )
    verification: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class FacebookSearchPagesData(BaseModel):
    items: list[FacebookSearchPagesItem] = Field(
        description="Matching Facebook Page records for the query. Populated whenever the provider has data for the entity."
    )


class FacebookSearchPagesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    about: str | None = Field(default=None, description="The page's intro text.")
    ad_library_page_id: str | None = Field(
        default=None,
        alias="adLibraryPageId",
        description="The page's Facebook Ad Library id, the `pageId` facebook.company_ads takes. It differs from `id`. Absent when Facebook shows none.",
    )
    ad_status: str | None = Field(
        default=None,
        alias="adStatus",
        description="Facebook Ad Library status sentence for the page, e.g. whether it is currently running ads.",
    )
    categories: list[str] | None = Field(
        default=None, description="Categories Facebook lists the page under."
    )
    category: str | None = Field(
        default=None,
        description='The page\'s primary category (e.g. "Sportswear Store"). Empty when the upstream omits it.',
    )
    cover_photo_url: str | None = Field(
        default=None,
        alias="coverPhotoUrl",
        description="Cover photo image URL of the page.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the page was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    followers: int | None = Field(
        default=None, description="The page's follower count."
    )
    id: str = Field(
        description="The page's numeric Facebook ID, as a string. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the page's profile picture, a signed CDN URL whose query must be kept. Empty when the upstream omits it.",
    )
    likes: int | None = Field(default=None, description="The page's like count.")
    owner: str | None = Field(
        default=None,
        description="Confirmed owner of the page, when Facebook publishes one.",
    )
    page_alias: str | None = Field(
        default=None,
        alias="pageAlias",
        description='The page\'s vanity URL alias, e.g. "nikesportswear".',
    )
    phone: str | None = Field(
        default=None,
        description="The page's public phone number. Empty when the upstream omits it.",
    )
    title: str = Field(
        description="The page's public name. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the Facebook Page, with tracking query params stripped. Populated whenever the provider has data for the entity."
    )
    website: str | None = Field(
        default=None,
        description="The page's public website URL. Empty when the upstream omits it.",
    )


class FacebookSearchPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    album_preview: list[FacebookSearchPostsAlbumPreview] | None = Field(
        default=None,
        alias="albumPreview",
        description="Preview of the photos attached to the post.",
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric Facebook id of the page or profile that posted, as a string.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Profile picture URL of the page or profile that posted.",
    )
    images_count: int | None = Field(
        default=None,
        alias="imagesCount",
        description="Number of images attached to the post. Null when the source does not report it.",
    )
    items: list[FacebookSearchPostsItem] = Field(
        description="Matching public Facebook post records for the query. Populated whenever the provider has data for the entity."
    )
    reactions: FacebookSearchPostsReaction | None = Field(
        default=None,
        description="Reaction counts on the post, broken down by reaction type.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description='Kind of record Facebook returned, e.g. "post".',
    )


class FacebookSearchPostsAlbumPreview(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(
        default=None, description="Numeric Facebook id of the photo, as a string."
    )
    image: str | None = Field(default=None, description="Image URL of the photo.")
    type_: str | None = Field(
        default=None, alias="type", description='Kind of attachment, e.g. "photo".'
    )
    url: str | None = Field(
        default=None, description="Canonical Facebook URL of the photo."
    )


class FacebookSearchPostsItem(BaseModel):
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
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Total number of comments on the post.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(
        description="The post's numeric Facebook ID, as a string. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the post's primary image, a signed CDN URL whose query must be kept. Empty for text-only or video posts.",
    )
    reaction_count: int | None = Field(
        default=None,
        alias="reactionCount",
        description="Total number of reactions on the post.",
    )
    share_count: int | None = Field(
        default=None,
        alias="shareCount",
        description="Total number of shares/reshares of the post.",
    )
    text: str = Field(
        description="The post's text/message. Empty for media-only posts with no caption."
    )
    url: str = Field(
        description="Canonical URL of the post. A post with no page path keeps the query that identifies it (permalink.php?story_fbid=...&id=...). Populated whenever the provider has data for the entity."
    )


class FacebookSearchPostsReaction(BaseModel):
    model_config = ConfigDict(extra="allow")

    angry: int | None = Field(default=None, description="Angry reactions.")
    care: int | None = Field(default=None, description="Care reactions.")
    haha: int | None = Field(default=None, description="Haha reactions.")
    like: int | None = Field(default=None, description="Like reactions.")
    love: int | None = Field(default=None, description="Love reactions.")
    sad: int | None = Field(default=None, description="Sad reactions.")
    wow: int | None = Field(default=None, description="Wow reactions.")


class FacebookNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ad_details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdDetailsInput],
    ) -> RunResult[FacebookAdDetailsData]:
        """Facebook Ad Details

        Look up a single Meta Ad Library ad by ID or URL and get the advertiser,
        creative text, call-to-action, platforms, and run dates as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.ad_details(id="962050096457659")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ad_details", dict(input), options
        )
        return RunResult[FacebookAdDetailsData].model_validate(raw)

    def ad_details_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdDetailsFullInput],
    ) -> RunResult[FacebookAdDetailsFullData]:
        """Facebook Ad Creative Details

        Pull one Meta Ad Library ad with its creative: every carousel variant, image
        and video URL, headline, body, and call to action.

        Price: $0.00462 per request plus $0 per result (maximum $0.00462).

        Example:
            res = client.facebook.ad_details_full(id="962050096457659")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ad_details_full", dict(input), options
        )
        return RunResult[FacebookAdDetailsFullData].model_validate(raw)

    def ad_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdTranscriptInput],
    ) -> RunResult[FacebookAdTranscriptData]:
        """Facebook Ad Transcript

        Get the spoken-word transcript of a Meta Ad Library video ad by ad ID or
        URL.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.ad_transcript(id="931919822778200")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ad_transcript", dict(input), options
        )
        return RunResult[FacebookAdTranscriptData].model_validate(raw)

    def ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdsSearchInput],
    ) -> RunResult[FacebookAdsSearchData]:
        """Facebook Ad Search

        Search the Meta Ad Library by keyword and get matching ads (advertiser,
        creative text, CTA, platforms, and run dates) with cursor pagination.

        Price: $0.0011 per request.

        Example:
            res = client.facebook.ads_search(country="US", query="nike", searchType="keyword_exact_phrase")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ads_search", dict(input), options
        )
        return RunResult[FacebookAdsSearchData].model_validate(raw)

    def iter_ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdsSearchInput],
    ) -> Paginator[FacebookAdsSearchAd, FacebookAdsSearchData]:
        """Iterate Facebook Ad Search results, following pagination cursors.

        Yields validated `FacebookAdsSearchAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.ads_search",
            dict(input),
            "ads",
            item_model=FacebookAdsSearchAd,
            data_model=FacebookAdsSearchData,
            bare=False,
            options=options,
        )

    def comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCommentRepliesInput],
    ) -> RunResult[FacebookCommentRepliesData]:
        """Facebook Comment Replies

        List the replies to a Facebook post comment (text, author, reactions, and
        timestamps) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.comment_replies(expansionToken="MjoxNzgzMjI4OTY4OgF_o5zrjDnpemv4bwPtpsShXutqvKIw2bKs2YuJksL1Ak8n8YG-_KPSQGkIks5oW6wdRfhb_cRv9q5OX0NHjFJwEupYNZi9pcMV-FYLWLp47u-eusMkZFOMwbkISsTln7gtSvQrOzlffyavOTIL85PECYzGfunU2IAEkd13CIikxu06Mw10UJ1ShcFAmz8175R1uJfYy_iOixWZukqfrWhUfVOXApXznxx7qXvUxPwct76qe6p7-nVWQrPC_SZc2xh9Z8ggL3WMjgTzSq4oWFSsyZuuVsyVVjSgdjRQiDqtJSeEUlSjTr6vOnKsvKV-GpnBRaeA0BCaNRhqpB4xDZoduBuO5ZYrFvWLJdJLryDhCPI2Ss-Z33cEM2Vz7pLf1wJzE7TuizXPwICSn1DA_Prca-BItTbOUjAjfiySap1LXYkGuuDC2ziUdiEsmE5XhevMP8XtF_2WQlMNcGbXMEQyAWDUawtPAxXgMeRrCO9YGSweFQ4OZumoIlSGa3Vfjy-euUOHT1IAsNbV2A8rAq4HJNU3jCXQTn0vfW9xvbVQhL-53Mhw2YPjhlvUj6QpnGA25N8", feedbackId="ZmVlZGJhY2s6MTM5MzQ2MTExNTQ4MTkyN18yMDgyNjUzMjQ1ODA5Mzg2")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.comment_replies", dict(input), options
        )
        return RunResult[FacebookCommentRepliesData].model_validate(raw)

    def iter_comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCommentRepliesInput],
    ) -> Paginator[FacebookCommentRepliesReplie, FacebookCommentRepliesData]:
        """Iterate Facebook Comment Replies results, following pagination cursors.

        Yields validated `FacebookCommentRepliesReplie` items from the `replies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.comment_replies",
            dict(input),
            "replies",
            item_model=FacebookCommentRepliesReplie,
            data_model=FacebookCommentRepliesData,
            bare=False,
            options=options,
        )

    def company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCompanyAdsInput],
    ) -> RunResult[FacebookCompanyAdsData]:
        """Facebook Company Ads

        List the Meta Ad Library ads a company is running by page ID or company name
        (creative text, format, platforms, and run dates) with cursor pagination.

        Price: $0.0011 per request.

        Example:
            res = client.facebook.company_ads(pageId="15087023444", sortBy="recent")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.company_ads", dict(input), options
        )
        return RunResult[FacebookCompanyAdsData].model_validate(raw)

    def iter_company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCompanyAdsInput],
    ) -> Paginator[FacebookCompanyAdsAd, FacebookCompanyAdsData]:
        """Iterate Facebook Company Ads results, following pagination cursors.

        Yields validated `FacebookCompanyAdsAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.company_ads",
            dict(input),
            "ads",
            item_model=FacebookCompanyAdsAd,
            data_model=FacebookCompanyAdsData,
            bare=False,
            options=options,
        )

    def event_details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventDetailsInput],
    ) -> RunResult[FacebookEventDetailsData]:
        """Facebook Event Details

        Fetch full details for a single Facebook event by ID or URL (name, schedule,
        venue, hosts, and attendance) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.event_details(id="4045709448982422")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.event_details", dict(input), options
        )
        return RunResult[FacebookEventDetailsData].model_validate(raw)

    def events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsInput],
    ) -> RunResult[FacebookEventsData]:
        """Facebook Events

        List public Facebook events for a city or place by its events-page URL
        (event name, date, venue, and attendance) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.events(url="https://www.facebook.com/events/explore/saint-petersburg-florida/111326725552547")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.events", dict(input), options
        )
        return RunResult[FacebookEventsData].model_validate(raw)

    def iter_events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsInput],
    ) -> Paginator[FacebookEventsEvent, FacebookEventsData]:
        """Iterate Facebook Events results, following pagination cursors.

        Yields validated `FacebookEventsEvent` items from the `events` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.events",
            dict(input),
            "events",
            item_model=FacebookEventsEvent,
            data_model=FacebookEventsData,
            bare=False,
            options=options,
        )

    def events_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsSearchInput],
    ) -> RunResult[FacebookEventsSearchData]:
        """Facebook Events Search

        Search public Facebook events by keyword and get structured event records
        (name, schedule, venue, pricing, and attendance) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.events_search(query="music festival")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.events_search", dict(input), options
        )
        return RunResult[FacebookEventsSearchData].model_validate(raw)

    def iter_events_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsSearchInput],
    ) -> Paginator[FacebookEventsSearchEvent, FacebookEventsSearchData]:
        """Iterate Facebook Events Search results, following pagination cursors.

        Yields validated `FacebookEventsSearchEvent` items from the `events` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.events_search",
            dict(input),
            "events",
            item_model=FacebookEventsSearchEvent,
            data_model=FacebookEventsSearchData,
            bare=False,
            options=options,
        )

    def followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookFollowersInput],
    ) -> RunResult[FacebookFollowersData]:
        """Facebook Followers

        List the public followers (or accounts followed) of any Facebook page or
        profile URL as normalized JSON records.

        Price: $0.03 per request plus $0.0045 per result (maximum $0.12).

        Example:
            res = client.facebook.followers(limit=3, url="https://www.facebook.com/nike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.followers", dict(input), options
        )
        return RunResult[FacebookFollowersData].model_validate(raw)

    def group_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookGroupPostsInput],
    ) -> RunResult[FacebookGroupPostsData]:
        """Facebook Group Posts

        Fetch recent posts from any public Facebook group by URL: text, author,
        reactions, and comment counts.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.group_posts(url="https://www.facebook.com/groups/instantpotcommunity/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.group_posts", dict(input), options
        )
        return RunResult[FacebookGroupPostsData].model_validate(raw)

    def iter_group_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookGroupPostsInput],
    ) -> Paginator[FacebookGroupPostsPost, FacebookGroupPostsData]:
        """Iterate Facebook Group Posts results, following pagination cursors.

        Yields validated `FacebookGroupPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.group_posts",
            dict(input),
            "posts",
            item_model=FacebookGroupPostsPost,
            data_model=FacebookGroupPostsData,
            bare=False,
            options=options,
        )

    def marketplace(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceInput],
    ) -> RunResult[FacebookMarketplaceData]:
        """Facebook Marketplace

        Search Facebook Marketplace listings by keyword near a location, filter by
        price, condition, delivery, recency, and availability, and get title, price,
        location, and image as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.marketplace(lat="30.2677", lng="-97.7475", priceMax=500, priceMin=100, query="bike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.marketplace", dict(input), options
        )
        return RunResult[FacebookMarketplaceData].model_validate(raw)

    def iter_marketplace(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceInput],
    ) -> Paginator[FacebookMarketplaceListing, FacebookMarketplaceData]:
        """Iterate Facebook Marketplace results, following pagination cursors.

        Yields validated `FacebookMarketplaceListing` items from the `listings` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.marketplace",
            dict(input),
            "listings",
            item_model=FacebookMarketplaceListing,
            data_model=FacebookMarketplaceData,
            bare=False,
            options=options,
        )

    def marketplace_item(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceItemInput],
    ) -> RunResult[FacebookMarketplaceItemData]:
        """Facebook Marketplace Item

        Fetch full details for a single Facebook Marketplace listing by ID or URL
        (title, price, location, photos, and attributes) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.marketplace_item(url="https://www.facebook.com/marketplace/item/1656586118821988/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.marketplace_item", dict(input), options
        )
        return RunResult[FacebookMarketplaceItemData].model_validate(raw)

    def marketplace_location_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceLocationSearchInput],
    ) -> RunResult[FacebookMarketplaceLocationSearchData]:
        """Facebook Marketplace Location Search

        Resolve a place name to Facebook Marketplace locations with coordinates and
        metadata as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.marketplace_location_search(query="Austin")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.marketplace_location_search", dict(input), options
        )
        return RunResult[FacebookMarketplaceLocationSearchData].model_validate(raw)

    def page_contact(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPageContactInput],
    ) -> RunResult[FacebookPageContactData]:
        """Facebook Page Contact Info

        Look up a Facebook Page's public contact details (email, phone, website, and
        address) by page URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.page_contact(page="https://www.facebook.com/joesstonecrab")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.page_contact", dict(input), options
        )
        return RunResult[FacebookPageContactData].model_validate(raw)

    def page_lookup(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPageLookupInput],
    ) -> RunResult[FacebookPageLookupData]:
        """Facebook Page Lookup

        Look up Facebook Pages and profiles by name with Facebook's own quick
        search. A name lookup that returns basic identity fields only: name, URL,
        profile image, Facebook id, and verified status. Matches can include
        personal profiles as well as Pages. For full Page details (category,
        followers, phone, website), use facebook.search_pages.

        Price: $0.00975 per request.

        Example:
            res = client.facebook.page_lookup(limit=5, query="NASA")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.page_lookup", dict(input), options
        )
        return RunResult[FacebookPageLookupData].model_validate(raw)

    def photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPhotosInput],
    ) -> RunResult[FacebookPhotosData]:
        """Facebook Page Photos

        Fetch recent photos posted by any public Facebook page or profile (image
        URLs, captions, and dimensions) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.photos(url="https://www.facebook.com/Spurs")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.photos", dict(input), options
        )
        return RunResult[FacebookPhotosData].model_validate(raw)

    def iter_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPhotosInput],
    ) -> Paginator[FacebookPhotosPhoto, FacebookPhotosData]:
        """Iterate Facebook Page Photos results, following pagination cursors.

        Yields validated `FacebookPhotosPhoto` items from the `photos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.photos",
            dict(input),
            "photos",
            item_model=FacebookPhotosPhoto,
            data_model=FacebookPhotosData,
            bare=False,
            options=options,
        )

    def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostInput],
    ) -> RunResult[FacebookPostData]:
        """Facebook Post

        Fetch a single Facebook post by URL with its text and engagement counts
        (likes, comments, shares, views).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.post(url="https://www.facebook.com/reel/2166091230582141/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.post", dict(input), options
        )
        return RunResult[FacebookPostData].model_validate(raw)

    def post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostCommentsInput],
    ) -> RunResult[FacebookPostCommentsData]:
        """Facebook Post Comments

        List the comments on a Facebook post by URL with cursor pagination (text,
        author, reactions, reply count).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.post_comments(url="https://www.facebook.com/reel/2166091230582141/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.post_comments", dict(input), options
        )
        return RunResult[FacebookPostCommentsData].model_validate(raw)

    def iter_post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostCommentsInput],
    ) -> Paginator[FacebookPostCommentsComment, FacebookPostCommentsData]:
        """Iterate Facebook Post Comments results, following pagination cursors.

        Yields validated `FacebookPostCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.post_comments",
            dict(input),
            "comments",
            item_model=FacebookPostCommentsComment,
            data_model=FacebookPostCommentsData,
            bare=False,
            options=options,
        )

    def post_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostTranscriptInput],
    ) -> RunResult[FacebookPostTranscriptData]:
        """Facebook Post Transcript

        Get the spoken-word transcript of any public Facebook video post by URL as
        normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.post_transcript(url="https://www.facebook.com/reel/2166091230582141/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.post_transcript", dict(input), options
        )
        return RunResult[FacebookPostTranscriptData].model_validate(raw)

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileInput],
    ) -> RunResult[FacebookProfileData]:
        """Facebook Profile

        Fetch a Facebook page's public profile (likes, followers, category, about)
        by URL or handle.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile(url="https://www.facebook.com/nike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile", dict(input), options
        )
        return RunResult[FacebookProfileData].model_validate(raw)

    def profile_events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileEventsInput],
    ) -> RunResult[FacebookProfileEventsData]:
        """Facebook Page Events

        List upcoming and past events hosted by any public Facebook page by URL
        (name, schedule, venue, and host) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile_events(url="https://www.facebook.com/brickyardoldtown")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile_events", dict(input), options
        )
        return RunResult[FacebookProfileEventsData].model_validate(raw)

    def iter_profile_events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileEventsInput],
    ) -> Paginator[FacebookProfileEventsEvent, FacebookProfileEventsData]:
        """Iterate Facebook Page Events results, following pagination cursors.

        Yields validated `FacebookProfileEventsEvent` items from the `events` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.profile_events",
            dict(input),
            "events",
            item_model=FacebookProfileEventsEvent,
            data_model=FacebookProfileEventsData,
            bare=False,
            options=options,
        )

    def profile_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfilePostsInput],
    ) -> RunResult[FacebookProfilePostsData]:
        """Facebook Profile Posts

        List a Facebook page's recent posts by URL or page id with cursor pagination
        (text, author, publication time, permalink).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile_posts(url="https://www.facebook.com/nike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile_posts", dict(input), options
        )
        return RunResult[FacebookProfilePostsData].model_validate(raw)

    def iter_profile_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfilePostsInput],
    ) -> Paginator[FacebookProfilePostsPost, FacebookProfilePostsData]:
        """Iterate Facebook Profile Posts results, following pagination cursors.

        Yields validated `FacebookProfilePostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.profile_posts",
            dict(input),
            "posts",
            item_model=FacebookProfilePostsPost,
            data_model=FacebookProfilePostsData,
            bare=False,
            options=options,
        )

    def profile_reels(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileReelsInput],
    ) -> RunResult[FacebookProfileReelsData]:
        """Facebook Profile Reels

        List a Facebook page's reels by URL with cursor pagination (caption, view
        count, permalink, thumbnail).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile_reels(url="https://www.facebook.com/nike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile_reels", dict(input), options
        )
        return RunResult[FacebookProfileReelsData].model_validate(raw)

    def iter_profile_reels(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileReelsInput],
    ) -> Paginator[FacebookProfileReelsReel, FacebookProfileReelsData]:
        """Iterate Facebook Profile Reels results, following pagination cursors.

        Yields validated `FacebookProfileReelsReel` items from the `reels` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "facebook.profile_reels",
            dict(input),
            "reels",
            item_model=FacebookProfileReelsReel,
            data_model=FacebookProfileReelsData,
            bare=False,
            options=options,
        )

    def search_companies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookSearchCompaniesInput],
    ) -> RunResult[FacebookSearchCompaniesData]:
        """Facebook Company Search

        Search the Meta Ad Library for advertisers by keyword and get matching
        pages: page ID, category, verification, follower counts, and linked
        Instagram.

        Price: $0.0011 per request.

        Example:
            res = client.facebook.search_companies(query="nike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.search_companies", dict(input), options
        )
        return RunResult[FacebookSearchCompaniesData].model_validate(raw)

    def search_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookSearchPagesInput],
    ) -> RunResult[FacebookSearchPagesData]:
        """Facebook Page Search

        Search Facebook Pages by keyword, optionally narrowed to a location, and get
        structured page profiles (name, category, followers, contact details).

        Price: $0.0011 per request plus $0.0121 per result (maximum $0.123).

        Example:
            res = client.facebook.search_pages(limit=3, query="nike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.search_pages", dict(input), options
        )
        return RunResult[FacebookSearchPagesData].model_validate(raw)

    def search_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookSearchPostsInput],
    ) -> RunResult[FacebookSearchPostsData]:
        """Facebook Post Search

        Search public Facebook posts by keyword, optionally filtered by location,
        and get structured post records (text, author, engagement).

        Price: $0.03 per request.

        Example:
            res = client.facebook.search_posts(limit=3, query="nike")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.search_posts", dict(input), options
        )
        return RunResult[FacebookSearchPostsData].model_validate(raw)


class AsyncFacebookNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ad_details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdDetailsInput],
    ) -> RunResult[FacebookAdDetailsData]:
        """Facebook Ad Details

        Look up a single Meta Ad Library ad by ID or URL and get the advertiser,
        creative text, call-to-action, platforms, and run dates as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.ad_details(id="962050096457659")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ad_details", dict(input), options
        )
        return RunResult[FacebookAdDetailsData].model_validate(raw)

    async def ad_details_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdDetailsFullInput],
    ) -> RunResult[FacebookAdDetailsFullData]:
        """Facebook Ad Creative Details

        Pull one Meta Ad Library ad with its creative: every carousel variant, image
        and video URL, headline, body, and call to action.

        Price: $0.00462 per request plus $0 per result (maximum $0.00462).

        Example:
            res = client.facebook.ad_details_full(id="962050096457659")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ad_details_full", dict(input), options
        )
        return RunResult[FacebookAdDetailsFullData].model_validate(raw)

    async def ad_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdTranscriptInput],
    ) -> RunResult[FacebookAdTranscriptData]:
        """Facebook Ad Transcript

        Get the spoken-word transcript of a Meta Ad Library video ad by ad ID or
        URL.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.ad_transcript(id="931919822778200")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ad_transcript", dict(input), options
        )
        return RunResult[FacebookAdTranscriptData].model_validate(raw)

    async def ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdsSearchInput],
    ) -> RunResult[FacebookAdsSearchData]:
        """Facebook Ad Search

        Search the Meta Ad Library by keyword and get matching ads (advertiser,
        creative text, CTA, platforms, and run dates) with cursor pagination.

        Price: $0.0011 per request.

        Example:
            res = client.facebook.ads_search(country="US", query="nike", searchType="keyword_exact_phrase")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.ads_search", dict(input), options
        )
        return RunResult[FacebookAdsSearchData].model_validate(raw)

    def iter_ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookAdsSearchInput],
    ) -> AsyncPaginator[FacebookAdsSearchAd, FacebookAdsSearchData]:
        """Iterate Facebook Ad Search results, following pagination cursors.

        Yields validated `FacebookAdsSearchAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.ads_search",
            dict(input),
            "ads",
            item_model=FacebookAdsSearchAd,
            data_model=FacebookAdsSearchData,
            bare=False,
            options=options,
        )

    async def comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCommentRepliesInput],
    ) -> RunResult[FacebookCommentRepliesData]:
        """Facebook Comment Replies

        List the replies to a Facebook post comment (text, author, reactions, and
        timestamps) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.comment_replies(expansionToken="MjoxNzgzMjI4OTY4OgF_o5zrjDnpemv4bwPtpsShXutqvKIw2bKs2YuJksL1Ak8n8YG-_KPSQGkIks5oW6wdRfhb_cRv9q5OX0NHjFJwEupYNZi9pcMV-FYLWLp47u-eusMkZFOMwbkISsTln7gtSvQrOzlffyavOTIL85PECYzGfunU2IAEkd13CIikxu06Mw10UJ1ShcFAmz8175R1uJfYy_iOixWZukqfrWhUfVOXApXznxx7qXvUxPwct76qe6p7-nVWQrPC_SZc2xh9Z8ggL3WMjgTzSq4oWFSsyZuuVsyVVjSgdjRQiDqtJSeEUlSjTr6vOnKsvKV-GpnBRaeA0BCaNRhqpB4xDZoduBuO5ZYrFvWLJdJLryDhCPI2Ss-Z33cEM2Vz7pLf1wJzE7TuizXPwICSn1DA_Prca-BItTbOUjAjfiySap1LXYkGuuDC2ziUdiEsmE5XhevMP8XtF_2WQlMNcGbXMEQyAWDUawtPAxXgMeRrCO9YGSweFQ4OZumoIlSGa3Vfjy-euUOHT1IAsNbV2A8rAq4HJNU3jCXQTn0vfW9xvbVQhL-53Mhw2YPjhlvUj6QpnGA25N8", feedbackId="ZmVlZGJhY2s6MTM5MzQ2MTExNTQ4MTkyN18yMDgyNjUzMjQ1ODA5Mzg2")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.comment_replies", dict(input), options
        )
        return RunResult[FacebookCommentRepliesData].model_validate(raw)

    def iter_comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCommentRepliesInput],
    ) -> AsyncPaginator[FacebookCommentRepliesReplie, FacebookCommentRepliesData]:
        """Iterate Facebook Comment Replies results, following pagination cursors.

        Yields validated `FacebookCommentRepliesReplie` items from the `replies` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.comment_replies",
            dict(input),
            "replies",
            item_model=FacebookCommentRepliesReplie,
            data_model=FacebookCommentRepliesData,
            bare=False,
            options=options,
        )

    async def company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCompanyAdsInput],
    ) -> RunResult[FacebookCompanyAdsData]:
        """Facebook Company Ads

        List the Meta Ad Library ads a company is running by page ID or company name
        (creative text, format, platforms, and run dates) with cursor pagination.

        Price: $0.0011 per request.

        Example:
            res = client.facebook.company_ads(pageId="15087023444", sortBy="recent")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.company_ads", dict(input), options
        )
        return RunResult[FacebookCompanyAdsData].model_validate(raw)

    def iter_company_ads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookCompanyAdsInput],
    ) -> AsyncPaginator[FacebookCompanyAdsAd, FacebookCompanyAdsData]:
        """Iterate Facebook Company Ads results, following pagination cursors.

        Yields validated `FacebookCompanyAdsAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.company_ads",
            dict(input),
            "ads",
            item_model=FacebookCompanyAdsAd,
            data_model=FacebookCompanyAdsData,
            bare=False,
            options=options,
        )

    async def event_details(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventDetailsInput],
    ) -> RunResult[FacebookEventDetailsData]:
        """Facebook Event Details

        Fetch full details for a single Facebook event by ID or URL (name, schedule,
        venue, hosts, and attendance) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.event_details(id="4045709448982422")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.event_details", dict(input), options
        )
        return RunResult[FacebookEventDetailsData].model_validate(raw)

    async def events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsInput],
    ) -> RunResult[FacebookEventsData]:
        """Facebook Events

        List public Facebook events for a city or place by its events-page URL
        (event name, date, venue, and attendance) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.events(url="https://www.facebook.com/events/explore/saint-petersburg-florida/111326725552547")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.events", dict(input), options
        )
        return RunResult[FacebookEventsData].model_validate(raw)

    def iter_events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsInput],
    ) -> AsyncPaginator[FacebookEventsEvent, FacebookEventsData]:
        """Iterate Facebook Events results, following pagination cursors.

        Yields validated `FacebookEventsEvent` items from the `events` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.events",
            dict(input),
            "events",
            item_model=FacebookEventsEvent,
            data_model=FacebookEventsData,
            bare=False,
            options=options,
        )

    async def events_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsSearchInput],
    ) -> RunResult[FacebookEventsSearchData]:
        """Facebook Events Search

        Search public Facebook events by keyword and get structured event records
        (name, schedule, venue, pricing, and attendance) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.events_search(query="music festival")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.events_search", dict(input), options
        )
        return RunResult[FacebookEventsSearchData].model_validate(raw)

    def iter_events_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookEventsSearchInput],
    ) -> AsyncPaginator[FacebookEventsSearchEvent, FacebookEventsSearchData]:
        """Iterate Facebook Events Search results, following pagination cursors.

        Yields validated `FacebookEventsSearchEvent` items from the `events` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.events_search",
            dict(input),
            "events",
            item_model=FacebookEventsSearchEvent,
            data_model=FacebookEventsSearchData,
            bare=False,
            options=options,
        )

    async def followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookFollowersInput],
    ) -> RunResult[FacebookFollowersData]:
        """Facebook Followers

        List the public followers (or accounts followed) of any Facebook page or
        profile URL as normalized JSON records.

        Price: $0.03 per request plus $0.0045 per result (maximum $0.12).

        Example:
            res = client.facebook.followers(limit=3, url="https://www.facebook.com/nike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.followers", dict(input), options
        )
        return RunResult[FacebookFollowersData].model_validate(raw)

    async def group_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookGroupPostsInput],
    ) -> RunResult[FacebookGroupPostsData]:
        """Facebook Group Posts

        Fetch recent posts from any public Facebook group by URL: text, author,
        reactions, and comment counts.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.group_posts(url="https://www.facebook.com/groups/instantpotcommunity/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.group_posts", dict(input), options
        )
        return RunResult[FacebookGroupPostsData].model_validate(raw)

    def iter_group_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookGroupPostsInput],
    ) -> AsyncPaginator[FacebookGroupPostsPost, FacebookGroupPostsData]:
        """Iterate Facebook Group Posts results, following pagination cursors.

        Yields validated `FacebookGroupPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.group_posts",
            dict(input),
            "posts",
            item_model=FacebookGroupPostsPost,
            data_model=FacebookGroupPostsData,
            bare=False,
            options=options,
        )

    async def marketplace(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceInput],
    ) -> RunResult[FacebookMarketplaceData]:
        """Facebook Marketplace

        Search Facebook Marketplace listings by keyword near a location, filter by
        price, condition, delivery, recency, and availability, and get title, price,
        location, and image as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.marketplace(lat="30.2677", lng="-97.7475", priceMax=500, priceMin=100, query="bike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.marketplace", dict(input), options
        )
        return RunResult[FacebookMarketplaceData].model_validate(raw)

    def iter_marketplace(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceInput],
    ) -> AsyncPaginator[FacebookMarketplaceListing, FacebookMarketplaceData]:
        """Iterate Facebook Marketplace results, following pagination cursors.

        Yields validated `FacebookMarketplaceListing` items from the `listings` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.marketplace",
            dict(input),
            "listings",
            item_model=FacebookMarketplaceListing,
            data_model=FacebookMarketplaceData,
            bare=False,
            options=options,
        )

    async def marketplace_item(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceItemInput],
    ) -> RunResult[FacebookMarketplaceItemData]:
        """Facebook Marketplace Item

        Fetch full details for a single Facebook Marketplace listing by ID or URL
        (title, price, location, photos, and attributes) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.marketplace_item(url="https://www.facebook.com/marketplace/item/1656586118821988/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.marketplace_item", dict(input), options
        )
        return RunResult[FacebookMarketplaceItemData].model_validate(raw)

    async def marketplace_location_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookMarketplaceLocationSearchInput],
    ) -> RunResult[FacebookMarketplaceLocationSearchData]:
        """Facebook Marketplace Location Search

        Resolve a place name to Facebook Marketplace locations with coordinates and
        metadata as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.marketplace_location_search(query="Austin")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.marketplace_location_search", dict(input), options
        )
        return RunResult[FacebookMarketplaceLocationSearchData].model_validate(raw)

    async def page_contact(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPageContactInput],
    ) -> RunResult[FacebookPageContactData]:
        """Facebook Page Contact Info

        Look up a Facebook Page's public contact details (email, phone, website, and
        address) by page URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.page_contact(page="https://www.facebook.com/joesstonecrab")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.page_contact", dict(input), options
        )
        return RunResult[FacebookPageContactData].model_validate(raw)

    async def page_lookup(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPageLookupInput],
    ) -> RunResult[FacebookPageLookupData]:
        """Facebook Page Lookup

        Look up Facebook Pages and profiles by name with Facebook's own quick
        search. A name lookup that returns basic identity fields only: name, URL,
        profile image, Facebook id, and verified status. Matches can include
        personal profiles as well as Pages. For full Page details (category,
        followers, phone, website), use facebook.search_pages.

        Price: $0.00975 per request.

        Example:
            res = client.facebook.page_lookup(limit=5, query="NASA")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.page_lookup", dict(input), options
        )
        return RunResult[FacebookPageLookupData].model_validate(raw)

    async def photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPhotosInput],
    ) -> RunResult[FacebookPhotosData]:
        """Facebook Page Photos

        Fetch recent photos posted by any public Facebook page or profile (image
        URLs, captions, and dimensions) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.photos(url="https://www.facebook.com/Spurs")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.photos", dict(input), options
        )
        return RunResult[FacebookPhotosData].model_validate(raw)

    def iter_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPhotosInput],
    ) -> AsyncPaginator[FacebookPhotosPhoto, FacebookPhotosData]:
        """Iterate Facebook Page Photos results, following pagination cursors.

        Yields validated `FacebookPhotosPhoto` items from the `photos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.photos",
            dict(input),
            "photos",
            item_model=FacebookPhotosPhoto,
            data_model=FacebookPhotosData,
            bare=False,
            options=options,
        )

    async def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostInput],
    ) -> RunResult[FacebookPostData]:
        """Facebook Post

        Fetch a single Facebook post by URL with its text and engagement counts
        (likes, comments, shares, views).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.post(url="https://www.facebook.com/reel/2166091230582141/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.post", dict(input), options
        )
        return RunResult[FacebookPostData].model_validate(raw)

    async def post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostCommentsInput],
    ) -> RunResult[FacebookPostCommentsData]:
        """Facebook Post Comments

        List the comments on a Facebook post by URL with cursor pagination (text,
        author, reactions, reply count).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.post_comments(url="https://www.facebook.com/reel/2166091230582141/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.post_comments", dict(input), options
        )
        return RunResult[FacebookPostCommentsData].model_validate(raw)

    def iter_post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostCommentsInput],
    ) -> AsyncPaginator[FacebookPostCommentsComment, FacebookPostCommentsData]:
        """Iterate Facebook Post Comments results, following pagination cursors.

        Yields validated `FacebookPostCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.post_comments",
            dict(input),
            "comments",
            item_model=FacebookPostCommentsComment,
            data_model=FacebookPostCommentsData,
            bare=False,
            options=options,
        )

    async def post_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookPostTranscriptInput],
    ) -> RunResult[FacebookPostTranscriptData]:
        """Facebook Post Transcript

        Get the spoken-word transcript of any public Facebook video post by URL as
        normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.post_transcript(url="https://www.facebook.com/reel/2166091230582141/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.post_transcript", dict(input), options
        )
        return RunResult[FacebookPostTranscriptData].model_validate(raw)

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileInput],
    ) -> RunResult[FacebookProfileData]:
        """Facebook Profile

        Fetch a Facebook page's public profile (likes, followers, category, about)
        by URL or handle.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile(url="https://www.facebook.com/nike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile", dict(input), options
        )
        return RunResult[FacebookProfileData].model_validate(raw)

    async def profile_events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileEventsInput],
    ) -> RunResult[FacebookProfileEventsData]:
        """Facebook Page Events

        List upcoming and past events hosted by any public Facebook page by URL
        (name, schedule, venue, and host) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile_events(url="https://www.facebook.com/brickyardoldtown")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile_events", dict(input), options
        )
        return RunResult[FacebookProfileEventsData].model_validate(raw)

    def iter_profile_events(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileEventsInput],
    ) -> AsyncPaginator[FacebookProfileEventsEvent, FacebookProfileEventsData]:
        """Iterate Facebook Page Events results, following pagination cursors.

        Yields validated `FacebookProfileEventsEvent` items from the `events` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.profile_events",
            dict(input),
            "events",
            item_model=FacebookProfileEventsEvent,
            data_model=FacebookProfileEventsData,
            bare=False,
            options=options,
        )

    async def profile_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfilePostsInput],
    ) -> RunResult[FacebookProfilePostsData]:
        """Facebook Profile Posts

        List a Facebook page's recent posts by URL or page id with cursor pagination
        (text, author, publication time, permalink).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile_posts(url="https://www.facebook.com/nike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile_posts", dict(input), options
        )
        return RunResult[FacebookProfilePostsData].model_validate(raw)

    def iter_profile_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfilePostsInput],
    ) -> AsyncPaginator[FacebookProfilePostsPost, FacebookProfilePostsData]:
        """Iterate Facebook Profile Posts results, following pagination cursors.

        Yields validated `FacebookProfilePostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.profile_posts",
            dict(input),
            "posts",
            item_model=FacebookProfilePostsPost,
            data_model=FacebookProfilePostsData,
            bare=False,
            options=options,
        )

    async def profile_reels(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileReelsInput],
    ) -> RunResult[FacebookProfileReelsData]:
        """Facebook Profile Reels

        List a Facebook page's reels by URL with cursor pagination (caption, view
        count, permalink, thumbnail).

        Price: $0.0012 per request.

        Example:
            res = client.facebook.profile_reels(url="https://www.facebook.com/nike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.profile_reels", dict(input), options
        )
        return RunResult[FacebookProfileReelsData].model_validate(raw)

    def iter_profile_reels(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookProfileReelsInput],
    ) -> AsyncPaginator[FacebookProfileReelsReel, FacebookProfileReelsData]:
        """Iterate Facebook Profile Reels results, following pagination cursors.

        Yields validated `FacebookProfileReelsReel` items from the `reels` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "facebook.profile_reels",
            dict(input),
            "reels",
            item_model=FacebookProfileReelsReel,
            data_model=FacebookProfileReelsData,
            bare=False,
            options=options,
        )

    async def search_companies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookSearchCompaniesInput],
    ) -> RunResult[FacebookSearchCompaniesData]:
        """Facebook Company Search

        Search the Meta Ad Library for advertisers by keyword and get matching
        pages: page ID, category, verification, follower counts, and linked
        Instagram.

        Price: $0.0011 per request.

        Example:
            res = client.facebook.search_companies(query="nike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.search_companies", dict(input), options
        )
        return RunResult[FacebookSearchCompaniesData].model_validate(raw)

    async def search_pages(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookSearchPagesInput],
    ) -> RunResult[FacebookSearchPagesData]:
        """Facebook Page Search

        Search Facebook Pages by keyword, optionally narrowed to a location, and get
        structured page profiles (name, category, followers, contact details).

        Price: $0.0011 per request plus $0.0121 per result (maximum $0.123).

        Example:
            res = client.facebook.search_pages(limit=3, query="nike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.search_pages", dict(input), options
        )
        return RunResult[FacebookSearchPagesData].model_validate(raw)

    async def search_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[FacebookSearchPostsInput],
    ) -> RunResult[FacebookSearchPostsData]:
        """Facebook Post Search

        Search public Facebook posts by keyword, optionally filtered by location,
        and get structured post records (text, author, engagement).

        Price: $0.03 per request.

        Example:
            res = client.facebook.search_posts(limit=3, query="nike")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "facebook.search_posts", dict(input), options
        )
        return RunResult[FacebookSearchPostsData].model_validate(raw)
