"""
LLM client auto-instrumentation.

Automatically patches OpenAI, Anthropic, and Gemini clients to create spans
and track token usage, costs, and latency.
"""

import functools
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


def _is_aigie_callback(cb: Any) -> bool:
    """True if `cb` is an AigieCallbackHandler or any subclass of it.

    Walks the MRO by name to avoid importing AigieCallbackHandler here
    (would cycle via the autonomous runtime).
    """
    return any(c.__name__ == "AigieCallbackHandler" for c in type(cb).__mro__)


_patched_modules = set()


def patch_all_llms() -> None:
    """Patch all available LLM clients."""
    _patch_openai()
    _patch_anthropic()
    _patch_gemini()
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
            try:
                from aigie.auto_instrument.trace import (
                    is_in_callback_context,
                    is_in_llm_instrumentation,
                )

                if is_in_callback_context() or is_in_llm_instrumentation():
                    return original_getattribute(self, name)
            except ImportError:
                pass

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
        if name == "messages":
            try:
                from aigie.auto_instrument.trace import (
                    is_in_callback_context,
                    is_in_llm_instrumentation,
                )

                if is_in_callback_context() or is_in_llm_instrumentation():
                    return original_getattribute(self, name)
            except ImportError:
                pass

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


def _patch_gemini() -> None:
    """Patch Google Gemini client for auto-instrumentation."""
    try:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            import google.generativeai as genai

        if "gemini" in _patched_modules:
            return

        # Patch generate_content method directly
        if hasattr(genai, "GenerativeModel"):
            original_generate_content = genai.GenerativeModel.generate_content

            @functools.wraps(original_generate_content)
            def traced_generate_content(self, *args, **kwargs):
                """Traced version of generate_content."""
                from aigie.auto_instrument.trace import (
                    get_or_create_trace,
                    is_in_callback_context,
                    is_in_llm_instrumentation,
                )
                from aigie.client import get_aigie

                aigie = get_aigie()
                if (
                    not aigie
                    or not aigie._initialized
                    or is_in_callback_context()
                    or is_in_llm_instrumentation()
                ):
                    return original_generate_content(self, *args, **kwargs)

                # Extract model name from the Gemini instance
                model_name = getattr(self, "model_name", None) or getattr(
                    self, "_model_name", "gemini"
                )

                # Inline tracing: create trace + span directly to avoid kwarg conflicts
                import time as _time

                trace = _run_async_safely(
                    get_or_create_trace(
                        name="LLM Call: gemini", metadata={"provider": "gemini", "type": "llm"}
                    )
                )
                if not trace:
                    return original_generate_content(self, *args, **kwargs)

                # Extract prompt content for input
                prompt_content = args[0] if args else kwargs.get("contents", "")
                if isinstance(prompt_content, str):
                    input_text = prompt_content[:500]
                else:
                    input_text = str(prompt_content)[:500]

                span_ctx = trace.span(f"LLM: gemini - {model_name}", type="llm")
                span_ctx.set_input(
                    {
                        "provider": "gemini",
                        "model": model_name,
                        "prompt": input_text,
                    }
                )

                start = _time.time()
                try:
                    response = original_generate_content(self, *args, **kwargs)
                    latency = _time.time() - start

                    # Extract usage from Gemini response
                    output = {"latency": latency, "model": model_name, "provider": "gemini"}
                    if hasattr(response, "usage_metadata"):
                        um = response.usage_metadata
                        output["usage"] = {
                            "prompt_tokens": getattr(um, "prompt_token_count", 0),
                            "completion_tokens": getattr(um, "candidates_token_count", 0),
                            "total_tokens": getattr(um, "total_token_count", 0),
                        }
                    if hasattr(response, "text"):
                        output["content"] = response.text[:500]

                    span_ctx.set_output(output)
                    return response

                except Exception as e:
                    latency = _time.time() - start
                    span_ctx.set_output({"error": str(e), "latency": latency, "status": "error"})
                    raise

            genai.GenerativeModel.generate_content = traced_generate_content

        _patched_modules.add("gemini")
        logger.debug("Patched Gemini client for auto-instrumentation")

    except ImportError:
        pass  # Gemini not installed
    except Exception as e:
        logger.warning(f"Failed to patch Gemini: {e}")


