from enum import StrEnum

class GradingConfigInputProgrammaticOutputFormat(StrEnum):
    JSON = "json"
    JSON_RUBRIC = "json_rubric"
    JUNIT = "junit"

    def __str__(self) -> str:
        return str(self.value)
