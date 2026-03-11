from enum import Enum


class KafkaTriggerAutoOffsetReset(str, Enum):
    EARLIEST = "earliest"
    LATEST = "latest"

    def __str__(self) -> str:
        return str(self.value)
