from enum import StrEnum

class ManagedAgentsCoverageTileHistoryStatus(StrEnum):
    COMPLETE = "complete"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
