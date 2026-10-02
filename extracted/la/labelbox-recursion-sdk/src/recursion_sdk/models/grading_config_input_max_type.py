from enum import StrEnum

class GradingConfigInputMaxType(StrEnum):
    MAX = "max"

    def __str__(self) -> str:
        return str(self.value)
