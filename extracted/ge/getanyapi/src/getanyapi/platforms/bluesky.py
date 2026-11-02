# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the bluesky platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class BlueskyPostInput(TypedDict, total=False):
    """Input for Bluesky Post."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Bluesky post URL, e.g. "https://bsky.app/profile/bsky.app/post/3l6oveex3ii2l"."""


class BlueskyProfileInput(TypedDict, total=False):
    """Input for Bluesky Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """Bluesky handle, e.g. "bsky.app" or "jay.bsky.team"."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class BlueskyUserPostsInput(TypedDict, total=False):
    """Input for Bluesky User Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """Bluesky handle, e.g. "bsky.app" or "jay.bsky.team"."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class BlueskyPostData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str = Field(
        alias="authorHandle",
        description="Handle of the account that authored the post. Populated whenever the provider has data for the entity.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Avatar URL of the account that posted.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that posted.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str | None = Field(default=None, description="Bluesky record key of the post.")
    likes: int = Field(description="Number of likes on the post.")
    replies: int = Field(description="Number of replies to the post.")
    reposts: int = Field(description="Number of reposts of the post.")
    text: str = Field(
        description="The post's text content. Populated whenever the provider has data for the entity."
    )


class BlueskyProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None, alias="avatarUrl", description="Avatar URL of the account."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time) the account was created. Multiply by 1000 for a JS Date in milliseconds.",
    )
    description: str = Field(
        description="Populated whenever the provider has data for the entity."
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
        default=None,
        description="Bluesky decentralized identifier (DID) of the account.",
    )
    posts_count: int = Field(alias="postsCount")


class BlueskyUserPostsData(BaseModel):
    posts: list[BlueskyUserPostsPost] = Field(
        description="The account's recent posts. Populated whenever the provider has data for the entity."
    )


class BlueskyUserPostsPost(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str = Field(
        alias="authorHandle",
        description="Handle of the account that authored the post. Populated whenever the provider has data for the entity.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Avatar URL of the account that posted.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that posted.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str | None = Field(default=None, description="Bluesky record key of the post.")
    likes: int = Field(description="Number of likes on the post.")
    replies: int = Field(description="Number of replies to the post.")
    reposts: int = Field(description="Number of reposts of the post.")
    text: str = Field(
        description="The post's text content. Populated whenever the provider has data for the entity."
    )


class BlueskyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BlueskyPostInput],
    ) -> RunResult[BlueskyPostData]:
        """Bluesky Post

        Get a single Bluesky post by URL - text, author handle, like, reply, and
        repost counts as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.bluesky.post(url="https://bsky.app/profile/bsky.app/post/3l6oveex3ii2l")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bluesky.post", dict(input), options
        )
        return RunResult[BlueskyPostData].model_validate(raw)

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BlueskyProfileInput],
    ) -> RunResult[BlueskyProfileData]:
        """Bluesky Profile

        Get a Bluesky user's public profile by handle - display name, bio, follower
        and post counts as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.bluesky.profile(handle="bsky.app")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bluesky.profile", dict(input), options
        )
        return RunResult[BlueskyProfileData].model_validate(raw)

    def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BlueskyUserPostsInput],
    ) -> RunResult[BlueskyUserPostsData]:
        """Bluesky User Posts

        List a Bluesky account's recent posts (text, author handle, like, reply, and
        repost counts) by handle as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.bluesky.user_posts(handle="bsky.app")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bluesky.user_posts", dict(input), options
        )
        return RunResult[BlueskyUserPostsData].model_validate(raw)


class AsyncBlueskyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def post(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BlueskyPostInput],
    ) -> RunResult[BlueskyPostData]:
        """Bluesky Post

        Get a single Bluesky post by URL - text, author handle, like, reply, and
        repost counts as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.bluesky.post(url="https://bsky.app/profile/bsky.app/post/3l6oveex3ii2l")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bluesky.post", dict(input), options
        )
        return RunResult[BlueskyPostData].model_validate(raw)

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BlueskyProfileInput],
    ) -> RunResult[BlueskyProfileData]:
        """Bluesky Profile

        Get a Bluesky user's public profile by handle - display name, bio, follower
        and post counts as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.bluesky.profile(handle="bsky.app")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bluesky.profile", dict(input), options
        )
        return RunResult[BlueskyProfileData].model_validate(raw)

    async def user_posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BlueskyUserPostsInput],
    ) -> RunResult[BlueskyUserPostsData]:
        """Bluesky User Posts

        List a Bluesky account's recent posts (text, author handle, like, reply, and
        repost counts) by handle as clean JSON.

        Price: $0.0011 per request.

        Example:
            res = client.bluesky.user_posts(handle="bsky.app")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bluesky.user_posts", dict(input), options
        )
        return RunResult[BlueskyUserPostsData].model_validate(raw)
