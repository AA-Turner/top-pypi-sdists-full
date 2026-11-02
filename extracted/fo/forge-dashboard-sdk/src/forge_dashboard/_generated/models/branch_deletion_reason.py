from enum import StrEnum

class BranchDeletionReason(StrEnum):
    DEFAULT_BRANCH = "default_branch"
    FORK = "fork"
    IN_USE = "in_use"
    PROTECTED = "protected"
    UNSUPPORTED = "unsupported"

    def __str__(self) -> str:
        return str(self.value)
