"""ABC monkey-patch factory for the query entry point."""

from __future__ import annotations

import functools
import logging
from typing import Any

from aigie.tracing.monkey_patch_lifecycle import PatchTarget

from ..session_context import (
    clear_session_context,
    get_or_create_session_context,
    get_session_context,
)
from ._shared import (
    _extract_agent_name,
    _wrap_tools_with_remediation,
)

logger = logging.getLogger(__name__)


def query_patch_target() -> PatchTarget:  # noqa: C901, PLR0915
    """Declarative patch target for ``claude_agent_sdk.query``."""

    def get_target() -> tuple[Any, str]:
        import claude_agent_sdk

        return claude_agent_sdk, "query"

    def make_wrapper(original_query: Any) -> Any:  # noqa: C901, PLR0915
        @functools.wraps(original_query)
        async def traced_query(*, prompt: str, **kwargs):  # noqa: C901, PLR0915, PLR0912
            """Traced version of claude_agent_sdk.query()."""
            from ....client import get_aigie
            from ..config import ClaudeAgentSDKConfig
            from ..native_callback import ClaudeAgentSDKEvents

            aigie = get_aigie()
            config = ClaudeAgentSDKConfig.from_env()

            if aigie and aigie._initialized and config.enabled:
                prompt_str = prompt if isinstance(prompt, str) else "<async_input>"

                # Check if we're already in a session scope (e.g., claude_session context manager)
                existing_ctx = get_session_context()
                owns_context = existing_ctx is None

                # Model and system_prompt can arrive either as flat kwargs
                # (legacy call shape) or nested on a ClaudeAgentOptions dataclass.
                _opts = kwargs.get("options")
                model = (
                    kwargs.get("model")
                    or getattr(_opts, "model", None)
                    or "claude-sonnet-4-20250514"
                )
                system_prompt = (
                    kwargs.get("system_prompt")
                    or getattr(_opts, "system_prompt", "")
                    or ""
                )
                trace_name = _extract_agent_name(system_prompt, model, aigie)

                # Get or create session context - reuse existing trace if in a session
                session_ctx = get_or_create_session_context(trace_name=trace_name)

                handler = ClaudeAgentSDKEvents(
                    trace_name=trace_name,
                    metadata={
                        "prompt_preview": prompt_str[:100] if isinstance(prompt_str, str) else ""
                    },
                    capture_tool_results=config.capture_tool_results,
                    capture_messages=config.capture_messages,
                    session_context=session_ctx,
                )
                handler._aigie = aigie

                # Build options from kwargs/_opts
                options = {
                    "model": model,
                    "tools": kwargs.get("tools") or getattr(_opts, "tools", []) or [],
                    "system_prompt": system_prompt,
                    "max_tokens": kwargs.get("max_tokens") or getattr(_opts, "max_tokens", None),
                    "max_turns": kwargs.get("max_turns") or getattr(_opts, "max_turns", None),
                }

                # Initialize remediation engine if enabled
                if config.enable_realtime_remediation:
                    api_url = getattr(aigie, "_api_url", None) or getattr(aigie, "api_url", None)
                    api_key = getattr(aigie, "_api_key", None) or getattr(aigie, "api_key", None)
                    if api_url:
                        from ....realtime.remediation_engine import RemediationEngine

                        rem_engine = RemediationEngine(
                            api_url=api_url,
                            api_key=api_key or "",
                            query_timeout=config.remediation_query_timeout,
                        )
                        handler._remediation_engine = rem_engine
                        # Grab gateway intervention dispatcher if available
                        _dispatcher = getattr(aigie, "_intervention_dispatcher", None)
                        # Wrap tools for autonomous error guidance injection
                        original_tools = kwargs.get("tools", [])
                        if original_tools and config.remediation_mode == "autonomous":
                            kwargs["tools"] = _wrap_tools_with_remediation(
                                original_tools,
                                rem_engine,
                                config,
                                handler,
                                dispatcher=_dispatcher,
                            )

                # Subscribe to gateway push interventions for this trace
                _query_dispatcher = getattr(aigie, "_intervention_dispatcher", None)
                if _query_dispatcher and handler.trace_id:
                    _query_dispatcher.subscribe_trace(handler.trace_id)

                query_id = await handler.handle_query_start(prompt, options, model)

                # Collect messages from the generator
                messages = []
                result_message = None
                error_msg = None
                response_index = 0

                try:
                    async for message in original_query(prompt=prompt, **kwargs):
                        messages.append(message)

                        # Get message type name for detection
                        msg_type = type(message).__name__

                        if msg_type == "SystemMessage":
                            await handler.maybe_capture_sdk_session_id(message)

                        # Span every AssistantMessage that produced model output —
                        # either text or tool-call/thinking blocks. Tool-only
                        # rounds still consume tokens and we don't want them to
                        # vanish from per-LLM-call accounting.
                        if msg_type == "AssistantMessage" and hasattr(message, "content"):
                            content = message.content
                            has_content = (
                                bool(content) if not isinstance(content, list) else len(content) > 0
                            )
                            has_usage = getattr(message, "usage", None) is not None
                            if has_content or has_usage:
                                await handler.handle_llm_response(message, model, response_index)
                                response_index += 1

                        # Track tool usage from content blocks
                        # Note: ToolUseBlock/ToolResultBlock don't have .type, check class name
                        if hasattr(message, "content") and isinstance(message.content, list):
                            # IMPORTANT: For parallel subagent spawning, we need to process all
                            # Task tools with the SAME parent. Collect them first, then process.
                            task_tools = []
                            other_tool_uses = []
                            tool_results = []

                            for block in message.content:
                                block_class = type(block).__name__
                                logger.debug(f"[AIGIE] Block detected: {block_class}")

                                if block_class == "ToolUseBlock":
                                    tool_name = getattr(block, "name", "unknown")
                                    tool_input = getattr(block, "input", {}) or {}
                                    is_subagent_call = (
                                        tool_name in ("Task", "Agent")
                                        or (isinstance(tool_input, dict)
                                            and "subagent_type" in tool_input)
                                    )
                                    if is_subagent_call:
                                        task_tools.append(block)
                                    else:
                                        other_tool_uses.append(block)
                                elif block_class == "ToolResultBlock":
                                    tool_results.append(block)

                            # Track parent context from AssistantMessage (for subagent hierarchy)
                            # CRITICAL: If this message is from a subagent, switch context FIRST
                            # so that any nested subagents spawned here get the correct parent
                            parent_tool_use_id = getattr(message, "parent_tool_use_id", None)
                            if parent_tool_use_id:
                                logger.debug(
                                    f"[AIGIE] Message has parent_tool_use_id: {parent_tool_use_id}"
                                )
                                handler.set_parent_context(parent_tool_use_id)

                            # NOW get batch_parent (which will be correct subagent span if inside one)
                            # All parallel subagents in this message should have this same parent
                            batch_parent = handler._get_current_parent()
                            logger.debug(
                                f"[AIGIE] Batch parent for {len(task_tools)} Task tools: {batch_parent}"
                            )

                            # Process all Task tools (subagents) with the same parent
                            # If there are multiple Task tools in one message, they're parallel
                            is_parallel = len(task_tools) > 1
                            for block in task_tools:
                                tool_use_id = getattr(block, "id", str(len(handler.subagent_map)))
                                tool_input = getattr(block, "input", {})
                                subagent_type = tool_input.get("subagent_type", "unknown")
                                description = tool_input.get("description", "")
                                subagent_prompt = tool_input.get("prompt", "")
                                logger.debug(
                                    f"[AIGIE] Creating subagent span: {subagent_type} ({tool_use_id}), parent={batch_parent}, is_parallel={is_parallel}"
                                )

                                # Pass batch_parent explicitly to ensure all parallel subagents
                                # have the same parent, bypassing any state changes
                                await handler.handle_subagent_spawn(
                                    tool_use_id,
                                    subagent_type,
                                    description,
                                    subagent_prompt,
                                    override_parent_id=batch_parent,
                                    is_parallel=is_parallel,
                                )

                            # Process other tool uses
                            for block in other_tool_uses:
                                tool_use_id = getattr(block, "id", str(len(handler.tool_map)))
                                tool_name = getattr(block, "name", "unknown")
                                tool_input = getattr(block, "input", {})
                                logger.debug(
                                    f"[AIGIE] Creating tool span: {tool_name} ({tool_use_id}), parent_tool_use_id={parent_tool_use_id}"
                                )
                                await handler.handle_tool_use_start(
                                    tool_name,
                                    tool_input,
                                    tool_use_id,
                                    parent_tool_use_id=parent_tool_use_id,
                                )

                            # Process tool results
                            for block in tool_results:
                                tool_use_id = getattr(block, "tool_use_id", "")
                                content = getattr(block, "content", "")
                                is_error = getattr(block, "is_error", False)
                                # Check both tool_map and subagent_map
                                if tool_use_id and tool_use_id in handler.tool_map:
                                    await handler.handle_tool_use_end(
                                        tool_use_id, content, is_error
                                    )
                                elif tool_use_id and tool_use_id in handler.subagent_map:
                                    await handler.handle_subagent_end(
                                        tool_use_id, content, is_error
                                    )

                        # Check for ResultMessage (final message with usage/cost)
                        if hasattr(message, "usage") or hasattr(message, "total_cost_usd"):
                            result_message = message

                        yield message

                except Exception as e:
                    error_msg = str(e)
                    raise
                finally:
                    # Complete any pending tool and subagent spans first
                    await handler.complete_pending_tool_spans()
                    await handler.complete_pending_subagent_spans()
                    # Then end the query
                    await handler.handle_query_end(query_id, messages, result_message, error_msg)
                    # Unsubscribe from gateway push interventions
                    if _query_dispatcher and handler.trace_id:
                        _query_dispatcher.unsubscribe_trace(handler.trace_id)
                    # Clear session context if this query created it
                    # This ensures each standalone query() gets its own trace
                    if owns_context:
                        clear_session_context()

            else:
                # No tracing, just yield through
                async for message in original_query(prompt=prompt, **kwargs):
                    yield message

        return traced_query

    return PatchTarget(
        name="query",
        get_target=get_target,
        make_wrapper=make_wrapper,
    )


