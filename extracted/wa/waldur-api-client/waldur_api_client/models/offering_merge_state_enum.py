from enum import Enum


class OfferingMergeStateEnum(str, Enum):
    DONE = "done"
    DRAFT = "draft"
    FAILED = "failed"
    PREVIEWED = "previewed"
    QUEUED = "queued"
    RUNNING = "running"
    UNDOING = "undoing"
    UNDONE = "undone"

    def __str__(self) -> str:
        return str(self.value)
