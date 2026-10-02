from enum import StrEnum

class StageClearanceRequestBodyDtoType0Stage(StrEnum):
    LOCKING = "locking"
    RUNNING = "running"
    SUBMITTING = "submitting"

    def __str__(self) -> str:
        return str(self.value)
