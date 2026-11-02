from enum import Enum


class WorkspaceComparisonDiffsItemForkLastEventKind(str, Enum):
    DELETE = "delete"
    RENAME_FROM = "rename_from"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
