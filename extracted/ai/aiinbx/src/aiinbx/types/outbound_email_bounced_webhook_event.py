# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OutboundEmailBouncedWebhookEvent", "Data", "DataRecipient"]


class DataRecipient(BaseModel):
    email_address: str = FieldInfo(alias="emailAddress")

    action: Optional[str] = None

    diagnostic_code: Optional[str] = FieldInfo(alias="diagnosticCode", default=None)

    status: Optional[str] = None


class Data(BaseModel):
    bounced_at: str = FieldInfo(alias="bouncedAt")

    bounce_type: Literal["Permanent", "Transient", "Undetermined"] = FieldInfo(alias="bounceType")

    message_id: str = FieldInfo(alias="messageId")

    recipients: List[DataRecipient]

    bounce_sub_type: Optional[str] = FieldInfo(alias="bounceSubType", default=None)

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)


class OutboundEmailBouncedWebhookEvent(BaseModel):
    attempt: int

    data: Data

    event: Literal["outbound.email.bounced"]

    timestamp: int
