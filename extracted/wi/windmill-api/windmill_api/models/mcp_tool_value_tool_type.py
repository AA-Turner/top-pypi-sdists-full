from enum import Enum


class McpToolValueToolType(str, Enum):
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
