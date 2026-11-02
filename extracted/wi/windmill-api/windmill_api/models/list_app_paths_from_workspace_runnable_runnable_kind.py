from enum import Enum


class ListAppPathsFromWorkspaceRunnableRunnableKind(str, Enum):
    FLOW = "flow"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
