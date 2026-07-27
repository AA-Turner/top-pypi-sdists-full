"""Force-close helpers for pending turn and subagent spans."""

# mypy: disable-error-code="attr-defined,has-type,assignment,var-annotated"

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from aigie.context_manager import merge_metadata
from aigie.integrations.claude_agent_sdk.native_callback import (
    _format_subagent_name,
    _utc_now,
)

logger = logging.getLogger(__name__)


class CompletionEvents:
    _current_turn_span_id: str | None

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
            "status": "success",
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
                "status": "success",
                "start_time": turn_data.get("startTimeIso"),
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
            }

            if aigie._buffer:
                logger.debug(
                    "[AIGIE] Completing pending turn span: Turn %s",
                    turn_data["turnNumber"],
                )
                self.close_span(payload=update_data)

            del self.turn_map[turn_id]

        self._current_turn_span_id = None
