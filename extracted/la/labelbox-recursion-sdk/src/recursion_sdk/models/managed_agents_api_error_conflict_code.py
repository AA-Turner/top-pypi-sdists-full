from enum import StrEnum

class ManagedAgentsApiErrorConflictCode(StrEnum):
    CONFLICT = "conflict"

    def __str__(self) -> str:
        return str(self.value)
