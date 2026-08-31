"""
LLM client auto-instrumentation.

Automatically patches OpenAI and Anthropic clients to create spans and track token
usage, costs, and latency. Gemini's two clients live in their own modules
(``gemini_legacy.py``, ``google_genai.py``) and are installed from ``patch_all_llms``.
"""

import functools
import logging
from typing import Any, cast

logger = logging.getLogger(__name__)


def _is_aigie_callback(cb: Any) -> bool:
    """True if `cb` is an Aigie-injected callback handler.

    Aigie's native callbacks (LangGraph / LangChain, both subclasses of
    ``LangChainCallbackBase``) set the class-level marker
    ``_is_aigie_handler = True``. Strict ``is True`` so MagicMocks (which
    auto-vivify attributes into truthy mocks) don't match. Avoids importing the
    callback class here (would cycle via the autonomous runtime).
    """
    return getattr(cb, "_is_aigie_handler", False) is True


def _is_inside_langchain_run() -> bool:
    """True when the current call originates from a LangChain/LangGraph run that
    an Aigie callback is already tracing.

    LangChain propagates the active ``RunnableConfig`` via a contextvar that
    crosses async boundaries. The callback-driven LangChain integration only
    sets our ambient trace_state inside callback executions (which run on
    executor threads for async), so the bare provider call on the main task
    can't see it via ``is_in_callback_context()``. Reading LangChain's own
    contextvar here lets the bare LLM-provider patch suppress itself when the
    provider call comes from a LangChain model whose run is already traced —
    e.g. a tool-bound model whose call bypasses the patched ``ChatModel.invoke``.
    """
    try:
        from langchain_core.runnables.config import var_child_runnable_config

        from aigie.auto_instrument._callback_utils import normalize_callbacks
    except ImportError:
        return False
    # var holds a RunnableConfig (TypedDict, a dict at runtime); normalize_callbacks
    # only reads .get("callbacks"), so pass it through without copying.
    cfg = cast("dict | None", var_child_runnable_config.get())
    return any(_is_aigie_callback(cb) for cb in normalize_callbacks(cfg))


def _llm_autoinstrument_suppressed() -> bool:
    """True when this LLM call is already traced by a framework callback
    (LangChain/LangGraph) or an outer LLM wrapper, so the bare provider patch
    must not trace it a second time."""
    try:
        from aigie.auto_instrument.trace import (
            is_in_callback_context,
            is_in_llm_instrumentation,
        )
    except ImportError:
        return False
    return is_in_callback_context() or is_in_llm_instrumentation() or _is_inside_langchain_run()


# Provider names as strings, plus the LangChain chat-model classes that
# `langchain_llms.py` adds — hence `Any` rather than `set[str]`.
_patched_modules: set[Any] = set()


def patch_all_llms() -> None:
    """Patch all available LLM clients."""
    from aigie.auto_instrument.gemini_legacy import patch_gemini_legacy
    from aigie.auto_instrument.google_genai import patch_google_genai
    from aigie.auto_instrument.langchain_llms import _patch_langchain_llms

    _patch_openai()
    _patch_anthropic()
    # Gemini ships as two separate clients and each needs its own patch; both live in
    # their own modules rather than here, so this file stops growing.
    patch_gemini_legacy()
    patch_google_genai()
    _patch_langchain_llms()


def _patch_openai() -> None:
    """Patch OpenAI client for auto-instrumentation."""
    try:
        import openai

        if "openai" in _patched_modules:
            return

        # Patch OpenAI client class
        if hasattr(openai, "OpenAI"):
            _patch_openai_client(openai.OpenAI)

        # Patch AsyncOpenAI
        if hasattr(openai, "AsyncOpenAI"):
            _patch_openai_client(openai.AsyncOpenAI, is_async=True)

        _patched_modules.add("openai")
        logger.debug("Patched OpenAI client for auto-instrumentation")

    except ImportError:
        pass  # OpenAI not installed
    except Exception as e:
        logger.warning(f"Failed to patch OpenAI: {e}")


