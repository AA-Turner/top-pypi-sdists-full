from enum import StrEnum

class RolloutBatchResultsResponseDtoOutputType0Verdict(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

    def __str__(self) -> str:
        return str(self.value)
