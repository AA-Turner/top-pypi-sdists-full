from enum import Enum


class ToolValueType1ToolType(str, Enum):
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
