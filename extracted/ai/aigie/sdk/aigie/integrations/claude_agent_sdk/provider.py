"""LLM-provider resolution for the Claude Agent SDK integration."""

from __future__ import annotations

import os


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() not in ("", "0", "false", "no")


_PROVIDER_ROUTING_FLAGS = (
    ("CLAUDE_CODE_USE_BEDROCK", "bedrock"),
    ("CLAUDE_CODE_USE_VERTEX", "vertex_ai"),
    ("CLAUDE_CODE_USE_FOUNDRY", "foundry"),
    ("CLAUDE_CODE_USE_ANTHROPIC_AWS", "anthropic_aws"),
)


def resolve_claude_provider() -> str:
    """Resolve the canonical LLM provider for a Claude Agent SDK run."""
    for flag, provider in _PROVIDER_ROUTING_FLAGS:
        if _truthy(flag):
            return provider
    return "anthropic"
