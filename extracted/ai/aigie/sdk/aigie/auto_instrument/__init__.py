"""
Auto-instrumentation module for Aigie SDK.

This module provides automatic instrumentation for:
- LangChain agents and chains
- LangGraph workflows
- Claude Agent SDK sessions
- LLM clients (OpenAI, Anthropic, Gemini)
- Tool calls
- Automatic trace creation

Usage:
    from aigie import Aigie

    # Simple init - automatically enables all instrumentation
    aigie = Aigie(api_url="https://app.aigie.io/api", api_key="your-key")
    await aigie.initialize()

    # All frameworks are now automatically traced
"""

from typing import Any

# Store original methods before patching for proper restoration
_original_methods: dict[str, Any] = {}

# Adapter-backed frameworks (langgraph, claude_agent_sdk, ...) are installed
# by `aigie.integrations.install.install_framework_adapters` directly from
# `Aigie.initialize()` — they have no entry here.
_instrumentation_state = {
    "llm": False,
    "tools": False,
    "haystack": False,
}


def enable_all() -> None:
    """Enable auto-instrumentation for legacy (non-adapter-backed) frameworks.

    Adapter-backed frameworks (LangChain, LangGraph, Claude Agent SDK) are
    installed separately via
    ``aigie.integrations.install.install_framework_adapters``.
    """
    enable_llm()
    enable_tools()
    enable_haystack()


def enable_llm() -> None:
    """Enable LLM client auto-instrumentation."""
    if _instrumentation_state["llm"]:
        return

    try:
        from aigie.auto_instrument.llm import patch_all_llms

        patch_all_llms()
        _instrumentation_state["llm"] = True
    except ImportError:
        pass


def enable_tools() -> None:
    """Enable tool call auto-instrumentation."""
    if _instrumentation_state["tools"]:
        return

    try:
        from aigie.auto_instrument.tools import patch_tools

        patch_tools()
        _instrumentation_state["tools"] = True
    except ImportError:
        pass


def enable_haystack() -> None:
    """Enable Haystack auto-instrumentation."""
    if _instrumentation_state["haystack"]:
        return

    try:
        from aigie.auto_instrument.haystack import patch_haystack

        patch_haystack()
        _instrumentation_state["haystack"] = True
    except ImportError:
        pass  # Haystack not installed


def disable_all() -> None:
    """Disable all auto-instrumentation and restore original methods."""
    # Restore any stored original methods
    import contextlib as _contextlib

    for _key, (target_obj, attr_name, original) in list(_original_methods.items()):
        with _contextlib.suppress(Exception):
            setattr(target_obj, attr_name, original)

    _original_methods.clear()

    # Reset all state flags
    for key in _instrumentation_state:
        _instrumentation_state[key] = False


def is_enabled(framework: str) -> bool:
    """Check if instrumentation is enabled for a framework."""
    return _instrumentation_state.get(framework, False)
