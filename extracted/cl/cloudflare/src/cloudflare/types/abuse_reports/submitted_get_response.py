# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SubmittedGetResponse", "RegWhoRequest", "Submitter"]


class RegWhoRequest(BaseModel):
    """RDP-mandated fields for registrar WHOIS data disclosure requests."""

    reg_who_good_faith_affirmation: bool
    """Affirmation that the request is made in good faith per RDP 10.2.4.

    Must be true.
    """

    reg_who_lawful_processing_agreement: bool
    """Agreement to process data lawfully per RDP 10.2.5. Must be true."""

    reg_who_legal_basis: str
    """Legal rights and rationale for the request per RDP 10.2.3.

    Required for all WHOIS requests.
    """

    reg_who_request_type: Literal["disclosure", "invalid_whois"]
    """The type of WHOIS data request per RDP procedure."""

    reg_who_requested_data_elements: List[
        Literal[
            "registrant_name",
            "registrant_organization",
            "registrant_email",
            "registrant_phone",
            "registrant_address",
            "registrant_address_country",
            "registrant_address_postal_code",
            "admin_name",
            "admin_organization",
            "admin_email",
            "admin_phone",
            "admin_address",
            "tech_name",
            "tech_organization",
            "tech_email",
            "tech_phone",
            "tech_address",
        ]
    ]
    """The specific WHOIS data elements being requested per RDP 10.2.2.

    Required for all WHOIS requests.
    """

    reg_who_authorization_statement: Optional[str] = None
    """Optional authorization statement or power of attorney per RDP 10.2.1.3."""

    reg_who_requestor_type: Optional[Literal["government", "corporation", "individual"]] = None
    """The nature of the requestor per RDP 10.2.1.2."""


class Submitter(BaseModel):
    """Information about the submitter of the report."""

    company: Optional[str] = None

    email: Optional[str] = None

    name: Optional[str] = None

    telephone: Optional[str] = None


class SubmittedGetResponse(BaseModel):
    id: str
    """Public report code."""

    cdate: datetime
    """Time the report was submitted."""

    denial_reason: Optional[
        Literal[
            "unable_to_confirm",
            "incomplete_report",
            "not_on_cloudflare",
            "duplicate_report",
            "content_removed",
            "report_details_mismatch",
            "no_abuse_found",
            "missing_original_work",
            "direct_url_required",
            "wrong_report_category",
            "content_unavailable",
            "law_enforcement_referral_required",
            "domain_dispute_process_required",
        ]
    ] = None
    """Submitter-safe reason for a denied report. Null when unavailable."""

    domain: str
    """Domain identified in the report."""

    dsa_attestation: bool
    """Whether the submitter provided the Digital Services Act attestation."""

    status: Literal["submitted", "accepted", "denied"]
    """Status visible to the account that submitted the report."""

    type: Literal["PHISH", "GEN", "THREAT", "DMCA", "EMER", "TM", "REG_WHO", "NCSEI", "NETWORK"]
    """The abuse report type"""

    urls: List[str]
    """URLs supplied with the report."""

    agent_name: Optional[str] = None
    """Authorized agent name supplied with the report."""

    comments: Optional[str] = None
    """Additional comments supplied with the report."""

    court: Optional[str] = None
    """
    The string "on" when a court proceeding applies to the report; otherwise
    omitted.
    """

    destination_ips: Optional[List[str]] = None
    """Destination IP addresses supplied with a network abuse report."""

    host_notification: Optional[str] = None
    """Submitter preference for notifying the hosting provider."""

    justification: Optional[str] = None
    """Evidence supplied with the report."""

    ncmec_notification: Optional[str] = None
    """Submitter preference for notifying NCMEC."""

    ncsei_subject_representation: Optional[bool] = None
    """Representation supplied for an NCSEI report."""

    original_work: Optional[str] = None
    """Original work or targeted brand supplied with the report."""

    owner_notification: Optional[str] = None
    """Submitter preference for notifying the content owner."""

    ports_protocols: Optional[List[str]] = None
    """Ports and protocols supplied with a network abuse report."""

    reg_who_request: Optional[RegWhoRequest] = None
    """RDP-mandated fields for registrar WHOIS data disclosure requests."""

    reported_country: Optional[str] = None
    """Country associated with the reported activity."""

    reported_user_agent: Optional[str] = None
    """User agent associated with the reported activity."""

    source_ips: Optional[List[str]] = None
    """Source IP addresses supplied with a network abuse report."""

    submitter: Optional[Submitter] = None
    """Information about the submitter of the report."""

    subtypes: Optional[List[str]] = None
    """Additional abuse classifications supplied with the report."""

    title: Optional[str] = None
    """Title supplied with the report."""

    udrp: Optional[str] = None
    """
    The string "on" when a UDRP proceeding applies to the report; otherwise omitted.
    """

    urs: Optional[str] = None
    """The string "on" when a URS proceeding applies to the report; otherwise omitted."""
