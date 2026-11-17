from enum import StrEnum

class MainBranchStatus(StrEnum):
    AWAITING_APPROVAL = "awaiting_approval"
    CANCELLED = "cancelled"
    FAILED = "failed"
    NONE = "none"
    PASSED = "passed"
    RUNNING = "running"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
