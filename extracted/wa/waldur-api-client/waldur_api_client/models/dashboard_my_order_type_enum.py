from enum import Enum


class DashboardMyOrderTypeEnum(str, Enum):
    CREATE = "create"
    RESTORE = "restore"
    TERMINATE = "terminate"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
