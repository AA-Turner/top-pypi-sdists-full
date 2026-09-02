"""`releases content` says when the tickets were last refreshed, and never blocks.

A stale board and a quiet release are the same shape on screen: both say nothing
moved. One is a fact about the team and the other is a fact about a credential
that expired, and only one is actionable -- so the payload has to carry which.

**Reported, not enforced.** The pull-request half of a release report comes from
GitHub and is unaffected by a stale board, so refusing to answer would withhold
good data over a defect in unrelated data. The MCP tool asks the caller whether
to sync; the HTTP route just tells the truth and returns.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.board import BoardRegistration, BoardSyncHistory, SyncStatus
from src.domain.organization import Organization
from src.domain.project import Project
from src.routers.summaries import _board_sync_state
from tests.db_helpers import build_test_engine

NOW = datetime.now(timezone.utc)


@pytest.fixture
def world():
    engine = build_test_engine()
    with Session(engine) as session:
        org = Organization(id=str(uuid4()), name="BP", alias=f"b{str(uuid4())[:5]}")
        session.add(org)
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BPAI",
            name="Bright Power AI",
            description="d",
        )
        session.add(project)
        session.commit()
        yield session, org, project


def _board(session, org, project) -> BoardRegistration:
    """A sync belongs to a board, and a board to a project.

    `latest_sync` joins through the registration rather than reading a
    `project_id` off the history row -- there isn't one. A fixture that skipped
    the board made every row invisible to the query, which is a test that passes
    for the wrong reason waiting to happen.
    """
    board = BoardRegistration(
        id=str(uuid4()),
        user_id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="BPAI",
        board_url="https://linear.app/havilandsoftware",
        board_external_id="bpai-board",
        board_type="linear",
    )
    session.add(board)
    session.commit()
    return board


def _sync(session, board, *, minutes_ago: int, status=SyncStatus.COMPLETED, error=None):
    row = BoardSyncHistory(
        id=str(uuid4()),
        board_registration_id=board.id,
        sync_status=status,
        dry_run=False,
        completed_at=NOW - timedelta(minutes=minutes_ago),
        error_message=error,
    )
    session.add(row)
    session.commit()
    return row


class TestItReportsTheAge:
    def test_a_recent_sync_is_not_stale(self, world):
        session, org, project = world
        _sync(session, _board(session, org, project), minutes_ago=10)
        state = _board_sync_state(session, project.id)
        assert state["stale"] is False
        assert state["age_seconds"] < 3600
        assert state["synced_at"] is not None

    def test_over_an_hour_is_stale(self, world):
        session, org, project = world
        _sync(session, _board(session, org, project), minutes_ago=90)
        assert _board_sync_state(session, project.id)["stale"] is True

    def test_never_synced_is_stale_and_says_so(self, world):
        """Not a hedge: never-synced tickets are the stalest there are, and "no
        evidence of a sync" does not honestly read as "probably fine"."""
        session, org, project = world
        _board(session, org, project)
        state = _board_sync_state(session, project.id)
        assert state["stale"] is True
        assert state["synced_at"] is None
        assert state["age_seconds"] is None

    def test_a_failed_run_is_not_freshness(self, world):
        """A failure carries a `completed_at` too, so the clock alone would call
        an expired credential fresh for an hour after every failure."""
        session, org, project = world
        _sync(
            session,
            _board(session, org, project),
            minutes_ago=2,
            status=SyncStatus.FAILED,
            error="401",
        )
        state = _board_sync_state(session, project.id)
        assert state["stale"] is True
        assert state["error"] == "401"

    def test_the_error_is_carried_not_summarised(self, world):
        session, org, project = world
        _sync(
            session,
            _board(session, org, project),
            minutes_ago=5,
            status=SyncStatus.FAILED,
            error="Linear: GraphQL validation failed",
        )
        assert "GraphQL" in _board_sync_state(session, project.id)["error"]

    def test_it_reads_the_newest_run(self, world):
        session, org, project = world
        board = _board(session, org, project)
        _sync(session, board, minutes_ago=200)
        _sync(session, board, minutes_ago=5)
        assert _board_sync_state(session, project.id)["stale"] is False

    def test_another_projects_sync_is_not_this_one_s(self, world):
        session, org, project = world
        other = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BPCL",
            name="BP Cloud",
            description="d",
        )
        session.add(other)
        session.commit()
        _sync(session, _board(session, org, other), minutes_ago=2)

        assert _board_sync_state(session, project.id)["synced_at"] is None
