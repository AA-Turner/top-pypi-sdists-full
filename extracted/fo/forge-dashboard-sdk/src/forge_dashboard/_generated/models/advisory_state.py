from enum import StrEnum

class AdvisoryState(StrEnum):
    KNOWN = "known"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
