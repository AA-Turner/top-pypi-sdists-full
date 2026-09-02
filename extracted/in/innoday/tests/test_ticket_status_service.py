"""`src/services/ticket_status_service.py` -- the one place a status move is written.

**What this module is for, and why it is not in `scrum_service`.** A move is two
writes to two systems: `Ticket` here, and the board out there. The local one is
authoritative and must never be rolled back because a third party was down; the
outbound one is best effort and must be *reported* when it fails rather than
swallowed. Those rules are the same whoever asks for the move -- the personal
scrum update asks for it today, and the two ticket `PUT` routes want it next --
so they live in one service rather than in whichever caller happened to need
them first.

The tests below are grouped by the failure the rule prevents, because every one
of them is a way this feature could ship looking correct:

* **the local write** -- status, and the `completed_at` rule in both directions.
  A stale `completed_at` makes `SummaryService._activity_at` read a reopened
  ticket as in-window finished work (see `board_sync_service.py:511-524`).
* **classification before persistence** -- `str(exc)` on a DB error stringifies
  to SQL with bound parameters, and on a connection error to host/port/user.
  That string is rendered to every org member.
* **initialize() before the push** -- `LinearBoardAdapter.update_ticket_status`
  reads `state_name_to_id`, which only `initialize` populates. Omitting it fails
  *only* against a live board, so it is pinned with a stub that checks the map.
* **status-name normalisation** -- `"todo"` does not match a Linear state named
  "To Do" by any comparison the adapter made before this change, and
  `_STATUS_MAP` proves both spellings occur in the wild. This is the single most
  likely way the whole feature silently half-works on a real board.
* **never guessing an assignee** -- two members with the same display name must
  not be matched. `identity_resolution.py:50-56` forbids fuzzy name matching
  inbound, and the rule holds identically in reverse.
"""

from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlmodel import Session as SQLSession

from src.adapters.base_adapter import BoardAdapterError, BoardCapabilityError
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity
from src.services import ticket_status_service


@pytest.fixture
def world(db_engine):
    """One org, one project, one member, and a Linear board they could push to."""
    with SQLSession(db_engine) as session:
        org = Organization(id=str(uuid4()), name="Haviland", alias="hs")
        alice = User(id=str(uuid4()), email="Alice@Example.com", full_name="Alice A")
        session.add_all([org, alice])
        session.commit()
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                organization_id=org.id,
                user_id=alice.id,
                role=OrganizationRole.MEMBER,
                is_active=True,
            )
        )
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        board = BoardRegistration(
            id=str(uuid4()),
            user_id=alice.id,
            organization_id=org.id,
            project_id=project.id,
            board_name="PixelFuel",
            board_url="https://linear.app/hs/team/PF",
            board_type=BoardType.LINEAR,
            board_external_id="team-uuid",
        )
        session.add(board)
        session.commit()
        for row in (org, project, alice, board):
            session.refresh(row)
        yield SimpleNamespace(
            engine=db_engine, org=org, project=project, alice=alice, board=board
        )


