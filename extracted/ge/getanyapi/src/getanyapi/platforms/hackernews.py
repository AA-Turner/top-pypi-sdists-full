# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the hackernews platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class HackernewsProfileInput(TypedDict, total=False):
    """Input for Hacker News Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """Hacker News username, e.g. "pg"."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class HackernewsSearchInput(TypedDict, total=False):
    """Input for Hacker News Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword, e.g. "ai"."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    tags: NotRequired[str]
    """Optional result filter, e.g. "story" or "comment"."""


class HackernewsStoryInput(TypedDict, total=False):
    """Input for Hacker News Story."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: Required[str]
    """Hacker News story id, e.g. "47340079"."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class HackernewsStoryCommentsInput(TypedDict, total=False):
    """Input for Hacker News Story Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: Required[str]
    """Hacker News story id, e.g. "47340079"."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class HackernewsProfileData(BaseModel):
    model_config = ConfigDict(extra="allow")

    bio: str
    karma: int
    username: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class HackernewsSearchData(BaseModel):
    results: list[HackernewsSearchResult] = Field(
        description="Matching Hacker News stories. Populated whenever the provider has data for the entity."
    )


class HackernewsSearchResult(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Submitting user's username. Populated whenever the provider has data for the entity."
    )
    comments: int = Field(description="Number of comments on the story.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Hacker News item id. Populated whenever the provider has data for the entity."
    )
    permalink: str | None = Field(
        default=None, description="Permalink to the item on news.ycombinator.com."
    )
    points: int = Field(description="Story score (upvotes).")
    title: str = Field(
        description="Story title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(description="Story link.")


class HackernewsStoryData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Submitting user's username. Populated whenever the provider has data for the entity."
    )
    comments: int = Field(description="Number of comments on the story.")
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str | None = Field(
        default=None, description="Hacker News item ID of the story."
    )
    permalink: str | None = Field(
        default=None, description="Permalink to the item on news.ycombinator.com."
    )
    points: int = Field(description="Story score (upvotes).")
    title: str = Field(
        description="Story title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(description="Story link.")


class HackernewsStoryCommentsData(BaseModel):
    comments: list[HackernewsStoryCommentsComment] = Field(
        description="Comments on the story. Populated whenever the provider has data for the entity."
    )


class HackernewsStoryCommentsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str = Field(
        description="Commenting user's username. Populated whenever the provider has data for the entity."
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Hacker News comment id. Populated whenever the provider has data for the entity."
    )
    parent_id: str = Field(
        alias="parentId",
        description="Id of the parent item (story or comment) this reply belongs to.",
    )
    permalink: str | None = Field(
        default=None, description="Permalink to the item on news.ycombinator.com."
    )
    post_id: str | None = Field(
        default=None,
        alias="postId",
        description="Hacker News item ID of the story the comment belongs to.",
    )
    text: str = Field(description="Comment body text.")


class HackernewsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsProfileInput],
    ) -> RunResult[HackernewsProfileData]:
        """Hacker News Profile

        Get a Hacker News user's public profile by username - karma, bio, and
        account details as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.profile(handle="pg")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.profile", dict(input), options
        )
        return RunResult[HackernewsProfileData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsSearchInput],
    ) -> RunResult[HackernewsSearchData]:
        """Hacker News Search

        Search Hacker News by keyword - matching stories with title, link, author,
        points, and comment count as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.search(query="ai")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.search", dict(input), options
        )
        return RunResult[HackernewsSearchData].model_validate(raw)

    def story(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsStoryInput],
    ) -> RunResult[HackernewsStoryData]:
        """Hacker News Story

        Get a Hacker News story by id - title, link, author, points, and comment
        count as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.story(id="47340079")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.story", dict(input), options
        )
        return RunResult[HackernewsStoryData].model_validate(raw)

    def story_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsStoryCommentsInput],
    ) -> RunResult[HackernewsStoryCommentsData]:
        """Hacker News Story Comments

        List the comments on a Hacker News story by id - text, author, and timestamp
        as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.story_comments(id="47340079")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.story_comments", dict(input), options
        )
        return RunResult[HackernewsStoryCommentsData].model_validate(raw)


class AsyncHackernewsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsProfileInput],
    ) -> RunResult[HackernewsProfileData]:
        """Hacker News Profile

        Get a Hacker News user's public profile by username - karma, bio, and
        account details as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.profile(handle="pg")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.profile", dict(input), options
        )
        return RunResult[HackernewsProfileData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsSearchInput],
    ) -> RunResult[HackernewsSearchData]:
        """Hacker News Search

        Search Hacker News by keyword - matching stories with title, link, author,
        points, and comment count as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.search(query="ai")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.search", dict(input), options
        )
        return RunResult[HackernewsSearchData].model_validate(raw)

    async def story(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsStoryInput],
    ) -> RunResult[HackernewsStoryData]:
        """Hacker News Story

        Get a Hacker News story by id - title, link, author, points, and comment
        count as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.story(id="47340079")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.story", dict(input), options
        )
        return RunResult[HackernewsStoryData].model_validate(raw)

    async def story_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[HackernewsStoryCommentsInput],
    ) -> RunResult[HackernewsStoryCommentsData]:
        """Hacker News Story Comments

        List the comments on a Hacker News story by id - text, author, and timestamp
        as clean JSON.

        Price: $0.0015 per request.

        Example:
            res = client.hackernews.story_comments(id="47340079")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "hackernews.story_comments", dict(input), options
        )
        return RunResult[HackernewsStoryCommentsData].model_validate(raw)
