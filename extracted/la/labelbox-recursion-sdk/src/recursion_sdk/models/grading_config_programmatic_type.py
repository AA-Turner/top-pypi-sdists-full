from enum import StrEnum

class GradingConfigProgrammaticType(StrEnum):
    PROGRAMMATIC = "programmatic"

    def __str__(self) -> str:
        return str(self.value)
