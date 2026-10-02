from enum import StrEnum

class ManagedAgentsEvaluationOverviewComparisonMetric(StrEnum):
    CRITERION = "criterion"
    OVERALL = "overall"

    def __str__(self) -> str:
        return str(self.value)
