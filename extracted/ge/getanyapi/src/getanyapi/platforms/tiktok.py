# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the tiktok platform."""

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


class TiktokAdLibraryAdInput(TypedDict, total=False):
    """Input for TikTok Ad Library Ad."""

    adId: Required[str]
    """TikTok Top Ads material/ad ID, or a Top Ads detail URL (e.g. 7648493525660270600)."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokAdLibrarySearchInput(TypedDict, total=False):
    """Input for TikTok Ad Library Search."""

    advertiserName: NotRequired[str]
    """Advertiser name to list ads for (e.g. Spotify). Provide advertiserName or query, never both."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque cursor from a previous response's nextCursor. Omit it for the first page."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: NotRequired[str]
    """Keyword to search ad titles and content (e.g. spotify). Provide query or advertiserName, never both."""
    region: NotRequired[str]
    """Two-letter region code for TikTok's Commercial Content Library, such as DE, FR, GB or IT. Each region holds a different set of ads. Omit it to take the library's own default region, DE. Coverage is the EU and EEA; a non-EU code such as US is not served."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokAdTransparencySearchInput(TypedDict, total=False):
    """Input for TikTok Ad Transparency Search."""

    advertiserId: NotRequired[str]
    """TikTok Commercial Content Library advertiser ID. Provide advertiserId or query."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Search cursor from a previous response's nextCursor."""
    days: NotRequired[int]
    """Number of days of Commercial Content Library history to search, from 1 to 365. Defaults to 30. Range: 1 to 365. Default: 30."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of ads to return, from 1 to 50. Defaults to 20. Billing is flat per request. Range: 1 to 50. Default: 20."""
    offset: NotRequired[int]
    """Zero-based result offset. Defaults to 0. Minimum: 0. Default: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: NotRequired[str]
    """Keyword to search in TikTok's EU Commercial Content Library. Provide query or advertiserId."""
    region: NotRequired[str]
    """Region code for the transparency search. Defaults to DE. Default: DE."""
    sort: NotRequired[str]
    """Upstream sort expression. Defaults to last_shown_date,desc. Default: last_shown_date,desc."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokAudienceDemographicsInput(TypedDict, total=False):
    """Input for TikTok Audience Demographics."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """TikTok username without the leading @ (e.g. "shakira")."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokCommentRepliesInput(TypedDict, total=False):
    """Input for TikTok Comment Replies."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    commentId: Required[str]
    """TikTok comment ID (the comment's cid from the comments endpoint)."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["authorUserId"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `authorUserId`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a reply that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """TikTok video URL the comment belongs to."""


class TiktokFollowersInput(TypedDict, total=False):
    """Input for TikTok Followers."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor, to fetch the next page of followers."""
    handle: Required[str]
    """TikTok username whose followers to list, without the @ prefix (e.g. stoolpresidente)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[Literal["likeCount", "nextCursor", "secUid", "videoCount"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `videoCount` or `secUid`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a follower that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokFollowingInput(TypedDict, total=False):
    """Input for TikTok Following."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    handle: Required[str]
    """TikTok username without the leading @ (e.g. "stoolpresidente")."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireCursor: NotRequired[bool]
    """Deprecated; send `requireFields: ["nextCursor"]` instead, which does exactly the same thing. Set true if you intend to page through results, so the request is only served by a source that can return a nextCursor. Omit it and routing is unchanged, with the cheapest source serving. This can raise your price: when the cheapest source cannot page, a source that can serves, and you are quoted and charged its price. It stays accepted so callers that already send it keep working."""
    requireFields: NotRequired[
        list[Literal["instagramUrl", "nextCursor", "secUid", "youtubeUrl"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `secUid` or `instagramUrl`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokHashtagVideosInput(TypedDict, total=False):
    """Input for TikTok Hashtag Videos."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of videos."""
    hashtag: Required[str]
    """TikTok hashtag to fetch videos for, without the # prefix (e.g. booktok)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-20, default 20). Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "commentCount",
                "likeCount",
                "nextCursor",
                "playCount",
                "shareCount",
                "soundAuthor",
                "soundClipId",
                "soundTitle",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `playCount`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a video that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. A source that returns only a rounded or shortened value for a field does not count as returning it. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokLiveInput(TypedDict, total=False):
    """Input for TikTok Live."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """TikTok username without the leading @ (e.g. "thejustalex")."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokPhotosInput(TypedDict, total=False):
    """Input for TikTok Photos."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["authorFollowers"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `authorFollowers`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full TikTok photo-mode post URL. TikTok serves slideshow posts under the same /video/<id> path as videos, so the normal share link works."""


class TiktokPlaylistVideosInput(TypedDict, total=False):
    """Input for TikTok Playlist Videos."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    id: NotRequired[str]
    """TikTok playlist id. Use it when tiktok.profile_playlists handed you the id."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum items to return in one page. Range: 1 to 30. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Full TikTok playlist URL. The playlist id is the numeric run at the end."""


class TiktokProfileInput(TypedDict, total=False):
    """Input for TikTok Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """TikTok username without the leading @ (e.g. "stoolpresidente")."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["createdUtc"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `createdUtc`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an account that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokProfileContactInput(TypedDict, total=False):
    """Input for TikTok Profile Contact Info."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """TikTok username without the leading @."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["domain", "sourceUrl"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `domain` or `sourceUrl`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokProfilePlaylistsInput(TypedDict, total=False):
    """Input for TikTok Profile Playlists."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum items to return in one page. Range: 1 to 30. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    secUid: Required[str]
    """TikTok's opaque sec_uid for the account. TikTok's own endpoint keys on it and will not accept a handle; call tiktok.profile with the handle first and read secUid off its response."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokProfileRegionInput(TypedDict, total=False):
    """Input for TikTok Profile Region."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """TikTok username without the leading @ (e.g. "stoolpresidente")."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokProfileRepostsInput(TypedDict, total=False):
    """Input for TikTok Profile Reposts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum items to return in one page. Range: 1 to 30. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    secUid: Required[str]
    """TikTok's opaque sec_uid for the account. TikTok's own endpoint keys on it and will not accept a handle; call tiktok.profile with the handle first and read secUid off its response."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokProfileVideosInput(TypedDict, total=False):
    """Input for TikTok Profile Videos."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    handle: Required[str]
    """TikTok username without the leading @."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "authorFollowers",
                "authorVerified",
                "locationName",
                "nextCursor",
                "paidPartnership",
                "soundAuthor",
                "soundTitle",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a video that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSearchHashtagInput(TypedDict, total=False):
    """Input for TikTok Hashtag Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Hashtag or keyword to search for (without the leading #)."""
    requireFields: NotRequired[
        list[Literal["locationName", "soundAuthor", "soundTitle"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `soundTitle` or `locationName`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a video that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSearchKeywordInput(TypedDict, total=False):
    """Input for TikTok Keyword Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    datePosted: NotRequired[Any]
    """Time frame filter, in days back from now. Use a canonical JSON integer that is nonnegative: 0 for any time, 1 for the past 24 hours, 7 for the past week, 30 for the past month, 90 for the past three months, or 180 for the past six months. Any other number is not guaranteed to filter anything. Legacy numeric strings remain accepted."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The keyword to search TikTok for."""
    requireCursor: NotRequired[bool]
    """Deprecated: name `nextCursor` in `requireFields` instead, which is the field this flag is translated into. It stays accepted so callers that already send it keep working. Sending it routes you to a source that returns a pagination cursor, which can raise your price when the cheapest source cannot page."""
    requireFields: NotRequired[
        list[
            Literal[
                "authorFollowers",
                "authorVerified",
                "locationName",
                "nextCursor",
                "paidPartnership",
                "soundAuthor",
                "soundTitle",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sortBy: NotRequired[Literal["relevance", "most-liked", "date-posted"]]
    """Sort order: relevance, most-liked, date-posted. Default: relevance."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSearchPhotosInput(TypedDict, total=False):
    """Input for TikTok Photo Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum items to return in one page. Range: 1 to 30. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSearchSuggestionsInput(TypedDict, total=False):
    """Input for TikTok Search Suggestions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Seed keyword to expand."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSearchTopInput(TypedDict, total=False):
    """Input for TikTok Top Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    publishTime: NotRequired[
        Literal[
            "yesterday",
            "this-week",
            "this-month",
            "last-3-months",
            "last-6-months",
            "all-time",
        ]
    ]
    """Time-frame filter: yesterday, this-week, this-month, last-3-months, last-6-months, all-time."""
    query: Required[str]
    """Keyword to search for (e.g. "funny")."""
    region: NotRequired[str]
    """2-letter country code for the proxy location (e.g. US, GB, FR)."""
    requireFields: NotRequired[
        list[
            Literal[
                "authorFollowers",
                "contentType",
                "nextCursor",
                "soundAuthor",
                "soundClipId",
                "soundTitle",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `soundClipId` or `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sortBy: NotRequired[Literal["relevance", "most-liked", "date-posted"]]
    """Sort order: relevance, most-liked, date-posted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSearchUsersInput(TypedDict, total=False):
    """Input for TikTok User Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The keyword to search TikTok accounts for."""
    requireFields: NotRequired[
        list[
            Literal[
                "bio", "instagramUrl", "nextCursor", "region", "secUid", "youtubeUrl"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `secUid` or `bio`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSongInput(TypedDict, total=False):
    """Input for TikTok Song."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    clipId: Required[str]
    """The clip identifier for the song, found in TikTok music URLs (e.g. 7439295283975702544)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokSongVideosInput(TypedDict, total=False):
    """Input for TikTok Song Videos."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    clipId: Required[str]
    """The song ID found in TikTok music URLs (e.g. 7439295283975702544)."""
    cursor: NotRequired[str]
    """Pagination cursor for retrieving the next page of results."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["nextCursor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokTopAdsSearchInput(TypedDict, total=False):
    """Input for TikTok Top Ads Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of ads requested for this page, from 1 through 20 (default 20). Range: 1 to 20. Default: 20."""
    objective: NotRequired[
        Literal[
            "traffic",
            "app_installs",
            "conversions",
            "video_views",
            "reach",
            "lead_generation",
            "product_sales",
        ]
    ]
    """Campaign objective filter. Omit it to search every objective."""
    page: NotRequired[int]
    """One-based provider page number (default 1). Minimum: 1. Default: 1."""
    performanceRank: NotRequired[
        Literal["top_1_20", "top_21_40", "top_41_60", "top_61_80"]
    ]
    """Ad performance percentile bucket, where top_1_20 is the highest-performing 20 percent. Omit it to search every bucket."""
    period: NotRequired[int]
    """Lookback period in days (default 180). Default: 180."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search in TikTok Creative Center top video ads."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokTrendingFeedInput(TypedDict, total=False):
    """Input for TikTok Trending Feed."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: Required[str]
    """2-letter country code for the proxy location (e.g. "US")."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    trim: NotRequired[str]
    """Set to true to return a simplified response."""


class TiktokTrendingHashtagsInput(TypedDict, total=False):
    """Input for TikTok Trending Hashtags."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    industry: NotRequired[
        Literal[
            "apparel_accessories",
            "baby_kids_maternity",
            "beauty_personal_care",
            "education",
            "food_beverage",
            "games",
            "health",
            "home_improvement",
            "household_products",
            "news_entertainment",
            "pets",
            "sports_outdoor",
            "tech_electronics",
            "travel",
            "vehicle_transportation",
        ]
    ]
    """Restrict the ranking to one industry. Omit for the all-industries board."""
    limit: NotRequired[int]
    """Maximum number of ranked hashtags to return, from 1 through 100 (default 3). TikTok publishes only the top 3 hashtags per board to anonymous callers, so 1 through 3 is served by the cheapest source; a higher limit routes to a dearer source that reads the full ranking. Range: 1 to 100. Default: 3."""
    period: NotRequired[int]
    """Lookback window in days that the ranking and the popularity curve cover (default 7). Default: 7."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[
        Literal[
            "US",
            "FR",
            "DE",
            "IT",
            "ES",
            "GB",
            "AR",
            "AU",
            "BR",
            "CA",
            "CO",
            "EG",
            "ID",
            "IL",
            "JP",
            "KR",
            "MY",
            "MX",
            "PH",
            "SA",
            "SG",
            "ZA",
            "TW",
            "TH",
            "TR",
            "AE",
            "VN",
        ]
    ]
    """Two-letter country code of the market whose hashtag ranking to read (default US). Each market is ranked independently, so US and DE return different boards. Default: US."""
    requireFields: NotRequired[list[Literal["industryIds", "topCreators"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `industryIds`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a hashtag that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokUserStoriesInput(TypedDict, total=False):
    """Input for TikTok User Stories."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """TikTok username, without the @ (e.g. "jasonderulo")."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[Literal["authorVerified", "expiresUtc", "photos", "reposts", "totalCount"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `expiresUtc`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a story that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokVideoInput(TypedDict, total=False):
    """Input for TikTok Video."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """TikTok video ID, the numeric run at the end of a video URL. Use it when a listing SKU handed you an id and no URL."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "authorFollowers",
                "authorVerified",
                "comments",
                "likes",
                "sdVideoUrl",
                "shares",
                "videoUrl",
                "views",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `views`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a video that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. A source that returns only a rounded or shortened value for a field does not count as returning it."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Full TikTok video URL."""


class TiktokVideoCommentsInput(TypedDict, total=False):
    """Input for TikTok Video Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["authorUserId", "language"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `authorUserId` or `language`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a comment that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """TikTok post URL on tiktok.com: a video or photo post (https://www.tiktok.com/@<user>/video/<id> or /photo/<id>) or a vm.tiktok.com or vt.tiktok.com short link. A profile link (https://www.tiktok.com/@<user>), a video file link (tiktokcdn.com) or a link to any other site is refused as invalid input, with no charge."""


class TiktokVideoDownloadInput(TypedDict, total=False):
    """Input for TikTok Video Download."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[Literal["authorFollowers", "authorVerified", "height", "width"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `height` or `width`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a video that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full TikTok video URL. Share links and tracking query params are fine."""


class TiktokVideoTranscriptInput(TypedDict, total=False):
    """Input for TikTok Video Transcript (native captions)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["language"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `language`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a video that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """TikTok video URL on tiktok.com: a video or photo post (https://www.tiktok.com/@<user>/video/<id> or /photo/<id>) or a vm.tiktok.com, vt.tiktok.com or tiktok.com/t/ share link. A profile link (https://www.tiktok.com/@<user>), a /@<user>/<id> link without /video/ (TikTok sends it to the For You feed, not a video), a video file link (tiktokcdn.com) or a link to any other site is refused as invalid input, with no charge."""


class TiktokVideoTranscriptFullInput(TypedDict, total=False):
    """Input for TikTok Video Transcript (AnyAPI speech to text)."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    hostVideo: NotRequired[bool]
    """Also store the video and return a hosted MP4 link that plays without TikTok's signed CDN URL. Charged as an extra on top of the transcript. Default: false."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """TikTok video URL (e.g. "https://www.tiktok.com/@user/video/1234567890")."""
    wordTimestamps: NotRequired[bool]
    """Return per-word timings inside each segment. Words carry timings only; the recognizer scores a phrase rather than a word, so there is no per-word confidence to report. Default: false."""


class TiktokAdLibraryAdData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_id: str = Field(
        alias="adId",
        description="Populated whenever the provider has data for the entity.",
    )
    ad_title: str = Field(
        alias="adTitle",
        description="Populated whenever the provider has data for the entity.",
    )
    brand_name: str = Field(alias="brandName")
    comments: int
    cost: float
    countries: list[str] | None = Field(
        default=None,
        description="Countries the ad ran in, as two-letter country codes. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cover_url: str = Field(
        alias="coverUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    ctr: float
    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Ad creative duration in seconds.",
    )
    height: int | None = Field(
        default=None, description="Pixel height of the ad video."
    )
    industry: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    landing_page: str = Field(
        alias="landingPage",
        description="Populated whenever the provider has data for the entity.",
    )
    likes: int
    objective: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    shares: int
    video_url: str = Field(
        alias="videoUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    width: int | None = Field(default=None, description="Pixel width of the ad video.")


class TiktokAdLibrarySearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[TiktokAdLibrarySearchAd] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    has_more: bool = Field(alias="hasMore")
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of ads, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total: int


class TiktokAdLibrarySearchAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_id: str = Field(
        alias="adId",
        description="TikTok ad id. Populated whenever the provider has data for the entity.",
    )
    ad_title: str = Field(
        alias="adTitle",
        description="Ad title as shown in TikTok's ad library. Populated whenever the provider has data for the entity.",
    )
    brand_name: str = Field(alias="brandName", description="Advertiser name on the ad.")
    cover_url: str = Field(
        alias="coverUrl",
        description="Cover image URL of the ad's first video. Populated whenever the provider has data for the entity.",
    )
    estimated_audience: str = Field(
        alias="estimatedAudience",
        description='Audience size band TikTok publishes for the ad, for example "100K-200K".',
    )
    first_shown_utc: int | None = Field(
        default=None,
        alias="firstShownUtc",
        description="UTC epoch timestamp in seconds (Unix time) when TikTok first showed the ad. Multiply by 1000 for a JS Date in milliseconds.",
    )
    format: str | None = Field(
        default=None,
        description="TikTok's creative format code for the ad, as the ad library reports it.",
    )
    last_shown_utc: int | None = Field(
        default=None,
        alias="lastShownUtc",
        description="UTC epoch timestamp in seconds (Unix time) when TikTok last showed the ad. Multiply by 1000 for a JS Date in milliseconds.",
    )
    status: str | None = Field(
        default=None,
        description="TikTok's audit status code for the ad, as the ad library reports it.",
    )
    url: str | None = Field(
        default=None,
        description="Link to the ad's detail page in TikTok's public Ads Library.",
    )
    video_url: str = Field(
        alias="videoUrl",
        description="Playable URL of the ad's first video. Populated whenever the provider has data for the entity.",
    )


class TiktokAdTransparencySearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[TiktokAdTransparencySearchAd] = Field(
        description="Commercial Content Library ad records returned for the search. Populated whenever the provider has data for the entity."
    )
    has_more: bool = Field(
        alias="hasMore",
        description="Whether the Commercial Content Library reports more matching ads. Populated whenever the provider has data for the entity.",
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Search cursor to pass as cursor on a subsequent request, or null when there is no next page. Populated whenever the provider has data for the entity.",
    )
    offset: int = Field(description="Zero-based result offset reported for this page.")
    region: str = Field(
        description="Region code applied to this transparency search. Populated whenever the provider has data for the entity."
    )
    total: int = Field(
        description="Total number of matching ads reported by the Commercial Content Library. Populated whenever the provider has data for the entity."
    )


class TiktokAdTransparencySearchAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_title: str | None = Field(
        default=None,
        alias="adTitle",
        description="Ad title as shown in TikTok's ad library.",
    )
    advertiser_name: str | None = Field(
        default=None,
        alias="advertiserName",
        description="Advertiser display name associated with the ad. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    estimated_audience: str | None = Field(
        default=None,
        alias="estimatedAudience",
        description="Estimated audience size band the ad reached, as a range string.",
    )
    first_shown_utc: float | None = Field(
        default=None,
        alias="firstShownUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the ad was first shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    format: str | None = Field(
        default=None,
        description="Commercial Content Library creative format code for the ad. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="TikTok Commercial Content Library ad identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Signed cover image URL exactly as returned by the Commercial Content Library. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    last_shown_utc: float | None = Field(
        default=None,
        alias="lastShownUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the ad was last shown. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    status: str | None = Field(
        default=None,
        description="Commercial Content Library audit status code for the ad. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Signed video asset URL exactly as returned by the Commercial Content Library. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class TiktokAudienceDemographicsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    audience_locations: list[TiktokAudienceDemographicsAudienceLocation] = Field(
        alias="audienceLocations"
    )


class TiktokAudienceDemographicsAudienceLocation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int
    country: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    country_code: str = Field(
        alias="countryCode",
        description="Populated whenever the provider has data for the entity.",
    )
    percentage: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokCommentRepliesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    comments: list[TiktokCommentRepliesComment]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of comments, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class TiktokCommentRepliesComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Reply author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Reply author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Reply author's numeric TikTok user id. Null when the serving source does not report it.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    likes: int
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_id: str | None = Field(
        default=None,
        alias="videoId",
        description="Identifier of the video the reply belongs to.",
    )


class TiktokFollowersData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    followers: list[TiktokFollowersFollower]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of followers, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total: int


class TiktokFollowersFollower(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(alias="avatarUrl")
    bio: str | None = Field(default=None, description="Account bio text.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the account was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    follower_count: int = Field(alias="followerCount")
    following_count: int = Field(alias="followingCount")
    like_count: int | None = Field(
        default=None,
        alias="likeCount",
        description="Total likes the account has received. Null when the serving source does not report it.",
    )
    nickname: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    region: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    sec_uid: str | None = Field(
        default=None,
        alias="secUid",
        description="TikTok's sec_uid for the account. Pass it to tiktok.profile_reposts or tiktok.profile_playlists. Null when the serving source does not report it.",
    )
    user_id: str = Field(
        alias="userId",
        description="Populated whenever the provider has data for the entity.",
    )
    username: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_count: int | None = Field(
        default=None,
        alias="videoCount",
        description="Number of videos the account has posted. Null when the serving source does not report it.",
    )


class TiktokFollowingData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    following: list[TiktokFollowingFollowing]
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of followed accounts, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class TiktokFollowingFollowing(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Account avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    bio: str
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the account was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    display_name: str = Field(
        alias="displayName",
        description="Populated whenever the provider has data for the entity.",
    )
    followers: int
    following: int | None = Field(
        default=None, description="Number of accounts this account follows."
    )
    handle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    instagram_url: str | None = Field(
        default=None,
        alias="instagramUrl",
        description="Instagram profile the account links on TikTok. Null when it links none or the serving source does not report it.",
    )
    likes: int | None = Field(
        default=None, description="Total likes the account has received."
    )
    private: bool | None = Field(
        default=None, description="Whether the account is private."
    )
    region: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    sec_uid: str | None = Field(
        default=None,
        alias="secUid",
        description="TikTok's sec_uid for the account. Pass it to tiktok.profile_reposts or tiktok.profile_playlists. Null when the serving source does not report it.",
    )
    videos: int
    youtube_url: str | None = Field(
        default=None,
        alias="youtubeUrl",
        description="YouTube channel the account links on TikTok. Null when it links none or the serving source does not report it.",
    )


class TiktokHashtagVideosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[TiktokHashtagVideosItem] = Field(
        description="Recent TikTok video records for the hashtag. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of videos, or null when there are no more. Pass it back as cursor to continue.",
    )


class TiktokHashtagVideosItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request; the serving source may round large counts. Null when the serving source does not report it.",
    )
    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Username of the video's creator, without the @ prefix. Empty when the upstream omits it.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account carries a TikTok verification badge.",
    )
    collect_count: int | None = Field(
        default=None,
        alias="collectCount",
        description="Number of times the video was saved.",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Number of comments on the video. Some sources round large counts (27.7M instead of 27,712,408); name the field in requireFields to be served only by a source that returns the exact count.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Video duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="The video's numeric TikTok ID, as a string. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover/thumbnail image. Signed and short-lived, so the query string is load-bearing and kept intact. Empty when the upstream omits it.",
    )
    like_count: int | None = Field(
        default=None,
        alias="likeCount",
        description="Number of likes on the video. Some sources round large counts (27.7M instead of 27,712,408); name the field in requireFields to be served only by a source that returns the exact count.",
    )
    play_count: int | None = Field(
        default=None,
        alias="playCount",
        description="Number of views/plays of the video. Some sources round large counts (27.7M instead of 27,712,408); name the field in requireFields to be served only by a source that returns the exact count.",
    )
    share_count: int | None = Field(
        default=None,
        alias="shareCount",
        description="Number of shares of the video. Some sources round large counts (27.7M instead of 27,712,408); name the field in requireFields to be served only by a source that returns the exact count.",
    )
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Null when the serving source does not report it.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Null when the serving source does not report it.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Null when the serving source does not report it.',
    )
    text: str | None = Field(
        default=None,
        description="The video caption text. Empty for videos with no caption.",
    )
    url: str = Field(
        description="Canonical tiktok.com URL of the video, with tracking query params stripped. Populated whenever the provider has data for the entity."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )


class TiktokLiveData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Host's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    bio: str | None = Field(default=None, description="Host's bio text.")
    cover_url: str = Field(
        alias="coverUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    display_name: str = Field(
        alias="displayName",
        description="Populated whenever the provider has data for the entity.",
    )
    enter_count: int = Field(alias="enterCount")
    followers: int | None = Field(default=None, description="Host's follower count.")
    following: int | None = Field(
        default=None, description="Number of accounts the host follows."
    )
    handle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    private: bool | None = Field(
        default=None, description="Whether the host's account is private."
    )
    room_id: str = Field(
        alias="roomId",
        description="Populated whenever the provider has data for the entity.",
    )
    sec_uid: str | None = Field(
        default=None,
        alias="secUid",
        description="Host's opaque secondary TikTok user id.",
    )
    start_time: int = Field(alias="startTime")
    status: int
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    user_id: str | None = Field(
        default=None, alias="userId", description="Host's numeric TikTok user id."
    )
    verified: bool | None = Field(
        default=None,
        description="Whether the host's account carries a TikTok verification badge.",
    )
    viewers: int


class TiktokPhotosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. Null when the serving source does not report it.",
    )
    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Author's TikTok handle, without the leading @.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    caption: str | None = Field(default=None, description="Post caption.")
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded.",
    )
    id: str = Field(
        description="TikTok post id. Populated whenever the provider has data for the entity."
    )
    images: list[TiktokPhotosImage] = Field(
        description="Every image in the post, in the order the creator arranged them. Populated whenever the provider has data for the entity."
    )
    likes: int | None = Field(default=None, description="Like count.")
    region: str | None = Field(
        default=None, description="Two-letter region code the post was published from."
    )
    saves: int | None = Field(default=None, description="Save count.")
    shares: int | None = Field(default=None, description="Share count.")
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the post uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    url: str | None = Field(
        default=None, description="Canonical TikTok URL of the photo post."
    )
    views: int | None = Field(default=None, description="View count.")


class TiktokPhotosImage(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(default=None, description="Pixel height of the image.")
    image: str = Field(
        description="The image without TikTok's watermark or the creator's handle. A signed, short-lived TikTok CDN URL, so fetch it promptly; the query params are the signature and must be kept intact. Despite the .jpeg in the path this is often served as HEIC, so transcode if you need broad browser support. Populated whenever the provider has data for the entity."
    )
    watermarked_image: str | None = Field(
        default=None,
        alias="watermarkedImage",
        description="The same image carrying TikTok's watermark and the creator's handle. Signed and short-lived on the same terms as image.",
    )
    width: int | None = Field(default=None, description="Pixel width of the image.")


class TiktokPlaylistVideosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page, or null when there are no more. Pass it back as cursor to continue.",
    )
    videos: list[TiktokPlaylistVideosVideo] = Field(
        description="Videos in the playlist, in the order TikTok lists them."
    )


class TiktokPlaylistVideosVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Handle of the account that posted the video, without the leading @. Populated whenever the provider has data for the entity."
    )
    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. TikTok rounds this for large accounts.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="The author's display name, which is not the handle and can contain any characters.",
    )
    author_sec_uid: str | None = Field(
        default=None,
        alias="authorSecUid",
        description="The author's TikTok sec_uid. Pass it straight to tiktok.profile_reposts or tiktok.profile_playlists to pivot to that creator without a tiktok.profile lookup.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(default=None, alias="authorVerified")
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    duration_seconds: int | None = Field(
        default=None, alias="durationSeconds", description="Video length in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded.",
    )
    id: str = Field(
        description="TikTok video id. Pass it to tiktok.video as id for the full record. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover image. A signed, short-lived TikTok CDN URL - the query params are load-bearing, so keep the URL intact. Absent when the upstream provides no cover.",
    )
    likes: int
    mentions: list[str] | None = Field(
        default=None,
        description="Accounts @mentioned in the caption, each as the handle with its leading @. Empty when the post mentions none.",
    )
    saves: int | None = None
    shares: int
    sound_author: str | None = Field(
        default=None, alias="soundAuthor", description="Credited author of the sound."
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the post uses. Pass it to tiktok.song or tiktok.song_videos as clipId.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track.',
    )
    url: str | None = Field(
        default=None,
        description="Canonical TikTok URL of the video. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL, or null when TikTok returns none. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int


class TiktokProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    bio: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    display_name: str = Field(
        alias="displayName",
        description="Populated whenever the provider has data for the entity.",
    )
    external_url: str | None = Field(
        default=None,
        alias="externalUrl",
        description="The single link the account publishes in its bio, normalized to an absolute URL. Absent when the account publishes no link. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    followers: int
    following: int
    handle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    likes: int
    private: bool | None = Field(
        default=None, description="Whether the account is private."
    )
    sec_uid: str | None = Field(
        default=None,
        alias="secUid",
        description="TikTok's sec_uid: the opaque account identifier TikTok's own web and app endpoints key on, and the id most third-party TikTok tools ask for.",
    )
    user_id: str | None = Field(
        default=None,
        alias="userId",
        description="TikTok's numeric internal user id for the account. Unlike the handle it never changes, so store it as the account's key. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    verified: bool
    videos: int


class TiktokProfileContactData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Profile picture URL. TikTok signs this URL, so it expires; re-fetch rather than storing it.",
    )
    bio: str | None = Field(default=None, description="Profile biography text.")
    display_name: str | None = Field(
        default=None, alias="displayName", description="Account display name."
    )
    emails: list[TiktokProfileContactEmail] = Field(
        description="Every public email the source publishes for the creator, each labelled with where it came from. Some sources report only the address they judge best, so a single entry does not mean a single address exists. Never empty: a creator with no public email returns found false instead. Populated whenever the provider has data for the entity."
    )
    external_url: str | None = Field(
        default=None,
        alias="externalUrl",
        description="The single link the account publishes in its bio. Absent when the account publishes no link.",
    )
    followers: int | None = Field(default=None, description="Follower count.")
    following: int | None = Field(
        default=None, description="Number of accounts this account follows."
    )
    handle: str = Field(
        description="TikTok username without the leading @. Populated whenever the provider has data for the entity."
    )
    likes: int | None = Field(
        default=None, description="Total likes across the account's videos."
    )
    primary_email: str | None = Field(
        default=None,
        alias="primaryEmail",
        description="The address the upstream considers the creator's best contact, chosen from emails. Absent when no email was found.",
    )
    private: bool | None = Field(
        default=None, description="Whether the account is private."
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical URL of the TikTok profile.",
    )
    seller: bool | None = Field(
        default=None, description="Whether the account sells through TikTok Shop."
    )
    social_links: list[TiktokProfileContactSocialLink] | None = Field(
        default=None,
        alias="socialLinks",
        description="Other social accounts found for the creator. Empty when none were found.",
    )
    user_id: str | None = Field(
        default=None,
        alias="userId",
        description="TikTok's numeric internal user id for the account. Unlike the handle it never changes, so store it as the account's key.",
    )
    verified: bool | None = Field(
        default=None, description="Whether the account carries TikTok's verified badge."
    )
    videos: int | None = Field(
        default=None, description="Number of videos the account has published."
    )


class TiktokProfileContactEmail(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str | None = Field(
        default=None,
        description="The email address's own domain. Absent when the source that served the request does not report it.",
    )
    domain_health: str | None = Field(
        default=None,
        alias="domainHealth",
        description="The source's verdict on whether the address can receive mail: healthy or unhealthy from a domain-level check, deliverable, risky or missing from a mailbox-level one. Which vocabulary you get varies with the source that served the request. Absent when the source gives no verdict for the address.",
    )
    email: str = Field(description="The email address as published.")
    source_type: str | None = Field(
        default=None,
        alias="sourceType",
        description="Where the address was read: the TikTok bio itself (tiktok_bio) or a page the profile links to (linked_page, website). An address read off a linked page may belong to a brand or a partner rather than the creator. The exact word varies with the source that served the request. Absent when the source lists the address without its origin.",
    )
    source_url: str | None = Field(
        default=None,
        alias="sourceUrl",
        description="The page the address was read from. Absent for an address read from the TikTok bio itself.",
    )


class TiktokProfileContactSocialLink(BaseModel):
    model_config = ConfigDict(extra="allow")

    platform: str = Field(
        description="The platform the link points at, for example instagram, youtube, facebook."
    )
    url: str = Field(description="The account URL on that platform.")


class TiktokProfilePlaylistsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page, or null when there are no more. Pass it back as cursor to continue.",
    )
    playlists: list[TiktokProfilePlaylistsPlaylist]


class TiktokProfilePlaylistsPlaylist(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cover_url: str | None = Field(
        default=None,
        alias="coverUrl",
        description="Playlist cover image. A signed, short-lived TikTok CDN URL - the query params are load-bearing, so keep the URL intact.",
    )
    creator_handle: str | None = Field(
        default=None,
        alias="creatorHandle",
        description="Handle of the account that owns the playlist, without the leading @. Useful because this SKU is keyed by secUid rather than handle.",
    )
    id: str = Field(
        description="Playlist id. Pass it to tiktok.playlist_videos as id to list the videos in it. Populated whenever the provider has data for the entity."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_count: int = Field(
        alias="videoCount",
        description="Number of videos TikTok reports in the playlist.",
    )


class TiktokProfileRegionData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    handle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    profile_url: str = Field(
        alias="profileUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    region: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokProfileRepostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page, or null when there are no more. Pass it back as cursor to continue.",
    )
    videos: list[TiktokProfileRepostsVideo] = Field(
        description="Videos the creator reposted, newest first. Reposts are other accounts' videos, so author is usually not the creator you asked about."
    )


class TiktokProfileRepostsVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Handle of the account that posted the video, without the leading @. Populated whenever the provider has data for the entity."
    )
    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. TikTok rounds this for large accounts.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="The author's display name, which is not the handle and can contain any characters.",
    )
    author_sec_uid: str | None = Field(
        default=None,
        alias="authorSecUid",
        description="The author's TikTok sec_uid. Pass it straight to tiktok.profile_reposts or tiktok.profile_playlists to pivot to that creator without a tiktok.profile lookup.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(default=None, alias="authorVerified")
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    duration_seconds: int | None = Field(
        default=None, alias="durationSeconds", description="Video length in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded.",
    )
    id: str = Field(
        description="TikTok video id. Pass it to tiktok.video as id for the full record. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover image. A signed, short-lived TikTok CDN URL - the query params are load-bearing, so keep the URL intact. Absent when the upstream provides no cover.",
    )
    likes: int
    location_name: str | None = Field(
        default=None,
        alias="locationName",
        description="Name of the place the post is tagged at, or null when it has no location tag.",
    )
    mentions: list[str] | None = Field(
        default=None,
        description="Accounts @mentioned in the caption, each as the handle with its leading @. Empty when the post mentions none.",
    )
    saves: int | None = None
    shares: int
    sound_author: str | None = Field(
        default=None, alias="soundAuthor", description="Credited author of the sound."
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the post uses. Pass it to tiktok.song or tiktok.song_videos as clipId.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track.',
    )
    url: str | None = Field(
        default=None,
        description="Canonical TikTok URL of the video. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL, or null when TikTok returns none. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int


class TiktokProfileVideosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of videos, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    videos: list[TiktokProfileVideosVideo]


class TiktokProfileVideosVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. Some sources round large counts; name `authorFollowers` in requireFields to be served only by a source that returns the exact count. Null when the serving source does not report it.",
    )
    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Author's TikTok handle, without the leading @.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account carries a TikTok verification badge. Null when the serving source does not report it.",
    )
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Video duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover/thumbnail image. A signed, short-lived TikTok CDN URL (typically expires within about a day; query params are load-bearing and kept intact), often served as HEIC rather than JPEG, so fetch it promptly and transcode if you need broad browser support. Absent when the upstream provides no cover.",
    )
    is_pinned: bool | None = Field(
        default=None,
        alias="isPinned",
        description="Whether the video is pinned to the top of the creator's profile grid.",
    )
    likes: int
    location_name: str | None = Field(
        default=None,
        alias="locationName",
        description="Name of the place the video is tagged at. Absent when the video has no location tag. Null when the serving source does not report it.",
    )
    paid_partnership: bool | None = Field(
        default=None,
        alias="paidPartnership",
        description="Whether the video is labeled as a paid partnership. Null when the serving source does not report it.",
    )
    saves: int | None = None
    shares: int | None = Field(default=None, description="Share count.")
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Null when the serving source does not report it.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Null when the serving source does not report it.',
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int


class TiktokSearchHashtagData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of videos, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    videos: list[TiktokSearchHashtagVideo] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokSearchHashtagVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account carries a TikTok verification badge.",
    )
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Video duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover image. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    likes: int
    location_name: str | None = Field(
        default=None,
        alias="locationName",
        description="Name of the place the video is tagged at, or null when it has no location tag or the serving source does not report it.",
    )
    saves: int | None = Field(default=None, description="Save count.")
    shares: int
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Null when the serving source does not report it.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Null when the serving source does not report it.',
    )
    url: str | None = Field(
        default=None, description="Canonical TikTok URL of the video."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int


class TiktokSearchKeywordData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of videos, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    videos: list[TiktokSearchKeywordVideo] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokSearchKeywordVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None,
        description="Username (handle) of the account that posted, without the @ prefix.",
    )
    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. Null when the serving source does not report it.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Author's display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account carries a TikTok verification badge. Null when the serving source does not report it.",
    )
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Video duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover/thumbnail image. A signed, short-lived TikTok CDN URL (typically expires within about a day; query params are load-bearing and kept intact), often served as HEIC rather than JPEG, so fetch it promptly and transcode if you need broad browser support. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    likes: int
    location_name: str | None = Field(
        default=None,
        alias="locationName",
        description="Name of the place the video is tagged at. Absent when the video has no location tag. Null when the serving source does not report it.",
    )
    paid_partnership: bool | None = Field(
        default=None,
        alias="paidPartnership",
        description="Whether the video is labeled as a paid partnership. Null when the serving source does not report it.",
    )
    region: str
    saves: int | None = None
    shares: int
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Null when the serving source does not report it.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Null when the serving source does not report it.',
    )
    url: str | None = Field(
        default=None,
        description="Canonical TikTok URL of the video. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int


class TiktokSearchPhotosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page, or null when there are no more. Pass it back as cursor to continue.",
    )
    posts: list[TiktokSearchPhotosPost] = Field(
        description="Photo-mode posts matching the keyword."
    )


class TiktokSearchPhotosPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Handle of the account that posted the video, without the leading @. Populated whenever the provider has data for the entity."
    )
    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. TikTok rounds this for large accounts.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="The author's display name, which is not the handle and can contain any characters.",
    )
    author_sec_uid: str | None = Field(
        default=None,
        alias="authorSecUid",
        description="The author's TikTok sec_uid. Pass it straight to tiktok.profile_reposts or tiktok.profile_playlists to pivot to that creator without a tiktok.profile lookup.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(default=None, alias="authorVerified")
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded.",
    )
    id: str = Field(
        description="TikTok video id. Pass it to tiktok.video as id for the full record. Populated whenever the provider has data for the entity."
    )
    images: list[TiktokSearchPhotosImage] | None = Field(
        default=None, description="The slideshow's images in order."
    )
    likes: int
    location_name: str | None = Field(
        default=None,
        alias="locationName",
        description="Name of the place the post is tagged at, or null when it has no location tag.",
    )
    saves: int | None = None
    shares: int
    sound_author: str | None = Field(
        default=None, alias="soundAuthor", description="Credited author of the sound."
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the post uses. Pass it to tiktok.song or tiktok.song_videos as clipId.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track.',
    )
    title: str | None = Field(
        default=None,
        description="The slideshow's own title, which TikTok stores separately from the caption. Absent when the creator set none.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical TikTok URL of the photo post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    views: int


class TiktokSearchPhotosImage(BaseModel):
    model_config = ConfigDict(extra="allow")

    height: int | None = None
    image: str = Field(
        description="Image URL. A signed, short-lived TikTok CDN URL - the query params are load-bearing, so keep the URL intact. Populated whenever the provider has data for the entity."
    )
    width: int | None = None


class TiktokSearchSuggestionsData(BaseModel):
    suggestions: list[TiktokSearchSuggestionsSuggestion] = Field(
        description="Suggested searches, most relevant first."
    )


class TiktokSearchSuggestionsSuggestion(BaseModel):
    model_config = ConfigDict(extra="allow")

    language: str | None = Field(
        default=None,
        description="BCP-47 language code TikTok assigns the suggestion, e.g. en.",
    )
    score: float | None = Field(
        default=None,
        description="TikTok's relative weight for the suggestion. Comparable within one response only; it is not a search volume.",
    )
    text: str = Field(
        description="The suggested search term. Populated whenever the provider has data for the entity."
    )


class TiktokSearchTopData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[TiktokSearchTopItem] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of results, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class TiktokSearchTopItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. Null when the serving source does not report it.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int
    content_type: str | None = Field(
        alias="contentType",
        description="TikTok's own label for the post format, such as video, or null when the serving source does not report it.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Media duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the item's cover image. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    likes: int
    saves: int | None = None
    shares: int
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Null when the serving source does not report it.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Null when the serving source does not report it.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Null when the serving source does not report it.',
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int


class TiktokSearchUsersData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of users, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    users: list[TiktokSearchUsersUser] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokSearchUsersUser(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Account avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    bio: str | None = Field(
        default=None,
        description="Profile biography text. Null when the serving source does not report it.",
    )
    followers: int
    following: int
    handle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    instagram_url: str | None = Field(
        default=None,
        alias="instagramUrl",
        description="Instagram profile the account links on TikTok. Null when it links none or the serving source does not report it.",
    )
    likes: int | None = Field(
        default=None, description="Total likes the account has received."
    )
    nickname: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    region: str | None = Field(
        default=None,
        description="Two-letter country code TikTok assigns the account. Null when the serving source does not report it.",
    )
    sec_uid: str | None = Field(
        default=None,
        alias="secUid",
        description="TikTok's sec_uid for the account. Pass it to tiktok.profile_reposts or tiktok.profile_playlists. Null when the serving source does not report it.",
    )
    user_id: str = Field(
        alias="userId",
        description="Populated whenever the provider has data for the entity.",
    )
    verified: bool | None = Field(
        default=None,
        description="Whether the account carries a TikTok verification badge.",
    )
    videos: int | None = Field(
        default=None, description="Number of videos the account has posted."
    )
    youtube_url: str | None = Field(
        default=None,
        alias="youtubeUrl",
        description="YouTube channel the account links on TikTok. Null when it links none or the serving source does not report it.",
    )


class TiktokSongData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    album: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    author: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    cover_url: str = Field(
        alias="coverUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    duration: int = Field(
        description="Populated whenever the provider has data for the entity."
    )
    is_original: bool = Field(alias="isOriginal")
    share_url: str = Field(
        alias="shareUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    song_id: str = Field(
        alias="songId",
        description="Populated whenever the provider has data for the entity.",
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_count: int = Field(alias="videoCount")


class TiktokSongVideosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: int = Field(alias="hasMore")
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of videos, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    videos: list[TiktokSongVideosVideo] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokSongVideosVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str = Field(
        alias="authorHandle",
        description="Populated whenever the provider has data for the entity.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str = Field(
        alias="authorName",
        description="Populated whenever the provider has data for the entity.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    collect_count: int | None = Field(
        default=None,
        alias="collectCount",
        description="Number of times the video was saved.",
    )
    comment_count: int = Field(alias="commentCount")
    create_time: int = Field(alias="createTime")
    description: str
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Video duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover image. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    like_count: int = Field(alias="likeCount")
    play_count: int = Field(alias="playCount")
    share_count: int = Field(alias="shareCount")
    url: str | None = Field(
        default=None, description="Canonical TikTok URL of the video."
    )
    video_id: str = Field(
        alias="videoId",
        description="Populated whenever the provider has data for the entity.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )


class TiktokTopAdsSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[TiktokTopAdsSearchAd] = Field(
        description="TikTok Creative Center top-ad records returned for this page. Populated whenever the provider has data for the entity."
    )
    has_more: bool = Field(
        alias="hasMore",
        description="Whether TikTok Creative Center reports another page of matching ads. Populated whenever the provider has data for the entity.",
    )
    page: int = Field(
        description="One-based page number reported by TikTok Creative Center. Populated whenever the provider has data for the entity."
    )
    page_size: int = Field(
        alias="pageSize",
        description="Page size reported by TikTok Creative Center. Populated whenever the provider has data for the entity.",
    )
    total: int = Field(
        description="Total number of matching top ads reported by TikTok Creative Center. Populated whenever the provider has data for the entity."
    )


class TiktokTopAdsSearchAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ad_id: str = Field(
        alias="adId",
        description="TikTok Creative Center ad material identifier. Populated whenever the provider has data for the entity.",
    )
    ad_title: str | None = Field(
        default=None,
        alias="adTitle",
        description="Title or primary copy shown for the ad. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    brand_name: str | None = Field(
        default=None,
        alias="brandName",
        description="Advertiser brand name when supplied by TikTok Creative Center. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cost: float | None = Field(
        default=None,
        description="TikTok Creative Center's relative cost ranking value for the ad. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    ctr: float | None = Field(
        default=None,
        description="TikTok Creative Center's click-through rate value for the ad. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Video duration in seconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    height: int | None = Field(
        default=None,
        description="Video height in pixels. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Signed video cover image URL exactly as returned by TikTok Creative Center. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    industry: str | None = Field(
        default=None,
        description="TikTok Creative Center industry classification key. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    likes: int | None = Field(
        default=None,
        description="Number of likes reported for the ad. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    objective: str | None = Field(
        default=None,
        description="TikTok Creative Center campaign objective key. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Signed 720p video asset URL exactly as returned by TikTok Creative Center. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    width: int | None = Field(
        default=None,
        description="Video width in pixels. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class TiktokTrendingFeedData(BaseModel):
    videos: list[TiktokTrendingFeedVideo] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokTrendingFeedVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    caption: str
    comments: int
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Video duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover image. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    likes: int
    region: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    saves: int | None = Field(default=None, description="Save count.")
    shares: int
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int


class TiktokTrendingHashtagsData(BaseModel):
    items: list[TiktokTrendingHashtagsItem] = Field(
        description="Hashtags in the market's own ranking order, best first. Populated whenever the provider has data for the entity."
    )


class TiktokTrendingHashtagsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    hashtag: str = Field(
        description="Hashtag name without the leading #. Populated whenever the provider has data for the entity."
    )
    hashtag_id: str = Field(
        alias="hashtagId",
        description="Stable TikTok hashtag identifier. Populated whenever the provider has data for the entity.",
    )
    industry_ids: list[int] | None = Field(
        default=None,
        alias="industryIds",
        description="TikTok industry identifiers the hashtag is classified under, matching the ids behind the `industry` input. Empty when TikTok classifies the hashtag under none.",
    )
    popularity: list[TiktokTrendingHashtagsPopularity] | None = Field(
        default=None,
        description="Daily popularity curve across the requested period, oldest first. Values are normalized 0-100 within this hashtag's own window, where 100 is its peak day, so they compare days of one hashtag rather than two hashtags. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    posts: int | None = Field(
        default=None,
        description="Number of videos published with the hashtag during the period. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rank: int = Field(
        description="One-based position in this market's ranking for the requested period. Populated whenever the provider has data for the entity. Minimum: 1."
    )
    top_creators: list[TiktokTrendingHashtagsTopCreator] | None = Field(
        default=None,
        alias="topCreators",
        description="Creators TikTok surfaces as leading the hashtag, in its own order.",
    )
    views: int | None = Field(
        default=None,
        description="Total video views the hashtag drew during the period. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class TiktokTrendingHashtagsPopularity(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    at_utc: float = Field(
        alias="atUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    value: float = Field(
        description="Normalized popularity for that day, 0 through 100. Range: 0 to 100."
    )


class TiktokTrendingHashtagsTopCreator(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country_code: str | None = Field(
        default=None,
        alias="countryCode",
        description="Two-letter country code TikTok reports for the creator.",
    )
    followers: int | None = Field(default=None, description="Creator's follower count.")
    handle: str | None = Field(
        default=None, description="Creator's TikTok username without the leading @."
    )
    image: str | None = Field(default=None, description="Creator's avatar image URL.")
    nickname: str | None = Field(default=None, description="Creator's display name.")
    rank: int | None = Field(
        default=None,
        description="One-based position among the hashtag's top creators. Minimum: 1.",
    )
    user_id: str | None = Field(
        default=None, alias="userId", description="Creator's stable TikTok user id."
    )


class TiktokUserStoriesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when TikTok reports more active stories than the ones returned; they cannot be fetched with another call.",
    )
    stories: list[TiktokUserStoriesStorie] = Field(
        description="The account's active public stories, up to 20, oldest first. Populated whenever the provider has data for the entity."
    )
    total_count: int | None = Field(
        default=None,
        alias="totalCount",
        description="How many active stories TikTok reports for the account, which can exceed the stories returned. Null when this source does not report it.",
    )


class TiktokUserStoriesStorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Author's TikTok handle, without the leading @.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so keep the query string.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account carries a TikTok verification badge. Null when this source does not report it.",
    )
    caption: str | None = Field(
        default=None, description="Caption text; usually empty on stories."
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Video length in seconds; 0 for a photo story.",
    )
    expires_utc: float | None = Field(
        default=None,
        alias="expiresUtc",
        description="When the story stops being visible. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Null when this source does not report it.",
    )
    id: str = Field(
        description="Story (video or photo post) id. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Cover image URL. Signed and short-lived, so keep the query string. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image_urls: list[str] | None = Field(
        default=None,
        alias="imageUrls",
        description="Photo URLs for a photo story; empty for a video story. Signed and short-lived.",
    )
    likes: int | None = Field(default=None, description="Like count.")
    photos: list[TiktokUserStoriesPhoto] | None = Field(
        default=None,
        description="The photos of a photo story with their pixel dimensions; empty for a video story. Null when this source does not report dimensions; imageUrls still lists the photos.",
    )
    reposts: int | None = Field(
        default=None,
        description="Repost count. Null when this source does not report it.",
    )
    saves: int | None = Field(default=None, description="Save (favorite) count.")
    shares: int | None = Field(default=None, description="Share count.")
    sound_author: str | None = Field(
        default=None, alias="soundAuthor", description="Credited author of the sound."
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the story uses. Pass it to tiktok.song or tiktok.song_videos as clipId.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description="Name of the sound the story uses; null when it has none.",
    )
    sound_url: str | None = Field(
        default=None,
        alias="soundUrl",
        description="Audio file URL of the sound. Signed and short-lived, so keep the query string.",
    )
    url: str | None = Field(
        default=None,
        description="The story on tiktok.com. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL for a video story; null for a photo story. Signed and short-lived, so keep the query string.",
    )
    views: int | None = Field(default=None, description="Play count.")


class TiktokUserStoriesPhoto(BaseModel):
    model_config = ConfigDict(extra="allow")

    height: int | None = Field(default=None, description="Photo height in pixels.")
    url: str | None = Field(
        default=None,
        description="Photo URL. Signed and short-lived, so keep the query string.",
    )
    width: int | None = Field(default=None, description="Photo width in pixels.")


class TiktokVideoData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. Some sources round large counts; name `authorFollowers` in requireFields to be served only by a source that returns the exact count. Null when the serving source does not report it.",
    )
    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Author's TikTok handle, without the leading @.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account carries a TikTok verification badge. Null when the serving source does not report it.",
    )
    caption: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    comments: int = Field(
        description="Number of comments. Some sources round large counts (48.5K instead of 48,536); name `comments` in requireFields to be served only by a source that returns the exact count."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    duration_seconds: float | None = Field(
        default=None, alias="durationSeconds", description="Video duration in seconds."
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the video's cover/thumbnail image. A signed, short-lived TikTok CDN URL (typically expires within about a day; query params are load-bearing and kept intact), often served as HEIC rather than JPEG, so fetch it promptly and transcode if you need broad browser support. Absent when the upstream provides no cover.",
    )
    likes: int = Field(
        description="Number of likes. Some sources round large counts (2.9M instead of 2,884,604); name `likes` in requireFields to be served only by a source that returns the exact count."
    )
    region: str
    saves: int
    sd_video_url: str | None = Field(
        default=None,
        alias="sdVideoUrl",
        description="Standard-resolution H.264 video URL without the watermark (often 720p), playable in every browser; the same file as videoUrl when the source has no higher-resolution file. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    shares: int = Field(
        description="Number of shares. Some sources round large counts (35.9K instead of 35,923); name `shares` in requireFields to be served only by a source that returns the exact count."
    )
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    url: str | None = Field(
        default=None, description="Canonical TikTok URL of the video."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL without the watermark, at the highest resolution the source has: often 1080p and often encoded as H.265 (HEVC), which some browsers such as Firefox cannot play; use sdVideoUrl for those. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    views: int = Field(
        description="Number of plays. Some sources round large counts (32.7M instead of 32,736,400); name `views` in requireFields to be served only by a source that returns the exact count."
    )


class TiktokVideoCommentsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    comments: list[TiktokVideoCommentsComment]
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of comments, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class TiktokVideoCommentsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Comment author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Comment author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Comment author's numeric TikTok user id. Null when the serving source does not report it.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    language: str | None = Field(
        default=None,
        description="Language TikTok detected for the comment text, as a code such as en. Null when the serving source does not report it.",
    )
    likes: int
    replies: int
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_id: str | None = Field(
        default=None,
        alias="videoId",
        description="Identifier of the video the comment belongs to.",
    )


class TiktokVideoDownloadData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="The author's follower count at the time of the request. Null when the serving source does not report it.",
    )
    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Author's TikTok handle, without the leading @.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Author's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_name: str | None = Field(
        default=None, alias="authorName", description="Author's display name."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author's numeric TikTok user id.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account carries a TikTok verification badge. Null when the serving source does not report it.",
    )
    caption: str | None = Field(default=None, description="Post caption.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Length of the video in seconds.",
    )
    hashtags: list[str] | None = Field(
        default=None,
        description="Hashtags carried in the caption, without the leading #. Empty when the post uses none; @-mentions are excluded.",
    )
    height: int | None = Field(
        default=None, description="Pixel height of the file in videoUrl."
    )
    id: str = Field(
        description="TikTok video id. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Cover image for the video. A signed, short-lived TikTok CDN URL, often served as HEIC rather than JPEG, so fetch it promptly and transcode if you need broad browser support.",
    )
    region: str | None = Field(
        default=None, description="Two-letter region code the video was published from."
    )
    sd_video_url: str | None = Field(
        default=None,
        alias="sdVideoUrl",
        description="Standard-resolution H.264 MP4 without the watermark (often 720p), playable in every browser; the same file as videoUrl when the source has no higher-resolution file. Signed and short-lived on the same terms as videoUrl.",
    )
    sound_author: str | None = Field(
        default=None,
        alias="soundAuthor",
        description="Credited author of the sound. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_clip_id: str | None = Field(
        default=None,
        alias="soundClipId",
        description="Id of the sound the video uses. Pass it to tiktok.song or tiktok.song_videos as clipId. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sound_title: str | None = Field(
        default=None,
        alias="soundTitle",
        description='Name of the sound. "original sound" means the creator\'s own audio rather than a licensed track. Some sources answer in another language ("原声" for original sound). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    url: str | None = Field(
        default=None, description="Canonical TikTok URL of the video."
    )
    video_url: str = Field(
        alias="videoUrl",
        description="Direct MP4 without the TikTok watermark or handle overlay, at the highest resolution the source has: often 1080p and often encoded as H.265 (HEVC), which some browsers such as Firefox cannot play; use sdVideoUrl for those. A signed, short-lived TikTok CDN URL, so fetch it promptly; the query params are the signature and must be kept intact. Send no cookies with the request - a tt_chain_token cookie makes the CDN answer 403. Still returned when the creator has turned off downloads: it is then the clean file TikTok streams for playback. Populated whenever the provider has data for the entity.",
    )
    watermarked_url: str | None = Field(
        default=None,
        alias="watermarkedUrl",
        description="Direct MP4 carrying TikTok's watermark and the creator's handle, the same file TikTok's own save button produces. Signed and short-lived on the same terms as videoUrl. Absent when the creator has turned off downloads, because TikTok then publishes no watermarked file.",
    )
    width: int | None = Field(
        default=None, description="Pixel width of the file in videoUrl."
    )


class TiktokVideoTranscriptData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = Field(
        default=None, description="TikTok video id the transcript belongs to."
    )
    language: str | None = Field(
        default=None,
        description="Language of the caption track, or null when the serving source does not report it.",
    )
    transcript: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None, description="Canonical TikTok URL of the video."
    )


class TiktokVideoTranscriptFullData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bytes: int | None = Field(
        default=None, description="Size of the hosted MP4 in bytes. Minimum: 0."
    )
    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Video duration in seconds. Minimum: 0.",
    )
    expires_utc: float | None = Field(
        default=None,
        alias="expiresUtc",
        description="When the hosted link stops working. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    hosted_url: str | None = Field(
        default=None,
        alias="hostedUrl",
        description="Hosted MP4 link, returned only when the request set hostVideo. It plays without TikTok's signed CDN URL and without any cookie, and it stops working at expiresUtc.",
    )
    id: str | None = Field(default=None, description="TikTok video id.")
    language: str | None = Field(
        default=None,
        description='Detected spoken language of the audio (BCP-47 style code, e.g. "en").',
    )
    owner_username: str | None = Field(
        default=None,
        alias="ownerUsername",
        description="Creator handle, without the leading @.",
    )
    segments: list[TiktokVideoTranscriptFullSegment] | None = Field(
        default=None,
        description="Timed transcript segments in playback order, one per sentence, so a segment locates a specific line in the video rather than a whole speaker turn. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    source: Literal["audio_asr", "no_audio", "transcript_unavailable"] = Field(
        description='How the text was produced. "audio_asr" means the words come from speech recognition over the video\'s audio, never from a caption track TikTok published - for TikTok\'s own captions, use tiktok.video_transcript. "transcript_unavailable" means recognition did not complete for this video, so the transcript is empty for that reason rather than because the video has no speech in it; the rest of the record is still what we resolved, and no audio time is charged. "no_audio" means there was nothing to listen to: the video has no audio track, or the post has no video. The transcript is empty because that is the answer, the rest of the record is still what we resolved, and only the request price is charged, with no audio time. Populated whenever the provider has data for the entity.'
    )
    thumbnail_url: str | None = Field(
        default=None,
        alias="thumbnailUrl",
        description="Cover image for the video. A signed, short-lived TikTok CDN URL, often served as HEIC rather than JPEG, so fetch it promptly and transcode if you need broad browser support.",
    )
    transcript: str = Field(
        description="Full spoken-word transcript, recognized from the video's audio track. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Canonical URL of the video this transcript came from.",
    )


class TiktokVideoTranscriptFullSegment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    end_seconds: float = Field(
        alias="endSeconds",
        description="Segment end offset in seconds, taken from the last word it contains. Minimum: 0.",
    )
    language: str | None = Field(
        default=None, description="Detected language for this segment."
    )
    speaker: str | None = Field(
        default=None,
        description="Speaker label for this segment, stable within one response and meaningless across responses. Telling voices apart is a guess, not an identification, and the label is not a name.",
    )
    start_seconds: float = Field(
        alias="startSeconds",
        description="Segment start offset in seconds, taken from the first word it contains. Minimum: 0.",
    )
    text: str = Field(description="Text of this segment.")
    words: list[TiktokVideoTranscriptFullWord] | None = Field(
        default=None,
        description="Per-word timings for this segment, returned only when the request set wordTimestamps. Words carry no confidence score: the recognizer scores a phrase rather than a word.",
    )


class TiktokVideoTranscriptFullWord(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    end_seconds: float | None = Field(
        default=None,
        alias="endSeconds",
        description="Word end offset in seconds. Minimum: 0.",
    )
    start_seconds: float | None = Field(
        default=None,
        alias="startSeconds",
        description="Word start offset in seconds. Minimum: 0.",
    )
    text: str = Field(
        description="The recognized word, in display form with its own punctuation."
    )


class TiktokNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ad_library_ad(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdLibraryAdInput],
    ) -> RunResult[TiktokAdLibraryAdData]:
        """TikTok Ad Library Ad

        Fetch full details for a single TikTok ad (brand, title, spend, CTR,
        objectives, landing page, and video info).

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.ad_library_ad(adId="7648493525660270600")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.ad_library_ad", dict(input), options
        )
        return RunResult[TiktokAdLibraryAdData].model_validate(raw)

    def ad_library_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdLibrarySearchInput],
    ) -> RunResult[TiktokAdLibrarySearchData]:
        """TikTok Ad Library Search

        Search TikTok's public Ads Library by keyword or advertiser (advertiser,
        title, audience band, run dates, library link, and video).

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.ad_library_search(query="spotify")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.ad_library_search", dict(input), options
        )
        return RunResult[TiktokAdLibrarySearchData].model_validate(raw)

    def iter_ad_library_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdLibrarySearchInput],
    ) -> Paginator[TiktokAdLibrarySearchAd, TiktokAdLibrarySearchData]:
        """Iterate TikTok Ad Library Search results, following pagination cursors.

        Yields validated `TiktokAdLibrarySearchAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.ad_library_search",
            dict(input),
            "ads",
            item_model=TiktokAdLibrarySearchAd,
            data_model=TiktokAdLibrarySearchData,
            bare=False,
            options=options,
        )

    def ad_transparency_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdTransparencySearchInput],
    ) -> RunResult[TiktokAdTransparencySearchData]:
        """TikTok Ad Transparency Search

        Search TikTok's EU Commercial Content Library by keyword or advertiser ID.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.ad_transparency_search(days=30, limit=20, query="nike", region="DE")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.ad_transparency_search", dict(input), options
        )
        return RunResult[TiktokAdTransparencySearchData].model_validate(raw)

    def iter_ad_transparency_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdTransparencySearchInput],
    ) -> Paginator[TiktokAdTransparencySearchAd, TiktokAdTransparencySearchData]:
        """Iterate TikTok Ad Transparency Search results, following pagination cursors.

        Yields validated `TiktokAdTransparencySearchAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.ad_transparency_search",
            dict(input),
            "ads",
            item_model=TiktokAdTransparencySearchAd,
            data_model=TiktokAdTransparencySearchData,
            bare=False,
            options=options,
        )

    def audience_demographics(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAudienceDemographicsInput],
    ) -> RunResult[TiktokAudienceDemographicsData]:
        """TikTok Audience Demographics

        Get the audience country breakdown (follower count and share per country)
        for a TikTok creator by handle.

        Price: $0.018 per request.

        Example:
            res = client.tiktok.audience_demographics(handle="shakira")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.audience_demographics", dict(input), options
        )
        return RunResult[TiktokAudienceDemographicsData].model_validate(raw)

    def comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokCommentRepliesInput],
    ) -> RunResult[TiktokCommentRepliesData]:
        """TikTok Comment Replies

        List the replies to a TikTok comment with cursor pagination (text, author,
        likes).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.comment_replies(commentId="7623828115408274207", url="https://www.tiktok.com/@stoolpresidente/video/7623818255903329566")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.comment_replies", dict(input), options
        )
        return RunResult[TiktokCommentRepliesData].model_validate(raw)

    def iter_comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokCommentRepliesInput],
    ) -> Paginator[TiktokCommentRepliesComment, TiktokCommentRepliesData]:
        """Iterate TikTok Comment Replies results, following pagination cursors.

        Yields validated `TiktokCommentRepliesComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.comment_replies",
            dict(input),
            "comments",
            item_model=TiktokCommentRepliesComment,
            data_model=TiktokCommentRepliesData,
            bare=False,
            options=options,
        )

    def followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowersInput],
    ) -> RunResult[TiktokFollowersData]:
        """TikTok Followers

        List the followers of a TikTok account by username, returning each
        follower's profile basics.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.followers(handle="stoolpresidente")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.followers", dict(input), options
        )
        return RunResult[TiktokFollowersData].model_validate(raw)

    def iter_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowersInput],
    ) -> Paginator[TiktokFollowersFollower, TiktokFollowersData]:
        """Iterate TikTok Followers results, following pagination cursors.

        Yields validated `TiktokFollowersFollower` items from the `followers` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.followers",
            dict(input),
            "followers",
            item_model=TiktokFollowersFollower,
            data_model=TiktokFollowersData,
            bare=False,
            options=options,
        )

    def following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowingInput],
    ) -> RunResult[TiktokFollowingData]:
        """TikTok Following

        List the accounts a TikTok user follows (handle, display name, follower
        count, bio) by username.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.following(handle="stoolpresidente")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.following", dict(input), options
        )
        return RunResult[TiktokFollowingData].model_validate(raw)

    def iter_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowingInput],
    ) -> Paginator[TiktokFollowingFollowing, TiktokFollowingData]:
        """Iterate TikTok Following results, following pagination cursors.

        Yields validated `TiktokFollowingFollowing` items from the `following` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.following",
            dict(input),
            "following",
            item_model=TiktokFollowingFollowing,
            data_model=TiktokFollowingData,
            bare=False,
            options=options,
        )

    def hashtag_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokHashtagVideosInput],
    ) -> RunResult[TiktokHashtagVideosData]:
        """TikTok Hashtag Videos

        List recent TikTok videos for a hashtag (creator, caption, views, likes,
        shares).

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.hashtag_videos(hashtag="cooking", limit=3)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.hashtag_videos", dict(input), options
        )
        return RunResult[TiktokHashtagVideosData].model_validate(raw)

    def iter_hashtag_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokHashtagVideosInput],
    ) -> Paginator[TiktokHashtagVideosItem, TiktokHashtagVideosData]:
        """Iterate TikTok Hashtag Videos results, following pagination cursors.

        Yields validated `TiktokHashtagVideosItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.hashtag_videos",
            dict(input),
            "items",
            item_model=TiktokHashtagVideosItem,
            data_model=TiktokHashtagVideosData,
            bare=False,
            options=options,
        )

    def live(
        self, *, options: RequestOptions | None = None, **input: Unpack[TiktokLiveInput]
    ) -> RunResult[TiktokLiveData]:
        """TikTok Live

        Check whether a TikTok creator is live and get the current live room (title,
        viewers, start time) by handle.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.live(handle="thejustalex")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.live", dict(input), options
        )
        return RunResult[TiktokLiveData].model_validate(raw)

    def photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokPhotosInput],
    ) -> RunResult[TiktokPhotosData]:
        """TikTok Photos

        Get every image in a TikTok photo-mode (slideshow) post by URL, in order,
        with pixel dimensions and both the clean and watermarked variant of each.
        Videos carry no images - use tiktok.video_download for those.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.photos(url="https://www.tiktok.com/@foodbyfranchi/video/7479916555602513174")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.photos", dict(input), options
        )
        return RunResult[TiktokPhotosData].model_validate(raw)

    def playlist_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokPlaylistVideosInput],
    ) -> RunResult[TiktokPlaylistVideosData]:
        """TikTok Playlist Videos

        List the videos inside one TikTok playlist by playlist URL or id, in
        playlist order, with view, like and comment counts.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.playlist_videos(url="https://www.tiktok.com/@mrbeast/playlist/Beast%20Games-7596415294902389534")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.playlist_videos", dict(input), options
        )
        return RunResult[TiktokPlaylistVideosData].model_validate(raw)

    def iter_playlist_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokPlaylistVideosInput],
    ) -> Paginator[TiktokPlaylistVideosVideo, TiktokPlaylistVideosData]:
        """Iterate TikTok Playlist Videos results, following pagination cursors.

        Yields validated `TiktokPlaylistVideosVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.playlist_videos",
            dict(input),
            "videos",
            item_model=TiktokPlaylistVideosVideo,
            data_model=TiktokPlaylistVideosData,
            bare=False,
            options=options,
        )

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileInput],
    ) -> RunResult[TiktokProfileData]:
        """TikTok Profile

        Fetch a TikTok creator's public profile (followers, likes, bio,
        verification) by handle.

        Price: $0.0004 per request.

        Example:
            res = client.tiktok.profile(handle="zachking")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile", dict(input), options
        )
        return RunResult[TiktokProfileData].model_validate(raw)

    def profile_contact(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileContactInput],
    ) -> RunResult[TiktokProfileContactData]:
        """TikTok Profile Contact Info

        Find the public contact email behind a TikTok creator's profile: the address
        written into the bio plus any published on the site the profile links to,
        each labelled with where it came from. Returns the creator's profile stats
        and linked social accounts alongside.

        Price: $0.00116 per request plus $0 per result (maximum $0.00116).

        Example:
            res = client.tiktok.profile_contact(handle="gordonramsayofficial")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_contact", dict(input), options
        )
        return RunResult[TiktokProfileContactData].model_validate(raw)

    def profile_playlists(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfilePlaylistsInput],
    ) -> RunResult[TiktokProfilePlaylistsData]:
        """TikTok Profile Playlists

        List the playlists a TikTok creator has published on their profile, with
        each playlist's name, video count and cover image.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.profile_playlists(secUid="MS4wLjABAAAABKjQkOz_IIzXXzEAl_9LGsWhvK-gBnlczwRPXK8EmxAp6K3X0qiaP5_OEqmm0XwG")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_playlists", dict(input), options
        )
        return RunResult[TiktokProfilePlaylistsData].model_validate(raw)

    def iter_profile_playlists(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfilePlaylistsInput],
    ) -> Paginator[TiktokProfilePlaylistsPlaylist, TiktokProfilePlaylistsData]:
        """Iterate TikTok Profile Playlists results, following pagination cursors.

        Yields validated `TiktokProfilePlaylistsPlaylist` items from the `playlists` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.profile_playlists",
            dict(input),
            "playlists",
            item_model=TiktokProfilePlaylistsPlaylist,
            data_model=TiktokProfilePlaylistsData,
            bare=False,
            options=options,
        )

    def profile_region(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileRegionInput],
    ) -> RunResult[TiktokProfileRegionData]:
        """TikTok Profile Region

        Resolve the home region (country) of a TikTok creator by handle.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.profile_region(handle="stoolpresidente")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_region", dict(input), options
        )
        return RunResult[TiktokProfileRegionData].model_validate(raw)

    def profile_reposts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileRepostsInput],
    ) -> RunResult[TiktokProfileRepostsData]:
        """TikTok Profile Reposts

        List the videos a TikTok creator has reposted to their profile, with view,
        like and comment counts and cursor pagination.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.profile_reposts(secUid="MS4wLjABAAAABKjQkOz_IIzXXzEAl_9LGsWhvK-gBnlczwRPXK8EmxAp6K3X0qiaP5_OEqmm0XwG")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_reposts", dict(input), options
        )
        return RunResult[TiktokProfileRepostsData].model_validate(raw)

    def iter_profile_reposts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileRepostsInput],
    ) -> Paginator[TiktokProfileRepostsVideo, TiktokProfileRepostsData]:
        """Iterate TikTok Profile Reposts results, following pagination cursors.

        Yields validated `TiktokProfileRepostsVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.profile_reposts",
            dict(input),
            "videos",
            item_model=TiktokProfileRepostsVideo,
            data_model=TiktokProfileRepostsData,
            bare=False,
            options=options,
        )

    def profile_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileVideosInput],
    ) -> RunResult[TiktokProfileVideosData]:
        """TikTok Profile Videos

        List a TikTok creator's recent videos (views, likes, comments) by handle
        with cursor pagination.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.profile_videos(handle="zachking")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_videos", dict(input), options
        )
        return RunResult[TiktokProfileVideosData].model_validate(raw)

    def iter_profile_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileVideosInput],
    ) -> Paginator[TiktokProfileVideosVideo, TiktokProfileVideosData]:
        """Iterate TikTok Profile Videos results, following pagination cursors.

        Yields validated `TiktokProfileVideosVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.profile_videos",
            dict(input),
            "videos",
            item_model=TiktokProfileVideosVideo,
            data_model=TiktokProfileVideosData,
            bare=False,
            options=options,
        )

    def search_hashtag(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchHashtagInput],
    ) -> RunResult[TiktokSearchHashtagData]:
        """TikTok Hashtag Search

        Search TikTok by hashtag and get matching videos (caption, views, likes,
        comments, shares) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.search_hashtag(query="recipe")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_hashtag", dict(input), options
        )
        return RunResult[TiktokSearchHashtagData].model_validate(raw)

    def iter_search_hashtag(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchHashtagInput],
    ) -> Paginator[TiktokSearchHashtagVideo, TiktokSearchHashtagData]:
        """Iterate TikTok Hashtag Search results, following pagination cursors.

        Yields validated `TiktokSearchHashtagVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.search_hashtag",
            dict(input),
            "videos",
            item_model=TiktokSearchHashtagVideo,
            data_model=TiktokSearchHashtagData,
            bare=False,
            options=options,
        )

    def search_keyword(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchKeywordInput],
    ) -> RunResult[TiktokSearchKeywordData]:
        """TikTok Keyword Search

        Search TikTok by keyword and get matching videos (caption, views, likes,
        comments, shares) as normalized JSON.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.search_keyword(datePosted=0, query="cooking", sortBy="relevance")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_keyword", dict(input), options
        )
        return RunResult[TiktokSearchKeywordData].model_validate(raw)

    def iter_search_keyword(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchKeywordInput],
    ) -> Paginator[TiktokSearchKeywordVideo, TiktokSearchKeywordData]:
        """Iterate TikTok Keyword Search results, following pagination cursors.

        Yields validated `TiktokSearchKeywordVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.search_keyword",
            dict(input),
            "videos",
            item_model=TiktokSearchKeywordVideo,
            data_model=TiktokSearchKeywordData,
            bare=False,
            options=options,
        )

    def search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchPhotosInput],
    ) -> RunResult[TiktokSearchPhotosData]:
        """TikTok Photo Search

        Search TikTok for photo-mode (slideshow) posts by keyword, with every image
        in each post plus view, like and comment counts. tiktok.search_keyword
        returns videos and drops these.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.search_photos(query="latte art")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_photos", dict(input), options
        )
        return RunResult[TiktokSearchPhotosData].model_validate(raw)

    def iter_search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchPhotosInput],
    ) -> Paginator[TiktokSearchPhotosPost, TiktokSearchPhotosData]:
        """Iterate TikTok Photo Search results, following pagination cursors.

        Yields validated `TiktokSearchPhotosPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.search_photos",
            dict(input),
            "posts",
            item_model=TiktokSearchPhotosPost,
            data_model=TiktokSearchPhotosData,
            bare=False,
            options=options,
        )

    def search_suggestions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchSuggestionsInput],
    ) -> RunResult[TiktokSearchSuggestionsData]:
        """TikTok Search Suggestions

        Get the search terms TikTok suggests for a keyword, each with its language
        and relative weight - the queries real TikTok users type around your topic.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.search_suggestions(query="protein powder")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_suggestions", dict(input), options
        )
        return RunResult[TiktokSearchSuggestionsData].model_validate(raw)

    def search_top(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchTopInput],
    ) -> RunResult[TiktokSearchTopData]:
        """TikTok Top Search

        Search TikTok's top results for a keyword (caption, views, likes, comments,
        shares) with cursor pagination.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.search_top(query="funny")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_top", dict(input), options
        )
        return RunResult[TiktokSearchTopData].model_validate(raw)

    def iter_search_top(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchTopInput],
    ) -> Paginator[TiktokSearchTopItem, TiktokSearchTopData]:
        """Iterate TikTok Top Search results, following pagination cursors.

        Yields validated `TiktokSearchTopItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.search_top",
            dict(input),
            "items",
            item_model=TiktokSearchTopItem,
            data_model=TiktokSearchTopData,
            bare=False,
            options=options,
        )

    def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchUsersInput],
    ) -> RunResult[TiktokSearchUsersData]:
        """TikTok User Search

        Search TikTok accounts by keyword (handle, nickname, follower count) with
        cursor pagination.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.search_users(query="chef")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_users", dict(input), options
        )
        return RunResult[TiktokSearchUsersData].model_validate(raw)

    def iter_search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchUsersInput],
    ) -> Paginator[TiktokSearchUsersUser, TiktokSearchUsersData]:
        """Iterate TikTok User Search results, following pagination cursors.

        Yields validated `TiktokSearchUsersUser` items from the `users` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.search_users",
            dict(input),
            "users",
            item_model=TiktokSearchUsersUser,
            data_model=TiktokSearchUsersData,
            bare=False,
            options=options,
        )

    def song(
        self, *, options: RequestOptions | None = None, **input: Unpack[TiktokSongInput]
    ) -> RunResult[TiktokSongData]:
        """TikTok Song

        Fetch details for a TikTok song or sound (title, author, duration, cover
        art, and how many videos use it).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.song(clipId="7439295283975702544")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.song", dict(input), options
        )
        return RunResult[TiktokSongData].model_validate(raw)

    def song_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSongVideosInput],
    ) -> RunResult[TiktokSongVideosData]:
        """TikTok Song Videos

        List TikTok videos that use a given song or sound (with descriptions,
        authors, and engagement stats).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.song_videos(clipId="7439295283975702544")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.song_videos", dict(input), options
        )
        return RunResult[TiktokSongVideosData].model_validate(raw)

    def iter_song_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSongVideosInput],
    ) -> Paginator[TiktokSongVideosVideo, TiktokSongVideosData]:
        """Iterate TikTok Song Videos results, following pagination cursors.

        Yields validated `TiktokSongVideosVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.song_videos",
            dict(input),
            "videos",
            item_model=TiktokSongVideosVideo,
            data_model=TiktokSongVideosData,
            bare=False,
            options=options,
        )

    def top_ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokTopAdsSearchInput],
    ) -> RunResult[TiktokTopAdsSearchData]:
        """TikTok Top Ads Search

        Search TikTok Creative Center top video ads by keyword, with campaign
        objective, performance percentile, and time-window filters.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.top_ads_search(query="glasses")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.top_ads_search", dict(input), options
        )
        return RunResult[TiktokTopAdsSearchData].model_validate(raw)

    def trending_feed(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokTrendingFeedInput],
    ) -> RunResult[TiktokTrendingFeedData]:
        """TikTok Trending Feed

        Sample TikTok's For You feed as served to a viewer in one country (caption,
        views, likes, comments, author). Returns a rotating sample, not a ranked
        chart.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.trending_feed(region="US")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.trending_feed", dict(input), options
        )
        return RunResult[TiktokTrendingFeedData].model_validate(raw)

    def trending_hashtags(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokTrendingHashtagsInput],
    ) -> RunResult[TiktokTrendingHashtagsData]:
        """TikTok Trending Hashtags

        Rank TikTok's trending hashtags for one country and industry, with each
        hashtag's daily popularity curve, post count, video views, and leading
        creators. Ranks 15 industry categories, or omit industry for the
        all-industries board. TikTok publishes only the top 3 hashtags per board to
        anonymous callers, so limit 1-3 is served cheaply; a limit above 3 routes to
        a dearer authenticated source that returns the full ranking. Covers 27
        markets: AE, AR, AU, BR, CA, CO, DE, EG, ES, FR, GB, ID, IL, IT, JP, KR, MX,
        MY, PH, SA, SG, TH, TR, TW, US, VN, ZA.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.trending_hashtags(limit=3, period=7, region="US")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.trending_hashtags", dict(input), options
        )
        return RunResult[TiktokTrendingHashtagsData].model_validate(raw)

    def user_stories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokUserStoriesInput],
    ) -> RunResult[TiktokUserStoriesData]:
        """TikTok User Stories

        Get a TikTok creator's active public stories by username: video or photo
        links, cover, posting and expiry times, and view, like, share and save
        counts.

        Price: $0.0011 per request.

        Example:
            res = client.tiktok.user_stories(handle="jasonderulo")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.user_stories", dict(input), options
        )
        return RunResult[TiktokUserStoriesData].model_validate(raw)

    def video(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoInput],
    ) -> RunResult[TiktokVideoData]:
        """TikTok Video

        Fetch a single TikTok video by URL with its caption and engagement counts
        (views, likes, comments, shares, saves).

        Price: $0.0004 per request.

        Example:
            res = client.tiktok.video(url="https://www.tiktok.com/@mrbeast/video/7654638524729216287?_r=1&u_code=elgjf3ff8cajhk&preview_pb=0&sharer_language=en&_d=elh6737j6kjl71&share_item_id=7654638524729216287&source=h5_m")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video", dict(input), options
        )
        return RunResult[TiktokVideoData].model_validate(raw)

    def video_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoCommentsInput],
    ) -> RunResult[TiktokVideoCommentsData]:
        """TikTok Video Comments

        List the comments on a TikTok video by URL with cursor pagination (text,
        author, likes, reply count).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.video_comments(url="https://www.tiktok.com/@zachking/video/7650468599424945422?_r=1&u_code=f0hj7d780760m9&preview_pb=0&sharer_language=en&_d=f0hj7blh067h71&share_item_id=7650468599424945422&source=h5_m")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_comments", dict(input), options
        )
        return RunResult[TiktokVideoCommentsData].model_validate(raw)

    def iter_video_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoCommentsInput],
    ) -> Paginator[TiktokVideoCommentsComment, TiktokVideoCommentsData]:
        """Iterate TikTok Video Comments results, following pagination cursors.

        Yields validated `TiktokVideoCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok.video_comments",
            dict(input),
            "comments",
            item_model=TiktokVideoCommentsComment,
            data_model=TiktokVideoCommentsData,
            bare=False,
            options=options,
        )

    def video_download(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoDownloadInput],
    ) -> RunResult[TiktokVideoDownloadData]:
        """TikTok Video Download

        Get the playable media files behind a TikTok video URL: the clean
        no-watermark MP4, the watermarked one TikTok's own save button produces, and
        the cover image, with duration and pixel dimensions. Photo-mode posts carry
        no video file - use tiktok.photos for those.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.video_download(url="https://www.tiktok.com/@mrbeast/video/7654638524729216287")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_download", dict(input), options
        )
        return RunResult[TiktokVideoDownloadData].model_validate(raw)

    def video_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoTranscriptInput],
    ) -> RunResult[TiktokVideoTranscriptData]:
        """TikTok Video Transcript (native captions)

        Fetch the caption track TikTok itself published for a video, as TikTok wrote
        it. It is the cheapest way to get the words, and it is only as good as
        TikTok's own transcription: it mishears names and uncommon words, and many
        videos - especially non-English ones - have no caption track at all, which
        comes back as not found. When you need the words to be right, or there is no
        track to read, tiktok.video_transcript_full transcribes the audio with
        AnyAPI's own speech-to-text instead.

        Price: $0.0011 per request.

        Example:
            res = client.tiktok.video_transcript(url="https://www.tiktok.com/@washingtonpost/video/7609177768793787679")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_transcript", dict(input), options
        )
        return RunResult[TiktokVideoTranscriptData].model_validate(raw)

    def video_transcript_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoTranscriptFullInput],
    ) -> RunResult[TiktokVideoTranscriptFullData]:
        """TikTok Video Transcript (AnyAPI speech to text)

        Transcribe the spoken audio of a TikTok video with AnyAPI's own
        speech-to-text: timed sentence-level segments, speaker labels, detected
        language, and optional per-word timings, for videos TikTok publishes no
        caption track for and for videos whose caption track gets the words wrong.
        AnyAPI downloads the video and runs the audio through MAI-Transcribe-2
        rather than reading anything TikTok wrote, which is why it handles
        non-English speech and hears words the native captions mishear. The answer
        also carries the video's id, URL, creator handle, and cover image. Turn on
        hostVideo to also get the MP4 on a hosted link that plays without TikTok's
        signed, short-lived CDN URL expiring on you. If you only want whatever
        TikTok itself published and you want it for a tenth of the price,
        tiktok.video_transcript is that.

        Price: $0.0015 per request plus $0.006 per audio minute (maximum $0.095).

        Example:
            res = client.tiktok.video_transcript_full(url="https://www.tiktok.com/@thatdudecancook/video/7649086431641521421")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_transcript_full", dict(input), options
        )
        return RunResult[TiktokVideoTranscriptFullData].model_validate(raw)


class AsyncTiktokNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ad_library_ad(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdLibraryAdInput],
    ) -> RunResult[TiktokAdLibraryAdData]:
        """TikTok Ad Library Ad

        Fetch full details for a single TikTok ad (brand, title, spend, CTR,
        objectives, landing page, and video info).

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.ad_library_ad(adId="7648493525660270600")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.ad_library_ad", dict(input), options
        )
        return RunResult[TiktokAdLibraryAdData].model_validate(raw)

    async def ad_library_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdLibrarySearchInput],
    ) -> RunResult[TiktokAdLibrarySearchData]:
        """TikTok Ad Library Search

        Search TikTok's public Ads Library by keyword or advertiser (advertiser,
        title, audience band, run dates, library link, and video).

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.ad_library_search(query="spotify")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.ad_library_search", dict(input), options
        )
        return RunResult[TiktokAdLibrarySearchData].model_validate(raw)

    def iter_ad_library_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdLibrarySearchInput],
    ) -> AsyncPaginator[TiktokAdLibrarySearchAd, TiktokAdLibrarySearchData]:
        """Iterate TikTok Ad Library Search results, following pagination cursors.

        Yields validated `TiktokAdLibrarySearchAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.ad_library_search",
            dict(input),
            "ads",
            item_model=TiktokAdLibrarySearchAd,
            data_model=TiktokAdLibrarySearchData,
            bare=False,
            options=options,
        )

    async def ad_transparency_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdTransparencySearchInput],
    ) -> RunResult[TiktokAdTransparencySearchData]:
        """TikTok Ad Transparency Search

        Search TikTok's EU Commercial Content Library by keyword or advertiser ID.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.ad_transparency_search(days=30, limit=20, query="nike", region="DE")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.ad_transparency_search", dict(input), options
        )
        return RunResult[TiktokAdTransparencySearchData].model_validate(raw)

    def iter_ad_transparency_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAdTransparencySearchInput],
    ) -> AsyncPaginator[TiktokAdTransparencySearchAd, TiktokAdTransparencySearchData]:
        """Iterate TikTok Ad Transparency Search results, following pagination cursors.

        Yields validated `TiktokAdTransparencySearchAd` items from the `ads` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.ad_transparency_search",
            dict(input),
            "ads",
            item_model=TiktokAdTransparencySearchAd,
            data_model=TiktokAdTransparencySearchData,
            bare=False,
            options=options,
        )

    async def audience_demographics(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokAudienceDemographicsInput],
    ) -> RunResult[TiktokAudienceDemographicsData]:
        """TikTok Audience Demographics

        Get the audience country breakdown (follower count and share per country)
        for a TikTok creator by handle.

        Price: $0.018 per request.

        Example:
            res = client.tiktok.audience_demographics(handle="shakira")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.audience_demographics", dict(input), options
        )
        return RunResult[TiktokAudienceDemographicsData].model_validate(raw)

    async def comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokCommentRepliesInput],
    ) -> RunResult[TiktokCommentRepliesData]:
        """TikTok Comment Replies

        List the replies to a TikTok comment with cursor pagination (text, author,
        likes).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.comment_replies(commentId="7623828115408274207", url="https://www.tiktok.com/@stoolpresidente/video/7623818255903329566")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.comment_replies", dict(input), options
        )
        return RunResult[TiktokCommentRepliesData].model_validate(raw)

    def iter_comment_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokCommentRepliesInput],
    ) -> AsyncPaginator[TiktokCommentRepliesComment, TiktokCommentRepliesData]:
        """Iterate TikTok Comment Replies results, following pagination cursors.

        Yields validated `TiktokCommentRepliesComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.comment_replies",
            dict(input),
            "comments",
            item_model=TiktokCommentRepliesComment,
            data_model=TiktokCommentRepliesData,
            bare=False,
            options=options,
        )

    async def followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowersInput],
    ) -> RunResult[TiktokFollowersData]:
        """TikTok Followers

        List the followers of a TikTok account by username, returning each
        follower's profile basics.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.followers(handle="stoolpresidente")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.followers", dict(input), options
        )
        return RunResult[TiktokFollowersData].model_validate(raw)

    def iter_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowersInput],
    ) -> AsyncPaginator[TiktokFollowersFollower, TiktokFollowersData]:
        """Iterate TikTok Followers results, following pagination cursors.

        Yields validated `TiktokFollowersFollower` items from the `followers` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.followers",
            dict(input),
            "followers",
            item_model=TiktokFollowersFollower,
            data_model=TiktokFollowersData,
            bare=False,
            options=options,
        )

    async def following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowingInput],
    ) -> RunResult[TiktokFollowingData]:
        """TikTok Following

        List the accounts a TikTok user follows (handle, display name, follower
        count, bio) by username.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.following(handle="stoolpresidente")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.following", dict(input), options
        )
        return RunResult[TiktokFollowingData].model_validate(raw)

    def iter_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokFollowingInput],
    ) -> AsyncPaginator[TiktokFollowingFollowing, TiktokFollowingData]:
        """Iterate TikTok Following results, following pagination cursors.

        Yields validated `TiktokFollowingFollowing` items from the `following` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.following",
            dict(input),
            "following",
            item_model=TiktokFollowingFollowing,
            data_model=TiktokFollowingData,
            bare=False,
            options=options,
        )

    async def hashtag_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokHashtagVideosInput],
    ) -> RunResult[TiktokHashtagVideosData]:
        """TikTok Hashtag Videos

        List recent TikTok videos for a hashtag (creator, caption, views, likes,
        shares).

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.hashtag_videos(hashtag="cooking", limit=3)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.hashtag_videos", dict(input), options
        )
        return RunResult[TiktokHashtagVideosData].model_validate(raw)

    def iter_hashtag_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokHashtagVideosInput],
    ) -> AsyncPaginator[TiktokHashtagVideosItem, TiktokHashtagVideosData]:
        """Iterate TikTok Hashtag Videos results, following pagination cursors.

        Yields validated `TiktokHashtagVideosItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.hashtag_videos",
            dict(input),
            "items",
            item_model=TiktokHashtagVideosItem,
            data_model=TiktokHashtagVideosData,
            bare=False,
            options=options,
        )

    async def live(
        self, *, options: RequestOptions | None = None, **input: Unpack[TiktokLiveInput]
    ) -> RunResult[TiktokLiveData]:
        """TikTok Live

        Check whether a TikTok creator is live and get the current live room (title,
        viewers, start time) by handle.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.live(handle="thejustalex")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.live", dict(input), options
        )
        return RunResult[TiktokLiveData].model_validate(raw)

    async def photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokPhotosInput],
    ) -> RunResult[TiktokPhotosData]:
        """TikTok Photos

        Get every image in a TikTok photo-mode (slideshow) post by URL, in order,
        with pixel dimensions and both the clean and watermarked variant of each.
        Videos carry no images - use tiktok.video_download for those.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.photos(url="https://www.tiktok.com/@foodbyfranchi/video/7479916555602513174")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.photos", dict(input), options
        )
        return RunResult[TiktokPhotosData].model_validate(raw)

    async def playlist_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokPlaylistVideosInput],
    ) -> RunResult[TiktokPlaylistVideosData]:
        """TikTok Playlist Videos

        List the videos inside one TikTok playlist by playlist URL or id, in
        playlist order, with view, like and comment counts.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.playlist_videos(url="https://www.tiktok.com/@mrbeast/playlist/Beast%20Games-7596415294902389534")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.playlist_videos", dict(input), options
        )
        return RunResult[TiktokPlaylistVideosData].model_validate(raw)

    def iter_playlist_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokPlaylistVideosInput],
    ) -> AsyncPaginator[TiktokPlaylistVideosVideo, TiktokPlaylistVideosData]:
        """Iterate TikTok Playlist Videos results, following pagination cursors.

        Yields validated `TiktokPlaylistVideosVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.playlist_videos",
            dict(input),
            "videos",
            item_model=TiktokPlaylistVideosVideo,
            data_model=TiktokPlaylistVideosData,
            bare=False,
            options=options,
        )

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileInput],
    ) -> RunResult[TiktokProfileData]:
        """TikTok Profile

        Fetch a TikTok creator's public profile (followers, likes, bio,
        verification) by handle.

        Price: $0.0004 per request.

        Example:
            res = client.tiktok.profile(handle="zachking")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile", dict(input), options
        )
        return RunResult[TiktokProfileData].model_validate(raw)

    async def profile_contact(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileContactInput],
    ) -> RunResult[TiktokProfileContactData]:
        """TikTok Profile Contact Info

        Find the public contact email behind a TikTok creator's profile: the address
        written into the bio plus any published on the site the profile links to,
        each labelled with where it came from. Returns the creator's profile stats
        and linked social accounts alongside.

        Price: $0.00116 per request plus $0 per result (maximum $0.00116).

        Example:
            res = client.tiktok.profile_contact(handle="gordonramsayofficial")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_contact", dict(input), options
        )
        return RunResult[TiktokProfileContactData].model_validate(raw)

    async def profile_playlists(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfilePlaylistsInput],
    ) -> RunResult[TiktokProfilePlaylistsData]:
        """TikTok Profile Playlists

        List the playlists a TikTok creator has published on their profile, with
        each playlist's name, video count and cover image.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.profile_playlists(secUid="MS4wLjABAAAABKjQkOz_IIzXXzEAl_9LGsWhvK-gBnlczwRPXK8EmxAp6K3X0qiaP5_OEqmm0XwG")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_playlists", dict(input), options
        )
        return RunResult[TiktokProfilePlaylistsData].model_validate(raw)

    def iter_profile_playlists(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfilePlaylistsInput],
    ) -> AsyncPaginator[TiktokProfilePlaylistsPlaylist, TiktokProfilePlaylistsData]:
        """Iterate TikTok Profile Playlists results, following pagination cursors.

        Yields validated `TiktokProfilePlaylistsPlaylist` items from the `playlists` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.profile_playlists",
            dict(input),
            "playlists",
            item_model=TiktokProfilePlaylistsPlaylist,
            data_model=TiktokProfilePlaylistsData,
            bare=False,
            options=options,
        )

    async def profile_region(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileRegionInput],
    ) -> RunResult[TiktokProfileRegionData]:
        """TikTok Profile Region

        Resolve the home region (country) of a TikTok creator by handle.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.profile_region(handle="stoolpresidente")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_region", dict(input), options
        )
        return RunResult[TiktokProfileRegionData].model_validate(raw)

    async def profile_reposts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileRepostsInput],
    ) -> RunResult[TiktokProfileRepostsData]:
        """TikTok Profile Reposts

        List the videos a TikTok creator has reposted to their profile, with view,
        like and comment counts and cursor pagination.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.profile_reposts(secUid="MS4wLjABAAAABKjQkOz_IIzXXzEAl_9LGsWhvK-gBnlczwRPXK8EmxAp6K3X0qiaP5_OEqmm0XwG")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_reposts", dict(input), options
        )
        return RunResult[TiktokProfileRepostsData].model_validate(raw)

    def iter_profile_reposts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileRepostsInput],
    ) -> AsyncPaginator[TiktokProfileRepostsVideo, TiktokProfileRepostsData]:
        """Iterate TikTok Profile Reposts results, following pagination cursors.

        Yields validated `TiktokProfileRepostsVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.profile_reposts",
            dict(input),
            "videos",
            item_model=TiktokProfileRepostsVideo,
            data_model=TiktokProfileRepostsData,
            bare=False,
            options=options,
        )

    async def profile_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileVideosInput],
    ) -> RunResult[TiktokProfileVideosData]:
        """TikTok Profile Videos

        List a TikTok creator's recent videos (views, likes, comments) by handle
        with cursor pagination.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.profile_videos(handle="zachking")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.profile_videos", dict(input), options
        )
        return RunResult[TiktokProfileVideosData].model_validate(raw)

    def iter_profile_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokProfileVideosInput],
    ) -> AsyncPaginator[TiktokProfileVideosVideo, TiktokProfileVideosData]:
        """Iterate TikTok Profile Videos results, following pagination cursors.

        Yields validated `TiktokProfileVideosVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.profile_videos",
            dict(input),
            "videos",
            item_model=TiktokProfileVideosVideo,
            data_model=TiktokProfileVideosData,
            bare=False,
            options=options,
        )

    async def search_hashtag(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchHashtagInput],
    ) -> RunResult[TiktokSearchHashtagData]:
        """TikTok Hashtag Search

        Search TikTok by hashtag and get matching videos (caption, views, likes,
        comments, shares) as normalized JSON.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.search_hashtag(query="recipe")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_hashtag", dict(input), options
        )
        return RunResult[TiktokSearchHashtagData].model_validate(raw)

    def iter_search_hashtag(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchHashtagInput],
    ) -> AsyncPaginator[TiktokSearchHashtagVideo, TiktokSearchHashtagData]:
        """Iterate TikTok Hashtag Search results, following pagination cursors.

        Yields validated `TiktokSearchHashtagVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.search_hashtag",
            dict(input),
            "videos",
            item_model=TiktokSearchHashtagVideo,
            data_model=TiktokSearchHashtagData,
            bare=False,
            options=options,
        )

    async def search_keyword(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchKeywordInput],
    ) -> RunResult[TiktokSearchKeywordData]:
        """TikTok Keyword Search

        Search TikTok by keyword and get matching videos (caption, views, likes,
        comments, shares) as normalized JSON.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.search_keyword(datePosted=0, query="cooking", sortBy="relevance")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_keyword", dict(input), options
        )
        return RunResult[TiktokSearchKeywordData].model_validate(raw)

    def iter_search_keyword(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchKeywordInput],
    ) -> AsyncPaginator[TiktokSearchKeywordVideo, TiktokSearchKeywordData]:
        """Iterate TikTok Keyword Search results, following pagination cursors.

        Yields validated `TiktokSearchKeywordVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.search_keyword",
            dict(input),
            "videos",
            item_model=TiktokSearchKeywordVideo,
            data_model=TiktokSearchKeywordData,
            bare=False,
            options=options,
        )

    async def search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchPhotosInput],
    ) -> RunResult[TiktokSearchPhotosData]:
        """TikTok Photo Search

        Search TikTok for photo-mode (slideshow) posts by keyword, with every image
        in each post plus view, like and comment counts. tiktok.search_keyword
        returns videos and drops these.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.search_photos(query="latte art")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_photos", dict(input), options
        )
        return RunResult[TiktokSearchPhotosData].model_validate(raw)

    def iter_search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchPhotosInput],
    ) -> AsyncPaginator[TiktokSearchPhotosPost, TiktokSearchPhotosData]:
        """Iterate TikTok Photo Search results, following pagination cursors.

        Yields validated `TiktokSearchPhotosPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.search_photos",
            dict(input),
            "posts",
            item_model=TiktokSearchPhotosPost,
            data_model=TiktokSearchPhotosData,
            bare=False,
            options=options,
        )

    async def search_suggestions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchSuggestionsInput],
    ) -> RunResult[TiktokSearchSuggestionsData]:
        """TikTok Search Suggestions

        Get the search terms TikTok suggests for a keyword, each with its language
        and relative weight - the queries real TikTok users type around your topic.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.search_suggestions(query="protein powder")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_suggestions", dict(input), options
        )
        return RunResult[TiktokSearchSuggestionsData].model_validate(raw)

    async def search_top(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchTopInput],
    ) -> RunResult[TiktokSearchTopData]:
        """TikTok Top Search

        Search TikTok's top results for a keyword (caption, views, likes, comments,
        shares) with cursor pagination.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.search_top(query="funny")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_top", dict(input), options
        )
        return RunResult[TiktokSearchTopData].model_validate(raw)

    def iter_search_top(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchTopInput],
    ) -> AsyncPaginator[TiktokSearchTopItem, TiktokSearchTopData]:
        """Iterate TikTok Top Search results, following pagination cursors.

        Yields validated `TiktokSearchTopItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.search_top",
            dict(input),
            "items",
            item_model=TiktokSearchTopItem,
            data_model=TiktokSearchTopData,
            bare=False,
            options=options,
        )

    async def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchUsersInput],
    ) -> RunResult[TiktokSearchUsersData]:
        """TikTok User Search

        Search TikTok accounts by keyword (handle, nickname, follower count) with
        cursor pagination.

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.search_users(query="chef")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.search_users", dict(input), options
        )
        return RunResult[TiktokSearchUsersData].model_validate(raw)

    def iter_search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSearchUsersInput],
    ) -> AsyncPaginator[TiktokSearchUsersUser, TiktokSearchUsersData]:
        """Iterate TikTok User Search results, following pagination cursors.

        Yields validated `TiktokSearchUsersUser` items from the `users` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.search_users",
            dict(input),
            "users",
            item_model=TiktokSearchUsersUser,
            data_model=TiktokSearchUsersData,
            bare=False,
            options=options,
        )

    async def song(
        self, *, options: RequestOptions | None = None, **input: Unpack[TiktokSongInput]
    ) -> RunResult[TiktokSongData]:
        """TikTok Song

        Fetch details for a TikTok song or sound (title, author, duration, cover
        art, and how many videos use it).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.song(clipId="7439295283975702544")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.song", dict(input), options
        )
        return RunResult[TiktokSongData].model_validate(raw)

    async def song_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSongVideosInput],
    ) -> RunResult[TiktokSongVideosData]:
        """TikTok Song Videos

        List TikTok videos that use a given song or sound (with descriptions,
        authors, and engagement stats).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.song_videos(clipId="7439295283975702544")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.song_videos", dict(input), options
        )
        return RunResult[TiktokSongVideosData].model_validate(raw)

    def iter_song_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokSongVideosInput],
    ) -> AsyncPaginator[TiktokSongVideosVideo, TiktokSongVideosData]:
        """Iterate TikTok Song Videos results, following pagination cursors.

        Yields validated `TiktokSongVideosVideo` items from the `videos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.song_videos",
            dict(input),
            "videos",
            item_model=TiktokSongVideosVideo,
            data_model=TiktokSongVideosData,
            bare=False,
            options=options,
        )

    async def top_ads_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokTopAdsSearchInput],
    ) -> RunResult[TiktokTopAdsSearchData]:
        """TikTok Top Ads Search

        Search TikTok Creative Center top video ads by keyword, with campaign
        objective, performance percentile, and time-window filters.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.top_ads_search(query="glasses")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.top_ads_search", dict(input), options
        )
        return RunResult[TiktokTopAdsSearchData].model_validate(raw)

    async def trending_feed(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokTrendingFeedInput],
    ) -> RunResult[TiktokTrendingFeedData]:
        """TikTok Trending Feed

        Sample TikTok's For You feed as served to a viewer in one country (caption,
        views, likes, comments, author). Returns a rotating sample, not a ranked
        chart.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.trending_feed(region="US")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.trending_feed", dict(input), options
        )
        return RunResult[TiktokTrendingFeedData].model_validate(raw)

    async def trending_hashtags(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokTrendingHashtagsInput],
    ) -> RunResult[TiktokTrendingHashtagsData]:
        """TikTok Trending Hashtags

        Rank TikTok's trending hashtags for one country and industry, with each
        hashtag's daily popularity curve, post count, video views, and leading
        creators. Ranks 15 industry categories, or omit industry for the
        all-industries board. TikTok publishes only the top 3 hashtags per board to
        anonymous callers, so limit 1-3 is served cheaply; a limit above 3 routes to
        a dearer authenticated source that returns the full ranking. Covers 27
        markets: AE, AR, AU, BR, CA, CO, DE, EG, ES, FR, GB, ID, IL, IT, JP, KR, MX,
        MY, PH, SA, SG, TH, TR, TW, US, VN, ZA.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok.trending_hashtags(limit=3, period=7, region="US")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.trending_hashtags", dict(input), options
        )
        return RunResult[TiktokTrendingHashtagsData].model_validate(raw)

    async def user_stories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokUserStoriesInput],
    ) -> RunResult[TiktokUserStoriesData]:
        """TikTok User Stories

        Get a TikTok creator's active public stories by username: video or photo
        links, cover, posting and expiry times, and view, like, share and save
        counts.

        Price: $0.0011 per request.

        Example:
            res = client.tiktok.user_stories(handle="jasonderulo")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.user_stories", dict(input), options
        )
        return RunResult[TiktokUserStoriesData].model_validate(raw)

    async def video(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoInput],
    ) -> RunResult[TiktokVideoData]:
        """TikTok Video

        Fetch a single TikTok video by URL with its caption and engagement counts
        (views, likes, comments, shares, saves).

        Price: $0.0004 per request.

        Example:
            res = client.tiktok.video(url="https://www.tiktok.com/@mrbeast/video/7654638524729216287?_r=1&u_code=elgjf3ff8cajhk&preview_pb=0&sharer_language=en&_d=elh6737j6kjl71&share_item_id=7654638524729216287&source=h5_m")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video", dict(input), options
        )
        return RunResult[TiktokVideoData].model_validate(raw)

    async def video_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoCommentsInput],
    ) -> RunResult[TiktokVideoCommentsData]:
        """TikTok Video Comments

        List the comments on a TikTok video by URL with cursor pagination (text,
        author, likes, reply count).

        Price: $0.0006 per request.

        Example:
            res = client.tiktok.video_comments(url="https://www.tiktok.com/@zachking/video/7650468599424945422?_r=1&u_code=f0hj7d780760m9&preview_pb=0&sharer_language=en&_d=f0hj7blh067h71&share_item_id=7650468599424945422&source=h5_m")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_comments", dict(input), options
        )
        return RunResult[TiktokVideoCommentsData].model_validate(raw)

    def iter_video_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoCommentsInput],
    ) -> AsyncPaginator[TiktokVideoCommentsComment, TiktokVideoCommentsData]:
        """Iterate TikTok Video Comments results, following pagination cursors.

        Yields validated `TiktokVideoCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok.video_comments",
            dict(input),
            "comments",
            item_model=TiktokVideoCommentsComment,
            data_model=TiktokVideoCommentsData,
            bare=False,
            options=options,
        )

    async def video_download(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoDownloadInput],
    ) -> RunResult[TiktokVideoDownloadData]:
        """TikTok Video Download

        Get the playable media files behind a TikTok video URL: the clean
        no-watermark MP4, the watermarked one TikTok's own save button produces, and
        the cover image, with duration and pixel dimensions. Photo-mode posts carry
        no video file - use tiktok.photos for those.

        Price: $0.0008 per request.

        Example:
            res = client.tiktok.video_download(url="https://www.tiktok.com/@mrbeast/video/7654638524729216287")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_download", dict(input), options
        )
        return RunResult[TiktokVideoDownloadData].model_validate(raw)

    async def video_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoTranscriptInput],
    ) -> RunResult[TiktokVideoTranscriptData]:
        """TikTok Video Transcript (native captions)

        Fetch the caption track TikTok itself published for a video, as TikTok wrote
        it. It is the cheapest way to get the words, and it is only as good as
        TikTok's own transcription: it mishears names and uncommon words, and many
        videos - especially non-English ones - have no caption track at all, which
        comes back as not found. When you need the words to be right, or there is no
        track to read, tiktok.video_transcript_full transcribes the audio with
        AnyAPI's own speech-to-text instead.

        Price: $0.0011 per request.

        Example:
            res = client.tiktok.video_transcript(url="https://www.tiktok.com/@washingtonpost/video/7609177768793787679")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_transcript", dict(input), options
        )
        return RunResult[TiktokVideoTranscriptData].model_validate(raw)

    async def video_transcript_full(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokVideoTranscriptFullInput],
    ) -> RunResult[TiktokVideoTranscriptFullData]:
        """TikTok Video Transcript (AnyAPI speech to text)

        Transcribe the spoken audio of a TikTok video with AnyAPI's own
        speech-to-text: timed sentence-level segments, speaker labels, detected
        language, and optional per-word timings, for videos TikTok publishes no
        caption track for and for videos whose caption track gets the words wrong.
        AnyAPI downloads the video and runs the audio through MAI-Transcribe-2
        rather than reading anything TikTok wrote, which is why it handles
        non-English speech and hears words the native captions mishear. The answer
        also carries the video's id, URL, creator handle, and cover image. Turn on
        hostVideo to also get the MP4 on a hosted link that plays without TikTok's
        signed, short-lived CDN URL expiring on you. If you only want whatever
        TikTok itself published and you want it for a tenth of the price,
        tiktok.video_transcript is that.

        Price: $0.0015 per request plus $0.006 per audio minute (maximum $0.095).

        Example:
            res = client.tiktok.video_transcript_full(url="https://www.tiktok.com/@thatdudecancook/video/7649086431641521421")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok.video_transcript_full", dict(input), options
        )
        return RunResult[TiktokVideoTranscriptFullData].model_validate(raw)
