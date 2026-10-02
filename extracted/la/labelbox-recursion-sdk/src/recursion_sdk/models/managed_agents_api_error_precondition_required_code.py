from enum import StrEnum

class ManagedAgentsApiErrorPreconditionRequiredCode(StrEnum):
    PRECONDITION_REQUIRED = "precondition_required"

    def __str__(self) -> str:
        return str(self.value)
