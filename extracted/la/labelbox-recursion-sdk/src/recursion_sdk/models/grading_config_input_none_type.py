from enum import StrEnum

class GradingConfigInputNoneType(StrEnum):
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
