from enum import StrEnum

class RunConfigListItemListDtoItemType(StrEnum):
    AGENT_HARNESS = "agent-harness"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