def _run_async_safely(coro):
    """Run an async coroutine safely, handling already-running event loops.

    Uses safe_context_run to preserve contextvars across thread boundaries.
    """
    from aigie.utils.safe import safe_context_run

    return safe_context_run(coro)


def _trace_llm_call(provider: str, original_func: Any, *args, **kwargs) -> Any:
    """
    Trace an LLM call by creating a span and tracking metrics.

    Args:
        provider: LLM provider name ('openai', 'anthropic', 'gemini')
        original_func: Original LLM function to call
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        LLM response
    """

    # Skip LLM auto-instrumentation if we're in a callback context
    # (LangChain/LangGraph callbacks are already handling LLM tracing)
    from aigie.auto_instrument.trace import get_or_create_trace, is_in_callback_context
    from aigie.client import get_aigie

    in_callback = is_in_callback_context()
    logger.debug("is_in_callback_context=%s, provider=%s", in_callback, provider)
    if in_callback:
        if asyncio.iscoroutinefunction(original_func):
            return _run_async_safely(original_func(*args, **kwargs))
        return original_func(*args, **kwargs)

    aigie = get_aigie()
    if not aigie or not aigie._initialized:
        # No instrumentation, call original function
        if asyncio.iscoroutinefunction(original_func):
            return _run_async_safely(original_func(*args, **kwargs))
        return original_func(*args, **kwargs)

    # Get or create trace (handle both sync and async)
    if asyncio.iscoroutinefunction(original_func):
        # Async function - use async trace creation
        async def _async_trace():
            trace = await get_or_create_trace(
                name=f"LLM Call: {provider}", metadata={"provider": provider, "type": "llm"}
            )

            if not trace:
                return await original_func(*args, **kwargs)

            model = kwargs.get("model") or kwargs.get("model_name") or "unknown"

            async with trace.span(f"LLM: {provider} - {model}", type="llm") as span:
                return await _execute_llm_call(
                    span, original_func, provider, model, *args, **kwargs
                )

        return _run_async_safely(_async_trace())
    # Sync function - use sync trace creation
    trace = _run_async_safely(
        get_or_create_trace(
            name=f"LLM Call: {provider}", metadata={"provider": provider, "type": "llm"}
        )
    )

    if not trace:
        return original_func(*args, **kwargs)

    model = kwargs.get("model") or kwargs.get("model_name") or "unknown"

    # For sync, we need to handle span differently
    span_ctx = trace.span(f"LLM: {provider} - {model}", type="llm")
    return _execute_llm_call_sync(span_ctx, original_func, provider, model, *args, **kwargs)


