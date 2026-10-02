from enum import StrEnum

class ManagedAgentsMemoryStatus(StrEnum):
    ACTIVE = "active"
    RETIRED = "retired"
    SUPERSEDED = "superseded"

    def __str__(self) -> str:
        return str(self.value)
