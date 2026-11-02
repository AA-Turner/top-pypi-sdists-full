# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the social platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SocialFinderInput(TypedDict, total=False):
    """Input for Social Profile Finder."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-10, default 10). You are billed per result returned, so a lower limit costs less. Range: 1 to 10."""
    name: Required[str]
    """The profile name or handle to search for across social networks (e.g. johndoe)."""
    platform: NotRequired[str]
    """Limit the search to one network: askfm, discord, facebook, github, instagram, linkedin, medium, pinterest, steam, threads, tiktok, twitch, or youtube (e.g. instagram); all networks are searched when omitted."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SocialFinderData(BaseModel):
    items: list[SocialFinderItem] = Field(
        description="Profile match records: the queried profile name, the social network, and the matching profile URL when one was found. Populated whenever the provider has data for the entity."
    )


class SocialFinderItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    input_profile_name: str | None = Field(
        default=None,
        alias="inputProfileName",
        description="The name that was searched for. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    social: str | None = Field(
        description="The social network checked (e.g. discord, facebook, github). Populated whenever the provider has data for the entity."
    )
    social_profile_url: str | None = Field(
        alias="socialProfileUrl",
        description="URL of the matching profile, or null when no account was found on that network.",
    )


class SocialNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def finder(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SocialFinderInput],
    ) -> RunResult[SocialFinderData]:
        """Social Profile Finder

        Find a person's or brand's profiles across major social networks from a
        single name, returned as normalized JSON.

        Price: $0.0011 per request plus $0.0022 per result (maximum $0.0231).

        Example:
            res = client.social.finder(limit=3, name="Elon Musk")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "social.finder", dict(input), options
        )
        return RunResult[SocialFinderData].model_validate(raw)


class AsyncSocialNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def finder(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SocialFinderInput],
    ) -> RunResult[SocialFinderData]:
        """Social Profile Finder

        Find a person's or brand's profiles across major social networks from a
        single name, returned as normalized JSON.

        Price: $0.0011 per request plus $0.0022 per result (maximum $0.0231).

        Example:
            res = client.social.finder(limit=3, name="Elon Musk")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "social.finder", dict(input), options
        )
        return RunResult[SocialFinderData].model_validate(raw)
