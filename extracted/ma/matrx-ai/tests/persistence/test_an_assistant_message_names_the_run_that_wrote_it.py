"""FORCING TEST — every assistant chat.message row carries the run that produced it, in metadata only.

chat.message has no request column; read-aloud (``metadata.request_id``) and cost/nesting
(``metadata.runtime_execution_id``) had to look the run up. The ONE write funnel
(``queue_message_create`` / ``queue_message_update``) stamps both ids from the carried AppContext.
Voice turns reach the same funnel (``RunConversation.record`` -> ``persist_completed_request``),
with ``ctx.request_id`` set to the exchange's request, so this covers them too.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace

from matrx_ai.persistence import queue_helpers

REQ = "33333333-3333-4333-8333-333333333333"
EXE = "44444444-4444-4444-8444-444444444444"
USER = "11111111-1111-4111-8111-111111111111"


class _MessageMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "message"
    db_schema = "chat"


class _PackageMessage:
    _meta = _MessageMeta()


def _carry(monkeypatch, *, metadata: dict) -> None:
    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(
            organization_id=USER, request_id=REQ, user_id=USER, conversation_id=None, metadata=metadata
        ),
    )


def _queued(monkeypatch, metadata: dict, writes):
    from matrx_orm.session.coalesce import coalesce_ops

    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.registry import override_table

    coord = Coordinator(request_id=str(uuid.uuid4()))
    token = queue_helpers._coordinator_cv.set(coord)
    stand_in = override_table("chat.message", _PackageMessage)
    stand_in.__enter__()
    try:
        _carry(monkeypatch, metadata=metadata)
        writes()
        return {op.pk_value: op.payload for op in coalesce_ops(list(coord._session._ops))}
    finally:
        stand_in.__exit__(None, None, None)
        queue_helpers._coordinator_cv.reset(token)
        coord._session._ops.clear()


def test_a_chat_reply_carries_both_run_ids(monkeypatch) -> None:
    conv, reply, user_row, final = (str(uuid.uuid4()) for _ in range(4))

    def writes() -> None:
        queue_helpers.queue_message_create(
            id=user_row, conversation_id=conv, role="user", status="active", content=[{"type": "text", "text": "hi"}]
        )
        queue_helpers.queue_message_create(id=reply, conversation_id=conv, role="assistant", status="pending", content=[])
        queue_helpers.queue_message_create(
            id=final, conversation_id=conv, role="assistant", status="active",
            content=[{"type": "text", "text": "x"}], metadata={"duration_ms": 5},
        )
        # the end-of-turn rewrite carries the whole stored metadata; the ids ride along
        queue_helpers.queue_message_update(reply, status="active", metadata={"iteration": 1})

    ops = _queued(monkeypatch, {"runtime_root_execution_id": EXE}, writes)
    want = {"request_id": REQ, "runtime_execution_id": EXE}
    assert {k: ops[reply]["metadata"][k] for k in want} == want, ops[reply]
    assert ops[reply]["metadata"]["iteration"] == 1
    assert ops[final]["metadata"] == {**want, "duration_ms": 5}
    assert "metadata" not in ops[user_row], "a user row is never stamped"
    assert "request_id" not in str(ops[reply]["content"]), "ids never enter content blocks"


def test_a_voice_reply_with_no_spine_run_still_carries_its_request(monkeypatch) -> None:
    conv, reply = str(uuid.uuid4()), str(uuid.uuid4())
    ops = _queued(
        monkeypatch,
        {},
        lambda: queue_helpers.queue_message_create(
            id=reply, conversation_id=conv, role="assistant", status="active",
            content=[{"type": "text", "text": "spoken"}], metadata={"voice": {"turn_ids": ["t1"]}},
        ),
    )
    assert ops[reply]["metadata"] == {"request_id": REQ, "voice": {"turn_ids": ["t1"]}}


def test_a_callers_own_run_id_wins(monkeypatch) -> None:
    conv, reply = str(uuid.uuid4()), str(uuid.uuid4())
    other = "55555555-5555-4555-8555-555555555555"
    ops = _queued(
        monkeypatch,
        {"runtime_root_execution_id": EXE},
        lambda: queue_helpers.queue_message_create(
            id=reply, conversation_id=conv, role="assistant", status="active", content=[],
            metadata={"request_id": other},
        ),
    )
    assert ops[reply]["metadata"]["request_id"] == other


def test_a_later_turns_write_never_stamps_its_ids_on_an_earlier_answer(monkeypatch) -> None:
    """Two turns, one conversation: answer 1's metadata rewrite in turn 2 must not name turn 2's run."""
    from matrx_orm import JsonbPatch

    _conv, answer_one = str(uuid.uuid4()), str(uuid.uuid4())
    # turn 2's context is the carried one (REQ / EXE); answer 1 belongs to another run
    ops = _queued(
        monkeypatch,
        {"runtime_root_execution_id": EXE},
        lambda: queue_helpers.queue_message_update(answer_one, metadata={"iteration": 2}),
    )
    meta = ops[answer_one]["metadata"]
    assert isinstance(meta, JsonbPatch), "an update patches by key; it never rewrites the whole object"
    assert "request_id" not in meta.set and "runtime_execution_id" not in meta.set, meta.set


def test_the_end_of_turn_metadata_rewrite_keeps_the_rows_ids() -> None:
    """The patch applied over the stored metadata (what the database does) keeps both ids."""
    stored = {"request_id": REQ, "runtime_execution_id": EXE, "iteration": 1}
    patch = queue_helpers._with_run_ids({"metadata": {"iteration": 2, "duration_ms": 9}}, creating=False, row_id="x")["metadata"]
    assert patch.apply(stored) == {**stored, "iteration": 2, "duration_ms": 9}
