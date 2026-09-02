"""Behaviour that only exists on Postgres, tested on Postgres.

The rest of the suite runs on in-memory SQLite. That is fine for logic, but it
cannot express two things we depend on, and one of them already cost us a silent
data-loss bug (#424):

1. **Aborted transactions.** After a failed statement Postgres refuses every later
   statement in the transaction *and* turns `COMMIT` into a `ROLLBACK` that reports
   success. SQLite has no such state, so a sync loop that swallowed a per-ticket
   error looked fine in tests and silently discarded every write in production.
2. **Row-level security, roles, `SET LOCAL`.** SQLite has none of these, so no RLS
   policy can be verified there at all. These fixtures are the prerequisite for
   making RLS real.

Runs against local Supabase (`supabase start`); skips cleanly if it isn't up.
"""

from datetime import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, InternalError, ProgrammingError


class TestAbortedTransactionSemantics:
    """Why the board-sync fix in #424 had to use SAVEPOINT."""

    def test_a_failed_statement_poisons_the_transaction(self, pg_session):
        """The behaviour SQLite cannot reproduce."""
        pg_session.execute(text("CREATE TEMPORARY TABLE t (id int)"))
        pg_session.execute(text("INSERT INTO t VALUES (1)"))

        with pytest.raises((ProgrammingError, InternalError)):
            pg_session.execute(text("SELECT from_a_table_that_does_not_exist"))

        # Every later statement is now refused until the transaction ends.
        with pytest.raises(InternalError):
            pg_session.execute(text("INSERT INTO t VALUES (2)"))

    def test_a_savepoint_contains_the_failure(self, pg_session):
        """The fix: a failure inside a SAVEPOINT leaves the outer txn usable."""
        pg_session.execute(text("CREATE TEMPORARY TABLE t (id int)"))

        for i in (1, 2, 3):
            try:
                with pg_session.begin_nested():
                    pg_session.execute(text(f"INSERT INTO t VALUES ({i})"))
                    if i == 2:
                        pg_session.execute(text("SELECT nope_"))
            except Exception:
                pass  # rolled back to the savepoint only

        rows = [r[0] for r in pg_session.execute(text("SELECT id FROM t ORDER BY id"))]
        assert rows == [1, 3], "the good writes must survive the poisoned sibling"

    def test_a_resolver_db_fault_does_not_poison_the_sync_transaction(
        self, pg_session, monkeypatch
    ):
        """`_resolve_assigned_user_id` swallows DB faults inside a SAVEPOINT.

        The resolver answers None rather than raising, which is right — an
        unresolvable assignee must not cost a ticket. But a *database* fault
        (`relation "user_identity" does not exist`, an image live ahead of
        `alembic upgrade head`) aborts the Postgres transaction, and swallowing
        that without a savepoint leaves the session unusable: every later
        statement is refused and `sync_single_ticket`'s bare `commit()` becomes
        a silent ROLLBACK. Only Postgres has that state, so only here can it
        be pinned.
        """
        from src.domain.board import BoardRegistration, BoardType
        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.domain.ticket import Ticket
        from src.services.board_sync_service import BoardSyncService
        from src.services.identity_resolution import IdentityResolutionService

        org = Organization(name="PG Org 2", alias="PGORG2", github_org="pg")
        pg_session.add(org)
        pg_session.flush()
        proj = Project(name="P2", alias="PGP2", description="d", organization_id=org.id)
        pg_session.add(proj)
        pg_session.flush()
        board = BoardRegistration(
            organization_id=org.id,
            project_id=proj.id,
            board_name="PG board",
            board_type=BoardType.LINEAR,
            board_url="https://example.invalid",
            board_external_id="EX",
        )
        pg_session.add(board)
        pg_session.flush()

        def read_a_missing_relation(session, **kwargs):
            session.execute(text("SELECT 1 FROM a_relation_that_does_not_exist"))

        monkeypatch.setattr(
            IdentityResolutionService, "resolve", read_a_missing_relation
        )

        service = BoardSyncService()
        _, ticket = service._create_or_update_ticket(
            {
                "id": "PG-1",
                "summary": "Survives a resolver fault",
                "status": "To Do",
                "assignee": "A. Lice",
            },
            board,
            pg_session,
            project_id=proj.id,
        )
        assert ticket.assigned_to is None

        # The real assertion: the transaction is still usable, so the write
        # this sync just made can actually be persisted.
        pg_session.flush()
        found = pg_session.execute(
            text("SELECT summary FROM ticket WHERE external_ticket_id = 'PG-1'")
        ).scalar()
        assert found == "Survives a resolver fault", (
            "the ticket must still be writable after the resolver hit a DB "
            "fault — without a SAVEPOINT the transaction is aborted here"
        )
        assert isinstance(ticket, Ticket)

        # The batch path nests this savepoint inside _persist_ticket's own.
        was_created, batched = service._persist_ticket(
            {
                "id": "PG-2",
                "summary": "Also survives, one savepoint deeper",
                "status": "To Do",
                "assignee": "A. Lice",
            },
            board,
            pg_session,
            proj.id,
        )
        assert was_created is True
        assert batched.assigned_to is None
        assert (
            pg_session.execute(
                text("SELECT count(*) FROM ticket WHERE external_ticket_id = 'PG-2'")
            ).scalar()
            == 1
        )

    @pytest.mark.asyncio
    async def test_a_failed_flush_does_not_lose_the_project_sync_error(self, pg_engine):
        """`_record_project_sync_error` must roll back *before* it writes (#640).

        This is the only place that line is testable at all. A sync usually dies
        with its transaction already aborted, because what killed it was a failed
        statement. Postgres then refuses every later statement *and* silently
        turns the recorder's `COMMIT` into a `ROLLBACK` while reporting success —
        so the flag the code believes it persisted is gone, and the icon stays
        green over a dead token. SQLite has no aborted state, so the default
        fixtures cannot fail this.

        **Deliberately not on the `pg_session` fixture.** That session joins an
        externally-begun transaction in SQLAlchemy's `rollback_only` mode, where
        `Session.commit()` never issues a real COMMIT and `Session.rollback()`
        rolls back the *fixture's* transaction — the two calls under test would
        both mean something other than what they mean in production, and the setup
        rows would vanish with the first one. So this test owns a real top-level
        transaction and cleans up after itself.
        """
        from unittest.mock import AsyncMock, patch

        from sqlmodel import Session

        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.services.github_connect_service import GitHubConnectService

        org_id = proj_id = None
        try:
            with Session(pg_engine) as setup:
                org = Organization(name="PG Org 640", alias="PGORG640", github_org="pg")
                setup.add(org)
                setup.flush()
                proj = Project(
                    name="P640",
                    alias="PG640",
                    description="d",
                    organization_id=org.id,
                )
                setup.add(proj)
                setup.commit()
                org_id, proj_id = org.id, proj.id

            with Session(pg_engine) as session:
                service = GitHubConnectService(session)
                service._get_github_credentials = lambda *a, **k: {
                    "token": "tok",
                    "github_org": "pg",
                }

                def poison_the_transaction(*args, **kwargs):
                    session.execute(
                        text("SELECT 1 FROM a_relation_that_does_not_exist")
                    )

                # The failure lands after the sync has already written rows, which
                # is what leaves the transaction *aborted* rather than merely
                # holding work nobody wants.
                with (
                    patch(
                        "src.api.github_api.GitHubAPI.search_organization_repositories",
                        new=AsyncMock(
                            return_value=[
                                {
                                    "id": 909090,
                                    "name": "repo-pg",
                                    "full_name": "pg/repo-pg",
                                    "html_url": "https://github.com/pg/repo-pg",
                                    "description": None,
                                    "language": "Python",
                                    "topics": ["pg640"],
                                    "archived": False,
                                    "private": False,
                                }
                            ]
                        ),
                    ),
                    patch(
                        "src.services.github_connect_service.add_timeline_entry",
                        side_effect=poison_the_transaction,
                    ),
                ):
                    with pytest.raises(Exception):
                        await service.sync_project_repositories(org_id, proj_id)

            # A session that has never seen this row: the same session's identity
            # map would answer from memory and pass whether or not anything landed.
            with Session(pg_engine) as fresh:
                recorded = fresh.get(Project, proj_id)
                assert recorded is not None
                assert recorded.github_errored_at is not None, (
                    "the sync failure must survive the aborted transaction it "
                    "happened in — without the rollback first, COMMIT is "
                    "silently downgraded to ROLLBACK and this flag is lost"
                )
                # And the rollback that made that possible took the half-applied
                # sync with it, which is the other half of why it is safe.
                assert (
                    fresh.execute(
                        text(
                            "SELECT count(*) FROM project_repositories "
                            "WHERE project_id = :p"
                        ),
                        {"p": proj_id},
                    ).scalar()
                    == 0
                )
        finally:
            with Session(pg_engine) as cleanup:
                for stmt, params in (
                    (
                        "DELETE FROM project_repositories WHERE project_id = :p",
                        {"p": proj_id},
                    ),
                    ("DELETE FROM repositories WHERE id = '909090'", {}),
                    (
                        "DELETE FROM github_sync_history WHERE project_id = :p",
                        {"p": proj_id},
                    ),
                    ("DELETE FROM projects WHERE id = :p", {"p": proj_id}),
                    ("DELETE FROM organizations WHERE id = :o", {"o": org_id}),
                ):
                    cleanup.execute(text(stmt), params)
                cleanup.commit()

    @pytest.mark.asyncio
    async def test_the_sync_record_survives_a_recorder_that_fails_too(self, pg_engine):
        """`_record_sync_history` must roll back before it writes (#650).

        **The path this exercises is the one where the rollback is the only thing
        standing between the failure and no record of it**: the sync dies, and then
        `_record_project_sync_error` -- which runs first and would otherwise have
        cleaned the transaction up as a side effect -- dies as well. That is exactly
        why the caller wraps it: its three statements (rollback, get, commit) all go
        through a connection that may have gone away behind the session, and a
        pooler restart or failover surfaces there as `OperationalError` /
        `PendingRollbackError`.

        An earlier version of this test let the error recorder succeed, and was
        vacuous as a result. By the time `_record_sync_history` ran, the session was
        neither in a transaction nor aborted -- the recorder had already rolled back
        and committed -- so the test passed with `_record_sync_history`'s own
        rollback deleted. It certified #641's rollback, not this one.

        Here the recorder raises before it can clean anything up, so the aborted
        transaction the sync died in is still current. On Postgres that means every
        later statement is refused *and* `COMMIT` is silently downgraded to
        `ROLLBACK` while reporting success: without the rollback first, the audit row
        is lost, silently, on the one path it exists for -- and no SQLite test can
        see it, because SQLite has no aborted state.

        The flag the dashboard reads is asserted **absent** on purpose. Its recorder
        was the thing that failed, so the history row is the only surviving record of
        this sync, which is precisely the situation that makes the rollback
        load-bearing rather than incidental.

        Owns a real top-level transaction rather than using `pg_session`, for the
        reason the test above documents -- that fixture's `commit()` and `rollback()`
        do not mean what they mean in production.
        """
        from unittest.mock import AsyncMock, patch

        from sqlmodel import Session

        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.services.github_connect_service import GitHubConnectService

        org_id = proj_id = None
        try:
            with Session(pg_engine) as setup:
                org = Organization(name="PG Org 650", alias="PGORG650", github_org="pg")
                setup.add(org)
                setup.flush()
                proj = Project(
                    name="P650",
                    alias="PG650",
                    description="d",
                    organization_id=org.id,
                )
                setup.add(proj)
                setup.commit()
                org_id, proj_id = org.id, proj.id

            with Session(pg_engine) as session:
                service = GitHubConnectService(session)
                service._get_github_credentials = lambda *a, **k: {
                    "token": "tok",
                    "github_org": "pg",
                }

                def poison_the_transaction(*args, **kwargs):
                    session.execute(
                        text("SELECT 1 FROM a_relation_that_does_not_exist")
                    )

                def the_recorder_dies_too(*args, **kwargs):
                    # Raises before its own rollback, the way a connection that died
                    # behind the session does: the aborted transaction is left
                    # exactly as the sync failure left it.
                    raise RuntimeError("connection went away recording the flag")

                with (
                    patch(
                        "src.api.github_api.GitHubAPI.search_organization_repositories",
                        new=AsyncMock(
                            return_value=[
                                {
                                    "id": 909650,
                                    "name": "repo-pg650",
                                    "full_name": "pg/repo-pg650",
                                    "html_url": "https://github.com/pg/repo-pg650",
                                    "description": None,
                                    "language": "Python",
                                    "topics": ["pg650"],
                                    "archived": False,
                                    "private": False,
                                }
                            ]
                        ),
                    ),
                    patch(
                        "src.services.github_connect_service.add_timeline_entry",
                        side_effect=poison_the_transaction,
                    ),
                    patch.object(
                        GitHubConnectService,
                        "_record_project_sync_error",
                        side_effect=the_recorder_dies_too,
                        autospec=True,
                    ),
                ):
                    with pytest.raises(Exception):
                        await service.sync_project_repositories(org_id, proj_id)

            with Session(pg_engine) as fresh:
                rows = fresh.execute(
                    text(
                        "SELECT status, repositories_synced, organization_id "
                        "FROM github_sync_history WHERE project_id = :p"
                    ),
                    {"p": proj_id},
                ).all()
                assert len(rows) == 1, (
                    "the record of a failed sync must survive the aborted "
                    "transaction it happened in — without the rollback first, "
                    "COMMIT is silently downgraded to ROLLBACK and this row is "
                    "lost exactly when it was needed"
                )
                status, discovered, recorded_org = rows[0]
                assert status == "failed"
                assert discovered == 1, "what it had got to before it died"
                # The tenant, which is what makes the row attributable and what the
                # RLS policy keys on. Nothing created a registration for this org and
                # nothing needs one: #658 dropped that column with the org-wide sync.
                assert recorded_org == org_id

                # The flag never landed: its recorder was the thing that failed. So
                # this row is the only record that the sync ran at all, which is what
                # makes the rollback above load-bearing.
                assert fresh.get(Project, proj_id).github_errored_at is None
        finally:
            with Session(pg_engine) as cleanup:
                for stmt, params in (
                    (
                        "DELETE FROM github_sync_history WHERE project_id = :p",
                        {"p": proj_id},
                    ),
                    (
                        "DELETE FROM project_repositories WHERE project_id = :p",
                        {"p": proj_id},
                    ),
                    ("DELETE FROM repositories WHERE id = '909650'", {}),
                    ("DELETE FROM projects WHERE id = :p", {"p": proj_id}),
                    ("DELETE FROM organizations WHERE id = :o", {"o": org_id}),
                ):
                    cleanup.execute(text(stmt), params)
                cleanup.commit()

    @pytest.mark.asyncio
    async def test_a_board_syncs_failure_survives_the_transaction_it_died_in(
        self, pg_engine
    ):
        """`sync_board_tickets`' error handler must roll back before it writes (#652).

        **The highest-harm case of this class, because the loss is not merely an
        absent record — it disables the board.** `sync_board` refuses to start while
        a PENDING/IN_PROGRESS row exists, and the 30-minute scheduler posts with
        `force=False`. So when the FAILED write is lost, the row stays IN_PROGRESS
        and that board **429s every thirty minutes** until an API restart lets
        `reap_orphaned_syncs` clear it — while the dashboard icon stays green,
        because `BoardRegistration.errored_at` was lost in the very same downgraded
        commit. Every signal that something was wrong is produced by the same bug.

        The mechanism is the one this class exists for: the sync dies of a failed
        *statement*, which on Postgres leaves the transaction aborted, and `COMMIT`
        on an aborted transaction is silently downgraded to `ROLLBACK` while
        reporting success. SQLite has no such state, so no fixture in the default
        suite can fail this — with `session.rollback()` deleted from
        `_record_sync_failure`, the whole SQLite suite still passes.

        `_get_adapter` is what reads the missing relation here. *Where* the sync
        dies does not matter to the mechanism — only that the transaction is
        aborted by the time the handler runs — and failing there keeps the test to
        the thing under test rather than standing up a working board adapter.

        **Not on the `pg_session` fixture**, for the reason the two tests above
        document: that session joins an externally-begun transaction, where
        `commit()` issues no real COMMIT and `rollback()` discards the setup rows.
        `sync_board_tickets` opens its own `Session(engine)`, so the module's
        `engine` is pointed at the test database instead.
        """
        from unittest.mock import patch

        from sqlmodel import Session

        from src.domain.board import (
            BoardRegistration,
            BoardSyncHistory,
            BoardType,
            SyncStatus,
        )
        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.services import board_sync_service as bss

        org_id = proj_id = board_id = history_id = None
        try:
            with Session(pg_engine) as setup:
                org = Organization(name="PG Org 652", alias="PGORG652", github_org="pg")
                setup.add(org)
                setup.flush()
                proj = Project(
                    name="P652",
                    alias="PG652",
                    description="d",
                    organization_id=org.id,
                )
                setup.add(proj)
                setup.flush()
                board = BoardRegistration(
                    organization_id=org.id,
                    project_id=proj.id,
                    board_name="PG board 652",
                    board_type=BoardType.LINEAR,
                    board_url="https://example.invalid",
                    board_external_id="EX652",
                )
                setup.add(board)
                setup.flush()
                # `started_at` is left to the model's own default (naive UTC),
                # which is also what the production writers do.
                history = BoardSyncHistory(
                    board_registration_id=board.id,
                    sync_status=SyncStatus.PENDING,
                )
                setup.add(history)
                setup.commit()
                org_id, proj_id = org.id, proj.id
                board_id, history_id = board.id, history.id

            def read_a_missing_relation(self, registration, token, session):
                # A failed statement, not a bare `raise`: the aborted transaction is
                # the whole subject, and an exception on its own would not create one.
                session.execute(text("SELECT 1 FROM a_relation_that_does_not_exist"))

            with (
                patch.object(bss, "engine", pg_engine),
                patch.object(
                    bss.BoardSyncService, "_get_adapter", read_a_missing_relation
                ),
            ):
                # Reports failure by returning, not by raising — see the method's
                # docstring and `summary_service._run_board_sync`.
                result = await bss.BoardSyncService().sync_board_tickets(
                    registration_id=board_id,
                    sync_history_id=history_id,
                    token="tok",
                )

            assert result["success"] is False

            # The message handed back to a reader must not be the raw exception.
            # `str(ProgrammingError)` is the failing SQL; this one goes into the
            # summary payload's `sync_error`.
            assert "a_relation_that_does_not_exist" not in result["error_message"]
            assert "SELECT" not in result["error_message"]

            with Session(pg_engine) as fresh:
                row = fresh.get(BoardSyncHistory, history_id)
                assert row is not None
                assert row.sync_status == SyncStatus.FAILED, (
                    "the FAILED write must survive the aborted transaction the sync "
                    "died in — without the rollback first, COMMIT is silently "
                    "downgraded to ROLLBACK, the row stays IN_PROGRESS, and this "
                    "board then 429s every 30 minutes until the API restarts"
                )
                assert row.completed_at is not None
                assert row.error_message
                assert "a_relation_that_does_not_exist" not in row.error_message

                registration = fresh.get(BoardRegistration, board_id)
                assert registration is not None
                assert registration.errored_at is not None, (
                    "the flag the dashboard icon reads is written in the same "
                    "transaction, so it is lost by the same downgraded commit — "
                    "which is why the board stayed green while it was broken"
                )
                assert registration.error_message
        finally:
            with Session(pg_engine) as cleanup:
                for stmt, params in (
                    (
                        "DELETE FROM board_sync_history WHERE board_registration_id "
                        "= :b",
                        {"b": board_id},
                    ),
                    ("DELETE FROM ticket WHERE project_id = :p", {"p": proj_id}),
                    ("DELETE FROM board_registrations WHERE id = :b", {"b": board_id}),
                    ("DELETE FROM projects WHERE id = :p", {"p": proj_id}),
                    ("DELETE FROM organizations WHERE id = :o", {"o": org_id}),
                ):
                    cleanup.execute(text(stmt), params)
                cleanup.commit()

    def test_ref_number_is_unique_per_project_not_per_org(self, pg_session, pg_engine):
        """The #424 constraint, re-keyed to the project.

        Both halves matter and the second is the point of the change. Asserting
        only that *a* collision is refused would pass just as well against the
        old organisation-scoped constraint, so it would not distinguish the two
        and would not notice a revert.
        """
        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.domain.ticket import Ticket

        org = Organization(name="PG Org", alias="PGORG", github_org="pg")
        pg_session.add(org)
        pg_session.flush()
        first = Project(name="P", alias="PGP", description="d", organization_id=org.id)
        second = Project(name="Q", alias="PGQ", description="d", organization_id=org.id)
        pg_session.add_all([first, second])
        pg_session.flush()

        def ticket(project, ref, ext):
            return Ticket(
                summary=ext,
                organization_id=org.id,
                project_id=project.id,
                external_ticket_id=ext,
                project_ref_number=ref,
            )

        # Two projects in one org may now both have a #1 -- the whole reason for
        # the change, and what the old constraint made impossible.
        pg_session.add(ticket(first, 1, "A"))
        pg_session.add(ticket(second, 1, "B"))
        pg_session.flush()

        # Within one project it is still refused.
        pg_session.add(ticket(first, 1, "C"))
        with pytest.raises(IntegrityError):
            pg_session.flush()


