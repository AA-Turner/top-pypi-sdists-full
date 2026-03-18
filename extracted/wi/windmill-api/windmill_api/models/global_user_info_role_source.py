from enum import Enum


class GlobalUserInfoRoleSource(str, Enum):
    INSTANCE_GROUP = "instance_group"
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
