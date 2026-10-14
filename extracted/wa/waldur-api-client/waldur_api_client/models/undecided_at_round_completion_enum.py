from enum import Enum


class UndecidedAtRoundCompletionEnum(str, Enum):
    REFUSE = "refuse"
    REJECT = "reject"

    def __str__(self) -> str:
        return str(self.value)
