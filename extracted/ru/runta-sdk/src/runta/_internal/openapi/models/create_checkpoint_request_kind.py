from enum import Enum


class CreateCheckpointRequestKind(str, Enum):
    COLD = "cold"
    FULL = "full"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
