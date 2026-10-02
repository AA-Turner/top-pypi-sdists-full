from enum import StrEnum

class ManagedAgentsApiErrorModelGatewayUnconfiguredCode(StrEnum):
    MODEL_GATEWAY_UNCONFIGURED = "model_gateway_unconfigured"

    def __str__(self) -> str:
        return str(self.value)
