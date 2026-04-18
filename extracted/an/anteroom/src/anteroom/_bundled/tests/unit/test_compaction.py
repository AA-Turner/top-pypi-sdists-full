"""Tests for the shared compaction service (#1412)."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.services.agent_loop import _compact_messages as _agent_loop_compact
from anteroom.services.compaction import (
    AGENT_LOOP_CONTENT_TEMPLATE,
    COMPACTION_MIN_MESSAGES,
    REPL_CONTENT_TEMPLATE,
    CompactionResult,
    build_compaction_history,
    compact_messages,
)


def _msgs(n: int) -> list[dict[str, Any]]:
    """Build a realistic conversation message list of length n."""
    out: list[dict[str, Any]] = []
    for i in range(n):
        if i % 2 == 0:
            out.append({"role": "user", "content": f"user message {i}"})
        else:
            out.append({"role": "assistant", "content": f"assistant reply {i}"})
    return out


def _mock_ai_service(summary_text: str = "compacted summary") -> Any:
    """Build a mock AIService whose .complete() returns summary_text."""
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value=summary_text)
    return svc


@pytest.mark.asyncio
async def test_compact_messages_success_user_role_matches_agent_loop_shape() -> None:
    """Agent-loop caller path: role=user + AGENT_LOOP_CONTENT_TEMPLATE produces the
    exact compacted shape that agent_loop.py shipped before the refactor.
    """
    svc = _mock_ai_service(summary_text="SUMMARY-A")
    messages = _msgs(10)

    result = await compact_messages(
        svc,
        messages,
        role="user",
        content_template=AGENT_LOOP_CONTENT_TEMPLATE,
    )

    assert result.success is True
    assert result.original_count == 10
    assert result.summary == "SUMMARY-A"
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert "[Previous conversation summary (auto-compacted from 10 messages)]" in messages[0]["content"]
    assert "SUMMARY-A" in messages[0]["content"]
    assert "Please continue from where we left off." in messages[0]["content"]


@pytest.mark.asyncio
async def test_compact_messages_success_system_role_matches_repl_shape() -> None:
    """CLI /compact caller path: role=system + REPL_CONTENT_TEMPLATE produces the
    exact compacted shape that repl.py shipped before the refactor, including
    the "~X tokens" token count.
    """
    svc = _mock_ai_service(summary_text="SUMMARY-B")
    messages = _msgs(10)

    result = await compact_messages(
        svc,
        messages,
        role="system",
        content_template=REPL_CONTENT_TEMPLATE,
    )

    assert result.success is True
    assert result.original_count == 10
    assert result.original_tokens > 0
    assert result.summary == "SUMMARY-B"
    assert len(messages) == 1
    assert messages[0]["role"] == "system"
    assert "Previous conversation summary" in messages[0]["content"]
    assert "auto-compacted from 10 messages" in messages[0]["content"]
    assert "tokens):" in messages[0]["content"]
    assert "SUMMARY-B" in messages[0]["content"]


@pytest.mark.asyncio
async def test_compact_messages_too_few_returns_failure_and_leaves_messages() -> None:
    svc = _mock_ai_service()
    messages = _msgs(COMPACTION_MIN_MESSAGES - 1)
    snapshot = list(messages)

    result = await compact_messages(svc, messages)

    assert result.success is False
    assert result.original_count == COMPACTION_MIN_MESSAGES - 1
    assert messages == snapshot
    svc.complete.assert_not_awaited()


@pytest.mark.asyncio
async def test_compact_messages_llm_exception_returns_failure_and_leaves_messages() -> None:
    svc = AsyncMock()
    svc.complete = AsyncMock(side_effect=RuntimeError("boom"))
    messages = _msgs(10)
    snapshot = list(messages)

    result = await compact_messages(svc, messages)

    assert result.success is False
    assert result.summary == ""
    assert messages == snapshot


@pytest.mark.asyncio
async def test_compact_messages_uses_ai_service_complete_not_client_bypass() -> None:
    """repl.py previously called ai_service.client.chat.completions.create
    directly. The shared service must use ai_service.complete() — the
    proper service-layer abstraction.
    """
    svc = _mock_ai_service()
    # Expose a client attribute but make its completion path raise if used.
    svc.client = AsyncMock()
    svc.client.chat = AsyncMock()
    svc.client.chat.completions = AsyncMock()
    svc.client.chat.completions.create = AsyncMock(side_effect=AssertionError("must not bypass the service layer"))
    messages = _msgs(10)

    result = await compact_messages(svc, messages)

    assert result.success is True
    svc.complete.assert_awaited_once()
    svc.client.chat.completions.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_compact_messages_replaces_history_with_single_message() -> None:
    svc = _mock_ai_service()
    messages = _msgs(12)

    await compact_messages(svc, messages)

    assert len(messages) == 1


@pytest.mark.asyncio
async def test_compact_messages_complete_returns_none_is_failure_leaves_messages() -> None:
    """Regression for senior review on #1412.

    ``AIService.complete()`` swallows provider errors (AuthenticationError,
    network, rate limit, empty response) and returns ``None``.  Before the
    shared-service refactor, the CLI ``/compact`` path used
    ``client.chat.completions.create()`` directly, which raises on those
    errors — the old handler rendered an error and left ``ai_messages``
    untouched.  The shared service must preserve that contract rather than
    collapsing the conversation into fallback text.
    """
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value=None)
    messages = _msgs(10)
    snapshot = list(messages)

    result = await compact_messages(
        svc,
        messages,
        role="system",
        content_template=REPL_CONTENT_TEMPLATE,
    )

    assert result.success is False
    assert result.summary == ""
    assert messages == snapshot, "history must be left untouched on complete() -> None"


@pytest.mark.asyncio
async def test_compact_messages_complete_returns_empty_string_is_failure_leaves_messages() -> None:
    """Empty-string response from ``complete()`` is also a failure — do not
    collapse history into a zero-content summary.
    """
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value="")
    messages = _msgs(10)
    snapshot = list(messages)

    result = await compact_messages(svc, messages)

    assert result.success is False
    assert messages == snapshot


@pytest.mark.asyncio
async def test_compact_messages_agent_loop_path_also_treats_none_as_failure() -> None:
    """The agent-loop (``role="user"``) path receives the same failure
    semantics: ``None`` from ``complete()`` must leave history untouched.
    The agent loop's ``_compact_messages`` wrapper returns ``False`` in
    that case and the caller falls through to its "recovery failed" path,
    which is a cleaner outcome than the previous silent fallback-text
    collapse.
    """
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value=None)
    messages = _msgs(10)
    snapshot = list(messages)

    result = await compact_messages(
        svc,
        messages,
        role="user",
        content_template=AGENT_LOOP_CONTENT_TEMPLATE,
    )

    assert result.success is False
    assert messages == snapshot


@pytest.mark.asyncio
async def test_agent_loop_compact_wrapper_returns_false_on_complete_none() -> None:
    """End-to-end through the agent_loop wrapper: ``complete() -> None``
    must propagate as ``False`` so the caller surfaces its recovery-failed
    error path instead of silently collapsing history.
    """
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value=None)
    messages = _msgs(10)
    snapshot = list(messages)

    ok = await _agent_loop_compact(svc, messages)

    assert ok is False
    assert messages == snapshot


@pytest.mark.asyncio
async def test_compact_messages_returns_result_dataclass_with_metadata() -> None:
    svc = _mock_ai_service(summary_text="X")
    messages = _msgs(10)

    result = await compact_messages(svc, messages)

    assert isinstance(result, CompactionResult)
    assert result.success is True
    assert result.original_count == 10
    assert result.summary == "X"
    # Frozen dataclass: attempting to mutate should fail.
    with pytest.raises(Exception):
        result.success = False  # type: ignore[misc]


# -- build_compaction_history --


def test_build_compaction_history_empty() -> None:
    assert build_compaction_history([]) == ""


def test_build_compaction_history_includes_roles_and_content() -> None:
    messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
    ]
    out = build_compaction_history(messages)
    assert "user: hello" in out
    assert "assistant: hi" in out


def test_build_compaction_history_truncates_long_content() -> None:
    messages = [{"role": "user", "content": "x" * 600}]
    out = build_compaction_history(messages)
    assert "..." in out
    # Should not include the full 600-char payload verbatim.
    assert "x" * 600 not in out


def test_build_compaction_history_tool_call_and_result_success() -> None:
    messages = [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "read_file", "arguments": '{"path": "a.py"}'},
                }
            ],
        },
        {"role": "tool", "tool_call_id": "call_1", "content": '{"text": "hello"}'},
    ]
    out = build_compaction_history(messages)
    assert "tool_call: read_file" in out
    assert "tool_result: read_file" in out
    assert "SUCCESS" in out


def test_build_compaction_history_tool_result_error() -> None:
    messages = [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [{"id": "call_1", "function": {"name": "bash", "arguments": "{}"}}],
        },
        {
            "role": "tool",
            "tool_call_id": "call_1",
            "content": '{"error": "permission denied"}',
        },
    ]
    out = build_compaction_history(messages)
    assert "tool_result: bash -> ERROR" in out
    assert "permission denied" in out


def test_build_compaction_history_tool_result_unknown_tool_id() -> None:
    messages = [{"role": "tool", "tool_call_id": "missing", "content": '{"ok": true}'}]
    out = build_compaction_history(messages)
    assert "tool_result: unknown" in out


def test_build_compaction_history_tool_call_bad_args_json() -> None:
    messages = [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [{"id": "c1", "function": {"name": "grep", "arguments": "not-json"}}],
        }
    ]
    out = build_compaction_history(messages)
    assert "tool_call: grep(" in out
