"""Tests for agent loop safety features: DLP, line repeat, consecutive text, context recovery (#1021)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.services.agent_loop import AgentEvent, run_agent_loop
from anteroom.services.ai_service import CompletionResult


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


class _StructuredCompactionAi:
    def __init__(self, rounds: list[list[dict[str, Any]]], completions: list[CompletionResult]) -> None:
        self.rounds = rounds
        self.completions = completions
        self.stream_calls = 0
        self.complete_calls: list[dict[str, Any]] = []

    async def stream_chat(
        self,
        messages: Any,
        tools: Any = None,
        cancel_event: Any = None,
        extra_system_prompt: Any = None,
    ) -> Any:
        idx = min(self.stream_calls, len(self.rounds) - 1)
        self.stream_calls += 1
        for event in self.rounds[idx]:
            yield event

    async def complete_result(
        self,
        messages: list[dict[str, Any]],
        max_completion_tokens: int = 1000,
        **kwargs: Any,
    ) -> CompletionResult:
        self.complete_calls.append({"messages": messages, "max_completion_tokens": max_completion_tokens})
        idx = min(len(self.complete_calls) - 1, len(self.completions) - 1)
        return self.completions[idx]


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

    # ------------------------------------------------------------------
    # Staged overflow recovery integration (#1415)
    # ------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_staged_recovery_order_skips_to_drop_when_no_tools(self) -> None:
        """With no oversized tool output and no older tool results, the
        staged path falls through Strategy 1 and 2 and recovers via
        Strategy 3 (drop old turn groups) without an LLM summary call.
        """
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"message": "too long", "code": "context_length_exceeded", "retryable": False}},
        ]
        success_events = _make_stream_events("recovered")

        ai = _mock_ai_service(context_error_events, success_events)
        ai.complete = AsyncMock(return_value="unused LLM summary")

        # Plenty of user/assistant turn groups (>4) — no tool results.
        messages: list[dict[str, Any]] = []
        for i in range(12):
            messages.append({"role": "user", "content": f"u{i}"})
            messages.append({"role": "assistant", "content": f"a{i}"})

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
            )
        )

        assert any(e.kind == "done" for e in events)
        # Strategy 3 is deterministic — no LLM complete() call required.
        ai.complete.assert_not_awaited()
        # Recovery notification for "dropped older conversation turns" fired.
        notif = "".join(
            e.data.get("content", "") for e in events if e.kind == "token" and isinstance(e.data.get("content"), str)
        )
        assert "dropped older conversation turns" in notif

    @pytest.mark.asyncio
    async def test_full_compaction_is_last_resort(self) -> None:
        """When Strategies 1-3 cannot make progress (too few turn groups,
        no tool outputs), Strategy 4 (full LLM compaction) fires.
        """
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"message": "too long", "code": "context_length_exceeded", "retryable": False}},
        ]
        success_events = _make_stream_events("done")

        ai = _mock_ai_service(context_error_events, success_events)
        ai.complete = AsyncMock(return_value="Final summary")

        # 4 turn groups exactly — drop_old_turn_groups (keep_recent=4)
        # returns False because ``len(groups) <= keep_recent_groups``.
        # Collapse has no tool messages so also returns False.
        # Strategy 4 (full LLM compaction) must then fire.  Note:
        # compact_messages() requires >= COMPACTION_MIN_MESSAGES (4) messages.
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "u1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "u2"},
            {"role": "assistant", "content": "a2"},
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
        # Strategy 4 requires an LLM summary call.
        ai.complete.assert_awaited()

    @pytest.mark.asyncio
    async def test_strategy4_compaction_prompt_too_long_retry_metadata(self) -> None:
        """Strategy 4 emits retry metadata when summary prompt reduction recovers."""
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"message": "too long", "code": "context_length_exceeded", "retryable": False}},
        ]
        success_events = _make_stream_events("done")
        ai = _StructuredCompactionAi(
            [context_error_events, success_events],
            [
                CompletionResult(text=None, error_code="context_length_exceeded", error_message="too long"),
                CompletionResult(text="Recovered summary"),
            ],
        )

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "u1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "u2"},
            {"role": "assistant", "content": "a2"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,  # type: ignore[arg-type]
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_retry_max_attempts=2,
                summary_retry_drop_groups=1,
            )
        )

        assert any(e.kind == "done" for e in events)
        retry_phases = [
            e.data for e in events if e.kind == "phase" and e.data.get("reason") == "compaction_prompt_too_long"
        ]
        assert retry_phases
        assert retry_phases[0]["attempt"] == 2
        assert retry_phases[0]["dropped_messages"] == 1
        assert any(
            "Compaction summary prompt was too long" in e.data.get("content", "") for e in events if e.kind == "token"
        )

    @pytest.mark.asyncio
    async def test_max_recovery_attempts_bounded(self) -> None:
        """After max_context_recoveries repeated context errors, the loop
        gives up with a hard error rather than retrying forever.
        """
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"message": "too long", "code": "context_length_exceeded", "retryable": False}},
        ]

        # Unlimited context errors — never recovers.
        ai = _mock_ai_service(
            context_error_events,
            context_error_events,
            context_error_events,
            context_error_events,
            context_error_events,
            context_error_events,
            context_error_events,
            context_error_events,
        )
        # Make compact return None so Strategy 4 also fails every time.
        ai.complete = AsyncMock(return_value=None)

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

        # Loop must terminate (not hang) with a recovery-failed error.
        errors = [e for e in events if e.kind == "error"]
        assert any(
            "Recovery failed" in e.data.get("message", "") or "too long" in e.data.get("message", "").lower()
            for e in errors
        )

    @pytest.mark.asyncio
    async def test_reactive_max_attempts_from_config(self) -> None:
        """The retry cap is sourced from reactive_max_attempts (#1266)."""
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"code": "context_length_exceeded", "retryable": False}},
        ]
        # 5 rounds of context errors — but we'll cap at 1 retry.
        ai = _mock_ai_service(
            context_error_events,
            context_error_events,
            context_error_events,
            context_error_events,
            context_error_events,
        )
        ai.complete = AsyncMock(return_value=None)

        messages: list[dict[str, Any]] = [{"role": "user", "content": f"m{i}"} for i in range(6)]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                reactive_max_attempts=1,
            )
        )

        errors = [e for e in events if e.kind == "error"]
        assert len(errors) >= 1

    @pytest.mark.asyncio
    async def test_summary_trigger_msg_count_from_config(self) -> None:
        """Proactive summary triggers at the config-provided message count (#1266)."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        # 10 messages — trigger at 8.
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": f"m{i}"} if i % 2 == 0 else {"role": "assistant", "content": f"r{i}"}
            for i in range(10)
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=8,
                summary_trigger_token_count=1_000_000,
            )
        )

        # Compaction event indicates summary fired.
        assert any(e.kind == "compaction" for e in events)
        phases = [e.data for e in events if e.kind == "phase" and e.data.get("phase") == "compacting"]
        assert phases
        assert phases[0]["reason"] == "message_count"
        assert phases[0]["message_count"] == 10
        assert phases[0]["message_threshold"] == 8
        tokens = [e.data.get("content", "") for e in events if e.kind == "token"]
        assert not any("Compacting conversation history" in token for token in tokens)

    @pytest.mark.asyncio
    async def test_summary_trigger_token_count_from_config(self) -> None:
        """Proactive summary triggers at the config-provided token count (#1266)."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        # Large content — trigger on tokens.
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "word " * 500},
            {"role": "assistant", "content": "word " * 500},
            {"role": "user", "content": "word " * 500},
            {"role": "assistant", "content": "word " * 500},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=10_000,
                summary_trigger_token_count=100,
            )
        )

        assert any(e.kind == "compaction" for e in events)
        phases = [e.data for e in events if e.kind == "phase" and e.data.get("phase") == "compacting"]
        assert phases
        assert phases[0]["reason"] == "token_threshold"
        assert phases[0]["estimated_tokens"] >= 100
        assert phases[0]["token_threshold"] == 100

    @pytest.mark.asyncio
    async def test_summary_triggers_on_full_request_fixed_overhead(self) -> None:
        """Large system/tool overhead triggers even when message-only tokens are below threshold."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.config = SimpleNamespace(system_prompt="system overhead " * 500)
        ai.complete = AsyncMock(return_value="Summary")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "short 1"},
            {"role": "assistant", "content": "short 2"},
            {"role": "user", "content": "short 3"},
            {"role": "assistant", "content": "short 4"},
            {"role": "user", "content": "short 5"},
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "large_tool",
                    "description": "tool schema overhead " * 100,
                    "parameters": {"type": "object", "properties": {}},
                },
            }
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=tools,
                extra_system_prompt="dynamic overhead " * 100,
                summary_trigger_msg_count=10_000,
                summary_trigger_token_count=100,
            )
        )

        assert any(e.kind == "compaction" for e in events)
        phase = next(e.data for e in events if e.kind == "phase" and e.data.get("phase") == "compacting")
        assert phase["reason"] == "token_threshold"
        assert phase["message_tokens"] < 100
        assert phase["estimated_tokens"] >= 100
        assert phase["system_prompt_tokens"] > 0
        assert phase["tool_schema_tokens"] > 0

        compaction = next(e.data for e in events if e.kind == "compaction")
        assert compaction["message_tokens"] == phase["message_tokens"]
        assert compaction["system_prompt_tokens"] == phase["system_prompt_tokens"]
        assert compaction["tool_schema_tokens"] == phase["tool_schema_tokens"]

    @pytest.mark.asyncio
    async def test_summary_does_not_trigger_below_thresholds(self) -> None:
        """Proactive summary stays quiet when token and message thresholds are both below budget."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "short"},
            {"role": "assistant", "content": "short"},
            {"role": "user", "content": "short"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=10,
                summary_trigger_token_count=128_000,
            )
        )

        assert not any(e.kind == "compaction" for e in events)
        assert not any(e.kind == "phase" and e.data.get("phase") == "compacting" for e in events)
        ai.complete.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_compacted_history_does_not_immediately_recompact_preserved_tail(self) -> None:
        """Existing compacted prefix/tail does not retrigger until new history accumulates."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "summary", "metadata": {"compact_summary": True}},
            {
                "role": "system",
                "content": "boundary",
                "metadata": {"compact_boundary": True, "preserved_count": 4},
            },
            {"role": "user", "content": "tail 1"},
            {"role": "assistant", "content": "tail 2"},
            {"role": "user", "content": "tail 3"},
            {"role": "assistant", "content": "tail 4"},
            {"role": "user", "content": "new 1"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=4,
                summary_trigger_token_count=1_000_000,
            )
        )

        assert not any(e.kind == "compaction" for e in events)
        assert not any(e.kind == "phase" and e.data.get("phase") == "compacting" for e in events)
        ai.complete.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_compacted_history_fixed_overhead_does_not_recompact_without_new_history(self) -> None:
        """A compacted history is not repeatedly compacted for irreducible fixed overhead."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.config = SimpleNamespace(system_prompt="fixed overhead " * 500)
        ai.complete = AsyncMock(return_value="Summary")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "summary", "metadata": {"compact_summary": True}},
            {
                "role": "system",
                "content": "boundary",
                "metadata": {"compact_boundary": True, "preserved_count": 4},
            },
            {"role": "user", "content": "tail 1", "metadata": {"compact_preserved_tail": True}},
            {"role": "assistant", "content": "tail 2", "metadata": {"compact_preserved_tail": True}},
            {"role": "user", "content": "new 1"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=10_000,
                summary_trigger_token_count=100,
            )
        )

        assert not any(e.kind == "compaction" for e in events)
        assert not any(e.kind == "phase" and e.data.get("phase") == "compacting" for e in events)
        ai.complete.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_compacted_history_recompacts_after_enough_new_messages(self) -> None:
        """Compacted histories can compact again after the post-compaction tail crosses threshold."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "summary", "metadata": {"compact_summary": True}},
            {
                "role": "system",
                "content": "boundary",
                "metadata": {"compact_boundary": True, "preserved_count": 2},
            },
            {"role": "user", "content": "tail 1"},
            {"role": "assistant", "content": "tail 2"},
            {"role": "user", "content": "new 1"},
            {"role": "assistant", "content": "new 2"},
            {"role": "user", "content": "new 3"},
            {"role": "assistant", "content": "new 4"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=4,
                summary_trigger_token_count=1_000_000,
            )
        )

        assert any(e.kind == "compaction" for e in events)
        phases = [e.data for e in events if e.kind == "phase" and e.data.get("phase") == "compacting"]
        assert phases
        assert phases[0]["reason"] == "message_count"
        assert phases[0]["message_count"] == 4

    @pytest.mark.asyncio
    async def test_compacted_history_counts_new_messages_after_preserved_tail_trim(self) -> None:
        """Marked preserved-tail messages prevent stale boundary counts from hiding new turns."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "summary", "metadata": {"compact_summary": True}},
            {
                "role": "system",
                "content": "boundary",
                "metadata": {"compact_boundary": True, "preserved_count": 4},
            },
            {"role": "assistant", "content": "remaining tail", "metadata": {"compact_preserved_tail": True}},
            {"role": "user", "content": "new 1"},
            {"role": "assistant", "content": "new 2"},
            {"role": "user", "content": "new 3"},
            {"role": "assistant", "content": "new 4"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=4,
                summary_trigger_token_count=1_000_000,
            )
        )

        assert any(e.kind == "compaction" for e in events)
        phases = [e.data for e in events if e.kind == "phase" and e.data.get("phase") == "compacting"]
        assert phases
        assert phases[0]["reason"] == "message_count"
        assert phases[0]["message_count"] == 4

    @pytest.mark.asyncio
    async def test_compacted_history_ignores_rebuilt_tool_results_inside_marked_tail(self) -> None:
        """Unmarked synthetic tool results inside a marked tail do not count as new turns."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "summary", "metadata": {"compact_summary": True}},
            {
                "role": "system",
                "content": "boundary",
                "metadata": {"compact_boundary": True, "preserved_count": 4},
            },
            {"role": "assistant", "content": "", "metadata": {"compact_preserved_tail": True}},
            {"role": "tool", "tool_call_id": "tc1", "content": "rebuilt tool result"},
            {"role": "user", "content": "remaining tail", "metadata": {"compact_preserved_tail": True}},
            {"role": "user", "content": "new 1"},
            {"role": "assistant", "content": "new 2"},
            {"role": "user", "content": "new 3"},
            {"role": "assistant", "content": "new 4"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=4,
                summary_trigger_token_count=1_000_000,
            )
        )

        assert any(e.kind == "compaction" for e in events)
        phases = [e.data for e in events if e.kind == "phase" and e.data.get("phase") == "compacting"]
        assert phases
        assert phases[0]["reason"] == "message_count"
        assert phases[0]["message_count"] == 4

    @pytest.mark.asyncio
    async def test_microcompact_fires_before_summary(self) -> None:
        """Proactive microcompact emits its own narration token before the summary check (#1266)."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        # History with an oversized tool result to trigger microcompact.
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "hi"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"id": "tc1", "type": "function", "function": {"name": "bash", "arguments": "{}"}}],
            },
            {"role": "tool", "tool_call_id": "tc1", "content": "X" * 10_000},
            {"role": "user", "content": "continue"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                tool_output_max_chars=200,
                microcompact_enabled=True,
                # Keep summary thresholds high so only microcompact fires.
                summary_trigger_msg_count=10_000,
                summary_trigger_token_count=1_000_000,
            )
        )

        # Microcompact narration token surfaces in the event stream.
        tokens = [e for e in events if e.kind == "token"]
        assert any("Trimmed oversized tool outputs" in e.data.get("content", "") for e in tokens)

    @pytest.mark.asyncio
    async def test_historical_tool_collapse_fires_before_summary(self) -> None:
        """Historical tool-result collapse can reduce pressure before LLM summary compaction."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        large_payload = json.dumps(
            {"status": "ok", "path": "/tmp/big.log", "stdout": " ".join(f"token{i}" for i in range(10_000))}
        )
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "first"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"id": "tc1", "type": "function", "function": {"name": "bash", "arguments": "{}"}}],
            },
            {"role": "tool", "tool_call_id": "tc1", "content": large_payload},
            {"role": "user", "content": "recent"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"id": "tc2", "type": "function", "function": {"name": "bash", "arguments": "{}"}}],
            },
            {"role": "tool", "tool_call_id": "tc2", "content": json.dumps({"stdout": "recent"})},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                tool_output_max_chars=100_000,
                historical_tool_collapse_enabled=True,
                historical_tool_collapse_trigger_token_count=5_000,
                historical_tool_collapse_keep_recent_groups=2,
                historical_tool_collapse_compact_chars=250,
                summary_trigger_msg_count=10_000,
                summary_trigger_token_count=5_000,
            )
        )

        collapse_events = [
            e for e in events if e.kind == "compaction" and e.data.get("strategy") == "historical_tool_results"
        ]
        assert collapse_events
        assert collapse_events[0].data["in_memory_only"] is True
        assert collapse_events[0].data["modified_count"] == 1
        assert any(e.kind == "phase" and e.data.get("reason") == "historical_tool_results" for e in events)
        assert not any(e.kind == "compaction" and e.data.get("strategy") != "historical_tool_results" for e in events)
        ai.complete.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_historical_tool_collapse_noops_below_pressure(self) -> None:
        """Historical collapse does not run on small or low-token histories."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "first"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"id": "tc1", "type": "function", "function": {"name": "bash", "arguments": "{}"}}],
            },
            {"role": "tool", "tool_call_id": "tc1", "content": json.dumps({"stdout": "x" * 5000})},
            {"role": "user", "content": "recent"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                historical_tool_collapse_enabled=True,
                historical_tool_collapse_trigger_token_count=500_000,
                summary_trigger_msg_count=10_000,
                summary_trigger_token_count=1_000_000,
            )
        )

        assert not any(e.kind == "compaction" for e in events)
        assert not any("Collapsed older tool results" in e.data.get("content", "") for e in events if e.kind == "token")

    @pytest.mark.asyncio
    async def test_summary_triggers_at_exactly_threshold(self) -> None:
        """Proactive summary fires when len(messages) == summary_trigger_msg_count (>= semantics)."""
        success_events = _make_stream_events("ok")
        ai = _mock_ai_service(success_events)
        ai.complete = AsyncMock(return_value="Summary")

        # Exactly at threshold — must trigger (>= not >).
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": f"m{i}"} if i % 2 == 0 else {"role": "assistant", "content": f"r{i}"}
            for i in range(8)
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                summary_trigger_msg_count=8,
                summary_trigger_token_count=1_000_000,
            )
        )

        assert any(e.kind == "compaction" for e in events)

    @pytest.mark.asyncio
    async def test_reactive_max_attempts_zero_disables_recovery(self) -> None:
        """reactive_max_attempts=0 disables reactive recovery — original error surfaces."""
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"code": "context_length_exceeded", "retryable": False}},
        ]
        ai = _mock_ai_service(context_error_events)
        ai.complete = AsyncMock(return_value=None)

        messages: list[dict[str, Any]] = [{"role": "user", "content": f"m{i}"} for i in range(4)]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                reactive_max_attempts=0,
            )
        )

        # With recovery disabled, the stream's original context_length_exceeded
        # propagates up without any recovery narration tokens appearing.
        token_content = " ".join(e.data.get("content", "") for e in events if e.kind == "token")
        assert "truncated and retrying" not in token_content
        assert "collapsed historical tool results" not in token_content

    @pytest.mark.asyncio
    async def test_cancel_during_strategy_4_summary_emits_cancelled_not_error(self) -> None:
        """Cancel during Strategy 4 LLM summary emits `cancelled`, NOT `recovery failed` error.

        Regression for the #1445 senior-review blocker: previously, a
        cancel during the final reactive compaction made
        ai_service.complete() return None, which compact_messages()
        mapped to a success=False CompactionResult, which Strategy 4
        treated as ordinary failure and fell through to the terminal
        "Recovery failed after all strategies" error. The loop must
        distinguish cancel from real compaction failure.
        """
        import asyncio

        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"code": "context_length_exceeded", "retryable": False}},
        ]
        ai = _mock_ai_service(context_error_events)

        cancel_event = asyncio.Event()

        async def _cancel_then_return_none(
            *_args: Any, cancel_event: asyncio.Event | None = None, **_kwargs: Any
        ) -> str | None:
            # Simulate the race-against-cancel behavior in
            # AIService.complete() — when cancel fires, the provider task
            # is cancelled and the method returns None.
            if cancel_event is not None and cancel_event.is_set():
                return None
            return None

        ai.complete = _cancel_then_return_none

        # History with only user+assistant messages — forces the reactive
        # ladder to skip Strategies 1, 2, 3 (nothing to trim/collapse/drop)
        # and fall through to Strategy 4, where the cancel check fires.
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "m1"},
            {"role": "assistant", "content": "r1"},
            {"role": "user", "content": "m2"},
            {"role": "assistant", "content": "r2"},
        ]

        cancel_event.set()
        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                cancel_event=cancel_event,
                reactive_max_attempts=1,
            )
        )

        # A `cancelled` event must surface with the cancel reason.
        cancelled = [e for e in events if e.kind == "cancelled"]
        assert len(cancelled) == 1
        assert cancelled[0].data.get("reason") == "user_cancel_during_recovery"

        # The terminal "Recovery failed after all strategies" error must
        # NOT appear — that's the bug the senior review flagged.
        errors = [e for e in events if e.kind == "error"]
        for err in errors:
            msg = err.data.get("message", "")
            assert "Recovery failed after all strategies" not in msg, (
                f"User cancel during Strategy 4 incorrectly emitted recovery-failed error: {msg!r}"
            )

    @pytest.mark.asyncio
    async def test_strategy_4_genuine_failure_still_emits_recovery_failed(self) -> None:
        """When complete() fails for non-cancel reasons, recovery-failed error still fires.

        Ensures the cancel-check added for #1445 doesn't swallow genuine
        compaction failures. cancel_event is None (or not set), so the
        terminal error must surface.
        """
        context_error_events: list[dict[str, Any]] = [
            {"event": "error", "data": {"code": "context_length_exceeded", "retryable": False}},
        ]
        ai = _mock_ai_service(context_error_events)
        # Genuine failure — complete returns None but no cancel involved.
        ai.complete = AsyncMock(return_value=None)

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": "m1"},
            {"role": "assistant", "content": "r1"},
            {"role": "user", "content": "m2"},
            {"role": "assistant", "content": "r2"},
        ]

        events = await _collect(
            run_agent_loop(
                ai_service=ai,
                messages=messages,
                tool_executor=_executor,
                tools_openai=None,
                reactive_max_attempts=1,
            )
        )

        errors = [e for e in events if e.kind == "error"]
        assert any("Recovery failed" in e.data.get("message", "") for e in errors), (
            "Genuine compaction failure must still surface recovery-failed error"
        )
        phases = [e.data for e in events if e.kind == "phase" and e.data.get("phase") == "compacting"]
        assert phases
        assert phases[0]["reason"] == "context_error_recovery"

        # No `cancelled` event — this is a real failure, not a cancel.
        assert not any(e.kind == "cancelled" for e in events)


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
