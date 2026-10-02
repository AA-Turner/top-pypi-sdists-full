from enum import Enum


class MinimalConsumptionLogicEnum(str, Enum):
    FIXED = "fixed"
    LINEAR = "linear"

    def __str__(self) -> str:
        return str(self.value)