async def _execute_llm_call(
    span: Any, original_func: Any, provider: str, model: str, *args, **kwargs
) -> Any:
    # Extract LLM parameters
    llm_params = {
        "temperature": kwargs.get("temperature"),
        "top_p": kwargs.get("top_p"),
        "top_k": kwargs.get("top_k"),
        "max_tokens": kwargs.get("max_tokens") or kwargs.get("max_tokens_to_sample"),
        "frequency_penalty": kwargs.get("frequency_penalty"),
        "presence_penalty": kwargs.get("presence_penalty"),
        "stop": kwargs.get("stop") or kwargs.get("stop_sequences"),
        "logprobs": kwargs.get("logprobs"),
        "logit_bias": kwargs.get("logit_bias"),
    }
    llm_params = {k: v for k, v in llm_params.items() if v is not None}

    # Extract messages and separate system prompts
    messages = kwargs.get("messages", [])
    system_prompt = None
    user_messages = []
    if messages:
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    system_prompt = content
                else:
                    user_messages.append(msg)
            elif hasattr(msg, "role") and hasattr(msg, "content"):
                if msg.role == "system":
                    system_prompt = msg.content
                else:
                    user_messages.append({"role": msg.role, "content": msg.content})

    # Build input data
    input_data = {
        "provider": provider,
        "model": model,
    }
    if llm_params:
        input_data["parameters"] = llm_params
    if system_prompt:
        input_data["system_prompt"] = system_prompt
    if user_messages:
        input_data["messages"] = user_messages
    else:
        # Fallback to truncated kwargs if no messages
        input_data["kwargs"] = {
            k: str(v)[:200]
            for k, v in kwargs.items()
            if k not in ["api_key", "temperature", "top_p", "max_tokens"]
        }

    span.set_input(input_data)

    start_time = time.time()

    try:
        # Call original function (it's async)
        response = await original_func(*args, **kwargs)

        latency = time.time() - start_time

        # Extract token usage and cost
        usage = None
        cost_data = None

        if hasattr(response, "usage"):
            usage = response.usage
        elif isinstance(response, dict) and "usage" in response:
            usage = response["usage"]

        if usage:
            from aigie.cost_tracking import extract_and_calculate_cost

            cost_data = extract_and_calculate_cost(model=model, usage=usage)

        # Extract response metadata
        finish_reason = None
        request_id = None
        model_version = model
        response_metadata = {}

        if hasattr(response, "choices") and response.choices:
            # OpenAI format
            choice = response.choices[0]
            content = choice.message.content if hasattr(choice.message, "content") else None
            finish_reason = getattr(choice, "finish_reason", None)
            # Extract request_id and system_fingerprint
            if hasattr(response, "id"):
                request_id = response.id
            if hasattr(response, "system_fingerprint"):
                response_metadata["system_fingerprint"] = response.system_fingerprint
            if hasattr(response, "model"):
                model_version = response.model
        elif hasattr(response, "content"):
            # Anthropic/Gemini format
            content = response.content
            if hasattr(response, "stop_reason"):
                finish_reason = response.stop_reason
            if hasattr(response, "id"):
                request_id = response.id
            if hasattr(response, "model"):
                model_version = response.model
        elif isinstance(response, dict):
            content = response.get("content", str(response))[:500]
            finish_reason = response.get("finish_reason") or response.get("stop_reason")
            request_id = response.get("id") or response.get("request_id")
            model_version = response.get("model", model)
        else:
            content = str(response)[:500]

        # Set output
        output = {"latency": latency, "model": model, "provider": provider}

        if usage:
            output["usage"] = usage
        if cost_data:
            output["cost"] = cost_data.get("total_cost", 0)
        if content:
            output["content"] = content[:500]  # Truncate
        if finish_reason:
            output["finish_reason"] = finish_reason
        if request_id:
            output["request_id"] = request_id
        if model_version != model:
            output["model_version"] = model_version
        if response_metadata:
            output["response_metadata"] = response_metadata

        span.set_output(output)

        # Store in metadata for aggregation
        if hasattr(span, "set_metadata"):
            current_metadata = getattr(span, "_metadata", {})
            enriched_metadata = dict(current_metadata)
            enriched_metadata["llm_parameters"] = llm_params
            if system_prompt:
                enriched_metadata["system_prompt"] = system_prompt
            if finish_reason:
                enriched_metadata["finish_reason"] = finish_reason
            if request_id:
                enriched_metadata["request_id"] = request_id
            if model_version:
                enriched_metadata["model_version"] = model_version
            if usage:
                enriched_metadata["token_usage"] = {
                    "input_tokens": getattr(
                        usage,
                        "prompt_tokens",
                        usage.get("prompt_tokens", 0) if isinstance(usage, dict) else 0,
                    ),
                    "output_tokens": getattr(
                        usage,
                        "completion_tokens",
                        usage.get("completion_tokens", 0) if isinstance(usage, dict) else 0,
                    ),
                    "total_tokens": getattr(
                        usage,
                        "total_tokens",
                        usage.get("total_tokens", 0) if isinstance(usage, dict) else 0,
                    ),
                }
            # Extract cache and reasoning tokens
            usage_details = {}
            if usage:
                # OpenAI format: completion_tokens_details / prompt_tokens_details
                if hasattr(usage, "completion_tokens_details"):
                    ctd = usage.completion_tokens_details
                    reasoning = getattr(ctd, "reasoning_tokens", 0) or 0
                    if reasoning:
                        usage_details["reasoning_tokens"] = reasoning
                if hasattr(usage, "prompt_tokens_details"):
                    ptd = usage.prompt_tokens_details
                    cached = getattr(ptd, "cached_tokens", 0) or 0
                    if cached:
                        usage_details["cache_read_input_tokens"] = cached

                # Anthropic format: direct attributes on usage
                cache_read = getattr(usage, "cache_read_input_tokens", 0) or (
                    usage.get("cache_read_input_tokens", 0) if isinstance(usage, dict) else 0
                )
                cache_create = getattr(usage, "cache_creation_input_tokens", 0) or (
                    usage.get("cache_creation_input_tokens", 0) if isinstance(usage, dict) else 0
                )
                if cache_read:
                    usage_details["cache_read_input_tokens"] = cache_read
                if cache_create:
                    usage_details["cache_creation_input_tokens"] = cache_create

            if usage_details:
                enriched_metadata["usage_details"] = usage_details
            span.set_metadata(enriched_metadata)

        return response

    except Exception as e:
        latency = time.time() - start_time

        span.set_output(
            {"error": str(e), "error_type": type(e).__name__, "latency": latency, "status": "error"}
        )

        raise


