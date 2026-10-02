from enum import StrEnum

class ManagedAgentsGestaltSessionRowStatus(StrEnum):
    ACTIVE = "active"
    AWAITING_HUMAN = "awaiting_human"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
