from enum import Enum


class GetInstanceGroupResponse200InstanceRole(str, Enum):
    DEVOPS = "devops"
    SUPERADMIN = "superadmin"

    def __str__(self) -> str:
        return str(self.value)
