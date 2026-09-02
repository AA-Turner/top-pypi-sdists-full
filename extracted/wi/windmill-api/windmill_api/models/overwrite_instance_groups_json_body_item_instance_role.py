from enum import Enum


class OverwriteInstanceGroupsJsonBodyItemInstanceRole(str, Enum):
    DEVOPS = "devops"
    SUPERADMIN = "superadmin"

    def __str__(self) -> str:
        return str(self.value)
