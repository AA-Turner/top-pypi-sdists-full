# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OutboundEmailClickedWebhookEvent", "Data"]


class Data(BaseModel):
    clicked_at: str = FieldInfo(alias="clickedAt")

    link: str

    message_id: str = FieldInfo(alias="messageId")

    email_id: Optional[str] = FieldInfo(alias="emailId", default=None)

    ip_address: Optional[str] = FieldInfo(alias="ipAddress", default=None)

    link_domain: Optional[str] = FieldInfo(alias="linkDomain", default=None)

    user_agent: Optional[str] = FieldInfo(alias="userAgent", default=None)


class OutboundEmailClickedWebhookEvent(BaseModel):
    attempt: int

    data: Data

    event: Literal["outbound.email.clicked"]

    timestamp: int