def _ticket(world, **kw) -> int:
    with SQLSession(world.engine) as session:
        ticket = Ticket(
            summary=kw.pop("summary", "a ticket"),
            organization_id=world.org.id,
            project_id=world.project.id,
            **kw,
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        return ticket.id


class _StubAdapter:
    """A board that records what it was asked to do, and can be told to fail.

    Deliberately not a `MagicMock`: two of the rules below are about *order*
    (initialize before push) and about a value being populated at the moment of
    the call, and a mock records the call without being able to see either.
    """

    def __init__(self, *, raises=None, members=None, assignee_raises=None):
        self.raises = raises
        self.assignee_raises = assignee_raises
        self.members = members if members is not None else []
        self.initialized = False
        self.state_name_to_id = {}
        self.calls = []
        self.assigned = []

    async def initialize(self, token):
        self.initialized = True
        self.state_name_to_id = {"To Do": "s1", "In Progress": "s2", "Done": "s3"}

    async def update_ticket_status(self, ticket, new_status):
        # Recorded **before** the failure check, unlike the assertion it used to
        # serve: "was the board asked?" and "did the board agree?" are different
        # questions, and a retry test needs the first one to count attempts that
        # went on to fail.
        self.calls.append((new_status, dict(self.state_name_to_id)))
        if self.raises is not None:
            raise self.raises
        return ticket

    async def set_board_assignee(self, ticket, board_user_id):
        if self.assignee_raises is not None:
            raise self.assignee_raises
        self.assigned.append(board_user_id)
        return ticket

    async def get_board_metadata(self):
        return {"members": self.members}


def _use(monkeypatch, adapter, *, token="tok"):
    """Point the service's two outbound seams at a stub, and nothing else."""
    monkeypatch.setattr(
        ticket_status_service, "resolve_board_token", lambda *a, **k: token
    )
    monkeypatch.setattr(
        ticket_status_service,
        "build_board_adapter",
        AsyncMock(return_value=adapter),
    )


async def _move(world, ticket_id, status, **kw):
    with SQLSession(world.engine) as session:
        ticket = session.get(Ticket, ticket_id)
        actor = session.get(User, world.alice.id)
        return await ticket_status_service.move_ticket_status(
            session, ticket=ticket, new_status=status, actor=actor, **kw
        )


def _reload(world, ticket_id) -> Ticket:
    with SQLSession(world.engine) as session:
        return session.get(Ticket, ticket_id)


# --------------------------------------------------------------------------- #
# The local write
# --------------------------------------------------------------------------- #


class TestTheLocalWrite:
    @pytest.mark.asyncio
    async def test_reopening_a_done_ticket_clears_its_completion_time(
        self, world, monkeypatch
    ):
        """DONE -> IN_PROGRESS must not leave the old `completed_at` behind.

        `SummaryService._activity_at` reads `completed_at` as evidence of a real
        terminal transition, so a stale one makes a reopened ticket look like
        in-window finished work for as long as the window covers the date it was
        closed. Board sync learned this the hard way
        (`board_sync_service.py:511-524`); neither ticket `PUT` route does it
        even now.
        """
        _use(monkeypatch, _StubAdapter())
        finished = datetime.utcnow() - timedelta(days=2)
        ticket_id = _ticket(
            world, status=TicketStatus.DONE, completed_at=finished, url=None
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.applied is True
        row = _reload(world, ticket_id)
        assert row.status == TicketStatus.IN_PROGRESS
        assert row.completed_at is None, "a reopened ticket kept its completion date"

    @pytest.mark.asyncio
    async def test_finishing_a_ticket_stamps_its_completion_time(
        self, world, monkeypatch
    ):
        """The same rule in the other direction, which is the half that is easy
        to write and easy to forget: moving *to* DONE stamps `completed_at`."""
        _use(monkeypatch, _StubAdapter())
        ticket_id = _ticket(world, status=TicketStatus.IN_PROGRESS)

        await _move(world, ticket_id, TicketStatus.DONE)

        row = _reload(world, ticket_id)
        assert row.status == TicketStatus.DONE
        assert row.completed_at is not None

    @pytest.mark.asyncio
    async def test_the_move_restamps_updated_at(self, world, monkeypatch):
        """`updated_at` is what every activity reader treats as "this moved"."""
        _use(monkeypatch, _StubAdapter())
        ticket_id = _ticket(world, status=TicketStatus.TODO)
        before = _reload(world, ticket_id).updated_at

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert _reload(world, ticket_id).updated_at > before

    @pytest.mark.asyncio
    async def test_taking_a_ticket_writes_both_halves_of_the_assignment(
        self, world, monkeypatch
    ):
        """`assigned_to` is the FK every InnoDay reader uses; `assignee` is the
        board's display mirror. Writing one without the other leaves the ticket
        looking assigned on exactly one of the two surfaces that show it."""
        _use(monkeypatch, _StubAdapter())
        ticket_id = _ticket(world, status=TicketStatus.TODO)

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True)

        row = _reload(world, ticket_id)
        assert row.assigned_to == world.alice.id
        assert row.assignee == "Alice A"

    @pytest.mark.asyncio
    async def test_a_move_that_is_not_a_take_leaves_the_assignment_alone(
        self, world, monkeypatch
    ):
        """Bringing your own finished work back is not a reassignment."""
        _use(monkeypatch, _StubAdapter())
        ticket_id = _ticket(
            world, status=TicketStatus.DONE, assignee="Someone Else", completed_at=None
        )

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        row = _reload(world, ticket_id)
        assert row.assigned_to is None
        assert row.assignee == "Someone Else"


class TestIdempotence:
    @pytest.mark.asyncio
    async def test_a_ticket_already_in_the_target_status_is_a_no_op_success(
        self, world, monkeypatch
    ):
        """What makes a lost response safe to retry.

        Asserted as "nothing was written", not merely "no error": a second call
        that rewrites `updated_at` republishes the ticket as freshly active to
        every consumer that reads that column as an activity signal.

        **The ticket has a board on purpose.** Without one this test's
        "a no-op still pushed" assertion could not fail at all -- `_push` is
        unreachable when `board_registration_id` is NULL, so it certified nothing
        whatever the short-circuit did.
        """
        adapter = _StubAdapter()
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.IN_PROGRESS,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )
        before = _reload(world, ticket_id).updated_at

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.applied is True
        assert result.written is False
        assert result.error is None
        # None, not False: no push was attempted, which is a different answer
        # from "attempted and failed" and is what stops the caller clearing a
        # `push_error` that is still true.
        assert result.pushed is None
        assert _reload(world, ticket_id).updated_at == before
        assert adapter.calls == [], "a no-op still pushed to the board"

    @pytest.mark.asyncio
    async def test_a_no_op_still_pushes_when_the_last_push_failed(
        self, world, monkeypatch
    ):
        """**The retry path, which is the only way the board ever converges.**

        "The local state is correct" and "the board has been told" are different
        questions, and answering the second with the first is what made a failed
        push permanent: the status already matches, so no later call could ever
        re-attempt it without somebody moving the ticket somewhere else and back.
        """
        adapter = _StubAdapter()
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.IN_PROGRESS,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(
            world, ticket_id, TicketStatus.IN_PROGRESS, retry_push=True
        )

        assert result.written is False, "a retry rewrote a local row that was fine"
        assert result.pushed is True
        assert len(adapter.calls) == 1, "the retry never reached the board"

    @pytest.mark.asyncio
    async def test_a_no_op_status_still_applies_an_outstanding_take(
        self, world, monkeypatch
    ):
        """The status half being settled does not settle the assignment half.

        A ticket already IN_PROGRESS but unowned is exactly what "take this on"
        means, and short-circuiting on status alone would silently drop it.
        """
        _use(monkeypatch, _StubAdapter())
        ticket_id = _ticket(world, status=TicketStatus.IN_PROGRESS)

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True)

        assert _reload(world, ticket_id).assigned_to == world.alice.id


