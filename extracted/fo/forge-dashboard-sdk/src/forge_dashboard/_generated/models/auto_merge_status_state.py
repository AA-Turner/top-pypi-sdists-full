from enum import StrEnum

class AutoMergeStatusState(StrEnum):
    STOPPED = "stopped"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)
