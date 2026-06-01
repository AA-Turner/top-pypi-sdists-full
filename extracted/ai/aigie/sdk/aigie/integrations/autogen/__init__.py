"""
Aigie AutoGen/AG2 Integration

Full workflow tracing for AutoGen/AG2 multi-agent conversations with the Aigie SDK.
Traces agent conversations, group chats, tool calls, and code execution.

Note: AutoGen was rebranded to AG2. This integration supports both package names.

Usage (Auto-Instrumentation - Recommended):
    import aigie
    from aigie.integrations.autogen import patch_autogen

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Enable auto-instrumentation
    patch_autogen()

    # Now all AutoGen/AG2 operations are automatically traced
    from autogen import ConversableAgent, AssistantAgent, UserProxyAgent
    # or: from ag2 import ConversableAgent, AssistantAgent, UserProxyAgent

    assistant = AssistantAgent("assistant", llm_config={...})
    user = UserProxyAgent("user")
    result = user.initiate_chat(assistant, message="Hello")  # Automatically traced!

Usage (Manual Callback Handler):
    from aigie.integrations.autogen import AutoGenHandler

    # Create handler with trace context
    async with aigie.trace("Agent Conversation") as trace:
        handler = AutoGenHandler(trace_name="AI Assistant Chat")
        handler.set_trace_context(trace)

        await handler.handle_conversation_start(
            initiator="user",
            recipient="assistant",
            message="Hello"
        )

        # ... run conversation ...

        await handler.handle_conversation_end(success=True, result=result)

Usage (Configuration):
    from aigie.integrations.autogen import AutoGenConfig, patch_autogen

    # Custom configuration
    config = AutoGenConfig(
        trace_conversations=True,
        trace_agents=True,
        trace_code_execution=True,
        conversation_timeout=3600.0,  # 1 hour timeout
        max_retries=5,
    )

    # Apply configuration (config is used by handlers)
    patch_autogen()
"""

__all__ = [
    # Handler
    "AutoGenHandler",
    # Configuration
    "AutoGenConfig",
    # Cost tracking
    "AUTOGEN_MODEL_PRICING",
    "get_autogen_cost",
    "extract_tokens_from_response",
    "extract_model_from_agent",
    "aggregate_conversation_costs",
    # Auto-instrumentation
    "patch_autogen",
    "unpatch_autogen",
    "is_autogen_patched",
    # Utilities
    "is_autogen_available",
    "get_autogen_version",
    "safe_str",
    "extract_agent_info",
    "extract_message_info",
    "extract_conversation_summary",
    "extract_group_chat_info",
    "get_conversation_participants",
    "mask_sensitive_content",
    # Retry/Timeout utilities
    "RetryExhaustedError",
    "TimeoutExceededError",
    "ConversationError",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_decorator",
    "RetryContext",
    "ConversationRetryContext",
]

from typing import TYPE_CHECKING, Any


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "AutoGenHandler":
        from .handler import AutoGenHandler

        return AutoGenHandler

    # Configuration
    if name == "AutoGenConfig":
        from .config import AutoGenConfig

        return AutoGenConfig

    # Cost tracking
    if name == "AUTOGEN_MODEL_PRICING":
        from .cost_tracking import AUTOGEN_MODEL_PRICING

        return AUTOGEN_MODEL_PRICING

    if name == "get_autogen_cost":
        from .cost_tracking import get_autogen_cost

        return get_autogen_cost

    if name == "extract_tokens_from_response":
        from .cost_tracking import extract_tokens_from_response

        return extract_tokens_from_response

    if name == "extract_model_from_agent":
        from .cost_tracking import extract_model_from_agent

        return extract_model_from_agent

    if name == "aggregate_conversation_costs":
        from .cost_tracking import aggregate_conversation_costs

        return aggregate_conversation_costs

    # Auto-instrumentation
    if name == "patch_autogen":
        from .auto_instrument import patch_autogen

        return patch_autogen

    if name == "unpatch_autogen":
        from .auto_instrument import unpatch_autogen

        return unpatch_autogen

    if name == "is_autogen_patched":
        from .auto_instrument import is_autogen_patched

        return is_autogen_patched

    # Utilities
    if name == "is_autogen_available":
        from .utils import is_autogen_available

        return is_autogen_available

    if name == "get_autogen_version":
        from .utils import get_autogen_version

        return get_autogen_version

    if name == "safe_str":
        from .utils import safe_str

        return safe_str

    if name == "extract_agent_info":
        from .utils import extract_agent_info

        return extract_agent_info

    if name == "extract_message_info":
        from .utils import extract_message_info

        return extract_message_info

    if name == "extract_conversation_summary":
        from .utils import extract_conversation_summary

        return extract_conversation_summary

    if name == "extract_group_chat_info":
        from .utils import extract_group_chat_info

        return extract_group_chat_info

    if name == "get_conversation_participants":
        from .utils import get_conversation_participants

        return get_conversation_participants

    if name == "mask_sensitive_content":
        from .utils import mask_sensitive_content

        return mask_sensitive_content

    # Retry/Timeout utilities
    if name == "RetryExhaustedError":
        from ..._legacy_stubs import RetryExhaustedError

        return RetryExhaustedError

    if name == "TimeoutExceededError":
        from ..._legacy_stubs import TimeoutExceededError

        return TimeoutExceededError

    if name == "ConversationError":
        from ..._legacy_stubs import ConversationError

        return ConversationError

    if name == "with_timeout":
        from ..._legacy_stubs import with_timeout

        return with_timeout

    if name == "with_retry":
        from ..._legacy_stubs import with_retry

        return with_retry

    if name == "with_timeout_and_retry":
        from ..._legacy_stubs import with_timeout_and_retry

        return with_timeout_and_retry

    if name == "retry_decorator":
        from ..._legacy_stubs import retry_decorator

        return retry_decorator

    if name == "RetryContext":
        from ..._legacy_stubs import RetryContext

        return RetryContext

    if name == "ConversationRetryContext":
        from ..._legacy_stubs import ConversationRetryContext

        return ConversationRetryContext

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_autogen_patched,
        patch_autogen,
        unpatch_autogen,
    )
    from .config import AutoGenConfig
    from .cost_tracking import (
        AUTOGEN_MODEL_PRICING,
        aggregate_conversation_costs,
        extract_model_from_agent,
        extract_tokens_from_response,
        get_autogen_cost,
    )
    from .handler import AutoGenHandler
    from ..._legacy_stubs import (
        ConversationError,
        ConversationRetryContext,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from .utils import (
        extract_agent_info,
        extract_conversation_summary,
        extract_group_chat_info,
        extract_message_info,
        get_autogen_version,
        get_conversation_participants,
        is_autogen_available,
        mask_sensitive_content,
        safe_str,
    )
