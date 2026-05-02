from enum import Enum


class AiAgentToolsItemValueType2ToolType(str, Enum):
    WEBSEARCH = "websearch"

    def __str__(self) -> str:
        return str(self.value)
