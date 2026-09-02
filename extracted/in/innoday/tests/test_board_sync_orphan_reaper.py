"""#613: a deploy landing mid-sync used to wedge a board forever.

`sync_board` queues a FastAPI `BackgroundTasks` task, so the run dies with the
process. Nothing marked its `board_sync_history` row afterwards, and the
already-in-progress guard refuses to start while such a row exists -- so one
interrupted deploy silently disabled sync for that board until someone passed
`--force` or edited the row by hand (which is what actually happened, twice on
the same board in four days).

Two halves are pinned here:

* **the reap** -- at startup every PENDING/IN_PROGRESS row belongs to another
  process, and only those rows are touched. Whether that process is *gone* is
  a separate question the reap cannot answer, and the row's own text must not
  pretend it can (`TestTheReapedRowOnlyClaimsWhatIsKnown`);
* **the refusal** -- when a sync really is refused, the message names the
  blocking run and `--force`, and the CLI shows what the server said rather
  than a summary of it.
"""

import json
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import BackgroundTasks, HTTPException
from sqlmodel import select

from src.domain.board import (
    BoardRegistration,
    BoardSyncHistory,
    BoardType,
    SyncStatus,
)
from src.services.board_sync_service import ORPHANED_SYNC_ERROR, reap_orphaned_syncs

COMPLETED_MESSAGE = "this one finished on its own"
FAILED_MESSAGE = "Marked failed by hand because a PENDING row blocks every later sync"


@pytest.fixture
def board(db_session, org, project):
    registration = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Atomic PE (UI)",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net/browse/AT",
        board_external_id=uuid4().hex[:8],
        is_active=True,
    )
    db_session.add(registration)
    db_session.commit()
    db_session.refresh(registration)
    return registration


