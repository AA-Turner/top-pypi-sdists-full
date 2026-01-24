from enum import Enum


class ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType1Type(str, Enum):
    MCP_TOOL_CALL = "mcp_tool_call"

    def __str__(self) -> str:
        return str(self.value)
