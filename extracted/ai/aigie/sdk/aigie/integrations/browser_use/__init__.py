"""
Aigie Browser-Use Integration

Full workflow tracing for browser-use with the Aigie SDK.
Traces LLM calls, agent steps, and browser actions.

Usage (Manual Wrapping):
    from aigie.integrations.browser_use import TracedAgent, TracedBrowser
    from browser_use import ChatBrowserUse
    import aigie

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Create traced components
    browser = TracedBrowser()
    llm = ChatBrowserUse()

    # Run with full tracing
    agent = TracedAgent(
        task="Search for restaurants in NYC",
        llm=llm,
        browser=browser,
        aigie=aigie_client,
    )
    result = await agent.run()

Usage (Auto-Instrumentation - Recommended):
    import aigie
    from aigie.integrations.browser_use import patch_browser_use

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Enable auto-instrumentation
    patch_browser_use()

    # Now all browser-use operations are automatically traced
    from browser_use import Agent, ChatBrowserUse

    agent = Agent(task="...", llm=ChatBrowserUse())
    result = await agent.run()  # Automatically traced!

Usage (Handler Pattern - like LangGraph):
    from aigie.integrations.browser_use import BrowserUseHandler
    from browser_use import Agent, ChatBrowserUse

    # Create handler
    handler = BrowserUseHandler(
        trace_name="My Browser Task",
        metadata={"task_type": "research"},
        capture_screenshots=True,
    )

    # Use handler with agent (manual integration)
    agent = Agent(task="...", llm=ChatBrowserUse())
    await handler.handle_task_start(task="...", max_steps=100)
    result = await agent.run()
    await handler.handle_task_end(success=True, result=result)
"""

__all__ = [
    # Main wrappers
    "TracedAgent",
    "TracedBrowser",
    "TracedLLM",
    # Handler (like LangGraphHandler)
    "BrowserUseHandler",
    # Configuration
    "BrowserUseConfig",
    # Cost tracking
    "BROWSER_USE_MODEL_PRICING",
    "get_browser_use_cost",
    "extract_tokens_from_response",
    # Auto-instrumentation
    "patch_browser_use",
    "unpatch_browser_use",
    "is_browser_use_patched",
    # Utilities
    "wrap_browser_use_llm",
    "is_browser_use_available",
    # Retry/Timeout utilities
    "RetryExhaustedError",
    "TimeoutExceededError",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_decorator",
    "RetryContext",
]

from typing import TYPE_CHECKING, Any


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Main wrappers
    if name == "TracedAgent":
        from .agent import TracedAgent

        return TracedAgent

    if name == "TracedBrowser":
        from .browser import TracedBrowser

        return TracedBrowser

    if name == "TracedLLM":
        from .llm import TracedLLM

        return TracedLLM

    # Handler
    if name == "BrowserUseHandler":
        from .handler import BrowserUseHandler

        return BrowserUseHandler

    # Configuration
    if name == "BrowserUseConfig":
        from .config import BrowserUseConfig

        return BrowserUseConfig

    # Cost tracking
    if name == "BROWSER_USE_MODEL_PRICING":
        from .cost_tracking import BROWSER_USE_MODEL_PRICING

        return BROWSER_USE_MODEL_PRICING

    if name == "get_browser_use_cost":
        from .cost_tracking import get_browser_use_cost

        return get_browser_use_cost

    if name == "extract_tokens_from_response":
        from .cost_tracking import extract_tokens_from_response

        return extract_tokens_from_response

    # Auto-instrumentation
    if name == "patch_browser_use":
        from .auto_instrument import patch_browser_use

        return patch_browser_use

    if name == "unpatch_browser_use":
        from .auto_instrument import unpatch_browser_use

        return unpatch_browser_use

    if name == "is_browser_use_patched":
        from .auto_instrument import is_browser_use_patched

        return is_browser_use_patched

    # Utilities
    if name == "wrap_browser_use_llm":
        from .llm import wrap_browser_use_llm

        return wrap_browser_use_llm

    if name == "is_browser_use_available":
        from .utils import is_browser_use_available

        return is_browser_use_available

    # Retry/Timeout utilities
    if name == "RetryExhaustedError":
        from ..._legacy_stubs import RetryExhaustedError

        return RetryExhaustedError

    if name == "TimeoutExceededError":
        from ..._legacy_stubs import TimeoutExceededError

        return TimeoutExceededError

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

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .agent import TracedAgent
    from .auto_instrument import (
        is_browser_use_patched,
        patch_browser_use,
        unpatch_browser_use,
    )
    from .browser import TracedBrowser
    from .config import BrowserUseConfig
    from .cost_tracking import (
        BROWSER_USE_MODEL_PRICING,
        extract_tokens_from_response,
        get_browser_use_cost,
    )
    from .handler import BrowserUseHandler
    from .llm import TracedLLM, wrap_browser_use_llm
    from ..._legacy_stubs import (
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from .utils import is_browser_use_available
