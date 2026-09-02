from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus
from src.services.board_clear_service import clear_board_tickets, soft_delete_board
from tests.db_helpers import build_test_engine


@pytest.fixture
def session():
    engine = build_test_engine()
    with Session(engine) as s:
        yield s


def _seed(session, n=3):
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
    for i in range(n):
        session.add(
            Ticket(
                summary=f"t{i}",
                organization_id=org.id,
                project_id=proj.id,
                board_registration_id=board.id,
                external_ticket_id=f"E-{i}",
                status=TicketStatus.TODO,
            )
        )
    session.commit()
    return org, proj, board


def test_clear_soft_deletes_all_live_tickets(session):
    _, _, board = _seed(session, 3)
    count = clear_board_tickets(session, board.id)
    assert count == 3
    rows = session.exec(
        select(Ticket).where(Ticket.board_registration_id == board.id)
    ).all()
    assert len(rows) == 3  # rows preserved
    assert all(r.deleted_at is not None for r in rows)
    session.refresh(board)
    assert board.deleted_at is None  # board untouched by clear
    assert board.is_active is True


def test_clear_dry_run_mutates_nothing(session):
    _, _, board = _seed(session, 2)
    count = clear_board_tickets(session, board.id, dry_run=True)
    assert count == 2
    rows = session.exec(
        select(Ticket).where(Ticket.board_registration_id == board.id)
    ).all()
    assert all(r.deleted_at is None for r in rows)


def test_clear_skips_already_deleted(session):
    _, _, board = _seed(session, 2)
    clear_board_tickets(session, board.id)  # first clear -> 2
    count = clear_board_tickets(session, board.id)  # second clear -> 0 live left
    assert count == 0


def test_soft_delete_board_sets_flags_and_cascades(session):
    _, _, board = _seed(session, 2)
    count = soft_delete_board(session, board)
    assert count == 2
    session.refresh(board)
    assert board.deleted_at is not None
    assert board.is_active is False
    rows = session.exec(
        select(Ticket).where(Ticket.board_registration_id == board.id)
    ).all()
    assert all(r.deleted_at is not None for r in rows)
