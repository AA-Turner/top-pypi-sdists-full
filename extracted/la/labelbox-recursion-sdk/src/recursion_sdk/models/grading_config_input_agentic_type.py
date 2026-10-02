from enum import StrEnum

class GradingConfigInputAgenticType(StrEnum):
    AGENTIC = "agentic"

    def __str__(self) -> str:
        return str(self.value)
