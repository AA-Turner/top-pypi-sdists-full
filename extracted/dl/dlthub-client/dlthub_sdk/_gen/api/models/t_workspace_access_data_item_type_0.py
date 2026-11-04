from enum import Enum


class TWorkspaceAccessDataItemType0(str, Enum):
    ALL = "all"
    READ = "read"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
