from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Event(BaseModel):
    event_type: str
    source: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict
    metadata: dict = {}
