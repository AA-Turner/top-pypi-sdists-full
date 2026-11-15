# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the person platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class PersonSkipTraceInput(TypedDict, total=False):
    """Input for Skip Trace."""

    address: NotRequired[str]
    """Street address with city/state/zip."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: NotRequired[str]
    """Email address to reverse-trace (e.g. john.smith@example.com)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    name: NotRequired[str]
    """Full name of the person to trace. Provide at least one of name, address, phone, or email."""
    phone: NotRequired[str]
    """Phone number to reverse-trace (e.g. 415-555-2671)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PersonSkipTraceData(BaseModel):
    items: list[PersonSkipTraceItem] = Field(
        description="Matched person records with identity, address, and contact details. Populated whenever the provider has data for the entity."
    )


class PersonSkipTraceItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address_locality: str | None = Field(
        default=None, alias="addressLocality", description="Current city."
    )
    address_region: str | None = Field(
        default=None, alias="addressRegion", description="Current state."
    )
    age: str | None = Field(default=None, description="Reported age.")
    associates: list[PersonSkipTraceAssociate] | None = Field(
        default=None,
        description="Reported associates. Each entry is an open object with name and age.",
    )
    born: str | None = Field(default=None, description="Reported birth month and year.")
    county: str | None = Field(default=None, description="Current county.")
    emails: PersonSkipTraceEmail | None = Field(
        default=None,
        description="Up to five known email addresses, most-recent first. Absent slots are empty strings.",
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="First name of the matched person."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Last name of the matched person."
    )
    location: str | None = Field(
        default=None, description="Current city and state (e.g. Brook Park, OH)."
    )
    phones: PersonSkipTracePhone | None = Field(
        default=None,
        description="Up to five known phone numbers with line type, most-recent first. Absent slots are empty strings.",
    )
    postal_code: str | None = Field(
        default=None, alias="postalCode", description="Current ZIP code."
    )
    previous_addresses: list[PersonSkipTracePreviousAddresse] | None = Field(
        default=None,
        alias="previousAddresses",
        description="Prior addresses. Each entry is an open object with street, locality, region, postal code, county, and timespan.",
    )
    relatives: list[PersonSkipTraceRelative] | None = Field(
        default=None,
        description="Reported relatives. Each entry is an open object with name and age.",
    )
    street_address: str | None = Field(
        default=None, alias="streetAddress", description="Current street address."
    )
    url: str | None = Field(
        description="Source record URL for the matched person. Populated whenever the provider has data for the entity."
    )


class PersonSkipTraceAssociate(BaseModel):
    model_config = ConfigDict(extra="allow")


class PersonSkipTraceEmail(BaseModel):
    model_config = ConfigDict(extra="allow")

    email1: str | None = None
    email2: str | None = None
    email3: str | None = None
    email4: str | None = None
    email5: str | None = None


class PersonSkipTracePhone(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    phone1: str | None = None
    phone1_type: str | None = Field(default=None, alias="phone1Type")
    phone2: str | None = None
    phone2_type: str | None = Field(default=None, alias="phone2Type")
    phone3: str | None = None
    phone3_type: str | None = Field(default=None, alias="phone3Type")
    phone4: str | None = None
    phone4_type: str | None = Field(default=None, alias="phone4Type")
    phone5: str | None = None
    phone5_type: str | None = Field(default=None, alias="phone5Type")


class PersonSkipTracePreviousAddresse(BaseModel):
    model_config = ConfigDict(extra="allow")


class PersonSkipTraceRelative(BaseModel):
    model_config = ConfigDict(extra="allow")


class PersonNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def skip_trace(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PersonSkipTraceInput],
    ) -> RunResult[PersonSkipTraceData]:
        """Skip Trace

        Skip-trace a person in the US by name, address, phone, or email and get back
        identity, address, and contact records in normalized JSON.

        Price: $0 per request plus $0.0077 per result (maximum $0.0077).

        Example:
            res = client.person.skip_trace(address="123 Main St, Austin, TX 78701", name="John Smith")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "person.skip_trace", dict(input), options
        )
        return RunResult[PersonSkipTraceData].model_validate(raw)


class AsyncPersonNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def skip_trace(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PersonSkipTraceInput],
    ) -> RunResult[PersonSkipTraceData]:
        """Skip Trace

        Skip-trace a person in the US by name, address, phone, or email and get back
        identity, address, and contact records in normalized JSON.

        Price: $0 per request plus $0.0077 per result (maximum $0.0077).

        Example:
            res = client.person.skip_trace(address="123 Main St, Austin, TX 78701", name="John Smith")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "person.skip_trace", dict(input), options
        )
        return RunResult[PersonSkipTraceData].model_validate(raw)
