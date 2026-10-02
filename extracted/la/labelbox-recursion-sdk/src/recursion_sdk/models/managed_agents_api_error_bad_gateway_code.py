from enum import StrEnum

class ManagedAgentsApiErrorBadGatewayCode(StrEnum):
    BAD_GATEWAY = "bad_gateway"

    def __str__(self) -> str:
        return str(self.value)
