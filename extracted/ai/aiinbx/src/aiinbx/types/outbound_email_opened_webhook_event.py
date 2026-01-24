# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OutboundEmailOpenedWebhookEvent", "Data"]


class Data(BaseModel):
    message_id: str = FieldInfo(alias="messageId")

    opened_at: str = FieldInfo(alias="openedAt")

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    ip_address: Optional[str] = FieldInfo(alias="ipAddress", default=None)

    user_agent: Optional[str] = FieldInfo(alias="userAgent", default=None)


class OutboundEmailOpenedWebhookEvent(BaseModel):
    attempt: int

    data: Data

    event: Literal["outbound.email.opened"]

    timestamp: int
