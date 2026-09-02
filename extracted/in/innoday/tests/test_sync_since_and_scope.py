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
