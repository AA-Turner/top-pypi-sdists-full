from enum import Enum


class RoundStatus(str, Enum):
    ENDED = "ended"
    OPEN = "open"
    SCHEDULED = "scheduled"

    def __str__(self) -> str:
        return str(self.value)
