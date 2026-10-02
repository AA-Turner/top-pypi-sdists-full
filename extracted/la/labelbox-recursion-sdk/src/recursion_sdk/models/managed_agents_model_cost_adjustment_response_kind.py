from enum import StrEnum

class ManagedAgentsModelCostAdjustmentResponseKind(StrEnum):
    CORRECTION = "correction"
    PROVIDER_AUTHORITY = "provider_authority"

    def __str__(self) -> str:
        return str(self.value)
