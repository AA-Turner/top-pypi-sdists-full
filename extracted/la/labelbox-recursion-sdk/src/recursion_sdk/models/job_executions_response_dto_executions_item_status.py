from enum import StrEnum

class JobExecutionsResponseDtoExecutionsItemStatus(StrEnum):
    FAILED = "failed"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
