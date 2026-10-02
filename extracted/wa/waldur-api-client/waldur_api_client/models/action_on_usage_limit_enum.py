from enum import Enum


class ActionOnUsageLimitEnum(str, Enum):
    DOWNSCALE = "downscale"
    PAUSE = "pause"

    def __str__(self) -> str:
        return str(self.value)
