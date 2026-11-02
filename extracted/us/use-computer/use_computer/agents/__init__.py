"""Optional computer-use agents.

Install provider-backed agents with `use-computer[agents]`.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from use_computer.agents.core import AgentRunOptions, AgentRunResult, AgentUsage

_LAZY_EXPORTS = {
    "AnthropicComputerAgent": (
        "use_computer.agents.providers.anthropic",
        "AnthropicComputerAgent",
    ),
    "AnthropicCUAAgent": ("use_computer.agents.providers.anthropic", "AnthropicCUAAgent"),
    "DebugComputerAgent": ("use_computer.agents.debug.agent", "DebugComputerAgent"),
    "DebugCUAAgent": ("use_computer.agents.debug.agent", "DebugCUAAgent"),
    "GeminiComputerAgent": ("use_computer.agents.providers.gemini", "GeminiComputerAgent"),
    "GeminiCUAAgent": ("use_computer.agents.providers.gemini", "GeminiCUAAgent"),
    "GenericComputerAgent": ("use_computer.agents.providers.generic", "GenericComputerAgent"),
    "GenericCUAAgent": ("use_computer.agents.providers.generic", "GenericCUAAgent"),
    "OpenAIComputerAgent": ("use_computer.agents.providers.openai", "OpenAIComputerAgent"),
    "OpenAICUAAgent": ("use_computer.agents.providers.openai", "OpenAICUAAgent"),
    "OSWorldAgent": ("use_computer.agents.providers.osworld", "OSWorldAgent"),
    "OSWorldComputerAgent": ("use_computer.agents.providers.osworld", "OSWorldComputerAgent"),
}

__all__ = [
    "AgentRunOptions",
    "AgentRunResult",
    "AgentUsage",
    *_LAZY_EXPORTS,
]


def __getattr__(name: str) -> Any:
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(name)
    module_name, attr = target
    try:
        module = import_module(module_name)
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            f"{name} requires optional agent dependencies. Install `use-computer[agents]`."
        ) from exc
    value = getattr(module, attr)
    globals()[name] = value
    return value
