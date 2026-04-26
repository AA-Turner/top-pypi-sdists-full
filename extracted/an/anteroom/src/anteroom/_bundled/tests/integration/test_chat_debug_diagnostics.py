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
    tool_output_max_chars = 10_000
    max_consecutive_text_only = 3
    max_line_repeats = 5
    density = None


def _event(kind: str, data: dict[str, Any]) -> SimpleNamespace:
    return SimpleNamespace(kind=kind, data=data)


def _make_context(*, debug: bool) -> MagicMock:
    ctx = MagicMock()
    ctx.ai_service = MagicMock()
    ctx.ai_service.config.provider = "openai"
    ctx.ai_service.config.model = "gpt-test"
    ctx.ai_service.config.narration_cadence = 0
    ctx.ai_messages = []
    ctx.tool_executor = MagicMock()
    ctx.tools = []
    ctx.cancel_event = asyncio.Event()
    ctx.extra_system_prompt = ""
    ctx.conversation_id = str(uuid.uuid4())
    ctx.plan_mode = False
    ctx.plan_path = None
    ctx.db = MagicMock()
    ctx.db_name = "personal"
    ctx.uid = None
    ctx.uname = None
    ctx.event_bus = None
    ctx.client_id = "client-1"
    ctx.tool_registry = MagicMock()
    ctx.tool_registry.has_tool.return_value = True
    ctx.mcp_manager = None
    ctx.subagent_events = asyncio.Queue()
    ctx.is_first_message = False
    ctx.first_user_text = "hello"
    ctx.conv_title = "Test Conversation"
    ctx.embedding_worker = None
    ctx.planning_config = MagicMock()
    ctx.planning_config.auto_mode = "off"
    ctx.planning_config.auto_threshold_tools = 0
    ctx.budget_config = None
    ctx.request = MagicMock()
    ctx.request.app.state.config.cli = _FakeCliConfig()
    ctx.request.app.state.config.safety.output_filter = None
    ctx.request.app.state.config.memory = None
    ctx.request.app.state.audit_writer = None
    ctx.request.app.state.dlp_scanner = None
    ctx.request.app.state.injection_detector = None
    ctx.canvas_needs_approval = False
    ctx.token_throttle_interval = 999
    ctx.last_token_broadcast = 0.0
    ctx.prompt_meta = {
        "context_turns": [],
        "rag_sources": [],
        "memory_recall_items": [],
        "pack_attachments": [],
        "instruction_files": [],
    }
    ctx.user_msg = None
    ctx.debug_diagnostics = debug
    ctx.recalled_memories = []
    return ctx


async def _collect(ctx: MagicMock, events: list[SimpleNamespace]) -> list[dict[str, Any]]:
    async def fake_agent(*args: Any, **kwargs: Any) -> Any:
        for ev in events:
            yield ev

    assistant_msg = {"id": "assistant-1", "position": 2, "content": "done"}
    with (
        patch("anteroom.routers.chat.run_agent_loop", side_effect=fake_agent),
        patch("anteroom.routers.chat.storage") as mock_storage,
        patch("anteroom.services.packs.list_packs", return_value=[]),
    ):
        mock_storage.get_conversation_token_total.return_value = 0
        mock_storage.get_daily_token_total.return_value = 0
        mock_storage.create_message.return_value = assistant_msg
        mock_storage.list_tool_calls.return_value = []
        mock_storage.merge_message_metadata = MagicMock()
        return [ev async for ev in _stream_chat_events(ctx)]


@pytest.mark.asyncio
async def test_debug_summary_sse_is_absent_by_default() -> None:
    result = await _collect(
        _make_context(debug=False),
        [_event("assistant_message", {"content": "done"}), _event("done", {})],
    )

    assert "debug_summary" not in [ev.get("event") for ev in result]


@pytest.mark.asyncio
async def test_debug_summary_sse_is_gated_and_precedes_done() -> None:
    result = await _collect(
        _make_context(debug=True),
        [
            _event("phase", {"phase": "waiting"}),
            _event("tool_call_start", {"id": "tc-1", "tool_name": "bash", "arguments": {"command": "secret"}}),
            _event(
                "tool_call_end",
                {
                    "id": "tc-1",
                    "tool_name": "bash",
                    "status": "success",
                    "output": {"stdout": "secret", "error": "secret"},
                },
            ),
            _event("assistant_message", {"content": "done"}),
            _event("done", {"stop_reason": "completed"}),
        ],
    )

    event_names = [ev.get("event") for ev in result]
    assert "debug_summary" in event_names
    assert event_names.index("debug_summary") < event_names.index("done")

    payload = json.loads(next(ev["data"] for ev in result if ev.get("event") == "debug_summary"))
    assert payload["stop_reason"] == "completed"
    assert payload["tools"][0]["name"] == "bash"
    rendered = json.dumps(payload)
    assert "secret" not in rendered
    assert "error_preview" not in rendered
    assert "raw_tool_arguments" in rendered
    assert "raw_tool_output" in rendered
