from enum import StrEnum

class UpdateRequestPhase(StrEnum):
    EXPIRED = "expired"
    QUEUED = "queued"

    def __str__(self) -> str:
        return str(self.value)
