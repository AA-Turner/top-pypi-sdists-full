from enum import Enum


class TIntervalSpecMode(str, Enum):
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"

    def __str__(self) -> str:
        return str(self.value)
