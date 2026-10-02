from enum import StrEnum

class ManagedAgentsUnsignedCustomEventSourceVerificationType(StrEnum):
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
