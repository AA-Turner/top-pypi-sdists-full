from enum import StrEnum

class GradingConfigInputProgrammaticType(StrEnum):
    PROGRAMMATIC = "programmatic"

    def __str__(self) -> str:
        return str(self.value)
