from enum import Enum


class TWorkspaceAccessLocalItem(str, Enum):
    ALL = "all"
    EXECUTE = "execute"
    NETWORK = "network"
    READ = "read"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
