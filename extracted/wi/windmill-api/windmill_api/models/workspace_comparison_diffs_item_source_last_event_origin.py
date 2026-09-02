from enum import Enum


class WorkspaceComparisonDiffsItemSourceLastEventOrigin(str, Enum):
    AUTHORED = "authored"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
