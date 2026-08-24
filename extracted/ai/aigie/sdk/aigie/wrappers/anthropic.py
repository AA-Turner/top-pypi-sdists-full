"""Tracing wrapper for the Anthropic client.

`wrap_anthropic` returns a stand-in that proxies attribute access to the real
client. Unlike the OpenAI wrapper this one keeps metadata lean: the prompt and
the completion travel as the span's own `input` and `output` fields rather than
inside metadata.

**It does not trace on the bare `wrap_anthropic(...)` path.** The `messages`
property below needs `_original_messages`, which only `auto_instrument.llm`
sets; without it the property raises AttributeError, `__getattr__` takes over,
and the caller receives the real client's untraced namespace. So spans appear
under auto-instrumentation and not otherwise. Inherited, pinned in
`test_wrapper_tracing.py`, and not fixed here.

This wrapper traces a *bare* Anthropic call — the customer imported the
anthropic library and called it directly. No agent framework is involved, so
the span claims none. Tracing through the Claude Agent SDK is a different path
entirely, in `aigie.integrations.claude_agent_sdk`, which stamps its own
`framework` where that is actually true.
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from aigie._system_prompt import system_prompt_text
from aigie.context_manager import (
    RunContext,
    get_current_span_context,
    get_current_trace_context,
    get_parent_context,
    set_current_span_context,
)
from aigie.cost_tracking import extract_and_calculate_cost
from aigie.wrappers._base import (
    SpanTotals,
    apply_duration,
    apply_totals,
    build_span_payload,
    record_error,
    stamp_totals_into_metadata,
)

logger = logging.getLogger(__name__)


def _new_run_context(model: str, trace_ctx: Any) -> RunContext:
    """Open a span for one messages.create.

    Metadata deliberately carries no `framework`: this is a bare provider call.
    It also stays lean — the prompt and completion are span fields, not metadata.
    """
    parent_ctx = get_parent_context()
    span_parent_id = parent_ctx.id if parent_ctx else (trace_ctx.id if trace_ctx else None)
    return RunContext(
        id=str(uuid4()),
        name=f"anthropic.messages.create [{model}]",
        type="span",
        span_type="llm",
        parent_id=span_parent_id,
        metadata={
            "provider": "anthropic",
            "model": model,
        },
        tags=["anthropic", "llm", model],
        start_time=datetime.now(timezone.utc),
    )


def _text_from_content_blocks(blocks: Any) -> str:
    """Concatenate the text of every content block that carries any."""
    output_text = ""
    for block in blocks:
        if hasattr(block, "text"):
            output_text += block.text
    return output_text


@dataclass
class _Call:
    """Everything one traced messages.create accumulates before it is emitted."""

    run_ctx: RunContext
    trace_ctx: Any
    span_input: dict = field(default_factory=dict)
    span_output: dict | None = None
    span_usage: dict | None = None
    span_cost: dict | None = None

    @property
    def trace_id(self) -> str:
        return self.trace_ctx.id if self.trace_ctx else self.run_ctx.id

    @classmethod
    def begin(cls, kwargs: dict) -> _Call:
        """Read the request and open its span."""
        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])

        trace_ctx = get_current_trace_context()
        run_ctx = _new_run_context(model, trace_ctx)

        system_text = system_prompt_text(kwargs.get("system"))
        if system_text:
            run_ctx.metadata["system_prompt"] = system_text

        # Not a message, but still part of what the model was asked.
        span_input: dict[str, Any] = {"messages": messages}
        if system_text:
            span_input["system_prompt"] = system_text

        return cls(run_ctx=run_ctx, trace_ctx=trace_ctx, span_input=span_input)

    def record_response(self, response: Any, *, fall_back_to_repr: bool) -> None:
        """Read the completion, tokens and cost off the provider's response.

        `fall_back_to_repr` carries an inherited divergence between the two
        paths: given a response with no content, the async handler recorded
        `str(response)` as the output while the sync handler recorded none.
        """
        if getattr(response, "content", None):
            self.span_output = {"content": _text_from_content_blocks(response.content)}
        elif fall_back_to_repr:
            self.span_output = {"content": str(response)}

        self._record_usage_and_cost(response)

    def _record_usage_and_cost(self, response: Any) -> None:
        if not hasattr(response, "usage"):
            return

        usage = response.usage
        input_tokens = getattr(usage, "input_tokens", 0)
        output_tokens = getattr(usage, "output_tokens", 0)
        self.span_usage = {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        }

        try:
            cost_info = extract_and_calculate_cost(response, "anthropic")
        except Exception as e:
            # Contained: an unpriceable span still ships. Logged so a gap in
            # the pricing table is discoverable rather than invisible.
            logger.debug("[wrapper] Cost calculation failed for anthropic: %s", e)
            cost_info = None

        if cost_info:
            self.span_cost = {
                "input_cost": float(cost_info.input_cost),
                "output_cost": float(cost_info.output_cost),
                "total_cost": float(cost_info.total_cost),
                "currency": cost_info.currency,
            }


async def emit_span(call: _Call) -> None:
    """Emit the finalized span, exactly once.

    Two details differ from the shared emitter and are passed explicitly: any
    non-zero cost component counts as a cost, and totals are also stamped back
    into metadata for backend extraction.
    """
    try:
        from aigie.client import get_aigie

        aigie = get_aigie()
        if not aigie or not aigie._buffer:
            return

        end_time = datetime.now(timezone.utc)
        totals = SpanTotals.from_usage_and_cost(
            call.span_usage, call.span_cost, derive_total_tokens=False
        )

        payload = build_span_payload(
            call.run_ctx,
            call.trace_id,
            span_input=call.span_input,
            span_output=call.span_output,
            end_time=end_time,
        )
        apply_totals(payload, totals, include_cost=totals.has_any_cost)
        stamp_totals_into_metadata(payload, totals)
        apply_duration(payload, call.run_ctx, end_time, with_latency=True)

        await aigie._buffer.add(payload)
        logger.debug(
            "[wrapper] Queued Anthropic span: %s (%s) -> trace:%s",
            call.run_ctx.name,
            call.run_ctx.id,
            call.trace_id,
        )

    except Exception as e:
        logger.debug("[wrapper] Failed to queue Anthropic span: %s", e)


def _emit_span_from_sync(call: _Call) -> None:
    """Emit from sync code.

    Identical to the shared `schedule_async` when a loop is already running —
    both create a task. They diverge when no loop is running: `schedule_async`
    uses a thread with its own loop, while this calls `asyncio.run` directly,
    which `schedule_async`'s own docstring says must not happen on an SDK hot
    path because the throwaway loop competes with the caller's. Inherited and
    preserved deliberately; changing it changes sync emission for every
    Anthropic call, which is not this change's job.
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(emit_span(call))
    except RuntimeError:
        try:
            asyncio.run(emit_span(call))
        except Exception as e:
            logger.debug("[wrapper] Failed to queue span sync: %s", e)


