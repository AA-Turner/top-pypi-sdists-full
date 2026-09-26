"""The edited-answer knob is respected where the model's history is assembled.

A person edits an assistant answer in place (``cx_message_edit`` archives the
model's own output as ``content_history[0]`` and stamps ``status='edited'``).
``rebuild_conversation_messages`` — THE funnel every continuation path reads
(full config reload, hot cache-hit continuation, persistence resume) — must
replay the EDITED text by default and the model's ORIGINAL output when the
organization's ``agents.messages / edited_answer_visible_to_model`` knob is
false (rich-content PLAN decision 13). The stored row is never mutated.
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
from matrx_ai.db.edited_answers import set_edited_answer_visibility_resolver  # noqa: E402

ORG_A = "aaaaaaaa-0000-0000-0000-000000000001"
ORG_B = "bbbbbbbb-0000-0000-0000-000000000002"

ORIGINAL = [
    {"type": "text", "text": "The capital of Australia is Sydney."},
    {"type": "tool_call", "call_id": "call-9", "name": "lookup", "arguments": {}},
]
EDITED = [
    {"type": "text", "text": "The capital of Australia is Canberra."},
    {"type": "tool_call", "call_id": "call-9", "name": "lookup", "arguments": {}},
]


def _conversation(org: str) -> list[SimpleNamespace]:
    return [
        SimpleNamespace(
            id="u1", role="user", position=0, created_at=None, status="active",
            metadata={}, deleted_at=None, is_visible_to_model=True,
            organization_id=org,
            content=[{"type": "text", "text": "What is the capital of Australia?"}],
        ),
        SimpleNamespace(
            id="a1", role="assistant", position=1, created_at=None, status="edited",
            metadata={}, deleted_at=None, is_visible_to_model=True,
            organization_id=org, content=EDITED,
            content_history=[{"content": ORIGINAL, "saved_at": "2026-09-25T00:00:00Z"}],
        ),
    ]


def _assistant_text(messages: list[Any]) -> str:
    for m in messages:
        role = m.role.value if hasattr(m.role, "value") else m.role
        if role == "assistant":
            return "".join(
                getattr(c, "text", "") or "" for c in m.content if getattr(c, "type", None) == "text"
            )
    raise AssertionError("no assistant message in the rebuilt history")


@pytest.fixture(autouse=True)
def _reset_resolver():
    yield
    set_edited_answer_visibility_resolver(None)


@pytest.mark.asyncio
async def test_default_replays_the_edited_answer() -> None:
    rebuilt = await rebuild_conversation_messages(_conversation(ORG_A), [], [])
    assert _assistant_text(rebuilt) == "The capital of Australia is Canberra."


@pytest.mark.asyncio
async def test_knob_false_replays_the_models_original_output() -> None:
    asked: list[str | None] = []

    async def resolver(org: str | None) -> bool:
        asked.append(org)
        return org != ORG_B

    set_edited_answer_visibility_resolver(resolver)
    rows = _conversation(ORG_B)
    rebuilt = await rebuild_conversation_messages(rows, [], [])
    assert _assistant_text(rebuilt) == "The capital of Australia is Sydney."
    assert asked == [ORG_B]
    # The stored row is untouched — only the model-facing projection changed.
    assert rows[1].content is EDITED


@pytest.mark.asyncio
async def test_knob_true_for_another_org_keeps_the_edit() -> None:
    async def resolver(org: str | None) -> bool:
        return org != ORG_B

    set_edited_answer_visibility_resolver(resolver)
    rebuilt = await rebuild_conversation_messages(_conversation(ORG_A), [], [])
    assert _assistant_text(rebuilt) == "The capital of Australia is Canberra."


@pytest.mark.asyncio
async def test_failing_resolver_announces_and_keeps_the_edit() -> None:
    async def resolver(org: str | None) -> bool:
        raise RuntimeError("knob row missing")

    set_edited_answer_visibility_resolver(resolver)
    rebuilt = await rebuild_conversation_messages(_conversation(ORG_B), [], [])
    assert _assistant_text(rebuilt) == "The capital of Australia is Canberra."


@pytest.mark.asyncio
async def test_knob_false_replays_the_first_archive_even_before_materialization() -> None:
    """Named case (verify-RC-B5): a server-side ``artifact_materialization``
    archives the model's raw text as ``content_history[0]`` BEFORE any person
    edits. With the knob off, the model gets that entry — its own output, as it
    produced it (without the artifact ids the server added later) — never the
    person's edit and never the materialized row the person saw."""

    async def resolver(org: str | None) -> bool:
        return False

    set_edited_answer_visibility_resolver(resolver)
    raw = [{"type": "text", "text": "Model draft with a table."}]
    materialized = [{"type": "text", "text": "Model draft with a table. <artifact id='a1'/>"}]
    rows = _conversation(ORG_B)
    rows[1].content = [{"type": "text", "text": "Person's edit."}]
    rows[1].content_history = [
        {"content": raw, "saved_at": "t0", "reason": "artifact_materialization"},
        {"content": materialized, "saved_at": "t1"},
    ]
    rebuilt = await rebuild_conversation_messages(rows, [], [])
    assert _assistant_text(rebuilt) == "Model draft with a table."
