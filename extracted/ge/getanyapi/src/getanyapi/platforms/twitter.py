# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the twitter platform."""

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


class TwitterArticleInput(TypedDict, total=False):
    """Input for X / Twitter Article."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Canonical x.com or twitter.com URL of the public wrapper post for an X Article."""


class TwitterCommunityInput(TypedDict, total=False):
    """Input for Twitter Community."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Community URL (e.g. https://x.com/i/communities/1926186499399139650)."""


class TwitterCommunityTweetsInput(TypedDict, total=False):
    """Input for Twitter Community Tweets."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Community URL (e.g. https://x.com/i/communities/1926186499399139650)."""


class TwitterFollowersInput(TypedDict, total=False):
    """Input for X / Twitter Followers."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of followers."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Accepted but does not change the page: every call returns one full native page of followers (up to 200, depending on the source), never trimmed, so follow nextCursor to continue exactly where this response ended. Range: 1 to 100000. Default: 200."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["bio", "following"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `bio`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    username: Required[str]
    """The X (Twitter) username to fetch followers for, without the @ prefix (e.g. elonmusk)."""


class TwitterFollowingInput(TypedDict, total=False):
    """Input for X / Twitter Following."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of followed accounts."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Accepted but does not change the page: every call returns one full native page of followed accounts (about 50), never trimmed, so follow nextCursor to continue exactly where this response ended. Range: 1 to 100000. Default: 200."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["location"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `location`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    username: Required[str]
    """The X (Twitter) username to fetch the following list for, without the @ prefix (e.g. elonmusk)."""


class TwitterProfileInput(TypedDict, total=False):
    """Input for Twitter Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """Twitter/X handle without the leading @."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TwitterRepliesInput(TypedDict, total=False):
    """Input for X / Twitter Post Replies."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of replies."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-40, default 40). Per-result lanes cost less at lower limits; a backup that bills its native page may cost up to the advertised request price. Range: 1 to 40."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["nextCursor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full URL of the X (Twitter) post to fetch replies for (e.g. https://x.com/nasa/status/1846987139428634858)."""


