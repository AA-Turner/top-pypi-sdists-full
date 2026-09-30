from enum import Enum


class GetForkCreationStatusResponse200Status(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