def _execute_llm_call_sync(
    span_ctx: Any, original_func: Any, provider: str, model: str, *args, **kwargs
) -> Any:
    """Execute LLM call synchronously with tracing."""
    from aigie.cost_tracking import extract_and_calculate_cost

    # Extract LLM parameters (same as async version)
    llm_params = {
        "temperature": kwargs.get("temperature"),
        "top_p": kwargs.get("top_p"),
        "top_k": kwargs.get("top_k"),
        "max_tokens": kwargs.get("max_tokens") or kwargs.get("max_tokens_to_sample"),
        "frequency_penalty": kwargs.get("frequency_penalty"),
        "presence_penalty": kwargs.get("presence_penalty"),
        "stop": kwargs.get("stop") or kwargs.get("stop_sequences"),
    }
    llm_params = {k: v for k, v in llm_params.items() if v is not None}

    # Extract messages and separate system prompts
    messages = kwargs.get("messages", [])
    system_prompt = None
    user_messages = []
    if messages:
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    system_prompt = content
                else:
                    user_messages.append(msg)
            elif hasattr(msg, "role") and hasattr(msg, "content"):
                if msg.role == "system":
                    system_prompt = msg.content
                else:
                    user_messages.append({"role": msg.role, "content": msg.content})

    # Build input data
    input_data = {
        "provider": provider,
        "model": model,
    }
    if llm_params:
        input_data["parameters"] = llm_params
    if system_prompt:
        input_data["system_prompt"] = system_prompt
    if user_messages:
        input_data["messages"] = user_messages
    else:
        input_data["kwargs"] = {
            k: str(v)[:200]
            for k, v in kwargs.items()
            if k not in ["api_key", "temperature", "top_p", "max_tokens"]
        }

    span_ctx.set_input(input_data)

    start_time = time.time()

    try:
        response = original_func(*args, **kwargs)
        latency = time.time() - start_time

        # Extract token usage and cost
        usage = None
        cost_data = None

        if hasattr(response, "usage"):
            usage = response.usage
        elif isinstance(response, dict) and "usage" in response:
            usage = response["usage"]

        if usage:
            cost_data = extract_and_calculate_cost(model=model, usage=usage)

        # Extract response metadata (same as async version)
        finish_reason = None
        request_id = None
        model_version = model
        response_metadata = {}

        if hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            content = choice.message.content if hasattr(choice.message, "content") else None
            finish_reason = getattr(choice, "finish_reason", None)
            if hasattr(response, "id"):
                request_id = response.id
            if hasattr(response, "system_fingerprint"):
                response_metadata["system_fingerprint"] = response.system_fingerprint
            if hasattr(response, "model"):
                model_version = response.model
        elif hasattr(response, "content"):
            content = response.content
            if hasattr(response, "stop_reason"):
                finish_reason = response.stop_reason
            if hasattr(response, "id"):
                request_id = response.id
            if hasattr(response, "model"):
                model_version = response.model
        elif isinstance(response, dict):
            content = response.get("content", str(response))[:500]
            finish_reason = response.get("finish_reason") or response.get("stop_reason")
            request_id = response.get("id") or response.get("request_id")
            model_version = response.get("model", model)
        else:
            content = str(response)[:500]

        output = {"latency": latency, "model": model, "provider": provider}

        if usage:
            output["usage"] = usage
        if cost_data:
            output["cost"] = cost_data.get("total_cost", 0)
        if content:
            output["content"] = content[:500]
        if finish_reason:
            output["finish_reason"] = finish_reason
        if request_id:
            output["request_id"] = request_id
        if model_version != model:
            output["model_version"] = model_version
        if response_metadata:
            output["response_metadata"] = response_metadata

        span_ctx.set_output(output)

        # Store in metadata
        if hasattr(span_ctx, "set_metadata"):
            current_metadata = getattr(span_ctx, "_metadata", {})
            enriched_metadata = dict(current_metadata)
            enriched_metadata["llm_parameters"] = llm_params
            if system_prompt:
                enriched_metadata["system_prompt"] = system_prompt
            if finish_reason:
                enriched_metadata["finish_reason"] = finish_reason
            if request_id:
                enriched_metadata["request_id"] = request_id
            if model_version:
                enriched_metadata["model_version"] = model_version
            if usage:
                enriched_metadata["token_usage"] = {
                    "input_tokens": getattr(
                        usage,
                        "prompt_tokens",
                        usage.get("prompt_tokens", 0) if isinstance(usage, dict) else 0,
                    ),
                    "output_tokens": getattr(
                        usage,
                        "completion_tokens",
                        usage.get("completion_tokens", 0) if isinstance(usage, dict) else 0,
                    ),
                    "total_tokens": getattr(
                        usage,
                        "total_tokens",
                        usage.get("total_tokens", 0) if isinstance(usage, dict) else 0,
                    ),
                }
            # Extract cache and reasoning tokens
            usage_details = {}
            if usage:
                # OpenAI format: completion_tokens_details / prompt_tokens_details
                if hasattr(usage, "completion_tokens_details"):
                    ctd = usage.completion_tokens_details
                    reasoning = getattr(ctd, "reasoning_tokens", 0) or 0
                    if reasoning:
                        usage_details["reasoning_tokens"] = reasoning
                if hasattr(usage, "prompt_tokens_details"):
                    ptd = usage.prompt_tokens_details
                    cached = getattr(ptd, "cached_tokens", 0) or 0
                    if cached:
                        usage_details["cache_read_input_tokens"] = cached

                # Anthropic format: direct attributes on usage
                cache_read = getattr(usage, "cache_read_input_tokens", 0) or (
                    usage.get("cache_read_input_tokens", 0) if isinstance(usage, dict) else 0
                )
                cache_create = getattr(usage, "cache_creation_input_tokens", 0) or (
                    usage.get("cache_creation_input_tokens", 0) if isinstance(usage, dict) else 0
                )
                if cache_read:
                    usage_details["cache_read_input_tokens"] = cache_read
                if cache_create:
                    usage_details["cache_creation_input_tokens"] = cache_create

            if usage_details:
                enriched_metadata["usage_details"] = usage_details
            span_ctx.set_metadata(enriched_metadata)

        return response

    except Exception as e:
        latency = time.time() - start_time

        span_ctx.set_output(
            {"error": str(e), "error_type": type(e).__name__, "latency": latency, "status": "error"}
        )

        raise


