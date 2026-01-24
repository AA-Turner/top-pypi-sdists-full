from enum import Enum


class FlowModuleValue2Type8ToolsItemValueType1ToolType(str, Enum):
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
