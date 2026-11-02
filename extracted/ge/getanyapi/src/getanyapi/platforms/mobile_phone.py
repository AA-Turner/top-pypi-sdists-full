# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the mobile_phone platform."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class MobilePhoneAiArkInput(TypedDict, total=False):
    """Input for Mobile Phone - AI Ark."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: NotRequired[str]
    """Person's company domain."""
    fullName: NotRequired[str]
    """Person's full name."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    linkedinUrl: NotRequired[str]
    """Person's LinkedIn profile URL."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class MobilePhoneLeadmagicInput(TypedDict, total=False):
    """Input for Mobile Phone - LeadMagic."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: NotRequired[str]
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    personalEmail: NotRequired[str]
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    profileUrl: NotRequired[str]
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    workEmail: NotRequired[str]


class MobilePhoneAiArkData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="Canonical LinkedIn profile URL returned with the match.",
    )
    phone: str | None = Field(description="Matched mobile phone number.")
    phone_groups: Any | None = Field(
        default=None,
        alias="phoneGroups",
        description="Every phone group the source returned, in source order: an array of groups where each group is an array of numbers. Untyped passthrough, because the source may return more than one group and this field carries all of them unchanged rather than reshaping them. The phone and phones fields are the first number and the first group of this same structure.",
    )
    phones: list[str] | None = Field(
        default=None,
        description="Every mobile phone number returned for the match, in source order. The first entry is the same value as phone.",
    )
    record_id: str | None = Field(
        default=None,
        alias="recordId",
        description="The source's own record identifier for this match, exposed so you can trace a result back to the record it came from.",
    )


class MobilePhoneLeadmagicData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    message: str | None = Field(
        default=None, description="Source's own description of the match outcome."
    )
    mobile: str | None = Field(description="Matched mobile phone number.")
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="Canonical profile URL the match was resolved against.",
    )


class MobilePhoneNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ai_ark(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MobilePhoneAiArkInput],
    ) -> RunResult[MobilePhoneAiArkData]:
        """Mobile Phone - AI Ark

        Find a person's mobile phone from a LinkedIn URL or from a domain and full
        name.

        Price: $0.084 per request.

        Example:
            res = client.mobile_phone.ai_ark(linkedinUrl="https://www.linkedin.com/in/tim-zheng")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "mobile_phone.ai_ark", dict(input), options
        )
        return RunResult[MobilePhoneAiArkData].model_validate(raw)

    def leadmagic(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MobilePhoneLeadmagicInput],
    ) -> RunResult[MobilePhoneLeadmagicData]:
        """Mobile Phone - LeadMagic

        Find a person's mobile phone from a profile URL or email. A no-match answer
        is a successful, billable result.

        Price: $0.2016 per request.

        Example:
            res = client.mobile_phone.leadmagic(profileUrl="https://www.linkedin.com/in/tim-zheng")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "mobile_phone.leadmagic", dict(input), options
        )
        return RunResult[MobilePhoneLeadmagicData].model_validate(raw)


class AsyncMobilePhoneNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ai_ark(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MobilePhoneAiArkInput],
    ) -> RunResult[MobilePhoneAiArkData]:
        """Mobile Phone - AI Ark

        Find a person's mobile phone from a LinkedIn URL or from a domain and full
        name.

        Price: $0.084 per request.

        Example:
            res = client.mobile_phone.ai_ark(linkedinUrl="https://www.linkedin.com/in/tim-zheng")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "mobile_phone.ai_ark", dict(input), options
        )
        return RunResult[MobilePhoneAiArkData].model_validate(raw)

    async def leadmagic(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[MobilePhoneLeadmagicInput],
    ) -> RunResult[MobilePhoneLeadmagicData]:
        """Mobile Phone - LeadMagic

        Find a person's mobile phone from a profile URL or email. A no-match answer
        is a successful, billable result.

        Price: $0.2016 per request.

        Example:
            res = client.mobile_phone.leadmagic(profileUrl="https://www.linkedin.com/in/tim-zheng")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "mobile_phone.leadmagic", dict(input), options
        )
        return RunResult[MobilePhoneLeadmagicData].model_validate(raw)
