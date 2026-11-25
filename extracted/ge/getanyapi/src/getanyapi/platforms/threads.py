# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the threads platform."""

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


class ThreadsPostInput(TypedDict, total=False):
    """Input for Threads Post."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The full URL of the Threads post to fetch (e.g. https://www.threads.com/@zuck/post/C8yKXdRxKqK)."""


class ThreadsProfileInput(TypedDict, total=False):
    """Input for Threads Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    username: Required[str]
    """The Threads username to look up, without the @ prefix (e.g. zuck)."""


class ThreadsSearchInput(TypedDict, total=False):
    """Input for Threads Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    endDate: NotRequired[str]
    """Only return posts published on or before this date, format YYYY-MM-DD (e.g. 2026-08-07). Threads pages backwards in time from here, so narrowing this is how you walk older results."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword or #hashtag to search public Threads posts for (e.g. Widgetable). A #hashtag can return different posts than the plain word, so if a tag returns nothing, try the word without #. Single words and brand names return the most; quotes around the whole query are removed, since quoted searches return nothing. Search a brand or topic rather than a URL - a query that is only a domain is searched by its name (wander.com is searched as wander)."""
    requireFields: NotRequired[list[Literal["nextCursor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Only return posts published on or after this date, format YYYY-MM-DD (e.g. 2026-08-01). Without dates, results lean toward popular posts of any age, so set startDate (e.g. a week ago) to get recent posts; there is no sort option."""


class ThreadsSearchUsersInput(TypedDict, total=False):
    """Input for Threads User Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The name or username to search Threads users for."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ThreadsUserPostsInput(TypedDict, total=False):
    """Input for Threads User Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    handle: Required[str]
    """The Threads username to list posts for, without the @ prefix."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["nextCursor"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `nextCursor`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ThreadsPostData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str = Field(description="Threads post shortcode.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    full_name: str = Field(
        alias="fullName",
        description="Display name of the author. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    is_verified: bool | None = Field(
        default=None,
        alias="isVerified",
        description="True when the author's account carries a verified badge.",
    )
    like_count: int = Field(
        alias="likeCount", description="Number of likes on the post."
    )
    profile_pic_url: str | None = Field(
        default=None,
        alias="profilePicUrl",
        description="Profile picture URL of the author.",
    )
    quote_count: int | None = Field(
        alias="quoteCount",
        description="Number of quote posts. Null when the source does not report it.",
    )
    reply_count: int | None = Field(
        alias="replyCount",
        description="Number of replies to the post. Null when the source does not report it.",
    )
    repost_count: int | None = Field(
        alias="repostCount",
        description="Number of reposts of the post. Null when the source does not report it.",
    )
    text: str = Field(
        description="Post text content. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(default=None, description="Canonical URL of the post.")
    username: str = Field(
        description="Username of the author. Populated whenever the provider has data for the entity."
    )


class ThreadsProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    biography: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    follower_count: int = Field(alias="followerCount")
    full_name: str = Field(
        alias="fullName",
        description="Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    is_private: bool = Field(alias="isPrivate")
    is_verified: bool = Field(alias="isVerified")
    profile_pic_url: str = Field(
        alias="profilePicUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    username: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class ThreadsSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when this source has no more. Pass it back as cursor to continue.",
    )
    posts: list[ThreadsSearchPost] = Field(
        description="Matching public post records: text, author, engagement counts, timestamp, and URL. Without date filters, results tend to favor popular posts of any age. Use startDate or endDate to narrow the results; neither guarantees newest-first order. Populated whenever the provider has data for the entity."
    )


class ThreadsSearchPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str = Field(description="Threads post shortcode.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    full_name: str = Field(
        alias="fullName",
        description="Display name of the author. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    is_verified: bool | None = Field(
        default=None,
        alias="isVerified",
        description="True when the author's account carries a verified badge.",
    )
    like_count: int = Field(
        alias="likeCount", description="Number of likes on the post."
    )
    profile_pic_url: str | None = Field(
        default=None,
        alias="profilePicUrl",
        description="Profile picture URL of the author.",
    )
    quote_count: int | None = Field(
        default=None, alias="quoteCount", description="Number of quote posts."
    )
    reply_count: int = Field(
        alias="replyCount", description="Number of replies to the post."
    )
    repost_count: int = Field(
        alias="repostCount", description="Number of reposts of the post."
    )
    text: str = Field(
        description="Post text content. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )
    username: str = Field(
        description="Username of the author. Populated whenever the provider has data for the entity."
    )


class ThreadsSearchUsersData(BaseModel):
    users: list[ThreadsSearchUsersUser] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class ThreadsSearchUsersUser(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    full_name: str = Field(
        alias="fullName",
        description="Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    is_verified: bool = Field(alias="isVerified")
    profile_pic_url: str = Field(
        alias="profilePicUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    username: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class ThreadsUserPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when this source has no more. Pass it back as cursor to continue.",
    )
    posts: list[ThreadsUserPostsPost] = Field(
        description="One page of recent public posts (typically 10 to 15). An older pinned post may appear first. Populated whenever the provider has data for the entity."
    )


class ThreadsUserPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str = Field(description="Threads post shortcode.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    is_verified: bool | None = Field(
        default=None,
        alias="isVerified",
        description="True when the author's account carries a verified badge.",
    )
    like_count: int = Field(
        alias="likeCount", description="Number of likes on the post."
    )
    profile_pic_url: str | None = Field(
        default=None,
        alias="profilePicUrl",
        description="Profile picture URL of the author.",
    )
    quote_count: int = Field(alias="quoteCount", description="Number of quote posts.")
    reply_count: int = Field(
        alias="replyCount", description="Number of replies to the post."
    )
    repost_count: int = Field(
        alias="repostCount", description="Number of reposts of the post."
    )
    text: str = Field(
        description="Post text content. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )
    username: str = Field(
        description="Username of the author. Populated whenever the provider has data for the entity."
    )


class ThreadsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsPostInput],
    ) -> RunResult[ThreadsPostData]:
        """Threads Post

        Fetch a single Threads post by URL: text, author, engagement counts, and
        timestamp.

        Price: $0.0011 per request.

        Example:
            res = client.threads.post(url="https://www.threads.com/@aaronparnas/post/DZxPYVFkYSq")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.post", dict(input), options
        )
        return RunResult[ThreadsPostData].model_validate(raw)

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsProfileInput],
    ) -> RunResult[ThreadsProfileData]:
        """Threads Profile

        Fetch a Threads user's public profile (bio, follower count, verification,
        profile picture) by username.

        Price: $0.0011 per request.

        Example:
            res = client.threads.profile(username="zuck")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.profile", dict(input), options
        )
        return RunResult[ThreadsProfileData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsSearchInput],
    ) -> RunResult[ThreadsSearchData]:
        """Threads Search

        Search public Threads posts by keyword or hashtag and get normalized post
        records: text, author, and engagement.

        Price: $0.0012 per request.

        Example:
            res = client.threads.search(query="trump")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.search", dict(input), options
        )
        return RunResult[ThreadsSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsSearchInput],
    ) -> Paginator[ThreadsSearchPost, ThreadsSearchData]:
        """Iterate Threads Search results, following pagination cursors.

        Yields validated `ThreadsSearchPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "threads.search",
            dict(input),
            "posts",
            item_model=ThreadsSearchPost,
            data_model=ThreadsSearchData,
            bare=False,
            options=options,
        )

    def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsSearchUsersInput],
    ) -> RunResult[ThreadsSearchUsersData]:
        """Threads User Search

        Search Threads users by name or username and get normalized profile records:
        username, full name, verification, and picture.

        Price: $0.0012 per request.

        Example:
            res = client.threads.search_users(query="shams")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.search_users", dict(input), options
        )
        return RunResult[ThreadsSearchUsersData].model_validate(raw)

    def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsUserPostsInput],
    ) -> RunResult[ThreadsUserPostsData]:
        """Threads User Posts

        List a Threads user's recent public posts by username, one page per call
        (typically 10 to 15): text, engagement counts, and post URLs. Pass
        nextCursor back as cursor for older posts when it is not null. There is no
        date filter, and an older pinned post may appear first.

        Price: $0.0012 per request.

        Example:
            res = client.threads.user_posts(handle="trendspider")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.user_posts", dict(input), options
        )
        return RunResult[ThreadsUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsUserPostsInput],
    ) -> Paginator[ThreadsUserPostsPost, ThreadsUserPostsData]:
        """Iterate Threads User Posts results, following pagination cursors.

        Yields validated `ThreadsUserPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "threads.user_posts",
            dict(input),
            "posts",
            item_model=ThreadsUserPostsPost,
            data_model=ThreadsUserPostsData,
            bare=False,
            options=options,
        )


class AsyncThreadsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsPostInput],
    ) -> RunResult[ThreadsPostData]:
        """Threads Post

        Fetch a single Threads post by URL: text, author, engagement counts, and
        timestamp.

        Price: $0.0011 per request.

        Example:
            res = client.threads.post(url="https://www.threads.com/@aaronparnas/post/DZxPYVFkYSq")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.post", dict(input), options
        )
        return RunResult[ThreadsPostData].model_validate(raw)

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsProfileInput],
    ) -> RunResult[ThreadsProfileData]:
        """Threads Profile

        Fetch a Threads user's public profile (bio, follower count, verification,
        profile picture) by username.

        Price: $0.0011 per request.

        Example:
            res = client.threads.profile(username="zuck")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.profile", dict(input), options
        )
        return RunResult[ThreadsProfileData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsSearchInput],
    ) -> RunResult[ThreadsSearchData]:
        """Threads Search

        Search public Threads posts by keyword or hashtag and get normalized post
        records: text, author, and engagement.

        Price: $0.0012 per request.

        Example:
            res = client.threads.search(query="trump")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.search", dict(input), options
        )
        return RunResult[ThreadsSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsSearchInput],
    ) -> AsyncPaginator[ThreadsSearchPost, ThreadsSearchData]:
        """Iterate Threads Search results, following pagination cursors.

        Yields validated `ThreadsSearchPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "threads.search",
            dict(input),
            "posts",
            item_model=ThreadsSearchPost,
            data_model=ThreadsSearchData,
            bare=False,
            options=options,
        )

    async def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsSearchUsersInput],
    ) -> RunResult[ThreadsSearchUsersData]:
        """Threads User Search

        Search Threads users by name or username and get normalized profile records:
        username, full name, verification, and picture.

        Price: $0.0012 per request.

        Example:
            res = client.threads.search_users(query="shams")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.search_users", dict(input), options
        )
        return RunResult[ThreadsSearchUsersData].model_validate(raw)

    async def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsUserPostsInput],
    ) -> RunResult[ThreadsUserPostsData]:
        """Threads User Posts

        List a Threads user's recent public posts by username, one page per call
        (typically 10 to 15): text, engagement counts, and post URLs. Pass
        nextCursor back as cursor for older posts when it is not null. There is no
        date filter, and an older pinned post may appear first.

        Price: $0.0012 per request.

        Example:
            res = client.threads.user_posts(handle="trendspider")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "threads.user_posts", dict(input), options
        )
        return RunResult[ThreadsUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ThreadsUserPostsInput],
    ) -> AsyncPaginator[ThreadsUserPostsPost, ThreadsUserPostsData]:
        """Iterate Threads User Posts results, following pagination cursors.

        Yields validated `ThreadsUserPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "threads.user_posts",
            dict(input),
            "posts",
            item_model=ThreadsUserPostsPost,
            data_model=ThreadsUserPostsData,
            bare=False,
            options=options,
        )
