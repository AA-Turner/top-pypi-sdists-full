from enum import StrEnum

class GradingConfigMaxType(StrEnum):
    MAX = "max"

    def __str__(self) -> str:
        return str(self.value)
