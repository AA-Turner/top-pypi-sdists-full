"""Tracing wrapper for the OpenAI client, including Azure OpenAI.

`wrap_openai` returns a stand-in that proxies attribute access to the real
client and traces `chat.completions.create`. The customer's call goes through
untouched; the span is the side effect.

The two handlers below keep the same shape: open a span, run the interception
hooks the path supports, call the provider, record what came back, and emit the
span from a `finally` so it is emitted whether the call succeeded, failed, or
returned a stream. Interception lives in `_openai_interception`, streaming in
`_openai_stream`, and the span payload itself in `_base`.
"""

from __future__ import annotations

import functools
import inspect
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from aigie.context_manager import (
    RunContext,
    get_current_span_context,
    get_current_trace_context,
    get_parent_context,
    is_tracing_enabled,
    set_current_span_context,
)
from aigie.cost_tracking import extract_and_calculate_cost
from aigie.wrappers._base import (
    extract_system_prompt,
    queue_llm_span_event,
    queue_llm_span_event_sync,
    record_error,
    update_trace_system_prompt,
)
from aigie.wrappers._openai_interception import (
    retry_kwargs_from,
    run_error_post_call,
    run_post_call,
    run_pre_call,
    run_sync_pre_call,
)
from aigie.wrappers._openai_stream import wrap_stream_async, wrap_stream_sync

logger = logging.getLogger(__name__)

SPAN_NAME = "openai.chat.completions.create"


def _new_run_context(model: str, messages: list) -> RunContext:
    """Open a span for one chat completion."""
    parent_ctx = get_parent_context()
    return RunContext(
        id=str(uuid4()),
        name=SPAN_NAME,
        type="span",
        span_type="llm",
        parent_id=parent_ctx.id if parent_ctx else None,
        metadata={
            "provider": "openai",
            "model": model,
            "input": {"messages": messages},
        },
        tags=["openai", "llm", model],
        start_time=datetime.now(timezone.utc),
    )


def _extract_output_content(response: Any) -> str:
    """The assistant text of a chat completion, however the response is shaped."""
    if hasattr(response, "choices") and len(response.choices) > 0:
        output_message = response.choices[0].message
        if hasattr(output_message, "content"):
            content: str = output_message.content
            return content
        return str(output_message)
    return str(response)


def _record_usage_and_cost(run_ctx: RunContext, response: Any) -> None:
    """Stamp token counts and price onto the span, if the response reports any."""
    if not hasattr(response, "usage"):
        return

    run_ctx.metadata["usage"] = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    try:
        cost_info = extract_and_calculate_cost(response, "openai")
    except Exception as e:
        # An unpriceable span is still a useful span, so this is contained —
        # but silently is how a pricing-table gap goes unnoticed for months.
        logger.debug("[wrapper] Cost calculation failed for openai: %s", e)
        cost_info = None

    if cost_info:
        run_ctx.metadata["cost"] = {
            "input_cost": float(cost_info.input_cost),
            "output_cost": float(cost_info.output_cost),
            "total_cost": float(cost_info.total_cost),
            "currency": cost_info.currency,
        }


def _record_success(run_ctx: RunContext, response: Any) -> str:
    """Record a completed call and return the assistant text."""
    output_content = _extract_output_content(response)
    _record_usage_and_cost(run_ctx, response)
    run_ctx.metadata["output"] = {"content": output_content}
    run_ctx.metadata["status"] = "success"
    return output_content


@dataclass
class _Call:
    """Everything one traced completion needs to carry through its handler."""

    run_ctx: RunContext
    aigie: Any
    trace_ctx: Any
    model: str
    messages: list
    stream: bool
    interception_ctx: Any = None

    @property
    def trace_id(self) -> str:
        return self.trace_ctx.id if self.trace_ctx else self.run_ctx.id

    @property
    def intercepts(self) -> bool:
        return bool(self.aigie and self.aigie._interceptor_chain)

    @classmethod
    def begin(cls, kwargs: dict) -> _Call:
        """Read the request and open its span."""
        from aigie.client import get_aigie

        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])

        system_prompt = extract_system_prompt(messages)
        if system_prompt:
            update_trace_system_prompt(system_prompt)

        return cls(
            run_ctx=_new_run_context(model, messages),
            aigie=get_aigie(),
            trace_ctx=get_current_trace_context(),
            model=model,
            messages=messages,
            stream=kwargs.get("stream", False),
        )


