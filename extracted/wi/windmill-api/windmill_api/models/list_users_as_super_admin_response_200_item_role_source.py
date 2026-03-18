from enum import Enum


class ListUsersAsSuperAdminResponse200ItemRoleSource(str, Enum):
    INSTANCE_GROUP = "instance_group"
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
