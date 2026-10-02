from enum import StrEnum

class GradingConfigInputComputeExecOutputFormat(StrEnum):
    JSON = "json"
    JSON_RUBRIC = "json_rubric"
    JUNIT = "junit"

    def __str__(self) -> str:
        return str(self.value)
