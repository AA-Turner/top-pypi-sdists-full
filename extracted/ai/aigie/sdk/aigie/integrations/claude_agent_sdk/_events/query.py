"""``handle_*`` / ``complete_pending_*`` methods for query events.

Composed into ``ClaudeAgentSDKEvents``; reads/writes state owned by the
main class.
"""

# mypy: disable-error-code="attr-defined,has-type,assignment,var-annotated"

from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING, Any

from ....context_manager import merge_metadata
from ..cost_tracking import calculate_claude_cost
from ..monitoring import DriftDetector
from ..native_callback import (
    _pick_error_message,
    _shorten_model_name,
    _utc_isoformat,
    _utc_now,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

class QueryEvents:

    async def handle_query_start(  # noqa: C901, PLR0912, PLR0915
        self,
        prompt: str,
        options: dict[str, Any],
        model: str | None = None,
    ):
        """
        Called when a query() call starts.

        Args:
            prompt: The prompt being sent
            options: Query options (tools, system_prompt, etc.)
            model: The model being used

        Returns:
            The query ID for tracking
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            logger.warning(
                "Aigie not initialized, traces will not be created. Set AIGIE_TOKEN to enable tracing."
            )
            return ""

        # Record query start time for duration tracking
        self._query_start_time = _utc_now()
        self._query_start_time_iso = self._query_start_time.isoformat()
        if isinstance(prompt, str):
            self._current_user_prompt = prompt

        # Reset error tracking for this query
        self._detected_errors = []

        # Reset drift detector for this query (new plan per query)
        self._drift_detector = DriftDetector()

        # Capture initial plan for drift detection
        system_prompt = options.get("system_prompt", "")
        if system_prompt:
            self._drift_detector.capture_system_prompt(system_prompt)
        self._drift_detector.capture_initial_prompt(prompt)

        # Generate trace ID if not set - use session context if available
        if not self.trace_id:
            if self._session_context:
                self.trace_id = self._session_context.trace_id
            elif self._trace_context and hasattr(self._trace_context, "id"):
                self.trace_id = str(self._trace_context.id)
            else:
                self.trace_id = str(uuid.uuid4())

        # Build trace name - use session context name if available
        trace_name = self.trace_name
        if not trace_name and self._session_context:
            trace_name = self._session_context.trace_name
        if not trace_name:
            # Generate descriptive name with model and prompt preview
            model_short = (model or "claude").split("-")[0].capitalize()
            if prompt:
                # Create prompt preview (30 chars, remove newlines)
                preview = prompt[:30].replace("\n", " ").strip()
                if len(prompt) > 30:
                    preview += "..."
                trace_name = f"{model_short}: {preview}"
            else:
                trace_name = f"{model_short} Agent"

        # Extract tool names and schemas if present
        tools = options.get("tools", [])
        tool_names = []
        tool_definitions = []
        if tools:
            for t in tools[:10]:
                if hasattr(t, "name"):
                    tool_names.append(t.name)
                    # Capture tool schema for Tool Usage Judge
                    tool_def = {"name": t.name}
                    if hasattr(t, "description"):
                        tool_def["description"] = t.description
                    if hasattr(t, "input_schema"):
                        tool_def["input_schema"] = t.input_schema
                    elif hasattr(t, "parameters"):
                        tool_def["parameters"] = t.parameters
                    tool_definitions.append(tool_def)
                elif isinstance(t, dict) and "name" in t:
                    tool_names.append(t["name"])
                    tool_definitions.append(t)

        # Extract model parameters
        model_parameters = {}
        for param_key in (
            "temperature",
            "top_p",
            "top_k",
            "max_tokens",
            "stop_sequences",
        ):
            val = options.get(param_key)
            if val is not None:
                model_parameters[param_key] = val

        resolved_model = model or options.get("model") or "claude-sonnet-4-20250514"
        # Cache resolved model so downstream events (handle_query_end,
        # LLM spans) don't independently fall back to the Sonnet default.
        self.metadata["model"] = resolved_model

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "model": resolved_model,
                "tool_count": len(tools),
                "tool_names": tool_names[:10],
                "framework": "claude_agent_sdk",
                "max_tokens": options.get("max_tokens"),
                "max_turns": options.get("max_turns"),
            }
        )

        if model_parameters:
            trace_metadata["model_parameters"] = model_parameters
        if tool_definitions:
            trace_metadata["available_tools"] = tool_definitions

        # Capture full system prompt in metadata
        system_prompt = options.get("system_prompt", "")
        if system_prompt and self.capture_messages:
            trace_metadata["system_prompt"] = system_prompt

        # Only create trace if we don't have a trace context AND haven't created one yet
        should_create_trace = not self._trace_context
        if self._session_context and self._session_context.trace_created:
            should_create_trace = False

        if should_create_trace:
            trace_data = {
                "id": self.trace_id,
                "name": trace_name,
                "type": "agent",
                "input": {
                    "prompt": prompt[:2000] if self.capture_messages else "[redacted]",
                    "model": trace_metadata["model"],
                    "tool_count": len(tools),
                },
                "status": "pending",
                "tags": [*self.tags, "claude_agent_sdk"],
                "metadata": merge_metadata(trace_metadata),
                "start_time": _utc_isoformat(),
                "created_at": _utc_isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            # Send trace via buffer
            if aigie._buffer:
                logger.debug(f"[AIGIE] TRACE_CREATE: id={self.trace_id}, name={trace_name}")
                self.open_trace(payload=trace_data)

            # Set process-level trace ID for OTel bridge
            try:
                from ....auto_instrument.span_enricher import set_active_trace_id

                set_active_trace_id(self.trace_id)
            except Exception as exc:  # noqa: BLE001
                logger.debug('set_active_trace_id failed' + ': %s', exc)
            if self._session_context:
                self._session_context.mark_trace_created()

        # Create query span with clean naming
        self.query_span_id = str(uuid.uuid4())
        model_short = _shorten_model_name(trace_metadata["model"])

        # Register query span depth (root level = 0)
        query_depth = self._register_span_depth(self.query_span_id, None)

        query_start_iso = self._query_start_time_iso
        query_span_data = {
            "id": self.query_span_id,
            "trace_id": self.trace_id,
            "name": f"Query ({model_short})",
            "type": "llm",
            "input": {
                "prompt": prompt[:2000] if self.capture_messages else "[redacted]",
                "model": trace_metadata["model"],
                "tools": tool_names,
                "system_prompt": options.get("system_prompt", "")
                if self.capture_messages
                else None,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata({**trace_metadata, "depth": query_depth}),
            "model": trace_metadata["model"],
            "start_time": query_start_iso,
            "created_at": query_start_iso,
            "depth": query_depth,  # For flow view ordering
        }
        # Store start_time_iso for inclusion in SPAN_UPDATE
        self._query_span_start_iso = query_start_iso

        self._current_query_span_id = self.query_span_id

        # Set query span as current parent in session context for child span nesting
        if self._session_context:
            self._session_context.current_query_span_id = self.query_span_id
            self._session_context.set_current_parent(self.query_span_id)

        if aigie._buffer:
            logger.debug(
                f"[AIGIE] SPAN_CREATE: id={self.query_span_id}, name=Query ({model_short}), parent=None (trace root)"
            )
            self.open_span(payload=query_span_data)

        return self.query_span_id

    async def handle_query_end(  # noqa: C901, PLR0912, PLR0915
        self,
        query_id: str,
        messages: list[Any],
        result_message: Any,
        error: str | None = None,
    ):
        """
        Called when a query() call completes.

        Args:
            query_id: Query ID from handle_query_start
            messages: List of messages from the conversation
            result_message: The ResultMessage with final output and costs
            error: Error message if query failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        end_time = _utc_now()
        success = error is None

        # Inspect the ResultMessage for content-level API errors. The SDK does
        # not raise on errors returned in message content (e.g. "API Error: 400
        # invalid model"), so without this the query/trace ship as success.
        result_error_message: str | None = None
        if result_message is not None:
            rm_subtype = getattr(result_message, "subtype", None)
            rm_is_error = bool(getattr(result_message, "is_error", None))
            rm_result_text = ""
            for attr in ("result", "error", "message"):
                val = getattr(result_message, attr, None)
                if val:
                    rm_result_text = str(val)
                    break
            subtype_signals_error = isinstance(rm_subtype, str) and "error" in rm_subtype.lower()
            text_signals_error = bool(
                rm_result_text
                and self._error_detector.detect_from_text(rm_result_text, source="result_message")
            )
            if rm_is_error or subtype_signals_error or text_signals_error:
                success = False
                result_error_message = rm_result_text or f"ResultMessage subtype={rm_subtype}"

        # Extract usage and cost from ResultMessage
        usage = {}
        cost = 0.0
        model = None

        if result_message:
            if hasattr(result_message, "usage"):
                usage_obj = result_message.usage
                # Handle both dict and object formats
                if isinstance(usage_obj, dict):
                    usage = {
                        "input_tokens": usage_obj.get("input_tokens", 0),
                        "output_tokens": usage_obj.get("output_tokens", 0),
                        "cache_read_input_tokens": usage_obj.get("cache_read_input_tokens", 0),
                        "cache_creation_input_tokens": usage_obj.get(
                            "cache_creation_input_tokens", 0
                        ),
                    }
                else:
                    usage = {
                        "input_tokens": getattr(usage_obj, "input_tokens", 0),
                        "output_tokens": getattr(usage_obj, "output_tokens", 0),
                        "cache_read_input_tokens": getattr(usage_obj, "cache_read_input_tokens", 0),
                        "cache_creation_input_tokens": getattr(
                            usage_obj, "cache_creation_input_tokens", 0
                        ),
                    }
                # Extract reasoning/thinking tokens if available
                if isinstance(usage_obj, dict):
                    usage["reasoning_tokens"] = usage_obj.get("reasoning_tokens", 0) or 0
                else:
                    usage["reasoning_tokens"] = getattr(usage_obj, "reasoning_tokens", 0) or 0

                # Update totals - skip if already accumulated from stream
                if not self._tokens_accumulated_from_stream:
                    self.total_input_tokens += usage.get("input_tokens", 0)
                    self.total_output_tokens += usage.get("output_tokens", 0)
                self.total_cache_read_tokens += usage.get("cache_read_input_tokens", 0)
                self.total_cache_creation_tokens += usage.get("cache_creation_input_tokens", 0)

            if hasattr(result_message, "total_cost_usd"):
                cost = result_message.total_cost_usd or 0.0
            elif hasattr(result_message, "model"):
                # Calculate cost from usage
                model = result_message.model
                cost = calculate_claude_cost(model, usage)

            self.total_cost += cost

            if hasattr(result_message, "model"):
                model = result_message.model

        # Extract final output, finish_reason, and thinking blocks
        output = None
        finish_reason = None
        thinking_content = None
        if messages and self.capture_messages:
            last_message = messages[-1] if messages else None
            if last_message:
                # Extract finish_reason / stop_reason from the result message
                if hasattr(last_message, "stop_reason"):
                    finish_reason = last_message.stop_reason
                elif hasattr(last_message, "finish_reason"):
                    finish_reason = last_message.finish_reason

                if hasattr(last_message, "content"):
                    content = last_message.content
                    if isinstance(content, str):
                        output = content[:2000]
                    elif isinstance(content, list):
                        # Extract text blocks and thinking blocks
                        text_parts = []
                        thinking_parts = []
                        for block in content:
                            # Check for thinking/extended thinking blocks
                            block_type = getattr(block, "type", None) or (
                                block.get("type") if isinstance(block, dict) else None
                            )
                            if block_type == "thinking":
                                thinking_text = getattr(block, "thinking", None) or (
                                    block.get("thinking") if isinstance(block, dict) else None
                                )
                                if thinking_text:
                                    thinking_parts.append(thinking_text)
                            elif hasattr(block, "text"):
                                text_parts.append(block.text)
                            elif isinstance(block, dict) and "text" in block:
                                text_parts.append(block["text"])
                        output = "\n".join(text_parts)[:2000]
                        if thinking_parts:
                            thinking_content = "\n---\n".join(thinking_parts)

        # Also try to extract finish_reason from result_message directly
        if not finish_reason and result_message:
            if hasattr(result_message, "stop_reason"):
                finish_reason = result_message.stop_reason
            elif hasattr(result_message, "finish_reason"):
                finish_reason = result_message.finish_reason

        # ResultMessage (the typical last message for query()) carries the
        # final assistant text on `.result`, not in a content block. Fall
        # back to it so the Query span's output isn't null when the only
        # source of text was the terminal ResultMessage.
        if not output and result_message is not None and self.capture_messages:
            rm_text = getattr(result_message, "result", None)
            if isinstance(rm_text, str) and rm_text:
                output = rm_text[:2000]

        # Update query span
        if self.query_span_id:
            # Get model name for span name
            model_name = (
                model
                or (self.metadata.get("model") if self.metadata else None)
                or "claude-sonnet-4-20250514"
            )
            model_short = _shorten_model_name(model_name)

            # Get token values - prefer local usage, fallback to accumulated totals
            span_input_tokens = usage.get("input_tokens") or self.total_input_tokens
            span_output_tokens = usage.get("output_tokens") or self.total_output_tokens
            span_total_tokens = span_input_tokens + span_output_tokens
            span_cost = cost if cost > 0 else self.total_cost

            query_output = {
                "response": output,
                "message_count": len(messages),
                "usage": {
                    "input_tokens": span_input_tokens,
                    "output_tokens": span_output_tokens,
                    "total_tokens": span_total_tokens,
                },
                "cost": span_cost,
            }
            if finish_reason:
                query_output["finish_reason"] = finish_reason

            query_metadata = {}
            if finish_reason:
                query_metadata["finish_reason"] = finish_reason
            if thinking_content:
                query_metadata["thinking"] = thinking_content
            if usage.get("reasoning_tokens"):
                query_metadata["reasoning_tokens"] = usage["reasoning_tokens"]

            if success and self._detected_errors:
                success = False

            query_update = {
                "id": self.query_span_id,
                "trace_id": self.trace_id,  # Required for backend merge
                "name": f"Query ({model_short})",  # Clean name without verbose model
                "type": "llm",  # Include type to handle race conditions
                "status": "success" if success else "failed",
                "is_error": not success,
                "output": query_output,
                "start_time": getattr(self, "_query_span_start_iso", None),  # Preserve start_time
                "end_time": end_time.isoformat(),
                "model": model_name,
                "prompt_tokens": span_input_tokens,
                "completion_tokens": span_output_tokens,
                "total_tokens": span_total_tokens,
                "total_cost": span_cost,
            }

            if query_metadata:
                query_update["metadata"] = query_metadata

            query_error_msg = _pick_error_message(
                error, result_error_message, self._detected_errors if not success else []
            )
            if query_error_msg:
                query_update["error"] = query_error_msg
                query_update["error_message"] = query_error_msg

            if aigie._buffer:
                logger.debug(
                    f"[AIGIE] SPAN_UPDATE: id={query_update['id']}, tokens={query_update.get('total_tokens')}, status={query_update.get('status')}"
                )
                self.close_span(payload=query_update)

        # Update trace with top-level token fields for backend aggregation
        update_data = {
            "id": self.trace_id,
            "name": self.trace_name,  # Include name so auto-created traces get proper name
            "status": "success" if success else "failed",
            "output": {
                "response": output,
                "message_count": len(messages),
                "total_tokens": self.total_input_tokens + self.total_output_tokens,
                "total_cost": self.total_cost,
                "tool_calls": self.total_tool_calls,
            },
            "end_time": end_time.isoformat(),
            # Top-level token/cost fields for backend aggregation display
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "prompt_tokens": self.total_input_tokens,
            "completion_tokens": self.total_output_tokens,
            "total_cost": self.total_cost,
            "turn_count": self._session_context.total_turns if self._session_context else 1,
        }

        trace_error_msg = _pick_error_message(
            error, result_error_message, self._detected_errors if not success else []
        )
        if trace_error_msg:
            update_data["error"] = trace_error_msg
            update_data["error_message"] = trace_error_msg

        # Finalize drift detection and get all detected drifts
        start_time = self._query_start_time or _utc_now()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        total_tokens = self.total_input_tokens + self.total_output_tokens

        detected_drifts = self._drift_detector.finalize(
            total_duration_ms=duration_ms,
            total_tokens=total_tokens,
            total_cost=self.total_cost,
            final_output=output,
        )

        # Add monitoring data to trace output
        monitoring_data = {
            "drift_detection": {
                "plan": self._drift_detector.plan.to_dict() if self._drift_detector.plan else None,
                "execution": self._drift_detector.execution.to_dict()
                if self._drift_detector.execution
                else None,
                "detected_drifts": [d.to_dict() for d in detected_drifts],
                "drift_count": len(detected_drifts),
            },
            "error_detection": {
                "stats": self._error_detector.stats.to_dict(),
                "detected_errors": [e.to_dict() for e in self._detected_errors],
                "error_count": len(self._detected_errors),
            },
        }

        # Add monitoring to trace metadata
        if "metadata" not in update_data:
            update_data["metadata"] = {}
        update_data["metadata"]["monitoring"] = monitoring_data  # type: ignore[index,assignment]

        # Also add summary to output for visibility
        update_data["output"]["monitoring"] = {  # type: ignore[index,assignment]
            "drift_count": len(detected_drifts),
            "error_count": len(self._detected_errors),
            "retries": self._drift_detector.execution.retry_count
            if self._drift_detector.execution
            else 0,
            "plan_captured": self._drift_detector._plan_captured,
        }

        # Log monitoring summary
        if detected_drifts:
            logger.info(f"[AIGIE] Drift detection summary: {len(detected_drifts)} drifts detected")
            for drift in detected_drifts[:3]:  # Log first 3
                logger.info(f"[AIGIE]   - {drift.drift_type.value}: {drift.description[:80]}")
        if self._detected_errors:
            logger.info(
                f"[AIGIE] Error detection summary: {len(self._detected_errors)} errors detected"
            )
            for err in self._detected_errors[:3]:  # Log first 3
                logger.info(f"[AIGIE]   - {err.error_type.value}: {err.message[:80]}")

        if aigie._buffer:
            # Debug: Log trace update data
            logger.debug(
                f"[AIGIE] TRACE_UPDATE: id={self.trace_id}, total_tokens={update_data['total_tokens']}, cost={update_data['total_cost']}"
            )
            self.close_trace(payload=update_data)

        # Complete any pending spans to ensure all have end_time
        await self.complete_pending_turn_spans()
        await self.complete_pending_tool_spans()
        await self.complete_pending_subagent_spans()

        # Clear query span from session context since query is done
        self._current_query_span_id = None
        if self._session_context:
            self._session_context.current_query_span_id = None
            self._session_context.set_current_parent(None)

