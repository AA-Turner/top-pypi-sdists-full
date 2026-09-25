from enum import Enum


class TWorkspaceAccessContextItem(str, Enum):
    ALL = "all"
    DEPLOY = "deploy"
    EXECUTE = "execute"
    READ = "read"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
