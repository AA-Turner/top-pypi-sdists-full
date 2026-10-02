from enum import StrEnum

class ReapedRunConfigPageDtoItemsItemType(StrEnum):
    AGENT_HARNESS = "agent-harness"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
