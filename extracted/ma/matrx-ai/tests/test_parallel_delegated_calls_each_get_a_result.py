"""Parallel client-resolved calls in one step: every call keeps its OWN result.

THE INCIDENT (chat 7e62c38a, 2026-10-18, Agent Studio assistant): the assistant
proposed several page edits in ONE step (parallel ``apply_surface_write``). Each
waits on the person's approval card, so each ``cx_tool_call`` row stays
``delegated``. The person typed a new message instead of deciding; the next
turn's rebuild saw four tool_uses with no result, the strict sanitizer paid each
the "TOOL NEVER ANSWERED ... no result ever came back" error, and the model
told the person its earlier tries "kept dropping out partway" (and re-sent the
same edits in parallel again).

A row still ``delegated`` is a decision the person has not made - not a failure.
The rebuild now hands the model one honest result PER CALL, in call order, that
says so; a later real answer replaces it (the row turns completed/error).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db._registry import configure_db

configure_db(
    models={
        "CxMessage": SimpleNamespace,
        "CxToolCall": SimpleNamespace,
        "CxMedia": SimpleNamespace,
    }
)

from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages  # noqa: E402

ASSISTANT = "22222222-2222-2222-2222-222222222222"


def _msg(*, id: str, role: str, position: int, content: list[dict[str, Any]]) -> SimpleNamespace:
    return SimpleNamespace(
        id=id, role=role, position=position, content=content, created_at=None,
        status="active", metadata={}, deleted_at=None, is_visible_to_model=True,
    )


def _row(call_id: str, status: str, n: int, output: str = "") -> SimpleNamespace:
    return SimpleNamespace(
        id=f"row-{n}", call_id=call_id, message_id=ASSISTANT, tool_name="apply_surface_write",
        output=output, is_error=False, status=status, output_chars=len(output),
        output_preview=None, error_type=None, error_message=None, deleted_at=None,
    )


def _calls(n: int) -> list[dict[str, Any]]:
    return [{"type": "tool_call", "call_id": f"toolu_{i}", "name": "apply_surface_write"} for i in range(n)]


def _results(rebuilt: list[Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for m in rebuilt:
        role = m.role.value if hasattr(m.role, "value") else m.role
        if role != "tool":
            continue
        for c in m.content:
            block = c if isinstance(c, dict) else c.to_storage_dict()
            if block.get("type") == "tool_result":
                out.append(block)
    return out


@pytest.mark.asyncio
@pytest.mark.parametrize("n", [3, 4])
async def test_every_parallel_delegated_call_gets_its_own_ordered_waiting_result(n: int) -> None:
    messages = [
        _msg(id=ASSISTANT, role="assistant", position=0, content=_calls(n)),
        _msg(id="u2", role="user", position=1, content=[{"type": "text", "text": "do it now"}]),
    ]
    rows = [_row(f"toolu_{i}", "delegated", i) for i in range(n)]

    results = _results(await rebuild_conversation_messages(messages, rows, []))

    assert [r["tool_use_id"] for r in results] == [f"toolu_{i}" for i in range(n)]
    for r in results:
        text = str(r["content"])
        assert "waiting" in text.lower() and "person" in text.lower()
        assert "NEVER ANSWERED" not in text
        assert not r.get("is_error")


@pytest.mark.asyncio
async def test_answered_and_waiting_calls_mix_in_order() -> None:
    messages = [
        _msg(id=ASSISTANT, role="assistant", position=0, content=_calls(3)),
        _msg(id="u2", role="user", position=1, content=[{"type": "text", "text": "and?"}]),
    ]
    rows = [
        _row("toolu_0", "completed", 0, output='{"ok": true}'),
        _row("toolu_1", "delegated", 1),
        _row("toolu_2", "delegated", 2),
    ]
    results = _results(await rebuild_conversation_messages(messages, rows, []))
    assert [r["tool_use_id"] for r in results] == ["toolu_0", "toolu_1", "toolu_2"]
    assert results[0]["content"] == '{"ok": true}'
    assert "waiting" in str(results[1]["content"]).lower()


@pytest.mark.asyncio
async def test_a_turn_ending_on_the_pending_calls_is_left_untouched() -> None:
    """Nothing came after the calls: the person is still deciding, no fake result."""
    messages = [_msg(id=ASSISTANT, role="assistant", position=0, content=_calls(2))]
    rows = [_row(f"toolu_{i}", "delegated", i) for i in range(2)]
    assert _results(await rebuild_conversation_messages(messages, rows, [])) == []
