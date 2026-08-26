"""Monkey-patch target for the one-shot ``query()`` path.

Patch ``InternalClient.process_query`` instead of the module-level function so
``from claude_agent_sdk import query`` callers are instrumented too.
"""

from __future__ import annotations

import functools
import logging
from typing import Any

from aigie.integrations.claude_agent_sdk._patches._shared import (
    _extract_agent_name,
    _get_batch_parent,
    _wrap_tools_with_remediation,
)
from aigie.integrations.claude_agent_sdk.session_context import (
    get_or_create_session_context,
    get_session_context,
    set_session_context,
)
from aigie.tracing.monkey_patch_lifecycle import PatchTarget

logger = logging.getLogger(__name__)


def query_patch_target() -> PatchTarget:  # noqa: C901, PLR0915
    """Declarative patch target for the ``query()`` path."""

    def get_target() -> tuple[Any, str]:
        from claude_agent_sdk._internal.client import InternalClient

        return InternalClient, "process_query"

    def make_wrapper(original_process_query: Any) -> Any:  # noqa: C901, PLR0915
        @functools.wraps(original_process_query)
        async def traced_process_query(  # noqa: C901, PLR0915, PLR0912
            self: Any, prompt: Any, options: Any = None, transport: Any = None
        ):
            """Traced ``InternalClient.process_query``."""
            from aigie.client import get_aigie
            from aigie.integrations.claude_agent_sdk.config import ClaudeAgentSDKConfig
            from aigie.integrations.claude_agent_sdk.native_callback import ClaudeAgentSDKEvents

            aigie = get_aigie()
            config = ClaudeAgentSDKConfig.from_env()

            if aigie and aigie._initialized and config.enabled:
                prompt_str = prompt if isinstance(prompt, str) else "<async_input>"

                existing_ctx = get_session_context()
                resume_id = getattr(options, "resume", None)
                owns_context = existing_ctx is None or (
                    resume_id is not None and existing_ctx.trace_id != resume_id
                )

                model = getattr(options, "model", None) or "claude-sonnet-4-20250514"
                system_prompt = getattr(options, "system_prompt", None) or ""
                trace_name = _extract_agent_name(system_prompt, model, aigie)

                session_ctx = get_or_create_session_context(
                    trace_name=trace_name, trace_id=resume_id
                )

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

                from aigie.integrations.claude_agent_sdk._events._tool_catalog import (
                    resolve_tool_defs,
                )

                # Use MCP/allowed_tools fallback when options.tools is empty.
                resolved_tools = await resolve_tool_defs(
                    options, getattr(options, "tools", []) or []
                )
                options_meta = {
                    "model": model,
                    "tools": resolved_tools,
                    "system_prompt": system_prompt,
                    "max_tokens": getattr(options, "max_tokens", None),
                    "max_turns": getattr(options, "max_turns", None),
                }

                # Initialize remediation engine if enabled
                if config.enable_realtime_remediation:
                    api_url = getattr(aigie, "_api_url", None) or getattr(aigie, "api_url", None)
                    api_key = getattr(aigie, "_api_key", None) or getattr(aigie, "api_key", None)
                    if api_url:
                        from aigie.realtime.remediation_engine import RemediationEngine

                        rem_engine = RemediationEngine(
                            api_url=api_url,
                            api_key=api_key or "",
                            query_timeout=config.remediation_query_timeout,
                        )
                        handler._remediation_engine = rem_engine
                        _dispatcher = getattr(aigie, "_intervention_dispatcher", None)
                        original_tools = getattr(options, "tools", []) or []
                        if original_tools and config.remediation_mode == "autonomous":
                            wrapped_tools = _wrap_tools_with_remediation(
                                original_tools,
                                rem_engine,
                                config,
                                handler,
                                dispatcher=_dispatcher,
                            )
                            try:
                                options.tools = wrapped_tools
                            except (AttributeError, TypeError):
                                logger.debug("could not set wrapped tools on options")

                _query_dispatcher = getattr(aigie, "_intervention_dispatcher", None)
                if _query_dispatcher and handler.trace_id:
                    _query_dispatcher.subscribe_trace(handler.trace_id)

                query_id = await handler.handle_query_start(prompt, options_meta, model)

                messages = []
                result_message = None
                error_msg = None
                response_index = 0

                try:
                    async for message in original_process_query(self, prompt, options, transport):
                        messages.append(message)

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
                                # A model round is a turn. handle_turn_start
                                # only runs on the client path, so without this
                                # the query root reports every run as a single
                                # turn. The counter is session-scoped on
                                # purpose: inside claude_session every query
                                # updates one shared root span, so that root
                                # reports the session's turns, not this call's.
                                handler.increment_turn()

                        if hasattr(message, "content") and isinstance(message.content, list):
                            task_tools = []
                            other_tool_uses = []
                            tool_results = []

                            for block in message.content:
                                block_class = type(block).__name__
                                logger.debug(f"[AIGIE] Block detected: {block_class}")

                                if block_class == "ToolUseBlock":
                                    tool_name = getattr(block, "name", "unknown")
                                    tool_input = getattr(block, "input", {}) or {}
                                    is_subagent_call = tool_name in ("Task", "Agent") or (
                                        isinstance(tool_input, dict)
                                        and "subagent_type" in tool_input
                                    )
                                    if is_subagent_call:
                                        task_tools.append(block)
                                    else:
                                        other_tool_uses.append(block)
                                elif block_class == "ToolResultBlock":
                                    tool_results.append(block)

                            parent_tool_use_id = getattr(message, "parent_tool_use_id", None)
                            if parent_tool_use_id:
                                logger.debug(
                                    f"[AIGIE] Message has parent_tool_use_id: {parent_tool_use_id}"
                                )
                                handler.set_parent_context(parent_tool_use_id)

                            batch_parent = _get_batch_parent(handler, parent_tool_use_id)
                            logger.debug(
                                f"[AIGIE] Batch parent for {len(task_tools)} Task tools: {batch_parent}"
                            )

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

                                await handler.handle_subagent_spawn(
                                    tool_use_id,
                                    subagent_type,
                                    description,
                                    subagent_prompt,
                                    override_parent_id=batch_parent,
                                    is_parallel=is_parallel,
                                )

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

                            for block in tool_results:
                                tool_use_id = getattr(block, "tool_use_id", "")
                                content = getattr(block, "content", "")
                                is_error = getattr(block, "is_error", False)
                                if tool_use_id and tool_use_id in handler.tool_map:
                                    await handler.handle_tool_use_end(
                                        tool_use_id, content, is_error
                                    )
                                elif tool_use_id and tool_use_id in handler.subagent_map:
                                    await handler.handle_subagent_end(
                                        tool_use_id, content, is_error
                                    )

                        if hasattr(message, "usage") or hasattr(message, "total_cost_usd"):
                            result_message = message

                        yield message

                except Exception as e:
                    error_msg = str(e)
                    raise
                finally:
                    await handler.complete_pending_tool_spans()
                    await handler.complete_pending_subagent_spans()
                    await handler.handle_query_end(query_id, messages, result_message, error_msg)
                    if _query_dispatcher and handler.trace_id:
                        _query_dispatcher.unsubscribe_trace(handler.trace_id)
                    if owns_context:
                        set_session_context(existing_ctx)

            else:
                async for message in original_process_query(self, prompt, options, transport):
                    yield message

        return traced_process_query

    return PatchTarget(
        name="process_query",
        get_target=get_target,
        make_wrapper=make_wrapper,
    )
