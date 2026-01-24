# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OutboundEmailComplainedWebhookEvent", "Data"]


class Data(BaseModel):
    complained_at: str = FieldInfo(alias="complainedAt")

    message_id: str = FieldInfo(alias="messageId")

    recipients: List[str]

    complaint_feedback_type: Optional[str] = FieldInfo(alias="complaintFeedbackType", default=None)

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    feedback_id: Optional[str] = FieldInfo(alias="feedbackId", default=None)

    user_agent: Optional[str] = FieldInfo(alias="userAgent", default=None)


class OutboundEmailComplainedWebhookEvent(BaseModel):
    attempt: int

    data: Data

    event: Literal["outbound.email.complained"]

    timestamp: int
