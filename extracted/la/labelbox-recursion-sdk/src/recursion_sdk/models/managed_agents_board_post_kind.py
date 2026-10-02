from enum import StrEnum

class ManagedAgentsBoardPostKind(StrEnum):
    DECISION = "decision"
    NOTICE = "notice"
    RECOMMENDATION = "recommendation"

    def __str__(self) -> str:
        return str(self.value)
