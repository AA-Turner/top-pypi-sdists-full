# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "DomainVerifyResponse",
    "Domain",
    "DomainDNSRecord",
    "Verification",
    "VerificationDebug",
    "VerificationDNS",
    "VerificationDNSDmarc",
    "VerificationDNSMailFrom",
    "VerificationDNSMx",
    "VerificationDNSMxRecord",
    "VerificationMxConflict",
    "VerificationMxConflictConflictingRecord",
]


class DomainDNSRecord(BaseModel):
    name: str

    type: Literal["TXT", "CNAME", "MX"]

    value: str

    is_verified: Optional[bool] = FieldInfo(alias="isVerified", default=None)

    last_checked_at: Optional[str] = FieldInfo(alias="lastCheckedAt", default=None)

    priority: Optional[float] = None

    verification_status: Optional[Literal["verified", "missing", "pending"]] = FieldInfo(
        alias="verificationStatus", default=None
    )


class Domain(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    domain: str

    is_managed_default: bool = FieldInfo(alias="isManagedDefault")

    status: Literal["VERIFIED", "PENDING_VERIFICATION", "NOT_REGISTERED"]

    updated_at: str = FieldInfo(alias="updatedAt")

    verified_at: Optional[str] = FieldInfo(alias="verifiedAt", default=None)

    dns_records: Optional[List[DomainDNSRecord]] = FieldInfo(alias="dnsRecords", default=None)


class VerificationDebug(BaseModel):
    actual_verification_tokens: List[str] = FieldInfo(alias="actualVerificationTokens")

    domain: str

    verification_token_match: bool = FieldInfo(alias="verificationTokenMatch")

    expected_verification_token: Optional[str] = FieldInfo(alias="expectedVerificationToken", default=None)


class VerificationDNSDmarc(BaseModel):
    present: bool

    source: Literal["subdomain", "parent", "none"]


class VerificationDNSMailFrom(BaseModel):
    domain: str

    mx: bool

    spf: bool


class VerificationDNSMxRecord(BaseModel):
    exchange: str

    priority: float


class VerificationDNSMx(BaseModel):
    expected_priority: float = FieldInfo(alias="expectedPriority")

    found: bool

    records: List[VerificationDNSMxRecord]


class VerificationDNS(BaseModel):
    dkim: Dict[str, bool]

    dmarc: VerificationDNSDmarc

    domain_verification: bool = FieldInfo(alias="domainVerification")

    mail_from: VerificationDNSMailFrom = FieldInfo(alias="mailFrom")

    mx: VerificationDNSMx

    spf: bool


class VerificationMxConflictConflictingRecord(BaseModel):
    exchange: str

    priority: float


class VerificationMxConflict(BaseModel):
    has_conflict: bool = FieldInfo(alias="hasConflict")

    conflicting_records: Optional[List[VerificationMxConflictConflictingRecord]] = FieldInfo(
        alias="conflictingRecords", default=None
    )

    message: Optional[str] = None


class Verification(BaseModel):
    debug: VerificationDebug

    dkim_status: Literal["Pending", "Success", "Failed", "NotStarted", "TemporaryFailure"] = FieldInfo(
        alias="dkimStatus"
    )

    dns: VerificationDNS

    mx_conflict: VerificationMxConflict = FieldInfo(alias="mxConflict")

    ready: bool

    verification: Literal["Pending", "Success", "Failed", "NotStarted", "TemporaryFailure"]


class DomainVerifyResponse(BaseModel):
    domain: Domain

    verification: Verification
