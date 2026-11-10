# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SessionLogsResponse", "Event"]


class Event(BaseModel):
    id: str

    log: str

    timestamp: datetime

    type: str


class SessionLogsResponse(BaseModel):
    events: List[Event]

    has_more: bool = FieldInfo(alias="hasMore")

    total: float
