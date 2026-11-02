from enum import Enum


class CompareWorkspacesResponse200DiffsItemForkLastEventOrigin(str, Enum):
    AUTHORED = "authored"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
