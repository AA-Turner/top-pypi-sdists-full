from enum import Enum


class OptionTransformCase(str, Enum):
    LOWER = "lower"
    UPPER = "upper"

    def __str__(self) -> str:
        return str(self.value)
