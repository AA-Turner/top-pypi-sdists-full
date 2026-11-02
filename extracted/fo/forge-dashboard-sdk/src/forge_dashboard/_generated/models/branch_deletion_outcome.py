from enum import StrEnum

class BranchDeletionOutcome(StrEnum):
    DELETED = "deleted"
    FAILED = "failed"
    SKIPPED = "skipped"

    def __str__(self) -> str:
        return str(self.value)
