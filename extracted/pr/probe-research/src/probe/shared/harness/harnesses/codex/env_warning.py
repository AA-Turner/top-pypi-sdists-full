"""Codex's warning in probe session status when its hooks could not read the launch state."""

from __future__ import annotations
from .....sdk import agent_session, session_marker


def _codex_env_warning(session_id: str) -> str | None:
    """`codex_hooks.ENV_WARNING` for a Codex session that took the shipped
    default where its hooks could not read the state Codex was started with
    (issue 3620: no /proc to read it from), else None. A machine default the
    researcher set is their choice for these sessions too: nothing to say."""
    from .hooks import ENV_WARNING, launch_env_unreadable
    from ...plugins import CODEX

    agent = agent_session.detect_agent()
    if agent is None or agent.label != CODEX or not launch_env_unreadable():
        return None
    if session_marker.resolve_state_default(None)[1] != "shipped":
        return None
    return ENV_WARNING if session_marker.state_source_label(session_id) == session_marker.SOURCE_DEFAULT else None
