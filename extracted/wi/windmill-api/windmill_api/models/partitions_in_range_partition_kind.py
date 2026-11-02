from enum import Enum


class PartitionsInRangePartitionKind(str, Enum):
    DAILY = "daily"
    DYNAMIC = "dynamic"
    HOURLY = "hourly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
