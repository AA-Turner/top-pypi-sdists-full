from enum import Enum


class TriggerHistoryEntryOperation(str, Enum):
    CREATE = "create"
    DELETE = "delete"
    DISABLE = "disable"
    ENABLE = "enable"
    SUSPEND = "suspend"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
