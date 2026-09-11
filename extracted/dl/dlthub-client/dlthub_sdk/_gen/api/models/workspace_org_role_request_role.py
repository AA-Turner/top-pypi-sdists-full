from enum import Enum


class WorkspaceOrgRoleRequestRole(str, Enum):
    DEVELOPER = "developer"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
