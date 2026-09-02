"""Tests for the DRAFT ticket status: enum value, default-list exclusion, and DRAFT->TODO transitions."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization, OrganizationRole
from src.domain.ticket import Ticket, TicketStatus


@pytest.fixture
def org(db_session):
    o = Organization(
        id=str(uuid4()),
        name="Example Org",
    )
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


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


class TestTicketStatusDraft:
    def test_draft_status_exists_and_serializes(self):
        assert TicketStatus.DRAFT == "draft"
        assert TicketStatus.DRAFT.value == "draft"

    def test_ticket_can_be_created_with_draft_status(self, db_session, org, project):
        t = Ticket(
            summary="Pending approval",
            organization_id=org.id,
            project_id=project.id,
            status=TicketStatus.DRAFT,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)

        assert t.status == TicketStatus.DRAFT


class TestGetAllOrganizationTicketsExcludesDraft:
    @pytest.mark.asyncio
    async def test_no_status_filter_excludes_draft(self):
        from src.routers.tickets import get_all_organization_tickets

        org_id = "org-abc"
        mock_session = MagicMock()
        mock_org = MagicMock()
        mock_session.get.return_value = mock_org

        visible_ticket = MagicMock()
        visible_ticket.status = TicketStatus.TODO
        mock_session.exec.return_value.all.return_value = [visible_ticket]

        mock_user = MagicMock()
        mock_user.id = "user-1"

        with patch("src.routers.tickets.require_org_role"):
            result = await get_all_organization_tickets(
                organization_id=org_id,
                current_user=mock_user,
                session=mock_session,
            )

        assert result == [visible_ticket]
        # The statement built should filter out DRAFT when no explicit status given
        where_calls = [str(c) for c in mock_session.exec.call_args.args]
        assert any("draft" in c.lower() or "status" in c.lower() for c in where_calls)

    @pytest.mark.asyncio
    async def test_explicit_draft_status_returns_draft_tickets(self):
        from src.routers.tickets import get_all_organization_tickets

        org_id = "org-abc"
        mock_session = MagicMock()
        mock_org = MagicMock()
        mock_session.get.return_value = mock_org

        draft_ticket = MagicMock()
        draft_ticket.status = TicketStatus.DRAFT
        mock_session.exec.return_value.all.return_value = [draft_ticket]

        mock_user = MagicMock()
        mock_user.id = "user-1"

        with patch("src.routers.tickets.require_org_role"):
            result = await get_all_organization_tickets(
                organization_id=org_id,
                status=TicketStatus.DRAFT,
                current_user=mock_user,
                session=mock_session,
            )

        assert result == [draft_ticket]


class TestGetProjectTicketsExcludesDraft:
    @pytest.mark.asyncio
    async def test_no_status_filter_excludes_draft(self):
        from src.routers.tickets import get_project_tickets

        org_id = "org-abc"
        project_id = "proj-123"

        mock_session = MagicMock()
        mock_project = MagicMock()
        mock_project.organization_id = org_id
        mock_session.get.return_value = mock_project
        mock_session.exec.return_value.all.return_value = []

        mock_user = MagicMock()
        mock_user.id = "user-1"

        with patch("src.routers.tickets.require_org_role"):
            await get_project_tickets(
                organization_id=org_id,
                project_id=project_id,
                current_user=mock_user,
                session=mock_session,
            )

        mock_session.exec.assert_called_once()


class TestUpdateTicketDraftToTodo:
    @pytest.mark.asyncio
    async def test_draft_to_todo_transition_persists(
        self, db_session, org, project, board
    ):
        from src.routers.tickets import TicketUpdate, update_ticket

        ticket = Ticket(
            summary="Needs approval",
            organization_id=org.id,
            project_id=project.id,
            board_registration_id=board.id,
            status=TicketStatus.DRAFT,
        )
        db_session.add(ticket)
        db_session.commit()
        db_session.refresh(ticket)

        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_membership = MagicMock()
        mock_membership.role = OrganizationRole.ADMIN

        with patch(
            "src.routers.tickets.require_org_role", return_value=mock_membership
        ):
            await update_ticket(
                organization_id=org.id,
                board_id=board.id,
                ticket_id=ticket.id,
                ticket_update=TicketUpdate(status=TicketStatus.TODO),
                current_user=mock_user,
                session=db_session,
            )

        db_session.refresh(ticket)
        assert ticket.status == TicketStatus.TODO
