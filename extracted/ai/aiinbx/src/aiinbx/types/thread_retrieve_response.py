# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ThreadRetrieveResponse", "Email", "EmailAttachment"]


class EmailAttachment(BaseModel):
    id: str

    cid: Optional[str] = None

    content_type: str = FieldInfo(alias="contentType")

    created_at: str = FieldInfo(alias="createdAt")

    disposition: Optional[str] = None

    expires_at: str = FieldInfo(alias="expiresAt")

    file_name: str = FieldInfo(alias="fileName")

    signed_url: str = FieldInfo(alias="signedUrl")

    size_in_bytes: float = FieldInfo(alias="sizeInBytes")


class Email(BaseModel):
    id: str

    attachments: List[EmailAttachment]

    bcc_addresses: List[str] = FieldInfo(alias="bccAddresses")

    cc_addresses: List[str] = FieldInfo(alias="ccAddresses")

    created_at: str = FieldInfo(alias="createdAt")

    direction: Literal["INBOUND", "OUTBOUND"]

    from_address: str = FieldInfo(alias="fromAddress")

    from_name: Optional[str] = FieldInfo(alias="fromName", default=None)

    html: Optional[str] = None

    in_reply_to_id: Optional[str] = FieldInfo(alias="inReplyToId", default=None)

    message_id: str = FieldInfo(alias="messageId")

    received_at: Optional[str] = FieldInfo(alias="receivedAt", default=None)

    references: List[str]

    reply_to_addresses: List[str] = FieldInfo(alias="replyToAddresses")

    sent_at: Optional[str] = FieldInfo(alias="sentAt", default=None)

    snippet: Optional[str] = None

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

    stripped_html: Optional[str] = FieldInfo(alias="strippedHtml", default=None)

    stripped_text: Optional[str] = FieldInfo(alias="strippedText", default=None)

    subject: Optional[str] = None

    text: Optional[str] = None

    thread_id: str = FieldInfo(alias="threadId")

    to_addresses: List[str] = FieldInfo(alias="toAddresses")


class ThreadRetrieveResponse(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    emails: List[Email]

    subject: Optional[str] = None
