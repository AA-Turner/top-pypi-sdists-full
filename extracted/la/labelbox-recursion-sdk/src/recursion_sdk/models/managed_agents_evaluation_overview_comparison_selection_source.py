from enum import StrEnum

class ManagedAgentsEvaluationOverviewComparisonSelectionSource(StrEnum):
    DEFAULT = "default"
    EXPLICIT = "explicit"

    def __str__(self) -> str:
        return str(self.value)
