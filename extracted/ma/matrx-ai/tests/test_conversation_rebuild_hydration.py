"""Regression guard for tool-result hydration in conversation rebuild.

The model-visible history is reconstructed from cx_message + cx_tool_call on
every /resume (and any DB load). Persisted role='tool' messages carry only
POINTER blocks (output_chars / output_preview, no actual output) — the real
output lives on cx_tool_call.output and MUST be joined back in by
``rebuild_conversation_messages``. If that join silently fails (e.g. an id
type mismatch between the message ids and cx_tool_call.message_id), the model
replays EMPTY tool results, never "sees" what its tools returned, and re-calls
the same tool until the duplicate-call guard kills the loop — the observed
failure shape of the 2026-06-09 matrx-extend incident (conversation
417e64ce-74ff-4fcd-b976-df1f0df56671).
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db._registry import configure_db

# conversation_rebuild resolves CxMessage/CxToolCall/CxMedia from the registry
# at import time. Register inert stand-ins BEFORE importing it — the module
# only uses them as type references, never constructs them.
configure_db(
    models={
        "CxMessage": SimpleNamespace,
        "CxToolCall": SimpleNamespace,
        "CxMedia": SimpleNamespace,
    }
)

from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages  # noqa: E402

MSG_USER = "11111111-1111-1111-1111-111111111111"
MSG_ASSISTANT = "22222222-2222-2222-2222-222222222222"
MSG_TOOL = "33333333-3333-3333-3333-333333333333"


def _msg(
    *,
    id: Any,
    role: str,
    position: int,
    content: list[dict[str, Any]] | None = None,
    visible: bool = True,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        role=role,
        position=position,
        content=content or [],
        created_at=None,
        status="active",
        metadata={},
        deleted_at=None,
        is_visible_to_model=visible,
    )


def _tool_call(
    *,
    call_id: str,
    message_id: Any,
    output: str,
    status: str = "completed",
    is_error: bool = False,
    error_type: str | None = None,
    error_message: str | None = None,
    tool_name: str = "tabs",
    row_id: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=row_id,
        call_id=call_id,
        message_id=message_id,
        tool_name=tool_name,
        output=output,
        is_error=is_error,
        status=status,
        output_chars=len(output),
        output_preview=None,
        error_type=error_type,
        error_message=error_message,
        deleted_at=None,
    )


def _tool_results_of(messages: list[Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for m in messages:
        role = m.role.value if hasattr(m.role, "value") else m.role
        if role != "tool":
            continue
        for c in m.content:
            block = c if isinstance(c, dict) else c.to_storage_dict()
            if block.get("type") == "tool_result":
                blocks.append(block)
    return blocks


@pytest.mark.asyncio
async def test_persisted_tool_message_hydrates_real_output() -> None:
    """A persisted role='tool' pointer-stub message must come back carrying
    the REAL cx_tool_call.output, not the stub."""
    output = '{"count": 71, "tabs": [{"id": 1, "url": "https://example.com"}]}'
    messages = [
        _msg(id=MSG_USER, role="user", position=0,
             content=[{"type": "text", "text": "list my tabs"}]),
        _msg(id=MSG_ASSISTANT, role="assistant", position=1,
             content=[{"type": "tool_call", "call_id": "call-1", "name": "tabs"}]),
        # Pointer stub — exactly what persistence writes (output_chars only).
        _msg(id=MSG_TOOL, role="tool", position=2,
             content=[{"type": "tool_result", "call_id": "call-1",
                       "tool_use_id": "call-1", "name": "tabs",
                       "output_chars": 0}]),
    ]
    tool_calls = [_tool_call(call_id="call-1", message_id=MSG_TOOL, output=output)]

    rebuilt = await rebuild_conversation_messages(messages, tool_calls, [])

    results = _tool_results_of(rebuilt)
    assert len(results) == 1, f"expected one tool_result, got: {results}"
    assert results[0].get("content") == output, (
        "tool_result content must be the real cx_tool_call.output — an empty "
        "result here means the model replays blind history and re-calls the "
        "same tool (the 2026-06-09 incident shape)"
    )


@pytest.mark.asyncio
async def test_uuid_typed_ids_still_hydrate() -> None:
    """The join must survive uuid.UUID-typed ids on either side — a silent
    type mismatch here degrades to empty tool results with no error."""
    output = '{"ok": true}'
    tool_msg_id = uuid.UUID(MSG_TOOL)
    messages = [
        _msg(id=uuid.UUID(MSG_ASSISTANT), role="assistant", position=0,
             content=[{"type": "tool_call", "call_id": "call-1", "name": "tabs"}]),
        _msg(id=tool_msg_id, role="tool", position=1,
             content=[{"type": "tool_result", "call_id": "call-1",
                       "tool_use_id": "call-1", "name": "tabs",
                       "output_chars": 0}]),
    ]
    tool_calls = [_tool_call(call_id="call-1", message_id=str(tool_msg_id), output=output)]

    rebuilt = await rebuild_conversation_messages(messages, tool_calls, [])

    results = _tool_results_of(rebuilt)
    assert len(results) == 1
    assert results[0].get("content") == output


@pytest.mark.asyncio
async def test_suspended_round_trip_synthesizes_tool_result() -> None:
    """The delegate/suspend/resume shape: the assistant message carries the
    tool_use, the loop suspended before any role='tool' message was written,
    and the client's result lives only on cx_tool_call. Rebuild must
    synthesize the pairing tool message or sanitize drops the round trip."""
    output = '{"id": 42, "title": "Pioneer AI"}'
    messages = [
        _msg(id=MSG_USER, role="user", position=0,
             content=[{"type": "text", "text": "what tab am I on?"}]),
        _msg(id=MSG_ASSISTANT, role="assistant", position=1,
             content=[{"type": "tool_call", "call_id": "call-9", "name": "tabs"}]),
    ]
    # Result resolved via POST /tool_results — message_id still points at the
    # assistant message (set at log time; no tool message row exists yet).
    tool_calls = [_tool_call(call_id="call-9", message_id=MSG_ASSISTANT, output=output)]

    rebuilt = await rebuild_conversation_messages(messages, tool_calls, [])

    results = _tool_results_of(rebuilt)
    assert len(results) == 1, (
        "rebuild must synthesize a tool message for the suspended round trip "
        f"(got {len(results)} tool_results)"
    )
    assert results[0].get("content") == output
    # And it must not double-emit: exactly one tool_result for call-9.
    assert sum(1 for r in results if r.get("call_id") == "call-9") == 1


@pytest.mark.asyncio
async def test_null_message_id_does_not_duplicate_tool_result() -> None:
    """The 2026-06-22 duplicate-tool_result 400 (conversation bcc588b6-...).

    A watchdog-timed-out ``research_web`` tool's cx_tool_call row was persisted
    with ``message_id = NULL``. The persisted role='tool' message still carries
    a tool_result pointer for that call_id. A naive rebuild keys its pairing
    guard off ``message_id`` only, fails to see the message as 'already paired',
    and the synthetic path emits a SECOND tool_result for the same id — two
    tool_result blocks with one tool_use_id, which Anthropic 400s
    ('each tool_use must have a single result').

    Rebuild must emit EXACTLY ONE tool_result for that id — rebuilt from the
    authoritative cx_tool_call row, not the empty pointer stub.
    """
    messages = [
        _msg(id=MSG_ASSISTANT, role="assistant", position=0,
             content=[{"type": "tool_call", "call_id": "call-x",
                       "name": "research_web"}]),
        # Persisted pointer stub for the same call (output_chars 0, no output).
        _msg(id=MSG_TOOL, role="tool", position=1,
             content=[{"type": "tool_result", "call_id": "call-x",
                       "tool_use_id": "call-x", "name": "research_web",
                       "is_error": False, "output_chars": 0}]),
    ]
    # The row finalized as a watchdog error AFTER the pointer message — and its
    # message_id link was never back-filled (NULL).
    tool_calls = [
        _tool_call(call_id="call-x", message_id=None, output="", status="error",
                   is_error=True, error_type="watchdog_timeout",
                   error_message="Tool call exceeded the 600s watchdog SLA",
                   tool_name="research_web"),
    ]

    rebuilt = await rebuild_conversation_messages(messages, tool_calls, [])

    results = _tool_results_of(rebuilt)
    matching = [
        r for r in results
        if (r.get("call_id") or r.get("tool_use_id")) == "call-x"
    ]
    assert len(matching) == 1, (
        f"expected EXACTLY ONE tool_result for call-x (the duplicate-400 fix), "
        f"got {len(matching)}: {results}"
    )
    # And it must carry the authoritative row content, not an empty stub.
    assert matching[0].get("content"), (
        "the surviving tool_result must rebuild from the cx_tool_call row "
        f"(non-empty error content), got: {matching[0]}"
    )
    assert matching[0].get("is_error") is True


@pytest.mark.asyncio
async def test_still_delegated_call_is_not_synthesized() -> None:
    """A row still in status='delegated' has no output — synthesizing an empty
    result would be dropped by sanitize anyway; rebuild must skip it."""
    messages = [
        _msg(id=MSG_ASSISTANT, role="assistant", position=0,
             content=[{"type": "tool_call", "call_id": "call-5", "name": "tabs"}]),
    ]
    tool_calls = [
        _tool_call(call_id="call-5", message_id=MSG_ASSISTANT, output="", status="delegated"),
    ]

    rebuilt = await rebuild_conversation_messages(messages, tool_calls, [])

    assert _tool_results_of(rebuilt) == []


@pytest.mark.asyncio
async def test_reused_call_id_across_turns_keeps_both_results() -> None:
    """Gemini REUSES a deterministic call_id across turns. Turn 1's call is
    answered by a persisted role='tool' message; turn 3 reuses the SAME id as a
    suspended call whose result lives only on cx_tool_call. A conversation-GLOBAL
    pairing guard treats the id as 'already paired' (from turn 1) and skips turn
    3's synthesis — silently dropping turn 3's result. Rebuild must keep BOTH
    (one per turn), consuming each cx_tool_call ROW exactly once."""
    a1 = "aaaaaaaa-0000-0000-0000-000000000001"
    m1 = "aaaaaaaa-0000-0000-0000-000000000002"
    a3 = "aaaaaaaa-0000-0000-0000-000000000003"
    messages = [
        _msg(id=a1, role="assistant", position=0,
             content=[{"type": "tool_call", "call_id": "gemini_-1", "name": "search"}]),
        # Turn 1 answered by a persisted role='tool' pointer message.
        _msg(id=m1, role="tool", position=1,
             content=[{"type": "tool_result", "call_id": "gemini_-1",
                       "tool_use_id": "gemini_-1", "name": "search", "output_chars": 0}]),
        # Turn 3 REUSES the same call_id; suspended → no persisted tool message.
        _msg(id=a3, role="assistant", position=2,
             content=[{"type": "tool_call", "call_id": "gemini_-1", "name": "search"}]),
    ]
    tool_calls = [
        _tool_call(row_id="R1", call_id="gemini_-1", message_id=m1, output="result-turn-1"),
        _tool_call(row_id="R3", call_id="gemini_-1", message_id=a3, output="result-turn-3"),
    ]

    rebuilt = await rebuild_conversation_messages(messages, tool_calls, [])

    results = _tool_results_of(rebuilt)
    contents = sorted(
        r.get("content")
        for r in results
        if (r.get("call_id") or r.get("tool_use_id")) == "gemini_-1"
    )
    assert contents == ["result-turn-1", "result-turn-3"], (
        "each reused-id turn must keep its OWN result — a global pairing guard "
        f"would drop turn 3; got: {contents}"
    )
