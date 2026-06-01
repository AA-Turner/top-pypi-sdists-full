"""
LangChain callback handler for Aigie SDK.

This module provides the LangChainHandler (also exported as AigieCallbackHandler)
which implements LangChain's BaseCallbackHandler protocol for automatic
trace/span creation and comprehensive tracing of LangChain workflows.

Features:
    - Automatic trace/span creation for chains, LLMs, tools, and retrievers
    - Token usage tracking with cost estimation
    - Error detection and classification
    - Drift detection for agent workflows
    - LangGraph integration support
    - Workflow execution path tracking

Usage:
    from aigie.integrations.langchain import LangChainHandler

    # With explicit trace
    async with aigie.trace("My Workflow") as trace:
        handler = LangChainHandler(trace=trace)
        result = await chain.ainvoke(input, config={"callbacks": [handler]})

    # Auto-instrumentation (recommended)
    from aigie.integrations.langchain import patch_langchain
    patch_langchain()  # Now all chains are automatically traced

Configuration:
    Use LangChainConfig to customize behavior:

    from aigie.integrations.langchain import LangChainConfig, LangChainHandler

    config = LangChainConfig(
        trace_llm_calls=True,
        capture_prompts=True,
        redact_pii=True,
        max_content_length=2000,
    )

For implementation details, see the core callback module at aigie/callback.py.
"""

# Re-export the main callback handler from core module
from .error_detection import (
    DetectedError,
    ErrorDetector,
    ErrorSeverity,
    ErrorType,
    get_error_detector,
)
from ...callback import AigieCallbackHandler

# Import config for easy access
from .config import LangChainConfig

# Import error detection components
# Import session management
from .session import (
    LangChainSessionContext,
    get_session_context,
    langchain_session,
    set_session_context,
)

# Primary handler class - use LangChainHandler for consistency with other integrations
LangChainHandler = AigieCallbackHandler

# Export all public symbols
__all__ = [
    # Primary handler (use either name)
    "LangChainHandler",
    "AigieCallbackHandler",
    # Configuration
    "LangChainConfig",
    # Session management
    "LangChainSessionContext",
    "get_session_context",
    "set_session_context",
    "langchain_session",
]
