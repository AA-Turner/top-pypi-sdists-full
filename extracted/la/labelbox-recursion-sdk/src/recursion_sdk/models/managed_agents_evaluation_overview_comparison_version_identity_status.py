from enum import StrEnum

class ManagedAgentsEvaluationOverviewComparisonVersionIdentityStatus(StrEnum):
    CATALOG = "catalog"
    RETAINED_HISTORY = "retained_history"

    def __str__(self) -> str:
        return str(self.value)
