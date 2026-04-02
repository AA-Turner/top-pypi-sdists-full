from enum import Enum


class EventFieldEnum(str, Enum):
    CONTEXT = "context"
    CREATED = "created"
    EVENT_TYPE = "event_type"
    MESSAGE = "message"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
