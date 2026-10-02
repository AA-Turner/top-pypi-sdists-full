from enum import StrEnum

class ManagedAgentsApiErrorModelGatewayUnreachableCode(StrEnum):
    MODEL_GATEWAY_UNREACHABLE = "model_gateway_unreachable"

    def __str__(self) -> str:
        return str(self.value)
