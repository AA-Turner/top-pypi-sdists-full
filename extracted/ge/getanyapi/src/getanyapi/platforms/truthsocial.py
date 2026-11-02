# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the truthsocial platform."""

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


class TruthsocialPostInput(TypedDict, total=False):
    """Input for Truth Social Post."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Full Truth Social post URL, e.g. "https://truthsocial.com/@realDonaldTrump/posts/116824551176646175"."""


class TruthsocialProfileInput(TypedDict, total=False):
    """Input for Truth Social Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """Truth Social handle without the @, e.g. "realDonaldTrump"."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TruthsocialUserPostsInput(TypedDict, total=False):
    """Input for Truth Social User Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; a page holds 20 posts."""
    handle: Required[str]
    """Truth Social handle without the @, e.g. "realDonaldTrump"."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TruthsocialPostData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Avatar URL of the account that posted.",
    )
    comments: int = Field(description="Number of comments on the post.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    display_name: str = Field(
        alias="displayName",
        description="Display name of the author. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None, description="Preview image URL for the post."
    )
    likes: int = Field(description="Number of likes on the post.")
    media_urls: list[str] | None = Field(
        default=None,
        alias="mediaUrls",
        description="URLs of media attached to the post.",
    )
    shares: int = Field(description="Number of reblogs of the post.")
    text: str = Field(
        description="Post text content. Populated whenever the provider has data for the entity."
    )
    username: str = Field(
        description="Username of the author. Populated whenever the provider has data for the entity."
    )
    verified: bool | None = Field(
        default=None,
        description="Whether the posting account is verified on Truth Social.",
    )


class TruthsocialProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    bio: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    display_name: str = Field(
        alias="displayName",
        description="Populated whenever the provider has data for the entity.",
    )
    followers: int
    following: int
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    joined_at: str = Field(
        alias="joinedAt",
        description="Populated whenever the provider has data for the entity.",
    )
    posts_count: int = Field(alias="postsCount")
    private: bool
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    username: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    verified: bool


class TruthsocialUserPostsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of posts, or null/empty when there are no more. Pass it back as cursor to continue.",
    )
    posts: list[TruthsocialUserPostsPost] = Field(
        description="The user's recent posts. Populated whenever the provider has data for the entity."
    )


class TruthsocialUserPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Avatar URL of the account that posted.",
    )
    comments: int = Field(description="Number of comments on the post.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    display_name: str | None = Field(
        default=None,
        alias="displayName",
        description="Display name of the account that posted.",
    )
    id: str = Field(
        description="Post identifier. Populated whenever the provider has data for the entity."
    )
    likes: int = Field(description="Number of likes on the post.")
    shares: int = Field(description="Number of reblogs of the post.")
    text: str = Field(
        description="Post text content. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the post. Populated whenever the provider has data for the entity."
    )
    username: str | None = Field(
        default=None, description="Handle of the account that posted."
    )
    verified: bool | None = Field(
        default=None,
        description="Whether the posting account is verified on Truth Social.",
    )


class TruthsocialNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialPostInput],
    ) -> RunResult[TruthsocialPostData]:
        """Truth Social Post

        Get a single Truth Social post by its URL - text, author, engagement (likes,
        comments, shares), and timestamp as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.truthsocial.post(url="https://truthsocial.com/@realDonaldTrump/posts/116824551176646175")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "truthsocial.post", dict(input), options
        )
        return RunResult[TruthsocialPostData].model_validate(raw)

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialProfileInput],
    ) -> RunResult[TruthsocialProfileData]:
        """Truth Social Profile

        Get a Truth Social account's public profile by handle - display name, bio,
        follower/following counts, and post count as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.truthsocial.profile(handle="DevinNunes")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "truthsocial.profile", dict(input), options
        )
        return RunResult[TruthsocialProfileData].model_validate(raw)

    def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialUserPostsInput],
    ) -> RunResult[TruthsocialUserPostsData]:
        """Truth Social User Posts

        List a Truth Social account's recent posts by handle - text, engagement
        (likes, comments, shares), and timestamps as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.truthsocial.user_posts(handle="realDonaldTrump")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "truthsocial.user_posts", dict(input), options
        )
        return RunResult[TruthsocialUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialUserPostsInput],
    ) -> Paginator[TruthsocialUserPostsPost, TruthsocialUserPostsData]:
        """Iterate Truth Social User Posts results, following pagination cursors.

        Yields validated `TruthsocialUserPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "truthsocial.user_posts",
            dict(input),
            "posts",
            item_model=TruthsocialUserPostsPost,
            data_model=TruthsocialUserPostsData,
            bare=False,
            options=options,
        )


class AsyncTruthsocialNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialPostInput],
    ) -> RunResult[TruthsocialPostData]:
        """Truth Social Post

        Get a single Truth Social post by its URL - text, author, engagement (likes,
        comments, shares), and timestamp as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.truthsocial.post(url="https://truthsocial.com/@realDonaldTrump/posts/116824551176646175")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "truthsocial.post", dict(input), options
        )
        return RunResult[TruthsocialPostData].model_validate(raw)

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialProfileInput],
    ) -> RunResult[TruthsocialProfileData]:
        """Truth Social Profile

        Get a Truth Social account's public profile by handle - display name, bio,
        follower/following counts, and post count as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.truthsocial.profile(handle="DevinNunes")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "truthsocial.profile", dict(input), options
        )
        return RunResult[TruthsocialProfileData].model_validate(raw)

    async def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialUserPostsInput],
    ) -> RunResult[TruthsocialUserPostsData]:
        """Truth Social User Posts

        List a Truth Social account's recent posts by handle - text, engagement
        (likes, comments, shares), and timestamps as clean JSON.

        Price: $0.0012 per request.

        Example:
            res = client.truthsocial.user_posts(handle="realDonaldTrump")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "truthsocial.user_posts", dict(input), options
        )
        return RunResult[TruthsocialUserPostsData].model_validate(raw)

    def iter_user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TruthsocialUserPostsInput],
    ) -> AsyncPaginator[TruthsocialUserPostsPost, TruthsocialUserPostsData]:
        """Iterate Truth Social User Posts results, following pagination cursors.

        Yields validated `TruthsocialUserPostsPost` items from the `posts` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "truthsocial.user_posts",
            dict(input),
            "posts",
            item_model=TruthsocialUserPostsPost,
            data_model=TruthsocialUserPostsData,
            bare=False,
            options=options,
        )
