from enum import StrEnum

class ManagedAgentsMemoryStoreStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"

    def __str__(self) -> str:
        return str(self.value)
