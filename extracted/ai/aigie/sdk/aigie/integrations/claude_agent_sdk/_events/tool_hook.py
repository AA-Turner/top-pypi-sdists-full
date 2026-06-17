"""``handle_*`` / ``complete_pending_*`` methods for tool / hook events.

Composed into ``ClaudeAgentSDKEvents``; reads/writes state owned by the
main class.
"""

# mypy: disable-error-code="attr-defined,has-type,assignment,var-annotated"

from __future__ import annotations

import contextlib
import logging
import uuid
from typing import TYPE_CHECKING, Any

from ....context_manager import merge_metadata
from ..native_callback import (
    _serialize_tool_result,
    _utc_isoformat,
    _utc_now,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

class ToolEvents:

    async def handle_tool_use_start(  # noqa: C901, PLR0915
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        tool_use_id: str,
        parent_tool_use_id: str | None = None,
    ):
        """
        Called when a tool use starts (PreToolUse hook).

        Args:
            tool_name: Name of the tool being called
            tool_input: Input arguments to the tool
            tool_use_id: Unique ID for this tool use
            parent_tool_use_id: Optional parent tool use ID from message context
                              (used to explicitly parent tools under their subagent)

        Returns:
            The span ID for this tool call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_tool_calls += 1
        span_id = str(uuid.uuid4())
        start_time = _utc_now()

        # Get parent span ID - prefer explicit parent_tool_use_id if it maps to a subagent
        if parent_tool_use_id and parent_tool_use_id in self.subagent_map:
            parent_id = self.subagent_map[parent_tool_use_id].get("spanId")
            logger.debug(
                f"[AIGIE] Tool {tool_name} using explicit parent from parent_tool_use_id: {parent_id}"
            )
        else:
            parent_id = self._get_current_parent()

        # Increment tool count on current subagent if we're inside one
        current_subagent = self._get_current_subagent()
        parent_subagent_type = None
        if current_subagent:
            current_subagent["tool_count"] = current_subagent.get("tool_count", 0) + 1
            parent_subagent_type = current_subagent.get("subagentType")

        # Calculate depth for flow view ordering
        tool_depth = self._register_span_depth(span_id, parent_id)

        self.tool_map[tool_use_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "startTimeIso": start_time.isoformat(),
            "toolName": tool_name,
            "parentSubagentType": parent_subagent_type,
            "tool_input": tool_input,  # Store for drift detection
            "depth": tool_depth,
        }

        # Serialize tool input
        input_data = {}
        if self.capture_tool_results:
            input_data = {k: str(v)[:500] for k, v in tool_input.items()} if tool_input else {}

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": tool_name,  # Clean name without prefix
            "type": "tool",
            "input": input_data,
            "status": "running",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "toolName": tool_name,
                    "toolUseId": tool_use_id,
                    "framework": "claude_agent_sdk",
                    "status": "running",
                    "parentSubagentType": parent_subagent_type,
                    "depth": tool_depth,
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
            "depth": tool_depth,  # For flow view ordering
        }

        # Add tool_category hint for component registry classification
        try:
            from ....tool_category import infer_tool_category

            category = infer_tool_category(tool_name, None)
            if category:
                span_data["metadata"]["tool_category"] = category  # type: ignore[index,call-overload]
        except ImportError as exc:
            logger.debug('tool_category lookup unavailable' + ': %s', exc)

        if aigie._buffer:
            logger.debug(
                f"[AIGIE] SPAN_CREATE: id={span_id}, name={tool_name}, parent={parent_id}, status=running"
            )
            self.open_span(payload=span_data)

        # Set process-level span ID for OTel bridge (infra calls inside this tool)
        try:
            from ....auto_instrument.span_enricher import set_active_span_id

            set_active_span_id(span_id)
        except Exception as exc:  # noqa: BLE001
            logger.debug('set_active_span_id (start) failed' + ': %s', exc)
        try:
            intercept = await aigie.intercept_before_tool(
                tool_name=tool_name,
                tool_args=tool_input or {},
                trace_id=self.trace_id,
                span_id=span_id,
            )
            if intercept.get("decision") != "allow":
                logger.info(f"[AIGIE] Pre-tool signal for {tool_name}: {intercept.get('decision')}")
        except Exception as exc:  # noqa: BLE001
            logger.debug('pre-tool intercept failed' + ': %s', exc)

        return span_id

    async def handle_tool_use_end(  # noqa: C901, PLR0912, PLR0915
        self,
        tool_use_id: str,
        result: Any,
        is_error: bool = False,
    ):
        """
        Called when a tool use completes (PostToolUse hook).

        Args:
            tool_use_id: Unique ID for this tool use
            result: Result from the tool execution
            is_error: Whether the tool execution failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        tool_data = self.tool_map.get(tool_use_id)
        if not tool_data:
            return

        end_time = _utc_now()
        duration = (end_time - tool_data["startTime"]).total_seconds()
        duration_ms = duration * 1000

        # Error detection - check tool result for errors
        detected_error = self._error_detector.detect_from_tool_result(
            tool_name=tool_data["toolName"],
            tool_use_id=tool_use_id,
            result=result,
            is_error_flag=is_error,
            duration_ms=duration_ms,
        )

        # Update is_error if we detected an error in the result
        if detected_error and not is_error:
            is_error = True
            self._detected_errors.append(detected_error)
            logger.warning(
                f"[AIGIE] Error detected in tool {tool_data['toolName']}: {detected_error.message[:100]}"
            )

        # Record for drift detection
        self._drift_detector.record_tool_use(
            tool_name=tool_data["toolName"],
            tool_input=tool_data.get("tool_input", {}),
            duration_ms=duration_ms,
            is_error=is_error,
        )

        # Determine status string
        status = "error" if is_error else "success"

        output_data = {}
        if self.capture_tool_results:
            output_data["result"] = _serialize_tool_result(result, 1000)
        output_data["is_error"] = is_error
        output_data["status"] = status

        # Add error details if detected
        error_metadata = {}
        if detected_error:
            error_metadata = {
                "error_type": detected_error.error_type.value,
                "error_severity": detected_error.severity.value,
                "error_is_transient": detected_error.is_transient,
            }

        update_data = {
            "id": tool_data["spanId"],
            "trace_id": self.trace_id,  # Required for backend merge
            "name": tool_data["toolName"],  # Clean name without prefix
            "type": "tool",  # Include type for race conditions
            "output": output_data,
            "status": status,
            "is_error": is_error,  # Top-level for backend visibility
            "start_time": tool_data.get("startTimeIso"),  # Preserve start_time
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
            "metadata": merge_metadata(
                {
                    "toolName": tool_data["toolName"],
                    "toolUseId": tool_use_id,
                    "framework": "claude_agent_sdk",
                    "status": status,
                    "duration_ms": int(duration_ms),
                    "parentSubagentType": tool_data.get("parentSubagentType"),
                    "hooks_fired": tool_data.get("hooks_fired") or [],
                    **error_metadata,
                }
            ),
        }

        if is_error:
            update_data["error"] = str(result)[:500]
            update_data["error_message"] = str(result)[:500]
            if detected_error:
                update_data["error_type"] = detected_error.error_type.value

        # Real-time remediation: detect and report (guidance injection happens
        # at the tool-wrapping level in auto_instrument.py for autonomous mode)
        if is_error and self._remediation_engine:
            error_msg = str(result)[:2000]
            try:
                rem_result = await self._remediation_engine.evaluate(
                    error_msg,
                    tool_data["toolName"],
                    tool_data["spanId"],
                    self.trace_id or "",
                )
                if rem_result:
                    rem_result.original_input = str(tool_data.get("tool_input", ""))
                    rem_result.original_output = error_msg
                    await self._report_remediation(tool_data["spanId"], rem_result)
            except Exception as exc:  # noqa: BLE001
                logger.debug('remediation lookup failed (best-effort)' + ': %s', exc)

        # Post-tool interception: report errors to backend for pattern learning
        if is_error:
            with contextlib.suppress(Exception):
                await aigie.intercept_after_tool(
                    tool_name=tool_data["toolName"],
                    result=result,
                    error=str(result)[:500] if is_error else None,
                    error_type=detected_error.error_type.value if detected_error else None,
                    trace_id=self.trace_id,
                    span_id=tool_data["spanId"],
                    duration_ms=duration_ms,
                )

        # Restore process-level span to parent for OTel bridge
        try:
            from ....auto_instrument.span_enricher import set_active_span_id

            set_active_span_id(update_data.get("parent_id"))
        except Exception as exc:  # noqa: BLE001
            logger.debug('set_active_span_id (end) failed' + ': %s', exc)

        if aigie._buffer:
            logger.debug(
                f"[AIGIE] SPAN_UPDATE: id={tool_data['spanId']}, name={tool_data['toolName']}, status={status}"
            )
            self.close_span(payload=update_data)

        del self.tool_map[tool_use_id]

    def _append_hook_entry(self, tool_use_id: str | None, entry: dict[str, Any]) -> None:
        target = None
        if tool_use_id and tool_use_id in self.tool_map:
            target = self.tool_map[tool_use_id]
        elif tool_use_id and tool_use_id in self.subagent_map:
            target = self.subagent_map[tool_use_id]
        if target is not None:
            target.setdefault("hooks_fired", []).append(entry)

    def _record_user_hook(
        self, event_name: str, tool_use_id: str | None, tool_name: str | None
    ) -> None:
        """Record a user-supplied HookCallback invocation on the matching tool span."""
        entry = {
            "hook_event_name": event_name,
            "source": "user_callback",
            "timestamp": _utc_isoformat(),
        }
        if tool_name:
            entry["tool_name"] = tool_name
        self._append_hook_entry(tool_use_id, entry)

    async def maybe_capture_sdk_session_id(self, message: Any) -> None:
        """If `message` is the SDK's init SystemMessage, capture its
        session_id onto the handler. It rides the root span's single
        finalized emit (root.id == trace_id), cross-correlating aigie traces
        with the underlying Claude Code session log."""
        if getattr(message, "subtype", None) != "init":
            return
        data = getattr(message, "data", {}) or {}
        sdk_session_id = data.get("session_id") or data.get("sessionId")
        if not sdk_session_id or sdk_session_id == self.session_id:
            return
        self.session_id = sdk_session_id

    async def handle_hook_event(self, message: Any) -> None:
        """Record a HookEventMessage emitted by the CLI (when
        ``ClaudeAgentOptions.include_hook_events`` is True)."""
        data = getattr(message, "data", {}) or {}
        entry = {
            "hook_event_name": getattr(message, "hook_event_name", "") or "",
            "subtype": getattr(message, "subtype", "") or "",
            "source": "cli_event",
            "timestamp": _utc_isoformat(),
        }
        for k in ("outcome", "exit_code"):
            v = data.get(k)
            if v is not None:
                entry[k] = v
        self._append_hook_entry(data.get("tool_use_id") or data.get("toolUseId"), entry)

    async def complete_pending_tool_spans(self) -> None:
        """
        Complete any pending tool spans that weren't explicitly closed.

        This ensures all tool spans have end_time populated even if
        the corresponding ToolResultBlock was missed.
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        end_time = _utc_now()
        pending_ids = list(self.tool_map.keys())

        for tool_use_id in pending_ids:
            tool_data = self.tool_map.get(tool_use_id)
            if not tool_data:
                continue

            duration = (end_time - tool_data["startTime"]).total_seconds()

            update_data = {
                "id": tool_data["spanId"],
                "trace_id": self.trace_id,  # Required for backend merge
                "name": tool_data["toolName"],  # Clean name without prefix
                "type": "tool",  # Include type for race conditions
                "status": "success",  # Assume success if not explicitly failed
                "start_time": tool_data.get("startTimeIso"),  # Preserve start_time
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
            }

            if aigie._buffer:
                self.close_span(payload=update_data)

            del self.tool_map[tool_use_id]

