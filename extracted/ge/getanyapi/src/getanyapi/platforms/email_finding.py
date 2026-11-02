# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the email_finding platform."""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class EmailFindingDropleadsInput(TypedDict, total=False):
    """Input for Email Finding - DropLeads."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: NotRequired[str]
    """Company domain without a path."""
    companyName: NotRequired[str]
    """Company name when the domain is unavailable."""
    firstName: Required[str]
    """Person's first name."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lastName: Required[str]
    """Person's last name."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailFindingHunterCountInput(TypedDict, total=False):
    """Input for Email Finding - Hunter Email Count."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: Required[str]
    """Company domain without a scheme or path, e.g. stripe.com."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    type: NotRequired[Literal["personal", "generic"]]
    """Count only personal mailboxes belonging to a named person, or only generic ones such as info@ and support@."""


class EmailFindingHunterDomainInput(TypedDict, total=False):
    """Input for Email Finding - Hunter Domain Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    department: NotRequired[
        Literal[
            "executive",
            "it",
            "finance",
            "management",
            "sales",
            "legal",
            "support",
            "hr",
            "marketing",
            "communication",
            "education",
            "design",
            "health",
            "operations",
        ]
    ]
    """Restrict to one department."""
    domain: Required[str]
    """Company domain without a scheme or path, e.g. stripe.com."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    jobTitle: NotRequired[str]
    """One job-title keyword to match, e.g. editor. A single keyword only: a comma-separated list is not supported and only its last entry would apply."""
    limit: NotRequired[int]
    """Maximum contacts to return in this response. Every returned contact is billed, so this is the cost control. Range: 1 to 100. Default: 3."""
    offset: NotRequired[int]
    """Number of contacts to skip before this page begins. Minimum: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requiredField: NotRequired[Literal["full_name", "position", "phone_number"]]
    """Only return contacts that carry this field."""
    seniority: NotRequired[Literal["junior", "senior", "executive"]]
    """Restrict to one seniority level."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    type: NotRequired[Literal["personal", "generic"]]
    """Restrict to personal mailboxes belonging to a named person, or to generic ones such as info@ and support@."""


class EmailFindingIcypeasInput(TypedDict, total=False):
    """Input for Email Finding - Icypeas."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domainOrCompany: Required[str]
    firstname: NotRequired[str]
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lastname: NotRequired[str]
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailFindingQuickenrichInput(TypedDict, total=False):
    """Input for Email Finding - QuickEnrich."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: NotRequired[str]
    """Company website domain, normalized upstream (example.com or https://example.com both work)."""
    firstName: NotRequired[str]
    """Person's first name."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lastName: NotRequired[str]
    """Person's last name."""
    linkedinUrl: NotRequired[str]
    """LinkedIn profile URL. Provide this, or companyDomain with firstName and lastName."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailFindingZerobounceInput(TypedDict, total=False):
    """Input for Email Finding - ZeroBounce."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: Required[str]
    """Company domain to search, e.g. hubspot.com."""
    firstName: NotRequired[str]
    """First name of the person to find."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    lastName: NotRequired[str]
    """Last name of the person to find."""
    middleName: NotRequired[str]
    """Middle name, when the company's address format uses one."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailFindingZerobounceDomainInput(TypedDict, total=False):
    """Input for Email Pattern - ZeroBounce."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    domain: Required[str]
    """Company domain to inspect, e.g. hubspot.com."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailFindingDropleadsData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Matched company domain."
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Matched company name."
    )
    company_size: Any | None = Field(
        default=None, alias="companySize", description="Company size when available."
    )
    email: str | None = Field(description="Matched email address.")
    first_name: str | None = Field(
        default=None, alias="firstName", description="Matched first name."
    )
    industry: str | None = Field(
        default=None, description="Company industry when available."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Matched last name."
    )
    mx_provider: str | None = Field(
        default=None, alias="mxProvider", description="Detected mail provider."
    )
    mx_record: str | None = Field(
        default=None, alias="mxRecord", description="Selected mail exchange record."
    )
    status: str | None = Field(
        description="Source validation status for the matched email."
    )


