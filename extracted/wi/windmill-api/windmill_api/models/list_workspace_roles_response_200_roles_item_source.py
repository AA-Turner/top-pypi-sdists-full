from enum import Enum


class ListWorkspaceRolesResponse200RolesItemSource(str, Enum):
    INSTANCE = "instance"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
