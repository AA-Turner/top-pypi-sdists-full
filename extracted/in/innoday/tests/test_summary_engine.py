"""The summary engine's three gates and its assembly rules (PF-398).

Each gate gets its own test, because each one is an escape hatch that is
invisible when it works: a cache that never hits, a sync that fires on every
read, or a fingerprint that calls a changed board "unchanged" all produce a
*plausible* summary and no error at all. The two bugs design review caught --
keying the cache on a computed timestamp, and fingerprinting commits only --
are pinned here by name.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.board import BoardRegistration, BoardSyncHistory, BoardType, SyncStatus
from src.domain.organization import Organization, OrganizationMembership
from src.domain.project import Project
from src.domain.project_timeline import ProjectTimeline, TimelineEventType
from src.domain.summary import (
    Attribution,
    GeneratedBy,
    Summary,
    SummaryItem,
    SummaryType,
)
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, UserIdentity
from src.routers.summaries import SummaryItemPayload
from src.services.code_activity import (
    CodeActivity,
    extract_ticket_ref,
    ticket_ref_pattern,
)
from src.services.summary_service import (
    ACTIVE_CAP,
    BLOCK_CAP,
    RELEASE_SPAN_CAP,
    RELEASE_SPAN_FALLBACK,
    Block,
    InvalidWindowSpec,
    SummaryLine,
    SummaryOutcome,
    SummaryService,
    as_utc,
    parse_window_spec,
)
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine

NOW = datetime(2026, 8, 5, 12, 0, tzinfo=timezone.utc)


# ------------------------------------------------------------------- doubles


class StubFetcher:
    """A `CodeActivityFetcher` that answers from a list instead of GitHub."""

    def __init__(self, activities: Optional[List[CodeActivity]] = None) -> None:
        self.activities = list(activities or [])
        self.calls = 0

    async def fetch(self, *, project, since, until=None):
        self.calls += 1
        return list(self.activities)


class SyncSpy:
    """Records whether gate 1 decided to sync, without syncing anything."""

    def __init__(self) -> None:
        self.calls: List[tuple] = []

    async def __call__(self, project, since, now, requested_by):
        self.calls.append((project.id, since, now, requested_by))
        return True


class ReplayingSync:
    """A sync runner that writes what a **real** no-op board sync writes.

    Every other double here writes nothing, which is why 40 tests watched gate 1
    fire and none of them noticed what it did to the rows underneath. This one
    feeds each ticket's own current state back through the same
    `_create_or_update_ticket` the adapter path uses -- the board said nothing
    new, and nothing should move.
    """

    def __init__(self, session, board) -> None:
        self.session = session
        self.board = board
        self.calls = 0

    async def __call__(self, project, since, now, requested_by):
        from src.services.board_sync_service import BoardSyncService

        self.calls += 1
        svc = BoardSyncService()
        tickets = list(
            self.session.exec(select(Ticket).where(Ticket.project_id == project.id))
        )
        for ticket in tickets:
            external = svc._ticket_to_external_dict(ticket, self.board)
            svc._create_or_update_ticket(external, self.board, self.session, project.id)
        self.session.commit()
        return True


class HangingSync:
    """A sync that never finishes -- what a full board pull looks like to a GET."""

    def __init__(self) -> None:
        self.started = False

    async def __call__(self, project, since, now, requested_by):
        import asyncio

        self.started = True
        await asyncio.sleep(3600)
        return True


# ------------------------------------------------------------------ fixtures


@pytest.fixture
def db_engine():
    engine = build_test_engine()
    return engine


@pytest.fixture
def session(db_engine):
    with Session(db_engine) as s:
        yield s


@pytest.fixture
def org(session):
    o = Organization(id=str(uuid4()), name="Summary Org", alias=f"s{uuid4().hex[:8]}")
    session.add(o)
    session.commit()
    return o


@pytest.fixture
def project(session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias="PF",
        name="Pixelfuel",
        description="engine fixture",
    )
    session.add(p)
    session.commit()
    return p


@pytest.fixture
def user(session):
    u = User(
        id=str(uuid4()),
        email=f"{uuid4().hex[:8]}@example.com",
        full_name="Ada Lovelace",
        is_platform_member=True,
    )
    session.add(u)
    session.commit()
    return u


@pytest.fixture
def board(session, org, project, user):
    b = BoardRegistration(
        id=str(uuid4()),
        user_id=user.id,
        organization_id=org.id,
        project_id=project.id,
        board_name="PF board",
        board_url="https://linear.app/pf",
        board_type=BoardType.LINEAR,
        board_external_id="PF",
    )
    session.add(b)
    session.commit()
    return b


def make_ticket(
    session,
    org,
    project,
    *,
    summary="A ticket",
    assignee=None,
    assigned_to=None,
    status=TicketStatus.IN_PROGRESS,
    updated_at=None,
    ref=None,
    board=None,
    source_platform=None,
    completed_at=None,
    release=None,
) -> Ticket:
    ticket = Ticket(
        summary=summary,
        release=release,
        organization_id=org.id,
        project_id=project.id,
        assignee=assignee,
        assigned_to=assigned_to,
        status=status,
        external_ticket_id=ref,
        board_registration_id=board.id if board is not None else None,
        source_platform=source_platform,
        completed_at=completed_at,
        updated_at=updated_at or (NOW - timedelta(days=30)),
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


def record_sync(session, board, *, completed_at, synced_by):
    history = BoardSyncHistory(
        board_registration_id=board.id,
        sync_status=SyncStatus.COMPLETED,
        started_at=completed_at - timedelta(minutes=1),
        completed_at=completed_at,
        synced_by=synced_by,
    )
    session.add(history)
    session.commit()
    return history


def service(session, *, activities=None, sync_runner=None) -> SummaryService:
    return SummaryService(
        session,
        activity_fetcher=StubFetcher(activities),
        sync_runner=sync_runner or SyncSpy(),
    )


# =========================================================== gate 1: freshness


class TestFreshnessGate:
    @pytest.mark.asyncio
    async def test_a_sync_under_an_hour_old_triggers_no_sync(
        self, session, org, project, board, user
    ):
        """A summary is a read. It must not make every read cost a board sync."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=10), synced_by=user.id
        )
        spy = SyncSpy()
        svc = service(session, sync_runner=spy)

        result = await svc.assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert spy.calls == []
        assert result.synced is False

    @pytest.mark.asyncio
    async def test_a_stale_sync_triggers_exactly_one(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(hours=5), synced_by=user.id
        )
        spy = SyncSpy()
        svc = service(session, sync_runner=spy)

        await svc.assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert len(spy.calls) == 1
        # Scoped to the window, not to all of history.
        assert spy.calls[0][1] == NOW - timedelta(days=3)

    @pytest.mark.asyncio
    async def test_an_unfinished_sync_is_not_freshness(
        self, session, org, project, board, user
    ):
        """A run still in progress proves nothing about the data on disk.

        The half this can prove on SQLite. The half it *cannot* --  that a
        pending run must not mask a genuinely fresh completed one -- is a
        Postgres NULLS-FIRST fact and lives in `TestPostgresGuarantees`.
        """
        session.add(
            BoardSyncHistory(
                board_registration_id=board.id,
                sync_status=SyncStatus.IN_PROGRESS,
                started_at=NOW - timedelta(minutes=2),
                completed_at=None,
                synced_by=user.id,
            )
        )
        session.commit()
        spy = SyncSpy()

        await service(session, sync_runner=spy).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )
        assert len(spy.calls) == 1

    @pytest.mark.asyncio
    async def test_a_failed_run_is_not_freshness_either(
        self, session, org, project, board, user
    ):
        """A failed sync carries a `completed_at`, so the timestamp alone lies.

        `sync_board_tickets`' error path stamps `completed_at` on the way out.
        Without checking the status too, a board whose credential expired would
        report "synced 5 minutes ago" and suppress every retry for an hour.
        """
        failed = BoardSyncHistory(
            board_registration_id=board.id,
            sync_status=SyncStatus.FAILED,
            started_at=NOW - timedelta(minutes=6),
            completed_at=NOW - timedelta(minutes=5),
            synced_by=user.id,
            error_message="401 from the board",
        )
        session.add(failed)
        session.commit()

        spy = SyncSpy()
        await service(session, sync_runner=spy).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )
        assert len(spy.calls) == 1

    @pytest.mark.asyncio
    async def test_a_sync_that_fails_is_not_reported_as_synced(
        self, session, org, project, board, user
    ):
        """`sync_board_tickets` reports failure by *returning*, not by raising.

        It catches everything, writes FAILED to the history row and hands back
        ``{"success": False, "error_message": ...}``. `_run_board_sync` used to
        ignore that return and answer True unconditionally, so the payload said
        `synced: true` over tickets the board had never delivered -- which is
        the worst possible shape, because a summary of stale data looks exactly
        like a quiet week. Measured on the live dev instance: every Linear sync
        had been failing on a GraphQL validation error for days while every
        summary claimed to be fresh.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(hours=5), synced_by=user.id
        )

        async def failing_sync(**kwargs):
            return {
                "success": False,
                "error_message": "Linear returned HTTP 400: unknown type",
            }

        # The real `_run_board_sync`, deliberately: `SyncSpy` returns True
        # unconditionally, which is exactly the bug being pinned. A double here
        # would make the test pass against the unfixed code.
        svc = SummaryService(session, activity_fetcher=StubFetcher())
        with (
            patch(
                "src.services.board_credential_service.get_board_credential_payload",
                return_value={"token": "t"},
            ),
            patch(
                "src.services.board_sync_service.board_sync_service.sync_board_tickets",
                side_effect=failing_sync,
            ),
        ):
            result = await svc.assemble(
                project=project,
                summary_type=SummaryType.SCRUM,
                window_spec="3d",
                now=NOW,
            )

        assert result.synced is False
        # ...and the reason travels with it, because "not synced" alone cannot
        # be acted on -- no board and a revoked credential are the same flag.
        assert "400" in (result.sync_error or "")
        assert result.to_dict()["sync_error"] == result.sync_error

    @pytest.mark.asyncio
    async def test_a_hanging_sync_falls_through_to_stale_data(
        self, session, org, project, board, user
    ):
        """A full board pull inside a GET must not become a 504.

        Gate 1 awaits its sync, so an unbounded await hands the timeout decision
        to whatever proxy is in front of the request -- and a gateway timeout
        kills the response before the soft-fail path can return anything. The
        engine bounds the wait itself and summarises what is already on disk.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(hours=5), synced_by=user.id
        )
        make_ticket(session, org, project, summary="already here", assignee="Ada")
        hanging = HangingSync()

        with patch("src.services.summary_service.SYNC_TIMEOUT_SECONDS", 0.05):
            result = await service(session, sync_runner=hanging).assemble(
                project=project,
                summary_type=SummaryType.SCRUM,
                window_spec="3d",
                now=NOW,
            )

        assert hanging.started is True
        assert result.synced is False
        assert result.outcome is SummaryOutcome.ASSEMBLED
        assert [line.ticket_summary for line in result.no_work_detected] == [
            "already here"
        ]


