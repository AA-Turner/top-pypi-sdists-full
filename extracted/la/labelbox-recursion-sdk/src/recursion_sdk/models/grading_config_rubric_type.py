from enum import StrEnum

class GradingConfigRubricType(StrEnum):
    RUBRIC = "rubric"

    def __str__(self) -> str:
        return str(self.value)
