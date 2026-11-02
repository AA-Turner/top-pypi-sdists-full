from enum import Enum


class ListAssetPartitionsInRangeResponse200PartitionKind(str, Enum):
    DAILY = "daily"
    DYNAMIC = "dynamic"
    HOURLY = "hourly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