class TestTicketCommentColumnTypes:
    """`ticket_comment.commenter_id` holds a UUID string, and Postgres cares.

    The column's own note records why this is here: it was **created as an
    integer** while `users.id` is a UUID string, which 500'd every write that
    reached it. It has been fixed, and the personal scrum update is the first
    thing to write it in anger.

    **SQLite cannot fail this.** Its column types are advisory -- a UUID string
    goes into an `INTEGER` column without complaint and comes back out as itself
    -- so the entire suite could be green over the same defect. Which is exactly
    what happened before: the bug shipped.
    """

    def test_a_comment_round_trips_with_a_uuid_author_on_postgres(self, pg_session):
        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.domain.ticket import Ticket, TicketComment
        from src.domain.user import User

        author = User(email="commenter-pg@example.com", full_name="Ada Lovelace")
        pg_session.add(author)
        org = Organization(name="PG Comments", alias="PGCOM", github_org="pg")
        pg_session.add(org)
        pg_session.flush()
        project = Project(
            name="C", alias="PGCOMP", description="d", organization_id=org.id
        )
        pg_session.add(project)
        pg_session.flush()
        ticket = Ticket(
            summary="a ticket somebody said something about",
            organization_id=org.id,
            project_id=project.id,
        )
        pg_session.add(ticket)
        pg_session.flush()

        pg_session.add(
            TicketComment(
                ticket_id=ticket.id,
                commenter_id=author.id,
                comment="first line\nsecond line",
            )
        )
        pg_session.flush()

        stored = pg_session.execute(
            text(
                "SELECT commenter_id, comment FROM ticket_comment WHERE ticket_id = :t"
            ),
            {"t": ticket.id},
        ).one()
        # Read back as a string, character for character, rather than as
        # whatever an integer column would have coerced the UUID into.
        assert stored[0] == author.id
        assert isinstance(stored[0], str)
        assert "-" in stored[0], "a UUID that lost its hyphens is a truncated UUID"
        assert stored[1] == "first line\nsecond line"

        # And the column is declared as text on the live schema, not merely
        # tolerant of one value.
        declared = pg_session.execute(
            text(
                "SELECT data_type FROM information_schema.columns "
                "WHERE table_name = 'ticket_comment' AND column_name = 'commenter_id'"
            )
        ).scalar()
        assert declared in ("character varying", "text"), declared

    def test_a_scrum_visit_remembers_which_comment_it_delivered(self, pg_session):
        """`scrum_ticket_visits.comment_id` really points at `ticket_comment`.

        The FK is the idempotence marker's integrity: a daily update is
        re-enterable all day, so a marker that could point at nothing would let
        the same sentence be posted to a client's board again and again.

        **Every other column is valid**, deliberately. A visit built with a bogus
        `scrum_id` *and* a bogus `comment_id` raises an `IntegrityError` either
        way, so it would pass identically with no comment FK at all -- a check
        that cannot fail for the reason it names.
        """
        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.domain.scrum import Scrum, ScrumKind, ScrumTicketVisit
        from src.domain.ticket import Ticket
        from src.domain.user import User

        runner = User(email="visit-pg@example.com", full_name="Grace Hopper")
        pg_session.add(runner)
        org = Organization(name="PG Visits", alias="PGVIS", github_org="pg")
        pg_session.add(org)
        pg_session.flush()
        project = Project(
            name="V", alias="PGVISP", description="d", organization_id=org.id
        )
        pg_session.add(project)
        pg_session.flush()
        ticket = Ticket(
            summary="walked past", organization_id=org.id, project_id=project.id
        )
        began = datetime.utcnow()
        scrum = Scrum(
            organization_id=org.id,
            project_id=project.id,
            run_by_user_id=runner.id,
            kind=ScrumKind.UPDATE.value,
            started_at=began,
            day=began.date(),
        )
        pg_session.add_all([ticket, scrum])
        pg_session.flush()

        def visit(position, **kw):
            return ScrumTicketVisit(
                scrum_id=scrum.id,
                ticket_id=ticket.id,
                position=position,
                seconds=0,
                status_at_visit="done",
                **kw,
            )

        # Everything but `comment_id` is real, so this row inserts cleanly --
        # which is what makes the refusal below attributable.
        with pg_session.begin_nested():
            pg_session.add(visit(0))
            pg_session.flush()

        with pytest.raises(IntegrityError) as caught:
            with pg_session.begin_nested():
                pg_session.add(visit(1, comment_id=987654321))
                pg_session.flush()
        assert "comment_id" in str(caught.value)


