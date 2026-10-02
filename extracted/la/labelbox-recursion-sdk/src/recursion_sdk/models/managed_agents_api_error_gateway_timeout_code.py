from enum import StrEnum

class ManagedAgentsApiErrorGatewayTimeoutCode(StrEnum):
    GATEWAY_TIMEOUT = "gateway_timeout"

    def __str__(self) -> str:
        return str(self.value)