class TestASyncThatActuallyWrites:
    """What gate 1's sync does to the rows the assembly then reads.

    Every other sync double in this file writes nothing, so 40 tests exercised
    gate 1 without once observing its effect. A board sync that restamped
    `updated_at` on every ticket it saw -- change or no change -- inverted every
    block below, and none of them noticed.
    """

    @staticmethod
    def _seed(session, org, project, board):
        """2 tickets with real code, 20 assigned and idle, 10 unassigned backlog."""
        activities = []
        for n in range(2):
            make_ticket(
                session,
                org,
                project,
                summary=f"real work {n}",
                assignee="Ada",
                ref=f"PF-{n}",
                board=board,
                source_platform="linear",
                updated_at=NOW - timedelta(hours=n + 1),
            )
            activities.append(
                CodeActivity(
                    repo="innoday",
                    ticket_ref=f"PF-{n}",
                    author_handle="ada",
                    occurred_at=NOW - timedelta(hours=n + 1),
                    commit_shas=(f"sha{n}",),
                )
            )
        for n in range(20):
            make_ticket(
                session,
                org,
                project,
                summary=f"assigned, untouched for 90 days {n}",
                assignee="Ada",
                ref=f"PF-1{n:02d}",
                board=board,
                source_platform="linear",
                updated_at=NOW - timedelta(days=90),
            )
        for n in range(10):
            make_ticket(
                session,
                org,
                project,
                summary=f"unassigned backlog {n}",
                status=TicketStatus.BACKLOG,
                ref=f"PF-2{n:02d}",
                board=board,
                source_platform="linear",
                updated_at=NOW - timedelta(days=90),
            )
        return activities

    @pytest.mark.asyncio
    async def test_a_no_op_sync_does_not_turn_a_stale_board_into_active_work(
        self, session, org, project, board, user
    ):
        """The measured inversion, pinned.

        With `updated_at` restamped unconditionally the numbers below came back
        22 / 0 / 0 / 10 instead of 2 / 20 / 10 / 0: `no_work_detected`
        permanently empty, the unassigned backlog **enumerated** rather than
        counted, and the five active slots filled by whichever rows an unordered
        SELECT returned first.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(hours=5), synced_by=user.id
        )
        activities = self._seed(session, org, project, board)
        replay = ReplayingSync(session, board)

        result = await SummaryService(
            session,
            activity_fetcher=StubFetcher(activities),
            sync_runner=replay,
        ).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert replay.calls == 1, "gate 1 must actually have run the sync"
        assert result.active_total == 2
        assert result.no_work_total == 20
        assert result.unassigned_idle_count == 10
        assert result.unassigned_active == []
        assert [line.ticket_summary for line in result.active] == [
            "real work 0",
            "real work 1",
        ]

    @pytest.mark.asyncio
    async def test_a_no_op_sync_leaves_updated_at_alone(
        self, session, org, project, board, user
    ):
        """The fix at source: `updated_at` means "this ticket changed".

        Correct independent of summaries -- an unconditional restamp destroys
        the column's meaning for every consumer and makes any future
        incremental-sync watermark useless.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(hours=5), synced_by=user.id
        )
        self._seed(session, org, project, board)
        before = {
            t.id: t.updated_at
            for t in session.exec(select(Ticket).where(Ticket.project_id == project.id))
        }

        await ReplayingSync(session, board)(project, NOW - timedelta(days=3), NOW, None)

        after = {
            t.id: t.updated_at
            for t in session.exec(select(Ticket).where(Ticket.project_id == project.id))
        }
        assert after == before

    @pytest.mark.asyncio
    async def test_a_real_board_change_still_restamps(
        self, session, org, project, board, user
    ):
        """The comparison must not turn the restamp off altogether."""
        ticket = make_ticket(
            session,
            org,
            project,
            summary="was called this",
            assignee="Ada",
            ref="PF-500",
            board=board,
            source_platform="linear",
        )
        before = ticket.updated_at

        from src.services.board_sync_service import BoardSyncService

        svc = BoardSyncService()
        external = svc._ticket_to_external_dict(ticket, board)
        external["summary"] = "renamed on the board"
        svc._create_or_update_ticket(external, board, session, project.id)
        session.commit()
        session.refresh(ticket)

        assert ticket.summary == "renamed on the board"
        assert ticket.updated_at > before


# =============================================================== gate 2: cache


def persist_summary(
    session,
    svc,
    org,
    project,
    *,
    window_spec="3d",
    body="the prose",
    fingerprint=None,
    user_id=None,
    created_at=None,
) -> Summary:
    summary = svc.persist(
        organization_id=org.id,
        project=project,
        summary_type=SummaryType.PERSONAL if user_id else SummaryType.SCRUM,
        window_spec=window_spec,
        body_markdown=body,
        items=[],
        source_fingerprint=fingerprint or {},
        user_id=user_id,
        period_start=NOW - timedelta(days=3),
        period_end=NOW,
    )
    if created_at is not None:
        summary.created_at = created_at
    session.commit()
    return summary


class TestCacheGate:
    @pytest.mark.asyncio
    async def test_a_live_summary_under_an_hour_old_is_returned_verbatim(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        svc = service(session)
        persist_summary(session, svc, org, project, body="cached prose", created_at=NOW)

        fetcher = StubFetcher()
        svc2 = SummaryService(session, activity_fetcher=fetcher, sync_runner=SyncSpy())
        result = await svc2.assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW + timedelta(minutes=1),
        )

        assert result.outcome is SummaryOutcome.CACHED
        assert result.body_markdown == "cached prose"
        # Short-circuited before any work: GitHub was never asked.
        assert fetcher.calls == 0

    @pytest.mark.asyncio
    async def test_two_runs_thirty_minutes_apart_hit_the_cache(
        self, session, org, project, board, user
    ):
        """The regression this whole design turns on.

        Both runs ask for "the last 3 days". Their resolved `period_start`s are
        30 minutes apart and would never compare equal -- a cache keyed on those
        timestamps would miss every single time while looking like it worked.
        Keying on `window_spec` is what makes the second run a hit.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        first = NOW
        svc = service(session)
        stored = persist_summary(
            session, svc, org, project, body="written once", created_at=first
        )

        second = first + timedelta(minutes=30)
        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=second,
        )

        assert result.outcome is SummaryOutcome.CACHED
        assert result.summary.id == stored.id
        assert result.period_start != stored.period_start  # the window did move
        assert result.body_markdown == "written once"

    @pytest.mark.asyncio
    async def test_a_different_window_spec_is_a_different_question(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        svc = service(session)
        persist_summary(session, svc, org, project, window_spec="3d", created_at=NOW)

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="1w",
            now=NOW,
        )
        assert result.outcome is SummaryOutcome.ASSEMBLED

    @pytest.mark.asyncio
    async def test_a_superseded_summary_is_not_a_cache_hit(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        svc = service(session)
        first = persist_summary(session, svc, org, project, created_at=NOW)
        second = persist_summary(
            session, svc, org, project, body="replacement", created_at=NOW
        )
        session.refresh(first)
        assert first.superseded_by_id == second.id

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )
        assert result.summary.id == second.id


# ========================================================= gate 3: fingerprint


class TestFingerprintGate:
    def test_the_fingerprint_covers_ticket_state_not_only_commits(
        self, session, org, project
    ):
        """A ticket that moves with no new code must not look unchanged."""
        ticket = make_ticket(session, org, project, status=TicketStatus.TODO)
        activity = CodeActivity(repo="innoday", commit_shas=("abc123",))

        before = SummaryService.compute_fingerprint([ticket], [activity])
        ticket.status = TicketStatus.IN_REVIEW
        after = SummaryService.compute_fingerprint([ticket], [activity])

        assert before != after
        assert before["commits"] == after["commits"] == ["abc123"]

    def test_a_ticket_with_no_commits_still_fingerprints(self, session, org, project):
        """Otherwise its fingerprint is permanently empty, so permanently equal."""
        ticket = make_ticket(session, org, project)
        fingerprint = SummaryService.compute_fingerprint([ticket], [])
        assert fingerprint["commits"] == []
        assert fingerprint["tickets"]

    @pytest.mark.asyncio
    async def test_identical_sources_reuse_the_prose_and_restamp_the_window(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        ticket = make_ticket(session, org, project, assignee="Ada")
        activities = [CodeActivity(repo="innoday", commit_shas=("deadbee",))]
        fingerprint = SummaryService.compute_fingerprint([ticket], activities)

        svc = service(session, activities=activities)
        stored = persist_summary(
            session,
            svc,
            org,
            project,
            body="unchanged prose",
            fingerprint=fingerprint,
            # Older than the cache TTL, so gate 2 cannot answer this.
            created_at=NOW - timedelta(hours=2),
        )

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.outcome is SummaryOutcome.UNCHANGED
        assert result.body_markdown == "unchanged prose"
        session.commit()
        session.refresh(stored)
        assert as_utc(stored.period_end) == NOW
        assert as_utc(stored.period_start) == NOW - timedelta(days=3)
        # Restamped, not superseded: the content did not change.
        assert stored.superseded_by_id is None

    def test_it_covers_open_prs_whose_commits_github_will_not_report(
        self, session, org, project
    ):
        """`get_commits` answers on the **default branch only**.

        For an open PR `commit_shas` is empty, so a fingerprint over commits and
        ticket state alone is byte-identical after a week of pushes to the
        branch -- and the gate serves back stale prose. The PR's own
        `updated_at` moves on every push, which is enough.
        """
        ticket = make_ticket(session, org, project, ref="PF-1")
        monday = CodeActivity(
            repo="innoday",
            ticket_ref="PF-1",
            pr_url="https://github.com/x/y/pull/9",
            pr_state="open",
            occurred_at=NOW - timedelta(days=2),
            commit_shas=(),  # unmerged: GitHub reports none on the default branch
        )
        friday = CodeActivity(
            repo="innoday",
            ticket_ref="PF-1",
            pr_url="https://github.com/x/y/pull/9",
            pr_state="open",
            occurred_at=NOW,
            commit_shas=(),
        )

        before = SummaryService.compute_fingerprint([ticket], [monday])
        after = SummaryService.compute_fingerprint([ticket], [friday])

        assert before["commits"] == after["commits"] == []
        assert before["tickets"] == after["tickets"]
        assert before != after, "the PR's updated_at is the only signal there is"

    @pytest.mark.asyncio
    async def test_a_status_change_with_no_new_commits_forces_a_regeneration(
        self, session, org, project, board, user
    ):
        """The second bug review caught: commits alone are not the source."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        ticket = make_ticket(
            session, org, project, assignee="Ada", status=TicketStatus.TODO
        )
        activities = [CodeActivity(repo="innoday", commit_shas=("deadbee",))]
        stale = SummaryService.compute_fingerprint([ticket], activities)

        svc = service(session, activities=activities)
        persist_summary(
            session,
            svc,
            org,
            project,
            body="stale prose",
            fingerprint=stale,
            created_at=NOW - timedelta(hours=2),
        )

        ticket.status = TicketStatus.IN_REVIEW
        session.add(ticket)
        session.commit()

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.outcome is SummaryOutcome.ASSEMBLED
        assert result.source_fingerprint != stale


# ==================================================================== assembly


class TestAssembly:
    @pytest.mark.asyncio
    async def test_fifty_idle_tickets_never_consume_an_active_slot(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        activities = []
        for n in range(8):
            make_ticket(
                session,
                org,
                project,
                summary=f"active {n}",
                assignee="Ada",
                ref=f"PF-{n}",
                updated_at=NOW - timedelta(hours=n + 1),
            )
            activities.append(
                CodeActivity(
                    repo="innoday",
                    ticket_ref=f"PF-{n}",
                    author_handle="ada",
                    occurred_at=NOW - timedelta(hours=n + 1),
                    commit_shas=(f"sha{n}",),
                )
            )
        for n in range(50):
            make_ticket(
                session,
                org,
                project,
                summary=f"idle {n}",
                status=TicketStatus.BACKLOG,
                updated_at=NOW - timedelta(days=90),
            )

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert len(result.active) == ACTIVE_CAP
        assert result.active_total == 8
        assert result.footer == "5 of 8 active shown"
        # Counted, never enumerated -- the backlog would drown the summary.
        assert result.unassigned_idle_count == 50
        # Most recent first.
        stamps = [line.occurred_at for line in result.active]
        assert stamps == sorted(stamps, reverse=True)

    @pytest.mark.asyncio
    async def test_unassigned_work_is_attributed_to_the_code_author(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        session.add(
            UserIdentity(
                user_id=user.id,
                project_id=project.id,
                platform=IdentityPlatform.GITHUB,
                handle="ada",
            )
        )
        from src.domain.organization import OrganizationMembership

        session.add(
            OrganizationMembership(
                organization_id=org.id, user_id=user.id, is_active=True
            )
        )
        session.commit()

        make_ticket(session, org, project, summary="nobody owns it", ref="PF-42")
        activities = [
            CodeActivity(
                repo="innoday",
                ticket_ref="PF-42",
                branch="PF-42-fix",
                pr_url="https://github.com/x/y/pull/1",
                pr_state="open",
                author_handle="ada",
                occurred_at=NOW - timedelta(hours=2),
                commit_shas=("aaa111",),
            )
        ]

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.active == []
        assert len(result.unassigned_active) == 1
        line = result.unassigned_active[0]
        assert line.attribution is Attribution.CODE
        assert line.assignee_user_id == user.id
        assert line.assignee_display == "ada"
        assert line.pr_url == "https://github.com/x/y/pull/1"

    @pytest.mark.asyncio
    async def test_the_id_and_the_display_always_name_the_same_person(
        self, session, org, project, board, user
    ):
        """The board names someone unmappable; the code author resolves.

        This returned the code author's `user_id` beside the *board's* display
        string, so the stored `SummaryItem` asserted user X while rendering
        name Y -- and anything joining on the id (the profile page, most
        obviously) drew the wrong person. The justification given was that the
        board's string had nowhere else to survive; it has, on
        `Ticket.assignee`, which is exactly what `unmapped_assignees()` reads.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        session.add(
            UserIdentity(
                user_id=user.id,
                project_id=project.id,
                platform=IdentityPlatform.GITHUB,
                handle="ada",
            )
        )
        session.add(
            OrganizationMembership(
                organization_id=org.id, user_id=user.id, is_active=True
            )
        )
        session.commit()

        # `assignee` is a board string nothing maps; `assigned_to` stays NULL.
        make_ticket(
            session,
            org,
            project,
            summary="board says Bob",
            ref="PF-77",
            assignee="Bob The Unmappable",
        )
        activities = [
            CodeActivity(
                repo="innoday",
                ticket_ref="PF-77",
                branch="PF-77-fix",
                author_handle="ada",
                occurred_at=NOW - timedelta(hours=2),
                commit_shas=("bbb222",),
            )
        ]

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        line = result.active[0]
        assert line.assignee_user_id == user.id
        assert line.assignee_display == "ada", (
            "the display must name whoever assignee_user_id names, not the "
            "board's string for a different person"
        )
        assert line.assignee_unmapped is False
        # And the board's own claim is not lost -- it never lived here.
        assert SummaryService(session).unmapped_assignees(project.id) == [
            {
                "assignee": "Bob The Unmappable",
                "ticket_count": 1,
                "display": "@Bob The Unmappable (unmapped)",
            }
        ]

    @pytest.mark.asyncio
    async def test_an_unmapped_board_assignee_is_rendered_and_counted(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(
            session,
            org,
            project,
            summary="assigned but unmapped",
            assignee="Bob Stranger",
            ref="PF-7",
        )
        activities = [
            CodeActivity(
                repo="innoday",
                ticket_ref="PF-7",
                occurred_at=NOW - timedelta(hours=1),
                commit_shas=("bbb222",),
            )
        ]

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        line = result.active[0]
        assert line.attribution is Attribution.BOARD
        assert line.assignee_user_id is None
        # The raw string is kept in the model field; the decoration is a view.
        assert line.assignee_display == "Bob Stranger"
        assert line.owner_label == "@Bob Stranger (unmapped)"
        assert result.unmapped_assignee_count == 1

    @pytest.mark.asyncio
    async def test_assigned_but_idle_lands_in_the_no_work_block(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(session, org, project, summary="nothing happened", assignee="Ada")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.active == []
        assert [line.ticket_summary for line in result.no_work_detected] == [
            "nothing happened"
        ]

    @pytest.mark.asyncio
    async def test_a_finished_ticket_is_not_idle_work(
        self, session, org, project, board, user
    ):
        """Otherwise every ticket the project ever closed sits in the block."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(
            session,
            org,
            project,
            summary="shipped ages ago",
            assignee="Ada",
            status=TicketStatus.DONE,
        )
        make_ticket(
            session,
            org,
            project,
            summary="cancelled ages ago",
            status=TicketStatus.CANCELLED,
        )

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )
        assert result.no_work_detected == []
        assert result.unassigned_idle_count == 0

    @pytest.mark.asyncio
    async def test_a_completion_inside_the_window_is_activity(
        self, session, org, project, board, user
    ):
        """`completed_at` is a real transition and the board supplies the date.

        Unlike `updated_at`, nothing writes it as a side effect of a sync
        running, so it survives as a signal even if the restamp regresses.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(
            session,
            org,
            project,
            summary="shipped yesterday",
            assignee="Ada",
            status=TicketStatus.DONE,
            completed_at=NOW - timedelta(days=1),
        )

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )
        assert [line.ticket_summary for line in result.active] == ["shipped yesterday"]

    @pytest.mark.asyncio
    async def test_a_board_move_since_the_last_summary_is_activity(
        self, session, org, project, board, user
    ):
        """The status half of the semantic signal.

        The previous summary's fingerprint is the only record of a ticket's
        prior state anywhere -- there is no status history table -- so it is
        what distinguishes a board move from a timestamp that merely moved.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        ticket = make_ticket(
            session,
            org,
            project,
            summary="moved to review",
            assignee="Ada",
            status=TicketStatus.TODO,
        )
        svc = service(session)
        stale = SummaryService.compute_fingerprint([ticket], [])
        persist_summary(
            session,
            svc,
            org,
            project,
            body="written when it was TODO",
            fingerprint=stale,
            created_at=NOW - timedelta(hours=2),  # too old for gate 2
        )

        ticket.status = TicketStatus.IN_REVIEW
        session.add(ticket)
        session.commit()

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.outcome is SummaryOutcome.ASSEMBLED
        assert [line.ticket_summary for line in result.active] == ["moved to review"]
        assert result.no_work_detected == []