class EmailFindingHunterCountData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    department_counts: EmailFindingHunterCountDepartmentCount | None = Field(
        default=None, alias="departmentCounts", description="Contacts per department."
    )
    domain: str | None = Field(description="The company domain the counts describe.")
    generic_emails: int | None = Field(
        default=None,
        alias="genericEmails",
        description="Contacts that are a shared inbox such as info@ or support@. Minimum: 0.",
    )
    personal_emails: int | None = Field(
        default=None,
        alias="personalEmails",
        description="Contacts that are a named person's mailbox. Minimum: 0.",
    )
    seniority_counts: EmailFindingHunterCountSeniorityCount | None = Field(
        default=None,
        alias="seniorityCounts",
        description="Contacts per seniority level.",
    )
    total: int | None = Field(description="Contacts known for the domain. Minimum: 0.")
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Mailbox type the counts are limited to when the request filtered by type: personal or generic. Absent when the counts cover both.",
    )


class EmailFindingHunterCountDepartmentCount(BaseModel):
    model_config = ConfigDict(extra="allow")

    administrative: int | None = Field(
        default=None,
        description="Contacts in the administrative department. Minimum: 0.",
    )
    communication: int | None = Field(
        default=None,
        description="Contacts in the communication department. Minimum: 0.",
    )
    consulting: int | None = Field(
        default=None, description="Contacts in the consulting department. Minimum: 0."
    )
    design: int | None = Field(
        default=None, description="Contacts in the design department. Minimum: 0."
    )
    education: int | None = Field(
        default=None, description="Contacts in the education department. Minimum: 0."
    )
    executive: int | None = Field(
        default=None, description="Contacts in the executive department. Minimum: 0."
    )
    finance: int | None = Field(
        default=None, description="Contacts in the finance department. Minimum: 0."
    )
    health: int | None = Field(
        default=None, description="Contacts in the health department. Minimum: 0."
    )
    hr: int | None = Field(
        default=None, description="Contacts in the HR department. Minimum: 0."
    )
    it: int | None = Field(
        default=None, description="Contacts in the IT department. Minimum: 0."
    )
    legal: int | None = Field(
        default=None, description="Contacts in the legal department. Minimum: 0."
    )
    management: int | None = Field(
        default=None, description="Contacts in the management department. Minimum: 0."
    )
    marketing: int | None = Field(
        default=None, description="Contacts in the marketing department. Minimum: 0."
    )
    operation: int | None = Field(
        default=None,
        description="Contacts Hunter files under its separate operation department. Minimum: 0.",
    )
    operations: int | None = Field(
        default=None, description="Contacts in the operations department. Minimum: 0."
    )
    procurement: int | None = Field(
        default=None, description="Contacts in the procurement department. Minimum: 0."
    )
    product: int | None = Field(
        default=None, description="Contacts in the product department. Minimum: 0."
    )
    research: int | None = Field(
        default=None, description="Contacts in the research department. Minimum: 0."
    )
    sales: int | None = Field(
        default=None, description="Contacts in the sales department. Minimum: 0."
    )
    support: int | None = Field(
        default=None, description="Contacts in the support department. Minimum: 0."
    )


class EmailFindingHunterCountSeniorityCount(BaseModel):
    model_config = ConfigDict(extra="allow")

    executive: int | None = Field(
        default=None, description="Contacts at executive level. Minimum: 0."
    )
    junior: int | None = Field(
        default=None, description="Contacts at junior level. Minimum: 0."
    )
    senior: int | None = Field(
        default=None, description="Contacts at senior level. Minimum: 0."
    )


class EmailFindingHunterDomainData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    accept_all: bool | None = Field(
        default=None,
        alias="acceptAll",
        description="True when the mail server accepts any address at this domain, so an address cannot be verified by delivery.",
    )
    disposable: bool | None = Field(
        default=None,
        description="True when the domain belongs to a disposable-email service.",
    )
    domain: str = Field(description="The company domain the contacts belong to.")
    email_pattern: str | None = Field(
        default=None,
        alias="emailPattern",
        description="Address pattern the company uses, e.g. {first}{last}.",
    )
    emails: list[EmailFindingHunterDomainEmail] = Field(
        description="Contacts returned by this page, one per billed result."
    )
    linked_domains: Any | None = Field(
        default=None,
        alias="linkedDomains",
        description="Other domains Hunter has linked to this company. Deliberately untyped: the field is empty in every response we have captured, so the value passes through without a shape guarantee.",
    )
    organization: str | None = Field(
        default=None, description="Company name registered against the domain."
    )
    total_count: int = Field(
        alias="totalCount",
        description="Contacts matching the filters across the whole domain, of which this response returns at most limit. Minimum: 0.",
    )
    webmail: bool | None = Field(
        default=None,
        description="True when the domain is a webmail provider rather than a company.",
    )


