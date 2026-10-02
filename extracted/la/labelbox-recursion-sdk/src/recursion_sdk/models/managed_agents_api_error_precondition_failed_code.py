from enum import StrEnum

class ManagedAgentsApiErrorPreconditionFailedCode(StrEnum):
    PRECONDITION_FAILED = "precondition_failed"

    def __str__(self) -> str:
        return str(self.value)
