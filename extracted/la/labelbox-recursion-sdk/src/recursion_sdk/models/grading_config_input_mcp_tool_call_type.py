from enum import StrEnum

class GradingConfigInputMcpToolCallType(StrEnum):
    MCP_TOOL_CALL = "mcp_tool_call"

    def __str__(self) -> str:
        return str(self.value)