class TestEveryBlockIsBounded:
    """Capping only the active list left the other blocks unbounded.

    A project with 400 open assigned tickets answered "what happened this week?"
    with 400 entries -- while the unassigned backlog next to them was carefully
    counted rather than listed.
    """

    @pytest.mark.asyncio
    async def test_no_work_and_unassigned_active_are_capped_with_totals(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        for n in range(40):
            make_ticket(
                session,
                org,
                project,
                summary=f"assigned and idle {n}",
                assignee="Ada",
                status=TicketStatus.TODO,
            )
        activities = []
        for n in range(30):
            make_ticket(session, org, project, summary=f"nobody's {n}", ref=f"PF-9{n}")
            activities.append(
                CodeActivity(
                    repo="innoday",
                    ticket_ref=f"PF-9{n}",
                    occurred_at=NOW - timedelta(hours=1),
                    commit_shas=(f"c{n}",),
                )
            )

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert len(result.no_work_detected) == BLOCK_CAP
        assert result.no_work_total == 40
        assert len(result.unassigned_active) == BLOCK_CAP
        assert result.unassigned_active_total == 30

    @pytest.mark.asyncio
    async def test_the_unmapped_count_agrees_with_the_unmapped_list(
        self, session, org, project, board, user
    ):
        """It used to be computed over the capped lists only, so the same
        payload carried a count and a list that contradicted each other."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        activities = []
        for n in range(8):
            make_ticket(
                session,
                org,
                project,
                summary=f"active {n}",
                assignee=f"Stranger {n}",  # 8 distinct unmapped handles
                ref=f"PF-{n}",
            )
            activities.append(
                CodeActivity(
                    repo="innoday",
                    ticket_ref=f"PF-{n}",
                    occurred_at=NOW - timedelta(hours=n + 1),
                    commit_shas=(f"s{n}",),
                )
            )

        svc = service(session, activities=activities)
        result = await svc.assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert len(result.active) == ACTIVE_CAP  # only 5 of the 8 are listed
        assert result.unmapped_assignee_count == 8
        assert len(svc.unmapped_assignees(project.id)) == 8


class TestPersonalSummary:
    @pytest.mark.asyncio
    async def test_it_includes_work_they_authored_but_were_not_assigned(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        from src.domain.organization import OrganizationMembership

        session.add(
            OrganizationMembership(
                organization_id=org.id, user_id=user.id, is_active=True
            )
        )
        session.add(
            UserIdentity(
                user_id=user.id,
                project_id=project.id,
                platform=IdentityPlatform.GITHUB,
                handle="ada",
            )
        )
        session.commit()

        make_ticket(session, org, project, summary="theirs by code", ref="PF-9")
        make_ticket(session, org, project, summary="someone else's", ref="PF-10")
        activities = [
            CodeActivity(
                repo="innoday",
                ticket_ref="PF-9",
                author_handle="ada",
                occurred_at=NOW - timedelta(hours=1),
                commit_shas=("ccc333",),
            ),
            CodeActivity(
                repo="innoday",
                ticket_ref="PF-10",
                author_handle="someone-else",
                occurred_at=NOW - timedelta(hours=1),
                commit_shas=("ddd444",),
            ),
        ]

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.PERSONAL,
            window_spec="3d",
            user_id=user.id,
            now=NOW,
        )

        summaries = [line.ticket_summary for line in result.unassigned_active]
        assert summaries == ["theirs by code"]

    @staticmethod
    def _map_identity(session, org, project, user):
        from src.domain.organization import OrganizationMembership

        session.add(
            OrganizationMembership(
                organization_id=org.id, user_id=user.id, is_active=True
            )
        )
        session.add(
            UserIdentity(
                user_id=user.id,
                project_id=project.id,
                platform=IdentityPlatform.GITHUB,
                handle="ada",
            )
        )
        session.commit()

    @pytest.mark.asyncio
    async def test_up_next_holds_board_assigned_work_not_authored_work(
        self, session, org, project, board, user
    ):
        """Authorship records what happened; it cannot predict what is queued.

        The previous version could not tell the two implementations apart: its
        authorship ticket had in-window activity, so it took the `has_activity`
        branch and could never have reached the `up_next` append under *either*
        rule. Both extra tickets below reach a branch that discriminates:

        * "only their commits" -- authored, active. An implementation that
          queued authored work would put it here.
        * "assigned in innoday only" -- assigned to them with no board assignee
          string, so `board_assigned` is false and it is *counted* as idle
          rather than listed. This is what "board assignment only" costs, and it
          is the assertion that fails if the `board_assigned` condition is
          loosened to `assigned_to`.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._map_identity(session, org, project, user)

        make_ticket(
            session,
            org,
            project,
            summary="queued for them",
            assignee="Ada",
            assigned_to=user.id,
            status=TicketStatus.TODO,
        )
        # Authored by them, so a candidate -- but active, not queued.
        make_ticket(session, org, project, summary="only their commits", ref="PF-11")
        # Assigned in InnoDay with nothing on the board. A candidate (the FK
        # matches) that never reaches the no-work branch at all.
        make_ticket(
            session,
            org,
            project,
            summary="assigned in innoday only",
            assignee=None,
            assigned_to=user.id,
            status=TicketStatus.TODO,
        )
        activities = [
            CodeActivity(
                repo="innoday",
                ticket_ref="PF-11",
                author_handle="ada",
                occurred_at=NOW - timedelta(hours=1),
                commit_shas=("eee555",),
            ),
        ]

        result = await service(session, activities=activities).assemble(
            project=project,
            summary_type=SummaryType.PERSONAL,
            window_spec="3d",
            user_id=user.id,
            now=NOW,
        )

        assert [line.ticket_summary for line in result.up_next] == ["queued for them"]
        assert [line.ticket_summary for line in result.unassigned_active] == [
            "only their commits"
        ]
        assert result.unassigned_idle_count == 1

    @pytest.mark.asyncio
    async def test_a_team_summary_never_queues_anything(
        self, session, org, project, board, user
    ):
        """`up_next` is personal by definition -- a roll-up has no "you".

        The other half the old test could not distinguish: drop the
        `user_id is not None` guard and every idle assigned ticket in a team
        summary lands in `up_next` as well as `no_work_detected`.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(
            session,
            org,
            project,
            summary="assigned and idle",
            assignee="Ada",
            assigned_to=user.id,
            status=TicketStatus.TODO,
        )

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert [line.ticket_summary for line in result.no_work_detected] == [
            "assigned and idle"
        ]
        assert result.up_next == []

    @pytest.mark.asyncio
    async def test_an_idle_ticket_of_theirs_is_in_both_blocks_deliberately(
        self, session, org, project, board, user
    ):
        """Documented, not accidental: two questions about the same fact."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._map_identity(session, org, project, user)
        make_ticket(
            session,
            org,
            project,
            summary="nothing yet",
            assignee="Ada",
            assigned_to=user.id,
            status=TicketStatus.TODO,
        )

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.PERSONAL,
            window_spec="3d",
            user_id=user.id,
            now=NOW,
        )

        assert [line.ticket_summary for line in result.no_work_detected] == [
            "nothing yet"
        ]
        assert [line.ticket_summary for line in result.up_next] == ["nothing yet"]


# ================================================================= persistence


