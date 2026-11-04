from enum import Enum


class TIntervalSpecModeType0(str, Enum):
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"

    def __str__(self) -> str:
        return str(self.value)
