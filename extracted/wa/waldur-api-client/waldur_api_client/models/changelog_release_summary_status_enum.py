from enum import Enum


class ChangelogReleaseSummaryStatusEnum(str, Enum):
    OLDER = "older"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
