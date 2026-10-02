from enum import StrEnum

class GradingConfigNoneType(StrEnum):
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