def _history(session, board, user, status, *, minutes_ago=5, **kwargs):
    row = BoardSyncHistory(
        id=str(uuid4()),
        board_registration_id=board.id,
        sync_status=status,
        started_at=datetime.now(timezone.utc) - timedelta(minutes=minutes_ago),
        synced_by=user.id,
        **kwargs,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


class TestTheReaper:
    def test_a_row_the_dead_process_left_running_is_failed(
        self, db_session, board, platform_user
    ):
        """The whole point: PENDING and IN_PROGRESS both stop blocking at boot."""
        pending = _history(db_session, board, platform_user, SyncStatus.PENDING)
        in_progress = _history(db_session, board, platform_user, SyncStatus.IN_PROGRESS)

        assert reap_orphaned_syncs(db_session) == 2

        for row in (pending, in_progress):
            db_session.refresh(row)
            assert row.sync_status == SyncStatus.FAILED
            # `completed_at` is what makes it distinguishable from "still
            # running" to every reader (`board sync-status`, the summary
            # engine's freshness gate), so a status change alone is not enough.
            assert row.completed_at is not None
            assert row.error_message == ORPHANED_SYNC_ERROR

    def test_a_finished_row_is_left_exactly_as_it_was(
        self, db_session, board, platform_user
    ):
        """A blanket UPDATE would rewrite history that is already correct.

        The FAILED row matters most: its `error_message` is the record of what
        went wrong (on the real board it was a hand-written post-mortem), and
        overwriting it with the reaper's text would destroy the only account of
        the incident.
        """
        finished_at = datetime.now(timezone.utc) - timedelta(hours=3)
        completed = _history(
            db_session,
            board,
            platform_user,
            SyncStatus.COMPLETED,
            completed_at=finished_at,
            tickets_found=339,
            error_message=COMPLETED_MESSAGE,
        )
        failed = _history(
            db_session,
            board,
            platform_user,
            SyncStatus.FAILED,
            completed_at=finished_at,
            error_message=FAILED_MESSAGE,
        )

        assert reap_orphaned_syncs(db_session) == 0

        db_session.refresh(completed)
        assert completed.sync_status == SyncStatus.COMPLETED
        assert completed.error_message == COMPLETED_MESSAGE
        assert completed.tickets_found == 339

        db_session.refresh(failed)
        assert failed.sync_status == SyncStatus.FAILED
        assert failed.error_message == FAILED_MESSAGE

    def test_an_abandoned_preview_is_reaped_too(self, db_session, board, platform_user):
        """A dry run does not block a later sync, but it is no less dead.

        Left PENDING it misreports the board's history, which is the reader
        problem #584 was about.
        """
        preview = _history(
            db_session, board, platform_user, SyncStatus.IN_PROGRESS, dry_run=True
        )

        assert reap_orphaned_syncs(db_session) == 1

        db_session.refresh(preview)
        assert preview.sync_status == SyncStatus.FAILED


class TestTheReapedRowOnlyClaimsWhatIsKnown:
    """The reap is unscoped -- no board, org or process filter -- and its
    premise ("the process that owned this row is gone") fails during exactly the
    event it was written for.

    A Railway rolling deploy starts and healthchecks the new container *before*
    stopping the old one, so for the length of that window two processes exist
    and the old one's sync is still running. The mechanism is deliberately left
    alone (a surviving run writes its own terminal status at the end, so status
    converges, and age-based expiry needs an N nobody can name). What must not
    stand is the row telling the operator to go and start a second concurrent
    sync against a board that may still be syncing -- `--force` is a deliberate
    human override; this would be the system prescribing one.

    Substring assertions over a message only catch a literal revert, and that is
    what they are here for: the wording is the fix.
    """

    def test_it_does_not_pronounce_the_run_dead(self, db_session, board, platform_user):
        orphan = _history(db_session, board, platform_user, SyncStatus.IN_PROGRESS)

        assert reap_orphaned_syncs(db_session) == 1
        db_session.refresh(orphan)

        said = orphan.error_message.lower()
        assert "just sync again" not in said
        assert "that is all that is known" in said
        # It has to name the case in which the run is *not* dead, or an operator
        # reading a FAILED row has no reason to think it might still be going.
        assert "may still be alive" in said

    def test_it_still_says_why_the_row_was_touched(
        self, db_session, board, platform_user
    ):
        """Narrowing the claim must not cost the reason. A bare FAILED with no
        account of who failed it is what #613 left behind."""
        orphan = _history(db_session, board, platform_user, SyncStatus.PENDING)

        assert reap_orphaned_syncs(db_session) == 1
        db_session.refresh(orphan)

        said = orphan.error_message.lower()
        assert "restarted" in said
        assert "blocking" in said


class TestStartupRunsIt:
    """The wiring, not the function -- a reaper nothing calls fixes nothing."""

    def test_booting_the_app_clears_an_orphaned_row(
        self, db_engine, db_session, board, platform_user
    ):
        from fastapi.testclient import TestClient

        from src.api.app import app

        orphan = _history(db_session, board, platform_user, SyncStatus.IN_PROGRESS)

        # `session_scope()` reads the module-global engine, so pointing that at
        # the test engine is what keeps boot off the real database.
        with patch("src.database.engine", db_engine):
            with patch("src.api.app._assert_schema_at_head"):
                with TestClient(app):
                    pass

        db_session.refresh(orphan)
        assert orphan.sync_status == SyncStatus.FAILED
        assert orphan.error_message == ORPHANED_SYNC_ERROR

    def test_it_runs_without_a_dependency_override(
        self, db_engine, db_session, board, platform_user
    ):
        """The production path, called directly: no request, no override.

        This began as the branch every other test overrode away. It is kept
        because it is the one that runs on a real boot, and because the reaper
        swallows every exception -- so a break here has no symptom other than
        #613 continuing to happen.
        """
        from src.api.app import _reap_orphaned_syncs, app

        orphan = _history(db_session, board, platform_user, SyncStatus.PENDING)

        assert app.dependency_overrides == {}, "another test leaked an override"
        with patch("src.database.engine", db_engine):
            _reap_orphaned_syncs()

        db_session.refresh(orphan)
        assert orphan.sync_status == SyncStatus.FAILED

    def test_a_request_override_is_not_consulted_at_boot(
        self, db_engine, db_session, board, platform_user
    ):
        """Boot is not a request, so `dependency_overrides` must play no part.

        The reap used to resolve its session through that dict by hand, which
        is exactly what `get_session`'s docstring forbids (#482) -- and it made
        which database boot writes to depend on whatever a caller had installed.
        `session_scope()` is the sanctioned route and ignores the dict; an
        override that is consulted raises here, and because the reaper swallows
        everything the row simply stays PENDING.
        """
        from src.api.app import _reap_orphaned_syncs, app
        from src.database import get_session

        orphan = _history(db_session, board, platform_user, SyncStatus.PENDING)

        def _must_not_be_used():
            raise AssertionError("dependency_overrides consulted outside a request")

        app.dependency_overrides[get_session] = _must_not_be_used
        try:
            with patch("src.database.engine", db_engine):
                _reap_orphaned_syncs()
        finally:
            app.dependency_overrides.clear()

        db_session.refresh(orphan)
        assert orphan.sync_status == SyncStatus.FAILED

    def test_a_broken_reaper_does_not_stop_the_app_serving(
        self, db_engine, db_session, board, platform_user
    ):
        """Housekeeping must never become a precondition of starting.

        An unreachable database at boot would otherwise turn a deploy into an
        outage -- the reap can simply happen on the next start. (An
        *unresponsive* one is the sibling hazard, bounded by the engine's
        connect timeout -- see `TestAnUnresponsiveDatabaseCannotHangTheBoot`.)
        """
        from fastapi.testclient import TestClient

        from src.api.app import app

        orphan = _history(db_session, board, platform_user, SyncStatus.IN_PROGRESS)

        with patch("src.database.engine", db_engine):
            with patch("src.api.app._assert_schema_at_head"):
                with patch(
                    "src.services.board_sync_service.reap_orphaned_syncs",
                    side_effect=RuntimeError("database is unreachable"),
                ):
                    with TestClient(app) as client:
                        response = client.get("/health")

        assert response.status_code == 200
        # And the row is untouched, so a failed reap is a no-op rather than a
        # half-applied one.
        db_session.refresh(orphan)
        assert orphan.sync_status == SyncStatus.IN_PROGRESS


class TestAnUnresponsiveDatabaseCannotHangTheBoot:
    """The other half of "a bad database must not fail the deploy".

    `test_a_broken_reaper_does_not_stop_the_app_serving` models a database that
    is *unreachable* -- it raises immediately and is swallowed. A database that
    completes the TCP handshake and then never answers raises nothing at all,
    and psycopg2's `connect_timeout` defaults to unlimited, so before this the
    reap (the only DB call at boot) would block `lifespan` before `yield`
    forever: healthcheck fails, deploy fails.
    """

    def test_a_postgres_connect_gives_up_instead_of_blocking(self, monkeypatch):
        import socket
        import threading

        from sqlmodel import create_engine

        from src.database import connect_args_for

        # A listening socket that never `accept()`s: the kernel completes the
        # handshake from the backlog, so connect() succeeds and the startup
        # packet is then answered by nobody. This is the black-holed pooler.
        sink = socket.socket()
        sink.bind(("127.0.0.1", 0))
        sink.listen(1)
        port = sink.getsockname()[1]
        monkeypatch.setenv("INNODAY_DB_CONNECT_TIMEOUT", "2")  # libpq's minimum

        url = f"postgresql://u:p@127.0.0.1:{port}/nowhere"
        engine = create_engine(url, connect_args=connect_args_for(url))
        done = threading.Event()

        def _connect():
            try:
                with engine.connect():
                    pass
            except Exception:
                pass
            finally:
                done.set()

        worker = threading.Thread(target=_connect, daemon=True)
        worker.start()
        finished = done.wait(timeout=15)
        sink.close()

        # Asserted rather than joined-without-timeout on purpose: an unbounded
        # connect makes this thread live forever, and the failure has to be a
        # red test rather than a hung suite.
        assert finished, (
            "the connect never returned -- connect_timeout is not being applied, "
            "which is the boot hang this pins"
        )

    def test_sqlite_is_left_alone(self):
        """The timeout is a psycopg2 key. SQLite's `connect()` raises
        `TypeError` on an unknown kwarg, so applying it everywhere would break
        the entire test suite's own database rather than protect anything.
        """
        from sqlmodel import create_engine

        from src.database import connect_args_for

        assert connect_args_for("sqlite:///./innoday.db") == {}
        engine = create_engine("sqlite://", connect_args=connect_args_for("sqlite://"))
        with engine.connect():
            pass


class TestTheRefusalExplainsItself:
    @pytest.mark.asyncio
    async def test_it_names_force_and_the_run_that_is_blocking(
        self, db_session, org, board, platform_user
    ):
        """The refusal used to name neither the blocker nor the way past it."""
        from src.routers.boards import SyncRequest, sync_board

        blocking = _history(
            db_session, board, platform_user, SyncStatus.IN_PROGRESS, minutes_ago=17
        )

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"email": "a@b.c", "api_token": "t"},
        ):
            with pytest.raises(HTTPException) as exc_info:
                await sync_board(
                    organization_id=org.id,
                    board_id=board.id,
                    sync_request=SyncRequest(full_sync=True),
                    background_tasks=BackgroundTasks(),
                    token=None,
                    session=db_session,
                    current_user=platform_user,
                )

        assert exc_info.value.status_code == 429
        detail = exc_info.value.detail
        assert "--force" in detail
        assert blocking.id in detail
        assert "17 min ago" in detail

    @pytest.mark.asyncio
    async def test_forcing_past_it_still_works(
        self, db_session, org, board, platform_user
    ):
        """The advice the message gives has to be true."""
        from src.routers.boards import SyncRequest, sync_board

        _history(db_session, board, platform_user, SyncStatus.IN_PROGRESS)

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"email": "a@b.c", "api_token": "t"},
        ):
            result = await sync_board(
                organization_id=org.id,
                board_id=board.id,
                sync_request=SyncRequest(full_sync=True, force=True),
                background_tasks=BackgroundTasks(),
                token=None,
                session=db_session,
                current_user=platform_user,
            )

        assert result.sync_id
        queued = db_session.exec(
            select(BoardSyncHistory).where(
                BoardSyncHistory.id == result.sync_id,
            )
        ).first()
        assert queued is not None