class TestPersistence:
    def test_persisting_supersedes_rather_than_overwrites(
        self, session, org, project, user
    ):
        svc = service(session)
        first = persist_summary(session, svc, org, project, body="v1")
        second = persist_summary(session, svc, org, project, body="v2")

        session.refresh(first)
        assert first.superseded_by_id == second.id
        assert first.body_markdown == "v1"  # never overwritten
        assert second.superseded_by_id is None

    def test_it_writes_a_scrum_summary_timeline_entry(
        self, session, org, project, user
    ):
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="prose",
            items=[{"ticket_id": None, "body_markdown": "a line"}],
            created_by=user.id,
        )
        session.commit()

        entries = session.exec(
            select(ProjectTimeline).where(ProjectTimeline.project_id == project.id)
        ).all()
        assert len(entries) == 1
        assert entries[0].event_type is TimelineEventType.SCRUM_SUMMARY

    @pytest.mark.asyncio
    async def test_the_note_travels_on_the_assembled_outcome(
        self, session, org, project, board, user
    ):
        """The outcome that matters most, and the one it was missing from.

        `assembled` fires precisely when something moved -- the common case, and
        the case anyone is actually reading. Carrying the note only on the two
        short-circuit outcomes meant it vanished from the CLI and from the
        narrating agent on every non-quiet day, while the dashboard (which reads
        the row directly) still showed it.
        """
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="yesterday",
            notes_markdown="Ken is out until Thursday.",
            items=[],
            created_by=user.id,
        )
        session.commit()

        # A different fingerprint, so gate 3 cannot short-circuit; and the
        # cached row is older than the TTL, so gate 2 cannot either.
        live = svc.live_summary(
            project_id=project.id,
            user_id=None,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
        )
        live.created_at = NOW - timedelta(hours=5)
        live.source_fingerprint = {"commits": ["stale"], "tickets": [], "prs": []}
        session.add(live)
        session.commit()

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.outcome is SummaryOutcome.ASSEMBLED
        assert result.notes_markdown == "Ken is out until Thursday."
        assert result.to_dict()["notes_markdown"] == "Ken is out until Thursday."

    def test_a_note_survives_the_summary_being_regenerated(
        self, session, org, project, user
    ):
        """The whole point of a separate column.

        `body_markdown` is disposable — rewritten on every run. A note is not:
        somebody typed it, and a 16:00 re-run silently discarding what they
        wrote at 09:00 is a data-loss bug they would have no way to notice.
        Omitting `notes_markdown` therefore *inherits*, it does not clear.
        """
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="morning",
            notes_markdown="Ken is out until Thursday.",
            items=[],
            created_by=user.id,
        )
        regenerated = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="afternoon",
            items=[],
            created_by=user.id,
        )
        session.commit()

        assert regenerated.body_markdown == "afternoon"
        assert regenerated.notes_markdown == "Ken is out until Thursday."

    def test_inheriting_a_note_does_not_restamp_its_date(
        self, session, org, project, user
    ):
        """A date that moves on every regeneration is worse than no date.

        It would read as "written today" about text somebody typed a month ago —
        confirmation rather than information. Only a real change restamps.
        """
        svc = service(session)
        first = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v1",
            notes_markdown="Ken is out until Thursday.",
            items=[],
            created_by=user.id,
        )
        session.commit()
        written_at = first.notes_updated_at
        assert written_at is not None

        inherited = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v2",
            items=[],
            created_by=user.id,
        )
        session.commit()
        assert inherited.notes_markdown == "Ken is out until Thursday."
        assert inherited.notes_updated_at == written_at

        changed = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v3",
            notes_markdown="Ken is back.",
            items=[],
            created_by=user.id,
        )
        session.commit()
        assert changed.notes_updated_at is not None
        assert changed.notes_updated_at >= written_at

    def test_clearing_a_note_clears_its_date_too(self, session, org, project, user):
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v1",
            notes_markdown="gone soon",
            items=[],
            created_by=user.id,
        )
        cleared = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v2",
            notes_markdown="",
            items=[],
            created_by=user.id,
        )
        session.commit()
        assert cleared.notes_markdown == ""
        assert cleared.notes_updated_at is None

    def test_a_note_survives_the_window_spec_drifting(
        self, session, org, project, user
    ):
        """A spec drifts between runs, and notes must survive it.

        The case that exposed this: `--window release` used to return "days since
        the last release" — `5d` on Monday, `6d` on Tuesday. Inheriting only from
        an identical `window_spec` meant a note written on Monday's release run
        was orphaned on Tuesday: left live in a slot nothing would ask for again.
        A release scope is `release:<version>` now and does not drift, but two
        runs at different windows still differ, and a note is a fact about the
        project rather than about a particular lens on it.
        """
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="5d",
            body_markdown="monday",
            notes_markdown="Short week — Thu/Fri are out.",
            items=[],
            created_by=user.id,
        )
        session.commit()

        tuesday = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="6d",
            body_markdown="tuesday",
            items=[],
            created_by=user.id,
        )
        session.commit()

        assert tuesday.notes_markdown == "Short week — Thu/Fri are out."

    def test_a_note_still_does_not_cross_scope(self, session, org, project, user):
        """Widening to any-window must not widen to any-*scope*.

        A team note appearing on someone's personal summary would attribute a
        comment to a summary it was never written about.
        """
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="team",
            notes_markdown="team note",
            items=[],
            created_by=user.id,
        )
        personal = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.PERSONAL,
            window_spec="3d",
            body_markdown="mine",
            items=[],
            user_id=user.id,
            created_by=user.id,
        )
        session.commit()
        assert personal.notes_markdown is None

    def test_reposting_identical_text_refreshes_the_date(
        self, session, org, project, user
    ):
        """Reconfirming a note is an act; inheriting one is not.

        Someone re-sending the same words is saying "still true today", and
        dating that as the original writing makes a current note read as stale.
        Told apart from inheritance by whether the caller supplied anything.
        """
        svc = service(session)
        first = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v1",
            notes_markdown="Still short-staffed.",
            items=[],
            created_by=user.id,
        )
        session.commit()
        original = first.notes_updated_at
        first.notes_updated_at = original - timedelta(days=9)
        session.add(first)
        session.commit()
        stale = first.notes_updated_at

        reconfirmed = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v2",
            notes_markdown="Still short-staffed.",
            items=[],
            created_by=user.id,
        )
        session.commit()
        assert reconfirmed.notes_updated_at > stale

    def test_a_note_can_be_replaced(self, session, org, project, user):
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v1",
            notes_markdown="first",
            items=[],
            created_by=user.id,
        )
        second = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v2",
            notes_markdown="second",
            items=[],
            created_by=user.id,
        )
        session.commit()
        assert second.notes_markdown == "second"

    def test_clearing_a_note_takes_an_empty_string_not_an_omission(
        self, session, org, project, user
    ):
        """`None` and `""` are genuinely different intentions here.

        If omission cleared, there would be no way to regenerate a summary
        *without* destroying the note; if `""` inherited, there would be no way
        to delete one. Both operations are needed, so they get distinct inputs.
        """
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v1",
            notes_markdown="delete me",
            items=[],
            created_by=user.id,
        )
        cleared = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v2",
            notes_markdown="",
            items=[],
            created_by=user.id,
        )
        session.commit()
        assert cleared.notes_markdown == ""

    def test_a_note_does_not_leak_across_scope_or_window(
        self, session, org, project, user
    ):
        """Inheritance follows the **scope**: project + type + team-vs-person.

        The window half of this originally asserted the opposite — that a 3d
        note must not reach the 1w summary — and that was wrong in a way only
        `--window release` made visible: its spec was "days since the last
        release", a different string every day, so keying notes on the window
        orphaned them silently. A note is a fact about the project ("short
        week"), not about a three-day lens on it, so it now follows the scope
        and crosses windows deliberately.

        What must still never happen is crossing *scope*: a team note on
        somebody's personal summary attributes a comment to a summary it was
        never written about. That is what this pins.
        """
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="team",
            notes_markdown="team note",
            items=[],
            created_by=user.id,
        )
        personal = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.PERSONAL,
            window_spec="3d",
            body_markdown="mine",
            items=[],
            user_id=user.id,
            created_by=user.id,
        )
        other_window = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="1w",
            body_markdown="team, week",
            items=[],
            created_by=user.id,
        )
        session.commit()

        assert personal.notes_markdown is None
        # ...and the other window now *does* inherit, on purpose — see above.
        assert other_window.notes_markdown == "team note"

    def test_a_second_scrum_run_the_same_day_reuses_one_timeline_entry(
        self, session, org, project, user
    ):
        """The feed must not read as two stand-ups because someone re-ran it.

        A scrum summary is a snapshot of where the project stands, not an event
        that happened. Persisting appends a `Summary` row (superseded, so the
        history survives) but the timeline gets exactly one entry per day,
        rewritten to the latest snapshot.
        """
        svc = service(session)
        for body, count in (("morning", 1), ("afternoon", 3)):
            svc.persist(
                organization_id=org.id,
                project=project,
                summary_type=SummaryType.SCRUM,
                window_spec="3d",
                body_markdown=body,
                items=[
                    {"ticket_id": None, "body_markdown": f"line {n}"}
                    for n in range(count)
                ],
                created_by=user.id,
            )
        session.commit()

        entries = session.exec(
            select(ProjectTimeline).where(
                ProjectTimeline.project_id == project.id,
                ProjectTimeline.event_type == TimelineEventType.SCRUM_SUMMARY,
            )
        ).all()
        assert len(entries) == 1
        # ...and it carries the *latest* snapshot, not the first one.
        assert (entries[0].metadata_json or {})["item_count"] == 3

    def test_a_personal_summary_does_not_reach_the_project_timeline(
        self, session, org, project, user
    ):
        """One person's own write-up is not a project event.

        It was previously filed on the shared feed *and* labelled
        `SCRUM_SUMMARY`, so the timeline could not tell a team roll-up from any
        individual's morning read of their own work. The `Summary` row is still
        written -- only the timeline entry is withheld.
        """
        svc = service(session)
        summary = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.PERSONAL,
            window_spec="3d",
            body_markdown="just me",
            items=[],
            user_id=user.id,
            created_by=user.id,
        )
        session.commit()

        assert session.get(Summary, summary.id) is not None
        entries = session.exec(
            select(ProjectTimeline).where(ProjectTimeline.project_id == project.id)
        ).all()
        assert entries == []

    def test_items_are_stored_with_their_attribution(self, session, org, project, user):
        svc = service(session)
        summary = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="prose",
            items=[
                {
                    "assignee_display": "ada",
                    "attribution": "code",
                    "repo": "innoday",
                    "no_work_detected": False,
                }
            ],
            created_by=user.id,
        )
        session.commit()

        items = session.exec(
            select(SummaryItem).where(SummaryItem.summary_id == summary.id)
        ).all()
        assert len(items) == 1
        assert items[0].attribution is Attribution.CODE
        assert items[0].rank == 0

    def test_window_spec_is_always_explicit(self, session, org, project, user):
        """`''` exempts a row from both live-uniqueness indexes -- never a default."""
        svc = service(session)
        summary = persist_summary(session, svc, org, project, window_spec="1w")
        assert summary.window_spec == "1w"


# ====================================================================== inputs


class TestWindowSpec:
    @pytest.mark.parametrize(
        "spec,expected",
        [
            ("3d", timedelta(days=3)),
            ("12h", timedelta(hours=12)),
            ("2w", timedelta(weeks=2)),
        ],
    )
    def test_it_parses_the_shapes_the_cli_uses(self, spec, expected):
        assert parse_window_spec(spec) == expected

    @pytest.mark.parametrize("spec", ["", "yesterday", "0d", "3", "3m"])
    def test_it_refuses_anything_else(self, spec):
        with pytest.raises(InvalidWindowSpec):
            parse_window_spec(spec)


class TestTicketRefParsing:
    def test_the_prefix_comes_from_the_project_not_a_literal(self):
        pattern = ticket_ref_pattern("HS")
        assert extract_ticket_ref("HS-412-add-thing", pattern) == "HS-412"
        # A different project's ref is not this project's work.
        assert extract_ticket_ref("PF-398-add-thing", pattern) is None

    def test_it_reads_branches_and_titles_case_insensitively(self):
        pattern = ticket_ref_pattern("PF")
        assert extract_ticket_ref("pf-398-summary-engine", pattern) == "PF-398"
        assert extract_ticket_ref("Fix the gate (PF-398)", pattern) == "PF-398"
        assert extract_ticket_ref("no reference here", pattern) is None


class TestUnmappedAssignees:
    def test_they_are_grouped_by_handle_not_listed_per_ticket(
        self, session, org, project, user
    ):
        make_ticket(session, org, project, assignee="Bob Stranger")
        make_ticket(session, org, project, assignee="Bob Stranger")
        make_ticket(session, org, project, assignee="Ada", assigned_to=user.id)

        rows = service(session).unmapped_assignees(project.id)
        assert rows == [
            {
                "assignee": "Bob Stranger",
                "ticket_count": 2,
                "display": "@Bob Stranger (unmapped)",
            }
        ]


# ============================================================ Postgres-only
#
# Both facts below are Postgres facts that SQLite cannot express, so a green
# SQLite run proves nothing about either:
#
#   * a failed statement aborts the whole transaction and turns the caller's
#     COMMIT into a silent ROLLBACK -- SQLite has no such state;
#   * the live-uniqueness indexes are *partial* and the self-FK is DEFERRABLE,
#     which is what makes update-then-insert the only legal supersede order.


@pytest.fixture
def pg_scope(pg_session):
    tag = uuid4().hex[:10]
    org = Organization(id=f"eng-org-{tag}", name=f"Org {tag}", alias=f"eng-{tag}")
    pg_session.add(org)
    project = Project(
        id=f"eng-proj-{tag}",
        organization_id=org.id,
        alias="PF",
        name=f"Project {tag}",
        description="engine pg fixture",
    )
    pg_session.add(project)
    pg_session.flush()
    return org, project


