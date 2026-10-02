from enum import StrEnum

class GetEvaluationOverviewSeriesResolution(StrEnum):
    ADAPTIVE = "adaptive"

    def __str__(self) -> str:
        return str(self.value)
