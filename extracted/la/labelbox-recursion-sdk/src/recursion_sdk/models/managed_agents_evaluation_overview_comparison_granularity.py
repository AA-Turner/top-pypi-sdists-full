from enum import StrEnum

class ManagedAgentsEvaluationOverviewComparisonGranularity(StrEnum):
    DAY = "day"
    EXACT = "exact"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"

    def __str__(self) -> str:
        return str(self.value)
