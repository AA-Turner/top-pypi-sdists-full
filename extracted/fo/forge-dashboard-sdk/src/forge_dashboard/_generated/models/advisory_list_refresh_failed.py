from enum import StrEnum

class AdvisoryListRefreshFailed(StrEnum):
    FAILED = "failed"
    THROTTLED = "throttled"

    def __str__(self) -> str:
        return str(self.value)
