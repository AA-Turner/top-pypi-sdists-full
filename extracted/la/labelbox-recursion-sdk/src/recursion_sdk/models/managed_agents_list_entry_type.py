from enum import StrEnum

class ManagedAgentsListEntryType(StrEnum):
    MEMORY = "memory"
    MEMORY_PREFIX = "memory_prefix"

    def __str__(self) -> str:
        return str(self.value)
