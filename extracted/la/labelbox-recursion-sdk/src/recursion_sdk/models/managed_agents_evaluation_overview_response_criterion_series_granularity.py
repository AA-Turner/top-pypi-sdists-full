from enum import StrEnum

class ManagedAgentsEvaluationOverviewResponseCriterionSeriesGranularity(StrEnum):
    DAY = "day"
    EXACT = "exact"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"

    def __str__(self) -> str:
        return str(self.value)