# --------------------------------------------------------------------------- #
# The push, and what happens when it fails
# --------------------------------------------------------------------------- #


class TestThePush:
    @pytest.mark.asyncio
    async def test_the_adapter_is_initialized_before_the_status_is_pushed(
        self, world, monkeypatch
    ):
        """`build_board_adapter` does not call `initialize`, and
        `LinearBoardAdapter.update_ticket_status` reads `state_name_to_id`, which
        only `initialize` fills. Omitting it raises "Unknown Linear workflow
        state" against a live board and nothing at all against a mock -- so the
        stub asserts the map is populated *at the moment of the call*."""
        adapter = _StubAdapter()
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.pushed is True
        assert adapter.initialized is True
        assert adapter.calls, "the status was never pushed"
        _, states_at_call = adapter.calls[0]
        assert states_at_call, "update_ticket_status ran before initialize()"

    @pytest.mark.asyncio
    async def test_the_caller_passes_the_status_value_not_board_vocabulary(
        self, world, monkeypatch
    ):
        """The adapter owns the board's spelling. The service passes
        `TicketStatus(...).value` and nothing else."""
        adapter = _StubAdapter()
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert adapter.calls[0][0] == TicketStatus.IN_PROGRESS.value

    @pytest.mark.asyncio
    async def test_a_ticket_with_no_board_is_moved_and_reported_as_a_success(
        self, world, monkeypatch
    ):
        """An InnoDay-only ticket has nothing to push to. That is not a failure,
        and reporting one would train people to ignore the banner that matters."""
        _use(monkeypatch, _StubAdapter())
        ticket_id = _ticket(world, status=TicketStatus.TODO)

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.applied is True
        assert result.error is None
        assert _reload(world, ticket_id).status == TicketStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_a_push_failure_keeps_the_local_move_and_carries_the_message(
        self, world, monkeypatch
    ):
        """Local-first, push-second, and the local write is never rolled back
        because a third party was down. Push-first would leave a board write with
        no local row, which the next inbound sync presents as a change nobody
        made from InnoDay."""
        _use(
            monkeypatch,
            _StubAdapter(raises=BoardAdapterError("Linear said no: rate limited")),
        )
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.applied is True
        assert result.pushed is False
        assert "rate limited" in result.error
        assert _reload(world, ticket_id).status == TicketStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_a_missing_credential_is_reported_in_its_own_words(
        self, world, monkeypatch
    ):
        """The credential refusal is written to be read -- it names the board and
        the one store that fixes it. Replacing it with the generic message would
        leave an operator a shrug.

        **The real chain runs here**, rather than a stub raising the exception the
        test hopes for: whether the production path raises something classified as
        readable is the entire question, and a hand-thrown exception answers it
        about the test instead of about the code.

        Only the vault *read* is stubbed, at the factory — `get_board_credential`
        is a Postgres `SECURITY DEFINER` function and SQLite has no such thing, so
        the unstubbed call raises an `OperationalError` and this would pass or
        fail for a reason that has nothing to do with credentials.
        """
        from src.services import board_adapter_factory

        adapter = _StubAdapter()
        monkeypatch.setattr(
            board_adapter_factory,
            "get_board_credential_payload",
            lambda session, board_id: None,
        )
        monkeypatch.setattr(
            ticket_status_service,
            "build_board_adapter",
            AsyncMock(return_value=adapter),
        )
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.pushed is False
        assert "No credential stored" in result.error

    @pytest.mark.asyncio
    async def test_an_unexpected_exception_never_reaches_the_reader(
        self, world, monkeypatch
    ):
        """**#641's finding, at a new seam.** `str(exc)` on a DBAPI error is the
        SQL plus its bound parameters; on a connection error it is host, port and
        user. Whatever is stored here is rendered to every member of the org, so
        only exceptions raised *to be read* pass through.
        """
        leaky = RuntimeError(
            'connection to server at "db.internal" (10.0.0.4), port 5432 '
            'failed: FATAL: password authentication failed for user "innoday" '
            "[SQL: UPDATE ticket SET status=%(status)s] [parameters: {'status': 1}]"
        )
        _use(monkeypatch, _StubAdapter(raises=leaky))
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.pushed is False
        assert result.error
        for leak in ("10.0.0.4", "5432", "password", "innoday", "SQL:", "parameters"):
            assert leak not in result.error, f"{leak!r} reached the reader"

    @pytest.mark.asyncio
    async def test_a_plain_value_error_is_not_treated_as_readable(
        self, world, monkeypatch
    ):
        """**Whitelisting a *type* cannot express "written to be read".**

        `ValueError` is far too broad to carry that meaning: `json.JSONDecodeError`,
        `pydantic.ValidationError` and `UnicodeDecodeError` are all subclasses, and
        `linear_api.py` used to raise a bare `ValueError` carrying Linear's whole
        raw error array. The signal has to be something an author sets on purpose.
        """
        _use(
            monkeypatch,
            _StubAdapter(
                raises=ValueError(
                    "GraphQL errors: [{'extensions': {'userPresentableMessage': "
                    "None, 'internal': 'db-shard-7.linear.internal'}}]"
                )
            ),
        )
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.pushed is False
        assert "db-shard-7" not in result.error
        assert "GraphQL errors" not in result.error

    @pytest.mark.asyncio
    async def test_a_credential_refusal_is_still_reported_in_its_own_words(
        self, world, monkeypatch
    ):
        """The one `ValueError` that *was* meant to be read keeps being read --
        it now says so with its own class rather than by being a `ValueError`."""
        from src.adapters.base_adapter import BoardCredentialError

        _use(monkeypatch, _StubAdapter())
        monkeypatch.setattr(
            ticket_status_service,
            "resolve_board_token",
            lambda *a, **k: (_ for _ in ()).throw(
                BoardCredentialError("No credential stored for linear board b1")
            ),
        )
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert result.pushed is False
        assert "No credential stored" in result.error

    @pytest.mark.asyncio
    async def test_a_push_failure_does_not_redden_the_whole_board(
        self, world, monkeypatch
    ):
        """`BoardRegistration.errored_at` means "the last *sync* of this board
        failed" and the dashboard's status icon reads it. One ticket's push
        failure marking the whole board broken is the misreport #641 was about,
        in the other direction."""
        _use(monkeypatch, _StubAdapter(raises=BoardAdapterError("nope")))
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        with SQLSession(world.engine) as session:
            board = session.get(BoardRegistration, world.board.id)
            assert board.errored_at is None
            assert board.error_message is None


