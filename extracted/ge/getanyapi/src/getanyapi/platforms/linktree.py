# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the linktree platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class LinktreeProfileInput(TypedDict, total=False):
    """Input for Linktree Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["locked", "thumbnailUrl", "title"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `title`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a page that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The Linktree profile URL, e.g. https://linktr.ee/mkbhd."""


class LinktreeProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    apple_music: str | None = Field(
        default=None,
        alias="appleMusic",
        description="Apple Music artist URL listed in the page's social icons; null when none.",
    )
    apple_podcast: str | None = Field(
        default=None,
        alias="applePodcast",
        description="Apple Podcasts show URL listed in the page's social icons; null when none.",
    )
    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Profile picture URL; null when none is set. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None, description="The page's bio as plain text; null when none is set."
    )
    email: str | None = Field(
        default=None,
        description="Contact email listed on the page; null when none is listed.",
    )
    facebook: str | None = Field(
        default=None,
        description="Facebook page URL listed in the page's social icons; null when none.",
    )
    id: str | None = Field(default=None, description="Linktree account id.")
    instagram: str | None = Field(
        default=None,
        description="Instagram profile URL listed in the page's social icons; null when none.",
    )
    linkedin: str | None = Field(
        default=None,
        description="LinkedIn profile URL listed in the page's social icons; null when none.",
    )
    links: list[LinktreeProfileLink] | None = Field(
        default=None,
        description="The page's link cards in page order. Headers and group cards have no url. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    soundcloud: str | None = Field(
        default=None,
        description="SoundCloud profile URL listed in the page's social icons; null when none.",
    )
    spotify: str | None = Field(
        default=None,
        description="Spotify artist or show URL listed in the page's social icons; null when none.",
    )
    tiktok: str | None = Field(
        default=None,
        description="TikTok profile URL listed in the page's social icons; null when none.",
    )
    timezone: str | None = Field(
        default=None,
        description="The account's timezone as the page reports it, e.g. America/New_York.",
    )
    title: str | None = Field(
        default=None,
        description="The page's title; the username when none is set. Null when this source does not report it.",
    )
    twitch: str | None = Field(
        default=None,
        description="Twitch channel URL listed in the page's social icons; null when none.",
    )
    username: str = Field(
        description="The page's Linktree username. Populated whenever the provider has data for the entity."
    )
    verticals: list[str] | None = Field(
        default=None,
        description="Creator categories picked on Linktree, e.g. Creator or Music.",
    )
    x: str | None = Field(
        default=None,
        description="X (Twitter) profile URL listed in the page's social icons; null when none.",
    )
    youtube: str | None = Field(
        default=None,
        description="YouTube channel URL listed in the page's social icons; null when none.",
    )


class LinktreeProfileLink(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(
        description="Link card id. Populated whenever the provider has data for the entity."
    )
    locked: bool | None = Field(
        default=None,
        description="True when Linktree locks the card and withholds its destination. Null when this source does not report it.",
    )
    thumbnail_url: str | None = Field(
        default=None,
        alias="thumbnailUrl",
        description="Card thumbnail URL; null when none is set or when this source does not report it.",
    )
    title: str | None = Field(
        default=None, description="Card title; null when none is set."
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Linktree card type, e.g. CLASSIC, HEADER, GROUP or YOUTUBE_VIDEO. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Where the card links to; null for headers, groups and locked cards. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class LinktreeNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinktreeProfileInput],
    ) -> RunResult[LinktreeProfileData]:
        """Linktree Profile

        Get a public Linktree page by URL: title, bio, picture, contact email,
        linked social accounts, and every link card with its destination.

        Price: $0.0011 per request.

        Example:
            res = client.linktree.profile(url="https://linktr.ee/mkbhd")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "linktree.profile", dict(input), options
        )
        return RunResult[LinktreeProfileData].model_validate(raw)


class AsyncLinktreeNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[LinktreeProfileInput],
    ) -> RunResult[LinktreeProfileData]:
        """Linktree Profile

        Get a public Linktree page by URL: title, bio, picture, contact email,
        linked social accounts, and every link card with its destination.

        Price: $0.0011 per request.

        Example:
            res = client.linktree.profile(url="https://linktr.ee/mkbhd")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "linktree.profile", dict(input), options
        )
        return RunResult[LinktreeProfileData].model_validate(raw)
