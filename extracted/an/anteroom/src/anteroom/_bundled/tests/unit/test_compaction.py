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
    RehydrationState,
    _identify_turn_groups,
    _strip_session_state,
    build_compaction_history,
    collapse_old_tool_results,
    compact_messages,
    drop_old_turn_groups,
    extract_rehydration_state,
    format_rehydration_block,
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


# ---------------------------------------------------------------------------
# Staged overflow recovery helpers (#1415)
# ---------------------------------------------------------------------------


def _tool_call_msg(call_id: str, name: str = "bash", args: str = "{}") -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [{"id": call_id, "function": {"name": name, "arguments": args}, "type": "function"}],
    }


def _tool_result(call_id: str, content: str = '{"ok": true}') -> dict[str, Any]:
    return {"role": "tool", "tool_call_id": call_id, "content": content}


def _validate_message_sequence(messages: list[dict[str, Any]]) -> None:
    """Assert every tool-role message has a matching assistant tool_call earlier."""
    known_ids: set[str] = set()
    for msg in messages:
        for tc in msg.get("tool_calls") or []:
            tcid = tc.get("id")
            if tcid:
                known_ids.add(tcid)
        if msg.get("role") == "tool":
            assert msg.get("tool_call_id") in known_ids, (
                f"Orphaned tool result {msg.get('tool_call_id')!r} — no matching assistant tool_call earlier"
            )


# --- Turn group identification (tests 1-3) ---


def test_turn_group_identification_simple() -> None:
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
        {"role": "user", "content": "again"},
    ]
    groups = _identify_turn_groups(messages)
    assert groups == [(0, 1), (1, 2), (2, 3)]


def test_turn_group_identification_with_tool_calls() -> None:
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "q"},
        _tool_call_msg("tc1"),
        _tool_result("tc1"),
        _tool_result("tc1"),
        {"role": "user", "content": "next"},
    ]
    # Note: two tool results with same call_id is degenerate but we'd
    # still group them together with the parent assistant.
    # Use distinct IDs to match the spec (user, assistant+2 tools = 1 group).
    messages = [
        {"role": "user", "content": "q"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"id": "tc1", "function": {"name": "bash", "arguments": "{}"}, "type": "function"},
                {"id": "tc2", "function": {"name": "grep", "arguments": "{}"}, "type": "function"},
            ],
        },
        _tool_result("tc1"),
        _tool_result("tc2"),
        {"role": "user", "content": "next"},
    ]
    groups = _identify_turn_groups(messages)
    # user=1 group, assistant+tc1+tc2=1 group, user=1 group
    assert groups == [(0, 1), (1, 4), (4, 5)]


def test_turn_group_never_orphans_tool_results() -> None:
    """The parent assistant and all its tool results are in the same group —
    no boundary ever splits them.
    """
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "q"},
        _tool_call_msg("tc1"),
        _tool_result("tc1"),
        {"role": "user", "content": "next"},
    ]
    groups = _identify_turn_groups(messages)
    # Every group should be internally consistent: if a tool-role message
    # is in the group, the parent assistant with the matching tool_call is
    # also in that same group.
    for start, end in groups:
        sub = messages[start:end]
        known_ids: set[str] = set()
        for msg in sub:
            for tc in msg.get("tool_calls") or []:
                if tc.get("id"):
                    known_ids.add(tc["id"])
        for msg in sub:
            if msg.get("role") == "tool":
                assert msg.get("tool_call_id") in known_ids


# --- collapse_old_tool_results (tests 4-6) ---


def test_collapse_old_tool_results_shrinks_history() -> None:
    large_payload = '{"stdout": "' + ("x" * 5000) + '"}'
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "q1"},
        _tool_call_msg("tc1"),
        _tool_result("tc1", content=large_payload),
        {"role": "user", "content": "q2"},
        _tool_call_msg("tc2"),
        _tool_result("tc2", content=large_payload),
        {"role": "user", "content": "q3"},
        _tool_call_msg("tc3"),
        _tool_result("tc3", content=large_payload),
    ]
    changed = collapse_old_tool_results(messages, keep_recent_groups=2, compact_chars=200)
    assert changed is True
    # Recent group's tool result should be intact (last 2 groups: q3, asst+tc3).
    # tc1 and tc2 are in older groups and should have been compacted.
    assert len(messages[2]["content"]) <= 500  # compacted
    assert len(messages[5]["content"]) <= 500  # compacted
    # tc3 preserved (keep_recent_groups=2 → [q3] and [asst+tc3]).
    assert messages[8]["content"] == large_payload