class EmailFindingHunterDomainEmail(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    confidence: int | None = Field(
        default=None,
        description="Upstream confidence in the address, 0 to 100. Range: 0 to 100.",
    )
    decision_maker: bool | None = Field(
        default=None,
        alias="decisionMaker",
        description="True when the contact is judged a decision maker.",
    )
    department: str | None = Field(
        default=None, description="Department the contact works in."
    )
    email: str | None = Field(description="The work email address.")
    first_name: str | None = Field(
        default=None, alias="firstName", description="Contact's first name."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Contact's last name."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Contact's LinkedIn profile URL."
    )
    phone: str | None = Field(default=None, description="Contact's phone number.")
    position: str | None = Field(default=None, description="Contact's job title.")
    position_raw: str | None = Field(
        default=None,
        alias="positionRaw",
        description="Contact's job title exactly as written on the source page, before it was cleaned up.",
    )
    seniority: str | None = Field(
        default=None, description="Seniority level: junior, senior or executive."
    )
    source_type: str | None = Field(
        default=None,
        alias="sourceType",
        description="How the address was obtained: found when it was seen on a public page, generated when it was inferred from the company's address pattern.",
    )
    sources: list[EmailFindingHunterDomainSource] | None = Field(
        default=None, description="Public pages the address was found on."
    )
    twitter: str | None = Field(
        default=None,
        description="Contact's Twitter/X handle or profile URL, exactly as the source recorded it.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description="personal for a named person's mailbox, generic for a shared inbox.",
    )
    verification_status: str | None = Field(
        default=None,
        alias="verificationStatus",
        description="Deliverability verdict recorded for the address.",
    )
    verified_utc: float | None = Field(
        default=None,
        alias="verifiedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class EmailFindingHunterDomainSource(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    domain: str | None = Field(
        description="Domain of the page the address was found on."
    )
    extracted_utc: float | None = Field(
        default=None,
        alias="extractedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    last_seen_utc: float | None = Field(
        default=None,
        alias="lastSeenUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    still_on_page: bool | None = Field(
        default=None,
        alias="stillOnPage",
        description="True when the address was still present at the last check.",
    )
    url: str | None = Field(
        default=None, description="URL of the page the address was found on."
    )


class EmailFindingIcypeasData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    certainty: str | None = Field(
        default=None,
        description="Confidence label for the best matching address, e.g. ultra_sure.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    email: str | None = Field(description="Best matching email address.")
    emails: list[EmailFindingIcypeasEmail] | None = Field(
        default=None,
        description="Every candidate address found for the person, best first. The top-level email is the first entry.",
    )
    firstname: str | None = Field(default=None, description="Matched first name.")
    fullname: str | None = Field(default=None, description="Matched full name.")
    gender: str | None = Field(
        default=None,
        description="Gender recorded for the matched person. Absent when the source does not know it.",
    )
    lastname: str | None = Field(default=None, description="Matched last name.")
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="LinkedIn profile URL for the matched person, when the source has one.",
    )
    modified_utc: float | None = Field(
        default=None,
        alias="modifiedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider behind the domain, e.g. google.",
    )
    mx_records: list[str] | None = Field(
        default=None,
        alias="mxRecords",
        description="Mail exchange records for the domain.",
    )
    phones: Any | None = Field(
        default=None,
        description="Phone numbers Icypeas returned alongside the address. Deliberately untyped: the field is empty in every response we have captured, so the value passes through without a shape guarantee.",
    )
    saas_services: Any | None = Field(
        default=None,
        alias="saasServices",
        description="SaaS services Icypeas associates with the person. Deliberately untyped: the field is empty in every response we have captured, so the value passes through without a shape guarantee.",
    )
    scan_id: str | None = Field(
        default=None,
        alias="scanId",
        description="Icypeas' identifier for the search that produced this result.",
    )
    scan_name: str | None = Field(
        default=None,
        alias="scanName",
        description="Icypeas' internal label for the kind of search that ran, e.g. __icypeas__individual.",
    )
    scan_order: int | None = Field(
        default=None,
        alias="scanOrder",
        description="Position of this result inside the Icypeas search batch. It is 0 for the single-person search this SKU runs.",
    )
    scan_status: str | None = Field(
        default=None,
        alias="scanStatus",
        description="Icypeas' terminal status for the search, FOUND or NOT_FOUND. It duplicates the envelope's found flag.",
    )
    scan_user: str | None = Field(
        default=None,
        alias="scanUser",
        description="Icypeas account that ran the search.",
    )


class EmailFindingIcypeasEmail(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    certainty: str | None = Field(
        default=None, description="Confidence label for this address, e.g. ultra_sure."
    )
    email: str | None = Field(default=None, description="Candidate email address.")
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider behind this address's domain.",
    )
    mx_records: list[str] | None = Field(
        default=None,
        alias="mxRecords",
        description="Mail exchange records for this address's domain.",
    )


class EmailFindingQuickenrichData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(
        default=None, description="Street address on the employer record."
    )
    city: str | None = Field(default=None, description="City on the employer record.")
    company_domain: str | None = Field(
        default=None, alias="companyDomain", description="Employer website domain."
    )
    company_employee_count: str | None = Field(
        default=None,
        alias="companyEmployeeCount",
        description='Employer headcount band, e.g. "20 - 99". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    company_industry: str | None = Field(
        default=None, alias="companyIndustry", description="Employer industry label."
    )
    company_linkedin_url: str | None = Field(
        default=None,
        alias="companyLinkedinUrl",
        description="Employer LinkedIn company URL.",
    )
    company_name: str | None = Field(
        default=None, alias="companyName", description="Employer name."
    )
    company_phone: str | None = Field(
        default=None, alias="companyPhone", description="Employer main phone line."
    )
    company_revenue: str | None = Field(
        default=None,
        alias="companyRevenue",
        description='Employer revenue band, e.g. "1 - 2.5 Million". Upstream band vocabulary; "Not Available" means the band is unknown.',
    )
    country: str | None = Field(
        default=None,
        description="ISO 3166-1 alpha-2 country code on the employer record.",
    )
    email: str | None = Field(description="Work email address.")
    email_domain: str | None = Field(
        default=None,
        alias="emailDomain",
        description="Domain the work email resolves to.",
    )
    email_verified_utc: float | None = Field(
        default=None,
        alias="emailVerifiedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    first_name: str | None = Field(
        default=None, alias="firstName", description="Person's first name."
    )
    last_name: str | None = Field(
        default=None, alias="lastName", description="Person's last name."
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="Person's LinkedIn profile URL."
    )
    phone: str | None = Field(
        default=None,
        description="Direct business phone line held for the person. Mostly desk lines; read phoneType before treating it as a mobile.",
    )
    phone_type: str | None = Field(
        default=None,
        alias="phoneType",
        description='Line type reported upstream, e.g. "mobile" or "landline".',
    )
    postal_code: str | None = Field(
        default=None,
        alias="postalCode",
        description="Postal code on the employer record.",
    )
    region: str | None = Field(
        default=None, description="State or region code on the employer record."
    )
    title: str | None = Field(default=None, description="Person's job title.")


class EmailFindingZerobounceData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Company ZeroBounce associates with the domain.",
    )
    confidence: str | None = Field(
        default=None,
        description="ZeroBounce's confidence in the address: high, medium, low or undetermined.",
    )
    did_you_mean: str | None = Field(
        default=None,
        alias="didYouMean",
        description="Corrected domain when ZeroBounce spots a likely typo.",
    )
    domain: str | None = Field(
        default=None, description="Domain the address belongs to."
    )
    email: str | None = Field(description="The email address ZeroBounce found.")
    failure_reason: str | None = Field(
        default=None,
        alias="failureReason",
        description="Why ZeroBounce could not answer with more confidence.",
    )


