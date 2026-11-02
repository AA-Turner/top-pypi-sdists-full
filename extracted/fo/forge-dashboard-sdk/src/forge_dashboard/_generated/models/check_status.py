from enum import StrEnum

class CheckStatus(StrEnum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    QUEUED = "queued"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)
