# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EmailReplyResponse"]


class EmailReplyResponse(BaseModel):
    email_id: str = FieldInfo(alias="emailId")

    message_id: str = FieldInfo(alias="messageId")

    thread_id: str = FieldInfo(alias="threadId")