class TestPostgresGuarantees:
    def test_a_failed_cache_read_leaves_the_transaction_usable(
        self, pg_session, pg_scope
    ):
        """The silent-data-loss trap slice 1 shipped, in the shape gate 2 has.

        Without the SAVEPOINT the failed SELECT would abort the transaction, the
        `except` would swallow it as "cache miss", and the caller's later COMMIT
        would be a ROLLBACK that reports success.
        """
        from sqlalchemy import text

        org, project = pg_scope
        svc = SummaryService(
            pg_session, activity_fetcher=StubFetcher(), sync_runner=SyncSpy()
        )

        real_exec = pg_session.exec
        state = {"first": True}

        def explode(statement, *args, **kwargs):
            if state["first"]:
                state["first"] = False
                return real_exec(text("SELECT * FROM summaries_that_do_not_exist"))
            return real_exec(statement, *args, **kwargs)

        with patch.object(pg_session, "exec", explode):
            assert (
                svc.live_summary(
                    project_id=project.id,
                    user_id=None,
                    summary_type=SummaryType.SCRUM,
                    window_spec="3d",
                )
                is None
            )

        # The transaction survived, so a write after the fault still lands.
        pg_session.add(
            Ticket(
                summary="written after the fault",
                organization_id=org.id,
                project_id=project.id,
            )
        )
        pg_session.flush()

    def test_a_pending_run_does_not_mask_a_fresh_completed_one(
        self, pg_session, pg_scope
    ):
        """The half of the freshness gate SQLite cannot express.

        On Postgres `ORDER BY completed_at DESC` is **NULLS FIRST**, so without
        the `completed_at IS NOT NULL` filter a run that started two minutes ago
        outranks a genuinely fresh completed one -- and every summary read would
        trigger a needless whole-board pull. On SQLite NULLs sort *last* with
        DESC, so the same query looks correct and the filter looks decorative:
        removing it left the entire gate suite green.
        """
        org, project = pg_scope
        now = datetime.now(timezone.utc)
        board = BoardRegistration(
            id=f"b-{uuid4().hex[:10]}",
            organization_id=org.id,
            project_id=project.id,
            board_name="PF board",
            board_url="https://linear.app/pf",
            board_type=BoardType.LINEAR,
            board_external_id="PF",
        )
        pg_session.add(board)
        pg_session.flush()

        pg_session.add(
            BoardSyncHistory(
                board_registration_id=board.id,
                sync_status=SyncStatus.COMPLETED,
                started_at=now - timedelta(minutes=12),
                completed_at=now - timedelta(minutes=10),
            )
        )
        pg_session.add(
            BoardSyncHistory(
                board_registration_id=board.id,
                sync_status=SyncStatus.PENDING,
                started_at=now - timedelta(minutes=2),
                completed_at=None,
            )
        )
        pg_session.flush()

        svc = SummaryService(
            pg_session, activity_fetcher=StubFetcher(), sync_runner=SyncSpy()
        )
        latest = svc.latest_sync(project.id)
        assert latest is not None and latest.completed_at is not None
        assert svc.sync_is_fresh(project.id, now) is True

    def test_supersede_satisfies_the_partial_index_and_deferred_fk(
        self, pg_session, pg_scope
    ):
        org, project = pg_scope
        svc = SummaryService(
            pg_session, activity_fetcher=StubFetcher(), sync_runner=SyncSpy()
        )

        first = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v1",
            items=[],
        )
        second = svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            body_markdown="v2",
            items=[],
        )
        pg_session.flush()

        assert pg_session.get(Summary, first.id).superseded_by_id == second.id
        assert pg_session.get(Summary, second.id).superseded_by_id is None


# =========================================================== cross-org writes
#
# **These must run on Postgres.** Two of the three findings below are invisible
# on SQLite: the test fixtures do not enforce foreign keys, so a `user_id` that
# exists nowhere inserts cleanly instead of reaching COMMIT as the FK violation
# it really is -- which is precisely why a green suite said nothing about any of
# this.


@pytest.fixture
def pg_app_session(pg_engine):
    """A `pg_session` a FastAPI route may `commit()` on without leaking rows.

    `join_transaction_mode="create_savepoint"` turns the route's COMMIT into a
    savepoint release inside the fixture's outer transaction, so the test can
    exercise the real write path and still roll everything back.
    """
    conn = pg_engine.connect()
    trans = conn.begin()
    s = Session(bind=conn, join_transaction_mode="create_savepoint")
    try:
        yield s
    finally:
        s.close()
        if trans.is_active:
            trans.rollback()
        conn.close()


@pytest.fixture
def two_orgs(pg_app_session):
    """Org A (the caller's) and org B (the victim's), each fully populated."""
    from src.domain.organization import OrganizationMembership

    made = {}
    for label in ("a", "b"):
        tag = uuid4().hex[:10]
        org = Organization(id=f"t-org-{tag}", name=f"Org {label}", alias=f"t-{tag}")
        project = Project(
            id=f"t-proj-{tag}",
            organization_id=org.id,
            alias="PF",
            name=f"Project {label}",
            description="tenancy fixture",
        )
        member = User(
            id=str(uuid4()),
            email=f"{tag}@example.com",
            full_name=f"Member {label}",
        )
        pg_app_session.add_all([org, project, member])
        pg_app_session.flush()
        pg_app_session.add(
            OrganizationMembership(
                organization_id=org.id, user_id=member.id, is_active=True
            )
        )
        ticket = Ticket(
            summary=f"{label}'s ticket",
            organization_id=org.id,
            project_id=project.id,
        )
        pg_app_session.add(ticket)
        pg_app_session.flush()
        made[label] = {
            "org": org,
            "project": project,
            "user": member,
            "ticket": ticket,
        }
    return made


@pytest.fixture
def pg_client(pg_app_session):
    def override():
        yield pg_app_session

    app.dependency_overrides[get_session] = override
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


class TestTheWritePathCannotReachAnotherOrg:
    """`POST .../summaries` took every id in the body on trust.

    Verified end-to-end before the fix: a member of org A could post a summary
    naming a user who exists only in org B and an item whose `ticket_id` belongs
    to org B, get a 201, and see the injected markdown read back through
    `GET /organizations/{B}/tickets/{id}/summary-items` -- a route that *does*
    check tenancy, and therefore makes the line look vouched for.
    `SummaryItem.ticket_id` is an FK to an integer PK, so the id space is
    trivially enumerable.
    """

    @staticmethod
    def _post(client, scope, auth, **overrides):
        payload = {
            "summary_type": "scrum",
            "window_spec": "3d",
            "body_markdown": "## injected",
            "items": [],
        }
        payload.update(overrides)
        return client.post(
            f"{BASE}/{scope['org'].id}/projects/{scope['project'].id}/summaries",
            json=payload,
            headers=auth,
        )

    def test_a_user_from_another_org_is_refused(
        self, pg_client, pg_app_session, two_orgs
    ):
        a, b = two_orgs["a"], two_orgs["b"]
        auth = bearer_for(pg_app_session, a["user"].id)

        response = self._post(pg_client, a, auth, user_id=b["user"].id)

        assert response.status_code == 422, response.text
        assert "member" in response.json()["detail"]

    def test_a_nonexistent_user_is_422_not_500(
        self, pg_client, pg_app_session, two_orgs
    ):
        """It used to reach `session.commit()` as a raw FK violation.

        `src/api/app.py` registers no exception handlers, so the violation
        surfaced as a 500 -- a client error reported as a server fault, and only
        on Postgres, since the SQLite fixtures do not enforce FKs at all.
        """
        a = two_orgs["a"]
        auth = bearer_for(pg_app_session, a["user"].id)

        response = self._post(pg_client, a, auth, user_id=str(uuid4()))

        assert response.status_code == 422, response.text

    def test_an_item_cannot_name_another_orgs_ticket(
        self, pg_client, pg_app_session, two_orgs
    ):
        a, b = two_orgs["a"], two_orgs["b"]
        auth = bearer_for(pg_app_session, a["user"].id)

        response = self._post(
            pg_client,
            a,
            auth,
            items=[{"ticket_id": b["ticket"].id, "body_markdown": "not yours"}],
        )
        assert response.status_code == 422, response.text

        # And nothing landed in the victim's per-ticket history.
        victim_auth = bearer_for(pg_app_session, b["user"].id)
        read_back = pg_client.get(
            f"{BASE}/{b['org'].id}/tickets/{b['ticket'].id}/summary-items",
            headers=victim_auth,
        )
        assert read_back.status_code == 200, read_back.text
        assert read_back.json()["count"] == 0

    def test_an_items_assignee_from_another_org_is_refused(
        self, pg_client, pg_app_session, two_orgs
    ):
        a, b = two_orgs["a"], two_orgs["b"]
        auth = bearer_for(pg_app_session, a["user"].id)

        response = self._post(
            pg_client,
            a,
            auth,
            items=[{"assignee_user_id": b["user"].id, "body_markdown": "x"}],
        )
        assert response.status_code == 422, response.text

    def test_the_legitimate_write_still_works(
        self, pg_client, pg_app_session, two_orgs
    ):
        """The guard must refuse the crossing, not the ordinary case."""
        a = two_orgs["a"]
        auth = bearer_for(pg_app_session, a["user"].id)

        response = self._post(
            pg_client,
            a,
            auth,
            user_id=a["user"].id,
            items=[
                {
                    "ticket_id": a["ticket"].id,
                    "assignee_user_id": a["user"].id,
                    "body_markdown": "mine",
                }
            ],
        )
        assert response.status_code == 201, response.text

    def test_user_id_is_not_a_platform_wide_existence_oracle(
        self, pg_client, pg_app_session, two_orgs
    ):
        """`?user_id=<email>` answered 200/404 for *any* account, in any org.

        Any authenticated member of any org could therefore test whether an
        arbitrary email has a platform account. `resolve_user` took an
        `organization_id` and never used it; scoped, a user outside the org is
        indistinguishable from one who does not exist.
        """
        a, b = two_orgs["a"], two_orgs["b"]
        auth = bearer_for(pg_app_session, a["user"].id)
        url = f"{BASE}/{a['org'].id}/projects/{a['project'].id}/summary-data"

        with patch(
            "src.services.summary_service.CodeActivityFetcher.fetch", return_value=[]
        ):
            foreign = pg_client.get(
                url, params={"user_id": b["user"].email}, headers=auth
            )
            unknown = pg_client.get(
                url,
                params={"user_id": f"{uuid4().hex}@nowhere.example"},
                headers=auth,
            )
            own = pg_client.get(url, params={"user_id": a["user"].email}, headers=auth)

        assert foreign.status_code == 404, foreign.text
        assert unknown.status_code == 404
        # Indistinguishable: the only thing that varies between the two bodies
        # is the ref the caller itself supplied.
        assert foreign.json()["detail"].replace(b["user"].email, "@") == unknown.json()[
            "detail"
        ].replace(unknown.request.url.params["user_id"], "@")
        assert own.status_code == 200, own.text


# ====================================================================== routes


@pytest.fixture
def client(db_engine):
    def override_get_session():
        with Session(db_engine) as s:
            yield s

    app.dependency_overrides[get_session] = override_get_session
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth(session, user):
    return bearer_for(session, user.id)


BASE = "/api/v1/organizations"


