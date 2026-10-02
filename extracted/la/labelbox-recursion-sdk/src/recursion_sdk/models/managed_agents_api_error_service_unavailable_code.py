from enum import StrEnum

class ManagedAgentsApiErrorServiceUnavailableCode(StrEnum):
    SERVICE_UNAVAILABLE = "service_unavailable"

    def __str__(self) -> str:
        return str(self.value)
