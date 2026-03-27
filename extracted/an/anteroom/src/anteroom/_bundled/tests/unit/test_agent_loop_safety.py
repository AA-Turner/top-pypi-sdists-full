"""Tests for agent loop safety features: DLP, line repeat, consecutive text, context recovery (#1021)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.services.agent_loop import AgentEvent, run_agent_loop


def _make_stream_events(
    content: str = "",
    tool_calls: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if content:
        events.append({"event": "token", "data": {"content": content}})
    for tc in tool_calls or []:
        events.append({"event": "tool_call", "data": tc})
    events.append({"event": "done", "data": {}})
    return events


def _mock_ai_service(*rounds: list[dict[str, Any]]) -> AsyncMock:
    service = AsyncMock()
    call_count = 0

    async def _stream_chat(
        messages: Any, tools: Any = None, cancel_event: Any = None, extra_system_prompt: Any = None
    ) -> Any:
        nonlocal call_count
        idx = min(call_count, len(rounds) - 1)
        call_count += 1
        for event in rounds[idx]:
            yield event

    service.stream_chat = _stream_chat
    return service


async def _collect(gen: Any) -> list[AgentEvent]:
    events: list[AgentEvent] = []
    async for e in gen:
        events.append(e)
    return events


async def _executor(name: str, args: dict[str, Any]) -> dict[str, Any]:
    return {"result": "ok"}


# ---------------------------------------------------------------------------
# DLP scanning
# ---------------------------------------------------------------------------


@dataclass
class _MockDlpMatch:
    rule_name: str


@dataclass
class _MockDlpResult:
    matched: bool
    action: str
    matches: list[_MockDlpMatch] = field(default_factory=list)


class _MockDlpScanner:
    def __init__(self, action: str = "block") -> None:
        self.enabled = True
        self.scan_output = True
        self._action = action
        self._call_count = 0

    def apply(self, text: str, direction: str) -> tuple[str, _MockDlpResult]:
        self._call_count += 1
        if "SSN" in text:
            return text, _MockDlpResult(
                matched=True, action=self._action, matches=[_MockDlpMatch(rule_name="ssn_pattern")]
            )
        return text, _MockDlpResult(matched=False, action="none")


class TestDlpScanning:
    @pytest.mark.asyncio
    async def test_dlp_block_stops_stream(self) -> None:
        ai = _mock_ai_service(_make_stream_events("Here is SSN 123-45-6789"))
        scanner = _MockDlpScanner(action="block")

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "show SSN"}],
                tool_executor=_executor,
                tools_openai=None,
                dlp_scanner=scanner,
            )
        )

        blocked = [e for e in events if e.kind == "dlp_blocked"]
        assert len(blocked) == 1
        assert "ssn_pattern" in blocked[0].data["matches"]
        assert not any(e.kind == "done" for e in events)

    @pytest.mark.asyncio
    async def test_dlp_warn_emits_warning(self) -> None:
        ai = _mock_ai_service(_make_stream_events("Found SSN 111-22-3333"))
        scanner = _MockDlpScanner(action="warn")

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "find SSN"}],
                tool_executor=_executor,
                tools_openai=None,
                dlp_scanner=scanner,
            )
        )

        warnings = [e for e in events if e.kind == "dlp_warning"]
        assert len(warnings) == 1
        assert any(e.kind == "done" for e in events)

    @pytest.mark.asyncio
    async def test_dlp_clean_text_passes(self) -> None:
        ai = _mock_ai_service(_make_stream_events("Hello world"))
        scanner = _MockDlpScanner(action="block")

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "hi"}],
                tool_executor=_executor,
                tools_openai=None,
                dlp_scanner=scanner,
            )
        )

        assert not any(e.kind == "dlp_blocked" for e in events)
        assert any(e.kind == "done" for e in events)


# ---------------------------------------------------------------------------
# Line repetition detection
# ---------------------------------------------------------------------------


class TestLineRepetition:
    @pytest.mark.asyncio
    async def test_repeated_lines_stop_loop(self) -> None:
        repeated = "\n".join(["same line"] * 6) + "\n"
        ai = _mock_ai_service(_make_stream_events(repeated))

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "repeat"}],
                tool_executor=_executor,
                tools_openai=None,
                max_line_repeats=5,
            )
        )

        errors = [e for e in events if e.kind == "error"]
        assert len(errors) == 1
        assert "Repetitive" in errors[0].data["message"]

    @pytest.mark.asyncio
    async def test_disabled_line_repeat_does_not_stop(self) -> None:
        repeated = "\n".join(["same line"] * 10) + "\n"
        ai = _mock_ai_service(_make_stream_events(repeated))

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "repeat"}],
                tool_executor=_executor,
                tools_openai=None,
                max_line_repeats=0,
            )
        )

        assert any(e.kind == "done" for e in events)
        assert not any(e.kind == "error" for e in events)

    @pytest.mark.asyncio
    async def test_below_threshold_passes(self) -> None:
        content = "\n".join(["same line"] * 4) + "\ndifferent\n"
        ai = _mock_ai_service(_make_stream_events(content))

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "test"}],
                tool_executor=_executor,
                tools_openai=None,
                max_line_repeats=5,
            )
        )

        assert any(e.kind == "done" for e in events)
        assert not any(e.kind == "error" for e in events)


# ---------------------------------------------------------------------------
# Consecutive text-only limit
# ---------------------------------------------------------------------------


class TestConsecutiveTextOnly:
    @pytest.mark.asyncio
    async def test_exceeding_limit_stops_loop(self) -> None:
        import asyncio

        text_events = _make_stream_events("response text")
        # Need enough rounds: the loop processes text-only then checks queue.
        # On the first text-only, consecutive_text_only=1, not > 3 so it returns done.
        # We need a queued message to keep the loop going.
        ai = _mock_ai_service(text_events, text_events, text_events, text_events, text_events)

        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        # Queue 4 follow-up messages to keep the loop going past the limit
        for _ in range(4):
            await queue.put({"role": "user", "content": "continue"})

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "loop"}],
                tool_executor=_executor,
                tools_openai=None,
                max_consecutive_text_only=3,
                message_queue=queue,
            )
        )

        errors = [e for e in events if e.kind == "error"]
        assert any("consecutive text-only" in e.data.get("message", "") for e in errors)

    @pytest.mark.asyncio
    async def test_tool_call_resets_counter(self) -> None:
        text_round = _make_stream_events("text")
        tool_round = _make_stream_events(
            content="using tool",
            tool_calls=[{"id": "tc1", "function_name": "bash", "arguments": {"cmd": "ls"}}],
        )
        text_round2 = _make_stream_events("final answer")

        ai = _mock_ai_service(text_round, text_round, tool_round, text_round2)

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "do stuff"}],
                tool_executor=_executor,
                tools_openai=None,
                max_consecutive_text_only=3,
            )
        )

        errors = [e for e in events if e.kind == "error" and "consecutive" in e.data.get("message", "")]
        assert len(errors) == 0

    @pytest.mark.asyncio
    async def test_disabled_consecutive_limit(self) -> None:
        text_events = _make_stream_events("response")
        ai = _mock_ai_service(text_events)

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "hi"}],
                tool_executor=_executor,
                tools_openai=None,
                max_consecutive_text_only=0,
            )
        )

        assert any(e.kind == "done" for e in events)


# ---------------------------------------------------------------------------
# Context recovery
# ---------------------------------------------------------------------------


class TestContextRecovery:
    @pytest.mark.asyncio
    async def test_context_error_triggers_truncation(self) -> None:
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"message": "too long", "code": "context_length_exceeded", "retryable": False}},
        ]
        success_events = _make_stream_events("recovered")

        ai = _mock_ai_service(context_error_events, success_events)

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "hi"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "tc1", "function": {"name": "bash", "arguments": '{"cmd": "ls"}'}, "type": "function"}
                ],
            },
            {"role": "tool", "tool_call_id": "tc1", "content": "x" * 50000},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                tool_output_max_chars=2000,
            )
        )

        assert any(e.kind == "done" for e in events)

    @pytest.mark.asyncio
    async def test_context_error_compacts_when_no_truncation(self) -> None:
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"message": "too long", "code": "context_length_exceeded", "retryable": False}},
        ]
        success_events = _make_stream_events("compacted")

        ai = _mock_ai_service(context_error_events, success_events)
        ai.complete = AsyncMock(return_value="Summary of conversation")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "message 1"},
            {"role": "assistant", "content": "response 1"},
            {"role": "user", "content": "message 2"},
            {"role": "assistant", "content": "response 2"},
            {"role": "user", "content": "message 3"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
            )
        )

        assert any(e.kind == "done" for e in events)


# ---------------------------------------------------------------------------
# Max iterations
# ---------------------------------------------------------------------------


class TestMaxIterations:
    @pytest.mark.asyncio
    async def test_max_iterations_yields_error(self) -> None:
        tool_round = _make_stream_events(
            content="",
            tool_calls=[{"id": "tc1", "function_name": "bash", "arguments": {"cmd": "ls"}}],
        )
        ai = _mock_ai_service(tool_round)

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "loop forever"}],
                tool_executor=_executor,
                tools_openai=None,
                max_iterations=2,
            )
        )

        errors = [e for e in events if e.kind == "error"]
        assert any("Max iterations" in e.data.get("message", "") for e in errors)


# ---------------------------------------------------------------------------
# Output filter
# ---------------------------------------------------------------------------


@dataclass
class _MockFilterMatch:
    rule_name: str


@dataclass
class _MockFilterResult:
    matched: bool
    action: str
    matches: list[_MockFilterMatch] = field(default_factory=list)


class _MockOutputFilter:
    def __init__(self, action: str = "block") -> None:
        self.enabled = True
        self._action = action

    def scan_patterns_only(self, text: str) -> _MockFilterResult:
        if "LEAKED" in text:
            return _MockFilterResult(matched=True, action=self._action, matches=[_MockFilterMatch("leak_pattern")])
        return _MockFilterResult(matched=False, action="none")

    def apply(self, text: str) -> tuple[str, _MockFilterResult]:
        if "LEAKED" in text:
            return text, _MockFilterResult(
                matched=True, action=self._action, matches=[_MockFilterMatch("leak_pattern")]
            )
        return text, _MockFilterResult(matched=False, action="none")


class TestOutputFilter:
    @pytest.mark.asyncio
    async def test_output_filter_block(self) -> None:
        ai = _mock_ai_service(_make_stream_events("This has LEAKED content"))
        filt = _MockOutputFilter(action="block")

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "leak"}],
                tool_executor=_executor,
                tools_openai=None,
                output_filter=filt,
            )
        )

        blocked = [e for e in events if e.kind == "output_filter_blocked"]
        assert len(blocked) == 1

    @pytest.mark.asyncio
    async def test_output_filter_warn(self) -> None:
        ai = _mock_ai_service(_make_stream_events("This has LEAKED data"))
        filt = _MockOutputFilter(action="warn")

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=[{"role": "user", "content": "warn"}],
                tool_executor=_executor,
                tools_openai=None,
                output_filter=filt,
            )
        )

        warnings = [e for e in events if e.kind == "output_filter_warning"]
        assert len(warnings) == 1
        assert any(e.kind == "done" for e in events)
