"""Regression tests for the board-sync correctness bugs in #417.

Two HIGH findings, both silent — they corrupt data or misreport success rather
than raising. Neither had any test cover, which is how both shipped.

1. ``project_ref_number`` was assigned by read-max-then-insert with no lock and no
   unique constraint, so two syncs mint the same user-facing id.
2. A per-ticket failure was swallowed without ``rollback()``, poisoning the
   transaction so the batch ``commit()`` silently dropped every write — while
   the result dict still reported ``success`` and positive created counts.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.domain.board import BoardRegistration, BoardType
from src.domain.ticket import Ticket
from src.services import board_sync_service as bss
from src.services.board_sync_service import BoardSyncService


@pytest.fixture
def board(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Sync Board",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net",
        board_external_id="example",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


def _external(ticket_id: str, summary: str = "t") -> dict:
    return {
        "id": ticket_id,
        "summary": summary,
        "description": None,
        "status": "backlog",
        "assignee": None,
        "url": None,
        "source_platform": "jira",
        "priority": None,
        "parent_external_id": None,
    }


class TestProjectRefNumberUniqueness:
    """Bug 1 — duplicate user-facing ticket ids."""

    def test_refs_are_unique_within_one_batch(self, db_session, board):
        """A batch must not hand the same ref to two tickets.

        ``_create_or_update_ticket`` only ``add()``s; the caller commits once
        per batch. Without a flush, ``max()`` cannot see earlier tickets from
        the same batch, so every ticket in the batch would get ref 1.
        """
        service = BoardSyncService()
        for i in range(3):
            service._create_or_update_ticket(
                _external(f"E-{i}"), board, db_session, project_id=board.project_id
            )
        db_session.commit()

        refs = [t.project_ref_number for t in db_session.exec(select(Ticket)).all()]
        assert sorted(refs) == [
            1,
            2,
            3,
        ], f"expected distinct sequential refs, got {refs}"

    def test_duplicate_ref_is_rejected_by_the_database(self, db_session, board, org):
        """The constraint — not just the read — is what makes the race safe."""
        db_session.add(
            Ticket(
                summary="a",
                organization_id=org.id,
                project_id=board.project_id,
                board_registration_id=board.id,
                external_ticket_id="X-1",
                project_ref_number=5,
            )
        )
        db_session.commit()

        db_session.add(
            Ticket(
                summary="b",
                organization_id=org.id,
                project_id=board.project_id,
                board_registration_id=board.id,
                external_ticket_id="X-2",
                project_ref_number=5,  # same project, same ref
            )
        )
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_same_ref_allowed_in_a_different_project(self, db_session, board, org):
        """The constraint is project-scoped, not global -- and not org-scoped.

        Two projects in the *same* organisation may both hold ref 1. That was
        impossible while the constraint keyed on ``organization_id``, and it is
        what lets a project keep its numbering when it moves between orgs.
        """
        from src.domain.project import Project

        # Same organisation, deliberately -- that is the case the old
        # org-scoped constraint rejected.
        sibling = Project(
            name="Sibling Project",
            alias="SIB",
            description="Second project in the same org",
            organization_id=org.id,
        )
        db_session.add(sibling)
        db_session.commit()
        db_session.refresh(sibling)

        db_session.add(
            Ticket(
                summary="a",
                organization_id=org.id,
                project_id=board.project_id,
                board_registration_id=board.id,
                external_ticket_id="Y-1",
                project_ref_number=1,
            )
        )
        db_session.add(
            Ticket(
                summary="b",
                organization_id=org.id,
                project_id=sibling.id,
                external_ticket_id="Y-2",
                project_ref_number=1,
            )
        )
        db_session.commit()  # must not raise

    def test_null_refs_do_not_collide(self, db_session, board, org):
        """Tickets created outside sync have no ref; NULLs must not conflict."""
        for n in ("N-1", "N-2"):
            db_session.add(
                Ticket(
                    summary=n,
                    organization_id=org.id,
                    project_id=board.project_id,
                    board_registration_id=board.id,
                    external_ticket_id=n,
                    project_ref_number=None,
                )
            )
        db_session.commit()  # must not raise

    def test_a_lost_race_is_retried_with_a_fresh_number(
        self, db_session, board, org, monkeypatch
    ):
        """The constraint stops the corruption; the retry stops it becoming an error.

        Simulates a concurrent sync taking the number between our read and our
        insert by making the first ref computation return an already-taken value.
        """
        db_session.add(
            Ticket(
                summary="incumbent",
                organization_id=org.id,
                project_id=board.project_id,
                board_registration_id=board.id,
                external_ticket_id="R-0",
                project_ref_number=1,
            )
        )
        db_session.commit()

        service = BoardSyncService()
        real = service._next_project_ref_number
        calls = []

        def racy(session, organization_id):
            calls.append(organization_id)
            if len(calls) == 1:
                return 1  # already taken -> IntegrityError inside the savepoint
            return real(session, organization_id)

        monkeypatch.setattr(service, "_next_project_ref_number", racy)

        _, ticket = service._persist_ticket(
            _external("R-1"), board, db_session, board.project_id
        )
        db_session.commit()

        assert len(calls) == 2, "the collision should have triggered exactly one retry"
        assert ticket.project_ref_number == 2, (
            f"retry should claim the next free number, got {ticket.project_ref_number}"
        )

    def test_a_different_violation_is_not_retried(
        self, db_session, board, org, monkeypatch
    ):
        """Only the ref race is retried — other IntegrityErrors must propagate."""
        service = BoardSyncService()
        attempts = []

        def exploding(external_ticket, registration, session, project_id):
            attempts.append(1)
            # A duplicate external id -- uq_ticket_board_external, not the ref
            # constraint. Retrying this would loop pointlessly.
            t = Ticket(
                summary="dup",
                organization_id=org.id,
                project_id=board.project_id,
                board_registration_id=board.id,
                external_ticket_id="DUP",
                project_ref_number=None,
            )
            session.add(t)
            return True, t

        db_session.add(
            Ticket(
                summary="first",
                organization_id=org.id,
                project_id=board.project_id,
                board_registration_id=board.id,
                external_ticket_id="DUP",
            )
        )
        db_session.commit()

        monkeypatch.setattr(service, "_create_or_update_ticket", exploding)
        with pytest.raises(IntegrityError):
            service._persist_ticket(
                _external("DUP"), board, db_session, board.project_id
            )
        db_session.rollback()
        assert len(attempts) == 1, "a non-ref violation must not be retried"


def _fake_adapter(tickets):
    """An adapter yielding ``Ticket`` domain objects, as the real ones do."""
    adapter = AsyncMock()
    adapter.initialize = AsyncMock(return_value=None)
    adapter.get_tickets = AsyncMock(return_value=tickets)
    return adapter


def _sync_history(session, board):
    from src.domain.board import BoardSyncHistory, SyncStatus

    h = BoardSyncHistory(
        board_registration_id=board.id,
        sync_status=SyncStatus.PENDING,
    )
    session.add(h)
    session.commit()
    session.refresh(h)
    return h


class TestTheSinceWatermark:
    """`options["since"]` must reach the adapter, not be dropped on the floor.

    The summary engine passed `{"full_sync": False, "since": ...}` with a
    comment claiming the pull was "scoped to the window". `sync_board_tickets`
    read exactly one key -- `dry_run` -- and `since` appeared nowhere in this
    module, so what gate 1 awaited inside a synchronous GET was a full board
    pull. The only test on it asserted against the *stub's* argument, which
    pinned nothing about this.
    """

    @pytest.mark.asyncio
    async def test_since_is_passed_down_to_the_adapter(
        self, db_engine, db_session, board, monkeypatch
    ):
        """...but only once the board has a baseline. See the first-sync test."""
        monkeypatch.setattr(bss, "engine", db_engine)
        board.last_sync_at = datetime(2026, 7, 30, tzinfo=timezone.utc)
        db_session.add(board)
        db_session.commit()
        history = _sync_history(db_session, board)
        service = BoardSyncService()
        adapter = _fake_adapter([])
        monkeypatch.setattr(service, "_get_adapter", AsyncMock(return_value=adapter))

        since = datetime(2026, 8, 1, 9, 30, tzinfo=timezone.utc)
        await service.sync_board_tickets(
            board.id, history.id, token="tok", options={"since": since.isoformat()}
        )

        adapter.get_tickets.assert_awaited_once_with(
            board.board_external_id, since=since
        )

    @pytest.mark.asyncio
    async def test_a_first_sync_ignores_since_and_pulls_everything(
        self, db_engine, db_session, board, monkeypatch
    ):
        """A windowed *fetch* on a board with no baseline is a windowed import.

        Adapters that honour `since` filter at the source, so a ticket InnoDay
        has never seen simply never arrives -- and `_unchanged_since`, which
        exists to protect unseen tickets, never gets to see it. The summary
        engine passes a window on every gate-1 sync, so without this guard the
        first summary anyone asked for would decide, permanently, how far back
        the project's history goes.
        """
        monkeypatch.setattr(bss, "engine", db_engine)
        assert board.last_sync_at is None
        history = _sync_history(db_session, board)
        service = BoardSyncService()
        adapter = _fake_adapter([])
        monkeypatch.setattr(service, "_get_adapter", AsyncMock(return_value=adapter))

        since = datetime(2026, 8, 1, 9, 30, tzinfo=timezone.utc)
        await service.sync_board_tickets(
            board.id, history.id, token="tok", options={"since": since.isoformat()}
        )

        adapter.get_tickets.assert_awaited_once_with(board.board_external_id)

    @pytest.mark.asyncio
    async def test_no_since_leaves_the_call_exactly_as_it_was(
        self, db_engine, db_session, board, monkeypatch
    ):
        """Default sync behaviour is unchanged -- no kwarg, no narrowing."""
        monkeypatch.setattr(bss, "engine", db_engine)
        history = _sync_history(db_session, board)
        service = BoardSyncService()
        adapter = _fake_adapter([])
        monkeypatch.setattr(service, "_get_adapter", AsyncMock(return_value=adapter))

        await service.sync_board_tickets(board.id, history.id, token="tok")

        adapter.get_tickets.assert_awaited_once_with(board.board_external_id)

    @pytest.mark.asyncio
    async def test_an_unparseable_since_degrades_to_a_full_pull(
        self, db_engine, db_session, board, monkeypatch
    ):
        """A malformed option must not fail a sync that would otherwise work."""
        monkeypatch.setattr(bss, "engine", db_engine)
        history = _sync_history(db_session, board)
        service = BoardSyncService()
        adapter = _fake_adapter([])
        monkeypatch.setattr(service, "_get_adapter", AsyncMock(return_value=adapter))

        result = await service.sync_board_tickets(
            board.id, history.id, token="tok", options={"since": "last tuesday"}
        )

        assert result["success"] is True
        adapter.get_tickets.assert_awaited_once_with(board.board_external_id)

    def test_every_adapter_accepts_the_watermark(self):
        """`since` is on the interface, so no adapter TypeErrors when it is passed."""
        import inspect

        from src.adapters.base_adapter import BaseBoardAdapter
        from src.adapters.jira_adapter import JiraBoardAdapter
        from src.adapters.linear_adapter import LinearBoardAdapter
        from src.adapters.notion_adapter import NotionBoardAdapter
        from src.adapters.trello_adapter import TrelloBoardAdapter

        for cls in (
            BaseBoardAdapter,
            JiraBoardAdapter,
            LinearBoardAdapter,
            NotionBoardAdapter,
            TrelloBoardAdapter,
        ):
            params = inspect.signature(cls.get_tickets).parameters
            assert "since" in params, f"{cls.__name__}.get_tickets lacks `since`"
            assert params["since"].default is None, (
                f"{cls.__name__}.get_tickets must default `since` to None"
            )


class TestPoisonedTransaction:
    """Bug 2 — a swallowed per-ticket error silently voided the whole sync.

    **The data-loss symptom cannot be reproduced on SQLite.** Measured against
    both backends: after a failed statement Postgres refuses every later
    statement in the transaction *and* turns the batch ``COMMIT`` into a silent
    ``ROLLBACK`` that reports success — so the sync claimed rows were created
    and wrote none. SQLite never enters that state and happily persists the
    surrounding writes.

    So the tests below pin the structural guarantee (a SAVEPOINT per ticket,
    which contains the failure identically on both backends) plus the
    success-reporting bug, which *is* portable.
    """

    @pytest.mark.asyncio
    async def test_one_bad_ticket_does_not_drop_the_good_ones(
        self, db_engine, db_session, board, monkeypatch
    ):
        """Ticket 2 hits a DB error; tickets 1 and 3 must still persist."""
        monkeypatch.setattr(bss, "engine", db_engine)
        history = _sync_history(db_session, board)

        service = BoardSyncService()
        source = [
            Ticket(
                summary=f"summary {i}",
                organization_id=board.organization_id,
                external_ticket_id=f"P-{i}",
            )
            for i in range(3)
        ]
        monkeypatch.setattr(
            service, "_get_adapter", AsyncMock(return_value=_fake_adapter(source))
        )

        real = service._create_or_update_ticket
        calls = {"n": 0}

        def flaky(external_ticket, registration, session, project_id=None):
            calls["n"] += 1
            if calls["n"] == 2:
                # A DB-level error is what marks the transaction rollback-only;
                # a plain ValueError would not reproduce the bug.
                session.execute(text("SELECT from_a_missing_table_"))
            return real(external_ticket, registration, session, project_id)

        monkeypatch.setattr(service, "_create_or_update_ticket", flaky)

        result = await service.sync_board_tickets(board.id, history.id, token="tok")

        with Session(db_engine) as check:
            persisted = check.exec(select(Ticket)).all()

        assert result["tickets_skipped"] == 1
        assert result["tickets_created"] == 2
        assert len(persisted) == 2, (
            "the two healthy tickets must survive one poisoned sibling; "
            f"persisted={[t.external_ticket_id for t in persisted]}"
        )

    @pytest.mark.asyncio
    async def test_each_ticket_writes_inside_its_own_savepoint(
        self, db_engine, db_session, board, monkeypatch
    ):
        """The structural guarantee that makes Postgres safe.

        Asserted directly because the symptom it prevents is invisible on
        SQLite — without a savepoint per ticket there is nothing to roll back
        to, and on Postgres the whole batch is lost.
        """
        from sqlalchemy import event

        monkeypatch.setattr(bss, "engine", db_engine)
        history = _sync_history(db_session, board)

        savepoints = []

        @event.listens_for(db_engine, "savepoint")
        def _record(conn, name):  # pragma: no cover - event hook
            savepoints.append(name)

        try:
            service = BoardSyncService()
            source = [
                Ticket(
                    summary=f"s{i}",
                    organization_id=board.organization_id,
                    external_ticket_id=f"S-{i}",
                )
                for i in range(3)
            ]
            monkeypatch.setattr(
                service, "_get_adapter", AsyncMock(return_value=_fake_adapter(source))
            )
            await service.sync_board_tickets(board.id, history.id, token="tok")
        finally:
            event.remove(db_engine, "savepoint", _record)

        assert len(savepoints) >= 3, (
            "expected one savepoint per ticket so a failure can be contained; "
            f"saw {len(savepoints)}"
        )

    @pytest.mark.asyncio
    async def test_all_tickets_failing_is_not_reported_as_success(
        self, db_engine, db_session, board, monkeypatch
    ):
        """``results['success'] = True`` was set unconditionally."""
        monkeypatch.setattr(bss, "engine", db_engine)
        history = _sync_history(db_session, board)

        service = BoardSyncService()
        source = [
            Ticket(
                summary=f"s{i}",
                organization_id=board.organization_id,
                external_ticket_id=f"F-{i}",
            )
            for i in range(3)
        ]
        monkeypatch.setattr(
            service, "_get_adapter", AsyncMock(return_value=_fake_adapter(source))
        )
        monkeypatch.setattr(
            service,
            "_create_or_update_ticket",
            lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("boom")),
        )

        result = await service.sync_board_tickets(board.id, history.id, token="tok")

        assert result["tickets_skipped"] == 3
        assert result["tickets_created"] == 0
        assert result["success"] is False, (
            "a sync where every ticket failed must not report success"
        )


class TestTheWatermarkAndSoftDeletion:
    """`_unchanged_since` treated a soft-deleted row as "already have it"."""

    def _idle_external(self, ticket_id: str, updated: str) -> dict:
        payload = _external(ticket_id)
        payload["fields"] = {"updated": updated}
        return payload

    def test_a_soft_deleted_ticket_still_at_source_is_not_skipped(
        self, db_session, board
    ):
        """It is skipped, so the revive path never runs and it never comes back.

        `_create_or_update_ticket` clears `deleted_at` for anything still
        present at the board, but only a ticket that is actually *processed*
        reaches it. The summary engine passes `since` on every gate-1 sync, so
        this was the normal path, not an edge case.
        """
        service = BoardSyncService()
        deleted = Ticket(
            organization_id=board.organization_id,
            project_id=board.project_id,
            board_registration_id=board.id,
            external_ticket_id="T-1",
            summary="cleared from InnoDay",
            deleted_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
        )
        db_session.add(deleted)
        db_session.commit()

        since = datetime(2026, 8, 5, tzinfo=timezone.utc)
        assert (
            service._unchanged_since(
                self._idle_external("T-1", "2026-07-01T00:00:00Z"),
                board,
                db_session,
                since,
            )
            is False
        )

    def test_a_live_idle_ticket_is_still_skipped(self, db_session, board):
        """The control: the watermark must keep doing what it is for."""
        service = BoardSyncService()
        db_session.add(
            Ticket(
                organization_id=board.organization_id,
                project_id=board.project_id,
                board_registration_id=board.id,
                external_ticket_id="T-2",
                summary="quietly idle",
            )
        )
        db_session.commit()

        since = datetime(2026, 8, 5, tzinfo=timezone.utc)
        assert (
            service._unchanged_since(
                self._idle_external("T-2", "2026-07-01T00:00:00Z"),
                board,
                db_session,
                since,
            )
            is True
        )


class TestReopeningClearsCompletedAt:
    """`completed_at` survived a DONE -> IN_PROGRESS transition.

    `_completed_at_from` returns None for every non-DONE status, and the update
    path only wrote the field when it was non-None -- so the old timestamp
    stayed. `SummaryService._activity_at` reads `completed_at` as evidence of a
    real terminal transition, so a reopened ticket looked like in-window work
    for as long as the window covered the date it was originally closed.
    """

    def _external_with_status(self, ticket_id: str, status: str, updated: str) -> dict:
        payload = _external(ticket_id)
        payload["status"] = status
        payload["fields"] = {"updated": updated, "resolutiondate": updated}
        return payload

    def test_reopening_clears_the_stale_completion_time(self, db_session, board):
        from src.domain.ticket import TicketStatus

        service = BoardSyncService()
        service._create_or_update_ticket(
            self._external_with_status("T-9", "done", "2026-08-01T00:00:00Z"),
            board,
            db_session,
            board.project_id,
        )
        db_session.commit()
        stored = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "T-9")
        ).one()
        assert stored.status is TicketStatus.DONE
        assert stored.completed_at is not None

        service._create_or_update_ticket(
            self._external_with_status("T-9", "in progress", "2026-08-06T00:00:00Z"),
            board,
            db_session,
            board.project_id,
        )
        db_session.commit()
        db_session.refresh(stored)
        assert stored.status is not TicketStatus.DONE
        assert stored.completed_at is None

    def test_a_done_ticket_the_board_dated_nothing_keeps_its_timestamp(
        self, db_session, board
    ):
        """The behaviour the old condition was protecting, still protected."""
        service = BoardSyncService()
        service._create_or_update_ticket(
            self._external_with_status("T-10", "done", "2026-08-01T00:00:00Z"),
            board,
            db_session,
            board.project_id,
        )
        db_session.commit()
        stored = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "T-10")
        ).one()
        original = stored.completed_at
        assert original is not None

        undated = _external("T-10")
        undated["status"] = "done"
        service._create_or_update_ticket(undated, board, db_session, board.project_id)
        db_session.commit()
        db_session.refresh(stored)
        assert stored.completed_at == original