class TwitterSearchInput(TypedDict, total=False):
    """Input for X / Twitter Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of search results."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Page size to ask for (1-50, default 20). Some sources honor it; others always return their whole native page of about 20. A page is never trimmed after the call, so follow nextCursor to continue exactly where this response ended. Range: 1 to 50. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search query using X (Twitter) advanced-search syntax. IMPORTANT: bare terms are ANDed - a tweet must contain EVERY word, so a list of loosely related keywords matches nothing; use one short phrase or OR between alternatives (e.g. 'anyapi OR getanyapi'). When an operator follows an OR list, put the list in parentheses, e.g. '(anyapi OR getanyapi) -filter:replies': without them X applies the operator to the last alternative only, so such a query still runs as X reads it and the response's hint carries the corrected query. You can embed X advanced-search operators directly in the query to filter results: from:username and to:username (author or recipient), since:YYYY-MM-DD and until:YYYY-MM-DD (date range), min_faves:N, min_retweets:N, min_replies:N (engagement floors), "exact phrase", -term to exclude, filter:media and filter:links and -filter:replies (content filters), lang:en, near:city, and geocode:lat,long,radius. Examples: 'from:OpenAI', 'AI agents min_faves:500 -filter:replies', 'nvidia since:2026-01-01 until:2026-03-01'. A query with no matches returns an empty items array; prefer the fewest words that identify the topic."""
    queryType: NotRequired[Literal["Latest", "Top", "Photos", "Videos"]]
    """Which posts to return: 'Latest' (newest first, the default), 'Top' (most popular), 'Photos' (newest posts with images), or 'Videos' (newest posts with video). Photos and Videos search your query as written with filter:images or filter:videos added after it, so they cost the same as a Latest search. Default: Latest."""
    requireFields: NotRequired[list[Literal["nextCursor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    requireSinglePage: NotRequired[bool]
    """Set true to get up to limit results in one response instead of provider-native pages, served by a bulk provider when needed."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TwitterSearchCommunitiesInput(TypedDict, total=False):
    """Input for X / Twitter Community Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of communities."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to match against X (Twitter) community names and topics (e.g. artificial intelligence)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TwitterSearchUsersInput(TypedDict, total=False):
    """Input for X / Twitter User Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of accounts."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to match against X (Twitter) handles, display names, and profile bios. This is the People tab of X search: pass a topic ('ai agents'), a name ('Elon Musk'), or a handle ('openai') and get back accounts, not posts. Use twitter.search for posts."""
    requireFields: NotRequired[list[Literal["canDm", "listedCount", "location"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `location`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a profile that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TwitterThreadInput(TypedDict, total=False):
    """Input for X / Twitter Tweet Thread."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Canonical x.com or twitter.com status URL with a numeric tweet ID. Any tweet in the self-thread can be supplied; the provider resolves the thread root."""


class TwitterTrendsInput(TypedDict, total=False):
    """Input for X / Twitter Trends."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of ranked trends to return (1-50, default 50). Range: 1 to 50. Default: 50."""
    location: NotRequired[str]
    """Country name, city name, or ISO country code. Omit for worldwide trends."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["isHashtag", "promoted"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `promoted`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a trend that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TwitterTweetInput(TypedDict, total=False):
    """Input for Twitter Tweet."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["height", "videoUrl", "width"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `videoUrl` or `width`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a tweet that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Canonical x.com or twitter.com status URL with a numeric tweet ID, including /i/web/status and media-share variants."""


class TwitterTweetTranscriptInput(TypedDict, total=False):
    """Input for Twitter Tweet Transcript."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Tweet URL of the video to transcribe (e.g. https://x.com/TheoVon/status/1916982720317821050)."""


class TwitterUserPostsInput(TypedDict, total=False):
    """Input for X / Twitter User Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page."""
    handle: Required[str]
    """Twitter/X handle without the leading @."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["isPinned"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `isPinned`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a tweet that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TwitterUserTweetsInput(TypedDict, total=False):
    """Input for X / Twitter User Tweets and Replies."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page."""
    handle: Required[str]
    """Twitter/X handle without the leading @."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Page size to ask for (1-100, default 20). Some sources honor it; others always return their whole native page of about 20 authored tweets and replies. A page is never trimmed after the call, so follow nextCursor and pass it back as cursor to continue exactly where this response ended. Range: 1 to 100. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["isPinned"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `isPinned`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    requireSinglePage: NotRequired[bool]
    """Require a lane that can return the requested limit in one response."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TwitterArticleData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    author: TwitterArticleAuthor = Field(
        description="Article author profile at retrieval time. Populated whenever the provider has data for the entity."
    )
    content_blocks: list[TwitterArticleContentBlock] = Field(
        alias="contentBlocks",
        description="Ordered, explicitly normalized article blocks. Unknown future block types remain representable through type and optional fields. Populated whenever the provider has data for the entity.",
    )
    cover_image: str | None = Field(
        default=None,
        alias="coverImage",
        description="Canonical article cover image URL when available.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Stable X Article entity ID. Populated whenever the provider has data for the entity."
    )
    likes: int | None = Field(
        default=None,
        description="Wrapper post like count at retrieval time. Minimum: 0.",
    )
    preview_text: str | None = Field(
        default=None, alias="previewText", description="Preview text supplied by X."
    )
    quotes: int | None = Field(
        default=None,
        description="Wrapper post quote count at retrieval time. Minimum: 0.",
    )
    replies: int | None = Field(
        default=None,
        description="Wrapper post reply count at retrieval time. Minimum: 0.",
    )
    title: str = Field(
        description="Article title. Populated whenever the provider has data for the entity."
    )
    views: int | None = Field(
        default=None,
        description="Wrapper post view count at retrieval time. Minimum: 0.",
    )


class TwitterArticleAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None, alias="avatarUrl", description="Profile avatar image URL."
    )
    bio: str | None = Field(default=None, description="Profile biography.")
    blue_verified: bool | None = Field(
        default=None,
        alias="blueVerified",
        description="Whether the account has X blue verification.",
    )
    cover_url: str | None = Field(
        default=None,
        alias="coverUrl",
        description="Profile cover image URL when available.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    followers: int | None = Field(
        default=None, description="Follower count at retrieval time. Minimum: 0."
    )
    following: int | None = Field(
        default=None, description="Following count at retrieval time. Minimum: 0."
    )
    handle: str = Field(
        description="Current X handle without @. Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Stable numeric X user ID. Populated whenever the provider has data for the entity."
    )
    location: str | None = Field(
        default=None, description="Self-reported profile location."
    )
    media_count: int | None = Field(
        default=None,
        alias="mediaCount",
        description="Number of media items the author has published.",
    )
    name: str | None = Field(default=None, description="Profile display name.")
    posts: int | None = Field(
        default=None, description="Number of posts the author has published."
    )
    url: str = Field(
        description="Canonical public X profile URL. Populated whenever the provider has data for the entity."
    )
    verified: bool | None = Field(
        default=None, description="Whether the account has legacy verification."
    )


class TwitterArticleContentBlock(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    entities: list[TwitterArticleEntitie] | None = Field(
        default=None, description="Entity references within the block text."
    )
    height: int | None = Field(
        default=None, description="Image height in pixels when supplied. Minimum: 0."
    )
    image: str | None = Field(
        default=None, description="Canonical image URL for an image block."
    )
    inline_styles: list[TwitterArticleInlineStyle] | None = Field(
        default=None,
        alias="inlineStyles",
        description="Formatting ranges within the block text.",
    )
    text: str | None = Field(
        default=None, description="Text content for a text-bearing block."
    )
    type_: str = Field(
        alias="type",
        description="Block type reported by X, such as unstyled, header-two, image, divider, blockquote, or list item. Populated whenever the provider has data for the entity.",
    )
    width: int | None = Field(
        default=None, description="Image width in pixels when supplied. Minimum: 0."
    )


class TwitterArticleEntitie(BaseModel):
    model_config = ConfigDict(extra="allow")

    key: int = Field(description="Upstream entity table key. Minimum: 0.")
    length: int = Field(description="Entity character length. Minimum: 0.")
    offset: int = Field(description="Zero-based character offset. Minimum: 0.")


class TwitterArticleInlineStyle(BaseModel):
    model_config = ConfigDict(extra="allow")

    length: int = Field(description="Formatted character length. Minimum: 0.")
    offset: int = Field(description="Zero-based character offset. Minimum: 0.")
    style: str = Field(description="Inline style name reported by X.")


class TwitterCommunityData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    creator_handle: str = Field(
        alias="creatorHandle",
        description="Handle of the account that created the community. Populated whenever the provider has data for the entity.",
    )
    description: str = Field(
        description="Community description text. Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Community identifier. Populated whenever the provider has data for the entity."
    )
    join_policy: str = Field(
        alias="joinPolicy",
        description='How members join, e.g. "open" or "restricted". Populated whenever the provider has data for the entity.',
    )
    member_count: int = Field(
        alias="memberCount", description="Number of members in the community."
    )
    name: str = Field(
        description="Community name. Populated whenever the provider has data for the entity."
    )
    nsfw: bool | None = Field(
        default=None, description="Whether the community is marked not-safe-for-work."
    )
    rules: list[TwitterCommunityRule] | None = Field(
        default=None, description="Rules the community publishes."
    )


class TwitterCommunityRule(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = Field(default=None, description="Name of the rule.")


class TwitterCommunityTweetsData(BaseModel):
    tweets: list[TwitterCommunityTweetsTweet] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TwitterCommunityTweetsTweet(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str = Field(
        alias="authorHandle",
        description="Populated whenever the provider has data for the entity.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that posted.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the posting account carries an X blue verification badge.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    favorite_count: int = Field(alias="favoriteCount")
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    lang: str | None = Field(
        default=None, description="Two-letter language code X detected for the post."
    )
    quote_count: int = Field(alias="quoteCount")
    reply_count: int = Field(alias="replyCount")
    retweet_count: int = Field(alias="retweetCount")
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    views: int | None = Field(default=None, description="View count of the post.")


class TwitterFollowersData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[TwitterFollowersItem] = Field(
        description="Follower records, normalized to a compact shape. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of followers, or null when there are no more. Pass it back as cursor to continue.",
    )


class TwitterFollowersItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="URL of the account's profile image (may be empty). Populated whenever the provider has data for the entity.",
    )
    bio: str | None = Field(
        default=None, description="The account's profile bio/description."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the account was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    followers: int = Field(description="How many followers this account has.")
    following: int | None = Field(
        default=None, description="How many accounts this account follows."
    )
    id: str | None = Field(
        default=None, description="Numeric X user id of the account, as a string."
    )
    location: str = Field(
        description="The account's self-reported location (may be empty)."
    )
    name: str = Field(
        description="The account's display name. Populated whenever the provider has data for the entity."
    )
    username: str = Field(
        description="The account's @ handle, without the @ prefix. Populated whenever the provider has data for the entity."
    )
    verified: bool = Field(description="Whether the account is verified.")


class TwitterFollowingData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[TwitterFollowingItem] = Field(
        description="Followed-account records, normalized to a compact shape. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of followed accounts, or null when there are no more. Pass it back as cursor to continue.",
    )


class TwitterFollowingItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="URL of the account's profile image (may be empty). Populated whenever the provider has data for the entity.",
    )
    bio: str = Field(description="The account's profile bio/description.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the account was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    followers: int = Field(description="How many followers this account has.")
    following: int = Field(description="How many accounts this account follows.")
    id: str | None = Field(
        default=None, description="Numeric X user id of the account, as a string."
    )
    location: str | None = Field(
        default=None, description="The account's self-reported location (may be empty)."
    )
    name: str = Field(
        description="The account's display name. Populated whenever the provider has data for the entity."
    )
    posts: int | None = Field(
        default=None, description="Number of posts the account has published."
    )
    username: str = Field(
        description="The account's @ handle, without the @ prefix. Populated whenever the provider has data for the entity."
    )


class TwitterProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    bio: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    cover_url: str | None = Field(
        default=None,
        alias="coverUrl",
        description="Profile banner image URL of the account.",
    )
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
    following: int
    handle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    id: str | None = Field(
        default=None, description="Numeric X user id of the account, as a string."
    )
    location: str | None = Field(
        default=None, description="Location text on the account's profile."
    )
    media_count: int | None = Field(
        default=None,
        alias="mediaCount",
        description="Number of media items the account has posted.",
    )
    pinned_post_ids: list[str] | None = Field(
        default=None,
        alias="pinnedPostIds",
        description="Ids of the posts pinned to the account's profile.",
    )
    private: bool | None = Field(
        default=None, description="Whether the account is protected (private)."
    )
    tweets: int
    verified: bool
    website: str


class TwitterRepliesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[TwitterRepliesItem] = Field(
        description="Reply records for the requested post. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of replies, or null when there are no more. Pass it back as cursor to continue.",
    )


class TwitterRepliesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Screen name / handle of the reply's author, without the @ prefix.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the reply's author. Empty when the upstream omits it.",
    )
    conversation_id: str | None = Field(
        default=None,
        alias="conversationId",
        description="Id of the conversation the reply belongs to, as a string.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(
        description="The reply's numeric tweet ID, as a string. Populated whenever the provider has data for the entity."
    )
    like_count: int | None = Field(
        default=None, alias="likeCount", description="Number of likes on this reply."
    )
    media: list[TwitterRepliesMedia] | None = Field(
        default=None,
        description="Photo, video, and GIF attachments on the post. Empty when the post has none.",
    )
    quote_count: int | None = Field(
        default=None,
        alias="quoteCount",
        description="Number of quote tweets of this reply.",
    )
    reply_count: int | None = Field(
        default=None, alias="replyCount", description="Number of replies to this reply."
    )
    repost_count: int | None = Field(
        default=None,
        alias="repostCount",
        description="Number of reposts/retweets of this reply.",
    )
    text: str = Field(
        description="The reply's text. Empty for media-only replies with no text."
    )
    url: str = Field(
        description="Canonical x.com URL of the reply, with tracking query params stripped. Populated whenever the provider has data for the entity."
    )
    view_count: int | None = Field(
        default=None,
        alias="viewCount",
        description="Number of views of this reply. Null when the source does not report it, as for posts older than X view counts.",
    )


class TwitterRepliesMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame. X media URLs on pbs.twimg.com are publicly fetchable without authentication; append ?name=orig for the full-resolution original."
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


class TwitterSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[TwitterSearchItem] = Field(
        description="Tweet records: text, author profile, timestamp, and engagement metrics (likes, retweets, replies, views). Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of search results, or null when there are no more. Pass it back as cursor to continue.",
    )


class TwitterSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="Follower count of the account that posted.",
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric X user id of the account that posted, as a string.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Avatar image URL of the account that posted.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_username: str | None = Field(
        default=None,
        alias="authorUsername",
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(default=None, alias="authorVerified")
    bookmark_count: int | None = Field(default=None, alias="bookmarkCount")
    conversation_id: str | None = Field(default=None, alias="conversationId")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    in_reply_to_id: str | None = Field(
        default=None,
        alias="inReplyToId",
        description="Id of the post this post directly replies to, as a string, or null when the post is not a reply.",
    )
    is_reply: bool | None = Field(default=None, alias="isReply")
    lang: str | None = None
    like_count: int | None = Field(default=None, alias="likeCount")
    media: list[TwitterSearchMedia] | None = Field(
        default=None,
        description="Photo, video, and GIF attachments on the post. Empty when the post has none.",
    )
    quote_count: int | None = Field(default=None, alias="quoteCount")
    reply_count: int | None = Field(default=None, alias="replyCount")
    retweet_count: int | None = Field(default=None, alias="retweetCount")
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    view_count: int | None = Field(
        default=None,
        alias="viewCount",
        description="Number of views. Null when the source does not report it, as for posts older than X view counts.",
    )


class TwitterSearchMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame. X media URLs on pbs.twimg.com are publicly fetchable without authentication; append ?name=orig for the full-resolution original."
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


class TwitterSearchCommunitiesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    communities: list[TwitterSearchCommunitiesCommunitie] = Field(
        description="Matching X (Twitter) communities. Search returns a summary record; pass url to twitter.community for the full detail, or to twitter.community_tweets for its posts. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of communities, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class TwitterSearchCommunitiesCommunitie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(
        description="Community identifier. Populated whenever the provider has data for the entity."
    )
    member_count: int = Field(
        alias="memberCount", description="Number of members in the community."
    )
    name: str = Field(
        description="Community name. Populated whenever the provider has data for the entity."
    )
    nsfw: bool = Field(
        description="Whether the community is flagged as not safe for work."
    )
    topic: str = Field(
        description="The community's primary topic label (may be empty)."
    )
    url: str = Field(
        description="Canonical URL of the community on X. Pass it to twitter.community or twitter.community_tweets. Populated whenever the provider has data for the entity."
    )


class TwitterSearchUsersData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of accounts, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    users: list[TwitterSearchUsersUser] = Field(
        description="Matching X (Twitter) accounts, normalized to a compact profile record. Populated whenever the provider has data for the entity."
    )


class TwitterSearchUsersUser(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="URL of the account's profile image. Populated whenever the provider has data for the entity.",
    )
    bio: str = Field(
        description="The account's profile bio/description (may be empty)."
    )
    can_dm: bool | None = Field(
        default=None,
        alias="canDm",
        description="Whether the account accepts direct messages; null when the serving source does not return it. Name it in requireFields to be served by a source that does.",
    )
    cover_url: str | None = Field(
        default=None,
        alias="coverUrl",
        description="Profile banner image URL of the account.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    followers: int = Field(description="How many followers this account has.")
    following: int = Field(description="How many accounts this account follows.")
    id: str = Field(
        description="The account's numeric X user id. Populated whenever the provider has data for the entity."
    )
    listed_count: int | None = Field(
        default=None,
        alias="listedCount",
        description="Number of public lists the account appears on; null when the serving source does not return it. Name it in requireFields to be served by a source that does.",
    )
    location: str | None = Field(
        description="The account's self-reported location (may be empty); null when the serving source does not return locations. Name it in requireFields to be served by a source that does."
    )
    name: str = Field(
        description="The account's display name. Populated whenever the provider has data for the entity."
    )
    posts: int = Field(description="How many posts this account has published.")
    profile_url: str = Field(
        alias="profileUrl",
        description="Canonical URL of the account's X profile. Populated whenever the provider has data for the entity.",
    )
    username: str = Field(
        description="The account's @ handle, without the @ prefix. Populated whenever the provider has data for the entity."
    )
    verified: bool = Field(
        description="Whether the account carries the blue verification check."
    )


class TwitterThreadData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    author: TwitterThreadAuthor
    complete: bool = Field(
        description="Whether the provider reached the end of the self-thread without hitting its internal cap."
    )
    conversation_id: str = Field(
        alias="conversationId",
        description="Conversation ID shared by the self-thread tweets. Populated whenever the provider has data for the entity.",
    )
    thread_length: int = Field(
        alias="threadLength",
        description="Number of tweets returned in the self-thread.",
    )
    tweets: list[TwitterThreadTweet] = Field(
        description="Ordered self-thread tweets. Replies from other users are excluded. Populated whenever the provider has data for the entity."
    )


class TwitterThreadAuthor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None, alias="avatarUrl", description="Avatar image URL of the author."
    )
    bio: str | None = Field(
        default=None, description="Bio text on the author's profile."
    )
    blue_verified: bool | None = Field(
        default=None,
        alias="blueVerified",
        description="Whether the author carries an X blue verification badge.",
    )
    cover_url: str | None = Field(
        default=None,
        alias="coverUrl",
        description="Profile banner image URL of the author.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the author's account was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    followers: int | None = Field(
        default=None, description="Follower count of the author."
    )
    following: int | None = Field(
        default=None, description="Number of accounts the author follows."
    )
    handle: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    location: str | None = Field(
        default=None, description="Location text on the author's profile."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None, description="Canonical X profile URL of the thread's author."
    )
    verified: bool | None = Field(
        default=None,
        description="Whether the author carries a legacy X verification badge.",
    )


class TwitterThreadTweet(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str = Field(
        alias="authorHandle",
        description="Populated whenever the provider has data for the entity.",
    )
    author_id: str = Field(
        alias="authorId",
        description="Populated whenever the provider has data for the entity.",
    )
    author_name: str = Field(
        alias="authorName",
        description="Populated whenever the provider has data for the entity.",
    )
    bookmark_count: int | None = Field(
        default=None, alias="bookmarkCount", description="Bookmark count of the post."
    )
    conversation_id: str = Field(alias="conversationId")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    in_reply_to_id: str | None = Field(alias="inReplyToId")
    is_reply: bool | None = Field(
        default=None,
        alias="isReply",
        description="Whether the post is a reply to another post.",
    )
    lang: str | None = Field(
        default=None, description="Two-letter language code X detected for the post."
    )
    like_count: int | None = Field(
        default=None, alias="likeCount", description="Like count of the post."
    )
    media: list[TwitterThreadMedia] | None = Field(
        default=None,
        description="Photo, video, and GIF attachments on the post. Empty when the post has none.",
    )
    quote_count: int | None = Field(
        default=None, alias="quoteCount", description="Quote count of the post."
    )
    reply_count: int | None = Field(
        default=None, alias="replyCount", description="Reply count of the post."
    )
    repost_count: int | None = Field(
        default=None, alias="repostCount", description="Repost count of the post."
    )
    source: str | None = Field(
        default=None,
        description='Client the post was sent from, e.g. "Twitter Web App".',
    )
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    view_count: int | None = Field(
        default=None, alias="viewCount", description="View count of the post."
    )


class TwitterThreadMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame. X media URLs on pbs.twimg.com are publicly fetchable without authentication; append ?name=orig for the full-resolution original."
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


class TwitterTrendsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    as_of_utc: float = Field(
        alias="asOfUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    items: list[TwitterTrendsItem] = Field(
        description="Current trends in X's own ranking order. Distinct ranks may carry the same trend name. Populated whenever the provider has data for the entity."
    )
    location: str = Field(
        description="Resolved X trend-location name. Populated whenever the provider has data for the entity."
    )
    location_id: str = Field(
        alias="locationId",
        description="Resolved Yahoo WOEID used by X, exposed as a stable location identifier. Populated whenever the provider has data for the entity.",
    )


class TwitterTrendsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    is_hashtag: bool | None = Field(
        default=None,
        alias="isHashtag",
        description="Whether the trend text is a hashtag.",
    )
    name: str = Field(
        description="Trend text displayed by X. Populated whenever the provider has data for the entity."
    )
    promoted: bool | None = Field(
        default=None, description="Whether X marks the trend as promoted."
    )
    query: str = Field(
        description="Search query corresponding to the trend. Populated whenever the provider has data for the entity."
    )
    rank: int = Field(
        description="One-based position in X's trend ranking. Populated whenever the provider has data for the entity. Minimum: 1."
    )
    url: str | None = Field(default=None, description="X search URL for the trend.")


class TwitterTweetData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Handle of the account that posted.",
    )
    author_id: str = Field(
        alias="authorId",
        description="Populated whenever the provider has data for the entity.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Avatar image URL of the account that posted.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that posted.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the posting account carries an X blue verification badge.",
    )
    bookmarks: int
    conversation_id: str | None = Field(
        default=None,
        alias="conversationId",
        description="Id of the conversation the post belongs to, as a string.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    in_reply_to_id: str | None = Field(
        default=None,
        alias="inReplyToId",
        description="Id of the post this post directly replies to, as a string, or null when the post is not a reply.",
    )
    lang: str | None = Field(
        default=None, description="Two-letter language code X detected for the post."
    )
    likes: int
    media: list[TwitterTweetMedia] | None = Field(
        default=None,
        description="Photo, video, and GIF attachments on the post. Empty when the post has none.",
    )
    quotes: int
    replies: int
    retweets: int
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    views: int | None = Field(
        description="View count, or null when X does not report one for this tweet. Distinct from 0, which means the tweet has no views."
    )


class TwitterTweetMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(
        default=None,
        description="Pixel height of the media item, when the lane reports it.",
    )
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame. X media URLs on pbs.twimg.com are publicly fetchable without authentication; append ?name=orig for the full-resolution original."
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


class TwitterTweetTranscriptData(BaseModel):
    model_config = ConfigDict(extra="allow")

    transcript: str


class TwitterUserPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next native Posts-tab page, or null when no more pages are available.",
    )
    tweets: list[TwitterUserPostsTweet] = Field(
        description="Posts in profile order. A pinned post may appear before otherwise reverse-chronological results. Populated whenever the provider has data for the entity."
    )


class TwitterUserPostsTweet(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Handle of the account that posted.",
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric X user id of the account that posted, as a string.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Avatar image URL of the account that posted.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that posted.",
    )
    bookmarks: int = Field(description="Number of bookmarks.")
    conversation_id: str | None = Field(
        default=None,
        alias="conversationId",
        description="Id of the conversation the post belongs to, as a string.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="The post's numeric tweet ID, represented as a string. Populated whenever the provider has data for the entity."
    )
    is_pinned: bool | None = Field(
        alias="isPinned",
        description="Whether X marks the post as pinned on the profile, or null when the serving source does not publish it.",
    )
    is_reply: bool | None = Field(
        default=None,
        alias="isReply",
        description="Whether X marks the record as a reply. Certified Posts-tab captures use this for self-thread continuations.",
    )
    lang: str | None = Field(
        default=None, description="Language code reported for the post, when available."
    )
    likes: int = Field(description="Number of likes.")
    media: list[TwitterUserPostsMedia] | None = Field(
        default=None,
        description="Photo, video, and GIF attachments on the post. Empty when the post has none.",
    )
    quotes: int | None = Field(default=None, description="Number of quote posts.")
    replies: int = Field(description="Number of replies.")
    retweets: int = Field(description="Number of reposts or retweets.")
    source: str | None = Field(
        default=None,
        description='Client the post was sent from, e.g. "Twitter Web App".',
    )
    text: str = Field(
        description="The post text. Empty for media-only posts. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical x.com URL of the post. Populated whenever the provider has data for the entity."
    )
    views: int = Field(description="Number of views.")


class TwitterUserPostsMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = None
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame. X media URLs on pbs.twimg.com are publicly fetchable without authentication; append ?name=orig for the full-resolution original."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL. Present only for video and gif items.",
    )
    width: int | None = None


class TwitterUserTweetsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page when the selected lane supports pagination, otherwise null.",
    )
    tweets: list[TwitterUserTweetsTweet] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TwitterUserTweetsTweet(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Handle of the account that posted.",
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric X user id of the account that posted, as a string.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Avatar image URL of the account that posted.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that posted.",
    )
    bookmarks: int
    conversation_id: str | None = Field(
        default=None,
        alias="conversationId",
        description="Id of the conversation the post belongs to, as a string.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    is_pinned: bool | None = Field(
        alias="isPinned",
        description="Whether X marks the post as pinned on the profile, or null when the serving source does not publish it.",
    )
    is_reply: bool | None = Field(default=None, alias="isReply")
    lang: str | None = None
    likes: int
    media: list[TwitterUserTweetsMedia] | None = Field(
        default=None,
        description="Photo, video, and GIF attachments on the post. Empty when the post has none.",
    )
    quotes: int | None = None
    replies: int
    retweets: int
    source: str | None = Field(
        default=None,
        description='Client the post was sent from, e.g. "Twitter Web App".',
    )
    text: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    views: int


class TwitterUserTweetsMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = None
    type_: str = Field(alias="type", description="One of photo, video, or gif.")
    url: str = Field(
        description="Image URL. For a video or GIF this is the poster/thumbnail frame. X media URLs on pbs.twimg.com are publicly fetchable without authentication; append ?name=orig for the full-resolution original."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video file URL. Present only for video and gif items.",
    )
    width: int | None = None


class TwitterNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def article(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterArticleInput],
    ) -> RunResult[TwitterArticleData]:
        """X / Twitter Article

        Get a public X long-form article from its wrapper post URL, including its
        author, engagement, cover image, and structured content blocks.

        Price: $0.00054 per request.

        Example:
            res = client.twitter.article(url="https://x.com/Decentralisedco/status/1905545699552375179")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.article", dict(input), options
        )
        return RunResult[TwitterArticleData].model_validate(raw)

    def community(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterCommunityInput],
    ) -> RunResult[TwitterCommunityData]:
        """Twitter Community

        Fetch a Twitter/X community's public details (name, description, member
        count, join policy) by URL.

        Price: $0.0001 per request.

        Example:
            res = client.twitter.community(url="https://x.com/i/communities/1926186499399139650")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.community", dict(input), options
        )
        return RunResult[TwitterCommunityData].model_validate(raw)

    def community_tweets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterCommunityTweetsInput],
    ) -> RunResult[TwitterCommunityTweetsData]:
        """Twitter Community Tweets

        List recent tweets posted in a Twitter/X community by URL.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.community_tweets(url="https://x.com/i/communities/1926186499399139650")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.community_tweets", dict(input), options
        )
        return RunResult[TwitterCommunityTweetsData].model_validate(raw)

    def followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowersInput],
    ) -> RunResult[TwitterFollowersData]:
        """X / Twitter Followers

        Fetch the follower list of any public X (Twitter) account by username with
        cursor pagination. Limit is a per-page maximum and a native page holds up to
        200 accounts; follow the response's nextCursor for more.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.followers(limit=200, username="nasa")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.followers", dict(input), options
        )
        return RunResult[TwitterFollowersData].model_validate(raw)

    def iter_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowersInput],
    ) -> Paginator[TwitterFollowersItem, TwitterFollowersData]:
        """Iterate X / Twitter Followers results, following pagination cursors.

        Yields validated `TwitterFollowersItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.followers",
            dict(input),
            "items",
            item_model=TwitterFollowersItem,
            data_model=TwitterFollowersData,
            bare=False,
            options=options,
        )

    def following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowingInput],
    ) -> RunResult[TwitterFollowingData]:
        """X / Twitter Following

        List the accounts a public X (Twitter) account follows by username with
        cursor pagination. Limit is a per-page maximum; follow the response's
        nextCursor for more.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.following(limit=200, username="nasa")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.following", dict(input), options
        )
        return RunResult[TwitterFollowingData].model_validate(raw)

    def iter_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowingInput],
    ) -> Paginator[TwitterFollowingItem, TwitterFollowingData]:
        """Iterate X / Twitter Following results, following pagination cursors.

        Yields validated `TwitterFollowingItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.following",
            dict(input),
            "items",
            item_model=TwitterFollowingItem,
            data_model=TwitterFollowingData,
            bare=False,
            options=options,
        )

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterProfileInput],
    ) -> RunResult[TwitterProfileData]:
        """Twitter Profile

        Fetch a Twitter/X account's public profile (followers, tweets, bio,
        verification) by handle.

        Price: $0.00022 per request.

        Example:
            res = client.twitter.profile(handle="nasa")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.profile", dict(input), options
        )
        return RunResult[TwitterProfileData].model_validate(raw)

    def replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterRepliesInput],
    ) -> RunResult[TwitterRepliesData]:
        """X / Twitter Post Replies

        Fetch the replies to any X (Twitter) post URL as structured records: author,
        text, and engagement. An empty result is valid and does not assert whether
        the target post exists.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.replies(url="https://x.com/jack/status/20")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.replies", dict(input), options
        )
        return RunResult[TwitterRepliesData].model_validate(raw)

    def iter_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterRepliesInput],
    ) -> Paginator[TwitterRepliesItem, TwitterRepliesData]:
        """Iterate X / Twitter Post Replies results, following pagination cursors.

        Yields validated `TwitterRepliesItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.replies",
            dict(input),
            "items",
            item_model=TwitterRepliesItem,
            data_model=TwitterRepliesData,
            bare=False,
            options=options,
        )

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchInput],
    ) -> RunResult[TwitterSearchData]:
        """X / Twitter Search

        Search X (Twitter) with full advanced-search syntax (operators like from:,
        since:, until:, min_faves: work inline in the query) and get structured
        tweets with text, author, engagement, and cursor pagination. Limit is a
        per-page maximum; native pages contain approximately 20 tweets unless
        requireSinglePage selects a bulk lane.

        Price: $0.00054 per request.

        Example:
            res = client.twitter.search(query="openai")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.search", dict(input), options
        )
        return RunResult[TwitterSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchInput],
    ) -> Paginator[TwitterSearchItem, TwitterSearchData]:
        """Iterate X / Twitter Search results, following pagination cursors.

        Yields validated `TwitterSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.search",
            dict(input),
            "items",
            item_model=TwitterSearchItem,
            data_model=TwitterSearchData,
            bare=False,
            options=options,
        )

    def search_communities(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchCommunitiesInput],
    ) -> RunResult[TwitterSearchCommunitiesData]:
        """X / Twitter Community Search

        Search X (Twitter) communities by keyword and get their id, name, topic, and
        member count with cursor pagination. This is how you find a community URL to
        pass to twitter.community or twitter.community_tweets.

        Price: $0.0001 per request plus $0.0001 per result (maximum $0.0011).

        Example:
            res = client.twitter.search_communities(query="artificial intelligence")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.search_communities", dict(input), options
        )
        return RunResult[TwitterSearchCommunitiesData].model_validate(raw)

    def iter_search_communities(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchCommunitiesInput],
    ) -> Paginator[TwitterSearchCommunitiesCommunitie, TwitterSearchCommunitiesData]:
        """Iterate X / Twitter Community Search results, following pagination cursors.

        Yields validated `TwitterSearchCommunitiesCommunitie` items from the `communities` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.search_communities",
            dict(input),
            "communities",
            item_model=TwitterSearchCommunitiesCommunitie,
            data_model=TwitterSearchCommunitiesData,
            bare=False,
            options=options,
        )

    def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchUsersInput],
    ) -> RunResult[TwitterSearchUsersData]:
        """X / Twitter User Search

        Search X (Twitter) accounts by keyword - the People tab of X search. Matches
        handles, display names, and profile bios, and returns normalized profile
        records with follower, following, and post counts plus cursor pagination.
        Use twitter.search for posts.

        Price: $0.00054 per request.

        Example:
            res = client.twitter.search_users(query="ai agents")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.search_users", dict(input), options
        )
        return RunResult[TwitterSearchUsersData].model_validate(raw)

    def iter_search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchUsersInput],
    ) -> Paginator[TwitterSearchUsersUser, TwitterSearchUsersData]:
        """Iterate X / Twitter User Search results, following pagination cursors.

        Yields validated `TwitterSearchUsersUser` items from the `users` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.search_users",
            dict(input),
            "users",
            item_model=TwitterSearchUsersUser,
            data_model=TwitterSearchUsersData,
            bare=False,
            options=options,
        )

    def thread(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterThreadInput],
    ) -> RunResult[TwitterThreadData]:
        """X / Twitter Tweet Thread

        Resolve the linear self-thread containing an X (Twitter) post, from its root
        through the author's linked continuations. This excludes replies from other
        users.

        Price: $0.00269 per request.

        Example:
            res = client.twitter.thread(url="https://x.com/SpaceX/status/1732824684683784516")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.thread", dict(input), options
        )
        return RunResult[TwitterThreadData].model_validate(raw)

    def trends(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterTrendsInput],
    ) -> RunResult[TwitterTrendsData]:
        """X / Twitter Trends

        Get current X (Twitter) trends for worldwide, a country, or a city in X
        ranking order, including the resolved location.

        Price: $0.0001 per request.

        Example:
            res = client.twitter.trends(limit=10, location="US")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.trends", dict(input), options
        )
        return RunResult[TwitterTrendsData].model_validate(raw)

    def tweet(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterTweetInput],
    ) -> RunResult[TwitterTweetData]:
        """Twitter Tweet

        Fetch a single Twitter/X tweet by URL with its full text and engagement
        counts (likes, retweets, replies, quotes, bookmarks, views).

        Price: $0.00022 per request.

        Example:
            res = client.twitter.tweet(url="https://x.com/SpaceX/status/1732824684683784516")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.tweet", dict(input), options
        )
        return RunResult[TwitterTweetData].model_validate(raw)

    def tweet_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterTweetTranscriptInput],
    ) -> RunResult[TwitterTweetTranscriptData]:
        """Twitter Tweet Transcript

        Extract the spoken transcript from a Twitter/X video tweet by URL.

        Price: $0.0012 per request.

        Example:
            res = client.twitter.tweet_transcript(url="https://x.com/TheoVon/status/1916982720317821050")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.tweet_transcript", dict(input), options
        )
        return RunResult[TwitterTweetTranscriptData].model_validate(raw)

    def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserPostsInput],
    ) -> RunResult[TwitterUserPostsData]:
        """X / Twitter User Posts

        Get an X (Twitter) account's profile Posts-tab timeline by handle. Results
        follow profile order: a pinned post may appear first, followed by otherwise
        reverse-chronological authored posts, reposts, quotes, and self-thread
        continuations.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.user_posts(handle="levelsio")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.user_posts", dict(input), options
        )
        return RunResult[TwitterUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserPostsInput],
    ) -> Paginator[TwitterUserPostsTweet, TwitterUserPostsData]:
        """Iterate X / Twitter User Posts results, following pagination cursors.

        Yields validated `TwitterUserPostsTweet` items from the `tweets` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.user_posts",
            dict(input),
            "tweets",
            item_model=TwitterUserPostsTweet,
            data_model=TwitterUserPostsData,
            bare=False,
            options=options,
        )

    def user_tweets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserTweetsInput],
    ) -> RunResult[TwitterUserTweetsData]:
        """X / Twitter User Tweets and Replies

        Get up to the requested limit of tweets and replies authored by an X
        (Twitter) account, with engagement, views, language, and cursor pagination
        where available.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.user_tweets(handle="levelsio", limit=20)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.user_tweets", dict(input), options
        )
        return RunResult[TwitterUserTweetsData].model_validate(raw)

    def iter_user_tweets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserTweetsInput],
    ) -> Paginator[TwitterUserTweetsTweet, TwitterUserTweetsData]:
        """Iterate X / Twitter User Tweets and Replies results, following pagination cursors.

        Yields validated `TwitterUserTweetsTweet` items from the `tweets` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "twitter.user_tweets",
            dict(input),
            "tweets",
            item_model=TwitterUserTweetsTweet,
            data_model=TwitterUserTweetsData,
            bare=False,
            options=options,
        )


class AsyncTwitterNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def article(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterArticleInput],
    ) -> RunResult[TwitterArticleData]:
        """X / Twitter Article

        Get a public X long-form article from its wrapper post URL, including its
        author, engagement, cover image, and structured content blocks.

        Price: $0.00054 per request.

        Example:
            res = client.twitter.article(url="https://x.com/Decentralisedco/status/1905545699552375179")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.article", dict(input), options
        )
        return RunResult[TwitterArticleData].model_validate(raw)

    async def community(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterCommunityInput],
    ) -> RunResult[TwitterCommunityData]:
        """Twitter Community

        Fetch a Twitter/X community's public details (name, description, member
        count, join policy) by URL.

        Price: $0.0001 per request.

        Example:
            res = client.twitter.community(url="https://x.com/i/communities/1926186499399139650")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.community", dict(input), options
        )
        return RunResult[TwitterCommunityData].model_validate(raw)

    async def community_tweets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterCommunityTweetsInput],
    ) -> RunResult[TwitterCommunityTweetsData]:
        """Twitter Community Tweets

        List recent tweets posted in a Twitter/X community by URL.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.community_tweets(url="https://x.com/i/communities/1926186499399139650")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.community_tweets", dict(input), options
        )
        return RunResult[TwitterCommunityTweetsData].model_validate(raw)

    async def followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowersInput],
    ) -> RunResult[TwitterFollowersData]:
        """X / Twitter Followers

        Fetch the follower list of any public X (Twitter) account by username with
        cursor pagination. Limit is a per-page maximum and a native page holds up to
        200 accounts; follow the response's nextCursor for more.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.followers(limit=200, username="nasa")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.followers", dict(input), options
        )
        return RunResult[TwitterFollowersData].model_validate(raw)

    def iter_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowersInput],
    ) -> AsyncPaginator[TwitterFollowersItem, TwitterFollowersData]:
        """Iterate X / Twitter Followers results, following pagination cursors.

        Yields validated `TwitterFollowersItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.followers",
            dict(input),
            "items",
            item_model=TwitterFollowersItem,
            data_model=TwitterFollowersData,
            bare=False,
            options=options,
        )

    async def following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowingInput],
    ) -> RunResult[TwitterFollowingData]:
        """X / Twitter Following

        List the accounts a public X (Twitter) account follows by username with
        cursor pagination. Limit is a per-page maximum; follow the response's
        nextCursor for more.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.following(limit=200, username="nasa")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.following", dict(input), options
        )
        return RunResult[TwitterFollowingData].model_validate(raw)

    def iter_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterFollowingInput],
    ) -> AsyncPaginator[TwitterFollowingItem, TwitterFollowingData]:
        """Iterate X / Twitter Following results, following pagination cursors.

        Yields validated `TwitterFollowingItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.following",
            dict(input),
            "items",
            item_model=TwitterFollowingItem,
            data_model=TwitterFollowingData,
            bare=False,
            options=options,
        )

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterProfileInput],
    ) -> RunResult[TwitterProfileData]:
        """Twitter Profile

        Fetch a Twitter/X account's public profile (followers, tweets, bio,
        verification) by handle.

        Price: $0.00022 per request.

        Example:
            res = client.twitter.profile(handle="nasa")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.profile", dict(input), options
        )
        return RunResult[TwitterProfileData].model_validate(raw)

    async def replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterRepliesInput],
    ) -> RunResult[TwitterRepliesData]:
        """X / Twitter Post Replies

        Fetch the replies to any X (Twitter) post URL as structured records: author,
        text, and engagement. An empty result is valid and does not assert whether
        the target post exists.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.replies(url="https://x.com/jack/status/20")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.replies", dict(input), options
        )
        return RunResult[TwitterRepliesData].model_validate(raw)

    def iter_replies(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterRepliesInput],
    ) -> AsyncPaginator[TwitterRepliesItem, TwitterRepliesData]:
        """Iterate X / Twitter Post Replies results, following pagination cursors.

        Yields validated `TwitterRepliesItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.replies",
            dict(input),
            "items",
            item_model=TwitterRepliesItem,
            data_model=TwitterRepliesData,
            bare=False,
            options=options,
        )

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchInput],
    ) -> RunResult[TwitterSearchData]:
        """X / Twitter Search

        Search X (Twitter) with full advanced-search syntax (operators like from:,
        since:, until:, min_faves: work inline in the query) and get structured
        tweets with text, author, engagement, and cursor pagination. Limit is a
        per-page maximum; native pages contain approximately 20 tweets unless
        requireSinglePage selects a bulk lane.

        Price: $0.00054 per request.

        Example:
            res = client.twitter.search(query="openai")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.search", dict(input), options
        )
        return RunResult[TwitterSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchInput],
    ) -> AsyncPaginator[TwitterSearchItem, TwitterSearchData]:
        """Iterate X / Twitter Search results, following pagination cursors.

        Yields validated `TwitterSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.search",
            dict(input),
            "items",
            item_model=TwitterSearchItem,
            data_model=TwitterSearchData,
            bare=False,
            options=options,
        )

    async def search_communities(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchCommunitiesInput],
    ) -> RunResult[TwitterSearchCommunitiesData]:
        """X / Twitter Community Search

        Search X (Twitter) communities by keyword and get their id, name, topic, and
        member count with cursor pagination. This is how you find a community URL to
        pass to twitter.community or twitter.community_tweets.

        Price: $0.0001 per request plus $0.0001 per result (maximum $0.0011).

        Example:
            res = client.twitter.search_communities(query="artificial intelligence")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.search_communities", dict(input), options
        )
        return RunResult[TwitterSearchCommunitiesData].model_validate(raw)

    def iter_search_communities(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchCommunitiesInput],
    ) -> AsyncPaginator[
        TwitterSearchCommunitiesCommunitie, TwitterSearchCommunitiesData
    ]:
        """Iterate X / Twitter Community Search results, following pagination cursors.

        Yields validated `TwitterSearchCommunitiesCommunitie` items from the `communities` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.search_communities",
            dict(input),
            "communities",
            item_model=TwitterSearchCommunitiesCommunitie,
            data_model=TwitterSearchCommunitiesData,
            bare=False,
            options=options,
        )

    async def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchUsersInput],
    ) -> RunResult[TwitterSearchUsersData]:
        """X / Twitter User Search

        Search X (Twitter) accounts by keyword - the People tab of X search. Matches
        handles, display names, and profile bios, and returns normalized profile
        records with follower, following, and post counts plus cursor pagination.
        Use twitter.search for posts.

        Price: $0.00054 per request.

        Example:
            res = client.twitter.search_users(query="ai agents")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.search_users", dict(input), options
        )
        return RunResult[TwitterSearchUsersData].model_validate(raw)

    def iter_search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterSearchUsersInput],
    ) -> AsyncPaginator[TwitterSearchUsersUser, TwitterSearchUsersData]:
        """Iterate X / Twitter User Search results, following pagination cursors.

        Yields validated `TwitterSearchUsersUser` items from the `users` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.search_users",
            dict(input),
            "users",
            item_model=TwitterSearchUsersUser,
            data_model=TwitterSearchUsersData,
            bare=False,
            options=options,
        )

    async def thread(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterThreadInput],
    ) -> RunResult[TwitterThreadData]:
        """X / Twitter Tweet Thread

        Resolve the linear self-thread containing an X (Twitter) post, from its root
        through the author's linked continuations. This excludes replies from other
        users.

        Price: $0.00269 per request.

        Example:
            res = client.twitter.thread(url="https://x.com/SpaceX/status/1732824684683784516")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.thread", dict(input), options
        )
        return RunResult[TwitterThreadData].model_validate(raw)

    async def trends(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterTrendsInput],
    ) -> RunResult[TwitterTrendsData]:
        """X / Twitter Trends

        Get current X (Twitter) trends for worldwide, a country, or a city in X
        ranking order, including the resolved location.

        Price: $0.0001 per request.

        Example:
            res = client.twitter.trends(limit=10, location="US")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.trends", dict(input), options
        )
        return RunResult[TwitterTrendsData].model_validate(raw)

    async def tweet(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterTweetInput],
    ) -> RunResult[TwitterTweetData]:
        """Twitter Tweet

        Fetch a single Twitter/X tweet by URL with its full text and engagement
        counts (likes, retweets, replies, quotes, bookmarks, views).

        Price: $0.00022 per request.

        Example:
            res = client.twitter.tweet(url="https://x.com/SpaceX/status/1732824684683784516")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.tweet", dict(input), options
        )
        return RunResult[TwitterTweetData].model_validate(raw)

    async def tweet_transcript(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterTweetTranscriptInput],
    ) -> RunResult[TwitterTweetTranscriptData]:
        """Twitter Tweet Transcript

        Extract the spoken transcript from a Twitter/X video tweet by URL.

        Price: $0.0012 per request.

        Example:
            res = client.twitter.tweet_transcript(url="https://x.com/TheoVon/status/1916982720317821050")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.tweet_transcript", dict(input), options
        )
        return RunResult[TwitterTweetTranscriptData].model_validate(raw)

    async def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserPostsInput],
    ) -> RunResult[TwitterUserPostsData]:
        """X / Twitter User Posts

        Get an X (Twitter) account's profile Posts-tab timeline by handle. Results
        follow profile order: a pinned post may appear first, followed by otherwise
        reverse-chronological authored posts, reposts, quotes, and self-thread
        continuations.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.user_posts(handle="levelsio")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.user_posts", dict(input), options
        )
        return RunResult[TwitterUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserPostsInput],
    ) -> AsyncPaginator[TwitterUserPostsTweet, TwitterUserPostsData]:
        """Iterate X / Twitter User Posts results, following pagination cursors.

        Yields validated `TwitterUserPostsTweet` items from the `tweets` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.user_posts",
            dict(input),
            "tweets",
            item_model=TwitterUserPostsTweet,
            data_model=TwitterUserPostsData,
            bare=False,
            options=options,
        )

    async def user_tweets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserTweetsInput],
    ) -> RunResult[TwitterUserTweetsData]:
        """X / Twitter User Tweets and Replies

        Get up to the requested limit of tweets and replies authored by an X
        (Twitter) account, with engagement, views, language, and cursor pagination
        where available.

        Price: $0.00045 per request.

        Example:
            res = client.twitter.user_tweets(handle="levelsio", limit=20)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "twitter.user_tweets", dict(input), options
        )
        return RunResult[TwitterUserTweetsData].model_validate(raw)

    def iter_user_tweets(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TwitterUserTweetsInput],
    ) -> AsyncPaginator[TwitterUserTweetsTweet, TwitterUserTweetsData]:
        """Iterate X / Twitter User Tweets and Replies results, following pagination cursors.

        Yields validated `TwitterUserTweetsTweet` items from the `tweets` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "twitter.user_tweets",
            dict(input),
            "tweets",
            item_model=TwitterUserTweetsTweet,
            data_model=TwitterUserTweetsData,
            bare=False,
            options=options,
        )
