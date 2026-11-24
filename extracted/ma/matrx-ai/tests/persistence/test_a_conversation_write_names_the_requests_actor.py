"""FORCING TEST — a server write on a person's behalf names that person as updated_by.

Since P7, ``platform._stamp_actor`` stamps the SYSTEM principal on an identity-less UPDATE (it reads only
``app.user_id`` / ``auth.uid()``, empty on the server connection). The conversation update (and every other
chat row the Coordinator writes) carried no ``updated_by``, so 53 of 152 recently updated conversations
read as system-written. The one write funnel now carries the request's actor.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest

PERSON = "33333333-3333-4333-8333-333333333333"


def _request_as(monkeypatch, user_id):
    from matrx_ai.persistence import queue_helpers

    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(
            organization_id="66666666-6666-4666-8666-666666666666",
            request_id=str(uuid.uuid4()),
            user_id=user_id,
            conversation_id=None,
        ),
    )


@pytest.mark.parametrize(
    "table",
    ["chat.conversation", "chat.request", "chat.user_request", "chat.tool_call"],
)
def test_the_funnel_names_the_requests_actor(monkeypatch, table) -> None:
    from matrx_ai.persistence.queue_helpers import _with_request_actor

    _request_as(monkeypatch, PERSON)
    assert _with_request_actor(table, {"status": "active"})["updated_by"] == PERSON


def test_a_named_author_is_kept_and_message_rows_are_left_to_their_own_rule(monkeypatch) -> None:
    from matrx_ai.persistence.queue_helpers import _with_request_actor

    _request_as(monkeypatch, PERSON)
    other = "44444444-4444-4444-8444-444444444444"
    assert _with_request_actor("chat.conversation", {"updated_by": other})["updated_by"] == other
    assert "updated_by" not in _with_request_actor("chat.message", {"x": 1})


def test_no_request_actor_leaves_the_row_untouched(monkeypatch) -> None:
    from matrx_ai.persistence.queue_helpers import _with_request_actor

    _request_as(monkeypatch, None)
    assert "updated_by" not in _with_request_actor("chat.conversation", {"status": "active"})


async def test_a_queued_conversation_update_carries_the_actor_to_the_session(monkeypatch) -> None:
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.queue_helpers import _coordinator_cv, queue_conversation_update
    from matrx_ai.persistence.registry import override_table

    class _Meta:
        primary_keys = ["id"]
        foreign_keys: dict = {}
        table_name = "conversation"
        db_schema = "chat"

    class _Conversation:
        _meta = _Meta()

    coord = Coordinator(request_id=str(uuid.uuid4()))
    token = _coordinator_cv.set(coord)
    stand_in = override_table("chat.conversation", _Conversation)
    stand_in.__enter__()
    try:
        _request_as(monkeypatch, PERSON)
        row = str(uuid.uuid4())
        queue_conversation_update(row, status="active")
        (op,) = [o for o in coord._session._ops if o.pk_value == row]
        assert (op.payload or {}).get("updated_by") == PERSON, op.payload
    finally:
        stand_in.__exit__(None, None, None)
        _coordinator_cv.reset(token)
        coord._session._ops.clear()
