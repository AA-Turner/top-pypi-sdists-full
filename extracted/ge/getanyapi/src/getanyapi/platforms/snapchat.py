# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the snapchat platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SnapchatProfileInput(TypedDict, total=False):
    """Input for Snapchat Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    username: Required[str]
    """The Snapchat username or profile URL to look up (e.g. fcbarcelona or https://www.snapchat.com/add/fcbarcelona)."""


class SnapchatProfileData(BaseModel):
    items: list[SnapchatProfileItem] = Field(
        description="Profile record for the requested Snapchat username (one item). Populated whenever the provider has data for the entity."
    )


class SnapchatProfileItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bio: str | None = Field(
        default=None,
        description="The profile's public bio / description text. Empty when the profile has none.",
    )
    category: str | None = Field(
        default=None,
        description='The profile\'s category (e.g. "Government Org"). Empty when the upstream omits it.',
    )
    display_name: str = Field(
        alias="displayName",
        description="The profile's public display name. Populated whenever the provider has data for the entity.",
    )
    handle: str = Field(
        description="The profile's Snapchat username (add-me handle). Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="URL of the profile avatar image, with tracking query params stripped. Empty when the upstream omits it.",
    )
    stories: list[SnapchatProfileStorie] | None = Field(
        default=None, description="Recent public stories on the profile."
    )
    subscribers: int | None = Field(
        default=None, description="Public subscriber count."
    )
    url: str = Field(
        description="Canonical public profile URL, with tracking query params stripped. Populated whenever the provider has data for the entity."
    )
    website: str | None = Field(
        default=None,
        description="The profile's linked website URL. Empty when the profile has none.",
    )


class SnapchatProfileStorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = Field(default=None, description="Story identifier.")
    story_title: str | None = Field(
        default=None,
        alias="storyTitle",
        description="Story title. Empty when the story has no title.",
    )
    thumbnail_url: str | None = Field(
        default=None,
        alias="thumbnailUrl",
        description="Story thumbnail image URL, preserving signed delivery parameters required to load the preview.",
    )


class SnapchatNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SnapchatProfileInput],
    ) -> RunResult[SnapchatProfileData]:
        """Snapchat Profile

        Fetch a Snapchat user's public profile by username: display name, bio,
        subscriber count, and recent public content.

        Price: $0.0011 per request.

        Example:
            res = client.snapchat.profile(username="nasa")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "snapchat.profile", dict(input), options
        )
        return RunResult[SnapchatProfileData].model_validate(raw)


class AsyncSnapchatNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SnapchatProfileInput],
    ) -> RunResult[SnapchatProfileData]:
        """Snapchat Profile

        Fetch a Snapchat user's public profile by username: display name, bio,
        subscriber count, and recent public content.

        Price: $0.0011 per request.

        Example:
            res = client.snapchat.profile(username="nasa")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "snapchat.profile", dict(input), options
        )
        return RunResult[SnapchatProfileData].model_validate(raw)
