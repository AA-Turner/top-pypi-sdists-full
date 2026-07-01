"""
cvc.adapters.capabilities — Capability matrix for LLM adapters.

Every adapter declares what it can do. The registry exposes the matrix so the
gateway, the agent loop, and the dashboard can ask: "which brain supports
vision + function calling + streaming right now?"
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class Capability(str, Enum):
    """The set of features an adapter may support."""

    CHAT = "chat"                       # basic chat completion
    STREAMING = "streaming"             # token-by-token streaming
    FUNCTION_CALLING = "function_calling"  # native tool/function calls
    VISION = "vision"                   # image inputs
    JSON_MODE = "json_mode"             # structured JSON output
    SYSTEM_MESSAGES = "system_messages"  # system role support
    EMBEDDINGS = "embeddings"           # text embedding endpoint
    LOCAL = "local"                     # runs on-device (no network egress)
    OPEN_SOURCE = "open_source"         # model weights are public
    CONTEXT_1M = "context_1m"           # supports ≥1M token context
    THINKING = "thinking"               # extended thinking / reasoning mode
    CODE_EXEC = "code_exec"             # provider-hosted code execution


# Static capability hints per adapter (best-effort, refined at runtime by
# live health probes). Unknown adapters get CHAT only.
_STATIC_CAPABILITIES: dict[str, set[Capability]] = {
    "openai": {Capability.CHAT, Capability.STREAMING, Capability.FUNCTION_CALLING,
               Capability.VISION, Capability.JSON_MODE, Capability.SYSTEM_MESSAGES,
               Capability.EMBEDDINGS, Capability.CONTEXT_1M, Capability.THINKING},
    "anthropic": {Capability.CHAT, Capability.STREAMING, Capability.FUNCTION_CALLING,
                  Capability.VISION, Capability.SYSTEM_MESSAGES, Capability.CONTEXT_1M,
                  Capability.THINKING},
    "google": {Capability.CHAT, Capability.STREAMING, Capability.FUNCTION_CALLING,
               Capability.VISION, Capability.JSON_MODE, Capability.SYSTEM_MESSAGES,
               Capability.EMBEDDINGS, Capability.CONTEXT_1M, Capability.THINKING},
    "vertex": {Capability.CHAT, Capability.STREAMING, Capability.FUNCTION_CALLING,
               Capability.VISION, Capability.JSON_MODE, Capability.SYSTEM_MESSAGES,
               Capability.EMBEDDINGS},
    "copilot": {Capability.CHAT, Capability.STREAMING, Capability.FUNCTION_CALLING,
                Capability.JSON_MODE, Capability.SYSTEM_MESSAGES},
    "github": {Capability.CHAT, Capability.STREAMING, Capability.JSON_MODE,
               Capability.SYSTEM_MESSAGES},
    "ollama": {Capability.CHAT, Capability.STREAMING, Capability.VISION,
               Capability.JSON_MODE, Capability.SYSTEM_MESSAGES, Capability.LOCAL,
               Capability.OPEN_SOURCE},
    "lmstudio": {Capability.CHAT, Capability.STREAMING, Capability.VISION,
                 Capability.JSON_MODE, Capability.SYSTEM_MESSAGES, Capability.LOCAL,
                 Capability.OPEN_SOURCE},
    "minimax": {Capability.CHAT, Capability.STREAMING, Capability.FUNCTION_CALLING,
                Capability.VISION, Capability.JSON_MODE, Capability.SYSTEM_MESSAGES},
    "nvidia": {Capability.CHAT, Capability.STREAMING, Capability.FUNCTION_CALLING,
               Capability.JSON_MODE, Capability.SYSTEM_MESSAGES, Capability.EMBEDDINGS},
}


@dataclass
class CapabilityReport:
    """The capability surface of one adapter."""

    adapter_id: str
    display_name: str
    capabilities: list[str] = field(default_factory=list)
    healthy: bool = False
    last_error: str = ""
    last_check: float = 0.0
    supports_streaming: bool = False
    supports_tools: bool = False
    supports_vision: bool = False
    supports_local: bool = False
    default_model: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def get_static_capabilities(adapter_id: str) -> set[Capability]:
    """Best-effort capability guess from the adapter id alone."""
    return _STATIC_CAPABILITIES.get(adapter_id.lower(), {Capability.CHAT})


def negotiate(
    required: set[Capability],
    available_reports: list[CapabilityReport],
) -> CapabilityReport | None:
    """
    Return the first adapter that supports ALL required capabilities, or None.

    Tries in the order given — so the caller controls preference (e.g. local
    first, then cloud).
    """
    for report in available_reports:
        caps = set(report.capabilities)
        if required.issubset(caps):
            return report
    return None