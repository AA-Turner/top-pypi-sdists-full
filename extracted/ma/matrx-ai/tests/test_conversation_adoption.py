"""Forcing-function: a re-attempted start ADOPTS an unstarted conversation.

THE INCIDENT (2026-08-30). A user attached a screenshot, sent it, and was told
"Conversation already exists" about a conversation he had never had. The row had
been published a fraction of a second earlier by his own request, which then
died on a pre-stream check. Because the client mints the conversation id and
keys its whole local state by it, that id was burned permanently — every retry
hit the same duplicate-key 409. A census the same day found 1,297 such shells in
30 days: 10% of every conversation created.

THE RULE UNDER TEST. ``is_new=true`` on an existing id is a conflict ONLY IF
that conversation has STARTED. The test is a PRECONDITION about the row, never a
story about why the earlier attempt failed — which is what makes it hold for the
unbounded set of ways a request can die (validation error, disconnect, provider
error, OOM, deploy, closed laptop). Nothing here enumerates failure paths, and
that is the point.

Every test below is written so it FAILS if adoption ever widens: a started
conversation, another user's conversation, and a lost concurrency race must all
still raise the ordinary duplicate-key error that the router maps to 409.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate


class _UpdateResult:
    def __init__(self, rows_affected: int = 1) -> None:
        self.rows_affected = rows_affected
        self.updated_rows: list = []


class _ConversationManager:
    """Records what adoption tried to write, and how it was scoped."""

    def __init__(self, existing=None, *, rows_affected: int = 1, raises: Exception | None = None):
        self._existing = existing
        self._rows_affected = rows_affected
        self._raises = raises
        self.model = object()
        self.update_calls: list[tuple[dict, dict, int | None]] = []

    async def filter_conversations(self, **_kwargs):
        return [self._existing] if self._existing is not None else []

    async def update_where(self, filters, *, expected_version=None, **updates):
        self.update_calls.append((dict(filters), dict(updates), expected_version))
        if self._raises is not None:
            raise self._raises
        return _UpdateResult(self._rows_affected)


class _MessageManager:
    def __init__(self, messages=None, *, raises: Exception | None = None):
        self._messages = messages or []
        self._raises = raises

    async def filter_messages_by_conversation_id(self, _conversation_id):
        if self._raises is not None:
            raise self._raises
        return list(self._messages)


def _shell(user_id: str, *, message_count: int = 0, version: int | None = 3):
    return SimpleNamespace(
        created_by=user_id,
        message_count=message_count,
        version=version,
        status="active",
        # No start claim and clean lineage — the ordinary adoptable shell.
        last_request_status=None,
        updated_at=None,
        created_at=None,
        system_instruction=None,
        parent_conversation_id=None,
        deleted_at=None,
    )


@pytest.fixture(autouse=True)
def _isolate(monkeypatch):
    gate._known_conversation_ids.clear()
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    yield
    gate._known_conversation_ids.clear()


def _wire(monkeypatch, conversation, message):
    monkeypatch.setattr(
        gate, "_cxm", lambda: SimpleNamespace(conversation=conversation, message=message)
    )


async def _adopt(conversation_id, user_id, create_kwargs, existing):
    return await gate._adopt_unstarted_conversation(
        existing, conversation_id, user_id, create_kwargs
    )


# --------------------------------------------------------------------------- #
# The rule: an unstarted shell is the SAME creation, re-attempted
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_unstarted_shell_is_adopted_and_restamped(monkeypatch):
    """THE regression test for the incident.

    The shell is the caller's own and carries no turn, so the retry succeeds and
    re-stamps the start-state it declares.
    """
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager())

    await _adopt(
        conversation_id,
        user_id,
        {"title": "Kind Creator", "organization_id": "team-org", "status": "active"},
        _shell(user_id),
    )

    filters, updates, expected_version = conversation.update_calls[0]
    assert updates["title"] == "Kind Creator"
    assert updates["message_count"] == 0
    assert expected_version == 3
    # Scoped so it can only ever touch an unstarted row the caller owns.
    assert filters == {"id": conversation_id, "created_by": user_id, "message_count": 0}
    # The gate memoizes the row so the executor skips its redundant existence read.
    assert conversation_id in gate._known_conversation_ids


@pytest.mark.asyncio
async def test_adoption_may_move_an_unstarted_conversation_between_orgs(monkeypatch):
    """The exact second half of the incident.

    The first attempt stamped one organization and died; the retry names a
    different one and MUST be free to. An unstarted conversation's organization
    is still the caller's to choose — it freezes only once a turn lands, which
    is also what the frontend enforces.
    """
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager())

    await _adopt(
        conversation_id,
        user_id,
        {"organization_id": "titanium-org"},
        _shell(user_id),
    )

    _filters, updates, _v = conversation.update_calls[0]
    assert updates["organization_id"] == "titanium-org"


@pytest.mark.asyncio
async def test_adoption_is_reason_agnostic(monkeypatch):
    """Adoption never asks WHY the first attempt died — only whether a turn
    landed. This is what makes it hold for failure paths nobody enumerated."""
    conversation_id, user_id = str(uuid4()), str(uuid4())
    for abandoned_status in ("active", "error", "cancelled", "failed"):
        conversation = _ConversationManager(_shell(user_id))
        _wire(monkeypatch, conversation, _MessageManager())
        stale = _shell(user_id)
        stale.status = abandoned_status

        await _adopt(conversation_id, user_id, {"status": "active"}, stale)

        _f, updates, _v = conversation.update_calls[0]
        assert updates["status"] == "active", abandoned_status


# --------------------------------------------------------------------------- #
# Planted bad cases — the gate must still refuse
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_started_conversation_is_never_adopted(monkeypatch):
    """A conversation that carried a turn is a REAL collision. Adopting it would
    rewrite a live conversation's title, agent, variables and organization."""
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id, message_count=4))
    _wire(monkeypatch, conversation, _MessageManager())

    with pytest.raises(gate.ConversationGateError) as exc:
        await _adopt(conversation_id, user_id, {"title": "x"}, _shell(user_id, message_count=4))

    assert "duplicate key" in str(exc.value)
    assert "already started" in str(exc.value)
    assert conversation.update_calls == []  # nothing was written


