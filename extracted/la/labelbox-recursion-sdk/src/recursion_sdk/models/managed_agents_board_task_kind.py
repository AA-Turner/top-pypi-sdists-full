from enum import StrEnum

class ManagedAgentsBoardTaskKind(StrEnum):
    EXPLORE = "explore"
    REVIEW = "review"
    TASK = "task"

    def __str__(self) -> str:
        return str(self.value)
