from enum import Enum


class AvailableExternalNetworkSourceEnum(str, Enum):
    GLOBAL = "global"
    RBAC = "rbac"

    def __str__(self) -> str:
        return str(self.value)
