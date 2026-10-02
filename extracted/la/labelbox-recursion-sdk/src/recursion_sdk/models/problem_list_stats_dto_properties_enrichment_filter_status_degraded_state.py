from enum import StrEnum

class ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedState(StrEnum):
    DEGRADED = "degraded"

    def __str__(self) -> str:
        return str(self.value)
