from enum import Enum


class JobDeployOutcome(str, Enum):
    ARCHIVED = "archived"
    CREATED = "created"
    UNCHANGED = "unchanged"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
