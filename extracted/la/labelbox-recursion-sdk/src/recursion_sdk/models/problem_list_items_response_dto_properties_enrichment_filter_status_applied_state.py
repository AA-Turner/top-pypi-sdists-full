from enum import StrEnum

class ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusAppliedState(StrEnum):
    APPLIED = "applied"

    def __str__(self) -> str:
        return str(self.value)
