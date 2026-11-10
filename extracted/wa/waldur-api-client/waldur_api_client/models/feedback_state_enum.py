from enum import Enum


class FeedbackStateEnum(str, Enum):
    ANSWERED = "answered"
    DISMISSED = "dismissed"
    EXPIRED = "expired"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
