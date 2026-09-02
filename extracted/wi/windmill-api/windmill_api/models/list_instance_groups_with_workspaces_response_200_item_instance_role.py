from enum import Enum


class ListInstanceGroupsWithWorkspacesResponse200ItemInstanceRole(str, Enum):
    DEVOPS = "devops"
    SUPERADMIN = "superadmin"

    def __str__(self) -> str:
        return str(self.value)
