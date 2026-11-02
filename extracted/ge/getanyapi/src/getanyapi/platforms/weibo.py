# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the weibo platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

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


class WeiboHotSearchInput(TypedDict, total=False):
    """Input for Weibo Hot Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class WeiboPostInput(TypedDict, total=False):
    """Input for Weibo Post."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeLongText: NotRequired[str]
    """Whether to include the full text of long posts. Default: true."""
    postId: Required[str]
    """Weibo post identifier."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class WeiboPostCommentsInput(TypedDict, total=False):
    """Input for Weibo Post Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor returned as nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Requested comment count. Default: 10."""
    postId: Required[str]
    """Weibo post identifier."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class WeiboProfileInput(TypedDict, total=False):
    """Input for Weibo Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    userId: Required[str]
    """Weibo user identifier."""


class WeiboSearchInput(TypedDict, total=False):
    """Input for Weibo Advanced Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeType: NotRequired[str]
    """Media filter, such as all, pic, video, music, or link."""
    page: NotRequired[int]
    """Page number starting at 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword."""
    searchType: NotRequired[str]
    """Search type, such as all, hot, original, verified, media, or viewpoint."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeScope: NotRequired[str]
    """Custom time range in the API's custom:start:end format."""


class WeiboUserPostsInput(TypedDict, total=False):
    """Input for Weibo User Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination identifier returned as nextCursor."""
    feature: NotRequired[int]
    """Response detail feature: 0 basic, 1 extended, 2 image-oriented, or 3 video-oriented. Default: 0."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """Page number starting at 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    userId: Required[str]
    """Weibo user identifier."""


class WeiboHotSearchData(BaseModel):
    topics: list[WeiboHotSearchTopic] = Field(
        description="Ranked hot-search topics. Populated whenever the provider has data for the entity."
    )
    total: int = Field(description="Total topics.")


class WeiboHotSearchTopic(BaseModel):
    model_config = ConfigDict(extra="allow")

    heat: str | None = Field(default=None, description="Topic popularity value.")
    keyword: str = Field(
        description="Hot-search keyword. Populated whenever the provider has data for the entity."
    )
    pinned: bool | None = Field(
        default=None, description="Whether the topic is pinned."
    )
    rank: int = Field(
        description="Ranking position; zero may indicate pinned content. Populated whenever the provider has data for the entity."
    )
    tag: str | None = Field(default=None, description="Hot-search label.")


