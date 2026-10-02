from enum import StrEnum

class ManagedAgentsMemoryVersionOperation(StrEnum):
    CREATE = "create"
    DELETE = "delete"
    RENAME = "rename"
    RETIRE = "retire"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
