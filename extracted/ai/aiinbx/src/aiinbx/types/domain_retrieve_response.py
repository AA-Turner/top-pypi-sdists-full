# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DomainRetrieveResponse", "DNSRecord"]


class DNSRecord(BaseModel):
    name: str

    type: Literal["TXT", "CNAME", "MX"]

    value: str

    is_verified: Optional[bool] = FieldInfo(alias="isVerified", default=None)

    last_checked_at: Optional[str] = FieldInfo(alias="lastCheckedAt", default=None)

    priority: Optional[float] = None

    verification_status: Optional[Literal["verified", "missing", "pending"]] = FieldInfo(
        alias="verificationStatus", default=None
    )


class DomainRetrieveResponse(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    domain: str

    is_managed_default: bool = FieldInfo(alias="isManagedDefault")

    status: Literal["VERIFIED", "PENDING_VERIFICATION", "NOT_REGISTERED"]

    updated_at: str = FieldInfo(alias="updatedAt")

    verified_at: Optional[str] = FieldInfo(alias="verifiedAt", default=None)

    dns_records: Optional[List[DNSRecord]] = FieldInfo(alias="dnsRecords", default=None)
