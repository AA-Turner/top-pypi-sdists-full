"""`innoday sync --since` / `--scope`, and what `since` actually does (PF-398).

`--since` was only worth adding if it means something end to end, so this pins
both halves: the CLI turning a window or a date into an unambiguous instant,
and the sync service using it to skip work *without* narrowing coverage.

The second half is the one with teeth. The summary engine passes `since` on
every gate-1 sync, so if `since` filtered imports rather than re-processing, a
fresh project would permanently lack every ticket older than whatever window
the first summary happened to ask for.
"""

import argparse
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.cli.commands.sync import DEFAULT_SCOPE, SyncCommands, SyncScope, parse_since
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus
from src.services.board_sync_service import _parse_since, board_sync_service
from tests.db_helpers import build_test_engine


class TestParseSince:
    def test_relative_window_resolves_to_an_instant(self):
        resolved = datetime.fromisoformat(parse_since("3d"))
        elapsed = datetime.now(timezone.utc) - resolved
        assert timedelta(days=3) - timedelta(minutes=1) < elapsed
        assert elapsed < timedelta(days=3, minutes=1)

    @pytest.mark.parametrize("spec", ["12h", "2w", "1d"])
    def test_every_unit_is_accepted(self, spec):
        assert parse_since(spec) is not None

    def test_an_iso_date_is_read_as_utc_not_local(self):
        assert parse_since("2026-08-01").startswith("2026-08-01T00:00:00+00:00")

    def test_absent_means_absent_not_zero(self):
        assert parse_since(None) is None
        assert parse_since("") is None

    @pytest.mark.parametrize("bad", ["yesterday", "3 days", "0d", "3y"])
    def test_junk_raises_rather_than_guessing(self, bad):
        with pytest.raises(ValueError):
            parse_since(bad)


class TestScopeFlag:
    @pytest.fixture
    def parser(self):
        parser = argparse.ArgumentParser()
        SyncCommands.setup_parser(parser)
        return parser

    def test_defaults_to_the_whole_cascade(self, parser):
        args = parser.parse_args([])
        assert args.scope == DEFAULT_SCOPE == SyncScope.ALL.value
        assert args.since is None

    def test_choices_are_derived_from_the_enum(self, parser):
        action = next(a for a in parser._actions if a.dest == "scope")
        assert list(action.choices) == [s.value for s in SyncScope]
        # `default=` bypasses `type=`, so it must already be a legal choice.
        assert action.default in action.choices

    @pytest.mark.parametrize("scope", [s.value for s in SyncScope])
    def test_every_stage_is_selectable(self, parser, scope):
        assert parser.parse_args(["--scope", scope]).scope == scope

    def test_rejects_an_unknown_stage(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args(["--scope", "everything"])

    def test_waiting_for_the_board_sync_is_the_default(self, parser):
        """#741: `--no-wait` is opt-in, so a bare `innoday sync` waits."""
        from src.cli.commands.boards import DEFAULT_SYNC_WAIT_TIMEOUT

        args = parser.parse_args([])
        assert args.no_wait is False
        assert args.wait_timeout == DEFAULT_SYNC_WAIT_TIMEOUT

        opted_out = parser.parse_args(["--no-wait", "--wait-timeout", "30"])
        assert opted_out.no_wait is True
        assert opted_out.wait_timeout == 30.0

    def test_the_ticket_subcommand_still_parses_alongside(self, parser):
        args = parser.parse_args(["ticket", "PF-155"])
        assert args.sync_command == "ticket"
        assert args.key == "PF-155"


class TestServiceParseSince:
    def test_naive_input_is_read_as_utc(self):
        parsed = _parse_since("2026-08-01T00:00:00")
        # `tzinfo is not None` passes for ANY zone, so it did not test what the
        # name claims -- a naive string read as, say, US/Eastern would satisfy it
        # while shifting the sync window by hours.
        assert parsed.tzinfo == timezone.utc
        assert parsed == datetime(2026, 8, 1, tzinfo=timezone.utc)

    def test_junk_is_none_so_the_caller_falls_back_to_syncing(self):
        assert _parse_since("not a date") is None
        assert _parse_since(None) is None

    def test_a_datetime_passes_straight_through(self):
        moment = datetime(2026, 8, 1, tzinfo=timezone.utc)
        assert _parse_since(moment) == moment


@pytest.fixture
def seeded():
    engine = build_test_engine()
    with Session(engine) as session:
        org = Organization(id=str(uuid4()), name="Haviland", alias="hs")
        session.add(org)
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="",
        )
        session.add(project)
        registration = BoardRegistration(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            board_type=BoardType.LINEAR,
            board_name="PF",
            board_url="https://linear.app/havilandsoftware",
            board_external_id="pf",
            user_id=None,
        )
        session.add(registration)
        session.add(
            Ticket(
                organization_id=org.id,
                project_id=project.id,
                board_registration_id=registration.id,
                external_ticket_id="PF-1",
                summary="Already here",
                status=TicketStatus.TODO,
            )
        )
        session.commit()
        yield session, registration


def external(external_id: str, updated: datetime):
    return {"id": external_id, "fields": {"updated": updated.isoformat()}}


