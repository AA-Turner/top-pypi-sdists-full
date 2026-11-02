from enum import Enum


class CompareWorkspacesResponse200DiffsItemSourceLastEventOrigin(str, Enum):
    AUTHORED = "authored"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
