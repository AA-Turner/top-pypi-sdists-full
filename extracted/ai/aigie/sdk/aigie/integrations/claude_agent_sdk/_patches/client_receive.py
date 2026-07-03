"""ABC monkey-patch factory for the client receive entry point."""

from __future__ import annotations

import functools
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from aigie.integrations.claude_agent_sdk._patches._shared import _get_batch_parent
from aigie.tracing.monkey_patch_lifecycle import PatchTarget

logger = logging.getLogger(__name__)


def client_receive_patch_target() -> PatchTarget:  # noqa: C901, PLR0915
    """Declarative patch target for ``ClaudeSDKClient.receive_response``."""

    def get_target() -> tuple[Any, str]:
        from claude_agent_sdk import ClaudeSDKClient

        if not hasattr(ClaudeSDKClient, "receive_response"):
            raise ImportError("ClaudeSDKClient.receive_response not available in this SDK version")
        return ClaudeSDKClient, "receive_response"

    def make_wrapper(original_receive: Any) -> Any:  # noqa: C901, PLR0915
        @functools.wraps(original_receive)
        async def traced_receive_response(self):  # noqa: C901, PLR0915, PLR0912
            """Traced version of ClaudeSDKClient.receive_response()."""

            handler = getattr(self, "_aigie_handler", None)
            pending_turn_ids = getattr(self, "_pending_turn_ids", [])

            # Collect all messages
            messages = []
            result_message = None
            error_msg = None
            response_index = 0
            last_event_time = datetime.now(timezone.utc)

            try:
                async for message in original_receive(self):
                    arrival_time = datetime.now(timezone.utc)
                    messages.append(message)

                    # Get message type name for detection
                    msg_type = type(message).__name__

                    if handler:
                        if msg_type == "SystemMessage":
                            await handler.maybe_capture_sdk_session_id(message)

                        # Record SDK-emitted hook lifecycle events when
                        # ClaudeAgentOptions.include_hook_events is True.
                        if msg_type == "HookEventMessage":
                            await handler.handle_hook_event(message)

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
                                # Get model from client options, then client attribute, then default
                                _client_options = getattr(self, "options", None)
                                model = getattr(_client_options, "model", None) or getattr(
                                    self, "model", "claude-sonnet-4-20250514"
                                )
                                await handler.handle_llm_response(
                                    message,
                                    model,
                                    response_index,
                                    start_time=last_event_time,
                                    end_time=arrival_time,
                                )
                                response_index += 1

                        # Track tool usage and subagent spawning from content blocks
                        if hasattr(message, "content") and isinstance(message.content, list):
                            # IMPORTANT: For parallel subagent spawning, we need to process all
                            # Task tools with the SAME parent. Collect them first, then process.
                            task_tools = []
                            other_tool_uses = []
                            tool_results = []

                            for block in message.content:
                                block_class = type(block).__name__
                                logger.debug(f"[AIGIE] Block detected (client): {block_class}")

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

                            # Track parent context from AssistantMessage (for subagent hierarchy)
                            # CRITICAL: If this message is from a subagent, switch context FIRST
                            # so that any nested subagents spawned here get the correct parent
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
                                    f"[AIGIE] Creating subagent span (client): {subagent_type} ({tool_use_id}), parent={batch_parent}, is_parallel={is_parallel}"
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
                                    f"[AIGIE] Creating tool span (client): {tool_name} ({tool_use_id}), parent_tool_use_id={parent_tool_use_id}"
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

                    # Accumulate per-turn token usage from result messages
                    if hasattr(message, "usage") and handler:
                        usage = message.usage
                        if isinstance(usage, dict):
                            input_t = usage.get("input_tokens", 0)
                            output_t = usage.get("output_tokens", 0)
                        else:
                            input_t = getattr(usage, "input_tokens", 0)
                            output_t = getattr(usage, "output_tokens", 0)
                        handler.total_input_tokens += input_t
                        handler.total_output_tokens += output_t
                        handler._tokens_accumulated_from_stream = True

                    # Detect new turn: stop_reason == 'tool_use' means another turn is starting
                    if (
                        handler
                        and hasattr(message, "stop_reason")
                        and message.stop_reason == "tool_use"
                    ):
                        turn_id = str(uuid.uuid4())
                        await handler.handle_turn_start(turn_id, "[tool_use continuation]")
                        if not hasattr(self, "_pending_turn_ids"):
                            self._pending_turn_ids = []
                        self._pending_turn_ids.append(turn_id)
                        pending_turn_ids = self._pending_turn_ids

                    # Check for ResultMessage (final message with usage/cost)
                    if hasattr(message, "usage") or hasattr(message, "total_cost_usd"):
                        result_message = message

                    last_event_time = datetime.now(timezone.utc)
                    yield message

            except Exception as e:
                error_msg = str(e)
                raise
            finally:
                # Complete any pending tool and subagent spans first
                if handler:
                    await handler.complete_pending_tool_spans()
                    await handler.complete_pending_subagent_spans()

                # Complete ALL pending turns, not just the first
                if handler and pending_turn_ids:
                    # Process all pending turns
                    while pending_turn_ids:
                        turn_id = pending_turn_ids.pop(0)

                        # Extract output and usage from messages
                        output = None
                        usage = {}
                        cost = 0.0

                        if result_message:
                            if hasattr(result_message, "usage"):
                                u = result_message.usage
                                # Handle both dict and object formats
                                if isinstance(u, dict):
                                    usage = {
                                        "input_tokens": u.get("input_tokens", 0),
                                        "output_tokens": u.get("output_tokens", 0),
                                    }
                                else:
                                    usage = {
                                        "input_tokens": getattr(u, "input_tokens", 0),
                                        "output_tokens": getattr(u, "output_tokens", 0),
                                    }
                            if hasattr(result_message, "total_cost_usd"):
                                cost = result_message.total_cost_usd or 0.0

                        # Extract text output from messages
                        for msg in messages:
                            if hasattr(msg, "content"):
                                content = msg.content
                                if isinstance(content, list):
                                    for block in content:
                                        if hasattr(block, "text"):
                                            output = block.text[:2000]
                                            break

                        await handler.handle_turn_end(
                            turn_id, output=output, usage=usage, cost=cost, error=error_msg
                        )

        return traced_receive_response

    return PatchTarget(
        name="ClaudeSDKClient.receive_response",
        get_target=get_target,
        make_wrapper=make_wrapper,
    )
