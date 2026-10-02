from enum import StrEnum

class ResolvedMenuDtoEntriesItemType(StrEnum):
    AGENT_HARNESS = "agent-harness"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
