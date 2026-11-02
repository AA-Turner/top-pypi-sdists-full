from enum import Enum


class AiAgentToolsItemValueType3ToolType(str, Enum):
    QUESTION = "question"

    def __str__(self) -> str:
        return str(self.value)
