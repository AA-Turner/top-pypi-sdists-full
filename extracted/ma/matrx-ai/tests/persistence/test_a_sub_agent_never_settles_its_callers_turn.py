"""A sub-agent never settles the outcome of its caller's turn (2026-10-21).

THE DEFECT. A helper forked without its own request record runs under its caller's
``chat.user_request`` id. When its run finished, ``persist_completed_request`` wrote
ITS status / completed_at / error over the caller's row: user_request 5add6922 (the
person's "go ahead and push" turn, which finished fine) read ``paused`` because a
helper stopped at its iteration ceiling, and c462f1d9 carried a child's tool error.

THE CONTRACT (``run_settles_user_request``). Every run settles its own row. A
sub-agent writing under its caller's row settles it only when that row is its own
conversation's (it was the first run there — a workflow or tool fan-out with no AI
turn above it). An unreadable or missing row settles as before, so the rule can never
strand a row unsettled.

Break that turns this red: drop the ownership check (always settle) and the
helper-under-a-chat case returns True; make children never settle and the
first-run-there case returns False.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db import persistence

PARENT_CONVERSATION = str(uuid.uuid4())
HELPER_CONVERSATION = str(uuid.uuid4())
SHARED_REQUEST = str(uuid.uuid4())


def _rows_owned_by(conversation_id: str | None, reads: list[str], *, fail: bool = False) -> Any:
    async def filter_user_requests(id: str) -> list[Any]:  # noqa: A002 — the manager's kwarg
        reads.append(id)
        if fail:
            raise ConnectionError("pooler reset")
        return [] if conversation_id is None else [SimpleNamespace(id=id, conversation_id=conversation_id)]

    return SimpleNamespace(user_request=SimpleNamespace(filter_user_requests=filter_user_requests))


def _helper_ctx() -> Any:
    # What child_agent_context produces: the caller's request id, recorded as parent.
    return SimpleNamespace(
        request_id=SHARED_REQUEST,
        parent_request_id=SHARED_REQUEST,
        conversation_id=HELPER_CONVERSATION,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("row_owner", "settles"),
    [
        (PARENT_CONVERSATION, False),  # the person's chat turn owns it — the helper keeps off
        (HELPER_CONVERSATION, True),  # the helper was the first run there — it owns it
        (None, True),  # no row found — never strand it
    ],
)
async def test_a_helper_settles_only_a_row_its_own_conversation_owns(
    monkeypatch, row_owner, settles
):
    reads: list[str] = []
    monkeypatch.setattr(persistence, "_cxm", lambda: _rows_owned_by(row_owner, reads))

    got = await persistence.run_settles_user_request(
        _helper_ctx(), SHARED_REQUEST, HELPER_CONVERSATION
    )

    assert got is settles
    assert reads == [SHARED_REQUEST]


@pytest.mark.asyncio
async def test_a_run_on_its_own_row_settles_without_a_read(monkeypatch):
    reads: list[str] = []
    monkeypatch.setattr(persistence, "_cxm", lambda: _rows_owned_by(PARENT_CONVERSATION, reads))
    root = SimpleNamespace(
        request_id=SHARED_REQUEST, parent_request_id=None, conversation_id=PARENT_CONVERSATION
    )
    independent = SimpleNamespace(  # a child given its own record (independent_request)
        request_id=str(uuid.uuid4()),
        parent_request_id=SHARED_REQUEST,
        conversation_id=HELPER_CONVERSATION,
    )

    assert await persistence.run_settles_user_request(root, SHARED_REQUEST, PARENT_CONVERSATION)
    assert await persistence.run_settles_user_request(
        independent, independent.request_id, HELPER_CONVERSATION
    )
    assert reads == []


@pytest.mark.asyncio
async def test_an_unreadable_row_is_settled_never_stranded(monkeypatch):
    reads: list[str] = []
    monkeypatch.setattr(persistence, "_cxm", lambda: _rows_owned_by(None, reads, fail=True))

    assert await persistence.run_settles_user_request(
        _helper_ctx(), SHARED_REQUEST, HELPER_CONVERSATION
    )


def test_only_a_settling_run_writes_outcome_columns():
    fields = persistence.user_request_outcome_fields(
        {"status": "paused", "error": {"error_type": "tool_loop_stalled", "message": "ceiling"}},
        [],
        now="2026-10-21T18:12:40Z",
    )
    assert fields["status"] == "paused"
    assert fields["completed_at"] == "2026-10-21T18:12:40Z"
    assert "ceiling" in fields["error"]
