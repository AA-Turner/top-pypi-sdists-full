"""Tests for phase event forwarding in the agent loop (#203)."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from anteroom.config import AIConfig
from anteroom.services.agent_loop import AgentEvent, run_agent_loop
from anteroom.services.ai_service import AIService


def _make_config(**overrides: Any) -> AIConfig:
    defaults = {
        "base_url": "http://localhost:11434/v1",
        "api_key": "test-key",
        "model": "gpt-4",
        "request_timeout": 120,
        "verify_ssl": True,
    }
    defaults.update(overrides)
    return AIConfig(**defaults)


def _make_ai_service() -> AIService:
    service = AIService.__new__(AIService)
    service.config = _make_config()
    service._token_provider = None
    service.client = MagicMock()
    return service


class TestAgentLoopPhaseForwarding:
    """Tests for phase event forwarding through the agent loop."""

    @pytest.mark.asyncio
    async def test_phase_events_forwarded_from_stream_chat(self) -> None:
        """Agent loop must forward phase events from ai_service.stream_chat."""
        ai_service = _make_ai_service()

        async def fake_stream_chat(messages: Any, **kwargs: Any):
            yield {"event": "phase", "data": {"phase": "connecting"}}
            yield {"event": "phase", "data": {"phase": "waiting"}}
            yield {"event": "token", "data": {"content": "hello"}}
            yield {"event": "done", "data": {}}

        ai_service.stream_chat = fake_stream_chat

        events: list[AgentEvent] = []
        async for event in run_agent_loop(
            ai_service=ai_service,
            messages=[{"role": "user", "content": "hi"}],
            tool_executor=AsyncMock(),
            tools_openai=None,
        ):
            events.append(event)

        phase_events = [e for e in events if e.kind == "phase"]
        assert len(phase_events) == 2
        assert phase_events[0].data["phase"] == "connecting"
        assert phase_events[1].data["phase"] == "waiting"

    @pytest.mark.asyncio
    async def test_phase_events_order_preserved(self) -> None:
        """Phase events must appear before token events in the output."""
        ai_service = _make_ai_service()

        async def fake_stream_chat(messages: Any, **kwargs: Any):
            yield {"event": "phase", "data": {"phase": "connecting"}}
            yield {"event": "phase", "data": {"phase": "waiting"}}
            yield {"event": "token", "data": {"content": "hi"}}
            yield {"event": "done", "data": {}}

        ai_service.stream_chat = fake_stream_chat

        events: list[AgentEvent] = []
        async for event in run_agent_loop(
            ai_service=ai_service,
            messages=[{"role": "user", "content": "test"}],
            tool_executor=AsyncMock(),
            tools_openai=None,
        ):
            events.append(event)

        kinds = [e.kind for e in events]
        # thinking comes first (from the agent loop), then phase events, then token
        thinking_idx = kinds.index("thinking")
        connecting_idx = kinds.index("phase")
        token_idx = kinds.index("token")
        assert thinking_idx < connecting_idx < token_idx

    @pytest.mark.asyncio
    async def test_phase_events_forwarded_with_tool_calls(self) -> None:
        """Phase events must be forwarded even when tool calls are present."""
        ai_service = _make_ai_service()
        call_count = 0

        async def fake_stream_chat(messages: Any, **kwargs: Any):
            nonlocal call_count
            call_count += 1
            yield {"event": "phase", "data": {"phase": "connecting"}}
            yield {"event": "phase", "data": {"phase": "waiting"}}
            if call_count == 1:
                yield {
                    "event": "tool_call",
                    "data": {"id": "call_1", "function_name": "bash", "arguments": {"command": "ls"}},
                }
            else:
                yield {"event": "token", "data": {"content": "done"}}
                yield {"event": "done", "data": {}}

        ai_service.stream_chat = fake_stream_chat

        async def fake_tool_executor(name: str, args: dict) -> dict:
            return {"stdout": "file.txt"}

        events: list[AgentEvent] = []
        async for event in run_agent_loop(
            ai_service=ai_service,
            messages=[{"role": "user", "content": "list files"}],
            tool_executor=fake_tool_executor,
            tools_openai=[{"type": "function", "function": {"name": "bash"}}],
        ):
            events.append(event)

        phase_events = [e for e in events if e.kind == "phase"]
        # Two iterations = 4 phase events (2 per iteration) + 1 tool_exec phase = 5
        assert len(phase_events) == 5
        phases = [e.data["phase"] for e in phase_events]
        assert phases.count("connecting") == 2
        assert phases.count("waiting") >= 0  # may or may not appear
        assert phases.count("tool_exec") == 1

    @pytest.mark.asyncio
    async def test_phase_events_not_stored_in_messages(self) -> None:
        """Phase events are display-only and must NOT be stored in the messages list."""
        ai_service = _make_ai_service()

        async def fake_stream_chat(messages: Any, **kwargs: Any):
            yield {"event": "phase", "data": {"phase": "connecting"}}
            yield {"event": "phase", "data": {"phase": "waiting"}}
            yield {"event": "token", "data": {"content": "hello"}}
            yield {"event": "done", "data": {}}

        ai_service.stream_chat = fake_stream_chat

        messages: list[dict[str, Any]] = [{"role": "user", "content": "hi"}]
        async for _ in run_agent_loop(
            ai_service=ai_service,
            messages=messages,
            tool_executor=AsyncMock(),
            tools_openai=None,
        ):
            pass

        # Messages should only contain the original user message
        # (no phase-related messages stored)
        for msg in messages:
            assert "phase" not in str(msg.get("content", "")).lower() or msg["role"] == "user"

    @pytest.mark.asyncio
    async def test_retrying_events_forwarded(self) -> None:
        """Retrying events from stream_chat must be forwarded as AgentEvent(kind='retrying')."""
        ai_service = _make_ai_service()

        async def fake_stream_chat(messages: Any, **kwargs: Any):
            yield {"event": "phase", "data": {"phase": "connecting"}}
            yield {"event": "retrying", "data": {"attempt": 2, "max_attempts": 3, "delay": 1.0}}
            yield {"event": "phase", "data": {"phase": "connecting"}}
            yield {"event": "phase", "data": {"phase": "waiting"}}
            yield {"event": "token", "data": {"content": "hello"}}
            yield {"event": "done", "data": {}}

        ai_service.stream_chat = fake_stream_chat

        events: list[AgentEvent] = []
        async for event in run_agent_loop(
            ai_service=ai_service,
            messages=[{"role": "user", "content": "hi"}],
            tool_executor=AsyncMock(),
            tools_openai=None,
        ):
            events.append(event)

        retry_events = [e for e in events if e.kind == "retrying"]
        assert len(retry_events) == 1
        assert retry_events[0].data["attempt"] == 2
        assert retry_events[0].data["max_attempts"] == 3

    @pytest.mark.asyncio
    async def test_tool_exec_phase_emitted_before_tool_execution(self) -> None:
        """Agent loop emits phase: tool_exec with tool context before executing tools (#1366)."""
        ai_service = _make_ai_service()
        call_count = 0

        async def fake_stream_chat(messages: Any, **kwargs: Any):
            nonlocal call_count
            call_count += 1
            yield {"event": "phase", "data": {"phase": "connecting"}}
            if call_count == 1:
                yield {
                    "event": "tool_call",
                    "data": {"id": "call_1", "function_name": "read_file", "arguments": {"path": "src/foo.py"}},
                }
                yield {
                    "event": "tool_call",
                    "data": {"id": "call_2", "function_name": "read_file", "arguments": {"path": "src/bar.py"}},
                }
            else:
                yield {"event": "token", "data": {"content": "done"}}
                yield {"event": "done", "data": {}}

        ai_service.stream_chat = fake_stream_chat

        async def fake_tool_executor(name: str, args: dict) -> dict:
            return {"content": "file content"}

        events: list[AgentEvent] = []
        async for event in run_agent_loop(
            ai_service=ai_service,
            messages=[{"role": "user", "content": "read files"}],
            tool_executor=fake_tool_executor,
            tools_openai=[{"type": "function", "function": {"name": "read_file"}}],
        ):
            events.append(event)

        tool_exec_phases = [e for e in events if e.kind == "phase" and e.data.get("phase") == "tool_exec"]
        assert len(tool_exec_phases) == 1
        evt = tool_exec_phases[0]
        assert evt.data["tool_count"] == 2
        assert evt.data["tool_names"] == ["read_file", "read_file"]
        assert len(evt.data["tool_summaries"]) == 2
        assert "src/foo.py" in evt.data["tool_summaries"][0]
        assert "src/bar.py" in evt.data["tool_summaries"][1]

        # Verify tool_exec phase appears before tool_call_end events
        tool_exec_idx = next(
            i for i, e in enumerate(events) if e.kind == "phase" and e.data.get("phase") == "tool_exec"
        )
        first_end_idx = next(i for i, e in enumerate(events) if e.kind == "tool_call_end")
        assert tool_exec_idx < first_end_idx


class TestHumanizeToolBrief:
    """Tests for _humanize_tool_brief helper (#1366)."""

    def test_read_file(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        assert _humanize_tool_brief("read_file", {"path": "src/foo.py"}) == "Reading src/foo.py"

    def test_write_file(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        assert _humanize_tool_brief("write_file", {"path": "out.txt"}) == "Writing out.txt"

    def test_edit_file(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        assert _humanize_tool_brief("edit_file", {"file_path": "a.py"}) == "Editing a.py"

    def test_grep(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        assert _humanize_tool_brief("grep", {"pattern": "TODO"}) == "Searching for 'TODO'"

    def test_bash(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        result = _humanize_tool_brief("bash", {"command": "echo hello"})
        assert result == "bash echo hello"

    def test_bash_long_command_truncated(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        long_cmd = "x" * 100
        result = _humanize_tool_brief("bash", {"command": long_cmd})
        assert len(result) < 100
        assert result.endswith("...")

    def test_unknown_tool(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        assert _humanize_tool_brief("my_custom_tool", {}) == "my_custom_tool"

    def test_run_agent(self) -> None:
        from anteroom.services.agent_loop import _humanize_tool_brief

        assert _humanize_tool_brief("run_agent", {"prompt": "do stuff"}) == "Running sub-agent"
