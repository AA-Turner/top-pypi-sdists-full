"""
Framework wrappers for automatic tracing of LLM providers.

Provides drop-in replacements and wrappers for:
- OpenAI (including Azure OpenAI)
- Anthropic Claude
- Google Gemini
- Generic LLM wrapper pattern

Features:
- Zero-code-change integration
- Automatic token tracking
- Cost calculation
- Streaming support
- Error handling and retries
- Context propagation
- Automatic event queueing to platform
"""

import asyncio
import functools
import inspect
import logging
from collections.abc import AsyncIterator, Callable, Iterator
from datetime import datetime, timezone
from typing import Any

from .buffer import EventType
from .context_manager import (
    RunContext,
    get_current_span_context,
    get_current_trace_context,
    get_parent_context,
    is_tracing_enabled,
    set_current_span_context,
)
from .cost_tracking import extract_and_calculate_cost

logger = logging.getLogger(__name__)


def _extract_system_prompt(messages: list) -> str | None:
    """
    Extract system prompt from messages array.

    Supports various message formats (OpenAI, Anthropic, dict, object).
    Returns the first system message content found.
    """
    if not messages:
        return None

    for msg in messages:
        # Handle dict-style messages
        if isinstance(msg, dict):
            role = msg.get("role", "")
            if role == "system":
                content = msg.get("content", "")
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    # Handle content blocks (e.g., [{"type": "text", "text": "..."}])
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            text_parts.append(block)
                    return " ".join(text_parts) if text_parts else None
        # Handle object-style messages (e.g., ChatCompletionMessage)
        elif hasattr(msg, "role"):
            role = getattr(msg, "role", None)
            if role == "system":
                content = getattr(msg, "content", None)
                if isinstance(content, str):
                    return content

    return None


def _update_trace_system_prompt(system_prompt: str) -> None:
    """
    Update the current trace's metadata with the extracted system prompt.

    Only updates if the trace doesn't already have a system prompt set.
    """
    try:
        trace_ctx = get_current_trace_context()
        if trace_ctx and hasattr(trace_ctx, "metadata"):
            # Only set if not already provided by user
            if "kytte.system_prompt" not in trace_ctx.metadata:
                trace_ctx.metadata["kytte.system_prompt"] = system_prompt
                logger.debug(
                    f"[wrapper] Auto-extracted system prompt ({len(system_prompt)} chars) to trace metadata"
                )
    except Exception as e:
        logger.debug(f"[wrapper] Could not update trace with system prompt: {e}")


async def _queue_llm_span_event(run_ctx: RunContext, trace_id: str) -> None:
    """
    Queue an LLM span event using two-phase SPAN_CREATE + SPAN_UPDATE.

    Uses the same pattern as SpanContext to ensure output, tokens, and cost
    data flows to the backend correctly.
    """
    try:
        from .client import get_aigie

        aigie = get_aigie()
        if not aigie or not aigie._buffer:
            logger.debug("[wrapper] No global Aigie client - skipping LLM span event queue")
            return

        end_time = datetime.now(timezone.utc)
        meta = run_ctx.metadata

        # Extract usage and cost from metadata
        usage = meta.get("usage", {})
        cost = meta.get("cost", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
        input_cost = cost.get("input_cost", 0.0)
        output_cost = cost.get("output_cost", 0.0)
        total_cost = cost.get("total_cost", 0.0)

        # Phase 1: SPAN_CREATE - basic structure (matches SpanCreateRequest)
        create_payload = {
            "id": run_ctx.id,
            "name": run_ctx.name,
            "trace_id": trace_id,
            "parent_id": run_ctx.parent_id if run_ctx.parent_id != trace_id else None,
            "type": "llm",
            "start_time": run_ctx.start_time.isoformat()
            if run_ctx.start_time
            else end_time.isoformat(),
            "metadata": meta,
            "tags": run_ctx.tags,
            "input": meta.get("input"),
            "model": meta.get("model"),
            "level": "ERROR" if meta.get("status") == "error" else "DEFAULT",
        }

        # Nested usage objects for SpanCreateRequest
        if prompt_tokens > 0 or completion_tokens > 0:
            create_payload["usage"] = {
                "input": prompt_tokens,
                "output": completion_tokens,
                "total": total_tokens,
                "unit": "TOKENS",
            }
            create_payload["token_usage"] = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            }
        if total_cost > 0:
            create_payload["cost_details"] = {
                "input_cost": input_cost,
                "output_cost": output_cost,
                "total_cost": total_cost,
            }

        await aigie._buffer.add(EventType.SPAN_CREATE, create_payload)

        # Phase 2: SPAN_UPDATE - output, tokens, cost (matches SpanUpdateRequest)
        update_payload = {
            "id": run_ctx.id,
            "span_id": run_ctx.id,
            "trace_id": trace_id,
            "name": run_ctx.name,
            "type": "llm",
            "start_time": run_ctx.start_time.isoformat()
            if run_ctx.start_time
            else end_time.isoformat(),
            "end_time": end_time.isoformat(),
            "input": meta.get("input"),
            "output": meta.get("output"),
            "metadata": meta,
            "status": meta.get("status", "success"),
            "model": meta.get("model"),
        }

        if run_ctx.parent_id and run_ctx.parent_id != trace_id:
            update_payload["parent_id"] = run_ctx.parent_id

        # Direct fields for SpanUpdateRequest
        if prompt_tokens > 0 or completion_tokens > 0:
            update_payload["prompt_tokens"] = prompt_tokens
            update_payload["completion_tokens"] = completion_tokens
            update_payload["total_tokens"] = total_tokens
        if total_cost > 0:
            update_payload["input_cost"] = input_cost
            update_payload["output_cost"] = output_cost
            update_payload["total_cost"] = total_cost

        # Also include nested usage objects
        if prompt_tokens > 0 or completion_tokens > 0 or total_cost > 0:
            update_payload["usage"] = {
                "input": prompt_tokens,
                "output": completion_tokens,
                "total": total_tokens,
                "unit": "TOKENS",
                "input_cost": input_cost if input_cost > 0 else None,
                "output_cost": output_cost if output_cost > 0 else None,
                "total_cost": total_cost if total_cost > 0 else None,
            }
            update_payload["token_usage"] = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "input_cost": input_cost if input_cost > 0 else None,
                "output_cost": output_cost if output_cost > 0 else None,
                "total_cost": total_cost if total_cost > 0 else None,
            }

        # Calculate duration
        if run_ctx.start_time:
            duration_ns = int((end_time - run_ctx.start_time).total_seconds() * 1e9)
            update_payload["duration"] = duration_ns

        # Add model provider and framework
        if "provider" in meta:
            update_payload["model_provider"] = meta["provider"]
        if "framework" in meta:
            update_payload["framework"] = meta["framework"]

        await aigie._buffer.add(EventType.SPAN_UPDATE, update_payload)
        logger.debug(
            f"[wrapper] Queued LLM span event: {run_ctx.name} ({run_ctx.id}) -> trace:{trace_id}"
        )

    except Exception as e:
        logger.warning(f"[wrapper] Failed to queue LLM span event: {e}")


