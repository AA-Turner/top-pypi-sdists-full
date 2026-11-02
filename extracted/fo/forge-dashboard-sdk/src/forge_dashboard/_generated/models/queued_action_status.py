from enum import StrEnum

class QueuedActionStatus(StrEnum):
    DONE = "done"
    FAILED = "failed"
    QUEUED = "queued"
    SKIPPED = "skipped"

    def __str__(self) -> str:
        return str(self.value)
