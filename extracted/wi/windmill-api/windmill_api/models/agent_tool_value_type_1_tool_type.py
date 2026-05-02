from enum import Enum


class AgentToolValueType1ToolType(str, Enum):
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
