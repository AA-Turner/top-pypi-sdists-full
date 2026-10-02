from enum import StrEnum

class CostStatsDtoCostByRunTypeItemRunType(StrEnum):
    AGENTIC_GRADING = "agentic_grading"
    CHECK_FIX_CYCLE = "check_fix_cycle"
    GRADE_EXTRACTION = "grade_extraction"
    MANAGED_AGENT_TURN = "managed_agent_turn"
    MCP_TOOL_CALL_GRADING = "mcp_tool_call_grading"
    PROBE_JUDGE = "probe_judge"
    PROGRAMMATIC_GRADING = "programmatic_grading"
    QA = "qa"
    ROLLOUT = "rollout"
    RUBRIC_GRADING = "rubric_grading"
    RUN_CONFIG_PROBE = "run_config_probe"
    RUN_CONFIG_RUN = "run_config_run"
    SOLVER = "solver"
    SYNTHESIZER = "synthesizer"
    TITLE_GENERATION = "title_generation"
    TRANSCRIPT_REFORMAT = "transcript_reformat"
    TRANSCRIPT_SYNTHESIS = "transcript_synthesis"

    def __str__(self) -> str:
        return str(self.value)