# --------------------------------------------------------------------------- #
# Pushing the assignee, and the identity trap
# --------------------------------------------------------------------------- #


class TestPushingTheAssignee:
    @pytest.mark.asyncio
    async def test_the_board_assignee_is_matched_on_email_case_insensitively(
        self, world, monkeypatch
    ):
        """Same first rule the inbound resolver uses, so the two agree."""
        adapter = _StubAdapter(
            members=[
                {"id": "lin-1", "name": "Someone", "email": "someone@example.com"},
                {"id": "lin-2", "name": "A. Alice", "email": "alice@EXAMPLE.com"},
            ]
        )
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(
            world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True
        )

        assert adapter.assigned == ["lin-2"]
        assert result.assignee_pushed is True
        assert result.notice is None

    @pytest.mark.asyncio
    async def test_a_claimed_linear_handle_matches_the_display_name_not_the_full_name(
        self, world, monkeypatch
    ):
        """Second rule, and the reason `UserIdentity` exists: a board that does
        not expose email still has a name somebody has *claimed*.

        **The field matters.** Linear's `name` is a person's full name; the
        unique `@`-handle is `displayName`. Matching a claimed handle against
        `name` means the person who claims their actual handle never matches, so
        the durability this whole feature exists for silently does not happen --
        and it is the common case, not an edge one. The member below has a full
        name that is nobody's handle, exactly as on a real board.
        """
        with SQLSession(world.engine) as session:
            session.add(
                UserIdentity(
                    id=str(uuid4()),
                    user_id=world.alice.id,
                    project_id=world.project.id,
                    platform=IdentityPlatform.LINEAR,
                    handle="alice-on-linear",
                    match_source=MatchSource.HANDLE,
                )
            )
            session.commit()
        adapter = _StubAdapter(
            members=[
                {
                    "id": "lin-1",
                    "name": "Alice Anderson",
                    "displayName": "alice-on-linear",
                    "email": None,
                },
                {
                    "id": "lin-2",
                    "name": "Someone",
                    "displayName": "someone",
                    "email": "someone@example.com",
                },
            ]
        )
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True)

        assert adapter.assigned == ["lin-1"]

    @pytest.mark.asyncio
    async def test_two_members_answering_to_the_claimed_handle_are_refused(
        self, world, monkeypatch
    ):
        """**The reachable half of the two-Alexes hazard.**

        The sibling test below rules out an unconditional display-name tail. This
        one is the case that actually happens: a handle *has* been claimed, and
        two members answer to it. Returning the first hit is a silent
        reassignment of somebody's work, and the ordering that decides which one
        is incidental.
        """
        with SQLSession(world.engine) as session:
            session.add(
                UserIdentity(
                    id=str(uuid4()),
                    user_id=world.alice.id,
                    project_id=world.project.id,
                    platform=IdentityPlatform.LINEAR,
                    handle="alex",
                    match_source=MatchSource.HANDLE,
                )
            )
            session.commit()
        adapter = _StubAdapter(
            members=[
                {
                    "id": "lin-1",
                    "name": "Alex One",
                    "displayName": "alex",
                    "email": None,
                },
                {
                    "id": "lin-2",
                    "name": "Alex Two",
                    "displayName": "Alex",
                    "email": None,
                },
            ]
        )
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(
            world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True
        )

        assert adapter.assigned == [], "an ambiguous handle picked a winner"
        assert result.assignee_pushed is False
        assert result.notice

    @pytest.mark.asyncio
    async def test_a_project_handle_beats_a_global_one(self, world, monkeypatch):
        """The only observable difference between the two kinds of row.

        A project row exists precisely because the global answer was wrong on this
        board, so an override a lookup can silently ignore is not an override.
        """
        with SQLSession(world.engine) as session:
            session.add_all(
                [
                    UserIdentity(
                        id=str(uuid4()),
                        user_id=world.alice.id,
                        project_id=None,
                        platform=IdentityPlatform.LINEAR,
                        handle="alice-global",
                        match_source=MatchSource.HANDLE,
                    ),
                    UserIdentity(
                        id=str(uuid4()),
                        user_id=world.alice.id,
                        project_id=world.project.id,
                        platform=IdentityPlatform.LINEAR,
                        handle="alice-on-this-board",
                        match_source=MatchSource.HANDLE,
                    ),
                ]
            )
            session.commit()
        adapter = _StubAdapter(
            members=[
                {
                    "id": "lin-global",
                    "name": "A",
                    "displayName": "alice-global",
                    "email": None,
                },
                {
                    "id": "lin-project",
                    "name": "B",
                    "displayName": "alice-on-this-board",
                    "email": None,
                },
            ]
        )
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        await _move(world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True)

        assert adapter.assigned == ["lin-project"]

    @pytest.mark.asyncio
    async def test_two_members_with_the_same_display_name_are_never_guessed_between(
        self, world, monkeypatch
    ):
        """**The rule with no tail.** `identity_resolution.py:50-56` refuses fuzzy
        display-name matching inbound -- "two people called 'Alex' on a client's
        board is normal; guessing between them silently reassigns someone's
        work" -- and reversing the direction does not make the guess safe.

        The move still applies and the local pair is still written; what the user
        gets is the truth on screen, because the next inbound sync will overwrite
        the assignment from the board.
        """
        adapter = _StubAdapter(
            members=[
                {"id": "lin-1", "name": "Alice A", "email": None},
                {"id": "lin-2", "name": "Alice A", "email": None},
            ]
        )
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(
            world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True
        )

        assert adapter.assigned == [], "a display name was guessed between"
        assert result.applied is True
        assert result.pushed is True
        assert result.assignee_pushed is False
        assert result.notice, "an unresolved board assignee was reported as fine"
        lowered = result.notice.lower()
        assert "sync" in lowered, "the notice does not say it will be overwritten"
        assert "handle" in lowered, "the notice does not say where to fix it"
        row = _reload(world, ticket_id)
        assert row.assigned_to == world.alice.id
        assert row.assignee == "Alice A"

    @pytest.mark.asyncio
    async def test_a_board_type_that_cannot_assign_degrades_cleanly(
        self, world, monkeypatch
    ):
        """**Only Linear implements the outbound assignee, and the other three
        must produce a clean outcome — not a stored failure.**

        This is the case the separate `set_board_assignee` call was added for. A
        board with no assignee field will refuse identically forever, so writing
        that to `push_error` makes it permanent and un-clearable — and because a
        stored error is what asks for a retry, it re-pushes the status on every
        later submit for something that can never succeed.

        The test that used to cover this scenario was repurposed to a 429 while
        keeping its name, which left the capability path uncovered. Both now
        exist, and they assert opposite things about `error`.
        """
        from src.adapters.base_adapter import BoardCapabilityError

        adapter = _StubAdapter(
            members=[
                {
                    "id": "b-1",
                    "name": "Alice A",
                    "displayName": "alice",
                    "email": "alice@example.com",
                }
            ],
            assignee_raises=BoardCapabilityError(
                "TrelloBoardAdapter cannot set a board assignee"
            ),
        )
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(
            world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True
        )

        assert result.pushed is True
        assert adapter.calls, "the status push was lost with the assignee push"
        assert result.assignee_pushed is False
        assert result.error is None, (
            "a board that structurally cannot assign was recorded as a failure, "
            "which makes it permanent and retries it forever"
        )
        assert result.notice
        assert "handle" not in result.notice.lower(), (
            "a board with no assignee field was blamed on the user's profile"
        )

    @pytest.mark.asyncio
    async def test_an_assignee_push_that_failed_is_reported_and_persisted(
        self, world, monkeypatch
    ):
        """The other half: a board that *can* assign and did not.

        **The failure is reported as a failure, not as a profile problem.**
        A raised push is a different thing from an unresolved member: the second
        is fixed by claiming a handle, the first is not, and telling somebody to
        go and edit their profile after a 429 sends them somewhere that cannot
        help. It also has to be *persisted* -- otherwise the only record that the
        board thinks the ticket is unowned dies with the response.
        """
        adapter = _StubAdapter(
            members=[
                {
                    "id": "b-1",
                    "name": "Alice A",
                    "displayName": "alice",
                    "email": "alice@example.com",
                }
            ],
            assignee_raises=BoardAdapterError("Linear returned HTTP 429: slow down"),
        )
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.TODO,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(
            world, ticket_id, TicketStatus.IN_PROGRESS, assign_to_actor=True
        )

        assert result.pushed is True
        assert adapter.calls, "the status push was lost with the assignee push"
        assert result.assignee_pushed is False
        assert result.error, "an assignee push failure was not reported at all"
        assert "429" in result.error
        assert "profile" not in result.error.lower(), (
            "a rate limit was diagnosed as a missing handle"
        )
        assert result.notice is None

    @pytest.mark.asyncio
    async def test_nothing_is_resolved_when_the_move_is_not_a_take(
        self, world, monkeypatch
    ):
        """A reopen does not touch the assignee, so it must not read the board's
        member list either -- one avoidable round trip per ticket, on the common
        path."""
        adapter = _StubAdapter(members=[{"id": "x", "name": "y", "email": None}])
        _use(monkeypatch, adapter)
        ticket_id = _ticket(
            world,
            status=TicketStatus.DONE,
            board_registration_id=world.board.id,
            external_ticket_id="PF-1",
        )

        result = await _move(world, ticket_id, TicketStatus.IN_PROGRESS)

        assert adapter.assigned == []
        assert result.assignee_pushed is None
        assert result.notice is None


