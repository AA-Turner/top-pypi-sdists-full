from enum import Enum


class GetApprovalStepDetailResponse200Status(str, Enum):
    FAILED = "failed"
    NOT_REACHED = "not_reached"
    NOT_RESUMED = "not_resumed"
    RESUMED = "resumed"
    SKIPPED = "skipped"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)
