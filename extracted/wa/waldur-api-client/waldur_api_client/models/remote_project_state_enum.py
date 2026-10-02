from enum import Enum


class RemoteProjectStateEnum(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    ERROR = "error"
    PENDING = "pending"
    STALE = "stale"

    def __str__(self) -> str:
        return str(self.value)