@pytest.mark.asyncio
async def test_counter_drift_cannot_make_a_live_conversation_adoptable(monkeypatch):
    """``message_count`` is a denormalized counter and can drift. When it says
    zero we read the messages themselves, so drift can never open the door."""
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager([{"id": "m1"}]))  # counter lied

    with pytest.raises(gate.ConversationGateError) as exc:
        await _adopt(conversation_id, user_id, {"title": "x"}, _shell(user_id))

    assert "already started" in str(exc.value)
    assert conversation.update_calls == []


@pytest.mark.asyncio
async def test_unverifiable_emptiness_fails_closed(monkeypatch):
    """If we cannot PROVE the conversation is empty, we refuse to adopt it."""
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager(raises=RuntimeError("db down")))

    with pytest.raises(gate.ConversationGateError) as exc:
        await _adopt(conversation_id, user_id, {"title": "x"}, _shell(user_id))

    assert "already started" in str(exc.value)
    assert conversation.update_calls == []


@pytest.mark.asyncio
async def test_another_users_conversation_is_never_adopted(monkeypatch):
    """Ownership is checked before emptiness — a stranger's empty conversation
    is still a stranger's, and adopting it would hand over the id."""
    conversation_id = str(uuid4())
    owner, intruder = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(owner))
    _wire(monkeypatch, conversation, _MessageManager())

    with pytest.raises(gate.ConversationGateError) as exc:
        await _adopt(conversation_id, intruder, {"title": "x"}, _shell(owner))

    assert "another user" in str(exc.value)
    assert conversation.update_calls == []


@pytest.mark.asyncio
async def test_losing_the_compare_and_swap_is_an_ordinary_conflict(monkeypatch):
    """Concurrency guard. The primary key used to stop a double-submit by
    accident; adoption retires that, so exactly one of N racing adopters wins the
    version CAS and the losers get the ordinary duplicate-key error."""
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(
        _shell(user_id), raises=RuntimeError("OptimisticLockError: version moved")
    )
    _wire(monkeypatch, conversation, _MessageManager())

    with pytest.raises(gate.ConversationGateError) as exc:
        await _adopt(conversation_id, user_id, {"title": "x"}, _shell(user_id))

    assert "duplicate key" in str(exc.value)
    assert "adoption race" in str(exc.value)
    assert conversation_id not in gate._known_conversation_ids


@pytest.mark.asyncio
async def test_version_less_row_falls_back_to_a_scoped_conditional_update(monkeypatch):
    """Older rows may carry no version. The write stays owner- and
    emptiness-scoped; a zero-row result is still a conflict, never a silent
    no-op that lets the caller believe it adopted something."""
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id, version=None), rows_affected=0)
    _wire(monkeypatch, conversation, _MessageManager())

    with pytest.raises(gate.ConversationGateError) as exc:
        await _adopt(conversation_id, user_id, {"title": "x"}, _shell(user_id, version=None))

    assert "duplicate key" in str(exc.value)
    filters, _updates, expected_version = conversation.update_calls[0]
    assert expected_version is None
    assert filters["created_by"] == user_id and filters["message_count"] == 0


