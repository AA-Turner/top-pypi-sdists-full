from enum import StrEnum

class ResolvedRunConfigDtoType(StrEnum):
    AGENT_HARNESS = "agent-harness"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
