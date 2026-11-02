"""Private metadata shared by the Agents SDK Workflow and remote transport."""

HARNESS_TURN_ID_ANNOTATION = "x-mistral-harness-turn-id"
HARNESS_TOOL_KIND_ANNOTATION = "x-mistral-harness-tool-kind"
HARNESS_COMMAND_OUTCOME_STATE = "x-mistral-harness-command-outcome"

__all__ = [
    "HARNESS_COMMAND_OUTCOME_STATE",
    "HARNESS_TOOL_KIND_ANNOTATION",
    "HARNESS_TURN_ID_ANNOTATION",
]
