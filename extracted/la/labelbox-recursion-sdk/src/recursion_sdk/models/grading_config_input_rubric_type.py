from enum import StrEnum

class GradingConfigInputRubricType(StrEnum):
    RUBRIC = "rubric"

    def __str__(self) -> str:
        return str(self.value)
