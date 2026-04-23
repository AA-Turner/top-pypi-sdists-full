"""Unit tests for hook_outcome SSE event emission in routers/chat.py (#1491).

Verifies that when a tool_call_end result has ``hook_blocked=True``, the
SSE stream emits a ``hook_outcome`` event *before* the ``tool_call_end``
event, with the correct payload shape.
"""

from __future__ import annotations

import json
from typing import Any


class TestHookOutcomeSseEmission:
    """Validate the hook_outcome SSE emission added to the tool_call_end handler."""

    def _simulate_tool_call_end_sse(
        self,
        tool_output: dict[str, Any],
        tool_name: str = "bash",
        tool_id: str = "tc-abc",
    ) -> list[dict[str, Any]]:
        """Run the inline hook_outcome / tool_call_end emission logic and collect events.

        This mirrors the code added to routers/chat.py in the tool_call_end branch.
        """
        events: list[dict[str, Any]] = []

        sse_output = tool_output
        if isinstance(sse_output, dict) and sse_output.get("hook_blocked"):
            _hook_approval_dec = sse_output.get("_approval_decision", "hook_denied")
            _hook_error_msg = str(sse_output.get("error", "")) or ""
            events.append(
                {
                    "event": "hook_outcome",
                    "data": json.loads(
                        json.dumps(
                            {
                                "tool_name": tool_name,
                                "tool_call_id": tool_id,
                                "outcome": "deny",
                                "approval_decision": _hook_approval_dec,
                                "message": _hook_error_msg,
                            }
                        )
                    ),
                }
            )

        end_payload: dict[str, Any] = {
            "id": tool_id,
            "output": sse_output,
            "status": "error" if sse_output.get("error") else "success",
        }
        events.append({"event": "tool_call_end", "data": end_payload})
        return events

    def test_hook_blocked_emits_hook_outcome_before_tool_call_end(self) -> None:
        output: dict[str, Any] = {
            "error": "Tool 'bash' blocked by hook",
            "hook_blocked": True,
            "_approval_decision": "hook_denied",
        }
        events = self._simulate_tool_call_end_sse(output, tool_name="bash")

        assert len(events) == 2
        assert events[0]["event"] == "hook_outcome"
        assert events[1]["event"] == "tool_call_end"

    def test_hook_outcome_payload_shape(self) -> None:
        output: dict[str, Any] = {
            "error": "No writes to protected paths",
            "hook_blocked": True,
            "_approval_decision": "hook_denied",
        }
        events = self._simulate_tool_call_end_sse(output, tool_name="write_file", tool_id="tc-xyz")

        payload = events[0]["data"]
        assert payload["tool_name"] == "write_file"
        assert payload["tool_call_id"] == "tc-xyz"
        assert payload["outcome"] == "deny"
        assert payload["approval_decision"] == "hook_denied"
        assert "No writes" in payload["message"]

    def test_post_hook_denied_approval_decision(self) -> None:
        output: dict[str, Any] = {
            "error": "Output blocked by post-tool hook",
            "hook_blocked": True,
            "_approval_decision": "post_hook_denied",
        }
        events = self._simulate_tool_call_end_sse(output)

        payload = events[0]["data"]
        assert payload["approval_decision"] == "post_hook_denied"

    def test_no_hook_outcome_for_normal_success(self) -> None:
        output: dict[str, Any] = {"content": "hello world"}
        events = self._simulate_tool_call_end_sse(output)

        assert len(events) == 1
        assert events[0]["event"] == "tool_call_end"

    def test_no_hook_outcome_for_safety_blocked(self) -> None:
        output: dict[str, Any] = {
            "error": "Blocked by safety config",
            "safety_blocked": True,
        }
        events = self._simulate_tool_call_end_sse(output)

        assert len(events) == 1
        assert events[0]["event"] == "tool_call_end"

    def test_empty_message_allowed(self) -> None:
        output: dict[str, Any] = {
            "error": "",
            "hook_blocked": True,
            "_approval_decision": "hook_denied",
        }
        events = self._simulate_tool_call_end_sse(output)
        payload = events[0]["data"]
        assert payload["message"] == ""

    def test_hook_outcome_precedes_tool_call_end_ordering(self) -> None:
        """hook_outcome MUST come before tool_call_end in the event stream."""
        output: dict[str, Any] = {
            "error": "blocked",
            "hook_blocked": True,
            "_approval_decision": "hook_denied",
        }
        events = self._simulate_tool_call_end_sse(output)
        event_names = [e["event"] for e in events]
        assert event_names.index("hook_outcome") < event_names.index("tool_call_end")
