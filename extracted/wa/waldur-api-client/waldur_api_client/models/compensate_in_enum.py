from enum import Enum


class CompensateInEnum(str, Enum):
    CURRENT_MONTH = "current_month"
    INCURRED_MONTH = "incurred_month"

    def __str__(self) -> str:
        return str(self.value)