class TestRoutes:
    def test_summary_data_assembles_without_calling_an_llm(
        self, client, auth, session, org, project, board, user
    ):
        record_sync(
            session,
            board,
            completed_at=datetime.now(timezone.utc) - timedelta(minutes=5),
            synced_by=user.id,
        )
        make_ticket(session, org, project, summary="a thing", assignee="Ada")

        with patch(
            "src.services.summary_service.CodeActivityFetcher.fetch",
            return_value=[],
        ) as fetch:
            fetch.return_value = []
            response = client.get(
                f"{BASE}/{org.id}/projects/{project.id}/summary-data",
                params={"window_spec": "3d"},
                headers=auth,
            )

        assert response.status_code == 200, response.text
        body = response.json()
        assert body["outcome"] == "assembled"
        assert body["footer"] == "0 of 0 active shown"
        assert body["no_work_detected"][0]["summary"] == "a thing"
        # The engine returns data, never prose.
        assert body["body_markdown"] is None

    def test_summary_data_rejects_an_unparseable_window(
        self, client, auth, org, project
    ):
        response = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summary-data",
            params={"window_spec": "yesterday"},
            headers=auth,
        )
        assert response.status_code == 422

    def test_a_personal_summary_must_say_whose_it_is(self, client, auth, org, project):
        """``summary_type=personal`` with no `user_id` is the team roll-up.

        `user_id IS NULL` is what the team slot *means* (`src/domain/summary.py`),
        so the row this used to write went into it: `uq_summaries_live_team` was
        the index that applied, `live_summary` looked it up with `user_id IS
        NULL`, gates 2 and 3 never matched the personal read that wrote it, and
        ``summaries/latest?user_id=me`` could not find it. Verified end to end
        before the fix: the second identical personal call answered `assembled`
        where the scrum control answered `cached`.
        """
        refused = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "personal",
                "window_spec": "3d",
                "body_markdown": "mine",
            },
            headers=auth,
        )
        assert refused.status_code == 422, refused.text
        assert "user_id" in refused.json()["detail"]

        # The read half of the same incoherence.
        read = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summary-data",
            params={"summary_type": "personal", "window_spec": "3d"},
            headers=auth,
        )
        assert read.status_code == 422, read.text

    def test_a_personal_summary_is_readable_back_as_that_users(
        self, client, auth, session, org, project, user
    ):
        """The round trip `scope='me'` never had a test at any layer.

        `tests/test_mcp_tools.py` hardcoded ``scope='scrum'``, and no route test
        posted a personal summary at all -- so nothing noticed that what came
        back out was the team's.
        """
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=user.id,
                organization_id=org.id,
                is_active=True,
            )
        )
        session.commit()

        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "personal",
                "window_spec": "3d",
                "body_markdown": "what I did",
                # 'me' is resolved against the token, exactly as the read path
                # resolves it -- the caller knows its scope, not its user id.
                "user_id": "me",
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        assert created.json()["user_id"] == user.id

        mine = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summaries/latest",
            params={"summary_type": "personal", "user_id": "me"},
            headers=auth,
        )
        assert mine.status_code == 200, mine.text
        assert mine.json()["id"] == created.json()["id"]

        # And it is emphatically *not* the team summary -- the whole defect was
        # that these two were the same row.
        team = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summaries/latest",
            params={"summary_type": "personal"},
            headers=auth,
        )
        assert team.status_code == 404, team.text

    def test_an_omitted_fingerprint_is_computed_server_side(
        self, client, auth, session, org, project, user
    ):
        """The caller must not have to carry ~28 KB of shas back to the server.

        The fingerprint is every ticket id + status and every commit sha in the
        window. Requiring it echoed meant an LLM narrator reproducing all of it
        verbatim purely to hand the server a value it had just computed. Omitted
        now means *recomputed*, not empty — an empty one silently costs a
        redundant re-narration on every subsequent run.
        """
        make_ticket(session, org, project, assignee="Ada")

        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "no fingerprint supplied",
                "items": [],
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text

        stored = session.exec(
            select(Summary).where(Summary.id == created.json()["id"])
        ).one()
        assert stored.source_fingerprint, "fingerprint was left empty"
        assert "tickets" in stored.source_fingerprint

    def test_an_explicitly_passed_fingerprint_still_wins_verbatim(
        self, client, auth, session, org, project, user
    ):
        """The echo path has to keep working for anything that already does it."""
        make_ticket(session, org, project, assignee="Ada")
        mine = {"commits": ["deadbeef"], "tickets": [], "prs": []}

        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "mine",
                "items": [],
                "source_fingerprint": mine,
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text

        stored = session.exec(
            select(Summary).where(Summary.id == created.json()["id"])
        ).one()
        assert stored.source_fingerprint == mine

    def test_a_note_round_trips_through_the_write_path(
        self, client, auth, session, org, project, user
    ):
        """Posted as `notes_markdown`, read back as `notes`, kept out of `summary`."""
        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "generated prose",
                "notes_markdown": "Ken is out until Thursday.",
                "items": [],
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        payload = created.json()
        assert payload["notes"] == "Ken is out until Thursday."
        # Never folded into the generated half.
        assert payload["summary"] == "generated prose"

        latest = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summaries/latest",
            headers=auth,
        )
        assert latest.status_code == 200
        assert latest.json()["notes"] == "Ken is out until Thursday."

    def test_a_regenerating_post_that_omits_notes_keeps_them(
        self, client, auth, session, org, project, user
    ):
        """The API-level guarantee behind the service-level carry-forward.

        This is the shape a real second run takes: same window, new prose, no
        mention of notes. Losing the note here would be silent.
        """
        for body, note in (("v1", "keep me"), ("v2", None)):
            request = {
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": body,
                "items": [],
            }
            if note is not None:
                request["notes_markdown"] = note
            response = client.post(
                f"{BASE}/{org.id}/projects/{project.id}/summaries",
                json=request,
                headers=auth,
            )
            assert response.status_code == 201, response.text

        latest = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summaries/latest",
            headers=auth,
        )
        assert latest.json()["summary"] == "v2"
        assert latest.json()["notes"] == "keep me"

    def test_the_narrated_write_path_round_trips(
        self, client, auth, session, org, project, user
    ):
        ticket = make_ticket(session, org, project, assignee="Ada")
        payload = {
            "summary_type": "scrum",
            "window_spec": "3d",
            "body_markdown": "## What happened\nA lot.",
            "source_fingerprint": {"commits": ["abc"], "tickets": []},
            "items": [
                {
                    "ticket_id": ticket.id,
                    "assignee_display": "Ada",
                    "attribution": "board",
                    "body_markdown": "moved to review",
                }
            ],
        }
        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json=payload,
            headers=auth,
        )
        assert created.status_code == 201, created.text
        assert created.json()["summary"] == "## What happened\nA lot."

        latest = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summaries/latest",
            headers=auth,
        )
        assert latest.status_code == 200
        assert latest.json()["id"] == created.json()["id"]

        listed = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            params={"type": "scrum", "window_spec": "3d"},
            headers=auth,
        )
        assert listed.status_code == 200
        assert listed.json()["count"] == 1

        items = client.get(
            f"{BASE}/{org.id}/tickets/{ticket.id}/summary-items", headers=auth
        )
        assert items.status_code == 200
        assert items.json()["items"][0]["body_markdown"] == "moved to review"

    def test_sync_status_reports_what_the_freshness_gate_reads(
        self, client, auth, session, org, project, board, user
    ):
        record_sync(
            session,
            board,
            completed_at=datetime.now(timezone.utc) - timedelta(minutes=5),
            synced_by=user.id,
        )
        response = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/sync/status", headers=auth
        )
        assert response.status_code == 200
        assert response.json()["is_fresh"] is True

    def test_unmapped_assignees_powers_the_footer_count(
        self, client, auth, session, org, project
    ):
        make_ticket(session, org, project, assignee="Bob Stranger")
        response = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/unmapped-assignees", headers=auth
        )
        assert response.status_code == 200
        assert response.json()["count"] == 1
        assert response.json()["assignees"][0]["assignee"] == "Bob Stranger"

    def test_an_assembler_line_posted_verbatim_keeps_its_block(
        self, client, auth, session, org, project, user
    ):
        """The one field the round trip used to lose.

        `SummaryLine.to_dict()` says `"block": "no_work_detected"`;
        `SummaryItem` records a boolean and no block. `SummaryItemPayload` had
        neither a `block` field nor a mapping, so pydantic dropped the key and
        the line stored `no_work_detected=False` -- 201, no error, wrong row.
        Every other test in this file sets the boolean by hand, which is exactly
        why nothing caught it, so this one posts what the assembler emits.
        """
        from src.services.summary_service import Block, SummaryLine

        ticket = make_ticket(session, org, project, summary="stalled", assignee="Ada")
        line = SummaryLine(
            block=Block.NO_WORK,
            ticket_id=ticket.id,
            ticket_ref="PF-1",
            ticket_summary="stalled",
            assignee_display="Ada",
        ).to_dict()
        assert line["block"] == "no_work_detected"
        assert "no_work_detected" not in line, "the boolean is not what is emitted"

        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "quiet",
                "items": [line],
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text

        stored = session.exec(
            select(SummaryItem).where(SummaryItem.summary_id == created.json()["id"])
        ).all()
        assert len(stored) == 1
        assert stored[0].no_work_detected is True

    def test_an_active_line_posted_verbatim_is_not_marked_no_work(
        self, client, auth, session, org, project, user
    ):
        """The mapping must read the block, not merely assume the common case."""
        from src.services.summary_service import Block, SummaryLine

        ticket = make_ticket(session, org, project, summary="moving", assignee="Ada")
        line = SummaryLine(
            block=Block.ACTIVE,
            ticket_id=ticket.id,
            ticket_summary="moving",
            assignee_display="Ada",
        ).to_dict()

        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "busy",
                "items": [line],
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        stored = session.exec(
            select(SummaryItem).where(SummaryItem.summary_id == created.json()["id"])
        ).all()
        assert stored[0].no_work_detected is False

    def test_an_explicit_boolean_still_wins_without_a_block(
        self, client, auth, session, org, project, user
    ):
        """The older shape -- callers that send the boolean -- is unaffected."""
        ticket = make_ticket(session, org, project, assignee="Ada")
        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "quiet",
                "items": [{"ticket_id": ticket.id, "no_work_detected": True}],
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        stored = session.exec(
            select(SummaryItem).where(SummaryItem.summary_id == created.json()["id"])
        ).all()
        assert stored[0].no_work_detected is True


class TestTheAssembledLineSurvivesTheWritePath:
    """The assembler's output and the write path's input are one shape.

    Posting an assembled line back unchanged is the *documented* use of
    `POST .../summaries`, so any key `SummaryLine.to_dict()` emits that
    `SummaryItemPayload` does not declare is data thrown away in silence.
    `block` was lost that way; six more keys were going the same way behind it.
    """

    def test_every_assembled_key_is_declared_by_the_request_model(self):
        """A set comparison, not a hand-kept list -- the point is that adding a
        field to `SummaryLine` cannot quietly outrun the payload model."""
        emitted = set(SummaryLine(block=Block.ACTIVE, ticket_id=1).to_dict().keys())
        declared = set(SummaryItemPayload.model_fields)
        assert emitted - declared == set(), (
            "SummaryLine emits keys the write path would drop: "
            f"{sorted(emitted - declared)}"
        )

    def test_an_unknown_key_is_a_422_rather_than_a_silent_drop(
        self, client, auth, session, org, project, user
    ):
        ticket = make_ticket(session, org, project, assignee="Ada")
        response = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "x",
                "items": [{"ticket_id": ticket.id, "totally_new_field": "boom"}],
            },
            headers=auth,
        )
        assert response.status_code == 422, response.text
        assert "totally_new_field" in response.text

    def test_a_verbatim_assembled_line_is_accepted_whole(
        self, client, auth, session, org, project, user
    ):
        """`extra="forbid"` must not break the very round trip it protects."""
        ticket = make_ticket(session, org, project, assignee="Ada")
        line = SummaryLine(
            block=Block.NO_WORK,
            ticket_id=ticket.id,
            ticket_ref="PF-1",
            ticket_summary="a thing",
            status="todo",
            assignee_display="Ada",
            assignee_unmapped=True,
            attribution=Attribution.BOARD,
            commit_count=3,
        ).to_dict()
        line["body_markdown"] = "nothing yet"

        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "x",
                "items": [line],
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        stored = session.exec(
            select(SummaryItem).where(SummaryItem.summary_id == created.json()["id"])
        ).all()
        # The columns that exist are populated; the six re-derivable ones are
        # accepted and deliberately not stored.
        assert stored[0].assignee_display == "Ada"
        assert stored[0].no_work_detected is True
        assert stored[0].body_markdown == "nothing yet"


class TestEchoingEveryBlockDoesNotDuplicateItems:
    """`_assemble` files one ticket under both `no_work_detected` and `up_next`.

    That is deliberate and documented (summary_service.py) -- the two blocks
    answer different questions of the same fact. Nothing on the write path knew
    it, so echoing all blocks back, which is exactly what the skill instructs,
    wrote the same `(summary_id, ticket_id)` twice and made
    `tickets show --with-summaries` print the ticket's history twice.
    """

    def test_one_ticket_echoed_under_two_blocks_stores_one_row(
        self, client, auth, session, org, project, user
    ):
        ticket = make_ticket(session, org, project, assignee="Ada")
        both_blocks = [
            SummaryLine(block=Block.NO_WORK, ticket_id=ticket.id).to_dict(),
            SummaryLine(block=Block.UP_NEXT, ticket_id=ticket.id).to_dict(),
        ]
        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "x",
                "items": both_blocks,
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        stored = session.exec(
            select(SummaryItem).where(SummaryItem.summary_id == created.json()["id"])
        ).all()
        assert len(stored) == 1
        # `no_work_detected` is the fact with no other home; `up_next` is
        # re-derivable from the ticket, so it is the one that yields.
        assert stored[0].no_work_detected is True

    def test_an_active_line_outranks_the_idle_spellings_of_itself(self):
        ordered = SummaryService._dedupe_items(
            [
                {"ticket_id": 1, "block": Block.UP_NEXT.value},
                {"ticket_id": 1, "block": Block.ACTIVE.value},
                {"ticket_id": 1, "block": Block.NO_WORK.value},
            ]
        )
        assert [i["block"] for i in ordered] == [Block.ACTIVE.value]

    def test_lines_with_no_ticket_are_never_merged(self):
        """Code on a branch nobody opened a ticket for is still distinct work."""
        loose = [
            {"ticket_id": None, "repo": "a", "branch": "x"},
            {"ticket_id": None, "repo": "a", "branch": "y"},
        ]
        assert SummaryService._dedupe_items(loose) == loose