# Import asyncio at module level
import asyncio
import contextlib


def _patch_langchain_llms() -> None:
    """Patch LangChain LLM classes to auto-inject callbacks.

    Covers all major LLM providers to ensure interception and tracing
    work regardless of which provider the customer uses — including
    fallback chains (e.g. Bedrock → Groq).
    """
    # Each entry: (import_path, class_name, provider_label)
    # Uses lazy imports so missing packages are silently skipped.
    _LANGCHAIN_LLM_TARGETS = [
        # --- Tier 1: Most common providers ---
        ("langchain_openai", "ChatOpenAI", "openai"),
        ("langchain_anthropic", "ChatAnthropic", "anthropic"),
        ("langchain_google_genai", "ChatGoogleGenerativeAI", "gemini"),
        # --- AWS Bedrock ---
        ("langchain_aws", "ChatBedrock", "bedrock"),
        ("langchain_aws", "ChatBedrockConverse", "bedrock"),
        # --- Groq ---
        ("langchain_groq", "ChatGroq", "groq"),
        # --- Mistral ---
        ("langchain_mistralai", "ChatMistralAI", "mistral"),
        # --- Cohere ---
        ("langchain_cohere", "ChatCohere", "cohere"),
        # --- Fireworks ---
        ("langchain_fireworks", "ChatFireworks", "fireworks"),
        # --- Together AI ---
        ("langchain_together", "ChatTogether", "together"),
        # --- NVIDIA NIM ---
        ("langchain_nvidia_ai_endpoints", "ChatNVIDIA", "nvidia"),
        # --- AI21 ---
        ("langchain_ai21", "ChatAI21", "ai21"),
        # --- DeepSeek (via openai-compatible or dedicated package) ---
        ("langchain_deepseek", "ChatDeepSeek", "deepseek"),
        # --- Ollama (local models) ---
        ("langchain_ollama", "ChatOllama", "ollama"),
        # --- Azure OpenAI ---
        ("langchain_openai", "AzureChatOpenAI", "azure_openai"),
        # --- Google Vertex AI ---
        ("langchain_google_vertexai", "ChatVertexAI", "vertex_ai"),
        # --- Hugging Face ---
        ("langchain_huggingface", "ChatHuggingFace", "huggingface"),
        # --- xAI (Grok) ---
        ("langchain_xai", "ChatXAI", "xai"),
        # --- Cerebras ---
        ("langchain_cerebras", "ChatCerebras", "cerebras"),
        # --- Sambanova ---
        ("langchain_sambanova", "ChatSambaNovaCloud", "sambanova"),
    ]

    patched_count = 0
    for module_path, class_name, provider in _LANGCHAIN_LLM_TARGETS:
        try:
            module = __import__(module_path, fromlist=[class_name])
            llm_class = getattr(module, class_name, None)
            if llm_class is None:
                continue
            if llm_class in _patched_modules:
                continue
            _patch_langchain_llm_class(llm_class, provider)
            _patched_modules.add(llm_class)
            patched_count += 1
        except ImportError:
            pass  # Provider package not installed — skip silently
        except Exception as e:
            logger.debug(f"Failed to patch {module_path}.{class_name}: {e}")

    if patched_count:
        logger.debug(f"Patched {patched_count} LangChain LLM classes for auto-instrumentation")