@pytest.mark.asyncio
async def test_adoption_never_writes_a_field_outside_the_start_state_allowlist(monkeypatch):
    """Only declared start-state may be re-stamped. A stray field reaching this
    write is how an adoption would start rewriting real history."""
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager())

    await _adopt(
        conversation_id,
        user_id,
        {
            "title": "ok",
            "created_by": "SOMEONE-ELSE",  # must never be re-stamped
            "created_at": "1999-01-01",  # nor identity/lineage timestamps
            "id": "OTHER-ID",
        },
        _shell(user_id),
    )

    _f, updates, _v = conversation.update_calls[0]
    allowed = (
        set(gate._ADOPTABLE_START_FIELDS)
        | set(gate._ADOPTION_RESET_TO_DEFAULT)
        | {"status", "message_count", "last_request_status", "last_request_id"}
    )
    assert set(updates) <= allowed
    # Identity and lineage are never re-stamped.
    assert "created_by" not in updates
    assert "created_at" not in updates
    assert "id" not in updates


@pytest.mark.asyncio
async def test_adoption_leaves_no_field_carrying_the_dead_attempts_value(monkeypatch):
    """An adopted conversation must be INDISTINGUISHABLE from a fresh one.

    Every mutable column is either re-stamped from this request's start-state or
    reset to a fresh row's default. A column that is neither — one nobody
    thought about — is exactly how a dead attempt's data leaks into a live
    conversation, so the reset map is the default and the allowlist lays over
    it.
    """
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager())

    await _adopt(conversation_id, user_id, {"title": "fresh"}, _shell(user_id))

    _f, updates, _v = conversation.update_calls[0]
    # The dead attempt's model, cached context, and scratch state are cleared.
    for cleared in ("last_model_id", "last_context_breakdown", "cache_state", "task_id"):
        assert cleared in updates, cleared
    assert updates["last_model_id"] is None
    assert updates["cache_state"] == {}


@pytest.mark.asyncio
async def test_a_live_start_claim_blocks_adoption(monkeypatch):
    """THE double-submit fix.

    Request A publishes the row and then spends the whole turn in prep — its
    messages land in ONE transaction at end-of-stream — so for seconds there is
    no committed evidence A exists. B would find an "unstarted" conversation and
    adopt it out from under a live run: two loops interleaving message
    positions, and A's messages inheriting B's organization.

    The claim is written in the same commit as the row, so B can see it.
    """
    from datetime import UTC, datetime

    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager())

    claimed = _shell(user_id)
    claimed.last_request_status = gate.CONVERSATION_START_CLAIM_STATUS
    claimed.updated_at = datetime.now(UTC)

    with pytest.raises(gate.ConversationRunInFlightError):
        await _adopt(conversation_id, user_id, {"title": "x"}, claimed)

    assert conversation.update_calls == []  # the live run keeps its conversation


@pytest.mark.asyncio
async def test_a_stale_claim_does_not_burn_the_id_forever(monkeypatch):
    """A crashed run must not keep an id hostage — that is the whole defect."""
    from datetime import UTC, datetime, timedelta

    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager())

    dead = _shell(user_id)
    dead.last_request_status = gate.CONVERSATION_START_CLAIM_STATUS
    dead.updated_at = datetime.now(UTC) - timedelta(
        seconds=gate.CONVERSATION_START_CLAIM_STALE_SECONDS + 60
    )

    await _adopt(conversation_id, user_id, {"title": "x"}, dead)
    assert conversation.update_calls  # adopted


@pytest.mark.asyncio
async def test_run_in_flight_is_a_conversation_gate_error_subclass():
    """Every existing `except ConversationGateError` must keep working."""
    assert issubclass(gate.ConversationRunInFlightError, gate.ConversationGateError)


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("system_instruction", "a dead attempt's frozen prompt"),
        ("parent_conversation_id", "11111111-1111-1111-1111-111111111111"),
        ("deleted_at", "2026-08-30T00:00:00Z"),
    ],
)
@pytest.mark.asyncio
async def test_state_a_new_conversation_cannot_have_refuses_adoption(
    monkeypatch, column, value
):
    """Adoption's rule is: match a fresh create, or refuse.

    `system_instruction` is immutable once set (a DB trigger rejects the
    mutation), so an adopted shell would run forever under a dead attempt's
    system prompt. `parent_conversation_id` would make the new conversation a
    child of an unrelated parent. `deleted_at` would give the person a
    brand-new conversation born in the trash — invisible in every list while
    its stream runs. None can be made equivalent to a fresh create.
    """
    conversation_id, user_id = str(uuid4()), str(uuid4())
    conversation = _ConversationManager(_shell(user_id))
    _wire(monkeypatch, conversation, _MessageManager())

    poisoned = _shell(user_id)
    setattr(poisoned, column, value)

    with pytest.raises(gate.ConversationGateError) as exc:
        await _adopt(conversation_id, user_id, {"title": "x"}, poisoned)

    assert column in str(exc.value)
    assert conversation.update_calls == []
