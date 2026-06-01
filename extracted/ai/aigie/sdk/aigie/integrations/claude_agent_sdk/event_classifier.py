"""Pure event-classification rules for the Claude Agent SDK integration."""

from __future__ import annotations

from enum import Enum
from typing import Any


class EventKind(str, Enum):
    LLM = "llm"
    TOOL = "tool"
    SUBGRAPH_WORKFLOW = "subgraph_workflow"
    WORKFLOW_END = "workflow_end"
    SYSTEM = "system"
    SKIP = "skip"


class ClaudeAgentSDKEventClassifier:
    """Maps SDK message/tool types to EventKinds. Stateless and pure."""

    def classify_message_kind(
        self, message_type: str, payload: dict[str, Any]
    ) -> EventKind:
        match message_type:
            case "AssistantMessage":
                return EventKind.LLM
            case "ToolUseBlock" | "ToolResultBlock":
                return EventKind.TOOL
            case "ResultMessage":
                return EventKind.WORKFLOW_END
            case "SystemMessage":
                return EventKind.SYSTEM
            case _:
                return EventKind.SKIP

    def classify_tool_use(self, tool_use: dict[str, Any]) -> EventKind:
        name = tool_use.get("name")
        input_ = tool_use.get("input") or {}
        if (
            name in ("Task", "Agent")
            and isinstance(input_, dict)
            and input_.get("subagent_type")
        ):
            return EventKind.SUBGRAPH_WORKFLOW
        return EventKind.TOOL
