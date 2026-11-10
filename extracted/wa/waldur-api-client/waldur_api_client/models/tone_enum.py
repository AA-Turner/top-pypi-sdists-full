from enum import Enum


class ToneEnum(str, Enum):
    DANGER = "danger"
    INFO = "info"
    NEUTRAL = "neutral"
    SUCCESS = "success"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
