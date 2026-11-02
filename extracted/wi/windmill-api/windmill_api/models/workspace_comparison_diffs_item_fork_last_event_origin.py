from enum import Enum


class WorkspaceComparisonDiffsItemForkLastEventOrigin(str, Enum):
    AUTHORED = "authored"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