def _queue_llm_span_event_sync(run_ctx: RunContext, trace_id: str) -> None:
    """Synchronously queue an LLM span event (schedules async operation)."""
    from .utils.safe import schedule_async

    schedule_async(_queue_llm_span_event(run_ctx, trace_id))


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

        # Wrap chat.completions.create
        if name == "chat":
            return self._wrap_chat(attr)

        # Wrap completions.create
        if name == "completions":
            return self._wrap_completions(attr)

        # Wrap embeddings.create
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
        # Detect async: iscoroutinefunction works for most cases, but openai v2.x
        # uses a descriptor pattern where AsyncCompletions.create is not a standard
        # coroutine function. Check the class name as a fallback.
        is_async = inspect.iscoroutinefunction(create_func)
        if not is_async:
            owner = getattr(create_func, "__self__", None) or getattr(
                create_func, "__objclass__", None
            )
            if owner is not None:
                owner_name = type(owner).__name__
                is_async = "Async" in owner_name
            # Also check if the client stored on our wrapper is async
            if not is_async and hasattr(self, "_client"):
                is_async = "Async" in type(self._client).__name__

        if is_async:

            @functools.wraps(create_func)
            async def async_wrapper(*args, **kwargs):
                return await self._handle_chat_completion_async(create_func, *args, **kwargs)

            return async_wrapper

        @functools.wraps(create_func)
        def sync_wrapper(*args, **kwargs):
            return self._handle_chat_completion_sync(create_func, *args, **kwargs)

        return sync_wrapper

    async def _handle_chat_completion_async(self, func: Callable, *args, **kwargs) -> Any:
        """Handle async chat completion with tracing and real-time interception."""
        if not is_tracing_enabled():
            return await func(*args, **kwargs)

        # Recursion guard: skip wrapper tracing if already inside an LLM instrumentation layer
        from .auto_instrument.trace import is_in_llm_instrumentation

        if is_in_llm_instrumentation():
            return await func(*args, **kwargs)

        from uuid import uuid4

        from .client import get_aigie

        # Extract parameters
        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])
        stream = kwargs.get("stream", False)

        # Auto-extract system prompt and update trace metadata
        system_prompt = _extract_system_prompt(messages)
        if system_prompt:
            _update_trace_system_prompt(system_prompt)

        # Create span context
        parent_ctx = get_parent_context()
        trace_ctx = get_current_trace_context()
        run_id = str(uuid4())
        run_ctx = RunContext(
            id=run_id,
            name="openai.chat.completions.create",
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

        prev_span_ctx = get_current_span_context()
        set_current_span_context(run_ctx)

        # Real-time interception context
        interception_ctx = None
        aigie = get_aigie()
        trace_id = trace_ctx.id if trace_ctx else run_id

        try:
            # ==================== FEED CONTEXT AGGREGATOR (Phase 1.2) ====================
            if aigie and aigie._context_aggregator:
                try:
                    aigie._context_aggregator.add_span(
                        trace_id=trace_id,
                        span_id=run_id,
                        span_type="llm",
                        parent_span_id=run_ctx.parent_id,
                        name=run_ctx.name,
                        input_messages=messages,
                        model=model,
                        provider="openai",
                    )
                except Exception:
                    pass  # Never block agent

            # ==================== PRE-CALL INTERCEPTION ====================
            if aigie and aigie._interceptor_chain:
                try:
                    interception_ctx = await aigie.intercept_pre_call(
                        provider="openai",
                        model=model,
                        messages=messages,
                        trace_id=trace_id,
                        span_id=run_id,
                        **{k: v for k, v in kwargs.items() if k not in ["messages", "model"]},
                    )

                    # Check if request was blocked
                    from .interceptor.protocols import (
                        InterceptionBlockedError,
                        InterceptionDecision,
                    )

                    if interception_ctx.decision == InterceptionDecision.BLOCK:
                        raise InterceptionBlockedError(
                            reason=interception_ctx.block_reason
                            or "Request blocked by interception",
                            hook_name="pre_call",
                        )

                    # Apply modifications if any
                    if interception_ctx.modified_messages:
                        kwargs["messages"] = interception_ctx.modified_messages
                        messages = interception_ctx.modified_messages
                    if interception_ctx.modified_kwargs:
                        kwargs.update(interception_ctx.modified_kwargs)
                        model = kwargs.get("model", model)

                except ImportError:
                    # Interception modules not available
                    pass

            # ==================== CALL OPENAI ====================
            response = await func(*args, **kwargs)

            # Handle streaming
            if stream:
                return self._wrap_stream_async(response, run_ctx, interception_ctx)

            # Extract response data
            if hasattr(response, "choices") and len(response.choices) > 0:
                output_message = response.choices[0].message
                output_content = (
                    output_message.content
                    if hasattr(output_message, "content")
                    else str(output_message)
                )
            else:
                output_content = str(response)

            # Track tokens and calculate cost
            if hasattr(response, "usage"):
                run_ctx.metadata["usage"] = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }

                # Automatic cost tracking
                try:
                    cost_info = extract_and_calculate_cost(response, "openai")
                except Exception:
                    cost_info = None
                if cost_info:
                    run_ctx.metadata["cost"] = {
                        "input_cost": float(cost_info.input_cost),
                        "output_cost": float(cost_info.output_cost),
                        "total_cost": float(cost_info.total_cost),
                        "currency": cost_info.currency,
                    }

            run_ctx.metadata["output"] = {"content": output_content}
            run_ctx.metadata["status"] = "success"

            # ==================== POST-CALL INTERCEPTION ====================
            if aigie and aigie._interceptor_chain and interception_ctx:
                try:
                    # Update interception context with cost/token info
                    if "cost" in run_ctx.metadata:
                        interception_ctx.actual_cost = run_ctx.metadata["cost"].get("total_cost", 0)
                    if "usage" in run_ctx.metadata:
                        interception_ctx.actual_input_tokens = run_ctx.metadata["usage"].get(
                            "prompt_tokens", 0
                        )
                        interception_ctx.actual_output_tokens = run_ctx.metadata["usage"].get(
                            "completion_tokens", 0
                        )
                    interception_ctx.response_content = output_content

                    interception_ctx = await aigie.intercept_post_call(
                        ctx=interception_ctx,
                        response=response,
                        error=None,
                    )

                    # Handle retry request
                    from .interceptor.protocols import InterceptionDecision, InterceptionRetryError

                    if (
                        interception_ctx.decision == InterceptionDecision.MODIFY
                        and interception_ctx.should_retry
                    ):
                        # Apply retry with modified parameters
                        retry_kwargs = interception_ctx.retry_kwargs or kwargs
                        raise InterceptionRetryError(
                            reason="Post-call interception requested retry",
                            retry_kwargs=retry_kwargs,
                        )

                    # Apply response modifications if any
                    if interception_ctx.modified_response:
                        # Return modified response (for content changes)
                        logger.debug("[wrapper] Applying post-call response modification")
                        # Note: We can't easily modify the OpenAI response object,
                        # but we update our tracking metadata
                        run_ctx.metadata["output"] = {
                            "content": interception_ctx.modified_response.get(
                                "content", output_content
                            )
                        }
                        run_ctx.metadata["interception_modified"] = True

                except ImportError:
                    pass

            return response

        except Exception as e:
            # Check if it's an interception retry request
            try:
                from .interceptor.protocols import InterceptionRetryError

                if isinstance(e, InterceptionRetryError) and e.retry_kwargs:
                    logger.info(f"[wrapper] Retrying with modified parameters: {e.reason}")
                    # Recursive retry with modified kwargs
                    return await self._handle_chat_completion_async(func, *args, **e.retry_kwargs)
            except ImportError:
                pass

            run_ctx.metadata["error"] = {
                "type": type(e).__name__,
                "message": str(e),
            }
            run_ctx.metadata["status"] = "error"

            # Post-call interception for errors
            if aigie and aigie._interceptor_chain and interception_ctx:
                try:
                    interception_ctx = await aigie.intercept_post_call(
                        ctx=interception_ctx,
                        response=None,
                        error=e,
                    )

                    # Check if auto-fix suggests retry
                    from .interceptor.protocols import InterceptionDecision

                    if interception_ctx.should_retry and interception_ctx.retry_kwargs:
                        logger.info("[wrapper] Auto-fix retry after error")
                        return await self._handle_chat_completion_async(
                            func, *args, **interception_ctx.retry_kwargs
                        )
                except ImportError:
                    pass
                except Exception as intercept_error:
                    logger.debug(
                        f"[wrapper] Post-call error interception failed: {intercept_error}"
                    )

            raise

        finally:
            # Queue LLM span event to buffer for API submission
            trace_id = trace_ctx.id if trace_ctx else run_ctx.id
            await _queue_llm_span_event(run_ctx, trace_id)

            set_current_span_context(prev_span_ctx)

    def _handle_chat_completion_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Handle sync chat completion with tracing and basic interception."""
        if not is_tracing_enabled():
            return func(*args, **kwargs)

        # Recursion guard: skip wrapper tracing if already inside an LLM instrumentation layer
        from .auto_instrument.trace import is_in_llm_instrumentation

        if is_in_llm_instrumentation():
            return func(*args, **kwargs)

        from uuid import uuid4

        from .client import get_aigie

        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])
        stream = kwargs.get("stream", False)

        # Auto-extract system prompt and update trace metadata
        system_prompt = _extract_system_prompt(messages)
        if system_prompt:
            _update_trace_system_prompt(system_prompt)

        parent_ctx = get_parent_context()
        trace_ctx = get_current_trace_context()
        run_id = str(uuid4())
        run_ctx = RunContext(
            id=run_id,
            name="openai.chat.completions.create",
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

        prev_span_ctx = get_current_span_context()
        set_current_span_context(run_ctx)

        # Basic sync interception using rules engine directly
        aigie = get_aigie()

        try:
            # ==================== SYNC PRE-CALL INTERCEPTION ====================
            # For sync calls, we can only use the local rules engine (no async backend)
            if aigie and aigie._rules_engine:
                try:
                    from .interceptor.protocols import (
                        InterceptionBlockedError,
                        InterceptionContext,
                        InterceptionDecision,
                    )

                    # Create interception context
                    interception_ctx = InterceptionContext(
                        provider="openai",
                        model=model,
                        messages=messages,
                        trace_id=trace_ctx.id if trace_ctx else None,
                        span_id=run_id,
                        request_kwargs=kwargs,
                    )

                    # Evaluate local rules synchronously (rules engine is sync)
                    # We can't call the full async chain, but we can check rules
                    try:
                        from .utils.safe import schedule_async

                        result = schedule_async(aigie._rules_engine.evaluate(interception_ctx))
                        if result is not None and result.decision == InterceptionDecision.BLOCK:
                            raise InterceptionBlockedError(
                                reason=result.reason or "Request blocked by rules",
                                hook_name="rules_engine",
                            )
                    except Exception as rule_error:
                        if isinstance(rule_error, InterceptionBlockedError):
                            raise
                        logger.debug(f"[wrapper] Sync rules evaluation failed: {rule_error}")

                except ImportError:
                    pass

            # ==================== CALL OPENAI ====================
            response = func(*args, **kwargs)

            if stream:
                return self._wrap_stream_sync(response, run_ctx)

            if hasattr(response, "choices") and len(response.choices) > 0:
                output_message = response.choices[0].message
                output_content = (
                    output_message.content
                    if hasattr(output_message, "content")
                    else str(output_message)
                )
            else:
                output_content = str(response)

            if hasattr(response, "usage"):
                run_ctx.metadata["usage"] = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }

                # Automatic cost tracking
                try:
                    cost_info = extract_and_calculate_cost(response, "openai")
                except Exception:
                    cost_info = None
                if cost_info:
                    run_ctx.metadata["cost"] = {
                        "input_cost": float(cost_info.input_cost),
                        "output_cost": float(cost_info.output_cost),
                        "total_cost": float(cost_info.total_cost),
                        "currency": cost_info.currency,
                    }

            run_ctx.metadata["output"] = {"content": output_content}
            run_ctx.metadata["status"] = "success"

            return response

        except Exception as e:
            run_ctx.metadata["error"] = {
                "type": type(e).__name__,
                "message": str(e),
            }
            run_ctx.metadata["status"] = "error"
            raise

        finally:
            # Queue LLM span event to buffer for API submission
            trace_id = trace_ctx.id if trace_ctx else run_ctx.id
            _queue_llm_span_event_sync(run_ctx, trace_id)

            set_current_span_context(prev_span_ctx)

    async def _wrap_stream_async(
        self, stream: AsyncIterator, run_ctx: RunContext, interception_ctx: Any = None
    ) -> AsyncIterator:
        """Wrap async stream to collect chunks and calculate streaming metrics."""
        import time

        chunks = []
        first_chunk_time = None
        last_chunk_time = None
        total_tokens = 0
        trace_ctx = get_current_trace_context()

        try:
            async for chunk in stream:
                if first_chunk_time is None:
                    first_chunk_time = time.time()
                last_chunk_time = time.time()

                chunks.append(chunk)
                yield chunk

                # Count tokens in chunk if available
                if hasattr(chunk, "usage") and chunk.usage:
                    if hasattr(chunk.usage, "total_tokens"):
                        total_tokens = chunk.usage.total_tokens
                    elif isinstance(chunk.usage, dict):
                        total_tokens = chunk.usage.get("total_tokens", 0)

            # Aggregate content
            full_content = ""
            for chunk in chunks:
                if hasattr(chunk, "choices") and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        full_content += delta.content

            # Calculate streaming metrics
            streaming_metrics = {}
            if first_chunk_time and last_chunk_time:
                time_to_first_token_ms = (first_chunk_time - run_ctx.start_time.timestamp()) * 1000
                streaming_duration_ms = (last_chunk_time - first_chunk_time) * 1000
                streaming_metrics["time_to_first_token_ms"] = time_to_first_token_ms
                streaming_metrics["streaming_duration_ms"] = streaming_duration_ms
                streaming_metrics["chunk_count"] = len(chunks)

                # Calculate tokens per second if we have tokens and duration
                if total_tokens > 0 and streaming_duration_ms > 0:
                    streaming_metrics["tokens_per_second"] = (
                        total_tokens / streaming_duration_ms
                    ) * 1000
                elif streaming_duration_ms > 0:
                    # Estimate tokens from content length (rough estimate: 1 token ≈ 4 chars)
                    estimated_tokens = len(full_content) / 4
                    streaming_metrics["estimated_tokens_per_second"] = (
                        estimated_tokens / streaming_duration_ms
                    ) * 1000

            # Update token usage from final chunk if available
            if total_tokens > 0:
                run_ctx.metadata["usage"] = {
                    "total_tokens": total_tokens,
                }

            run_ctx.metadata["output"] = {"content": full_content}
            run_ctx.metadata["stream_chunks"] = len(chunks)
            run_ctx.metadata["streaming"] = True
            if streaming_metrics:
                run_ctx.metadata["streaming_metrics"] = streaming_metrics
            run_ctx.metadata["status"] = "success"

            # Post-call interception for streaming
            if interception_ctx:
                try:
                    from .client import get_aigie

                    aigie = get_aigie()
                    if aigie and aigie._interceptor_chain:
                        interception_ctx.response_content = full_content
                        if total_tokens > 0:
                            interception_ctx.actual_output_tokens = total_tokens
                        await aigie.intercept_post_call(
                            ctx=interception_ctx,
                            response=None,  # Streaming doesn't have a single response object
                            error=None,
                        )
                except Exception as intercept_error:
                    logger.debug(
                        f"[wrapper] Stream post-call interception failed: {intercept_error}"
                    )

        except Exception as e:
            run_ctx.metadata["error"] = {"type": type(e).__name__, "message": str(e)}
            run_ctx.metadata["status"] = "error"
            raise

        finally:
            # Queue LLM span event after streaming completes
            trace_id = trace_ctx.id if trace_ctx else run_ctx.id
            await _queue_llm_span_event(run_ctx, trace_id)

    def _wrap_stream_sync(
        self, stream: Iterator, run_ctx: RunContext, interception_ctx: Any = None
    ) -> Iterator:
        """Wrap sync stream to collect chunks and calculate streaming metrics."""
        import time

        chunks = []
        first_chunk_time = None
        last_chunk_time = None
        total_tokens = 0
        trace_ctx = get_current_trace_context()

        try:
            for chunk in stream:
                if first_chunk_time is None:
                    first_chunk_time = time.time()
                last_chunk_time = time.time()

                chunks.append(chunk)
                yield chunk

                # Count tokens in chunk if available
                if hasattr(chunk, "usage") and chunk.usage:
                    if hasattr(chunk.usage, "total_tokens"):
                        total_tokens = chunk.usage.total_tokens
                    elif isinstance(chunk.usage, dict):
                        total_tokens = chunk.usage.get("total_tokens", 0)

            full_content = ""
            for chunk in chunks:
                if hasattr(chunk, "choices") and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        full_content += delta.content

            # Calculate streaming metrics (same as async version)
            streaming_metrics = {}
            if first_chunk_time and last_chunk_time:
                time_to_first_token_ms = (first_chunk_time - run_ctx.start_time.timestamp()) * 1000
                streaming_duration_ms = (last_chunk_time - first_chunk_time) * 1000
                streaming_metrics["time_to_first_token_ms"] = time_to_first_token_ms
                streaming_metrics["streaming_duration_ms"] = streaming_duration_ms
                streaming_metrics["chunk_count"] = len(chunks)

                if total_tokens > 0 and streaming_duration_ms > 0:
                    streaming_metrics["tokens_per_second"] = (
                        total_tokens / streaming_duration_ms
                    ) * 1000
                elif streaming_duration_ms > 0:
                    estimated_tokens = len(full_content) / 4
                    streaming_metrics["estimated_tokens_per_second"] = (
                        estimated_tokens / streaming_duration_ms
                    ) * 1000

            # Update token usage from final chunk if available
            if total_tokens > 0:
                run_ctx.metadata["usage"] = {
                    "total_tokens": total_tokens,
                }

            run_ctx.metadata["output"] = {"content": full_content}
            run_ctx.metadata["stream_chunks"] = len(chunks)
            run_ctx.metadata["streaming"] = True
            if streaming_metrics:
                run_ctx.metadata["streaming_metrics"] = streaming_metrics
            run_ctx.metadata["status"] = "success"

        except Exception as e:
            run_ctx.metadata["error"] = {"type": type(e).__name__, "message": str(e)}
            run_ctx.metadata["status"] = "error"
            raise

        finally:
            # Queue LLM span event after streaming completes
            trace_id = trace_ctx.id if trace_ctx else run_ctx.id
            _queue_llm_span_event_sync(run_ctx, trace_id)

    def _wrap_completions(self, completions_obj: Any) -> Any:
        """Wrap completions (legacy)."""
        # Similar pattern for legacy completions endpoint
        return completions_obj

    def _wrap_embeddings(self, embeddings_obj: Any) -> Any:
        """Wrap embeddings."""
        # Similar pattern for embeddings
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

        client = wrap_openai(openai.OpenAI(api_key="..."))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    return OpenAIWrapper(client, aigie_client)


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
        # Check if the client is async (AsyncAnthropic) or if the function is a coroutine.
        # AsyncAnthropic's messages.create may not be detected by iscoroutinefunction
        # because of SDK internal decorators, so also check the client type.
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
        # Recursion guard: skip wrapper tracing if already inside an LLM instrumentation layer
        from .auto_instrument.trace import is_in_llm_instrumentation

        if is_in_llm_instrumentation():
            return await func(*args, **kwargs)

        from uuid import uuid4

        from .client import get_aigie

        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])
        system = kwargs.get("system")

        trace_ctx = get_current_trace_context()
        get_aigie()

        # Create span context - keep metadata lean (no large input/output)
        parent_ctx = get_parent_context()
        run_id = str(uuid4())
        span_parent_id = parent_ctx.id if parent_ctx else (trace_ctx.id if trace_ctx else None)
        run_ctx = RunContext(
            id=run_id,
            name=f"anthropic.messages.create [{model}]",
            type="span",
            span_type="llm",
            parent_id=span_parent_id,
            metadata={
                "provider": "anthropic",
                "model": model,
                "framework": "claude_agent_sdk",
            },
            tags=["anthropic", "llm", model],
            start_time=datetime.now(timezone.utc),
        )

        if system:
            run_ctx.metadata["system_prompt"] = system if isinstance(system, str) else str(system)

        # Store input/output as separate fields, NOT inside metadata
        span_input = {"messages": messages}
        span_output = None
        span_usage = None
        span_cost = None

        prev_span_ctx = get_current_span_context()
        set_current_span_context(run_ctx)

        # Interception context for autonomous retry routing.
        _aigie_for_retry = get_aigie()
        _intercept_ctx = None
        if (
            _aigie_for_retry
            and getattr(_aigie_for_retry, "_initialized", False)
            and getattr(getattr(_aigie_for_retry, "config", None), "autonomous", False)
        ):
            try:
                _intercept_ctx = await _aigie_for_retry.intercept_pre_call(
                    provider="anthropic",
                    model=kwargs.get("model", "unknown"),
                    messages=kwargs.get("messages", []),
                )
            except Exception:
                _intercept_ctx = None

        async def _do_call():
            return await func(*args, **kwargs)

        from .autonomous.inline_call import acall_with_autonomous

        try:
            response = await acall_with_autonomous(_do_call, _intercept_ctx, _aigie_for_retry)

            # Extract response data
            if hasattr(response, "content") and response.content:
                content_blocks = response.content
                output_text = ""
                for block in content_blocks:
                    if hasattr(block, "text"):
                        output_text += block.text
                    elif hasattr(block, "type") and block.type == "text":
                        output_text += getattr(block, "text", "")
                span_output = {"content": output_text}
            else:
                span_output = {"content": str(response)}

            # Track tokens and calculate cost
            if hasattr(response, "usage"):
                usage = response.usage
                input_tokens = getattr(usage, "input_tokens", 0)
                output_tokens = getattr(usage, "output_tokens", 0)
                span_usage = {
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                }

                try:
                    cost_info = extract_and_calculate_cost(response, "anthropic")
                except Exception:
                    cost_info = None
                if cost_info:
                    span_cost = {
                        "input_cost": float(cost_info.input_cost),
                        "output_cost": float(cost_info.output_cost),
                        "total_cost": float(cost_info.total_cost),
                        "currency": cost_info.currency,
                    }

            run_ctx.metadata["status"] = "success"
            return response

        except Exception as e:
            run_ctx.metadata["error"] = {
                "type": type(e).__name__,
                "message": str(e),
            }
            run_ctx.metadata["status"] = "error"
            raise

        finally:
            trace_id = trace_ctx.id if trace_ctx else run_ctx.id
            await self._queue_anthropic_span(
                run_ctx, trace_id, span_input, span_output, span_usage, span_cost
            )
            set_current_span_context(prev_span_ctx)

    def _handle_messages_create_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Handle sync messages.create with tracing."""
        # Recursion guard: skip wrapper tracing if already inside an LLM instrumentation layer
        from .auto_instrument.trace import is_in_llm_instrumentation

        if is_in_llm_instrumentation():
            return func(*args, **kwargs)

        from uuid import uuid4

        from .client import get_aigie

        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])
        system = kwargs.get("system")

        trace_ctx = get_current_trace_context()
        get_aigie()

        parent_ctx = get_parent_context()
        run_id = str(uuid4())
        span_parent_id = parent_ctx.id if parent_ctx else (trace_ctx.id if trace_ctx else None)
        run_ctx = RunContext(
            id=run_id,
            name=f"anthropic.messages.create [{model}]",
            type="span",
            span_type="llm",
            parent_id=span_parent_id,
            metadata={
                "provider": "anthropic",
                "model": model,
                "framework": "claude_agent_sdk",
            },
            tags=["anthropic", "llm", model],
            start_time=datetime.now(timezone.utc),
        )

        if system:
            run_ctx.metadata["system_prompt"] = system if isinstance(system, str) else str(system)

        span_input = {"messages": messages}
        span_output = None
        span_usage = None
        span_cost = None

        prev_span_ctx = get_current_span_context()
        set_current_span_context(run_ctx)

        # Autonomous retry: build a minimal InterceptionContext so the chain
        # hook receives enough context to decide on retry. Pre-call blocking is
        # not available in the sync Anthropic path (by design — use async).
        _aigie_for_retry = get_aigie()
        _intercept_ctx = None
        if (
            _aigie_for_retry
            and getattr(_aigie_for_retry, "_initialized", False)
            and getattr(getattr(_aigie_for_retry, "config", None), "autonomous", False)
            and getattr(_aigie_for_retry, "_interceptor_chain", None) is not None
        ):
            try:
                from .interceptor.protocols import InterceptionContext as _IC

                _intercept_ctx = _IC(
                    provider="anthropic",
                    model=kwargs.get("model", "unknown"),
                    messages=list(kwargs.get("messages", [])),
                )
            except Exception:
                _intercept_ctx = None

        from .autonomous.inline_call import call_sync_with_autonomous

        try:
            response = call_sync_with_autonomous(
                lambda: func(*args, **kwargs), _intercept_ctx, _aigie_for_retry
            )

            if hasattr(response, "content") and response.content:
                content_blocks = response.content
                output_text = ""
                for block in content_blocks:
                    if hasattr(block, "text"):
                        output_text += block.text
                span_output = {"content": output_text}

            if hasattr(response, "usage"):
                usage = response.usage
                input_tokens = getattr(usage, "input_tokens", 0)
                output_tokens = getattr(usage, "output_tokens", 0)
                span_usage = {
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                }

                try:
                    cost_info = extract_and_calculate_cost(response, "anthropic")
                except Exception:
                    cost_info = None
                if cost_info:
                    span_cost = {
                        "input_cost": float(cost_info.input_cost),
                        "output_cost": float(cost_info.output_cost),
                        "total_cost": float(cost_info.total_cost),
                        "currency": cost_info.currency,
                    }

            run_ctx.metadata["status"] = "success"
            return response

        except Exception as e:
            run_ctx.metadata["error"] = {
                "type": type(e).__name__,
                "message": str(e),
            }
            run_ctx.metadata["status"] = "error"
            raise

        finally:
            trace_id = trace_ctx.id if trace_ctx else run_ctx.id
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(
                    self._queue_anthropic_span(
                        run_ctx, trace_id, span_input, span_output, span_usage, span_cost
                    )
                )
            except RuntimeError:
                try:
                    asyncio.run(
                        self._queue_anthropic_span(
                            run_ctx, trace_id, span_input, span_output, span_usage, span_cost
                        )
                    )
                except Exception as e:
                    logger.debug(f"[wrapper] Failed to queue span sync: {e}")
            set_current_span_context(prev_span_ctx)

    async def _queue_anthropic_span(
        self,
        run_ctx: RunContext,
        trace_id: str,
        span_input: dict | None = None,
        span_output: dict | None = None,
        span_usage: dict | None = None,
        span_cost: dict | None = None,
    ) -> None:
        """Queue Anthropic LLM span using two-phase SPAN_CREATE + SPAN_UPDATE.

        Uses the same pattern as SpanContext: SPAN_CREATE for basic structure,
        then SPAN_UPDATE with output, tokens, cost data. This matches the
        backend's SpanCreateRequest / SpanUpdateRequest schemas.
        """
        try:
            from .client import get_aigie

            aigie = get_aigie()
            if not aigie or not aigie._buffer:
                return

            end_time = datetime.now(timezone.utc)
            prompt_tokens = span_usage.get("prompt_tokens", 0) if span_usage else 0
            completion_tokens = span_usage.get("completion_tokens", 0) if span_usage else 0
            total_tokens = span_usage.get("total_tokens", 0) if span_usage else 0
            input_cost = span_cost.get("input_cost", 0.0) if span_cost else 0.0
            output_cost = span_cost.get("output_cost", 0.0) if span_cost else 0.0
            total_cost = span_cost.get("total_cost", 0.0) if span_cost else 0.0

            # Phase 1: SPAN_CREATE - basic structure (matches SpanCreateRequest)
            create_payload = {
                "id": run_ctx.id,
                "name": run_ctx.name,
                "trace_id": trace_id,
                "parent_id": run_ctx.parent_id if run_ctx.parent_id != trace_id else None,
                "type": "llm",
                "start_time": run_ctx.start_time.isoformat()
                if run_ctx.start_time
                else end_time.isoformat(),
                "metadata": run_ctx.metadata,
                "tags": run_ctx.tags,
                "input": span_input,
                "model": run_ctx.metadata.get("model"),
                "level": "ERROR" if run_ctx.metadata.get("status") == "error" else "DEFAULT",
            }

            # SpanCreateRequest accepts usage/token_usage as nested objects
            if prompt_tokens > 0 or completion_tokens > 0:
                create_payload["usage"] = {
                    "input": prompt_tokens,
                    "output": completion_tokens,
                    "total": total_tokens,
                    "unit": "TOKENS",
                }
                create_payload["token_usage"] = {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                }
            if input_cost > 0 or output_cost > 0 or total_cost > 0:
                create_payload["cost_details"] = {
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "total_cost": total_cost,
                }

            await aigie._buffer.add(EventType.SPAN_CREATE, create_payload)

            # Phase 2: SPAN_UPDATE - output, tokens, cost as direct fields
            # (matches SpanUpdateRequest which accepts prompt_tokens etc. directly)
            update_payload = {
                "id": run_ctx.id,
                "span_id": run_ctx.id,
                "trace_id": trace_id,
                "name": run_ctx.name,
                "type": "llm",
                "start_time": run_ctx.start_time.isoformat()
                if run_ctx.start_time
                else end_time.isoformat(),
                "end_time": end_time.isoformat(),
                "input": span_input,
                "output": span_output,
                "metadata": run_ctx.metadata,
                "status": run_ctx.metadata.get("status", "success"),
                "model": run_ctx.metadata.get("model"),
            }

            # Add parent_id for merge fallback
            if run_ctx.parent_id and run_ctx.parent_id != trace_id:
                update_payload["parent_id"] = run_ctx.parent_id

            # Direct fields for SpanUpdateRequest
            if prompt_tokens > 0 or completion_tokens > 0:
                update_payload["prompt_tokens"] = prompt_tokens
                update_payload["completion_tokens"] = completion_tokens
                update_payload["total_tokens"] = total_tokens
            if input_cost > 0 or output_cost > 0 or total_cost > 0:
                update_payload["input_cost"] = input_cost
                update_payload["output_cost"] = output_cost
                update_payload["total_cost"] = total_cost

            # Also include usage nested objects (same pattern as SpanContext)
            if prompt_tokens > 0 or completion_tokens > 0 or total_cost > 0:
                update_payload["usage"] = {
                    "input": prompt_tokens,
                    "output": completion_tokens,
                    "total": total_tokens,
                    "unit": "TOKENS",
                    "input_cost": input_cost if input_cost > 0 else None,
                    "output_cost": output_cost if output_cost > 0 else None,
                    "total_cost": total_cost if total_cost > 0 else None,
                }
                update_payload["token_usage"] = {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "input_cost": input_cost if input_cost > 0 else None,
                    "output_cost": output_cost if output_cost > 0 else None,
                    "total_cost": total_cost if total_cost > 0 else None,
                }

            # Put token data in metadata too (for backend extraction)
            meta = update_payload.get("metadata", {})
            if isinstance(meta, dict) and (prompt_tokens > 0 or completion_tokens > 0):
                meta["token_usage"] = {
                    "input_tokens": prompt_tokens,
                    "output_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "unit": "TOKENS",
                }
                meta["prompt_tokens"] = prompt_tokens
                meta["completion_tokens"] = completion_tokens
                meta["total_tokens"] = total_tokens
                if total_cost > 0:
                    meta["cost"] = total_cost
                    meta["estimated_cost"] = total_cost
                    meta["input_cost"] = input_cost
                    meta["output_cost"] = output_cost
                    meta["total_cost"] = total_cost
                update_payload["metadata"] = meta

            # Calculate duration
            if run_ctx.start_time:
                duration_ns = int((end_time - run_ctx.start_time).total_seconds() * 1e9)
                update_payload["duration"] = duration_ns
                update_payload["latency_seconds"] = (end_time - run_ctx.start_time).total_seconds()
                update_payload["duration_ns"] = duration_ns

            await aigie._buffer.add(EventType.SPAN_UPDATE, update_payload)
            logger.debug(
                f"[wrapper] Queued Anthropic span: {run_ctx.name} ({run_ctx.id}) -> trace:{trace_id}"
            )

        except Exception as e:
            logger.warning(f"[wrapper] Failed to queue Anthropic span: {e}")


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

        client = wrap_anthropic(anthropic.Anthropic(api_key="..."))

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    return AnthropicWrapper(client, aigie_client)


def wrap_gemini(client: Any, aigie_client: Any | None = None) -> Any:
    """
    Wrap Google Gemini client for automatic tracing.

    Args:
        client: Gemini client instance
        aigie_client: Optional Aigie client

    Returns:
        Wrapped client with tracing

    Example:
        import google.generativeai as genai
        from aigie.wrappers import wrap_gemini

        genai.configure(api_key="...")
        model = wrap_gemini(genai.GenerativeModel('gemini-pro'))

        response = model.generate_content("Hello")
    """
    # Implementation for Gemini
    logger.warning("Gemini wrapper not yet fully implemented")
    return client


__all__ = [
    "AnthropicWrapper",
    "OpenAIWrapper",
    "wrap_anthropic",
    "wrap_gemini",
    "wrap_openai",
]
