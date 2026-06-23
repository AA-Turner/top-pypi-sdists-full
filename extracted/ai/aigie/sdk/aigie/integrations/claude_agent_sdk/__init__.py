"""Claude Agent SDK integration for Aigie (post-ABC).

Public surface — every export below is part of the ABC-compliant integration.

  aigie.init(framework="claude_agent_sdk") triggers @register_adapter
  via the eager import at the bottom of this file. From then on every
  call to ``claude_agent_sdk.query`` / ``ClaudeSDKClient.*`` is wrapped by
  ``ClaudeAgentSDKLifecycle`` and emits spans through
  ``ClaudeAgentSDKNativeCallback`` (a ``SpanEventHandler`` subclass).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

__all__ = [
    # L1/L2/L3 ABC entry points
    "ClaudeAgentSDKAdapter",
    "ClaudeAgentSDKLifecycle",
    "ClaudeAgentSDKNativeCallback",
    # Configuration
    "ClaudeAgentSDKConfig",
    # Cost tracking
    "CLAUDE_MODEL_PRICING",
    "calculate_claude_cost",
    # Session management
    "ClaudeSessionContext",
    "claude_session",
    "clear_session_context",
    "get_or_create_session_context",
    "get_session_context",
]


def __getattr__(name: str) -> Any:
    if name == "ClaudeAgentSDKAdapter":
        from aigie.integrations.claude_agent_sdk.adapter import ClaudeAgentSDKAdapter

        return ClaudeAgentSDKAdapter
    if name == "ClaudeAgentSDKLifecycle":
        from aigie.integrations.claude_agent_sdk.lifecycle import ClaudeAgentSDKLifecycle

        return ClaudeAgentSDKLifecycle
    if name == "ClaudeAgentSDKNativeCallback":
        from aigie.integrations.claude_agent_sdk.native_callback import ClaudeAgentSDKNativeCallback

        return ClaudeAgentSDKNativeCallback
    if name == "ClaudeAgentSDKConfig":
        from aigie.integrations.claude_agent_sdk.config import ClaudeAgentSDKConfig

        return ClaudeAgentSDKConfig
    if name == "calculate_claude_cost":
        from aigie.integrations.claude_agent_sdk.cost_tracking import calculate_claude_cost

        return calculate_claude_cost
    if name == "CLAUDE_MODEL_PRICING":
        from aigie.integrations.claude_agent_sdk.cost_tracking import CLAUDE_MODEL_PRICING

        return CLAUDE_MODEL_PRICING
    if name == "ClaudeSessionContext":
        from aigie.integrations.claude_agent_sdk.session_context import ClaudeSessionContext

        return ClaudeSessionContext
    if name == "claude_session":
        from aigie.integrations.claude_agent_sdk.session_context import claude_session

        return claude_session
    if name == "get_session_context":
        from aigie.integrations.claude_agent_sdk.session_context import get_session_context

        return get_session_context
    if name == "get_or_create_session_context":
        from aigie.integrations.claude_agent_sdk.session_context import (
            get_or_create_session_context,
        )

        return get_or_create_session_context
    if name == "clear_session_context":
        from aigie.integrations.claude_agent_sdk.session_context import clear_session_context

        return clear_session_context
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from aigie.integrations.claude_agent_sdk.adapter import ClaudeAgentSDKAdapter
    from aigie.integrations.claude_agent_sdk.config import ClaudeAgentSDKConfig
    from aigie.integrations.claude_agent_sdk.cost_tracking import (
        CLAUDE_MODEL_PRICING,
        calculate_claude_cost,
    )
    from aigie.integrations.claude_agent_sdk.lifecycle import ClaudeAgentSDKLifecycle
    from aigie.integrations.claude_agent_sdk.native_callback import ClaudeAgentSDKNativeCallback
    from aigie.integrations.claude_agent_sdk.session_context import (
        ClaudeSessionContext,
        claude_session,
        clear_session_context,
        get_or_create_session_context,
        get_session_context,
    )


# Eager — triggers @register_adapter("claude_agent_sdk") at module import.
from aigie.integrations.claude_agent_sdk.adapter import ClaudeAgentSDKAdapter  # noqa: E402,F401
