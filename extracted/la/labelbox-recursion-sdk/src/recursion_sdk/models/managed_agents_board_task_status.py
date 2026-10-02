from enum import StrEnum

class ManagedAgentsBoardTaskStatus(StrEnum):
    BLOCKED = "blocked"
    CLAIMED = "claimed"
    DONE = "done"
    DROPPED = "dropped"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
