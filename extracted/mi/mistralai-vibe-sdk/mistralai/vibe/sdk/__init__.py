"""Vibe SDK high-level agent interface."""

from importlib import import_module
from typing import Any

__all__ = [
    "Agent",
    "AgentConfig",
    "AgentTaskFactory",
    "AsyncSession",
    "SkillDefinition",
    "SyncSession",
    "create_agent_task",
    "get_from_env",
]

_LAZY_EXPORTS = {
    "Agent": "mistralai.vibe.sdk.agent",
    "AgentConfig": "mistralai.vibe.sdk.agent",
    "AgentTaskFactory": "mistralai.vibe.sdk.agent",
    "AsyncSession": "mistralai.vibe.sdk.agent",
    "SkillDefinition": "mistralai.vibe.sdk.agent",
    "SyncSession": "mistralai.vibe.sdk.agent",
    "create_agent_task": "mistralai.vibe.sdk.agent",
    "get_from_env": "mistralai.vibe.sdk.agent",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