def _patch_langchain_llm_class(llm_class: Any, provider: str) -> None:
    """Patch a LangChain LLM class to auto-inject callbacks and interception hooks.

    This provides full auto-instrumentation:
    1. Pre-call interception (blocking, validation)
    2. Tracing (spans, metrics)
    3. Post-call interception (quality checks, recommendations)
    """
    original_ainvoke = getattr(llm_class, "ainvoke", None)
    original_invoke = getattr(llm_class, "invoke", None)

    def _convert_messages_to_dict(messages) -> list:
        """Convert LangChain messages to dict format for interception."""
        messages_dict = []
        for msg in messages:
            if hasattr(msg, "type"):
                role = msg.type
            elif hasattr(msg, "__class__"):
                role = msg.__class__.__name__.replace("Message", "").lower()
            else:
                role = "user"
            content = msg.content if hasattr(msg, "content") else str(msg)
            messages_dict.append({"role": role, "content": content})
        return messages_dict

    if original_ainvoke:

        @functools.wraps(original_ainvoke)
        async def traced_ainvoke(self, messages, config=None, **kwargs):
            """Intercepted version of LLM ainvoke.

            Automatically runs pre/post-call interception hooks.
            Tracing is handled by LangChain's callback mechanism.
            """
            from aigie.client import get_aigie

            aigie = get_aigie()

            # Recursion guard: skip instrumentation if already inside an LLM wrapper
            from aigie.auto_instrument.trace import (
                is_in_llm_instrumentation,
                set_llm_instrumentation,
            )

            if is_in_llm_instrumentation():
                return await original_ainvoke(self, messages, config=config, **kwargs)

            set_llm_instrumentation(True)
            try:
                model_name = getattr(self, "model_name", None) or getattr(self, "model", "unknown")

                # Convert messages for interception
                messages_dict = _convert_messages_to_dict(messages)

                # Pre-call interception was gated on the removed autonomous mode; ctx stays None.
                interception_ctx = None

                # Tracing: check if AigieCallbackHandler is present in config.
                # If callbacks handle tracing, we skip span creation here to avoid duplicates.
                # If no callbacks, we create a span so the LLM call is visible on the platform.
                _has_aigie_callback = False
                _fallback_span = None
                if config and isinstance(config, dict):
                    callbacks = config.get("callbacks")
                    if callbacks is not None:
                        # callbacks may be a list or an AsyncCallbackManager/CallbackManager
                        if isinstance(callbacks, list):
                            cb_list = callbacks
                        else:
                            cb_list = list(getattr(callbacks, "handlers", []))
                            cb_list += list(getattr(callbacks, "inheritable_handlers", []))
                        for cb in cb_list:
                            if _is_aigie_callback(cb):
                                _has_aigie_callback = True
                                break
                # Also skip fallback span when callback context is active (LangGraph/LangChain
                # callbacks handle tracing even if not visible in this config dict)
                from aigie.auto_instrument.trace import is_in_callback_context

                if (
                    not _has_aigie_callback
                    and not is_in_callback_context()
                    and aigie
                    and aigie._initialized
                ):
                    try:
                        from aigie.auto_instrument.trace import get_or_create_trace

                        trace = await get_or_create_trace(
                            name=f"LLM Call: {provider}",
                            metadata={"provider": provider, "type": "llm"},
                        )
                        if trace:
                            _fallback_span = trace.span(
                                f"LLM: {provider} - {model_name}", type="llm"
                            )
                            await _fallback_span.__aenter__()
                            _fallback_span.set_input(
                                {
                                    "provider": provider,
                                    "model": model_name,
                                    "messages": messages_dict[:5],
                                }
                            )
                    except Exception as e:
                        logger.debug(f"Fallback span creation error (continuing): {e}")

                # Make the actual LLM call. Errors route through the autonomous
                # chain (a no-op passthrough unless a chain hook is wired); the
                # post-call quality-retry loop was gated on the removed autonomous mode.
                from aigie.autonomous.inline_call import acall_with_autonomous

                last_response = await acall_with_autonomous(
                    lambda: original_ainvoke(self, messages, config=config, **kwargs),
                    interception_ctx,
                    aigie,
                )

                # Close fallback span on success
                if _fallback_span:
                    try:
                        response_content = (
                            last_response.content
                            if hasattr(last_response, "content")
                            else str(last_response)[:500]
                        )
                        _fallback_span.set_output(
                            {
                                "provider": provider,
                                "model": model_name,
                                "content": response_content[:500],
                            }
                        )
                        await _fallback_span.__aexit__(None, None, None)
                    except Exception as e:
                        logger.debug(f"Fallback span close error: {e}")

                return last_response
            except Exception as exc:
                # Close fallback span on error
                if _fallback_span:
                    try:
                        _fallback_span.set_output(
                            {
                                "error": str(exc),
                                "error_type": type(exc).__name__,
                                "provider": provider,
                                "model": model_name,
                            }
                        )
                        await _fallback_span.__aexit__(type(exc), exc, exc.__traceback__)
                    except Exception:
                        pass
                raise
            finally:
                set_llm_instrumentation(False)

        llm_class.ainvoke = traced_ainvoke

    if original_invoke:

        @functools.wraps(original_invoke)
        def traced_invoke(self, messages, config=None, **kwargs):
            """Intercepted version of LLM invoke (sync).

            Automatically runs pre/post-call interception hooks.
            Tracing is handled by LangChain's callback mechanism.
            """
            from aigie.client import get_aigie

            aigie = get_aigie()

            from aigie.auto_instrument.trace import (
                is_in_llm_instrumentation,
                set_llm_instrumentation,
            )

            if is_in_llm_instrumentation():
                return original_invoke(self, messages, config=config, **kwargs)

            set_llm_instrumentation(True)
            try:
                model_name = getattr(self, "model_name", None) or getattr(self, "model", "unknown")

                # Convert messages for interception
                messages_dict = _convert_messages_to_dict(messages)

                # Pre-call interception was gated on the removed autonomous mode; ctx stays None.
                interception_ctx = None

                # Tracing: check if AigieCallbackHandler is present in config.
                _has_aigie_callback = False
                _fallback_span = None
                if config and isinstance(config, dict):
                    callbacks = config.get("callbacks")
                    if callbacks is not None:
                        # callbacks can be a list, AsyncCallbackManager, or CallbackManager
                        cb_list = (
                            callbacks
                            if isinstance(callbacks, list)
                            else getattr(callbacks, "handlers", [])
                        )
                        for cb in cb_list:
                            if _is_aigie_callback(cb):
                                _has_aigie_callback = True
                                break
                # Also skip fallback span when callback context is active (LangGraph/LangChain
                # callbacks handle tracing even if not visible in this config dict)
                from aigie.auto_instrument.trace import is_in_callback_context

                if (
                    not _has_aigie_callback
                    and not is_in_callback_context()
                    and aigie
                    and aigie._initialized
                ):
                    try:
                        from aigie.auto_instrument.trace import get_or_create_trace_sync

                        trace = get_or_create_trace_sync(
                            name=f"LLM Call: {provider}",
                            metadata={"provider": provider, "type": "llm"},
                        )
                        if trace:
                            _fallback_span = trace.span(
                                f"LLM: {provider} - {model_name}", type="llm"
                            )
                            _fallback_span.set_input(
                                {
                                    "provider": provider,
                                    "model": model_name,
                                    "messages": messages_dict[:5],
                                }
                            )
                    except Exception as e:
                        logger.debug(f"Fallback span creation error (continuing): {e}")

                # Make the actual LLM call, routing errors through the autonomous
                # chain so hooks like RetryIntervention can fire on e.g. 429.
                from aigie.autonomous.inline_call import call_sync_with_autonomous

                response = call_sync_with_autonomous(
                    lambda: original_invoke(self, messages, config=config, **kwargs),
                    interception_ctx,
                    aigie,
                )

                # Close fallback span on success
                if _fallback_span:
                    try:
                        response_content = (
                            response.content
                            if hasattr(response, "content")
                            else str(response)[:500]
                        )
                        _fallback_span.set_output(
                            {
                                "provider": provider,
                                "model": model_name,
                                "content": response_content[:500],
                            }
                        )
                    except Exception as e:
                        logger.debug(f"Fallback span close error: {e}")

                return response
            except Exception as exc:
                # Close fallback span on error
                if _fallback_span:
                    with contextlib.suppress(Exception):
                        _fallback_span.set_output(
                            {
                                "error": str(exc),
                                "error_type": type(exc).__name__,
                                "provider": provider,
                                "model": model_name,
                            }
                        )
                raise
            finally:
                set_llm_instrumentation(False)

        llm_class.invoke = traced_invoke
