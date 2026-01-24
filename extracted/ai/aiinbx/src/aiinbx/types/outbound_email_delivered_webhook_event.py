# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OutboundEmailDeliveredWebhookEvent", "Data"]


class Data(BaseModel):
    delivered_at: str = FieldInfo(alias="deliveredAt")

    message_id: str = FieldInfo(alias="messageId")

    recipients: List[str]

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    processing_time_ms: Optional[int] = FieldInfo(alias="processingTimeMs", default=None)

    remote_mta_ip: Optional[str] = FieldInfo(alias="remoteMtaIp", default=None)

    smtp_response: Optional[str] = FieldInfo(alias="smtpResponse", default=None)


class OutboundEmailDeliveredWebhookEvent(BaseModel):
    attempt: int

    data: Data

    event: Literal["outbound.email.delivered"]

    timestamp: int