# --------------------------------------------------------------------------- #
# The adapter's own vocabulary
# --------------------------------------------------------------------------- #


class TestLinearStatusNames:
    """Tested against the adapter directly, not through the service.

    The service's whole contract is that it passes `TicketStatus(...).value` and
    knows nothing about board spellings, so a test that went through it would be
    asserting the service's ignorance rather than the adapter's competence -- and
    the bug is in the comparison, which only the adapter makes.
    """

    def _adapter(self, states):
        from src.adapters.linear_adapter import LinearBoardAdapter

        registration = SimpleNamespace(
            board_external_id="team-uuid", board_type=BoardType.LINEAR, id="b1"
        )
        adapter = LinearBoardAdapter.__new__(LinearBoardAdapter)
        adapter.board_registration = registration
        adapter.board_id = "team-uuid"
        adapter.workflow_states = {v: k for k, v in states.items()}
        adapter.state_name_to_id = dict(states)
        adapter._initialized = True
        adapter.api = SimpleNamespace(
            update_issue=AsyncMock(return_value={"id": "i1", "identifier": "PF-1"})
        )
        adapter._issue_to_ticket = lambda issue: Ticket(
            summary="s", organization_id="o", project_id="p"
        )
        return adapter

    @pytest.mark.asyncio
    async def test_todo_reaches_a_state_named_to_do(self):
        """The failure the whole feature would have shipped with.

        `TicketStatus.TODO.value` is `"todo"`. A Linear state is commonly named
        `"To Do"`. Neither an exact nor a case-insensitive comparison matches
        them, and `_STATUS_MAP` carries *both* spellings inbound -- which is the
        evidence that both occur on real boards.
        """
        adapter = self._adapter({"To Do": "s1", "In Progress": "s2"})

        await adapter.update_ticket_status(
            Ticket(summary="s", organization_id="o", project_id="p"),
            TicketStatus.TODO.value,
        )

        assert adapter.api.update_issue.await_args[0][1] == {"stateId": "s1"}

    @pytest.mark.asyncio
    async def test_in_progress_reaches_a_state_named_in_progress(self):
        adapter = self._adapter({"To Do": "s1", "In Progress": "s2"})

        await adapter.update_ticket_status(
            Ticket(summary="s", organization_id="o", project_id="p"),
            TicketStatus.IN_PROGRESS.value,
        )

        assert adapter.api.update_issue.await_args[0][1] == {"stateId": "s2"}

    @pytest.mark.asyncio
    async def test_a_board_that_spells_it_differently_still_matches(self):
        """Normalisation is on non-alphanumerics and case, not on one spelling:
        `"In-Progress"`, `"inprogress"` and `"In Progress"` are the same state
        name to a human and must be to this comparison."""
        adapter = self._adapter({"In-Progress": "s7"})

        await adapter.update_ticket_status(
            Ticket(summary="s", organization_id="o", project_id="p"),
            TicketStatus.IN_PROGRESS.value,
        )

        assert adapter.api.update_issue.await_args[0][1] == {"stateId": "s7"}

    @pytest.mark.asyncio
    async def test_done_is_never_quietly_substituted_for_a_cancelled_state(self):
        """**A wrong fact on a client's board is worse than a failed move.**

        `_STATUS_MAP` maps both `"done"` and `"cancelled"` to `TicketStatus.DONE`
        because *inbound* that conflation is merely lossy. Read backwards to find
        an alias it becomes a write: on a board with a "Cancelled" column and no
        "Done", finishing a ticket would mark it cancelled -- and
        `TicketStatus.CANCELLED` exists separately, so the reverse substitution
        is available too.

        Nothing may guess between two states a human would not call the same
        thing. Refusing names what the board does have, which is the diagnosis.
        """
        adapter = self._adapter({"Cancelled": "s9"})

        with pytest.raises(BoardAdapterError) as excinfo:
            await adapter.update_ticket_status(
                Ticket(summary="s", organization_id="o", project_id="p"),
                TicketStatus.DONE.value,
            )

        adapter.api.update_issue.assert_not_awaited()
        assert "Cancelled" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_a_live_http_failure_keeps_linears_own_explanation(self):
        """**The path that only exists against a real board.**

        `LinearAPIError` is a `RuntimeError`, and this method used not to wrap
        `api.update_issue` the way its siblings do -- so every real 401/403/429/502
        arrived at the service as an unexpected exception and was replaced by the
        generic message. The actionable text was lost exactly where the feature
        promised it, and no test could notice because every test fabricated a
        `BoardAdapterError` production could not produce.
        """
        from src.api.linear_api import LinearAPIError

        adapter = self._adapter({"In Progress": "s2"})
        adapter.api.update_issue = AsyncMock(
            side_effect=LinearAPIError("Linear returned HTTP 429: rate limited")
        )

        with pytest.raises(BoardAdapterError) as excinfo:
            await adapter.update_ticket_status(
                Ticket(summary="s", organization_id="o", project_id="p"),
                TicketStatus.IN_PROGRESS.value,
            )

        assert "429" in str(excinfo.value)
        assert "rate limited" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_an_assignee_push_failure_is_wrapped_the_same_way(self):
        from src.api.linear_api import LinearAPIError

        adapter = self._adapter({"In Progress": "s2"})
        adapter.api.update_issue = AsyncMock(
            side_effect=LinearAPIError("Linear returned HTTP 502: bad gateway")
        )

        with pytest.raises(BoardAdapterError) as excinfo:
            await adapter.set_board_assignee(
                Ticket(
                    summary="s",
                    organization_id="o",
                    project_id="p",
                    external_ticket_id="PF-1",
                ),
                "lin-9",
            )

        assert "502" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_a_state_the_board_does_not_have_is_still_refused_by_name(self):
        """Normalising must not become matching-anything: an unknown state is a
        `BoardAdapterError` that lists what the board does have, because that
        message is the whole diagnosis for an operator."""
        adapter = self._adapter({"To Do": "s1"})

        with pytest.raises(BoardAdapterError) as excinfo:
            await adapter.update_ticket_status(
                Ticket(summary="s", organization_id="o", project_id="p"),
                TicketStatus.IN_REVIEW.value,
            )

        assert "To Do" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_the_assignee_push_is_one_mutation_naming_the_board_user(self):
        adapter = self._adapter({"To Do": "s1"})

        await adapter.set_board_assignee(
            Ticket(
                summary="s",
                organization_id="o",
                project_id="p",
                external_ticket_id="PF-1",
            ),
            "lin-9",
        )

        assert adapter.api.update_issue.await_args[0][1] == {"assigneeId": "lin-9"}


