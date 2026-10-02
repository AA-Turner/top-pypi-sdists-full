from enum import StrEnum

class ManagedAgentsApiErrorNotFoundCode(StrEnum):
    NOT_FOUND = "not_found"

    def __str__(self) -> str:
        return str(self.value)
