from enum import StrEnum

class ManagedAgentsAnalyticsResponseGranularity(StrEnum):
    DAY = "day"
    HOUR = "hour"

    def __str__(self) -> str:
        return str(self.value)
