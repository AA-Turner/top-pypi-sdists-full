from enum import StrEnum

class RunConfigProbeRunDtoStatus(StrEnum):
    CANCELLED = "cancelled"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