class WeiboPostData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author avatar URL."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical URL of the author's Weibo profile.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author user identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author is verified.",
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    image_count: int | None = Field(
        default=None, alias="imageCount", description="Attached image count."
    )
    likes: int | None = Field(default=None, description="Like count.")
    region: str | None = Field(
        default=None, description="Region label reported by Weibo."
    )
    reposts: int | None = Field(default=None, description="Repost count.")
    short_id: str | None = Field(
        default=None,
        alias="shortId",
        description="Short Weibo post identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    text: str | None = Field(
        default=None,
        description="Plain post text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class WeiboPostCommentsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    comments: list[WeiboPostCommentsComment] = Field(
        description="Normalized first-level comments. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of comments, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total: int = Field(description="Total comments reported by Weibo.")


class WeiboPostCommentsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Comment author avatar URL."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Comment author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical URL of the author's Weibo profile.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Comment author user identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the comment author is verified.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Comment identifier. Populated whenever the provider has data for the entity."
    )
    image_count: int | None = Field(
        default=None,
        alias="imageCount",
        description="Number of images attached to the comment.",
    )
    likes: int | None = Field(default=None, description="Like count.")
    replies: int | None = Field(
        default=None, description="Number of replies to the comment."
    )
    text: str | None = Field(
        default=None,
        description="Plain comment text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class WeiboProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bio: str | None = Field(default=None, description="Profile biography.")
    custom_name: str | None = Field(
        default=None,
        alias="customName",
        description="Custom Weibo username when configured.",
    )
    external_url: str | None = Field(
        default=None, alias="externalUrl", description="External profile URL."
    )
    followers: int | None = Field(default=None, description="Follower count.")
    following: int | None = Field(default=None, description="Following count.")
    gender: str | None = Field(
        default=None, description="Gender code reported by Weibo."
    )
    image: str | None = Field(
        default=None,
        description="Profile image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    location: str | None = Field(default=None, description="Profile location.")
    name: str | None = Field(
        default=None,
        description="Display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    posts: int | None = Field(default=None, description="Published post count.")
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical URL of the Weibo profile.",
    )
    user_id: str = Field(
        alias="userId",
        description="User identifier. Populated whenever the provider has data for the entity.",
    )
    verified: bool | None = Field(
        default=None, description="Whether the account is verified."
    )
    verified_reason: str | None = Field(
        default=None, alias="verifiedReason", description="Verification reason."
    )


class WeiboSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool = Field(
        alias="hasMore", description="Whether another result page is available."
    )
    posts: list[WeiboSearchPost] = Field(
        description="Normalized Weibo search results. Populated whenever the provider has data for the entity."
    )
    result_count: int = Field(
        alias="resultCount", description="Result count reported for this page."
    )


class WeiboSearchPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author avatar URL."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical URL of the author's Weibo profile.",
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    has_image: bool | None = Field(
        default=None,
        alias="hasImage",
        description="Whether the result contains an image.",
    )
    has_video: bool | None = Field(
        default=None,
        alias="hasVideo",
        description="Whether the result contains a video.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    likes: int | None = Field(default=None, description="Like count.")
    reposts: int | None = Field(default=None, description="Repost count.")
    text: str | None = Field(
        default=None,
        description="Post text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(default=None, alias="type", description="Post type.")
    url: str | None = Field(
        default=None,
        description="Canonical post URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class WeiboUserPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    posts: list[WeiboUserPostsPost] = Field(
        description="Normalized Weibo posts. Populated whenever the provider has data for the entity."
    )


class WeiboUserPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author avatar URL."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical URL of the author's Weibo profile.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author user identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author is verified.",
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="Post preview image URL.")
    image_count: int | None = Field(
        default=None,
        alias="imageCount",
        description="Number of images attached to the post.",
    )
    likes: int | None = Field(default=None, description="Like count.")
    region: str | None = Field(
        default=None,
        description="Region the post was published from, as Weibo reports it.",
    )
    reposts: int | None = Field(default=None, description="Repost count.")
    short_id: str | None = Field(
        default=None,
        alias="shortId",
        description="Short Weibo post identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    text: str | None = Field(
        default=None,
        description="Plain post text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class WeiboNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def hot_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboHotSearchInput],
    ) -> RunResult[WeiboHotSearchData]:
        """Weibo Hot Search

        Get the complete current Weibo hot-search ranking with labels and heat
        values.

        Price: $0.0018 per request.

        Example:
            res = client.weibo.hot_search()
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.hot_search", dict(input), options
        )
        return RunResult[WeiboHotSearchData].model_validate(raw)

    def post(
        self, *, options: RequestOptions | None = None, **input: Unpack[WeiboPostInput]
    ) -> RunResult[WeiboPostData]:
        """Weibo Post

        Fetch a public Weibo post by ID with normalized author and engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.post(includeLongText="true", postId="5092682368025584")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.post", dict(input), options
        )
        return RunResult[WeiboPostData].model_validate(raw)

    def post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboPostCommentsInput],
    ) -> RunResult[WeiboPostCommentsData]:
        """Weibo Post Comments

        List first-level comments on a public Weibo post with pagination.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.post_comments(limit=10, postId="5283919831764022")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.post_comments", dict(input), options
        )
        return RunResult[WeiboPostCommentsData].model_validate(raw)

    def iter_post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboPostCommentsInput],
    ) -> Paginator[WeiboPostCommentsComment, WeiboPostCommentsData]:
        """Iterate Weibo Post Comments results, following pagination cursors.

        Yields validated `WeiboPostCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "weibo.post_comments",
            dict(input),
            "comments",
            item_model=WeiboPostCommentsComment,
            data_model=WeiboPostCommentsData,
            bare=False,
            options=options,
        )

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboProfileInput],
    ) -> RunResult[WeiboProfileData]:
        """Weibo Profile

        Fetch a public Weibo profile by user ID with normalized audience and account
        data.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.profile(userId="1722594714")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.profile", dict(input), options
        )
        return RunResult[WeiboProfileData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboSearchInput],
    ) -> RunResult[WeiboSearchData]:
        """Weibo Advanced Search

        Search public Weibo posts with optional result, media, and time filters.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.search(includeType="pic", page=1, query="python", searchType="hot")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.search", dict(input), options
        )
        return RunResult[WeiboSearchData].model_validate(raw)

    def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboUserPostsInput],
    ) -> RunResult[WeiboUserPostsData]:
        """Weibo User Posts

        List public posts from a Weibo user with normalized author and engagement
        data.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.user_posts(feature=3, page=1, userId="7277477906")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.user_posts", dict(input), options
        )
        return RunResult[WeiboUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboUserPostsInput],
    ) -> Paginator[WeiboUserPostsPost, WeiboUserPostsData]:
        """Iterate Weibo User Posts results, following pagination cursors.

        Yields validated `WeiboUserPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "weibo.user_posts",
            dict(input),
            "posts",
            item_model=WeiboUserPostsPost,
            data_model=WeiboUserPostsData,
            bare=False,
            options=options,
        )


class AsyncWeiboNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def hot_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboHotSearchInput],
    ) -> RunResult[WeiboHotSearchData]:
        """Weibo Hot Search

        Get the complete current Weibo hot-search ranking with labels and heat
        values.

        Price: $0.0018 per request.

        Example:
            res = client.weibo.hot_search()
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.hot_search", dict(input), options
        )
        return RunResult[WeiboHotSearchData].model_validate(raw)

    async def post(
        self, *, options: RequestOptions | None = None, **input: Unpack[WeiboPostInput]
    ) -> RunResult[WeiboPostData]:
        """Weibo Post

        Fetch a public Weibo post by ID with normalized author and engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.post(includeLongText="true", postId="5092682368025584")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.post", dict(input), options
        )
        return RunResult[WeiboPostData].model_validate(raw)

    async def post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboPostCommentsInput],
    ) -> RunResult[WeiboPostCommentsData]:
        """Weibo Post Comments

        List first-level comments on a public Weibo post with pagination.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.post_comments(limit=10, postId="5283919831764022")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.post_comments", dict(input), options
        )
        return RunResult[WeiboPostCommentsData].model_validate(raw)

    def iter_post_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboPostCommentsInput],
    ) -> AsyncPaginator[WeiboPostCommentsComment, WeiboPostCommentsData]:
        """Iterate Weibo Post Comments results, following pagination cursors.

        Yields validated `WeiboPostCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "weibo.post_comments",
            dict(input),
            "comments",
            item_model=WeiboPostCommentsComment,
            data_model=WeiboPostCommentsData,
            bare=False,
            options=options,
        )

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboProfileInput],
    ) -> RunResult[WeiboProfileData]:
        """Weibo Profile

        Fetch a public Weibo profile by user ID with normalized audience and account
        data.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.profile(userId="1722594714")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.profile", dict(input), options
        )
        return RunResult[WeiboProfileData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboSearchInput],
    ) -> RunResult[WeiboSearchData]:
        """Weibo Advanced Search

        Search public Weibo posts with optional result, media, and time filters.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.search(includeType="pic", page=1, query="python", searchType="hot")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.search", dict(input), options
        )
        return RunResult[WeiboSearchData].model_validate(raw)

    async def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboUserPostsInput],
    ) -> RunResult[WeiboUserPostsData]:
        """Weibo User Posts

        List public posts from a Weibo user with normalized author and engagement
        data.

        Price: $0.0012 per request.

        Example:
            res = client.weibo.user_posts(feature=3, page=1, userId="7277477906")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "weibo.user_posts", dict(input), options
        )
        return RunResult[WeiboUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WeiboUserPostsInput],
    ) -> AsyncPaginator[WeiboUserPostsPost, WeiboUserPostsData]:
        """Iterate Weibo User Posts results, following pagination cursors.

        Yields validated `WeiboUserPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "weibo.user_posts",
            dict(input),
            "posts",
            item_model=WeiboUserPostsPost,
            data_model=WeiboUserPostsData,
            bare=False,
            options=options,
        )
