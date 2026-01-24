# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "MetaWebhooksSchemaResponse",
    "InboundEmailReceivedEvent",
    "InboundEmailReceivedEventData",
    "InboundEmailReceivedEventDataEmail",
    "InboundEmailReceivedEventDataEmailAttachment",
    "InboundEmailReceivedEventDataOrganization",
    "OutboundDeliveredEvent",
    "OutboundDeliveredEventData",
    "OutboundBouncedEvent",
    "OutboundBouncedEventData",
    "OutboundBouncedEventDataRecipient",
    "OutboundComplainedEvent",
    "OutboundComplainedEventData",
    "OutboundRejectedEvent",
    "OutboundRejectedEventData",
    "OutboundOpenedEvent",
    "OutboundOpenedEventData",
    "OutboundClickedEvent",
    "OutboundClickedEventData",
]


class InboundEmailReceivedEventDataEmailAttachment(BaseModel):
    id: str

    content_type: str = FieldInfo(alias="contentType")

    created_at: datetime = FieldInfo(alias="createdAt")

    expires_at: datetime = FieldInfo(alias="expiresAt")

    file_name: str = FieldInfo(alias="fileName")

    signed_url: str = FieldInfo(alias="signedUrl")

    size_in_bytes: float = FieldInfo(alias="sizeInBytes")

    cid: Optional[str] = None

    disposition: Optional[str] = None


class InboundEmailReceivedEventDataEmail(BaseModel):
    id: str

    attachments: List[InboundEmailReceivedEventDataEmailAttachment]

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


class InboundEmailReceivedEventDataOrganization(BaseModel):
    id: str

    slug: str


class InboundEmailReceivedEventData(BaseModel):
    email: InboundEmailReceivedEventDataEmail

    organization: InboundEmailReceivedEventDataOrganization


class InboundEmailReceivedEvent(BaseModel):
    attempt: int

    data: InboundEmailReceivedEventData

    event: Literal["inbound.email.received"]

    timestamp: int


class OutboundDeliveredEventData(BaseModel):
    delivered_at: str = FieldInfo(alias="deliveredAt")

    message_id: str = FieldInfo(alias="messageId")

    recipients: List[str]

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    processing_time_ms: Optional[int] = FieldInfo(alias="processingTimeMs", default=None)

    remote_mta_ip: Optional[str] = FieldInfo(alias="remoteMtaIp", default=None)

    smtp_response: Optional[str] = FieldInfo(alias="smtpResponse", default=None)


class OutboundDeliveredEvent(BaseModel):
    attempt: int

    data: OutboundDeliveredEventData

    event: Literal["outbound.email.delivered"]

    timestamp: int


class OutboundBouncedEventDataRecipient(BaseModel):
    email_address: str = FieldInfo(alias="emailAddress")

    action: Optional[str] = None

    diagnostic_code: Optional[str] = FieldInfo(alias="diagnosticCode", default=None)

    status: Optional[str] = None


class OutboundBouncedEventData(BaseModel):
    bounced_at: str = FieldInfo(alias="bouncedAt")

    bounce_type: Literal["Permanent", "Transient", "Undetermined"] = FieldInfo(alias="bounceType")

    message_id: str = FieldInfo(alias="messageId")

    recipients: List[OutboundBouncedEventDataRecipient]

    bounce_sub_type: Optional[str] = FieldInfo(alias="bounceSubType", default=None)

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)


class OutboundBouncedEvent(BaseModel):
    attempt: int

    data: OutboundBouncedEventData

    event: Literal["outbound.email.bounced"]

    timestamp: int


class OutboundComplainedEventData(BaseModel):
    complained_at: str = FieldInfo(alias="complainedAt")

    message_id: str = FieldInfo(alias="messageId")

    recipients: List[str]

    complaint_feedback_type: Optional[str] = FieldInfo(alias="complaintFeedbackType", default=None)

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    feedback_id: Optional[str] = FieldInfo(alias="feedbackId", default=None)

    user_agent: Optional[str] = FieldInfo(alias="userAgent", default=None)


class OutboundComplainedEvent(BaseModel):
    attempt: int

    data: OutboundComplainedEventData

    event: Literal["outbound.email.complained"]

    timestamp: int


class OutboundRejectedEventData(BaseModel):
    message_id: str = FieldInfo(alias="messageId")

    rejected_at: str = FieldInfo(alias="rejectedAt")

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    reason: Optional[str] = None


class OutboundRejectedEvent(BaseModel):
    attempt: int

    data: OutboundRejectedEventData

    event: Literal["outbound.email.rejected"]

    timestamp: int


class OutboundOpenedEventData(BaseModel):
    message_id: str = FieldInfo(alias="messageId")

    opened_at: str = FieldInfo(alias="openedAt")

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    ip_address: Optional[str] = FieldInfo(alias="ipAddress", default=None)

    user_agent: Optional[str] = FieldInfo(alias="userAgent", default=None)


class OutboundOpenedEvent(BaseModel):
    attempt: int

    data: OutboundOpenedEventData

    event: Literal["outbound.email.opened"]

    timestamp: int


class OutboundClickedEventData(BaseModel):
    clicked_at: str = FieldInfo(alias="clickedAt")

    link: str

    message_id: str = FieldInfo(alias="messageId")

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    ip_address: Optional[str] = FieldInfo(alias="ipAddress", default=None)

    link_domain: Optional[str] = FieldInfo(alias="linkDomain", default=None)

    user_agent: Optional[str] = FieldInfo(alias="userAgent", default=None)


class OutboundClickedEvent(BaseModel):
    attempt: int

    data: OutboundClickedEventData

    event: Literal["outbound.email.clicked"]

    timestamp: int


MetaWebhooksSchemaResponse: TypeAlias = Union[
    InboundEmailReceivedEvent,
    OutboundDeliveredEvent,
    OutboundBouncedEvent,
    OutboundComplainedEvent,
    OutboundRejectedEvent,
    OutboundOpenedEvent,
    OutboundClickedEvent,
]
