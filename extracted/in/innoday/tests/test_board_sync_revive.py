"""Tests that board re-sync revives soft-deleted tickets.

If a ticket was soft-deleted (e.g. via a board clear) but its external id is
still present at source on the next sync, `_create_or_update_ticket` should
match the existing row (update path, not create) and clear `deleted_at` so
the ticket is revived.
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus
from src.services.board_sync_service import BoardSyncService


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Example Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        name="Core Platform",
        description="Main platform project",
        alias="BP",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def board(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="BP Jira",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net",
        board_external_id="example",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


@pytest.fixture
def soft_deleted_ticket(db_session, org, project, board):
    t = Ticket(
        summary="old",
        organization_id=org.id,
        project_id=project.id,
        board_registration_id=board.id,
        external_ticket_id="ITPT-5",
        status=TicketStatus.TODO,
        deleted_at=datetime.now(timezone.utc),
    )
    db_session.add(t)
    db_session.commit()
    db_session.refresh(t)
    return t


def test_resync_revives_soft_deleted_ticket(
    db_session, org, project, board, soft_deleted_ticket
):
    assert soft_deleted_ticket.deleted_at is not None

    service = BoardSyncService()
    external = {
        "id": "ITPT-5",
        "summary": "old (updated)",
        "description": None,
        "status": "To Do",
        "assignee": None,
        "url": None,
        "source_platform": "jira",
        "priority": None,
        "parent_external_id": None,
    }

    was_created, ticket = service._create_or_update_ticket(
        external, board, db_session, project_id=project.id
    )

    assert was_created is False  # matched the existing (soft-deleted) row
    assert ticket.id == soft_deleted_ticket.id
    assert ticket.deleted_at is None  # revived
    assert ticket.summary == "old (updated)"