class TestTheUnmappedCountAndListAnswerOneQuestion:
    """They are shipped side by side in one payload and used to disagree.

    The count was derived from the assembled lines -- assembly-scoped (a
    personal summary counted only that user's candidates; a terminal-status
    ticket never became a line) while `unmapped_assignees()` is project-wide
    and unfiltered. And when a gate short-circuited, no lines were built at
    all, so the count was 0 beside a non-empty list: the CLI footer dropped
    the "N assignees unmapped" hint on exactly the cached reads that are the
    common case.
    """

    @pytest.mark.asyncio
    async def test_a_cached_read_still_reports_the_unmapped_hint(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(session, org, project, summary="a thing", assignee="Bob Stranger")
        session.add(
            Summary(
                organization_id=org.id,
                project_id=project.id,
                window_spec="3d",
                summary_type=SummaryType.SCRUM,
                body_markdown="written moments ago",
                motivational_quote="",
                created_at=NOW - timedelta(minutes=1),
            )
        )
        session.commit()

        svc = service(session)
        result = await svc.assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.outcome is SummaryOutcome.CACHED
        assert (
            result.unmapped_assignee_count
            == len(svc.unmapped_assignees(project.id))
            == 1
        )

    @pytest.mark.asyncio
    async def test_a_personal_scope_does_not_shrink_the_project_wide_count(
        self, session, org, project, board, user
    ):
        """The count is about the *project*, like the list beside it.

        Scoping it to the requester's own candidates made two numbers with one
        name: the footer said 1 while `unmapped_assignees` listed 3.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        session.add(
            OrganizationMembership(
                organization_id=org.id, user_id=user.id, is_active=True
            )
        )
        for n, who in enumerate(("Stranger A", "Stranger B", "Stranger C")):
            make_ticket(session, org, project, summary=f"t{n}", assignee=who)
        session.commit()

        svc = service(session)
        result = await svc.assemble(
            project=project,
            summary_type=SummaryType.PERSONAL,
            window_spec="3d",
            user_id=user.id,
            now=NOW,
        )

        assert result.active == [] and result.no_work_detected == []
        assert (
            result.unmapped_assignee_count
            == len(svc.unmapped_assignees(project.id))
            == 3
        )


class TestWritePathContract:
    """Two things the write path claimed or implied but did not do."""

    def test_generated_by_is_accepted_rather_than_always_agent(
        self, client, auth, session, org, project, user
    ):
        """`SKILL.md` told the caller to record `hybrid` vs `agent`.

        `CreateSummaryRequest` had no such field, `persist()` never set one, so
        every row was AGENT and `HUMAN`/`HYBRID` had no writer at all -- the
        human-amended distinction is a design goal with nothing behind it.
        """
        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "agent drafted, human edited",
                "generated_by": "hybrid",
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        stored = session.get(Summary, created.json()["id"])
        assert stored.generated_by is GeneratedBy.HYBRID

    def test_generated_by_still_defaults_to_agent(
        self, client, auth, session, org, project, user
    ):
        created = client.post(
            f"{BASE}/{org.id}/projects/{project.id}/summaries",
            json={
                "summary_type": "scrum",
                "window_spec": "3d",
                "body_markdown": "unattended",
            },
            headers=auth,
        )
        assert created.status_code == 201, created.text
        assert session.get(Summary, created.json()["id"]).generated_by is (
            GeneratedBy.AGENT
        )

    def test_a_concurrent_second_save_is_a_409_not_a_500(
        self, client, auth, session, org, project, user
    ):
        """Two agents narrating the same (project, type, window) race the
        partial unique indexes. `src/api/app.py` registers no exception
        handlers at all, so the loser got a raw `IntegrityError` -> 500.

        The race is reproduced by making `live_summary` answer None while a
        live row exists -- which is exactly what the loser sees when it reads
        before the winner commits.
        """
        session.add(
            Summary(
                organization_id=org.id,
                project_id=project.id,
                window_spec="3d",
                summary_type=SummaryType.SCRUM,
                body_markdown="the winner",
                motivational_quote="",
            )
        )
        session.commit()

        with patch.object(SummaryService, "live_summary", return_value=None):
            response = client.post(
                f"{BASE}/{org.id}/projects/{project.id}/summaries",
                json={
                    "summary_type": "scrum",
                    "window_spec": "3d",
                    "body_markdown": "the loser",
                },
                headers=auth,
            )

        assert response.status_code == 409, response.text
        assert "concurrently" in response.json()["detail"]
        # The winner is untouched and still the only live row.
        live = session.exec(
            select(Summary).where(
                Summary.project_id == project.id,
                Summary.superseded_by_id.is_(None),
            )
        ).all()
        assert [s.body_markdown for s in live] == ["the winner"]


# ============================================================== release scope


class TestReleaseScope:
    """A release scope narrows the ticket universe (#563, defect 3).

    Out of release means **not assembled**, not "assembled and then filtered by
    whoever narrates it": handing a narrator tickets it must be instructed to
    ignore is the same failure as leaking another project's work, one size up.
    """

    def _release(self, session, org, project, version, *, created_at=None):
        from src.domain.release import Release, ReleaseStatus

        row = Release(
            organization_id=org.id,
            project_id=project.id,
            version=version,
            name=version,
            status=ReleaseStatus.IN_PROGRESS,
        )
        session.add(row)
        session.commit()
        if created_at is not None:
            # `created_at` has a default_factory, so it is set after the insert
            # rather than passed in -- the column is naive UTC.
            row.created_at = created_at
            session.add(row)
            session.commit()
        session.refresh(row)
        return row

    @pytest.mark.asyncio
    async def test_tickets_on_another_release_are_not_assembled(
        self, session, org, project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        make_ticket(
            session, org, project, summary="in scope", assignee="Ada", release="v1.9.0"
        )
        make_ticket(
            session,
            org,
            project,
            summary="last release",
            assignee="Ada",
            release="v1.8.0",
        )
        make_ticket(session, org, project, summary="no release", assignee="Ada")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            release="v1.9.0",
            now=NOW,
        )

        summaries = [
            line.ticket_summary
            for line in (
                list(result.active)
                + list(result.no_work_detected)
                + list(result.unassigned_active)
                + list(result.up_next)
            )
        ]
        assert summaries == ["in scope"]

    @pytest.mark.asyncio
    async def test_the_release_is_the_cache_key_not_the_day_window(
        self, session, org, project, board, user
    ):
        """A `3d` summary written minutes ago must not answer a release read.

        `window_spec` is the cache key, so a release-scoped run that reused the
        day-window spec would be served the day-window's prose -- a summary of a
        different question, with no sign that it was.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        make_ticket(
            session, org, project, summary="in scope", assignee="Ada", release="v1.9.0"
        )
        session.add(
            Summary(
                organization_id=org.id,
                project_id=project.id,
                window_spec="3d",
                summary_type=SummaryType.SCRUM,
                body_markdown="the last three days",
                motivational_quote="",
                created_at=NOW - timedelta(minutes=1),
            )
        )
        session.commit()

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            release="v1.9.0",
            now=NOW,
        )

        assert result.outcome is SummaryOutcome.ASSEMBLED
        assert result.body_markdown is None
        assert result.window_spec == "release:v1.9.0"

    @pytest.mark.asyncio
    async def test_the_release_spec_is_stable_from_one_day_to_the_next(
        self, session, org, project, board, user
    ):
        """The old `--window release` minted `5d`, then `6d`, then `7d`.

        A key that changes daily is a cache that never hits and a note that is
        orphaned every morning. The release names itself, so the spec can stand
        still while the calendar moves.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")

        today = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            release="v1.9.0",
            now=NOW,
        )
        tomorrow = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            release="v1.9.0",
            now=NOW + timedelta(days=1),
        )

        assert today.window_spec == tomorrow.window_spec == "release:v1.9.0"

    @pytest.mark.asyncio
    async def test_absence_is_measured_inside_the_release(
        self, session, org, project, board, user
    ):
        """`no_work_detected` and `unassigned_idle_count` are defined by absence.

        Left project-wide under a release scope, a quiet release reports the
        whole project's silence -- or a busy project's backlog as the release's
        own.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        make_ticket(session, org, project, summary="idle elsewhere", assignee="Ada")
        make_ticket(session, org, project, summary="nobody, elsewhere")
        make_ticket(
            session,
            org,
            project,
            summary="idle in scope",
            assignee="Ada",
            release="v1.9.0",
        )
        make_ticket(session, org, project, summary="nobody, in scope", release="v1.9.0")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            release="v1.9.0",
            now=NOW,
        )

        assert [line.ticket_summary for line in result.no_work_detected] == [
            "idle in scope"
        ]
        assert result.unassigned_idle_count == 1

    @pytest.mark.asyncio
    async def test_the_payload_states_its_own_boundary(
        self, session, org, project, board, user
    ):
        """A slice must say it is one, with the size of what it left out.

        Most tickets carry no release at all, so a release summary that does not
        state its boundary is a subset reported as the whole.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        make_ticket(session, org, project, summary="a", release="v1.9.0")
        make_ticket(session, org, project, summary="b", release="v1.9.0")
        make_ticket(session, org, project, summary="c", release="v1.8.0")
        make_ticket(session, org, project, summary="d")
        make_ticket(session, org, project, summary="e", release="")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            release="v1.9.0",
            now=NOW,
        )

        assert result.release == "v1.9.0"
        assert result.release_ticket_count == 2
        # `d` and `e`: a NULL and an emptied-out release are the same fact.
        assert result.tickets_without_release_count == 2
        payload = result.to_dict()
        assert payload["release"] == "v1.9.0"
        assert payload["release_ticket_count"] == 2
        assert payload["tickets_without_release_count"] == 2

    @pytest.mark.asyncio
    async def test_an_unscoped_run_says_it_is_not_a_release_slice(
        self, session, org, project, board, user
    ):
        """None, not 0: "no release scope" is a different fact from "nothing
        on this release", and a caller must not have to guess which it got."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(session, org, project, summary="a", release="v1.9.0")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="day",
            now=NOW,
        )

        assert result.window_spec == "1d"
        assert result.release is None
        assert result.release_ticket_count is None
        assert result.tickets_without_release_count is None

    @pytest.mark.asyncio
    async def test_the_fingerprint_covers_every_ticket_in_scope(
        self, session, org, project, board, user
    ):
        """Trap: a ticket missing from the fingerprint reads as "unchanged".

        The scope narrows what the fingerprint covers; it must not narrow it to
        less than the scope.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        wanted = {
            str(
                make_ticket(session, org, project, summary=f"t{n}", release="v1.9.0").id
            )
            for n in range(3)
        }
        make_ticket(session, org, project, summary="elsewhere", release="v1.8.0")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            release="v1.9.0",
            now=NOW,
        )

        assert {row[0] for row in result.source_fingerprint["tickets"]} == wanted

    @pytest.mark.asyncio
    async def test_the_fingerprint_moves_when_the_excluded_count_does(
        self, session, org, project, board, user
    ):
        """A ticket on **no** release changes what the boundary line must say.

        Everything else in the fingerprint is built from the release-filtered
        rows, so an out-of-scope ticket is invisible to it: gate 3 answered
        "unchanged" and re-served prose stating yesterday's
        `tickets_without_release_count`, while the CLI recomputed the boundary
        line fresh and printed a different number underneath it. A summary
        disagreeing with itself in one output.

        The `UNCHANGED` assertion in the middle is the control -- without it this
        test would also pass if the fingerprint simply never matched.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        make_ticket(session, org, project, summary="in scope", release="v1.9.0")

        first = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="release:v1.9.0",
            now=NOW,
        )
        assert first.outcome is SummaryOutcome.ASSEMBLED
        assert first.source_fingerprint["tickets_without_release_count"] == 0
        persist_summary(
            session,
            service(session),
            org,
            project,
            window_spec="release:v1.9.0",
            body="nothing else is on this release",
            fingerprint=first.source_fingerprint,
            created_at=NOW - timedelta(hours=2),  # too old for gate 2
        )

        unchanged = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="release:v1.9.0",
            now=NOW,
        )
        assert unchanged.outcome is SummaryOutcome.UNCHANGED

        make_ticket(session, org, project, summary="on no release at all")

        after = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="release:v1.9.0",
            now=NOW,
        )

        assert after.outcome is SummaryOutcome.ASSEMBLED
        assert after.source_fingerprint["tickets_without_release_count"] == 1
        assert after.source_fingerprint != first.source_fingerprint
        # The scoped rows did not move -- the excluded count is the whole signal.
        assert (
            after.source_fingerprint["tickets"] == first.source_fingerprint["tickets"]
        )

    def test_an_unscoped_fingerprint_carries_no_boundary_keys(self):
        """Adding `null`s to the unscoped shape would re-narrate every project once.

        Gate 3 compares the stored dict with `==`, so a new key on the
        no-release path makes every fingerprint written before this change
        unequal to the one computed next to it.
        """
        assert set(SummaryService.compute_fingerprint([], [])) == {
            "commits",
            "tickets",
            "prs",
        }

    @pytest.mark.asyncio
    async def test_the_save_path_and_assemble_gather_the_same_fingerprint(
        self, client, auth, session, org, project, board, user
    ):
        """One gather, or gate 3 can never answer UNCHANGED at all.

        The read path and the save path used to run the five gather steps
        separately, and had to hand `compute_fingerprint` an identical kwarg set.
        Twice they did not: the save path parsed `release:v1.9.0` as a *duration*
        (which raises, and its broad `except` turned that into `{}`), and later it
        lacked the two boundary counts `assemble` had gained. Neither surfaced as a
        failure -- a fingerprint that never matches looks exactly like a cache
        working correctly, and the only symptom is a summary re-narrated every
        morning.

        A release scope is the shape both bugs lived in, so it is the one pinned
        here. `SummaryService.fingerprint_for` is now the single gather, which is
        what makes this agreement structural rather than a coincidence to re-check.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        make_ticket(session, org, project, summary="in scope", release="v1.9.0")
        make_ticket(session, org, project, summary="on no release")

        assembled = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="release:v1.9.0",
            now=NOW,
        )
        assert assembled.outcome is SummaryOutcome.ASSEMBLED

        # No `source_fingerprint` in the body: the save path recomputes it, which
        # is the code under test here.
        with patch(
            "src.services.summary_service.CodeActivityFetcher.fetch", return_value=[]
        ):
            created = client.post(
                f"{BASE}/{org.id}/projects/{project.id}/summaries",
                json={
                    "summary_type": "scrum",
                    "window_spec": "release:v1.9.0",
                    "body_markdown": "narrated",
                    "items": [],
                },
                headers=auth,
            )
        assert created.status_code == 201, created.text

        stored = session.exec(
            select(Summary).where(Summary.id == created.json()["id"])
        ).one()
        assert stored.source_fingerprint == assembled.source_fingerprint
        # Not vacuously equal: both carry the boundary pair that had to be
        # back-filled into the save path once already, and it is not zero.
        assert stored.source_fingerprint["tickets_without_release_count"] == 1
        assert stored.source_fingerprint["release_ticket_count"] == 1

    # ------------------------------------------------- the release's period
    #
    # #563 fixed *which tickets* a release scope covers and said nothing about
    # the period. "Since the release was opened" is this change's own decision,
    # and the reason it needs pinning is the failure mode it sits next to: a
    # window shorter than the work it asks about **manufactures absence** --
    # `_activity_at` measures against `period_start`, so tickets land in
    # `no_work_detected` because of where the window starts rather than because
    # nothing happened. See `_release_period_start` for the whole rule.

    def test_the_period_starts_when_the_release_was_opened(self, session, org, project):
        opened = NOW - timedelta(days=17)
        self._release(session, org, project, "v1.9.0", created_at=opened)

        _, version, period_start = service(session).resolve_scope(
            project=project, window_spec="release:v1.9.0", now=NOW
        )

        assert version == "v1.9.0"
        assert as_utc(period_start) == opened

    def test_a_stale_release_row_is_capped_rather_than_obeyed(
        self, session, org, project
    ):
        """`period_start` bounds the board sync and the per-repo GitHub fetches
        inside a synchronous GET, and BPAI carries ~40 rows board sync invented
        from years-old version labels. Unbounded, that is a timed-out request
        rather than a longer summary."""
        self._release(
            session, org, project, "v1.9.0", created_at=NOW - timedelta(days=400)
        )

        _, _, period_start = service(session).resolve_scope(
            project=project, window_spec="release:v1.9.0", now=NOW
        )

        assert as_utc(period_start) == NOW - RELEASE_SPAN_CAP
        assert RELEASE_SPAN_CAP == timedelta(days=90)

    def test_a_version_with_no_release_row_gets_the_fallback_span(
        self, session, org, project
    ):
        """`Ticket.release` is free text a board wrote, so a scope InnoDay has no
        row for is a legitimate question. 28 days rather than the 3-day default:
        a window narrower than a release reports silence it created itself."""
        _, version, period_start = service(session).resolve_scope(
            project=project, window_spec="release:v1.9.0", now=NOW
        )

        assert version == "v1.9.0"
        assert as_utc(period_start) == NOW - RELEASE_SPAN_FALLBACK
        assert RELEASE_SPAN_FALLBACK == timedelta(days=28)

    def test_a_release_row_stamped_in_the_future_gets_the_fallback_too(
        self, session, org, project
    ):
        """Otherwise `period_start > now` and the window is empty by arithmetic --
        every ticket on the release reads as no-work, which is the manufactured
        absence this whole rule is trying not to produce."""
        self._release(
            session, org, project, "v1.9.0", created_at=NOW + timedelta(days=5)
        )

        _, _, period_start = service(session).resolve_scope(
            project=project, window_spec="release:v1.9.0", now=NOW
        )

        assert as_utc(period_start) == NOW - RELEASE_SPAN_FALLBACK

    def test_a_duration_scope_is_unaffected_by_any_of_this(self, session, org, project):
        """The control: a release row must not move an unscoped run's window."""
        self._release(
            session, org, project, "v1.9.0", created_at=NOW - timedelta(days=400)
        )

        spec, version, period_start = service(session).resolve_scope(
            project=project, window_spec="3d", now=NOW
        )

        assert (spec, version) == ("3d", None)
        assert as_utc(period_start) == NOW - timedelta(days=3)

    @pytest.mark.asyncio
    async def test_a_release_spec_in_the_window_is_the_same_scope(
        self, session, org, project, board, user
    ):
        """The stored spec must round-trip back into the scope it describes.

        The narrator echoes `window_spec` back on save, and the dashboard and
        the next read look the row up by it -- so `release:v1.9.0` arriving as a
        window has to mean the release, not 422.
        """
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        self._release(session, org, project, "v1.9.0")
        make_ticket(
            session, org, project, summary="in scope", assignee="Ada", release="v1.9.0"
        )
        make_ticket(session, org, project, summary="elsewhere", assignee="Ada")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="release:v1.9.0",
            now=NOW,
        )

        assert result.release == "v1.9.0"
        assert [line.ticket_summary for line in result.no_work_detected] == ["in scope"]

    def test_a_release_scope_survives_being_stored_and_read_back(
        self, session, org, project, user
    ):
        """`persist` canonicalises the spec, so it has to know this one."""
        svc = service(session)
        svc.persist(
            organization_id=org.id,
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="release:v1.9.0",
            body_markdown="the release so far",
            items=[],
            created_by=user.id,
        )
        session.commit()

        found = svc.live_summary(
            project_id=project.id,
            user_id=None,
            summary_type=SummaryType.SCRUM,
            window_spec="release:v1.9.0",
        )
        assert found is not None and found.body_markdown == "the release so far"

    def test_a_release_scope_must_name_a_version(self):
        from src.services.summary_service import canonical_window_spec

        with pytest.raises(InvalidWindowSpec):
            canonical_window_spec("release:")

    def test_the_version_is_kept_byte_exact(self):
        """`Ticket.release` is matched byte-exact, so the spec must not fold case.

        `V1.10.0` normalised to `v1.10.0` would name a release whose tickets are
        invisible to the very filter this spec exists to express.
        """
        from src.services.summary_service import canonical_window_spec

        assert canonical_window_spec("Release: V1.10.0 ") == "release:V1.10.0"


