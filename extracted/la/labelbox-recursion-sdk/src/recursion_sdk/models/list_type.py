from enum import StrEnum

class ListType(StrEnum):
    AGENT_INPUT = "agent-input"
    INSTRUCTIONS = "instructions"

    def __str__(self) -> str:
        return str(self.value)
