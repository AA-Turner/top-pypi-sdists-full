from enum import Enum


class PipelineRunStatus(str, Enum):
    FAILED = "failed"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
