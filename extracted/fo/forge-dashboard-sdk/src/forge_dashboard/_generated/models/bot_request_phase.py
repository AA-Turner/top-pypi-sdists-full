from enum import StrEnum

class BotRequestPhase(StrEnum):
    EXPIRED = "expired"
    QUEUED = "queued"
    REBASING = "rebasing"

    def __str__(self) -> str:
        return str(self.value)
