from enum import StrEnum

class GradingConfigWeightedSumType(StrEnum):
    WEIGHTED_SUM = "weighted-sum"

    def __str__(self) -> str:
        return str(self.value)
