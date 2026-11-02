# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the contact_enrichment platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class ContactEnrichmentCrustdataV3Input(TypedDict, total=False):
    """Input for Contact Enrichment - Crustdata v3."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: NotRequired[str]
    """The person's business email address."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    linkedinUrl: NotRequired[str]
    """LinkedIn profile URL, e.g. https://www.linkedin.com/in/satyanadella. Send exactly one of linkedinUrl or email."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ContactEnrichmentCrustdataV3Data(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_emails: list[ContactEnrichmentCrustdataV3BusinessEmail] | None = Field(
        default=None, alias="businessEmails", description="Work email addresses."
    )
    match_confidence: float | None = Field(
        default=None,
        alias="matchConfidence",
        description="Confidence from 0 to 1 that the returned person is the one asked for.",
    )
    person_id: str | None = Field(alias="personId", description="Crustdata person id.")
    personal_emails: list[ContactEnrichmentCrustdataV3PersonalEmail] | None = Field(
        default=None, alias="personalEmails", description="Personal email addresses."
    )
    phone_numbers: list[str] | None = Field(
        default=None,
        alias="phoneNumbers",
        description="Phone numbers, as Crustdata stores them.",
    )


class ContactEnrichmentCrustdataV3BusinessEmail(BaseModel):
    model_config = ConfigDict(extra="allow")

    email: str | None = Field(description="Email address.")
    status: str | None = Field(
        default=None, description="Deliverability status, e.g. deliverable or unknown."
    )


class ContactEnrichmentCrustdataV3PersonalEmail(BaseModel):
    model_config = ConfigDict(extra="allow")

    email: str | None = Field(description="Email address.")
    status: str | None = Field(
        default=None, description="Deliverability status, e.g. deliverable or unknown."
    )


class ContactEnrichmentNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ContactEnrichmentCrustdataV3Input],
    ) -> RunResult[ContactEnrichmentCrustdataV3Data]:
        """Contact Enrichment - Crustdata v3

        Find one person's business emails, personal emails, and phone numbers from a
        LinkedIn profile URL or a business email, with a deliverability status on
        every email. Billed only when the person is found.

        Price: $0.24 per request.

        Example:
            res = client.contact_enrichment.crustdata_v3(linkedinUrl="https://www.linkedin.com/in/satyanadella")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "contact_enrichment.crustdata_v3", dict(input), options
        )
        return RunResult[ContactEnrichmentCrustdataV3Data].model_validate(raw)


class AsyncContactEnrichmentNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ContactEnrichmentCrustdataV3Input],
    ) -> RunResult[ContactEnrichmentCrustdataV3Data]:
        """Contact Enrichment - Crustdata v3

        Find one person's business emails, personal emails, and phone numbers from a
        LinkedIn profile URL or a business email, with a deliverability status on
        every email. Billed only when the person is found.

        Price: $0.24 per request.

        Example:
            res = client.contact_enrichment.crustdata_v3(linkedinUrl="https://www.linkedin.com/in/satyanadella")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "contact_enrichment.crustdata_v3", dict(input), options
        )
        return RunResult[ContactEnrichmentCrustdataV3Data].model_validate(raw)
