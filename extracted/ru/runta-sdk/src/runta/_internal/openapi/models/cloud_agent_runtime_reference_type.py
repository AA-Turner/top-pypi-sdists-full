from enum import Enum


class CloudAgentRuntimeReferenceType(str, Enum):
    CHECKPOINT = "checkpoint"
    EXISTING = "existing"
    FRESH = "fresh"

    def __str__(self) -> str:
        return str(self.value)
