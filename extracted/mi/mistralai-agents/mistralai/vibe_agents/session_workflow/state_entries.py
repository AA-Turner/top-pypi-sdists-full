"""First-party ``StateEntry`` payloads emitted by vibe_agents runtimes."""

from typing import Literal

from mistralai.vibe_agents.session_workflow.task_protocol import (
    SessionInitializedStatePayload,
    StateHistoryEntry,
)

VibeAgentsStateKind = Literal["x-vibe-agent-session-initialized"]

# Compatibility names for callers that import first-party state entries from
# this focused module. The canonical models live in ``task_protocol`` and use
# the Task Protocol `{type, content}` state-payload shape.
AgentSessionInitializedPayload = SessionInitializedStatePayload
AgentSessionInitialized = StateHistoryEntry

__all__ = [
    "AgentSessionInitialized",
    "AgentSessionInitializedPayload",
    "VibeAgentsStateKind",
]