class TestProjectIsolation:
    """Two projects in one org. Summarise one; the other must not appear (#563).

    Every existing isolation test here is org-level, so the failure that
    actually happened -- one project's content in another's summary -- had
    nothing pinning it.
    """

    @pytest.fixture
    def other_project(self, session, org):
        p = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BB",
            name="Beta",
            description="the same org, a different project",
        )
        session.add(p)
        session.commit()
        return p

    @pytest.mark.asyncio
    async def test_nothing_from_the_sibling_project_reaches_the_summary(
        self, session, org, project, other_project, board, user
    ):
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        make_ticket(session, org, project, summary="ours", assignee="Ada", ref="PF-1")
        make_ticket(
            session,
            org,
            other_project,
            summary="theirs",
            assignee="Bee Stranger",
            ref="BB-1",
        )
        # A live summary on the sibling, written moments ago: gate 2 must not
        # see it, or one project's prose is served as another's.
        session.add(
            Summary(
                organization_id=org.id,
                project_id=other_project.id,
                window_spec="3d",
                summary_type=SummaryType.SCRUM,
                body_markdown="the sibling's prose",
                motivational_quote="",
                created_at=NOW - timedelta(minutes=1),
            )
        )
        session.commit()

        # Code activity naming the sibling's ticket, which the fetcher cannot
        # scope for us: the engine has to refuse to link it.
        activities = [
            CodeActivity(
                repo="beta",
                ticket_ref="BB-1",
                branch="BB-1-theirs",
                author_handle="bee",
                occurred_at=NOW - timedelta(hours=2),
                commit_shas=["deadbeef"],
            )
        ]
        svc = service(session, activities=activities)
        result = await svc.assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert result.outcome is SummaryOutcome.ASSEMBLED
        assert result.body_markdown is None
        rendered = [
            line.to_dict()
            for line in (
                list(result.active)
                + list(result.no_work_detected)
                + list(result.unassigned_active)
                + list(result.up_next)
            )
        ]
        assert "theirs" not in str(rendered)
        assert "BB-1" not in str(rendered)
        assert "Bee Stranger" not in str(rendered)
        # The counts are the project's own, too.
        assert result.unmapped_assignee_count == 1
        assert [u["assignee"] for u in svc.unmapped_assignees(project.id)] == ["Ada"]

    @pytest.mark.asyncio
    async def test_the_fingerprint_is_the_projects_own(
        self, session, org, project, other_project, board, user
    ):
        """A sibling's tickets in the fingerprint make its movement look like
        ours -- the summary would re-narrate on a day nothing here moved."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        ours = make_ticket(session, org, project, summary="ours")
        make_ticket(session, org, other_project, summary="theirs")

        result = await service(session).assemble(
            project=project,
            summary_type=SummaryType.SCRUM,
            window_spec="3d",
            now=NOW,
        )

        assert {row[0] for row in result.source_fingerprint["tickets"]} == {
            str(ours.id)
        }


class TestReleaseScopeRoute:
    """`?release=` on `summary-data` -- the door the CLI actually goes through."""

    def test_the_release_narrows_what_the_route_returns(
        self, client, auth, session, org, project, board, user
    ):
        record_sync(
            session,
            board,
            completed_at=datetime.now(timezone.utc) - timedelta(minutes=5),
            synced_by=user.id,
        )
        make_ticket(
            session, org, project, summary="in scope", assignee="Ada", release="v1.9.0"
        )
        make_ticket(session, org, project, summary="elsewhere", assignee="Ada")

        with patch(
            "src.services.summary_service.CodeActivityFetcher.fetch", return_value=[]
        ):
            response = client.get(
                f"{BASE}/{org.id}/projects/{project.id}/summary-data",
                params={"release": "v1.9.0"},
                headers=auth,
            )

        assert response.status_code == 200, response.text
        body = response.json()
        assert body["window_spec"] == "release:v1.9.0"
        assert [r["summary"] for r in body["no_work_detected"]] == ["in scope"]
        assert body["release"] == "v1.9.0"
        assert body["tickets_without_release_count"] == 1

    def test_current_is_resolved_by_the_existing_read_path_resolver(
        self, client, auth, session, org, project, board, user
    ):
        from src.domain.release import Release, ReleaseStatus

        record_sync(
            session,
            board,
            completed_at=datetime.now(timezone.utc) - timedelta(minutes=5),
            synced_by=user.id,
        )
        session.add(
            Release(
                organization_id=org.id,
                project_id=project.id,
                version="v2.0.0",
                name="v2.0.0",
                status=ReleaseStatus.IN_PROGRESS,
            )
        )
        session.commit()
        make_ticket(
            session, org, project, summary="cutting", assignee="Ada", release="v2.0.0"
        )

        with patch(
            "src.services.summary_service.CodeActivityFetcher.fetch", return_value=[]
        ):
            response = client.get(
                f"{BASE}/{org.id}/projects/{project.id}/summary-data",
                params={"release": "current"},
                headers=auth,
            )

        assert response.status_code == 200, response.text
        assert response.json()["release"] == "v2.0.0"

    def test_current_with_no_current_release_is_the_resolvers_own_404(
        self, client, auth, org, project
    ):
        """Not a silent fallback to a day window: the CLI used to do that, and a
        release summary that quietly became "the last week" is unmarked fiction.
        """
        response = client.get(
            f"{BASE}/{org.id}/projects/{project.id}/summary-data",
            params={"release": "current"},
            headers=auth,
        )
        assert response.status_code == 404, response.text
        assert "current release" in response.json()["detail"]


class TestRunningSyncs:
    """`running_syncs` is the complement of `latest_sync`, and the two must not
    be allowed to converge.

    One answers "is this data fresh", for which an unfinished run is no evidence
    and is excluded. The other answers "is something happening", for which an
    unfinished run is the only evidence. A filter dropped from either turns the
    pre-flight into a permanent yes or a permanent no, and both are silent.
    """

    def test_a_run_in_flight_is_reported(self, session, board, user):
        session.add(
            BoardSyncHistory(
                board_registration_id=board.id,
                sync_status=SyncStatus.IN_PROGRESS,
                started_at=NOW - timedelta(minutes=2),
                completed_at=None,
                synced_by=user.id,
            )
        )
        session.commit()
        running = service(session).running_syncs(board.project_id)
        assert len(running) == 1
        assert running[0].sync_status == SyncStatus.IN_PROGRESS

    def test_a_finished_run_is_not_running(self, session, board, user):
        """**The mutation that survived first time round.** Drop the
        completed_at filter and every project with any sync history reads as
        permanently busy, so the pre-flight refuses every sync forever — and
        says nothing that looks wrong while doing it."""
        record_sync(
            session, board, completed_at=NOW - timedelta(minutes=5), synced_by=user.id
        )
        assert service(session).running_syncs(board.project_id) == []

    def test_a_dry_run_is_not_work_to_wait_for(self, session, board, user):
        """A preview writes nothing, so nobody is blocked by one — the same rule
        `latest_sync` applies, for the same reason."""
        session.add(
            BoardSyncHistory(
                board_registration_id=board.id,
                sync_status=SyncStatus.IN_PROGRESS,
                started_at=NOW - timedelta(minutes=2),
                completed_at=None,
                dry_run=True,
                synced_by=user.id,
            )
        )
        session.commit()
        assert service(session).running_syncs(board.project_id) == []

    def test_another_project_s_run_is_not_this_project_s(self, session, board, user):
        session.add(
            BoardSyncHistory(
                board_registration_id=board.id,
                sync_status=SyncStatus.IN_PROGRESS,
                started_at=NOW - timedelta(minutes=2),
                completed_at=None,
                synced_by=user.id,
            )
        )
        session.commit()
        assert service(session).running_syncs("some-other-project") == []
