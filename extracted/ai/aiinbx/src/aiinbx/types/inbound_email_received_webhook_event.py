# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["InboundEmailReceivedWebhookEvent", "Data", "DataEmail", "DataEmailAttachment", "DataOrganization"]


class DataEmailAttachment(BaseModel):
    id: str

    content_type: str = FieldInfo(alias="contentType")

    created_at: datetime = FieldInfo(alias="createdAt")

    expires_at: datetime = FieldInfo(alias="expiresAt")

    file_name: str = FieldInfo(alias="fileName")

    signed_url: str = FieldInfo(alias="signedUrl")

    size_in_bytes: float = FieldInfo(alias="sizeInBytes")

    cid: Optional[str] = None

    disposition: Optional[str] = None


class DataEmail(BaseModel):
    id: str

    attachments: List[DataEmailAttachment]

    bcc_addresses: List[str] = FieldInfo(alias="bccAddresses")

    cc_addresses: List[str] = FieldInfo(alias="ccAddresses")

    created_at: datetime = FieldInfo(alias="createdAt")

    direction: Literal["INBOUND", "OUTBOUND"]

    from_address: str = FieldInfo(alias="fromAddress")

    message_id: str = FieldInfo(alias="messageId")

    references: List[str]

    reply_to_addresses: List[str] = FieldInfo(alias="replyToAddresses")

    status: Literal[
        "DRAFT",
        "QUEUED",
        "ACCEPTED",
        "SENT",
        "RECEIVED",
        "FAILED",
        "BOUNCED",
        "COMPLAINED",
        "REJECTED",
        "READ",
        "ARCHIVED",
    ]

    thread_id: str = FieldInfo(alias="threadId")

    to_addresses: List[str] = FieldInfo(alias="toAddresses")

    from_name: Optional[str] = FieldInfo(alias="fromName", default=None)

    html: Optional[str] = None

    in_reply_to_id: Optional[str] = FieldInfo(alias="inReplyToId", default=None)

    received_at: Optional[datetime] = FieldInfo(alias="receivedAt", default=None)

    sent_at: Optional[datetime] = FieldInfo(alias="sentAt", default=None)

    snippet: Optional[str] = None

    stripped_html: Optional[str] = FieldInfo(alias="strippedHtml", default=None)

    stripped_text: Optional[str] = FieldInfo(alias="strippedText", default=None)

    subject: Optional[str] = None

    text: Optional[str] = None


class DataOrganization(BaseModel):
    id: str

    slug: str


class Data(BaseModel):
    email: DataEmail

    organization: DataOrganization


class InboundEmailReceivedWebhookEvent(BaseModel):
    attempt: int

    data: Data

    event: Literal["inbound.email.received"]

    timestamp: int
