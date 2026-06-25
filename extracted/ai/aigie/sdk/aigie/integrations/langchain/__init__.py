"""Aigie LangChain integration (Framework ABC).

Auto-traces LangChain chains, agents, LLM calls, and tool invocations via
langchain_core's ``register_configure_hook`` — no user code changes beyond
``aigie.init()``.

Usage:
    import aigie

    aigie.init()                 # installs the LangChain adapter
    # or, explicitly:
    aigie.patch("langchain")

    from langchain_core.runnables import RunnableLambda
    chain = prompt | llm | parser
    chain.invoke({"input": "..."})   # automatically traced

The legacy callback-handler integration (``AigieCallbackHandler`` &
``patch_langchain``) was removed in favor of this ABC implementation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

__all__ = [
    "LangChainConfig",
    "LangChainNativeCallback",
    "LangChainEventClassifier",
    "install_langchain_patches",
    "uninstall_langchain_patches",
    "to_kytte_error",
]


def __getattr__(name: str) -> Any:
    """Lazy imports for import-time performance."""
    if name == "LangChainConfig":
        from aigie.integrations.langchain.config import LangChainConfig

        return LangChainConfig
    if name == "LangChainNativeCallback":
        from aigie.integrations.langchain.native_callback import LangChainNativeCallback

        return LangChainNativeCallback
    if name == "LangChainEventClassifier":
        from aigie.integrations.langchain.event_classifier import LangChainEventClassifier

        return LangChainEventClassifier
    if name in ("install_langchain_patches", "uninstall_langchain_patches"):
        from aigie.integrations.langchain import lifecycle

        return getattr(lifecycle, name)
    if name == "to_kytte_error":
        from aigie.integrations.langchain.error_conversion import to_kytte_error

        return to_kytte_error
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from aigie.integrations.langchain.config import LangChainConfig
    from aigie.integrations.langchain.error_conversion import to_kytte_error
    from aigie.integrations.langchain.event_classifier import LangChainEventClassifier
    from aigie.integrations.langchain.lifecycle import (
        install_langchain_patches,
        uninstall_langchain_patches,
    )
    from aigie.integrations.langchain.native_callback import LangChainNativeCallback

# Eager adapter import so @register_adapter("langchain") runs before
# aigie.init() looks the framework up.
from aigie.integrations.langchain.adapter import LangChainAdapter  # noqa: F401, E402
