from enum import StrEnum

class ManagedAgentsApiErrorForbiddenCode(StrEnum):
    FORBIDDEN = "forbidden"

    def __str__(self) -> str:
        return str(self.value)
