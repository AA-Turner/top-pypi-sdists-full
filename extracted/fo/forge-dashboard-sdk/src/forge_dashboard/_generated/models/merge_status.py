from enum import StrEnum

class MergeStatus(StrEnum):
    BLOCKED = "blocked"
    CONFLICTING = "conflicting"
    MERGEABLE = "mergeable"
    UNKNOWN = "unknown"
    UNSTABLE = "unstable"

    def __str__(self) -> str:
        return str(self.value)
