from enum import Enum


class QueueKindEnum(str, Enum):
    CONSUMER = "consumer"
    LEGACY = "legacy"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