def _patch_openai_client(client_class: Any, is_async: bool = False) -> None:
    """Patch OpenAI client by wrapping instances after creation."""
    original_init = client_class.__init__
    original_getattribute = getattr(client_class, "__getattribute__", object.__getattribute__)

    @functools.wraps(original_init)
    def traced_init(self, *args, **kwargs):
        """Init that creates wrapper and stores it."""
        original_init(self, *args, **kwargs)

        from aigie.client import get_aigie
        from aigie.wrappers import wrap_openai

        aigie = get_aigie()
        if aigie and aigie._initialized:
            # Create wrapper and store reference
            wrapped = wrap_openai(self, aigie_client=aigie)
            # Store wrapper on instance using object.__setattr__ to avoid recursion
            object.__setattr__(self, "_aigie_wrapper", wrapped)

    client_class.__init__ = traced_init

    # Patch __getattribute__ to intercept 'chat' access
    def traced_getattribute(self, name):
        # Special handling for 'chat' when we have a wrapper
        if name == "chat":
            # Skip wrapper when inside a callback-traced context (LangChain/LangGraph
            # callbacks are already handling tracing — wrapping here causes double-entry)
            if _llm_autoinstrument_suppressed():
                return original_getattribute(self, name)

            # Check if wrapper exists (using object.__getattribute__ to avoid recursion)
            try:
                wrapper = object.__getattribute__(self, "_aigie_wrapper")
                if wrapper:
                    # Get the ORIGINAL chat object (bypassing this patched __getattribute__)
                    # then wrap it directly. Do NOT use wrapper.chat — that triggers
                    # OpenAIWrapper.__getattr__("chat") → getattr(self._client, "chat")
                    # → traced_getattribute("chat") → infinite recursion.
                    original_chat = original_getattribute(self, "chat")
                    return wrapper._wrap_chat(original_chat)
            except AttributeError:
                # No wrapper yet, fall through to original behavior
                pass

        # For all other attributes, use original behavior
        # But avoid accessing _aigie_wrapper through normal path to prevent recursion
        if name == "_aigie_wrapper":
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                return None

        return original_getattribute(self, name)

    client_class.__getattribute__ = traced_getattribute


def _patch_anthropic() -> None:
    """Patch Anthropic client for auto-instrumentation."""
    try:
        import anthropic

        if "anthropic" in _patched_modules:
            return

        # Patch Anthropic client
        if hasattr(anthropic, "Anthropic"):
            _patch_anthropic_client(anthropic.Anthropic)

        # Patch AsyncAnthropic
        if hasattr(anthropic, "AsyncAnthropic"):
            _patch_anthropic_client(anthropic.AsyncAnthropic, is_async=True)

        _patched_modules.add("anthropic")
        logger.debug("Patched Anthropic client for auto-instrumentation")

    except ImportError:
        pass  # Anthropic not installed
    except Exception as e:
        logger.warning(f"Failed to patch Anthropic: {e}")


def _patch_anthropic_client(client_class: Any, is_async: bool = False) -> None:
    """Patch Anthropic client by wrapping instances after creation."""
    original_init = client_class.__init__

    @functools.wraps(original_init)
    def traced_init(self, *args, **kwargs):
        """Init that creates wrapper and stores it."""
        original_init(self, *args, **kwargs)

        from aigie.client import get_aigie
        from aigie.wrappers import wrap_anthropic

        aigie = get_aigie()
        if aigie and aigie._initialized:
            # Save original messages before wrapping (bypass any patched __getattribute__)
            original_messages = original_getattribute(self, "messages")
            wrapped = wrap_anthropic(self, aigie_client=aigie)
            # Store original messages on the wrapper for direct access
            object.__setattr__(wrapped, "_original_messages", original_messages)
            object.__setattr__(self, "_aigie_wrapper", wrapped)

    client_class.__init__ = traced_init

    # Patch __getattribute__ to intercept 'messages' access
    original_getattribute = getattr(client_class, "__getattribute__", object.__getattribute__)

    def traced_getattribute(self, name):
        # Skip wrapper when inside a callback-traced context or LLM instrumentation
        if name == "messages" and _llm_autoinstrument_suppressed():
            return original_getattribute(self, name)

        # Avoid recursion for internal attributes
        if name == "_aigie_wrapper":
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                return None

        # Special handling for 'messages' when we have a wrapper
        if name == "messages":
            try:
                wrapper = object.__getattribute__(self, "_aigie_wrapper")
                # Only delegate if wrapper is a different object (not self)
                if wrapper is not None and wrapper is not self:
                    # Access the messages property on the wrapper class
                    return type(wrapper).messages.fget(wrapper)
            except AttributeError:
                pass

        return original_getattribute(self, name)

    client_class.__getattribute__ = traced_getattribute


def _run_async_safely(coro):
    """Run an async coroutine safely, handling already-running event loops.

    Uses safe_context_run to preserve contextvars across thread boundaries.
    """
    from aigie.utils.safe import safe_context_run

    return safe_context_run(coro)
