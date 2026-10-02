from enum import StrEnum

class ProblemListStatsDtoPropertiesEnrichmentFilterStatusAppliedState(StrEnum):
    APPLIED = "applied"

    def __str__(self) -> str:
        return str(self.value)
