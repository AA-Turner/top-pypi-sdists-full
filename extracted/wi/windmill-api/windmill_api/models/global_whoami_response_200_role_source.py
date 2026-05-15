from enum import Enum


class GlobalWhoamiResponse200RoleSource(str, Enum):
    INSTANCE_GROUP = "instance_group"
    MANUAL = "manual"
    SERVICE_ACCOUNT = "service_account"

    def __str__(self) -> str:
        return str(self.value)