def test_collapse_old_tool_results_keeps_recent_groups() -> None:
    """``keep_recent_groups`` counts turn groups, not messages."""
    large_payload = '{"stdout": "' + ("x" * 5000) + '"}'
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "q1"},
        _tool_call_msg("tc1"),
        _tool_result("tc1", content=large_payload),
        {"role": "user", "content": "q2"},
        _tool_call_msg("tc2"),
        _tool_result("tc2", content=large_payload),
    ]
    # With 4 groups and keep_recent_groups=4, nothing should change.
    changed = collapse_old_tool_results(messages, keep_recent_groups=4, compact_chars=200)
    assert changed is False
    assert messages[2]["content"] == large_payload
    assert messages[5]["content"] == large_payload


def test_collapse_old_tool_results_returns_false_when_no_tools() -> None:
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": f"m{i}"} if i % 2 == 0 else {"role": "assistant", "content": f"r{i}"}
        for i in range(10)
    ]
    changed = collapse_old_tool_results(messages, keep_recent_groups=2, compact_chars=200)
    assert changed is False


# --- drop_old_turn_groups (tests 7-12) ---


def test_drop_old_turn_groups_preserves_recent() -> None:
    messages: list[dict[str, Any]] = []
    # Build 10 user/assistant turn groups (20 messages).
    for i in range(10):
        messages.append({"role": "user", "content": f"u{i}"})
        messages.append({"role": "assistant", "content": f"a{i}"})
    changed = drop_old_turn_groups(messages, keep_recent_groups=4)
    assert changed is True
    # First message should be the summary (role=user, compact_summary metadata).
    assert messages[0]["role"] == "user"
    assert messages[0].get("metadata", {}).get("compact_summary") is True
    # Boundary marker comes next when a tail is preserved.
    assert messages[1].get("metadata", {}).get("compact_boundary") is True
    # Preserved tail should start with a user message (provider-safe).
    assert messages[2]["role"] == "user"


def test_drop_old_turn_groups_preserves_system_messages() -> None:
    """When boundary walk-back lands past the system header, the system
    message is folded into the summarised head — provider-safe ordering
    requires the preserved tail to start with a user turn.
    """
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": "sys header"},
    ]
    for i in range(10):
        messages.append({"role": "user", "content": f"u{i}"})
        messages.append({"role": "assistant", "content": f"a{i}"})
    changed = drop_old_turn_groups(messages, keep_recent_groups=4)
    assert changed is True
    # The preserved tail must start with role=user.
    assert messages[2]["role"] == "user"


def test_drop_old_turn_groups_never_orphans_tool_results() -> None:
    messages: list[dict[str, Any]] = []
    for i in range(8):
        messages.append({"role": "user", "content": f"u{i}"})
        messages.append(_tool_call_msg(f"tc{i}"))
        messages.append(_tool_result(f"tc{i}", content='{"ok":true}'))
    changed = drop_old_turn_groups(messages, keep_recent_groups=4)
    assert changed is True
    _validate_message_sequence(messages)


def test_drop_old_turn_groups_returns_false_when_few_groups() -> None:
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "u1"},
        {"role": "assistant", "content": "a1"},
    ]
    changed = drop_old_turn_groups(messages, keep_recent_groups=4)
    assert changed is False


