# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the telegram platform."""

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


class TelegramChannelInput(TypedDict, total=False):
    """Input for Telegram Channel."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """Public Telegram channel username, with or without the @ (e.g. "telegram"), or its t.me link."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "fileCount", "linkCount", "photoCount", "previewEnabled", "videoCount"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `photoCount`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a channel that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TelegramChannelPostsInput(TypedDict, total=False):
    """Input for Telegram Channel Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor, for older posts. Omit for the newest page; a page holds about 20 posts."""
    handle: Required[str]
    """Public Telegram channel username, with or without the @ (e.g. "telegram"), or its t.me link."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "edited",
                "linkPreviewDescription",
                "linkPreviewTitle",
                "linkPreviewUrl",
                "media",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `linkPreviewUrl` or `edited`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TelegramPostInput(TypedDict, total=False):
    """Input for Telegram Post."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "durationSeconds",
                "edited",
                "linkPreviewDescription",
                "linkPreviewTitle",
                "linkPreviewUrl",
                "media",
                "type",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `linkPreviewUrl` or `edited`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a post that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Link to one public channel post, e.g. https://t.me/telegram/460 (t.me/s/ links work too)."""


class TelegramChannelData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Channel photo URL. Temporary: Telegram's CDN link expires.",
    )
    description: str | None = Field(
        default=None,
        description="Channel bio as plain text; null when the channel has none.",
    )
    file_count: int | None = Field(
        default=None,
        alias="fileCount",
        description="Files the channel has posted, rounded by Telegram. Null when not shown or when this source does not report it.",
    )
    handle: str = Field(
        description="Channel username, without the @. Populated whenever the provider has data for the entity."
    )
    link_count: int | None = Field(
        default=None,
        alias="linkCount",
        description="Links the channel has posted, rounded by Telegram. Null when not shown or when this source does not report it.",
    )
    photo_count: int | None = Field(
        default=None,
        alias="photoCount",
        description='Photos the channel has posted. Telegram rounds this count ("1.2K" becomes 1200). Null when not shown or when this source does not report it.',
    )
    preview_enabled: bool | None = Field(
        default=None,
        alias="previewEnabled",
        description="True when the channel's public web preview is on, which is what telegram.channel_posts and telegram.post read the channel's posts from. Null when this source does not report it.",
    )
    subscribers: int | None = Field(
        default=None,
        description="Exact subscriber count, read from the channel's public t.me page. Null when Telegram does not show it. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str | None = Field(
        default=None,
        description="Channel name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(default=None, description="The channel's t.me link.")
    verified: bool | None = Field(
        default=None,
        description="True when the channel carries Telegram's verified badge. Null when this source does not report it.",
    )
    video_count: int | None = Field(
        default=None,
        alias="videoCount",
        description="Videos the channel has posted, rounded by Telegram. Null when not shown or when this source does not report it.",
    )


class TelegramChannelPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next, older page of posts, or null/empty when there are no more. Pass it back as cursor to continue.",
    )
    posts: list[TelegramChannelPostsPost] = Field(
        description="One page of the channel's posts, about 20, from the newest page back. Populated whenever the provider has data for the entity."
    )


class TelegramChannelPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    channel: str | None = Field(
        default=None, description="Username of the channel that published the post."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    edited: bool | None = Field(
        default=None,
        description="True when the post was edited after it was published. Null when this source does not report it.",
    )
    id: str = Field(
        description="Post number, unique within the channel. Posts are numbered in order. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Thumbnail image URL for the post's photo, video or link preview; null when it has none. Temporary: Telegram's CDN link expires.",
    )
    link_preview_description: str | None = Field(
        default=None,
        alias="linkPreviewDescription",
        description="Description on the post's link preview card. Null when the post has no link preview, the card has no description, or this source does not report it.",
    )
    link_preview_title: str | None = Field(
        default=None,
        alias="linkPreviewTitle",
        description="Title on the post's link preview card. Null when the post has no link preview, the card has no title, or this source does not report it.",
    )
    link_preview_url: str | None = Field(
        default=None,
        alias="linkPreviewUrl",
        description="URL of the page the post's link preview card shows. Null when the post has no link preview or this source does not report it.",
    )
    media: list[TelegramChannelPostsMedia] | None = Field(
        default=None,
        description="The post's attachments in order, each with its kind, file URL, preview image and length. Empty when the post has none; null when this source does not report them.",
    )
    media_urls: list[str] | None = Field(
        default=None,
        alias="mediaUrls",
        description="Direct URLs of the post's photos and videos. Temporary and signed: keep the query string. Empty when the post has no media or Telegram withholds a large video's file.",
    )
    reactions: list[TelegramChannelPostsReaction] | None = Field(
        default=None,
        description="Reactions on the post and how many of each. Empty when the post has none or the channel hides them.",
    )
    text: str | None = Field(
        default=None,
        description="Post text or media caption, plain. Empty when the post has none. Some sources collapse line breaks into spaces. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="The post's t.me link, e.g. https://t.me/telegram/441. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    views: int | None = Field(
        default=None,
        description='View count. Telegram rounds it ("1.2K" becomes 1200). Null when not shown.',
    )


class TelegramChannelPostsMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Video length in seconds; null for other attachments.",
    )
    image: str | None = Field(
        default=None,
        description="Preview image URL (the photo itself for a photo). Temporary: Telegram's CDN link expires. Null when there is none.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Attachment kind as Telegram labels it, e.g. photo or video.",
    )
    url: str | None = Field(
        default=None,
        description="Direct file URL. Temporary and signed: keep the query string. Null when Telegram withholds the file, as for a large video.",
    )


class TelegramChannelPostsReaction(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = Field(
        default=None,
        description="How many times it was given. Telegram rounds large counts.",
    )
    emoji: str | None = Field(
        default=None,
        description="The reaction's emoji; null for a custom emoji, and on some sources for a paid star reaction.",
    )


class TelegramPostData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    channel: str | None = Field(
        default=None,
        description="Username of the channel that published the post. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    edited: bool | None = Field(
        default=None,
        description="True when the post was edited after it was published. Null when this source does not report it.",
    )
    id: str = Field(
        description="Post number, unique within the channel. Posts are numbered in order. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Thumbnail image URL for the post's photo, video or link preview; null when it has none. Temporary: Telegram's CDN link expires.",
    )
    link_preview_description: str | None = Field(
        default=None,
        alias="linkPreviewDescription",
        description="Description on the post's link preview card. Null when the post has no link preview, the card has no description, or this source does not report it.",
    )
    link_preview_title: str | None = Field(
        default=None,
        alias="linkPreviewTitle",
        description="Title on the post's link preview card. Null when the post has no link preview, the card has no title, or this source does not report it.",
    )
    link_preview_url: str | None = Field(
        default=None,
        alias="linkPreviewUrl",
        description="URL of the page the post's link preview card shows. Null when the post has no link preview or this source does not report it.",
    )
    media: list[TelegramPostMedia] | None = Field(
        default=None,
        description="The post's attachments in order, each with its kind, file URL, preview image and length. Empty when the post has none; null when this source does not report them.",
    )
    media_urls: list[str] | None = Field(
        default=None,
        alias="mediaUrls",
        description="Direct URLs of the post's photos and videos. Temporary and signed: keep the query string. Empty when the post has no media or Telegram withholds a large video's file.",
    )
    reactions: list[TelegramPostReaction] | None = Field(
        default=None,
        description="Reactions on the post and how many of each. Empty when the post has none or the channel hides them.",
    )
    text: str | None = Field(
        default=None,
        description="Post text or media caption, plain. Empty when the post has none. Some sources collapse line breaks into spaces. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="The post's t.me link. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    views: int | None = Field(
        default=None,
        description='View count. Telegram rounds it ("1.2K" becomes 1200). Null when not shown.',
    )


class TelegramPostMedia(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    duration_seconds: float | None = Field(
        default=None,
        alias="durationSeconds",
        description="Video length in seconds; null for other attachments.",
    )
    image: str | None = Field(
        default=None,
        description="Preview image URL (the photo itself for a photo). Temporary: Telegram's CDN link expires. Null when there is none.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Attachment kind as Telegram labels it, e.g. photo or video.",
    )
    url: str | None = Field(
        default=None,
        description="Direct file URL. Temporary and signed: keep the query string. Null when Telegram withholds the file, as for a large video.",
    )


class TelegramPostReaction(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = Field(
        default=None,
        description="How many times it was given. Telegram rounds large counts.",
    )
    emoji: str | None = Field(
        default=None,
        description="The reaction's emoji; null for a custom emoji, and on some sources for a paid star reaction.",
    )


class TelegramNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def channel(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramChannelInput],
    ) -> RunResult[TelegramChannelData]:
        """Telegram Channel

        Get a public Telegram channel by username: name, bio, photo, verified badge,
        exact subscriber count, and how many photos, videos, files and links it has
        posted.

        Price: $0.0011 per request.

        Example:
            res = client.telegram.channel(handle="telegram")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "telegram.channel", dict(input), options
        )
        return RunResult[TelegramChannelData].model_validate(raw)

    def channel_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramChannelPostsInput],
    ) -> RunResult[TelegramChannelPostsData]:
        """Telegram Channel Posts

        Get a public Telegram channel's posts by username, about 20 per page with a
        cursor for older pages: text, posting time, views, photo and video links,
        and reactions.

        Price: $0.0011 per request.

        Example:
            res = client.telegram.channel_posts(handle="telegram")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "telegram.channel_posts", dict(input), options
        )
        return RunResult[TelegramChannelPostsData].model_validate(raw)

    def iter_channel_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramChannelPostsInput],
    ) -> Paginator[TelegramChannelPostsPost, TelegramChannelPostsData]:
        """Iterate Telegram Channel Posts results, following pagination cursors.

        Yields validated `TelegramChannelPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "telegram.channel_posts",
            dict(input),
            "posts",
            item_model=TelegramChannelPostsPost,
            data_model=TelegramChannelPostsData,
            bare=False,
            options=options,
        )

    def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramPostInput],
    ) -> RunResult[TelegramPostData]:
        """Telegram Post

        Get one public Telegram channel post by its t.me link: text, posting time,
        views, photo and video links, and reactions.

        Price: $0.0011 per request.

        Example:
            res = client.telegram.post(url="https://t.me/telegram/460")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "telegram.post", dict(input), options
        )
        return RunResult[TelegramPostData].model_validate(raw)


class AsyncTelegramNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def channel(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramChannelInput],
    ) -> RunResult[TelegramChannelData]:
        """Telegram Channel

        Get a public Telegram channel by username: name, bio, photo, verified badge,
        exact subscriber count, and how many photos, videos, files and links it has
        posted.

        Price: $0.0011 per request.

        Example:
            res = client.telegram.channel(handle="telegram")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "telegram.channel", dict(input), options
        )
        return RunResult[TelegramChannelData].model_validate(raw)

    async def channel_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramChannelPostsInput],
    ) -> RunResult[TelegramChannelPostsData]:
        """Telegram Channel Posts

        Get a public Telegram channel's posts by username, about 20 per page with a
        cursor for older pages: text, posting time, views, photo and video links,
        and reactions.

        Price: $0.0011 per request.

        Example:
            res = client.telegram.channel_posts(handle="telegram")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "telegram.channel_posts", dict(input), options
        )
        return RunResult[TelegramChannelPostsData].model_validate(raw)

    def iter_channel_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramChannelPostsInput],
    ) -> AsyncPaginator[TelegramChannelPostsPost, TelegramChannelPostsData]:
        """Iterate Telegram Channel Posts results, following pagination cursors.

        Yields validated `TelegramChannelPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "telegram.channel_posts",
            dict(input),
            "posts",
            item_model=TelegramChannelPostsPost,
            data_model=TelegramChannelPostsData,
            bare=False,
            options=options,
        )

    async def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TelegramPostInput],
    ) -> RunResult[TelegramPostData]:
        """Telegram Post

        Get one public Telegram channel post by its t.me link: text, posting time,
        views, photo and video links, and reactions.

        Price: $0.0011 per request.

        Example:
            res = client.telegram.post(url="https://t.me/telegram/460")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "telegram.post", dict(input), options
        )
        return RunResult[TelegramPostData].model_validate(raw)
