# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the douyin platform."""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class DouyinProfileInput(TypedDict, total=False):
    """Input for Douyin Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    secUserId: Required[str]
    """Douyin sec_user_id for the public account."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class DouyinSearchVideosInput(TypedDict, total=False):
    """Input for Douyin Video Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    backtrace: NotRequired[str]
    """Backtrace token returned by the previous page."""
    cursor: NotRequired[Any]
    """Pagination cursor: pass the previous response's nextCursor; omit for the first page. A raw integer cursor is still accepted."""
    duration: NotRequired[Literal["0", "0-1", "1-5", "5-10000"]]
    """Duration filter in minutes: any, under 1, 1 to 5, or over 5. Default: 0."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    publishedWithin: NotRequired[Any]
    """Publication window in days. Use the canonical JSON integer 0 for any time, 1 for one day, 7 for seven days, or 180 for 180 days; legacy numeric strings remain accepted."""
    query: Required[str]
    """Keyword to search for."""
    searchId: NotRequired[str]
    """Search ID returned by the previous page."""
    sort: NotRequired[Literal["relevance", "most-liked", "date-posted"]]
    """Sort order: relevance (Douyin's comprehensive ranking), most-liked, date-posted. Default: relevance."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class DouyinUserPostsInput(TypedDict, total=False):
    """Input for Douyin User Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[Any]
    """Pagination cursor: pass the previous response's nextCursor; omit for the first page. A raw integer cursor is still accepted."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Requested page size. Values up to 20 are recommended. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    secUserId: Required[str]
    """Douyin sec_user_id for the public account."""
    sort: NotRequired[Literal["newest", "most-popular"]]
    """Post order: newest, most-popular. Default: newest."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class DouyinVideoInput(TypedDict, total=False):
    """Input for Douyin Video."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Public Douyin video share URL."""


class DouyinVideoCommentsInput(TypedDict, total=False):
    """Input for Douyin Video Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[Any]
    """Pagination cursor: pass the previous response's nextCursor; omit for the first page. A raw integer cursor is still accepted."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    videoId: Required[str]
    """Douyin aweme_id for the video."""


class DouyinProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bio: str | None = Field(default=None, description="Profile biography.")
    followers: int | None = Field(default=None, description="Follower count.")
    following: int | None = Field(default=None, description="Following count.")
    image: str | None = Field(
        default=None,
        description="Profile image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    likes: int | None = Field(default=None, description="Total likes received.")
    nickname: str | None = Field(
        default=None,
        description="Display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    posts: int | None = Field(default=None, description="Published post count.")
    sec_user_id: str = Field(
        alias="secUserId",
        description="Douyin sec_user_id. Populated whenever the provider has data for the entity.",
    )
    short_id: str | None = Field(
        default=None, alias="shortId", description="Legacy numeric short ID."
    )
    unique_id: str | None = Field(
        default=None,
        alias="uniqueId",
        description="Public Douyin handle when configured. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    user_id: str = Field(
        alias="userId",
        description="Douyin user identifier. Populated whenever the provider has data for the entity.",
    )


class DouyinSearchVideosData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    backtrace: str = Field(description="Backtrace token required for the next page.")
    has_more: bool = Field(
        alias="hasMore", description="Whether another page is available."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of videos, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    search_id: str = Field(
        alias="searchId", description="Search ID required for the next page."
    )
    videos: list[DouyinSearchVideosVideo] = Field(
        description="Normalized matching videos. Populated whenever the provider has data for the entity."
    )


class DouyinSearchVideosVideo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author's avatar image URL."
    )
    author_nickname: str | None = Field(
        default=None,
        alias="authorNickname",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_unique_id: str | None = Field(
        default=None,
        alias="authorUniqueId",
        description="Author's Douyin handle (unique id).",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author user identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account is verified.",
    )
    caption: str | None = Field(
        default=None,
        description="Video caption. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    duration_ms: int | None = Field(
        default=None, alias="durationMs", description="Video duration in milliseconds."
    )
    height: int | None = Field(default=None, description="Pixel height of the video.")
    id: str = Field(
        description="Video identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="Cover image URL.")
    likes: int | None = Field(default=None, description="Like count.")
    region: str | None = Field(
        default=None, description="Two-letter region code the video was published from."
    )
    saves: int | None = Field(default=None, description="Save count.")
    shares: int | None = Field(default=None, description="Share count.")
    url: str | None = Field(
        default=None,
        description="Canonical video URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. The query string carries required access parameters, so keep it intact.",
    )
    views: int | None = Field(default=None, description="Play count.")
    width: int | None = Field(default=None, description="Pixel width of the video.")


class DouyinUserPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool = Field(
        alias="hasMore", description="Whether another page is available."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    posts: list[DouyinUserPostsPost] = Field(
        description="Normalized Douyin posts. Populated whenever the provider has data for the entity."
    )


class DouyinUserPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author's avatar image URL."
    )
    author_nickname: str | None = Field(
        default=None,
        alias="authorNickname",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_sec_user_id: str | None = Field(
        default=None,
        alias="authorSecUserId",
        description="Author sec_user_id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_unique_id: str | None = Field(
        default=None,
        alias="authorUniqueId",
        description="Author's Douyin handle (unique id).",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author user identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account is verified.",
    )
    caption: str | None = Field(
        default=None,
        description="Post caption. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    duration_ms: int | None = Field(
        default=None, alias="durationMs", description="Media duration in milliseconds."
    )
    height: int | None = Field(default=None, description="Pixel height of the media.")
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="Cover image URL.")
    likes: int | None = Field(default=None, description="Like count.")
    region: str | None = Field(
        default=None, description="Two-letter region code the post was published from."
    )
    saves: int | None = Field(default=None, description="Save count.")
    shares: int | None = Field(default=None, description="Share count.")
    url: str | None = Field(
        default=None,
        description="Canonical post URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    views: int | None = Field(default=None, description="Play count.")
    width: int | None = Field(default=None, description="Pixel width of the media.")


class DouyinVideoData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author's avatar image URL."
    )
    author_nickname: str | None = Field(
        default=None,
        alias="authorNickname",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_sec_user_id: str | None = Field(
        default=None,
        alias="authorSecUserId",
        description="Author sec_user_id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_unique_id: str | None = Field(
        default=None,
        alias="authorUniqueId",
        description="Author's Douyin handle (unique id).",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author user identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author's account is verified.",
    )
    caption: str | None = Field(
        default=None,
        description="Video caption. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    duration_ms: int | None = Field(
        default=None, alias="durationMs", description="Video duration in milliseconds."
    )
    height: int | None = Field(default=None, description="Pixel height of the video.")
    id: str = Field(
        description="Video identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="Video cover image URL.")
    likes: int | None = Field(default=None, description="Like count.")
    region: str | None = Field(
        default=None, description="Two-letter region code the video was published from."
    )
    saves: int | None = Field(default=None, description="Save count.")
    shares: int | None = Field(default=None, description="Share count.")
    url: str | None = Field(
        default=None,
        description="Canonical Douyin video URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Playable video URL. The query string carries required access parameters, so keep it intact.",
    )
    views: int | None = Field(default=None, description="Play count.")
    width: int | None = Field(default=None, description="Pixel width of the video.")


class DouyinVideoCommentsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    comments: list[DouyinVideoCommentsComment] = Field(
        description="Normalized video comments. Populated whenever the provider has data for the entity."
    )
    has_more: bool = Field(
        alias="hasMore", description="Whether another page is available."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of comments, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total: int = Field(description="Total comment count reported by Douyin.")


class DouyinVideoCommentsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author profile image URL."
    )
    author_nickname: str | None = Field(
        default=None,
        alias="authorNickname",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_sec_user_id: str | None = Field(
        default=None,
        alias="authorSecUserId",
        description="Author sec_user_id. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_unique_id: str | None = Field(
        default=None, alias="authorUniqueId", description="Author public handle."
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Author user identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Comment identifier. Populated whenever the provider has data for the entity."
    )
    ip_label: str | None = Field(
        default=None,
        alias="ipLabel",
        description="Approximate location label shown by Douyin.",
    )
    likes: int | None = Field(default=None, description="Comment like count.")
    reply_count: int | None = Field(
        default=None, alias="replyCount", description="Direct reply count."
    )
    text: str | None = Field(
        default=None,
        description="Comment text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    video_id: str = Field(
        alias="videoId",
        description="Commented video identifier. Populated whenever the provider has data for the entity.",
    )


class DouyinNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinProfileInput],
    ) -> RunResult[DouyinProfileData]:
        """Douyin Profile

        Look up a public Douyin profile by sec_user_id and return normalized profile
        statistics.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.profile(secUserId="MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.profile", dict(input), options
        )
        return RunResult[DouyinProfileData].model_validate(raw)

    def search_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinSearchVideosInput],
    ) -> RunResult[DouyinSearchVideosData]:
        """Douyin Video Search

        Search public Douyin videos by keyword with sorting, time, duration, and
        content filters.

        Price: $0.012 per request.

        Example:
            res = client.douyin.search_videos(duration="0", publishedWithin=0, query="机器人", sort="relevance")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.search_videos", dict(input), options
        )
        return RunResult[DouyinSearchVideosData].model_validate(raw)

    def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinUserPostsInput],
    ) -> RunResult[DouyinUserPostsData]:
        """Douyin User Posts

        List public posts from a Douyin user with normalized engagement data and
        pagination.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.user_posts(limit=20, secUserId="MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE", sort="newest")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.user_posts", dict(input), options
        )
        return RunResult[DouyinUserPostsData].model_validate(raw)

    def video(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinVideoInput],
    ) -> RunResult[DouyinVideoData]:
        """Douyin Video

        Fetch a public Douyin video by share URL with normalized author and
        engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.video(url="https://www.douyin.com/video/6894784055775071503")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.video", dict(input), options
        )
        return RunResult[DouyinVideoData].model_validate(raw)

    def video_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinVideoCommentsInput],
    ) -> RunResult[DouyinVideoCommentsData]:
        """Douyin Video Comments

        List public comments on a Douyin video with author and engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.video_comments(videoId="7448118827402972455")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.video_comments", dict(input), options
        )
        return RunResult[DouyinVideoCommentsData].model_validate(raw)


class AsyncDouyinNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinProfileInput],
    ) -> RunResult[DouyinProfileData]:
        """Douyin Profile

        Look up a public Douyin profile by sec_user_id and return normalized profile
        statistics.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.profile(secUserId="MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.profile", dict(input), options
        )
        return RunResult[DouyinProfileData].model_validate(raw)

    async def search_videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinSearchVideosInput],
    ) -> RunResult[DouyinSearchVideosData]:
        """Douyin Video Search

        Search public Douyin videos by keyword with sorting, time, duration, and
        content filters.

        Price: $0.012 per request.

        Example:
            res = client.douyin.search_videos(duration="0", publishedWithin=0, query="机器人", sort="relevance")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.search_videos", dict(input), options
        )
        return RunResult[DouyinSearchVideosData].model_validate(raw)

    async def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinUserPostsInput],
    ) -> RunResult[DouyinUserPostsData]:
        """Douyin User Posts

        List public posts from a Douyin user with normalized engagement data and
        pagination.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.user_posts(limit=20, secUserId="MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE", sort="newest")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.user_posts", dict(input), options
        )
        return RunResult[DouyinUserPostsData].model_validate(raw)

    async def video(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinVideoInput],
    ) -> RunResult[DouyinVideoData]:
        """Douyin Video

        Fetch a public Douyin video by share URL with normalized author and
        engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.video(url="https://www.douyin.com/video/6894784055775071503")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.video", dict(input), options
        )
        return RunResult[DouyinVideoData].model_validate(raw)

    async def video_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[DouyinVideoCommentsInput],
    ) -> RunResult[DouyinVideoCommentsData]:
        """Douyin Video Comments

        List public comments on a Douyin video with author and engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.douyin.video_comments(videoId="7448118827402972455")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "douyin.video_comments", dict(input), options
        )
        return RunResult[DouyinVideoCommentsData].model_validate(raw)