class TestTheCascadeShowsWhatTheServerSaid:
    """`innoday sync` is the path most likely to meet a wedged board.

    Both handlers exit **1** on the refusal since #622 -- what they print is for
    the operator, the exit code is for the script, and it said "done" for both.
    """

    @pytest.mark.asyncio
    async def test_the_servers_detail_reaches_the_operator(self, capsys):
        from src.cli.commands.sync import SyncCommands

        detail = (
            "Sync already in progress for this board: run abc-123 started "
            "2026-08-13 23:24 UTC (17 min ago) and has not reported yet. If it "
            "is stuck, start a new sync anyway with `innoday board sync --force`."
        )

        board_response = MagicMock(status_code=200)
        board_response.json.return_value = [
            {"id": "board-1", "board_type": "jira", "board_name": "Board"}
        ]
        refusal = MagicMock(status_code=429)
        refusal.json.return_value = {"detail": detail}

        client = MagicMock()
        client.get = AsyncMock(return_value=board_response)
        client.post = AsyncMock(return_value=refusal)

        config = MagicMock()
        config.get_current_organization.return_value = "acme"
        config.get_organization_id.return_value = "org-1"

        result = await SyncCommands._sync_board(client, "org-1", "proj-1", config)

        # 1, not 0: the sync was refused, and a script reading the exit code is
        # the caller that never sees the detail below (#622).
        assert result == 1
        printed = capsys.readouterr().out
        assert "--force" in printed
        assert "abc-123" in printed
        # The success branch nine lines above prints this with the same
        # `board_id` in scope, so omitting it here gave the operator with a
        # *wedged* board less help than the one whose sync queued fine.
        #
        # **`--board-id`, not a positional.** All three assertions here pinned
        # the id bare, which is the shape the parser rejects -- so the tests
        # certified the broken advice they existed to guarantee. Fixed at four
        # print sites, with `test_printed_commands_parse.py` now checking the
        # whole CLI so the next one cannot be written.
        assert "innoday board sync-status --board-id board-1" in printed

    @pytest.mark.asyncio
    async def test_board_sync_points_at_sync_status_instead_of_saying_wait(
        self, capsys
    ):
        """`innoday board sync`'s own 429 branch, which said "please wait".

        That is the wrong advice when the blocker is a row a dead process left
        behind, and it is the branch an operator hits when they are already
        suspicious.
        """
        from src.cli.commands.boards import BoardCommands

        refusal = MagicMock(status_code=429, content=b"{}")
        refusal.json.return_value = {"detail": "Sync already in progress: run abc-123"}

        client = MagicMock()
        client.post = AsyncMock(return_value=refusal)

        config = MagicMock()
        config.get_current_organization.return_value = "acme"
        config.get_organization_id.return_value = "org-1"

        with patch.object(
            BoardCommands, "_resolve_board_id", AsyncMock(return_value="board-1")
        ):
            result = await BoardCommands._handle_sync(MagicMock(), client, config)

        assert result == 1  # refused, not done (#622)
        printed = capsys.readouterr().out
        assert "abc-123" in printed
        assert "innoday board sync-status --board-id board-1" in printed
        assert "Please wait" not in printed

    @pytest.mark.asyncio
    async def test_the_two_handlers_degrade_identically_on_an_unusable_body(
        self, capsys
    ):
        """One refusal reaches the operator down two paths, and they were fixed
        twice, separately, in different words.

        They diverged on three things -- the body guard, the fallback text, and
        whether the sync-status hint printed at all. Here the body is what a
        proxy in front of the API returns (HTML, not JSON), which exercises the
        guard: neither may traceback, and both must say the same thing.
        """
        from src.cli.commands.boards import BoardCommands
        from src.cli.commands.sync import SyncCommands

        def _html_429():
            refusal = MagicMock(status_code=429, content=b"<html>429</html>")
            refusal.json.side_effect = json.JSONDecodeError("nope", "", 0)
            return refusal

        config = MagicMock()
        config.get_current_organization.return_value = "acme"
        config.get_organization_id.return_value = "org-1"

        board_response = MagicMock(status_code=200)
        board_response.json.return_value = [
            {"id": "board-1", "board_type": "jira", "board_name": "Board"}
        ]
        cascade_client = MagicMock()
        cascade_client.get = AsyncMock(return_value=board_response)
        cascade_client.post = AsyncMock(return_value=_html_429())
        assert (
            await SyncCommands._sync_board(cascade_client, "org-1", "proj-1", config)
            == 1
        )
        cascade_output = capsys.readouterr().out

        board_client = MagicMock()
        board_client.post = AsyncMock(return_value=_html_429())
        with patch.object(
            BoardCommands, "_resolve_board_id", AsyncMock(return_value="board-1")
        ):
            assert (
                await BoardCommands._handle_sync(MagicMock(), board_client, config) == 1
            )
        board_output = capsys.readouterr().out

        for printed in (cascade_output, board_output):
            assert "Sync already in progress for this board." in printed
            assert "innoday board sync-status --board-id board-1" in printed
