from enum import StrEnum

class ManagedAgentsAgentMemorySummaryState(StrEnum):
    DELAYED = "delayed"
    IDLE = "idle"
    UPDATING = "updating"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)
