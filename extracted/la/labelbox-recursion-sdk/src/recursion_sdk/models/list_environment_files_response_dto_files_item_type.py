from enum import StrEnum

class ListEnvironmentFilesResponseDtoFilesItemType(StrEnum):
    AGENT_INPUT = "agent-input"
    INSTRUCTIONS = "instructions"

    def __str__(self) -> str:
        return str(self.value)