@pytest.mark.asyncio
async def test_linear_raises_its_own_error_type_for_a_graphql_error(monkeypatch):
    """A GraphQL error is a Linear failure, so it raises `LinearAPIError`.

    It raised a bare `ValueError`, which made it indistinguishable from a
    programming mistake -- and while the service classified by type, that put
    Linear's raw error array, `extensions` and all, verbatim into a string every
    member of the org reads.

    Driven through `_execute` with a stubbed transport rather than asserted on
    the source, because "which exception does this raise" is behaviour.

    **Module level, and it must stay below every class in this file.** Written
    between two methods of `TestLinearStatusNames` it silently ended that class's
    body, turning the two methods after it into nested functions pytest never
    collects -- and the file's test count went *up*, so nothing signalled it. One
    of the two was the guard for the DONE/Cancelled substitution.
    """
    import httpx

    from src.api.linear_api import LinearAPI, LinearAPIError

    class _Response:
        is_error = False

        @staticmethod
        def json():
            return {"errors": [{"message": "boom", "extensions": {"internal": "x"}}]}

    monkeypatch.setattr(httpx.AsyncClient, "post", AsyncMock(return_value=_Response()))

    with pytest.raises(LinearAPIError):
        await LinearAPI(api_key="k")._execute("query { x }", {})


