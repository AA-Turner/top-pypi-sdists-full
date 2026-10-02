from enum import StrEnum

class ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegradedState(StrEnum):
    DEGRADED = "degraded"

    def __str__(self) -> str:
        return str(self.value)
