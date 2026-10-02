from enum import StrEnum

class GetEvaluationOverviewRange(StrEnum):
    VALUE_0 = "7d"
    VALUE_1 = "28d"
    VALUE_2 = "90d"

    def __str__(self) -> str:
        return str(self.value)
