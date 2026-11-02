from enum import Enum


class RuntimeImageBuildStatus(str, Enum):
    BUILDING = "building"
    CANCELLED = "cancelled"
    FAILED = "failed"
    PENDING = "pending"
    RETRYING = "retrying"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
