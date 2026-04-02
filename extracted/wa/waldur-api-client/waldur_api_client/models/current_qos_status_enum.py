from enum import Enum


class CurrentQosStatusEnum(str, Enum):
    BLOCKED = "blocked"
    NORMAL = "normal"
    NOTIFICATION = "notification"
    SLOWDOWN = "slowdown"

    def __str__(self) -> str:
        return str(self.value)
