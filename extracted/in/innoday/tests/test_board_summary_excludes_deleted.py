"""Regression test for C2: soft-deleted tickets must NOT surface in the board
summary data (the feature's own flagship surface -- backs the
get_board_summary_data MCP tool + CLI board summary).

Seeds a board with a live ticket and a soft-deleted ticket, calls the shared
_assemble_board_summary_data assembler, and asserts the soft-deleted ticket is
excluded from the counts and the active-ticket data.
"""

import asyncio
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.summary import SummaryType
from src.domain.ticket import Ticket, TicketStatus
from src.routers.boards import _assemble_board_summary_data
from tests.db_helpers import build_test_engine


@pytest.fixture
def session():
    engine = build_test_engine()
    with Session(engine) as s:
        yield s


def _seed(session):
    org = Organization(id=str(uuid4()), name="Org")
    proj = Project(
        id=str(uuid4()),
        name="P",
        alias="P",
        description="d",
        organization_id=org.id,
    )
    board = BoardRegistration(
        id=str(uuid4()),
        user_id=str(uuid4()),
        organization_id=org.id,
        project_id=proj.id,
        board_name="B",
        board_url="https://x",
        board_type=BoardType.JIRA,
        board_external_id="ext-1",
    )
    session.add_all([org, proj, board])
    session.commit()

    live = Ticket(
        summary="live-in-progress",
        organization_id=org.id,
        project_id=proj.id,
        board_registration_id=board.id,
        external_ticket_id="E-live",
        status=TicketStatus.IN_PROGRESS,
    )
    deleted = Ticket(
        summary="deleted-in-progress",
        organization_id=org.id,
        project_id=proj.id,
        board_registration_id=board.id,
        external_ticket_id="E-deleted",
        status=TicketStatus.IN_PROGRESS,
        deleted_at=datetime.now(timezone.utc),  # soft-deleted
    )
    session.add_all([live, deleted])
    session.commit()
    return org, proj, board


def test_board_summary_excludes_soft_deleted_tickets(session):
    org, _, board = _seed(session)

    data = asyncio.run(
        _assemble_board_summary_data(
            organization_id=org.id,
            board_id=board.id,
            summary_type=SummaryType.STATUS,
            since_version=None,
            github_org=None,
            session=session,
        )
    )

    stats = data["stats"]
    # Only the single LIVE ticket is counted, not the soft-deleted one.
    assert stats["total_tickets"] == 1
    assert stats["in_progress"] == 1
    assert stats["active_tickets"] == 1

    # The soft-deleted ticket's summary must not appear anywhere in the
    # assembled context messages.
    joined = "\n".join(data["messages"])
    assert "live-in-progress" in joined
    assert "deleted-in-progress" not in joined
