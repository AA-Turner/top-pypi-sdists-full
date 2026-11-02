# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the email platform."""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class EmailFindInput(TypedDict, total=False):
    """Input for Email Finder."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    person: NotRequired[dict[str, Any]]
    """The person to find an email for, e.g. {"firstName": "Jane", "surname": "Doe", "domain": "acme.com"} (domain also accepts a company name)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailVerifyInput(TypedDict, total=False):
    """Input for Email Verifier."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: Required[str]
    """The email address to verify (e.g. jane.doe@acme.com). Exactly one @, a dotted domain, no whitespace or angle brackets. Addresses on reserved, never-deliverable TLDs (.invalid, .test, .example, .localhost, .local, .internal, .blink) and HTML/JSON escape artifacts (a u003e prefix) are rejected locally with no charge."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["mxProvider", "reason"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `reason`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a result that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailFindData(BaseModel):
    items: list[EmailFindItem] = Field(
        description="Email lookup records: the discovered email address, verification status, and the matched person and company details. Populated whenever the provider has data for the entity."
    )


class EmailFindItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    email: str | None = Field(
        description="The discovered work email address. Populated whenever the provider has data for the entity."
    )
    status: str | None = Field(
        description='Lookup status. Always "found": a lookup that finds nothing returns found:false with a null data instead of an item, and is not charged. Populated whenever the provider has data for the entity.'
    )


class EmailVerifyData(BaseModel):
    items: list[EmailVerifyItem] = Field(
        description="Verification records: the email address with its deliverability verdict and the domain, mailbox, and reputation signals behind it. A record is returned for every syntactically valid address, including ones the verdict marks undeliverable. Populated whenever the provider has data for the entity."
    )


class EmailVerifyItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    catch_all: bool | None = Field(
        default=None, alias="catchAll", description="Domain accepts all addresses."
    )
    disposable: bool | None = None
    domain: str | None = None
    email: str | None = Field(
        description="Populated whenever the provider has data for the entity."
    )
    free: bool | None = Field(default=None, description="Free email provider.")
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider behind the address domain, e.g. Google. Null when the serving source does not report one.",
    )
    mx_records: list[str] | None = Field(
        default=None,
        alias="mxRecords",
        description="MX record hosts published by the address domain.",
    )
    reason: str | None = Field(
        default=None,
        description="Why the verdict was reached. Published by only one of the two sources, so it is absent on most calls; never treat it as required.",
    )
    role: bool | None = Field(
        default=None, description="Role-based address (e.g. info@)."
    )
    score: int | None = Field(
        default=None,
        description="Confidence in the verdict, 0-100. Coarse rather than graded on most calls: it tracks the status rather than ranking addresses within one.",
    )
    status: str | None = Field(
        description="Deliverability verdict: good (the mailbox accepted), bad (it was refused), or risky (no source could settle it - usually a catch-all domain that accepts every address, sometimes a receiving server that declined to answer at all). Populated whenever the provider has data for the entity."
    )


class EmailNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def find(
        self, *, options: RequestOptions | None = None, **input: Unpack[EmailFindInput]
    ) -> RunResult[EmailFindData]:
        """Email Finder

        Find a person's work email address from their name and company domain.

        Price: $0.0308 per request.

        Example:
            res = client.email.find(person={"domain": "google.com", "firstName": "Damien", "surname": "Neil"})
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email.find", dict(input), options
        )
        return RunResult[EmailFindData].model_validate(raw)

    def verify(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerifyInput],
    ) -> RunResult[EmailVerifyData]:
        """Email Verifier

        Verify an email address for deliverability: a status verdict (good, risky,
        or bad) with domain, mailbox, catch-all, disposable, and role signals plus a
        confidence score. Malformed addresses are rejected by the input schema with
        no charge; every syntactically valid address returns a billed verdict,
        including undeliverable ones.

        Price: $0.0066 per request.

        Example:
            res = client.email.verify(email="patrick@stripe.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email.verify", dict(input), options
        )
        return RunResult[EmailVerifyData].model_validate(raw)


class AsyncEmailNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def find(
        self, *, options: RequestOptions | None = None, **input: Unpack[EmailFindInput]
    ) -> RunResult[EmailFindData]:
        """Email Finder

        Find a person's work email address from their name and company domain.

        Price: $0.0308 per request.

        Example:
            res = client.email.find(person={"domain": "google.com", "firstName": "Damien", "surname": "Neil"})
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email.find", dict(input), options
        )
        return RunResult[EmailFindData].model_validate(raw)

    async def verify(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerifyInput],
    ) -> RunResult[EmailVerifyData]:
        """Email Verifier

        Verify an email address for deliverability: a status verdict (good, risky,
        or bad) with domain, mailbox, catch-all, disposable, and role signals plus a
        confidence score. Malformed addresses are rejected by the input schema with
        no charge; every syntactically valid address returns a billed verdict,
        including undeliverable ones.

        Price: $0.0066 per request.

        Example:
            res = client.email.verify(email="patrick@stripe.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email.verify", dict(input), options
        )
        return RunResult[EmailVerifyData].model_validate(raw)
