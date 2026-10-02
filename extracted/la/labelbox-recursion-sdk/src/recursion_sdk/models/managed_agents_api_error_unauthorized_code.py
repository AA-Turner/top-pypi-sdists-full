from enum import StrEnum

class ManagedAgentsApiErrorUnauthorizedCode(StrEnum):
    UNAUTHORIZED = "unauthorized"

    def __str__(self) -> str:
        return str(self.value)