class TestAdaptersThatCannotAssign:
    """Every adapter answers the question; three of them answer "no".

    A default that silently did nothing would report a pushed assignment that
    never happened -- the exact shape this feature exists to avoid.
    """

    @pytest.mark.parametrize(
        "module_name, class_name",
        [
            ("src.adapters.jira_adapter", "JiraBoardAdapter"),
            ("src.adapters.trello_adapter", "TrelloBoardAdapter"),
            ("src.adapters.notion_adapter", "NotionBoardAdapter"),
        ],
    )
    @pytest.mark.asyncio
    async def test_it_refuses_rather_than_silently_dropping_the_assignment(
        self, module_name, class_name
    ):
        import importlib

        cls = getattr(importlib.import_module(module_name), class_name)
        adapter = cls.__new__(cls)

        # `BoardCapabilityError` specifically: the caller branches on it to
        # decide whether the outcome is recorded and retried, so "some
        # BoardAdapterError" is not a strong enough guarantee here.
        with pytest.raises(BoardCapabilityError):
            await adapter.set_board_assignee(
                Ticket(
                    summary="s",
                    organization_id="o",
                    project_id="p",
                    external_ticket_id="X-1",
                ),
                "who",
            )


# --------------------------------------------------------------------------- #
# The credential chain, now shared
# --------------------------------------------------------------------------- #


def test_the_credential_chain_lives_in_the_factory_and_is_not_copied():
    """`BoardTicketCreationService._resolve_token` was the only copy; a third
    one is exactly the drift a previous cleanup closed. The service keeps its
    method as a delegate so its own callers and tests are unchanged, and the
    chain itself is one function both callers import."""
    import inspect

    from src.services import board_adapter_factory
    from src.services.board_ticket_creation_service import BoardTicketCreationService

    assert hasattr(board_adapter_factory, "resolve_board_token")
    source = inspect.getsource(BoardTicketCreationService._resolve_token)
    assert "resolve_board_token" in source
    assert "get_board_credential_payload" not in source
