from enum import Enum


class WorkspaceRolesRolesItemSource(str, Enum):
    INSTANCE = "instance"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
