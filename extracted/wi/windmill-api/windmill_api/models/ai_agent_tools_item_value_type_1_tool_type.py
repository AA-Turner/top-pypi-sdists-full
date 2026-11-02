from enum import Enum


class AiAgentToolsItemValueType1ToolType(str, Enum):
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
