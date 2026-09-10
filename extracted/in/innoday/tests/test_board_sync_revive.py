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

    outcome, ticket = service._create_or_update_ticket(
        external, board, db_session, project_id=project.id
    )

    # Matched the existing (soft-deleted) row, and reviving it is a change.
    assert outcome == "updated"
    assert ticket.id == soft_deleted_ticket.id
    assert ticket.deleted_at is None  # revived
    assert ticket.summary == "old (updated)"


def _board_ticket(**over):
    """One ticket as the adapter hands it over."""
    base = {
        "id": "ITPT-9",
        "summary": "Quiet ticket",
        "description": None,
        "status": "To Do",
        "assignee": None,
        "url": None,
        "source_platform": "jira",
        "priority": None,
        "parent_external_id": None,
    }
    base.update(over)
    return base


class TestAQuietBoardReportsNoUpdates:
    """A full sync writes only what moved, and must say so.

    The board returns every ticket on every full sync, and
    `_create_or_update_ticket` already compared each field and skipped the
    write when nothing differed. It then threw that answer away and returned
    "not created", so the caller counted every row as an update: BPAI's 258
    tickets reported as "258 updated" with nothing written. The sync looked
    wasteful; the sentence was.
    """

    def _sync(self, service, external, board, db_session, project):
        return service._create_or_update_ticket(
            external, board, db_session, project_id=project.id
        )

    def test_the_second_sync_of_an_untouched_ticket_is_unchanged(
        self, db_session, org, project, board
    ):
        service = BoardSyncService()
        external = _board_ticket()

        first, _ = self._sync(service, external, board, db_session, project)
        second, _ = self._sync(service, external, board, db_session, project)

        assert first == "created"
        assert second == "unchanged"

    def test_a_real_edit_still_reports_an_update(self, db_session, org, project, board):
        """The counter has to stay useful -- an "unchanged" that swallowed real
        edits would be the same bug pointing the other way."""
        service = BoardSyncService()
        self._sync(service, _board_ticket(), board, db_session, project)

        outcome, ticket = self._sync(
            service,
            _board_ticket(summary="Renamed on the board"),
            board,
            db_session,
            project,
        )

        assert outcome == "updated"
        assert ticket.summary == "Renamed on the board"

    def test_an_unchanged_ticket_keeps_its_updated_at(
        self, db_session, org, project, board
    ):
        """The restamp guard and the counter now answer the same question, so
        they must not be able to disagree: if the row was not touched, the
        outcome cannot be "updated"."""
        service = BoardSyncService()
        _, ticket = self._sync(service, _board_ticket(), board, db_session, project)
        db_session.commit()
        before = ticket.updated_at

        outcome, again = self._sync(
            service, _board_ticket(), board, db_session, project
        )

        assert outcome == "unchanged"
        assert again.updated_at == before
