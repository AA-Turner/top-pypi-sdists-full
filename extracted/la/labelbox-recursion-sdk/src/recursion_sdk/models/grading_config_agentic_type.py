from enum import StrEnum

class GradingConfigAgenticType(StrEnum):
    AGENTIC = "agentic"

    def __str__(self) -> str:
        return str(self.value)
