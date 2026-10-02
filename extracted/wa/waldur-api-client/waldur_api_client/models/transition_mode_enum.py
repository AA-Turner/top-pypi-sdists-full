from enum import Enum


class TransitionModeEnum(str, Enum):
    AUTOMATIC_ON_COMPLETION = "automatic_on_completion"
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
