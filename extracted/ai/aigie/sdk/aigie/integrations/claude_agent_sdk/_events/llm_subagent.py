"""``handle_*`` / ``complete_pending_*`` methods for LLM response and subagent events.

Composed into ``ClaudeAgentSDKEvents``; reads/writes state owned by the
main class.
"""

# mypy: disable-error-code="attr-defined,has-type,assignment,var-annotated"

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ....context_manager import merge_metadata
from ..native_callback import (
    _format_subagent_name,
    _parse_subagent_usage_payload,
    _sanitize_error,
    _serialize_tool_result,
    _shorten_model_name,
    _utc_now,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

class LLMSubagentEvents:

    async def handle_llm_response(  # noqa: C901, PLR0912, PLR0915
        self,
        message: Any,
        model: str | None = None,
        response_index: int = 0,
        usage: dict[str, int] | None = None,
        cost: float = 0.0,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ):
        """
        Called when an LLM response (AssistantMessage with text) is received.

        Creates a span for the reasoning/response step.

        Args:
            message: The AssistantMessage or similar message with text content
            model: The model name
            response_index: Index of this response in the conversation
            usage: Token usage for this response (optional)
            cost: Cost for this response (optional)

        Returns:
            The span ID for this LLM response
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        if start_time is None:
            start_time = _utc_now()
        if usage is None:
            msg_usage = getattr(message, "usage", None)
            if msg_usage is not None:
                if isinstance(msg_usage, dict):
                    usage = msg_usage
                else:
                    usage = {
                        "input_tokens": getattr(msg_usage, "input_tokens", 0),
                        "output_tokens": getattr(msg_usage, "output_tokens", 0),
                    }

        # Get parent span ID from hierarchy
        parent_id = self._get_current_parent()

        # Extract text content from message
        text_content = ""
        if hasattr(message, "content"):
            content = message.content
            if isinstance(content, str):
                text_content = content[:500]
            elif isinstance(content, list):
                for block in content:
                    if hasattr(block, "text"):
                        text_content = block.text[:500]
                        break
                    if hasattr(block, "type") and block.type == "text":
                        text_content = getattr(block, "text", "")[:500]
                        break

        # Get model name
        model_name = model or getattr(message, "model", None) or "claude"
        model_short = _shorten_model_name(model_name)

        # Attribute tokens to current subagent if inside one
        if usage:
            current_subagent = self._get_current_subagent()
            if current_subagent:
                current_subagent["input_tokens"] = current_subagent.get(
                    "input_tokens", 0
                ) + usage.get("input_tokens", 0)
                current_subagent["output_tokens"] = current_subagent.get(
                    "output_tokens", 0
                ) + usage.get("output_tokens", 0)
                current_subagent["cost"] = current_subagent.get("cost", 0.0) + cost

        # Calculate depth for flow view ordering
        llm_depth = self._register_span_depth(span_id, parent_id)

        if end_time is None:
            end_time = _utc_now()
        prompt_tokens = usage.get("input_tokens", 0) if usage else 0
        completion_tokens = usage.get("output_tokens", 0) if usage else 0

        # Detect errors in the LLM response BEFORE building the span so status
        # reflects content-level API errors (e.g. "API Error: 400 invalid model").
        # The SDK surfaces these as plain AssistantMessage text without raising,
        # so without this check the span would ship as success.
        detected_error = self._error_detector.detect_from_llm_response(message, model_name)
        if detected_error:
            self._detected_errors.append(detected_error)
            logger.debug(
                f"[AIGIE] LLM error detected: {detected_error.error_type.value} - {detected_error.message[:100]}"
            )

        span_status = "error" if detected_error else "success"
        sanitized_err = _sanitize_error(detected_error.message) if detected_error else None
        span_output: dict[str, Any] = {
            "text": text_content if self.capture_messages else "[redacted]",
        }
        if detected_error:
            span_output["is_error"] = True
            span_output["error_message"] = sanitized_err

        llm_input: dict[str, Any] = {"response_index": response_index}
        if self._current_user_prompt and self.capture_messages:
            llm_input["prompt"] = self._current_user_prompt[:2000]

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": "LLM Response",  # Clean name without verbose model
            "type": "llm",
            "input": llm_input,
            "output": span_output,
            "status": span_status,
            "is_error": bool(detected_error),
            "error_message": sanitized_err,
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "model": model_name,
                    "model_short": model_short,
                    "framework": "claude_agent_sdk",
                    "response_index": response_index,
                    "depth": llm_depth,
                }
            ),
            "depth": llm_depth,  # For flow view ordering
            "model": model_name,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "total_cost": cost if cost else None,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            # The LLM Response span is fully finalized at creation (start_time,
            # end_time, status, output all known) — emit it exactly once.
            # Previously open_span'd as SPAN_CREATE and dropped at transport.
            self.close_span(payload=span_data)


        # Record LLM response for drift detection (captures planning from first response)
        if text_content:
            self._drift_detector.record_llm_response(text_content, model_name)

        return span_id

    async def handle_message(
        self,
        message_type: str,
        content: Any,
        role: str = "assistant",
    ) -> None:
        """
        Called for each message in the stream.

        Args:
            message_type: Type of message (AssistantMessage, ToolUseBlock, etc.)
            content: Message content
            role: Message role (user, assistant, tool)
        """
        # This can be used for detailed message tracking if needed
        pass

    def set_parent_context(self, parent_tool_use_id: str | None) -> None:
        """
        Set the current parent context for subagent hierarchy tracking.

        This is called when processing AssistantMessage with parent_tool_use_id
        to track which subagent context we're currently in. When we receive a message
        from a subagent, we need to set that subagent's span as the current parent
        so that tools and LLM responses are properly nested.

        Args:
            parent_tool_use_id: The parent tool use ID from the message
        """
        self._current_parent_tool_use_id = parent_tool_use_id
        logger.debug(f"[AIGIE] Set parent context: {parent_tool_use_id}")

        # If this is a subagent's tool_use_id, switch context to that subagent
        if parent_tool_use_id and parent_tool_use_id in self.subagent_map:
            subagent_data = self.subagent_map[parent_tool_use_id]
            subagent_span_id = subagent_data.get("spanId")
            if subagent_span_id:
                logger.debug(f"[AIGIE] Switching to subagent context: {subagent_span_id}")
                self._set_current_parent(subagent_span_id)

    async def handle_subagent_spawn(
        self,
        tool_use_id: str,
        subagent_type: str,
        description: str,
        prompt: str,
        override_parent_id: str | None = None,
        is_parallel: bool = False,
    ) -> str:
        """
        Called when a Task tool is used to spawn a subagent.

        Creates a span for the subagent execution and sets it as the new parent
        for nested tool calls.

        Args:
            tool_use_id: The tool_use_id of the Task tool
            subagent_type: Type of subagent (e.g., 'researcher', 'report-writer')
            description: Brief description of the subagent task
            prompt: The prompt given to the subagent
            override_parent_id: Optional explicit parent ID for parallel subagent spawning
            is_parallel: If True, don't change current parent (parallel subagents)

        Returns:
            The span ID for this subagent
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = _utc_now()

        # Use override parent if provided (for parallel subagent spawning),
        # otherwise get from current context
        parent_id = override_parent_id if override_parent_id else self._get_current_parent()

        # Format the subagent name nicely
        subagent_name = _format_subagent_name(subagent_type)

        # Record for drift detection (check if this is a retry)
        is_retry = any(
            sa.get("subagentType") == subagent_type and sa.get("description") == description
            for sa in self.subagent_map.values()
        )
        self._drift_detector.record_subagent_spawn(subagent_type, description, is_retry=is_retry)

        # Calculate depth for flow view ordering
        subagent_depth = self._register_span_depth(span_id, parent_id)

        # Initialize subagent tracking with token aggregation fields
        self.subagent_map[tool_use_id] = {
            "spanId": span_id,
            "parentId": parent_id,  # Store parent for restoration
            "startTime": start_time,
            "startTimeIso": start_time.isoformat(),
            "subagentType": subagent_type,
            "description": description,
            "depth": subagent_depth,
            # Token tracking for aggregation
            "input_tokens": 0,
            "output_tokens": 0,
            "cost": 0.0,
            "tool_count": 0,
        }

        # Inherit the orchestrator's model so the platform's cost calculator
        # can price subagent token usage. Subagents run under the same model
        # as the parent session unless explicitly overridden in AgentDefinition.
        subagent_model = self.metadata.get("model") if self.metadata else None

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": subagent_name,  # Clean name like "Researcher", "Data Analyst"
            "type": "agent",
            "input": {
                "subagent_type": subagent_type,
                "description": description,
                "prompt": prompt[:2000] if self.capture_messages else "[redacted]",
            },
            "status": "running",
            "tags": [*self.tags, f"subagent:{subagent_type}"],
            "metadata": merge_metadata(
                {
                    "subagentType": subagent_type,
                    "toolUseId": tool_use_id,
                    "framework": "claude_agent_sdk",
                    "description": description,
                    "depth": subagent_depth,
                    "model": subagent_model,
                }
            ),
            "model": subagent_model,
            "depth": subagent_depth,  # For flow view ordering
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            logger.debug(
                f"[AIGIE] SPAN_CREATE: id={span_id}, name={subagent_name}, parent={parent_id}, is_parallel={is_parallel}"
            )
            self.open_span(payload=span_data)

        # NEVER change the current parent when spawning subagents.
        # The parent context should ONLY be set when we receive messages FROM the subagent
        # (via set_parent_context with parent_tool_use_id).
        # This prevents cascading when subagents are spawned in separate messages.
        #
        # Old behavior (caused cascading):
        #   if not is_parallel:
        #       self._set_current_parent(span_id)
        #
        # New behavior: Don't change parent context when spawning.
        # Context is only switched when processing messages FROM subagents.

        return span_id

    async def handle_subagent_end(  # noqa: C901, PLR0915
        self,
        tool_use_id: str,
        result: Any,
        is_error: bool = False,
    ):
        """
        Called when a subagent completes execution.

        Restores the parent hierarchy and includes aggregated token/cost data.

        Args:
            tool_use_id: The tool_use_id of the Task tool
            result: Result from the subagent execution
            is_error: Whether the subagent execution failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        subagent_data = self.subagent_map.get(tool_use_id)
        if not subagent_data:
            return

        end_time = _utc_now()
        duration = (end_time - subagent_data["startTime"]).total_seconds()
        duration_ms = duration * 1000

        # Format the subagent name nicely
        subagent_name = _format_subagent_name(subagent_data["subagentType"])
        tool_count = subagent_data.get("tool_count", 0)

        # Error detection - check subagent result for errors
        detected_error = self._error_detector.detect_from_subagent_result(
            subagent_type=subagent_data["subagentType"],
            tool_use_id=tool_use_id,
            result=result,
            is_error_flag=is_error,
            duration_ms=duration_ms,
            tool_count=tool_count,
        )

        # Update is_error if we detected an error in the result
        if detected_error and not is_error:
            is_error = True
            self._detected_errors.append(detected_error)
            logger.warning(
                f"[AIGIE] Error detected in subagent {subagent_name}: {detected_error.message[:100]}"
            )

        # Record for drift detection
        self._drift_detector.record_subagent_end(subagent_data["subagentType"], tool_count)

        output_data = {}
        if self.capture_tool_results:
            output_data["result"] = _serialize_tool_result(result, 2000)
        output_data["is_error"] = is_error
        output_data["status"] = "error" if is_error else "success"

        # Get accumulated token data
        input_tokens = subagent_data.get("input_tokens", 0)
        output_tokens = subagent_data.get("output_tokens", 0)
        total_tokens = input_tokens + output_tokens
        total_cost = subagent_data.get("cost", 0.0)

        # Parse <usage>total_tokens: X tool_uses: Y duration_ms: Z</usage>
        # from the second content block of the SDK's Task-tool result. This
        # is the only place the subagent's own token usage is reported.
        parsed = _parse_subagent_usage_payload(result)
        if parsed["total_tokens"] is not None and total_tokens == 0:
            total_tokens = parsed["total_tokens"]
        if parsed["tool_uses"] is not None and tool_count == 0:
            tool_count = parsed["tool_uses"]

        # Add error details if detected
        error_metadata = {}
        if detected_error:
            error_metadata = {
                "error_type": detected_error.error_type.value,
                "error_severity": detected_error.severity.value,
                "error_is_transient": detected_error.is_transient,
            }

        subagent_model = self.metadata.get("model") if self.metadata else None

        update_data = {
            "id": subagent_data["spanId"],
            "trace_id": self.trace_id,
            "name": subagent_name,  # Clean name like "Researcher"
            "type": "agent",
            "output": output_data,
            "status": "error" if is_error else "success",
            "is_error": is_error,  # Top-level for backend visibility
            "start_time": subagent_data.get("startTimeIso"),  # Preserve start_time
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
            # Include aggregated token/cost data
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "model": subagent_model,
            "metadata": merge_metadata(
                {
                    "subagentType": subagent_data["subagentType"],
                    "tool_count": tool_count,
                    "duration_ms": int(duration_ms),
                    "status": "error" if is_error else "success",
                    "model": subagent_model,
                    **error_metadata,
                }
            ),
        }

        if is_error:
            update_data["error"] = str(result)[:500]
            update_data["error_message"] = str(result)[:500]
            if detected_error:
                update_data["error_type"] = detected_error.error_type.value

        if aigie._buffer:
            logger.debug(
                f"[AIGIE] SPAN_UPDATE: id={subagent_data['spanId']}, {subagent_name} completed, tokens={total_tokens}, cost=${total_cost:.4f}, status={'error' if is_error else 'success'}"
            )
            self.close_span(payload=update_data)


        # Restore parent context based on stored parentId
        stored_parent = subagent_data.get("parentId")
        if stored_parent:
            self._set_current_parent(stored_parent)
        else:
            # Fallback to query/turn span
            self._set_current_parent(self._current_turn_span_id or self._current_query_span_id)

        del self.subagent_map[tool_use_id]