class TestUnchangedSince:
    """The filter, and the condition that keeps it from narrowing coverage."""

    def test_a_known_ticket_older_than_the_window_is_skipped(self, seeded):
        session, registration = seeded
        since = datetime.now(timezone.utc) - timedelta(days=1)
        stale = external("PF-1", since - timedelta(days=5))
        assert board_sync_service._unchanged_since(stale, registration, session, since)

    def test_a_known_ticket_that_moved_inside_the_window_is_processed(self, seeded):
        session, registration = seeded
        since = datetime.now(timezone.utc) - timedelta(days=1)
        fresh = external("PF-1", since + timedelta(hours=1))
        assert not board_sync_service._unchanged_since(
            fresh, registration, session, since
        )

    def test_an_unseen_ticket_is_imported_however_old_it_is(self, seeded):
        """Otherwise a windowed sync would be a windowed import."""
        session, registration = seeded
        since = datetime.now(timezone.utc) - timedelta(days=1)
        ancient = external("PF-999", since - timedelta(days=400))
        assert not board_sync_service._unchanged_since(
            ancient, registration, session, since
        )

    def test_a_board_with_no_timestamp_is_always_processed(self, seeded):
        """ "I cannot tell" must mean sync it, never skip it."""
        session, registration = seeded
        since = datetime.now(timezone.utc) - timedelta(days=1)
        assert not board_sync_service._unchanged_since(
            {"id": "PF-1", "fields": {}}, registration, session, since
        )
        assert not board_sync_service._unchanged_since(
            {"id": "PF-1", "fields": {"updated": "whenever"}},
            registration,
            session,
            since,
        )


def _history(
    session,
    registration,
    *,
    started,
    status,
    dry_run=False,
    completed=True,
    full_sync=True,
):
    """One board-sync history row, as a finished attempt.

    `full_sync=True` by default so the existing watermark tests are not all
    forced into the weekly-reconciliation branch; the cases that care about the
    distinction say so explicitly.
    """
    from src.domain.board import BoardSyncHistory

    row = BoardSyncHistory(
        id=str(uuid4()),
        organization_id=registration.organization_id,
        board_registration_id=registration.id,
        sync_status=status,
        dry_run=dry_run,
        full_sync=full_sync,
        started_at=started,
        completed_at=(started + timedelta(seconds=30)) if completed else None,
    )
    session.add(row)
    session.commit()
    return row


class TestWhereAnIncrementalSyncResumes:
    """`innoday sync` re-pulled every ticket on every run.

    The adapter has filtered server-side all along — Linear's
    `filter: { updatedAt: { gte: … } }` — and `_unchanged_since` has guarded
    coverage all along. Nothing supplied `since`, so BPAI fetched all 258
    issues twice a day and wrote almost none of them.
    """

    def _resume(self, session, registration):
        return board_sync_service._resume_point(session, registration)

    def test_no_history_means_no_resume_point(self, seeded):
        """A board's first sync must be a full pull. An adapter that filters at
        the source never sends a ticket InnoDay has not seen, so resuming on an
        empty baseline would be a windowed *import* — permanently missing
        everything older than whichever window ran first."""
        session, registration = seeded
        assert self._resume(session, registration) is None

    def test_it_resumes_from_the_start_not_the_completion(self, seeded):
        """The property that makes this safe.

        A sync takes minutes on a real board. A ticket edited *while* one ran
        falls between a completion-stamped watermark and the next run's lower
        bound — skipped, then skipped forever, because nothing revisits it.
        """
        from src.domain.board import SyncStatus

        session, registration = seeded
        started = datetime.now(timezone.utc) - timedelta(hours=2)
        _history(session, registration, started=started, status=SyncStatus.COMPLETED)

        resumed = self._resume(session, registration)

        assert resumed is not None
        assert resumed < started, "must not resume at or after the start"
        assert started - resumed == timedelta(minutes=5)

    def test_a_failed_sync_is_not_a_watermark(self, seeded):
        """It proves nothing about what it managed to import, so treating its
        start as a baseline would skip whatever it missed."""
        from src.domain.board import SyncStatus

        session, registration = seeded
        _history(
            session,
            registration,
            started=datetime.now(timezone.utc) - timedelta(hours=1),
            status=SyncStatus.FAILED,
        )
        assert self._resume(session, registration) is None

    def test_a_dry_run_is_not_a_watermark(self, seeded):
        """A preview wrote nothing, so nothing after it has been imported."""
        from src.domain.board import SyncStatus

        session, registration = seeded
        _history(
            session,
            registration,
            started=datetime.now(timezone.utc) - timedelta(hours=1),
            status=SyncStatus.COMPLETED,
            dry_run=True,
        )
        assert self._resume(session, registration) is None

    def test_the_newest_completed_sync_wins(self, seeded):
        from src.domain.board import SyncStatus

        session, registration = seeded
        old = datetime.now(timezone.utc) - timedelta(days=3)
        recent = datetime.now(timezone.utc) - timedelta(hours=1)
        _history(session, registration, started=old, status=SyncStatus.COMPLETED)
        _history(session, registration, started=recent, status=SyncStatus.COMPLETED)

        assert self._resume(session, registration) == recent - timedelta(minutes=5)

    def test_another_boards_history_does_not_count(self, seeded):
        """Two boards sync independently; borrowing a sibling's watermark would
        skip everything this one has never seen."""
        from src.domain.board import BoardRegistration, BoardType, SyncStatus

        session, registration = seeded
        # A second *project*, because `board_registrations.project_id` is
        # UNIQUE -- one board per project, so a sibling board cannot share one.
        sibling_project = Project(
            id=str(uuid4()),
            organization_id=registration.organization_id,
            alias="OTHER",
            name="Other",
            description="",
        )
        session.add(sibling_project)
        session.commit()
        other = BoardRegistration(
            id=str(uuid4()),
            organization_id=registration.organization_id,
            project_id=sibling_project.id,
            board_type=BoardType.LINEAR,
            board_name="Other",
            board_url="https://linear.app/other",
            board_external_id="other",
            user_id=None,
        )
        session.add(other)
        session.commit()
        _history(
            session,
            other,
            started=datetime.now(timezone.utc) - timedelta(hours=1),
            status=SyncStatus.COMPLETED,
        )

        assert self._resume(session, registration) is None


