from enum import StrEnum

class QaJobResponseDtoChildRunsItemStrategy(StrEnum):
    AGENTIC = "agentic"
    MCP_TOOL_CALL = "mcp_tool_call"
    PROGRAMMATIC = "programmatic"
    RUBRIC = "rubric"
    RUN_CONFIG = "run_config"

    def __str__(self) -> str:
        return str(self.value)
