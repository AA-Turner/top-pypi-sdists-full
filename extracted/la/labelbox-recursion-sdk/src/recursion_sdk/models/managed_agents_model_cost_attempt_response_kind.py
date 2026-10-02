from enum import StrEnum

class ManagedAgentsModelCostAttemptResponseKind(StrEnum):
    MODEL = "model"
    PROVIDER_TOOL = "provider_tool"
    SANDBOX_COMPUTE = "sandbox_compute"

    def __str__(self) -> str:
        return str(self.value)
