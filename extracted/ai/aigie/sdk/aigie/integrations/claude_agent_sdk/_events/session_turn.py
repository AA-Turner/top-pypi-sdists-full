"""``handle_*`` / ``complete_pending_*`` methods for session and turn events.

Composed into ``ClaudeAgentSDKEvents``; reads/writes state owned by the
main class.
"""

# mypy: disable-error-code="attr-defined,has-type,assignment,var-annotated"

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from aigie.context_manager import merge_metadata
from aigie.integrations.claude_agent_sdk.native_callback import (
    _format_subagent_name,
    _sanitize_error,
    _utc_isoformat,
    _utc_now,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class SessionTurnEvents:
    async def complete_pending_subagent_spans(self):
        """Force-close any subagent spans whose ToolResultBlock was missed.

        Ensures every open subagent span gets an end_time and its parent
        pointer is restored from the span stack.
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        end_time = _utc_now()
        for tool_use_id in list(self.subagent_map.keys()):
            subagent_data = self.subagent_map.get(tool_use_id)
            if not subagent_data:
                continue
            self._close_pending_subagent(aigie, tool_use_id, subagent_data, end_time)

    def _close_pending_subagent(
        self,
        aigie: Any,
        tool_use_id: str,
        subagent_data: dict[str, Any],
        end_time: datetime,
    ) -> None:
        update_data = self._build_subagent_completion_payload(subagent_data, end_time)
        if aigie._buffer:
            logger.debug("[AIGIE] Completing pending subagent span: %s", update_data["name"])
            self.close_span(payload=update_data)
        self._pop_subagent_parent()
        del self.subagent_map[tool_use_id]

    def _build_subagent_completion_payload(
        self, subagent_data: dict[str, Any], end_time: datetime
    ) -> dict[str, Any]:
        duration = (end_time - subagent_data["startTime"]).total_seconds()
        input_tokens = subagent_data.get("input_tokens", 0)
        output_tokens = subagent_data.get("output_tokens", 0)
        return {
            "id": subagent_data["spanId"],
            "trace_id": self.trace_id,
            "name": _format_subagent_name(subagent_data["subagentType"]),
            "type": "agent",
            "status": "success",  # Assume success if not explicitly failed
            "start_time": subagent_data.get("startTimeIso"),
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "total_cost": subagent_data.get("cost", 0.0),
            "metadata": merge_metadata(
                {
                    "subagentType": subagent_data["subagentType"],
                    "tool_count": subagent_data.get("tool_count", 0),
                }
            ),
        }

    def _pop_subagent_parent(self) -> None:
        """Pop the current subagent off the parent stack and restore the
        previous parent (or fall back to turn/query)."""
        if not self._parent_span_stack:
            return
        self._parent_span_stack.pop()
        if self._parent_span_stack:
            self._set_current_parent(self._parent_span_stack[-1])
        else:
            self._set_current_parent(self._current_turn_span_id or self._current_query_span_id)

    async def complete_pending_turn_spans(self) -> None:
        """
        Complete any pending turn spans that weren't explicitly closed.

        This ensures all turn (chain) spans have end_time populated even if
        the turn wasn't properly ended via handle_turn_end.
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        end_time = _utc_now()
        pending_ids = list(self.turn_map.keys())

        for turn_id in pending_ids:
            turn_data = self.turn_map.get(turn_id)
            if not turn_data:
                continue

            duration = (end_time - turn_data["startTime"]).total_seconds()

            update_data = {
                "id": turn_data["spanId"],
                "trace_id": self.trace_id,
                "name": f"Turn {turn_data['turnNumber']}",
                "type": "chain",
                "status": "success",  # Assume success if not explicitly failed
                "start_time": turn_data.get("startTimeIso"),  # Preserve start_time
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
            }

            if aigie._buffer:
                logger.debug(
                    f"[AIGIE] Completing pending turn span: Turn {turn_data['turnNumber']}"
                )
                self.close_span(payload=update_data)

            del self.turn_map[turn_id]

        self._current_turn_span_id = None

    async def handle_session_start(  # noqa: PLR0915
        self,
        client: Any,
        options: dict[str, Any],
    ):
        """
        Called when a ClaudeSDKClient session starts.

        Args:
            client: The ClaudeSDKClient instance
            options: Session options

        Returns:
            The session ID for tracking
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return ""

        # Generate trace ID if not set
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())

        # Build descriptive trace name
        model = options.get("model", "claude-sonnet-4-20250514")
        model_short = model.split("-")[0].capitalize() if model else "Claude"
        trace_name = self.trace_name or f"{model_short} Session"
        self._root_name = trace_name

        # Cache so subagent / LLM spans can pick it up from one place.
        self.metadata["model"] = model

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "framework": "claude_agent_sdk",
                "session_type": "stateful",
                "model": model,
            }
        )

        # Capture system prompt for drift detection
        system_prompt = options.get("system_prompt", "")
        if system_prompt:
            self._drift_detector.capture_system_prompt(system_prompt)

        # The session span IS the trace root (root.id == trace_id, parent None,
        # carries the trace name/input/metadata/tags). No separate trace event
        # is emitted — trace identity rides this span.
        self.session_span_id = self.trace_id
        session_start_iso = _utc_isoformat()
        self._session_start_iso = session_start_iso
        session_span_data = {
            "id": self.session_span_id,
            "trace_id": self.trace_id,
            "parent_id": None,
            "name": trace_name,
            "type": "agent",
            "input": {
                "session_type": "stateful",
                "model": trace_metadata["model"],
            },
            "status": "pending",
            "tags": [*self.tags, "claude_agent_sdk", "session"],
            "metadata": trace_metadata,
            "start_time": session_start_iso,
            "created_at": session_start_iso,
        }
        if self.user_id:
            session_span_data["user_id"] = self.user_id
        if self.session_id:
            session_span_data["session_id"] = self.session_id

        if aigie._buffer:
            logger.debug(
                f"[AIGIE] root span (session): id={self.session_span_id}, name={trace_name}, parent=None"
            )
            self.open_span(payload=session_span_data)

        return self.trace_id

    async def handle_session_end(  # noqa: PLR0915
        self,
        turn_count: int,
        total_cost: float,
        error: str | None = None,
    ):
        """
        Called when a ClaudeSDKClient session ends.

        Args:
            turn_count: Number of conversation turns
            total_cost: Total cost in USD
            error: Error message if session failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        end_time = _utc_now()
        success = error is None

        # The session span IS the trace root: finalize it once, folding the
        # trace-level aggregate (top-level turn_count, name) onto it. No
        # separate trace event — trace identity rides this span.
        if self.session_span_id:
            session_tokens = self.total_input_tokens + self.total_output_tokens
            session_update = {
                "id": self.session_span_id,
                "trace_id": self.trace_id,  # Required for backend merge
                "parent_id": None,
                "name": getattr(self, "_root_name", self.trace_name),
                "type": "agent",
                "status": "success" if success else "error",
                "output": {
                    "turn_count": turn_count,
                    "total_cost": total_cost,
                    "total_tokens": session_tokens,
                    "total_tool_calls": self.total_tool_calls,
                    "usage": {
                        "input_tokens": self.total_input_tokens,
                        "output_tokens": self.total_output_tokens,
                        "total_tokens": session_tokens,
                    },
                },
                "start_time": getattr(self, "_session_start_iso", None),  # Preserve start_time
                "end_time": end_time.isoformat(),
                "prompt_tokens": self.total_input_tokens,
                "completion_tokens": self.total_output_tokens,
                "total_tokens": session_tokens,
                "total_cost": total_cost,
                "turn_count": turn_count,  # Top-level for backend indexing
            }
            if self.session_id:
                session_update["session_id"] = self.session_id

            if error:
                session_update["error"] = error
                session_update["error_message"] = error

            if aigie._buffer:
                logger.debug(
                    f"[AIGIE] root span (session) finalized: id={self.trace_id}, total_tokens={session_tokens}, cost={total_cost}, turn_count={turn_count}"
                )
                self.close_span(payload=session_update)

        # Complete any pending spans to ensure all have end_time
        await self.complete_pending_turn_spans()
        await self.complete_pending_tool_spans()
        await self.complete_pending_subagent_spans()

    async def handle_turn_start(  # noqa: PLR0915
        self,
        turn_id: str,
        user_message: str,
        turn_number: int | None = None,
    ) -> str:  # noqa: PLR0915
        """
        Called when a conversation turn starts.

        Args:
            turn_id: Unique turn identifier
            user_message: The user's message
            turn_number: Turn number in the conversation (optional, uses session count if not provided)

        Returns:
            The span ID for this turn
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        # Use session context turn number if not provided
        if turn_number is None:
            if self._session_context:
                turn_number = self._session_context.increment_turn()
            else:
                self._local_total_turns += 1
                turn_number = self._local_total_turns
        else:
            # Update total_turns to match provided turn_number
            self.total_turns = turn_number

        span_id = str(uuid.uuid4())
        start_time = _utc_now()
        start_time_iso = start_time.isoformat()

        # Get parent span ID
        parent_id = self.session_span_id or self.query_span_id

        self.turn_map[turn_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "startTimeIso": start_time_iso,
            "turnNumber": turn_number,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"Turn {turn_number}",
            "type": "chain",
            "input": {
                "user_message": user_message[:1000] if self.capture_messages else "[redacted]",
                "turn_number": turn_number,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "turnId": turn_id,
                    "turnNumber": turn_number,
                    "framework": "claude_agent_sdk",
                }
            ),
            "start_time": start_time_iso,
            "created_at": start_time_iso,
        }

        self._current_turn_span_id = span_id

        if user_message and user_message != "[tool_use continuation]":
            self._current_user_prompt = user_message
            if turn_number == 1:
                self._drift_detector.capture_initial_prompt(user_message)

        # Update session context current turn span ID and set as current parent
        if self._session_context:
            self._session_context.current_turn_span_id = span_id
            self._session_context.set_current_parent(span_id)

        if aigie._buffer:
            logger.debug(
                f"[AIGIE] SPAN_CREATE: id={span_id}, name=Turn {turn_number}, parent={parent_id}"
            )
            self.open_span(payload=span_data)

        return span_id

    async def handle_turn_end(  # noqa: C901, PLR0915
        self,
        turn_id: str,
        output: str | None = None,
        usage: dict[str, int] | None = None,
        cost: float = 0.0,
        error: str | None = None,
    ):
        """
        Called when a conversation turn completes.

        Args:
            turn_id: Unique turn identifier
            output: The assistant's response (optional)
            usage: Token usage for this turn
            cost: Cost for this turn
            error: Error message if turn failed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        turn_data = self.turn_map.get(turn_id)
        if not turn_data:
            return

        end_time = _utc_now()
        duration = (end_time - turn_data["startTime"]).total_seconds()

        # Update totals - skip if already accumulated from stream to avoid double-counting
        if usage and not self._tokens_accumulated_from_stream:
            self.total_input_tokens += usage.get("input_tokens", 0)
            self.total_output_tokens += usage.get("output_tokens", 0)
        if cost > 0 and not self._tokens_accumulated_from_stream:
            self.total_cost += cost

        # Determine status
        success = error is None

        update_data = {
            "id": turn_data["spanId"],
            "trace_id": self.trace_id,  # Required for backend merge
            "name": f"Turn {turn_data['turnNumber']}",  # Include name for race conditions
            "type": "chain",  # Include type for race conditions
            "status": "success" if success else "error",
            "start_time": turn_data.get("startTimeIso"),  # Preserve start_time
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        # Add output. Use `text` to match the key set on child LLM Response
        # spans so a single accessor works on both span types.
        if output:
            update_data["output"] = {
                "text": output[:1000] if self.capture_messages else "[redacted]",
            }

        # Add error info
        if error:
            sanitized = _sanitize_error(error)
            update_data["error"] = sanitized
            update_data["error_message"] = sanitized

        if usage:
            update_data["prompt_tokens"] = usage.get("input_tokens", 0)
            update_data["completion_tokens"] = usage.get("output_tokens", 0)
            update_data["total_tokens"] = usage.get("input_tokens", 0) + usage.get(
                "output_tokens", 0
            )

        if cost > 0:
            update_data["total_cost"] = cost

        if aigie._buffer:
            self.close_span(payload=update_data)

        del self.turn_map[turn_id]
        self._current_turn_span_id = None

        # Update session context - clear turn span and parent
        if self._session_context:
            self._session_context.current_turn_span_id = None
            # Revert parent to query span (if exists) since turn is done
            self._session_context.set_current_parent(self._current_query_span_id)

    async def handle_turn_error(self, turn_id: str, error: str) -> None:
        """Called when a turn encounters an error."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        turn_data = self.turn_map.get(turn_id)
        if not turn_data:
            return

        end_time = _utc_now()
        duration = (end_time - turn_data["startTime"]).total_seconds()

        sanitized = _sanitize_error(error)
        update_data = {
            "id": turn_data["spanId"],
            "trace_id": self.trace_id,  # Required for backend merge
            "name": f"Turn {turn_data['turnNumber']}",  # Include name for race conditions
            "type": "chain",  # Include type for race conditions
            "status": "error",
            "error": sanitized,
            "error_message": sanitized,
            "start_time": turn_data.get("startTimeIso"),  # Preserve start_time
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            self.close_span(payload=update_data)

        del self.turn_map[turn_id]
        self._current_turn_span_id = None

        # Update session context - clear turn span and parent
        if self._session_context:
            self._session_context.current_turn_span_id = None
            # Revert parent to query span (if exists) since turn errored
            self._session_context.set_current_parent(self._current_query_span_id)
