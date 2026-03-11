from enum import Enum


class ListKafkaTriggersResponse200ItemAutoOffsetReset(str, Enum):
    EARLIEST = "earliest"
    LATEST = "latest"

    def __str__(self) -> str:
        return str(self.value)
