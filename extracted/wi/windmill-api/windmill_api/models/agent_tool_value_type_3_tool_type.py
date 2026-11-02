from enum import Enum


class AgentToolValueType3ToolType(str, Enum):
    QUESTION = "question"

    def __str__(self) -> str:
        return str(self.value)
