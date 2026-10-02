from enum import StrEnum

class ProblemRunExecutionEvidenceDtoGradersItemStrategy(StrEnum):
    AGENTIC = "agentic"
    COMPUTE_EXEC = "compute_exec"
    MCP_TOOL_CALL = "mcp_tool_call"
    PROGRAMMATIC = "programmatic"
    RUBRIC = "rubric"

    def __str__(self) -> str:
        return str(self.value)
