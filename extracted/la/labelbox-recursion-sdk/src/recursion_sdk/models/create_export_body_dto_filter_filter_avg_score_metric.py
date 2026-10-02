from enum import StrEnum

class CreateExportBodyDtoFilterFilterAvgScoreMetric(StrEnum):
    AVG = "avg"
    MAX = "max"
    MIN = "min"

    def __str__(self) -> str:
        return str(self.value)
