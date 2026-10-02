from enum import Enum


class COISeverityLevel(str, Enum):
    APPARENT = "apparent"
    POTENTIAL = "potential"
    REAL = "real"

    def __str__(self) -> str:
        return str(self.value)
