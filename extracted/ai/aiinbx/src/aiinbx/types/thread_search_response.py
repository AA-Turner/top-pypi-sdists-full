# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ThreadSearchResponse", "Pagination", "Thread"]


class Pagination(BaseModel):
    has_more: bool = FieldInfo(alias="hasMore")

    limit: float

    offset: float

    total: float


class Thread(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    email_count: float = FieldInfo(alias="emailCount")

    last_email_at: Optional[str] = FieldInfo(alias="lastEmailAt", default=None)

    participant_emails: List[str] = FieldInfo(alias="participantEmails")

    snippet: Optional[str] = None

    subject: Optional[str] = None

    updated_at: str = FieldInfo(alias="updatedAt")


class ThreadSearchResponse(BaseModel):
    pagination: Pagination

    threads: List[Thread]