def test_drop_old_turn_groups_produces_valid_message_sequence() -> None:
    messages: list[dict[str, Any]] = []
    for i in range(6):
        messages.append({"role": "user", "content": f"u{i}"})
        messages.append(_tool_call_msg(f"tc{i}"))
        messages.append(_tool_result(f"tc{i}"))
    assert drop_old_turn_groups(messages, keep_recent_groups=4) is True
    _validate_message_sequence(messages)
    # The first tool_call_id referenced by any preserved tool result must
    # be defined by an assistant message preceding it.
    for idx, msg in enumerate(messages):
        if msg.get("role") == "tool":
            found = False
            tcid = msg.get("tool_call_id")
            for prev in messages[:idx]:
                for tc in prev.get("tool_calls") or []:
                    if tc.get("id") == tcid:
                        found = True
                        break
                if found:
                    break
            assert found


def test_drop_old_turn_groups_reuses_compaction_format() -> None:
    """Summary message must match compact_messages() output shape
    (#1412/#1413 contract): role=user, AGENT_LOOP_CONTENT_TEMPLATE content,
    and the four metadata keys.
    """
    messages: list[dict[str, Any]] = []
    for i in range(10):
        messages.append({"role": "user", "content": f"u{i}"})
        messages.append({"role": "assistant", "content": f"a{i}"})
    assert drop_old_turn_groups(messages, keep_recent_groups=4) is True
    summary = messages[0]
    assert summary["role"] == "user"
    meta = summary.get("metadata") or {}
    assert meta.get("compact_summary") is True
    assert "original_count" in meta
    assert "original_tokens" in meta
    assert "summary_tokens" in meta
    # The AGENT_LOOP_CONTENT_TEMPLATE prefix must be present.
    assert "[Previous conversation summary (auto-compacted from" in summary["content"]
    assert "Please continue from where we left off." in summary["content"]


def test_drop_old_turn_groups_original_tokens_describe_full_input() -> None:
    """``metadata["original_tokens"]`` must describe the full pre-mutation
    input, not just the summarised head.

    Regression: the initial implementation used ``count_message_tokens(head)``
    which under-reported tokens and broke the uniform metadata contract with
    ``compact_messages()``.  Downstream consumers that use
    ``metadata["original_tokens"]`` to drive UX (token bars, compaction
    badges) must see the same semantics regardless of whether the summary
    came from the staged recovery path or the full LLM compaction path.
    """
    from anteroom.services.token_estimator import count_message_tokens

    messages: list[dict[str, Any]] = []
    # 10 turn groups of user+assistant, with enough text that token counts
    # differ between head and full when we drop half.
    for i in range(10):
        messages.append({"role": "user", "content": f"user turn {i} " + "x " * 40})
        messages.append({"role": "assistant", "content": f"assistant turn {i} " + "y " * 40})
    full_tokens = count_message_tokens(messages)
    full_count = len(messages)

    assert drop_old_turn_groups(messages, keep_recent_groups=4) is True

    summary = messages[0]
    meta = summary.get("metadata") or {}
    # The full-input token count must be preserved in metadata so downstream
    # consumers see the same semantics as compact_messages() summaries.
    assert meta["original_tokens"] == full_tokens, (
        f"Expected full-input tokens ({full_tokens}), got {meta['original_tokens']}"
    )
    # ``original_count`` follows compact_messages()'s split convention:
    # the count of messages the summary REPLACED, not the full input.
    assert meta["original_count"] < full_count, (
        "original_count should describe the summarised head (replaced messages), not the full pre-mutation input"
    )


# -- Rehydration (#1414) --


def _rh_tool_call(tool_id: str, name: str, args: dict[str, Any]) -> dict[str, Any]:
    """Build an assistant message carrying one tool_call (rehydration tests).

    Separate from :func:`_tool_call_msg` so the two test suites
    (#1414 rehydration and #1415 staged recovery) don't collide on helper
    names — their call shapes are deliberately different (``args`` dict vs
    raw JSON string, plus matching result-helper shapes).
    """
    import json as _json

    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "id": tool_id,
                "function": {"name": name, "arguments": _json.dumps(args)},
            }
        ],
    }