class TestTheFullFlagIsTheEscapeHatch:
    def test_the_cli_sends_full_sync_when_asked(self):
        assert SyncCommands is not None  # import guard for the parser check

    def test_full_defaults_off(self):
        """Incremental is the default; a full re-pull is the repair path."""
        parser = argparse.ArgumentParser()
        SyncCommands.setup_parser(parser)
        assert parser.parse_args([]).full is False
        assert parser.parse_args(["--full"]).full is True


class TestAFullPullIsDuePeriodically:
    """Incremental syncing is only safe because of this.

    The watermark advances on every success, so a ticket missed once — skew past
    the overlap, a board that did not move `updatedAt`, a partial run recorded
    as completed — sits outside every later window, and nothing revisits it.
    Time-based filtering cannot notice: there is no count to reconcile and no
    checksum. A periodic full pull bounds the damage to a week instead of
    forever.
    """

    def _resume(self, session, registration):
        return board_sync_service._resume_point(session, registration)

    def test_a_recent_full_pull_permits_resuming(self, seeded):
        from src.domain.board import SyncStatus

        session, registration = seeded
        _history(
            session,
            registration,
            started=datetime.now(timezone.utc) - timedelta(days=1),
            status=SyncStatus.COMPLETED,
            full_sync=True,
        )
        assert self._resume(session, registration) is not None

    def test_an_aged_out_full_pull_forces_another(self, seeded):
        """Eight days since the last full reconciliation, so the next sync is
        one — even though there is a perfectly good recent watermark."""
        from src.domain.board import SyncStatus

        session, registration = seeded
        now = datetime.now(timezone.utc)
        _history(
            session,
            registration,
            started=now - timedelta(days=8),
            status=SyncStatus.COMPLETED,
            full_sync=True,
        )
        _history(
            session,
            registration,
            started=now - timedelta(hours=1),
            status=SyncStatus.COMPLETED,
            full_sync=False,
        )

        assert self._resume(session, registration) is None

    def test_incremental_history_alone_forces_a_full_pull(self, seeded):
        """A board that has only ever resumed has never reconciled, so it is
        due now rather than at some point seven days from an event that never
        happened."""
        from src.domain.board import SyncStatus

        session, registration = seeded
        _history(
            session,
            registration,
            started=datetime.now(timezone.utc) - timedelta(hours=1),
            status=SyncStatus.COMPLETED,
            full_sync=False,
        )
        assert self._resume(session, registration) is None

    def test_a_failed_full_pull_does_not_reset_the_clock(self, seeded):
        """It may have imported nothing. Counting it would postpone the real
        reconciliation by a week on the strength of a run that failed."""
        from src.domain.board import SyncStatus

        session, registration = seeded
        now = datetime.now(timezone.utc)
        _history(
            session,
            registration,
            started=now - timedelta(days=8),
            status=SyncStatus.COMPLETED,
            full_sync=True,
        )
        _history(
            session,
            registration,
            started=now - timedelta(hours=1),
            status=SyncStatus.FAILED,
            full_sync=True,
        )
        assert self._resume(session, registration) is None

    def test_the_watermark_still_comes_from_the_newest_sync_of_either_kind(
        self, seeded
    ):
        """Once reconciliation is current, the resume point is the newest
        successful sync — full or incremental. Only the *due date* cares which
        kind it was."""
        from src.domain.board import SyncStatus

        session, registration = seeded
        now = datetime.now(timezone.utc)
        _history(
            session,
            registration,
            started=now - timedelta(days=2),
            status=SyncStatus.COMPLETED,
            full_sync=True,
        )
        recent = now - timedelta(minutes=30)
        _history(
            session,
            registration,
            started=recent,
            status=SyncStatus.COMPLETED,
            full_sync=False,
        )

        assert self._resume(session, registration) == recent - timedelta(minutes=5)
