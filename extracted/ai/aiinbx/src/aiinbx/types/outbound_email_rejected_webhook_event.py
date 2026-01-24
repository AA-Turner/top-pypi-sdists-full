# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OutboundEmailRejectedWebhookEvent", "Data"]


class Data(BaseModel):
    message_id: str = FieldInfo(alias="messageId")

    rejected_at: str = FieldInfo(alias="rejectedAt")

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    reason: Optional[str] = None


class OutboundEmailRejectedWebhookEvent(BaseModel):
    attempt: int

    data: Data

    event: Literal["outbound.email.rejected"]

    timestamp: int
