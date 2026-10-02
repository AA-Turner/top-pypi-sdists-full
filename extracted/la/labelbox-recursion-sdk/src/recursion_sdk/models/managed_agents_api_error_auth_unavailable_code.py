from enum import StrEnum

class ManagedAgentsApiErrorAuthUnavailableCode(StrEnum):
    AUTH_UNAVAILABLE = "auth_unavailable"

    def __str__(self) -> str:
        return str(self.value)
