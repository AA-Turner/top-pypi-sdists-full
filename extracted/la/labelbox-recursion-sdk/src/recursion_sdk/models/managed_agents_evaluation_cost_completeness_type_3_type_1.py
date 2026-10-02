from enum import StrEnum

class ManagedAgentsEvaluationCostCompletenessType3Type1(StrEnum):
    COMPLETE = "complete"
    INDETERMINATE = "indeterminate"
    LEGACY_PARTIAL = "legacy_partial"
    PARTIAL = "partial"
    PENDING = "pending"
    UNPRICED = "unpriced"

    def __str__(self) -> str:
        return str(self.value)
