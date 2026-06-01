"""
Auto-instrumentation module for Aigie SDK.

This module provides automatic instrumentation for:
- LangChain agents and chains
- LangGraph workflows
- Browser-Use browser automation
- Claude Agent SDK sessions
- Google ADK agents
- Strands agents
- DSPy modules
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

import os
from typing import Any, Optional

# Store original methods before patching for proper restoration
_original_methods: dict[str, Any] = {}

# Adapter-backed frameworks (langgraph, claude_agent_sdk, ...) are installed
# by `aigie.integrations.install.install_framework_adapters` directly from
# `Aigie.initialize()` — they have no entry here.
_instrumentation_state = {
    "langchain": False,
    "browser_use": False,
    "google_adk": False,
    "strands": False,
    "openai_agents": False,
    "crewai": False,
    "agno": False,
    "livekit_agents": False,
    "llm": False,
    "tools": False,
    "dspy": False,
    "haystack": False,
    "pipecat": False,
    "infra": False,
}


def enable_all() -> None:
    """Enable auto-instrumentation for legacy (non-adapter-backed) frameworks.

    Adapter-backed frameworks are installed separately via
    ``aigie.integrations.install.install_framework_adapters``.
    """
    enable_langchain()
    enable_browser_use()
    enable_google_adk()
    enable_strands()
    enable_openai_agents()
    enable_crewai()
    enable_agno()
    enable_livekit_agents()
    enable_llm()
    enable_tools()
    enable_dspy()
    enable_haystack()
    enable_pipecat()
    enable_infra()


def enable_langchain() -> None:
    """Enable LangChain auto-instrumentation."""
    if _instrumentation_state["langchain"]:
        return

    try:
        from .langchain import patch_langchain

        patch_langchain()
        _instrumentation_state["langchain"] = True
    except ImportError:
        pass  # LangChain not installed


def enable_browser_use() -> None:
    """Enable Browser-Use auto-instrumentation."""
    if _instrumentation_state["browser_use"]:
        return

    try:
        from ..integrations.browser_use.auto_instrument import patch_browser_use

        patch_browser_use()
        _instrumentation_state["browser_use"] = True
    except ImportError:
        pass  # browser-use not installed


def enable_google_adk() -> None:
    """Enable Google ADK auto-instrumentation."""
    if _instrumentation_state["google_adk"]:
        return

    try:
        from ..integrations.google_adk.auto_instrument import patch_google_adk

        patch_google_adk()
        _instrumentation_state["google_adk"] = True
    except ImportError:
        pass  # google-adk not installed


def enable_strands() -> None:
    """Enable Strands Agents auto-instrumentation."""
    if _instrumentation_state["strands"]:
        return

    try:
        from ..integrations.strands.auto_instrument import patch_strands

        patch_strands()
        _instrumentation_state["strands"] = True
    except ImportError:
        pass  # strands-agents not installed


def enable_openai_agents() -> None:
    """Enable OpenAI Agents SDK auto-instrumentation."""
    if _instrumentation_state["openai_agents"]:
        return

    try:
        from ..integrations.openai_agents.auto_instrument import patch_openai_agents

        patch_openai_agents()
        _instrumentation_state["openai_agents"] = True
    except ImportError:
        pass


def enable_crewai() -> None:
    """Enable CrewAI auto-instrumentation."""
    if _instrumentation_state["crewai"]:
        return

    try:
        from ..integrations.crewai.auto_instrument import patch_crewai

        patch_crewai()
        _instrumentation_state["crewai"] = True
    except ImportError:
        pass


def enable_agno() -> None:
    """Enable Agno auto-instrumentation."""
    if _instrumentation_state["agno"]:
        return

    try:
        from ..integrations.agno.auto_instrument import patch_agno

        patch_agno()
        _instrumentation_state["agno"] = True
    except ImportError:
        pass


def enable_livekit_agents() -> None:
    """Enable LiveKit Agents auto-instrumentation."""
    if _instrumentation_state["livekit_agents"]:
        return

    # Opt-in like pipecat — voice framework, don't init unless present
    try:
        from ..integrations.livekit_agents.auto_instrument import patch_livekit_agents

        patch_livekit_agents()
        _instrumentation_state["livekit_agents"] = True
    except ImportError:
        pass


def enable_llm() -> None:
    """Enable LLM client auto-instrumentation."""
    if _instrumentation_state["llm"]:
        return

    try:
        from .llm import patch_all_llms

        patch_all_llms()
        _instrumentation_state["llm"] = True
    except ImportError:
        pass


def enable_tools() -> None:
    """Enable tool call auto-instrumentation."""
    if _instrumentation_state["tools"]:
        return

    try:
        from .tools import patch_tools

        patch_tools()
        _instrumentation_state["tools"] = True
    except ImportError:
        pass


def enable_dspy() -> None:
    """Enable DSPy auto-instrumentation."""
    if _instrumentation_state["dspy"]:
        return

    try:
        from .dspy import patch_dspy

        patch_dspy()
        _instrumentation_state["dspy"] = True
    except ImportError:
        pass  # DSPy not installed


def enable_haystack() -> None:
    """Enable Haystack auto-instrumentation."""
    if _instrumentation_state["haystack"]:
        return

    try:
        from .haystack import patch_haystack

        patch_haystack()
        _instrumentation_state["haystack"] = True
    except ImportError:
        pass  # Haystack not installed


def enable_pipecat() -> None:
    """Enable Pipecat auto-instrumentation."""
    if _instrumentation_state.get("pipecat"):
        return

    # Opt-in by default to avoid initializing Pipecat in non-voice apps.
    env_override = os.getenv("AIGIE_PIPECAT_AUTO_INSTRUMENT")
    if env_override is not None:
        should_enable = env_override.lower() in ("true", "1", "yes")
    else:
        env_enabled = os.getenv("AIGIE_PIPECAT_ENABLED")
        should_enable = env_enabled is not None and env_enabled.lower() in ("true", "1", "yes")

    if not should_enable:
        return

    try:
        from ..integrations.pipecat.auto_instrument import patch_pipecat

        patch_pipecat()
        _instrumentation_state["pipecat"] = True
    except ImportError:
        pass  # pipecat-ai not installed


def enable_infra() -> None:
    """Enable infrastructure auto-instrumentation (DB, HTTP, cache via OTel bridge)."""
    if _instrumentation_state["infra"]:
        return

    # Only instrument if OTel SDK is available
    try:
        from .infra import detect_and_instrument
        from .span_enricher import _setup_span_enricher

        if not _setup_span_enricher():
            return  # OTel SDK not installed or bridge setup failed

        # Mark as attempted even if no libraries found (prevents re-running)
        _instrumentation_state["infra"] = True

        detected = detect_and_instrument()
        if detected:
            import logging

            logging.getLogger(__name__).debug(
                "Aigie: auto-instrumented infrastructure: %s", ", ".join(detected)
            )
    except ImportError:
        pass  # OTel SDK not installed — skip silently


def disable_all() -> None:
    """Disable all auto-instrumentation and restore original methods."""
    # Uninstrument OTel-based infrastructure instrumentation
    try:
        from .infra import uninstrument_all as uninstrument_infra

        uninstrument_infra()
    except Exception:  # noqa: BLE001, S110 - never block disable_all due to infra teardown failure
        pass
    try:
        from .span_enricher import _teardown_span_enricher

        _teardown_span_enricher()
    except Exception:  # noqa: BLE001, S110 - span enricher teardown is best-effort
        pass

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