class AnthropicWrapper:
    """
    Wrapper for Anthropic client with automatic tracing.

    Usage:
        from aigie.wrappers import wrap_anthropic
        import anthropic

        client = wrap_anthropic(anthropic.Anthropic())

        # All calls are now automatically traced
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}]
        )
    """

    def __init__(self, client: Any, aigie_client: Any | None = None):
        self._client = client
        self._aigie = aigie_client

    @property
    def messages(self):
        """Return wrapped messages namespace using pre-saved original."""
        # _original_messages is set by auto_instrument/llm.py during traced_init
        original_messages = object.__getattribute__(self, "_original_messages")
        return self._wrap_messages(original_messages)

    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to wrapped client."""
        return getattr(self._client, name)

    def _wrap_messages(self, messages_obj: Any) -> Any:
        """Wrap messages namespace to intercept create()."""
        wrapper_self = self

        class MessagesWrapper:
            def __init__(mw_self, obj):
                mw_self._obj = obj

            def __getattr__(mw_self, name: str):
                attr = getattr(mw_self._obj, name)
                if name == "create":
                    return wrapper_self._trace_messages_create(attr)
                return attr

        return MessagesWrapper(messages_obj)

    def _trace_messages_create(self, create_func: Callable) -> Callable:
        """Trace messages.create calls."""
        # AsyncAnthropic's messages.create may not be detected by
        # iscoroutinefunction because of SDK internal decorators, so the client
        # type is also checked.
        is_async = (
            inspect.iscoroutinefunction(create_func)
            or asyncio.iscoroutinefunction(create_func)
            or "Async" in type(self._client).__name__
        )

        if is_async:

            @functools.wraps(create_func)
            async def async_wrapper(*args, **kwargs):
                return await self._handle_messages_create_async(create_func, *args, **kwargs)

            return async_wrapper

        @functools.wraps(create_func)
        def sync_wrapper(*args, **kwargs):
            return self._handle_messages_create_sync(create_func, *args, **kwargs)

        return sync_wrapper

    async def _handle_messages_create_async(self, func: Callable, *args, **kwargs) -> Any:
        """Handle async messages.create with tracing."""
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
            response = await func(*args, **kwargs)
            call.record_response(response, fall_back_to_repr=True)
            call.run_ctx.metadata["status"] = "success"
            return response
        except Exception as e:
            record_error(call.run_ctx, e)
            raise
        finally:
            await emit_span(call)
            set_current_span_context(prev_span_ctx)

    def _handle_messages_create_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Handle sync messages.create with tracing."""
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
            response = func(*args, **kwargs)
            call.record_response(response, fall_back_to_repr=False)
            call.run_ctx.metadata["status"] = "success"
            return response
        except Exception as e:
            record_error(call.run_ctx, e)
            raise
        finally:
            _emit_span_from_sync(call)
            set_current_span_context(prev_span_ctx)


def wrap_anthropic(client: Any, aigie_client: Any | None = None) -> Any:
    """
    Wrap Anthropic client for automatic tracing.

    Args:
        client: Anthropic client instance
        aigie_client: Optional Aigie client

    Returns:
        Wrapped client with tracing

    Example:
        import anthropic
        from aigie.wrappers import wrap_anthropic

        client = wrap_anthropic(anthropic.Anthropic())

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    return AnthropicWrapper(client, aigie_client)
