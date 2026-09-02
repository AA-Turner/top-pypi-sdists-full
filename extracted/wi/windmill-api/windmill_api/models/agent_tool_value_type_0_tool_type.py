from enum import Enum


class AgentToolValueType0ToolType(str, Enum):
    FLOWMODULE = "flowmodule"

    def __str__(self) -> str:
        return str(self.value)
