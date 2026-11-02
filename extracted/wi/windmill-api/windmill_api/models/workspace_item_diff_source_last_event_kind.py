from enum import Enum


class WorkspaceItemDiffSourceLastEventKind(str, Enum):
    DELETE = "delete"
    RENAME_FROM = "rename_from"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