def _rh_tool_result(tool_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Build a tool-role result message (rehydration tests)."""
    import json as _json

    return {"role": "tool", "tool_call_id": tool_id, "content": _json.dumps(payload)}


def test_extract_rehydration_state_file_paths() -> None:
    """Files from read_file / write_file / edit_file land in the right buckets."""
    messages = [
        _rh_tool_call("c1", "read_file", {"path": "src/foo.py"}),
        _rh_tool_result("c1", {"text": "..."}),
        _rh_tool_call("c2", "write_file", {"path": "src/bar.py", "content": "x"}),
        _rh_tool_result("c2", {"ok": True}),
        _rh_tool_call("c3", "edit_file", {"file_path": "src/baz.py"}),
        _rh_tool_result("c3", {"ok": True}),
    ]
    state = extract_rehydration_state(messages)
    assert state.files_read == ("src/foo.py",)
    assert state.files_written == ("src/bar.py",)
    assert state.files_edited == ("src/baz.py",)
    assert state.last_working_dir is None
    assert state.errors_unresolved == ()


def test_extract_rehydration_state_bounded() -> None:
    """Each file category is capped, most recent kept."""
    messages: list[dict[str, Any]] = []
    for i in range(30):
        messages.append(_rh_tool_call(f"r{i}", "read_file", {"path": f"f{i}.py"}))
        messages.append(_rh_tool_result(f"r{i}", {"text": "x"}))
    state = extract_rehydration_state(messages, max_files=5)
    assert len(state.files_read) == 5
    # Most recent 5 entries: f25..f29
    assert state.files_read == ("f25.py", "f26.py", "f27.py", "f28.py", "f29.py")


def test_extract_rehydration_state_deduplicates() -> None:
    """Repeated paths collapse to a single entry."""
    messages = [
        _rh_tool_call("c1", "read_file", {"path": "a.py"}),
        _rh_tool_result("c1", {"text": "x"}),
        _rh_tool_call("c2", "read_file", {"path": "a.py"}),
        _rh_tool_result("c2", {"text": "x"}),
        _rh_tool_call("c3", "read_file", {"path": "b.py"}),
        _rh_tool_result("c3", {"text": "x"}),
    ]
    state = extract_rehydration_state(messages)
    assert state.files_read == ("a.py", "b.py")


def test_extract_rehydration_state_empty_conversation() -> None:
    """No tool calls → empty state; format yields empty string."""
    state = extract_rehydration_state([{"role": "user", "content": "hi"}])
    assert state.is_empty()
    assert format_rehydration_block(state) == ""


def test_extract_rehydration_state_unresolved_errors() -> None:
    """Tool errors without a later success are captured; retried ones are dropped."""
    messages = [
        # bash error that is NOT retried — remains unresolved.
        _rh_tool_call("c1", "bash", {"command": "python -m pytest"}),
        _rh_tool_result("c1", {"error": "ModuleNotFoundError: foo"}),
        # read_file error followed by a success on the same path — resolved.
        _rh_tool_call("c2", "read_file", {"path": "x.py"}),
        _rh_tool_result("c2", {"error": "not found"}),
        _rh_tool_call("c3", "read_file", {"path": "x.py"}),
        _rh_tool_result("c3", {"text": "..."}),
    ]
    state = extract_rehydration_state(messages)
    assert len(state.errors_unresolved) == 1
    assert "bash: ModuleNotFoundError: foo" in state.errors_unresolved[0]


def test_extract_rehydration_state_unresolved_errors_order_aware() -> None:
    """A LATER error after an earlier success must remain unresolved.

    Regression for the bug where a single ``resolved`` set was applied to all
    errors at the end — an earlier success silently resolved later errors for
    the same (tool_name, target) pair.  The fix: resolution is order-aware,
    only successes that precede an error can resolve it.
    """
    # Case 1: success THEN error — the later error must remain unresolved.
    messages = [
        _rh_tool_call("c1", "read_file", {"path": "a.py"}),
        _rh_tool_result("c1", {"text": "first read ok"}),
        _rh_tool_call("c2", "read_file", {"path": "a.py"}),
        _rh_tool_result("c2", {"error": "file vanished"}),
    ]
    state = extract_rehydration_state(messages)
    assert len(state.errors_unresolved) == 1
    assert "read_file: file vanished" in state.errors_unresolved[0]

    # Case 2: error → success → error (same target) — first resolved, second unresolved.
    messages = [
        _rh_tool_call("c1", "read_file", {"path": "a.py"}),
        _rh_tool_result("c1", {"error": "first error"}),
        _rh_tool_call("c2", "read_file", {"path": "a.py"}),
        _rh_tool_result("c2", {"text": "retry ok"}),
        _rh_tool_call("c3", "read_file", {"path": "a.py"}),
        _rh_tool_result("c3", {"error": "second error"}),
    ]
    state = extract_rehydration_state(messages)
    assert len(state.errors_unresolved) == 1
    assert "second error" in state.errors_unresolved[0]
    assert "first error" not in " ".join(state.errors_unresolved)

    # Case 3: bash — target is None, but order-awareness still applies.
    # A successful bash call resolves only prior bash errors, not later ones.
    messages = [
        _rh_tool_call("c1", "bash", {"command": "ls"}),
        _rh_tool_result("c1", {"stdout": "ok"}),
        _rh_tool_call("c2", "bash", {"command": "python -m pytest"}),
        _rh_tool_result("c2", {"error": "ModuleNotFoundError: bar"}),
    ]
    state = extract_rehydration_state(messages)
    assert len(state.errors_unresolved) == 1
    assert "ModuleNotFoundError: bar" in state.errors_unresolved[0]


def test_extract_rehydration_state_bash_errors_keyed_by_command_identity() -> None:
    """An UNRELATED later bash success must NOT clear an earlier bash error.

    Regression for the follow-up finding on #1414: when bash calls were keyed
    as ``("bash", None)``, any successful bash call (e.g. a later ``ls``)
    silently resolved earlier failed bash commands (e.g. ``pytest``), because
    they shared the same ``None`` target key.  The fix: bash calls derive a
    retry-resolution key from the leading command token (``pytest``,
    ``python:<module>`` for ``python -m …``, etc.).  A successful ``ls`` has a
    different identity than a failed ``pytest`` and must leave the pytest
    error unresolved.
    """
    # An earlier pytest error + a later unrelated ls success.  The ls success
    # must NOT resolve the pytest error.
    messages = [
        _rh_tool_call("c1", "bash", {"command": "pytest tests/foo"}),
        _rh_tool_result("c1", {"error": "collection error: no tests ran"}),
        _rh_tool_call("c2", "bash", {"command": "ls -la"}),
        _rh_tool_result("c2", {"stdout": "total 8\ndrwxr-xr-x  2 user  staff"}),
    ]
    state = extract_rehydration_state(messages)
    assert len(state.errors_unresolved) == 1, (
        f"Expected pytest error to remain unresolved, got {state.errors_unresolved!r}"
    )
    assert "collection error" in state.errors_unresolved[0]


def test_extract_rehydration_state_bash_retry_resolves_same_command() -> None:
    """Same leading command token → retry semantics apply → error resolves.

    A second ``pytest`` invocation (possibly with different args — e.g.
    ``--rerun`` or a narrower path) that succeeds is a legitimate retry of
    the earlier failed pytest command and should resolve the error.
    """
    messages = [
        _rh_tool_call("c1", "bash", {"command": "pytest tests/foo"}),
        _rh_tool_result("c1", {"error": "flake"}),
        _rh_tool_call("c2", "bash", {"command": "pytest tests/foo --rerun 1"}),
        _rh_tool_result("c2", {"stdout": "2 passed"}),
    ]
    state = extract_rehydration_state(messages)
    assert state.errors_unresolved == ()


def test_extract_rehydration_state_bash_python_m_modules_are_different_identities() -> None:
    """``python -m pytest`` and ``python -m mypy`` are separate retry identities.

    A successful ``python -m mypy`` must not resolve a failed
    ``python -m pytest``.  The key is ``python:<module>`` so the two invocations
    are treated as distinct operations.
    """
    messages = [
        _rh_tool_call("c1", "bash", {"command": "python -m pytest tests/unit/"}),
        _rh_tool_result("c1", {"error": "1 failed, 99 passed"}),
        _rh_tool_call("c2", "bash", {"command": "python -m mypy src/"}),
        _rh_tool_result("c2", {"stdout": "Success: no issues found"}),
    ]
    state = extract_rehydration_state(messages)
    assert len(state.errors_unresolved) == 1
    assert "1 failed" in state.errors_unresolved[0]


def test_extract_rehydration_state_bash_cd_prefix_stripped_for_retry_key() -> None:
    """``cd foo && pytest`` has the same retry identity as bare ``pytest``.

    A common pattern is prefixing commands with ``cd some/dir &&`` so they
    run in a different directory.  The retry key should identify the actual
    operation (``pytest``), not the directory change.
    """
    messages = [
        _rh_tool_call("c1", "bash", {"command": "cd /repo && pytest tests/"}),
        _rh_tool_result("c1", {"error": "import error"}),
        _rh_tool_call("c2", "bash", {"command": "pytest tests/ --no-cov"}),
        _rh_tool_result("c2", {"stdout": "10 passed"}),
    ]
    state = extract_rehydration_state(messages)
    assert state.errors_unresolved == ()


def test_extract_rehydration_state_working_dir() -> None:
    """``cd`` inside a bash command updates ``last_working_dir``; latest wins."""
    messages = [
        _rh_tool_call("c1", "bash", {"command": "cd /tmp/a && ls"}),
        _rh_tool_result("c1", {"stdout": ""}),
        _rh_tool_call("c2", "bash", {"command": "cd /tmp/b && pwd"}),
        _rh_tool_result("c2", {"stdout": "/tmp/b"}),
    ]
    state = extract_rehydration_state(messages)
    assert state.last_working_dir == "/tmp/b"


def test_format_rehydration_block_nonempty() -> None:
    """Formatter produces an XML-tagged block with only non-empty sections."""
    state = RehydrationState(
        files_read=("a.py", "b.py"),
        files_written=("c.py",),
        files_edited=(),
        last_working_dir="/repo",
        errors_unresolved=("bash: boom",),
    )
    block = format_rehydration_block(state)
    assert block.startswith("<session_state>")
    assert block.endswith("</session_state>")
    assert "Files read: a.py, b.py" in block
    assert "Files written: c.py" in block
    assert "Files edited:" not in block  # empty section omitted
    assert "Working dir: /repo" in block
    assert "Last errors: bash: boom" in block


def test_format_rehydration_block_empty() -> None:
    """An all-empty state yields no block at all."""
    assert format_rehydration_block(RehydrationState()) == ""


@pytest.mark.asyncio
async def test_rehydration_appended_to_summary() -> None:
    """The <session_state> block ends up inside the summary message content."""
    svc = _mock_ai_service("SUMMARY")
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "start"},
        _rh_tool_call("c1", "read_file", {"path": "src/foo.py"}),
        _rh_tool_result("c1", {"text": "..."}),
        _rh_tool_call("c2", "edit_file", {"path": "src/foo.py"}),
        _rh_tool_result("c2", {"ok": True}),
        {"role": "user", "content": "thanks"},
    ]
    await compact_messages(svc, messages)
    assert len(messages) == 1
    content = messages[0]["content"]
    assert "<session_state>" in content
    assert "Files read: src/foo.py" in content
    assert "Files edited: src/foo.py" in content


@pytest.mark.asyncio
async def test_rehydration_no_extra_messages() -> None:
    """Rehydration must not add any new messages to the list."""
    svc = _mock_ai_service("SUMMARY")
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "start"},
        _rh_tool_call("c1", "read_file", {"path": "a.py"}),
        _rh_tool_result("c1", {"text": "x"}),
        {"role": "user", "content": "keep going"},
    ]
    await compact_messages(svc, messages, preserve_tail=0)
    # Full-summary shape: exactly one summary message.
    assert len(messages) == 1


@pytest.mark.asyncio
async def test_rehydration_disabled_via_config() -> None:
    """rehydrate=False skips the append entirely."""
    svc = _mock_ai_service("SUMMARY")
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "start"},
        _rh_tool_call("c1", "read_file", {"path": "a.py"}),
        _rh_tool_result("c1", {"text": "x"}),
        {"role": "user", "content": "done"},
    ]
    await compact_messages(svc, messages, rehydrate=False)
    assert "<session_state>" not in messages[0]["content"]


def test_strip_session_state_removes_existing_block() -> None:
    """_strip_session_state removes a <session_state>...</session_state> block."""
    content = "Summary prose.\n\n<session_state>\nFiles read: a.py\n</session_state>"
    stripped = _strip_session_state(content)
    assert "<session_state>" not in stripped
    assert "Summary prose." in stripped


def test_strip_session_state_preserves_other_content() -> None:
    """Content that does not contain a session_state block is untouched."""
    content = "A summary with <other_tag>content</other_tag>."
    # rstrip on the regex substitution leaves the non-matching content as-is.
    assert _strip_session_state(content).startswith("A summary with <other_tag>")


@pytest.mark.asyncio
async def test_recompaction_strips_old_state() -> None:
    """Second compaction must produce a fresh, non-nested <session_state>."""
    svc = _mock_ai_service("SUMMARY2")
    # First compaction output: summary already has a <session_state> block.
    prior_summary = (
        "[Previous conversation summary (auto-compacted from 4 messages)]\n\n"
        "SUMMARY1\n\nPlease continue from where we left off.\n\n"
        "<session_state>\nFiles read: old.py\n</session_state>"
    )
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": prior_summary, "metadata": {"compact_summary": True}},
        _rh_tool_call("c1", "read_file", {"path": "new.py"}),
        _rh_tool_result("c1", {"text": "x"}),
        {"role": "user", "content": "next"},
    ]
    await compact_messages(svc, messages)
    assert len(messages) == 1
    content = messages[0]["content"]
    # Exactly one <session_state> block in the output (no nesting).
    assert content.count("<session_state>") == 1
    assert content.count("</session_state>") == 1
    # Fresh state reflects the *current* tool calls, not the stale `old.py`.
    assert "Files read: new.py" in content
    assert "old.py" not in content


def test_recompaction_history_excludes_old_state() -> None:
    """build_compaction_history strips <session_state> from input messages."""
    messages = [
        {
            "role": "user",
            "content": "Some prose.\n\n<session_state>\nFiles read: leak.py\n</session_state>",
        },
    ]
    history = build_compaction_history(messages)
    assert "leak.py" not in history
    assert "<session_state>" not in history
    assert "Some prose." in history


@pytest.mark.asyncio
async def test_compact_messages_cancel_during_llm() -> None:
    """cancel_event propagates to ai_service.complete (#1266).

    The shared compaction service must pass the cancel_event kwarg
    through to the provider call so a user pressing Escape during a
    long summary compaction aborts cleanly instead of hanging on the
    LLM response.
    """
    import asyncio

    received_kwargs: dict[str, Any] = {}

    async def _capture_complete(*args: Any, **kwargs: Any) -> str | None:
        received_kwargs.update(kwargs)
        return "summary"

    svc = AsyncMock()
    svc.complete = _capture_complete

    messages = _msgs(6)
    cancel = asyncio.Event()
    await compact_messages(svc, messages, cancel_event=cancel)

    assert "cancel_event" in received_kwargs
    assert received_kwargs["cancel_event"] is cancel


@pytest.mark.asyncio
async def test_compact_messages_cancel_default_none_is_backward_compatible() -> None:
    """Callers that don't pass cancel_event still get it as None (#1266)."""
    received_kwargs: dict[str, Any] = {}

    async def _capture_complete(*args: Any, **kwargs: Any) -> str | None:
        received_kwargs.update(kwargs)
        return "summary"

    svc = AsyncMock()
    svc.complete = _capture_complete

    messages = _msgs(6)
    await compact_messages(svc, messages)

    assert received_kwargs.get("cancel_event") is None