class TestRLSPrerequisites:
    """What makes RLS testable at all — task #8 builds on these."""

    def test_the_app_role_bypasses_rls_which_is_the_whole_problem(self, pg_session):
        """Documents why a policy test must not run as the app's own role.

        The app connects as `postgres` (rolbypassrls = true), so every policy is
        skipped for it. A "policy test" as that role passes regardless of what the
        policy says — which is exactly how 32 RLS-enabled tables with 0 policies
        went unnoticed.
        """
        bypasses = pg_session.execute(
            text("SELECT rolbypassrls FROM pg_roles WHERE rolname = current_user")
        ).scalar()
        assert bypasses is True, (
            "expected the app role to bypass RLS; if this changed, the RLS work in "
            "task #8 has started and these tests need revisiting"
        )

    def test_the_rls_test_role_does_not_bypass(self, pg_session, rls_role):
        """SET ROLE gives us a role policies actually apply to."""
        pg_session.execute(text(f"SET LOCAL ROLE {rls_role}"))
        name, is_super, bypasses = pg_session.execute(
            text(
                "SELECT rolname, rolsuper, rolbypassrls FROM pg_roles "
                "WHERE rolname = current_user"
            )
        ).first()
        assert name == rls_role
        assert not is_super and not bypasses

    def test_set_local_is_scoped_to_the_transaction(self, pg_session):
        """How a tenant claim will be propagated, and why it must be LOCAL.

        Dev connects through the transaction-mode pooler, which recycles a
        connection at transaction end. A plain SET would leak the previous
        request's tenant to the next caller; SET LOCAL cannot.
        """
        pg_session.execute(text("SET LOCAL app.current_user_id = 'user-123'"))
        got = pg_session.execute(
            text("SELECT current_setting('app.current_user_id', true)")
        ).scalar()
        assert got == "user-123"

    def test_a_policy_actually_filters_rows_for_this_role(self, pg_session, rls_role):
        """End-to-end proof that a policy keyed on a GUC works.

        This is the shape task #8 needs: identity in a setting, policy compares
        against it, and the role cannot see rows that don't match.
        """
        pg_session.execute(text("CREATE TEMPORARY TABLE scoped (id int, owner text)"))
        pg_session.execute(text("INSERT INTO scoped VALUES (1, 'alice'), (2, 'bob')"))
        pg_session.execute(text("ALTER TABLE scoped ENABLE ROW LEVEL SECURITY"))
        pg_session.execute(
            text(
                "CREATE POLICY own_rows ON scoped USING "
                "(owner = current_setting('app.current_user_id', true))"
            )
        )
        pg_session.execute(text(f"GRANT SELECT ON scoped TO {rls_role}"))

        # Switch to the role policies apply to. Without this the table's owner
        # (postgres) is exempt and every row comes back — the trap that makes a
        # policy test look like it passes when nothing is being enforced.
        pg_session.execute(text(f"SET LOCAL ROLE {rls_role}"))

        pg_session.execute(text("SET LOCAL app.current_user_id = 'alice'"))
        assert [
            r[0] for r in pg_session.execute(text("SELECT id FROM scoped ORDER BY id"))
        ] == [1], "policy should hide bob's row from alice"

        pg_session.execute(text("SET LOCAL app.current_user_id = 'bob'"))
        assert [
            r[0] for r in pg_session.execute(text("SELECT id FROM scoped ORDER BY id"))
        ] == [2]

        # And with no claim set at all, nothing is visible — the deny-by-default
        # property RLS is supposed to give.
        pg_session.execute(text("SET LOCAL app.current_user_id = ''"))
        assert pg_session.execute(text("SELECT count(*) FROM scoped")).scalar() == 0, (
            "an unset claim must not see rows"
        )
