"""A platform system process (the title labeler, a condenser, a RAG judge) is never a CHILD of
the person's conversation.

PB-08 (2026-10-19, conversation b924e5b7…): the automatic title run ae0cc373 (Groq, no agent,
in the Matrx System organization — it runs as the platform, which pays) was stored with
``parent_conversation_id`` = the person's conversation. So it showed up in every
``parent_conversation_id`` query and helper listing, a foreign organization's row hanging
under the person's tree. The run still names the conversation it is ABOUT — as
``metadata.subject_conversation_id`` — and keeps its hidden ``system_process`` type; only a
helper an agent delegates to (``subagent``) is a child.

Covers both insert doors (``create_new_conversation``, ``ensure_conversation_exists``) and the
end-of-run UPDATE in ``persistence.py`` that re-stamps the parent (it coalesces with the
gate's INSERT).
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate

SUBJECT = "6b7d1d36-6d0b-4c6e-9a5e-2f4c8f0d1a11"


def _wire(monkeypatch) -> list[dict]:
    queued: list[dict] = []

    class _Conversation:
        async def filter_conversations(self, **_kw):
            return []

    class _Coordinator:
        def set_correlation(self, **_kw):
            return None

        async def finalize(self, *, reason):
            return None

    async def _verified(parent, _child):
        return parent

    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    monkeypatch.setattr(gate, "_get_coordinator", lambda: _Coordinator())
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: _Coordinator())
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **kw: queued.append(kw))
    monkeypatch.setattr(gate, "stamp_org_id", lambda *_a, **_k: None)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", _verified)
    gate._known_conversation_ids.clear()
    return queued


def _ctx(*, system_run: bool):
    from matrx_connect import AppContext
    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    return AppContext(
        emitter=ConsoleEmitter("t", accumulate=False),
        conversation_type="subagent",
        is_internal_agent=True,
        parent_conversation_id=SUBJECT,
        system_run=system_run,
        source_feature="mandate:conversation.label_agent_run",
    )


async def _through_door(monkeypatch, door: str, *, system_run: bool) -> dict:
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    queued = _wire(monkeypatch)
    token = set_app_context(_ctx(system_run=system_run))
    try:
        if door == "create":
            await gate.create_new_conversation(
                str(uuid4()), str(uuid4()), parent_conversation_id=SUBJECT
            )
        else:
            await gate.ensure_conversation_exists(
                str(uuid4()), str(uuid4()), parent_conversation_id=SUBJECT
            )
    finally:
        clear_app_context(token)
    return queued[0]


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["create", "ensure"])
async def test_a_system_process_names_its_subject_but_is_not_its_child(monkeypatch, door):
    row = await _through_door(monkeypatch, door, system_run=True)
    assert row["conversation_type"] == "system_process"
    assert row.get("parent_conversation_id") is None, (
        f"{door}: a platform system process was stored as a child of the person's conversation"
    )
    assert (row.get("metadata") or {}).get("subject_conversation_id") == SUBJECT


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["create", "ensure"])
async def test_a_delegated_helper_is_still_a_child(monkeypatch, door):
    row = await _through_door(monkeypatch, door, system_run=False)
    assert row["conversation_type"] == "subagent"
    assert row["parent_conversation_id"] == SUBJECT
    assert "subject_conversation_id" not in (row.get("metadata") or {})


def test_the_end_of_run_update_moves_the_parent_the_same_way() -> None:
    """persistence.py re-stamps ``parent_conversation_id`` on the end-of-run UPDATE, which
    coalesces with the gate's INSERT — it must pass through the same placement."""
    source = Path(gate.__file__).with_name("persistence.py").read_text()
    tree = ast.parse(source)
    stamps = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(t, ast.Subscript)
            and isinstance(t.slice, ast.Constant)
            and t.slice.value == "parent_conversation_id"
            for t in node.targets
        )
    ]
    assert stamps, "persistence.py no longer stamps a parent — re-read this guard"
    assert "place_system_process_subject(" in source, (
        "persistence.py stamps parent_conversation_id without place_system_process_subject"
    )

    kwargs = {"parent_conversation_id": SUBJECT, "metadata": {"a": 1}}
    gate.place_system_process_subject(kwargs, "system_process", add_metadata=False)
    assert "parent_conversation_id" not in kwargs
    assert kwargs["metadata"] == {"a": 1, "subject_conversation_id": SUBJECT}
    # No metadata in an UPDATE: dropping the parent never invents a metadata write that would
    # replace the INSERT's (the INSERT already carries the subject).
    bare = {"parent_conversation_id": SUBJECT}
    gate.place_system_process_subject(bare, "system_process", add_metadata=False)
    assert bare == {}
    helper = {"parent_conversation_id": SUBJECT}
    gate.place_system_process_subject(helper, "subagent", add_metadata=False)
    assert helper == {"parent_conversation_id": SUBJECT}
