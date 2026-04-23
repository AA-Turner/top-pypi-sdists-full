"""Integration tests for web-chat attribution (#923, regression for #1472).

Drives ``_stream_chat_events`` with a fake agent-loop event stream to
verify that the per-turn attribution snapshot reports ALL tool calls
executed during a multi-iteration turn, not just the tool calls on the
final stored assistant message.

Root cause recap for #1472: the final assistant message stored in the DB
only reflects the FINAL LLM iteration of a turn. If the final iteration
is pure prose (common for turns that end with a summary), the stored
``tool_calls`` list is empty — so the attribution footer reported
``0 tools`` even when many tools ran. The fix threads an authoritative
``turn_tool_calls`` list into ``build_attribution``.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from anteroom.routers.chat import _stream_chat_events


class _FakeCliConfig:
    max_tool_iterations = 50
    tool_output_max_chars = 2000
    max_consecutive_text_only = 3
    max_line_repeats = 5


def _make_stream_context(*, conv_id: str | None = None) -> MagicMock:
    """Build a minimal mock StreamContext (parallels test_chat_comprehensive)."""
    ctx = MagicMock()
    ctx.conversation_id = conv_id or str(uuid.uuid4())
    ctx.uid = None
    ctx.uname = None
    ctx.event_bus = None
    ctx.embedding_worker = None
    ctx.canvas_needs_approval = False
    ctx.plan_mode = False
    ctx.plan_path = None
    ctx.request = MagicMock()
    ctx.request.app.state.config.cli = _FakeCliConfig()
    ctx.request.app.state.config.safety.output_filter = None
    ctx.request.app.state.config.memory = None
    ctx.request.app.state.audit_writer = None
    ctx.request.app.state.dlp_scanner = None
    ctx.request.app.state.injection_detector = None
    ctx.last_token_broadcast = 0.0
    ctx.token_throttle_interval = 999
    ctx.client_id = ""
    ctx.budget_config = None
    ctx.planning_config = MagicMock()
    ctx.planning_config.auto_mode = "off"
    ctx.planning_config.auto_threshold_tools = 0
    ctx.extra_system_prompt = ""
    ctx.ai_service = MagicMock()
    ctx.ai_service.config.narration_cadence = 0
    ctx.tool_registry = MagicMock()
    ctx.tool_registry.has_tool.return_value = True
    ctx.mcp_manager = MagicMock()
    ctx.prompt_meta = {
        "context_turns": [],
        "rag_sources": [],
        "memory_recall_items": [],
        "pack_attachments": [],
        "instruction_files": [],
    }
    ctx.subagent_events = asyncio.Queue()
    ctx.is_first_message = False
    ctx.first_user_text = "hello"
    ctx.conv_title = "Test Conversation"
    ctx.db = MagicMock()
    ctx.db_name = "personal"
    ctx.cancel_event = asyncio.Event()
    ctx.user_msg = None
    ctx.recalled_memories = []
    return ctx


def _event(kind: str, data: dict[str, Any]) -> SimpleNamespace:
    return SimpleNamespace(kind=kind, data=data)


async def _collect(gen: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    async for ev in gen:
        events.append(ev)
    return events


class TestChatAttributionTurnToolCount:
    """Regression for #1472: attribution must count every tool executed in a
    turn, not just those on the final stored assistant message.
    """

    @pytest.mark.asyncio
    async def test_multi_iteration_turn_counts_all_tools(self) -> None:
        """3 tools run during the turn; final assistant message is prose-only.

        Before #1472 the SSE ``attribution`` payload reported 0 tools
        because ``storage.list_tool_calls`` returns the final message's
        tool_calls (which is empty for prose-only final iterations). The
        fix threads the in-memory per-turn accumulator, so all 3 surface.
        """
        ctx = _make_stream_context()
        # Iteration 1: read_file + tool_end
        # Iteration 2: grep + tool_end
        # Iteration 3: bash + tool_end
        # Final iteration: prose-only assistant message (no new tool calls)
        assistant_msg = {"id": "amsg-final", "position": 1, "content": "summary prose"}
        events = [
            _event("tool_call_start", {"id": "tc-1", "tool_name": "read_file", "index": 0, "arguments": {}}),
            _event("tool_call_end", {"id": "tc-1", "tool_name": "read_file", "output": {}, "status": "success"}),
            _event("tool_call_start", {"id": "tc-2", "tool_name": "grep", "index": 1, "arguments": {}}),
            _event("tool_call_end", {"id": "tc-2", "tool_name": "grep", "output": {}, "status": "success"}),
            _event("tool_call_start", {"id": "tc-3", "tool_name": "bash", "index": 2, "arguments": {}}),
            _event("tool_call_end", {"id": "tc-3", "tool_name": "bash", "output": {}, "status": "success"}),
            _event("assistant_message", {"content": "summary prose"}),
            _event("done", {}),
        ]

        async def fake_agent(*args: Any, **kwargs: Any) -> Any:
            for ev in events:
                yield ev

        with (
            patch("anteroom.routers.chat.run_agent_loop", side_effect=fake_agent),
            patch("anteroom.routers.chat.storage") as mock_storage,
            patch("anteroom.services.packs.list_packs", return_value=[]),
        ):
            mock_storage.get_conversation_token_total.return_value = 0
            mock_storage.get_daily_token_total.return_value = 0
            mock_storage.create_message.return_value = assistant_msg
            # CRUCIAL: simulate the root-cause symptom. The final stored
            # message's tool_calls list is empty because the final
            # iteration was prose-only. Pre-#1472 this caused 0 tools in
            # attribution; post-fix the authoritative per-turn list wins.
            mock_storage.list_tool_calls.return_value = []
            mock_storage.update_conversation_title = MagicMock()
            mock_storage.merge_message_metadata = MagicMock()
            result = await _collect(_stream_chat_events(ctx))

        attribution_events = [e for e in result if isinstance(e, dict) and e.get("event") == "attribution"]
        assert len(attribution_events) == 1, "expected exactly one attribution SSE event per turn"
        payload = json.loads(attribution_events[0]["data"])
        snapshot = payload["snapshot"]
        assert len(snapshot["tools"]) == 3
        assert [t["name"] for t in snapshot["tools"]] == ["read_file", "grep", "bash"]
        assert [t["id"] for t in snapshot["tools"]] == ["tc-1", "tc-2", "tc-3"]

    @pytest.mark.asyncio
    async def test_zero_tool_turn_reports_empty_tools(self) -> None:
        """Prose-only turn (no tools) reports an empty tools list, not undefined."""
        ctx = _make_stream_context()
        assistant_msg = {"id": "amsg-1", "position": 1, "content": "hello"}
        events = [
            _event("assistant_message", {"content": "hello"}),
            _event("done", {}),
        ]

        async def fake_agent(*args: Any, **kwargs: Any) -> Any:
            for ev in events:
                yield ev

        with (
            patch("anteroom.routers.chat.run_agent_loop", side_effect=fake_agent),
            patch("anteroom.routers.chat.storage") as mock_storage,
            patch("anteroom.services.packs.list_packs", return_value=[]),
        ):
            mock_storage.get_conversation_token_total.return_value = 0
            mock_storage.get_daily_token_total.return_value = 0
            mock_storage.create_message.return_value = assistant_msg
            mock_storage.list_tool_calls.return_value = []
            mock_storage.update_conversation_title = MagicMock()
            mock_storage.merge_message_metadata = MagicMock()
            result = await _collect(_stream_chat_events(ctx))

        attribution_events = [e for e in result if isinstance(e, dict) and e.get("event") == "attribution"]
        assert len(attribution_events) == 1
        snapshot = json.loads(attribution_events[0]["data"])["snapshot"]
        assert snapshot["tools"] == []

    @pytest.mark.asyncio
    async def test_sse_attribution_carries_tools_count_30_when_30_tools_ran(self) -> None:
        """Regression for #1473 (web path): when 30 tool calls execute in a
        single turn the SSE ``attribution`` payload MUST carry
        ``tools_count=30`` even though the ``tools`` list is capped at 20
        items (plus one ``{"truncated": 10}`` sentinel).

        Before the #1473 fix the web renderer used ``snapshot.tools.length``
        to show the count, yielding "21 tools" (20 items + sentinel) instead
        of the correct "30 tools".
        """
        ctx = _make_stream_context()
        assistant_msg = {"id": "amsg-30tools", "position": 1, "content": "done"}

        # Build 30 tool_call_start/tool_call_end event pairs.
        tool_events = []
        for i in range(30):
            tool_events.append(
                _event(
                    "tool_call_start",
                    {"id": f"tc-{i}", "tool_name": f"tool_{i}", "index": i, "arguments": {}},
                )
            )
            tool_events.append(
                _event(
                    "tool_call_end",
                    {"id": f"tc-{i}", "tool_name": f"tool_{i}", "output": {}, "status": "success"},
                )
            )
        tool_events.append(_event("assistant_message", {"content": "done"}))
        tool_events.append(_event("done", {}))

        async def fake_agent(*args: Any, **kwargs: Any) -> Any:
            for ev in tool_events:
                yield ev

        with (
            patch("anteroom.routers.chat.run_agent_loop", side_effect=fake_agent),
            patch("anteroom.routers.chat.storage") as mock_storage,
            patch("anteroom.services.packs.list_packs", return_value=[]),
        ):
            mock_storage.get_conversation_token_total.return_value = 0
            mock_storage.get_daily_token_total.return_value = 0
            mock_storage.create_message.return_value = assistant_msg
            # Simulate stored message with only the final iteration's tool calls
            # (empty, as the final iteration is prose-only).
            mock_storage.list_tool_calls.return_value = []
            mock_storage.update_conversation_title = MagicMock()
            mock_storage.merge_message_metadata = MagicMock()
            result = await _collect(_stream_chat_events(ctx))

        attribution_events = [e for e in result if isinstance(e, dict) and e.get("event") == "attribution"]
        assert len(attribution_events) == 1, "expected exactly one attribution SSE event"
        payload = json.loads(attribution_events[0]["data"])
        snapshot = payload["snapshot"]

        # The canonical count field must be 30.
        assert snapshot["tools_count"] == 30, (
            f"expected tools_count=30, got {snapshot.get('tools_count')}. "
            "The web footer would have shown the wrong number."
        )
        # The list must be capped: 20 real items + 1 truncation sentinel.
        assert len(snapshot["tools"]) == 21, (
            f"expected 21 items in tools list (20 cap + 1 sentinel), got {len(snapshot['tools'])}"
        )
        sentinel = snapshot["tools"][-1]
        assert sentinel.get("truncated") == 10, f"expected sentinel {{'truncated': 10}}, got {sentinel}"

        # Verify the persisted metadata carries the same tools_count.
        assert mock_storage.merge_message_metadata.call_count == 1
        persisted_meta = mock_storage.merge_message_metadata.call_args[0][2]
        assert persisted_meta["attribution"]["tools_count"] == 30, (
            "persisted attribution metadata must carry tools_count=30 for correct reload"
        )

    @pytest.mark.asyncio
    async def test_persisted_tools_count_30_survives_reload_and_renders_in_footer(self) -> None:
        """Regression for #1473 (web reload path): a snapshot persisted with
        ``tools_count=30`` must survive the SSE reload cycle.

        This test verifies the serialised attribution dict (as stored in
        ``messages.metadata["attribution"]``) contains the correct
        ``tools_count`` field. The browser-side rendering contract is covered
        by the JS tests in ``tests/js/chat_attribution.test.js``; this test
        ensures the Python-produced payload that feeds those JS tests is correct.
        """
        from anteroom.services.attribution import build_attribution, serialize_attribution

        pm: dict[str, Any] = {
            "context_turns": [],
            "rag_sources": [],
            "memory_recall_items": [],
            "pack_attachments": [],
            "instruction_files": [],
        }
        # 30 tool calls — more than the SECTION_CAP of 20.
        turn_tcs = [{"id": f"tc-{i}", "tool_name": f"tool_{i}", "name": f"tool_{i}"} for i in range(30)]
        stored_msg: dict[str, Any] = {"id": "msg-reload", "role": "assistant", "tool_calls": []}

        snap = build_attribution(pm, stored_msg, [], turn_tool_calls=turn_tcs)

        # The snapshot itself must carry tools_count=30.
        assert snap.tools_count == 30
        # The capped list: 20 real + 1 sentinel.
        assert len(snap.tools) == 21
        assert snap.tools[-1].get("truncated") == 10

        # Serialize to the wire format and verify the count field is present.
        serialized = serialize_attribution(snap)
        assert serialized["tools_count"] == 30, (
            "serialized attribution must include tools_count=30 so that browsers "
            "reading the SSE event or reloaded metadata can display '30 tools'"
        )
        # The tools list in the wire format must also be capped (21 items).
        assert len(serialized["tools"]) == 21
        sentinel = serialized["tools"][-1]
        assert sentinel.get("truncated") == 10

        # Simulate the persist → SSE reload cycle: wrap in the SSE envelope
        # and confirm the consumer (JS _attrCount / Python reload path) receives
        # the canonical field without having to count list items.
        sse_payload = json.dumps({"assistant_message_id": "msg-reload", "snapshot": serialized})
        reloaded = json.loads(sse_payload)["snapshot"]
        assert reloaded["tools_count"] == 30
        assert len(reloaded["tools"]) == 21