class EmailFindingZerobounceDomainData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Company ZeroBounce associates with the domain.",
    )
    confidence: str | None = Field(
        default=None, description="Confidence in that format: high, medium or low."
    )
    did_you_mean: str | None = Field(
        default=None,
        alias="didYouMean",
        description="Corrected domain when ZeroBounce spots a likely typo.",
    )
    domain: str | None = Field(description="The domain that was inspected.")
    failure_reason: str | None = Field(
        default=None,
        alias="failureReason",
        description="Why ZeroBounce could not answer with more confidence.",
    )
    format: str | None = Field(
        description="The address format ZeroBounce is most confident the domain uses, e.g. first.last or flast."
    )
    other_formats: list[EmailFindingZerobounceDomainOtherFormat] | None = Field(
        default=None,
        alias="otherFormats",
        description="Every other address format ZeroBounce has seen on this domain, most confident first.",
    )


class EmailFindingZerobounceDomainOtherFormat(BaseModel):
    model_config = ConfigDict(extra="allow")

    confidence: str | None = Field(
        default=None, description="Confidence in that format: high, medium or low."
    )
    format: str | None = Field(description="Address format, e.g. last.first.")


class EmailFindingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def dropleads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingDropleadsInput],
    ) -> RunResult[EmailFindingDropleadsData]:
        """Email Finding - DropLeads

        Find a professional email from a person's name and company domain or company
        name.

        Price: $0.0312 per request.

        Example:
            res = client.email_finding.dropleads(companyDomain="apollo.io", firstName="Tim", lastName="Zheng")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.dropleads", dict(input), options
        )
        return RunResult[EmailFindingDropleadsData].model_validate(raw)

    def hunter_count(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingHunterCountInput],
    ) -> RunResult[EmailFindingHunterCountData]:
        """Email Finding - Hunter Email Count

        Count how many contacts a company domain has, split by personal and generic
        mailboxes and broken down by department and seniority. Scope a domain for $1
        per 1,000 requests before paying per contact.

        Price: $0.001 per request.

        Example:
            res = client.email_finding.hunter_count(domain="stripe.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.hunter_count", dict(input), options
        )
        return RunResult[EmailFindingHunterCountData].model_validate(raw)

    def hunter_domain(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingHunterDomainInput],
    ) -> RunResult[EmailFindingHunterDomainData]:
        """Email Finding - Hunter Domain Search

        Find named contacts and their work email addresses at a company domain,
        filtered by job title, seniority or department. Priced per returned contact,
        so limit is the cost control.

        Price: $0.025 per request.

        Example:
            res = client.email_finding.hunter_domain(domain="stripe.com", limit=2, type_="personal")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.hunter_domain", dict(input), options
        )
        return RunResult[EmailFindingHunterDomainData].model_validate(raw)

    def icypeas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingIcypeasInput],
    ) -> RunResult[EmailFindingIcypeasData]:
        """Email Finding - Icypeas

        Find a professional email from a person and company through the durable
        Request lifecycle.

        Price: $0.0168 per request.

        Example:
            res = client.email_finding.icypeas(domainOrCompany="apollo.io", firstname="Tim", lastname="Zheng")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.icypeas", dict(input), options
        )
        return RunResult[EmailFindingIcypeasData].model_validate(raw)

    def quickenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingQuickenrichInput],
    ) -> RunResult[EmailFindingQuickenrichData]:
        """Email Finding - QuickEnrich

        Find a work email from a LinkedIn profile, or from a company domain plus a
        name. Coverage is strongest for small and local businesses and thin for
        large technology employers.

        Price: $0.0072 per request.

        Example:
            res = client.email_finding.quickenrich(companyDomain="southmemphisfence.com", firstName="Warren", lastName="Price")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.quickenrich", dict(input), options
        )
        return RunResult[EmailFindingQuickenrichData].model_validate(raw)

    def zerobounce(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingZerobounceInput],
    ) -> RunResult[EmailFindingZerobounceData]:
        """Email Finding - ZeroBounce

        Find a person's work email at a company domain from their name, with
        ZeroBounce's confidence in the guess.

        Price: $0.6552 per request.

        Example:
            res = client.email_finding.zerobounce(domain="hubspot.com", firstName="Dharmesh", lastName="Shah")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.zerobounce", dict(input), options
        )
        return RunResult[EmailFindingZerobounceData].model_validate(raw)

    def zerobounce_domain(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingZerobounceDomainInput],
    ) -> RunResult[EmailFindingZerobounceDomainData]:
        """Email Pattern - ZeroBounce

        Read the email address format a company domain uses, with every alternative
        format ZeroBounce has seen and how confident it is in each. Use it to build
        addresses for a whole account at once.

        Price: $0.6552 per request.

        Example:
            res = client.email_finding.zerobounce_domain(domain="hubspot.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.zerobounce_domain", dict(input), options
        )
        return RunResult[EmailFindingZerobounceDomainData].model_validate(raw)


class AsyncEmailFindingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def dropleads(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingDropleadsInput],
    ) -> RunResult[EmailFindingDropleadsData]:
        """Email Finding - DropLeads

        Find a professional email from a person's name and company domain or company
        name.

        Price: $0.0312 per request.

        Example:
            res = client.email_finding.dropleads(companyDomain="apollo.io", firstName="Tim", lastName="Zheng")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.dropleads", dict(input), options
        )
        return RunResult[EmailFindingDropleadsData].model_validate(raw)

    async def hunter_count(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingHunterCountInput],
    ) -> RunResult[EmailFindingHunterCountData]:
        """Email Finding - Hunter Email Count

        Count how many contacts a company domain has, split by personal and generic
        mailboxes and broken down by department and seniority. Scope a domain for $1
        per 1,000 requests before paying per contact.

        Price: $0.001 per request.

        Example:
            res = client.email_finding.hunter_count(domain="stripe.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.hunter_count", dict(input), options
        )
        return RunResult[EmailFindingHunterCountData].model_validate(raw)

    async def hunter_domain(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingHunterDomainInput],
    ) -> RunResult[EmailFindingHunterDomainData]:
        """Email Finding - Hunter Domain Search

        Find named contacts and their work email addresses at a company domain,
        filtered by job title, seniority or department. Priced per returned contact,
        so limit is the cost control.

        Price: $0.025 per request.

        Example:
            res = client.email_finding.hunter_domain(domain="stripe.com", limit=2, type_="personal")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.hunter_domain", dict(input), options
        )
        return RunResult[EmailFindingHunterDomainData].model_validate(raw)

    async def icypeas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingIcypeasInput],
    ) -> RunResult[EmailFindingIcypeasData]:
        """Email Finding - Icypeas

        Find a professional email from a person and company through the durable
        Request lifecycle.

        Price: $0.0168 per request.

        Example:
            res = client.email_finding.icypeas(domainOrCompany="apollo.io", firstname="Tim", lastname="Zheng")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.icypeas", dict(input), options
        )
        return RunResult[EmailFindingIcypeasData].model_validate(raw)

    async def quickenrich(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingQuickenrichInput],
    ) -> RunResult[EmailFindingQuickenrichData]:
        """Email Finding - QuickEnrich

        Find a work email from a LinkedIn profile, or from a company domain plus a
        name. Coverage is strongest for small and local businesses and thin for
        large technology employers.

        Price: $0.0072 per request.

        Example:
            res = client.email_finding.quickenrich(companyDomain="southmemphisfence.com", firstName="Warren", lastName="Price")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.quickenrich", dict(input), options
        )
        return RunResult[EmailFindingQuickenrichData].model_validate(raw)

    async def zerobounce(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingZerobounceInput],
    ) -> RunResult[EmailFindingZerobounceData]:
        """Email Finding - ZeroBounce

        Find a person's work email at a company domain from their name, with
        ZeroBounce's confidence in the guess.

        Price: $0.6552 per request.

        Example:
            res = client.email_finding.zerobounce(domain="hubspot.com", firstName="Dharmesh", lastName="Shah")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.zerobounce", dict(input), options
        )
        return RunResult[EmailFindingZerobounceData].model_validate(raw)

    async def zerobounce_domain(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailFindingZerobounceDomainInput],
    ) -> RunResult[EmailFindingZerobounceDomainData]:
        """Email Pattern - ZeroBounce

        Read the email address format a company domain uses, with every alternative
        format ZeroBounce has seen and how confident it is in each. Use it to build
        addresses for a whole account at once.

        Price: $0.6552 per request.

        Example:
            res = client.email_finding.zerobounce_domain(domain="hubspot.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_finding.zerobounce_domain", dict(input), options
        )
        return RunResult[EmailFindingZerobounceDomainData].model_validate(raw)