class OpenAIWrapper:
    """
    Wrapper for OpenAI client with automatic tracing.

    Usage:
        from aigie.wrappers import wrap_openai
        import openai

        client = wrap_openai(openai.OpenAI())

        # All calls are now automatically traced
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
    """

    def __init__(self, client: Any, aigie_client: Any | None = None):
        """
        Initialize wrapper.

        Args:
            client: OpenAI client instance
            aigie_client: Optional Aigie client for API calls
        """
        self._client = client
        self._aigie = aigie_client
        self._original_client = client

    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to wrapped client."""
        attr = getattr(self._client, name)

        if name == "chat":
            return self._wrap_chat(attr)
        if name == "completions":
            return self._wrap_completions(attr)
        if name == "embeddings":
            return self._wrap_embeddings(attr)

        return attr

    def _wrap_chat(self, chat_obj: Any) -> Any:
        """Wrap chat completions."""

        class ChatWrapper:
            def __init__(wrapper_self, obj):
                wrapper_self._obj = obj

            def __getattr__(wrapper_self, name: str):
                attr = getattr(wrapper_self._obj, name)
                if name == "completions":
                    return wrapper_self._wrap_completions(attr)
                return attr

            def _wrap_completions(wrapper_self, completions_obj):
                class CompletionsWrapper:
                    def __init__(comp_self, obj):
                        comp_self._obj = obj

                    def __getattr__(comp_self, name: str):
                        attr = getattr(comp_self._obj, name)
                        if name == "create":
                            return self._trace_chat_completion(attr)
                        return attr

                return CompletionsWrapper(completions_obj)

        return ChatWrapper(chat_obj)

    def _trace_chat_completion(self, create_func: Callable) -> Callable:
        """Trace chat completion calls."""
        if self._is_async(create_func):

            @functools.wraps(create_func)
            async def async_wrapper(*args, **kwargs):
                return await self._handle_chat_completion_async(create_func, *args, **kwargs)

            return async_wrapper

        @functools.wraps(create_func)
        def sync_wrapper(*args, **kwargs):
            return self._handle_chat_completion_sync(create_func, *args, **kwargs)

        return sync_wrapper

    def _is_async(self, create_func: Callable) -> bool:
        """Detect an async `create`.

        iscoroutinefunction works for most cases, but openai v2.x uses a
        descriptor pattern where AsyncCompletions.create is not a standard
        coroutine function, so the owner's class name is the fallback.
        """
        if inspect.iscoroutinefunction(create_func):
            return True

        owner = getattr(create_func, "__self__", None) or getattr(create_func, "__objclass__", None)
        if owner is not None and "Async" in type(owner).__name__:
            return True

        return hasattr(self, "_client") and "Async" in type(self._client).__name__

    # ─── async path ──────────────────────────────────────────────────────

    async def _handle_chat_completion_async(self, func: Callable, *args, **kwargs) -> Any:
        """Handle async chat completion with tracing and real-time interception."""
        if not is_tracing_enabled():
            return await func(*args, **kwargs)

        # Skip our tracing if an instrumentation layer is already tracing this call.
        from aigie.auto_instrument.trace import is_in_llm_instrumentation

        if is_in_llm_instrumentation():
            return await func(*args, **kwargs)

        return await self._traced_call_async(func, *args, **kwargs)

    async def _traced_call_async(self, func: Callable, *args, **kwargs) -> Any:
        """Open the span, run the call, and emit the span whatever happens."""
        call = _Call.begin(kwargs)
        prev_span_ctx = get_current_span_context()
        set_current_span_context(call.run_ctx)

        try:
            return await self._invoke_async(func, call, args, kwargs)
        except Exception as e:
            return await self._after_error_async(func, call, e, args, kwargs)
        finally:
            await queue_llm_span_event(call.run_ctx, call.trace_id)
            set_current_span_context(prev_span_ctx)

    async def _invoke_async(self, func: Callable, call: _Call, args: tuple, kwargs: dict) -> Any:
        """Pre-call hooks, the provider call, and post-call hooks."""
        if call.intercepts:
            # The provider call reads the edits from `kwargs`, which run_pre_call
            # mutates in place. Keeping them on `call` too only keeps the state
            # object honest — nothing downstream reads them, because the span's
            # metadata was already stamped in `_Call.begin`. So an interception
            # that rewrites the model is traced under the *original* model.
            # Inherited; fixing it means stamping the span after the hooks run.
            call.interception_ctx, call.messages, call.model = await run_pre_call(
                call.aigie,
                model=call.model,
                messages=call.messages,
                kwargs=kwargs,
                trace_id=call.trace_id,
                span_id=call.run_ctx.id,
            )

        response = await func(*args, **kwargs)

        # A stream is consumed after this returns, so the generator emits its
        # own span once it finishes.
        if call.stream:
            return wrap_stream_async(response, call.run_ctx, call.interception_ctx)

        output_content = _record_success(call.run_ctx, response)

        if call.intercepts and call.interception_ctx:
            call.interception_ctx = await run_post_call(
                call.aigie,
                call.interception_ctx,
                run_ctx=call.run_ctx,
                response=response,
                output_content=output_content,
                kwargs=kwargs,
            )

        return response

    async def _after_error_async(
        self, func: Callable, call: _Call, error: Exception, args: tuple, kwargs: dict
    ) -> Any:
        """Honour a retry request, otherwise record the failure and re-raise."""
        retry_kwargs = retry_kwargs_from(error)
        if retry_kwargs is not None:
            reason = getattr(error, "reason", error)
            logger.debug("[wrapper] Retrying with modified parameters: %s", reason)
            return await self._handle_chat_completion_async(func, *args, **retry_kwargs)

        record_error(call.run_ctx, error)

        if call.intercepts and call.interception_ctx:
            fix_kwargs = await run_error_post_call(call.aigie, call.interception_ctx, error)
            if fix_kwargs:
                try:
                    return await self._handle_chat_completion_async(func, *args, **fix_kwargs)
                except Exception as retry_error:
                    # Inherited: a failed auto-fix retry must not replace the
                    # error the provider actually produced. The span was already
                    # stamped with that one, so surfacing the retry's instead
                    # would hand the caller an error the trace disagrees with.
                    logger.debug("[wrapper] Auto-fix retry failed: %s", retry_error)

        raise error

    # ─── sync path ───────────────────────────────────────────────────────

    def _handle_chat_completion_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Handle sync chat completion with tracing and basic interception."""
        if not is_tracing_enabled():
            return func(*args, **kwargs)

        from aigie.auto_instrument.trace import is_in_llm_instrumentation

        if is_in_llm_instrumentation():
            return func(*args, **kwargs)

        return self._traced_call_sync(func, *args, **kwargs)

    def _traced_call_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Sync twin of `_traced_call_async`."""
        call = _Call.begin(kwargs)
        prev_span_ctx = get_current_span_context()
        set_current_span_context(call.run_ctx)

        try:
            return self._invoke_sync(func, call, args, kwargs)
        except Exception as e:
            record_error(call.run_ctx, e)
            raise
        finally:
            queue_llm_span_event_sync(call.run_ctx, call.trace_id)
            set_current_span_context(prev_span_ctx)

    def _invoke_sync(self, func: Callable, call: _Call, args: tuple, kwargs: dict) -> Any:
        """Local rule check, the provider call, and the recorded result."""
        if call.aigie and call.aigie._rules_engine:
            run_sync_pre_call(
                call.aigie,
                model=call.model,
                messages=call.messages,
                kwargs=kwargs,
                trace_id=call.trace_ctx.id if call.trace_ctx else None,
                span_id=call.run_ctx.id,
            )

        response = func(*args, **kwargs)

        if call.stream:
            return wrap_stream_sync(response, call.run_ctx)

        _record_success(call.run_ctx, response)
        return response

    # ─── endpoints that are proxied but not yet traced ───────────────────

    def _wrap_completions(self, completions_obj: Any) -> Any:
        """Wrap completions (legacy)."""
        return completions_obj

    def _wrap_embeddings(self, embeddings_obj: Any) -> Any:
        """Wrap embeddings."""
        return embeddings_obj


def wrap_openai(client: Any, aigie_client: Any | None = None) -> Any:
    """
    Wrap OpenAI client for automatic tracing.

    Args:
        client: OpenAI client instance
        aigie_client: Optional Aigie client

    Returns:
        Wrapped client with tracing

    Example:
        import openai
        from aigie.wrappers import wrap_openai

        client = wrap_openai(openai.OpenAI())

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    return OpenAIWrapper(client, aigie_client)
