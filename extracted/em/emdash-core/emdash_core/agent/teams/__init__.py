"""Agent Teams — multi-agent orchestration for EmDash.

Coordinate multiple independent agent sessions working together
with shared tasks, inter-agent messaging, and centralized management.

Enable via emdash.config.json:
    { "experimental": { "agent_teams": true } }

Or via environment variable:
    EMDASH_EXPERIMENTAL_AGENT_TEAMS=1
"""

from .manager import is_agent_teams_enabled

__all__ = ["is_agent_teams_enabled"]
