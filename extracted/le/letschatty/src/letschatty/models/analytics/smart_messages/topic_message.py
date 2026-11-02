from enum import StrEnum
from typing import Dict, Optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from ...utils.types import StrObjectId
from ...utils.custom_exceptions import DuplicatedMessage

class MessageTopicStatus(StrEnum):
    LOCKED = "locked"
    EXPIRED = "expired"
    AVAILABLE = "available"

class MessageTopic(BaseModel):
    content: str
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    is_locked: bool = Field(default=False)
    locked_by: Optional[StrObjectId] = Field(default=None)
    lock_time: Optional[datetime] = Field(default=None)
    is_default: bool = Field(default=False)

    def model_dump(self, *args, **kwargs) -> Dict:
        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        if self.lock_time:
            data["lock_time"] = self.lock_time.isoformat()
        return data

    @field_validator('lock_time', mode='before')
    def validate_lock_time(cls, v: datetime | str) -> datetime:
        if v is None:
            return None
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        elif isinstance(v, datetime):
            return v
        else:
            raise ValueError("lock_time must be a datetime or an isoformat string")

    @property
    def content_preview(self) -> str:
        return self.content[:20] + "..." if len(self.content) > 20 else self.content

    @property
    def time_locked(self) -> Optional[timedelta]:
        """Returns how long the message has been locked for.
        Calculated each time this property is accessed."""
        if self.lock_time:
            return datetime.now(ZoneInfo("UTC")) - self.lock_time
        return None

    def __eq__(self, other: 'MessageTopic') -> bool:
        return self.content == other.content

    def __hash__(self) -> int:
        return hash(self.content)

    def __contains__(self, other: 'MessageTopic') -> bool:
        return self.content in other.content or other.content in self.content

    def check_message_conflict(self, other: 'MessageTopic') -> None:
        if self in other or other in self or self == other:
            raise DuplicatedMessage(f"Message {self.content} is duplicated or conflicting with {other.content}")


    @property
    def contact_point_id_locking_message(self) -> StrObjectId:
        if not self.locked_by:
            raise ValueError("No contact point id locking message")
        return self.locked_by
