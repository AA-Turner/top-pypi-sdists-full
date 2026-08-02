"""Vibe SDK Agent module."""

from importlib import import_module
from typing import Any

__all__ = [
    "Agent",
    "AgentConfig",
    "AgentTaskFactory",
    "AsyncSession",
    "IdFactory",
    "SkillDefinition",
    "SyncSession",
    "create_agent_task",
    "default_id_factory",
    "get_from_env",
]

_LAZY_EXPORTS = {
    "Agent": "mistralai.vibe.sdk.agent.agent",
    "AgentConfig": "mistralai.vibe.sdk.agent.config",
    "AgentTaskFactory": "mistralai.vibe.sdk.agent.tasks.helpers",
    "AsyncSession": "mistralai.vibe.sdk.agent.sessions",
    "IdFactory": "mistralai.vibe.sdk.agent.sessions",
    "SkillDefinition": "mistralai.vibe.sdk.agent.skills",
    "SyncSession": "mistralai.vibe.sdk.agent.sessions",
    "create_agent_task": "mistralai.vibe.sdk.agent.tasks.helpers",
    "default_id_factory": "mistralai.vibe.sdk.agent.sessions",
    "get_from_env": "mistralai.vibe.sdk.agent.config",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
