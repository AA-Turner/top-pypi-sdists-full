from enum import Enum


class GetKafkaTriggerResponse200AutoOffsetReset(str, Enum):
    EARLIEST = "earliest"
    LATEST = "latest"

    def __str__(self) -> str:
        return str(self.value)
