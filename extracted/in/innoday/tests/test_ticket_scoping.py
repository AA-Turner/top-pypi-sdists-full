"""Tests for project-scoped tickets: project_id FK, project_ref_number, project alias, per-project endpoint."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
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


# ─── Ticket.project_id ────────────────────────────────────────────────────────


class TestTicketProjectId:
    def test_ticket_can_store_project_id(self, db_session, org, project):
        t = Ticket(
            summary="Fix login bug",
            organization_id=org.id,
            project_id=project.id,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)

        assert t.project_id == project.id

    def test_ticket_project_id_required(self, db_session, org):
        t = Ticket(
            summary="Unscoped ticket",
            organization_id=org.id,
        )
        db_session.add(t)
        with pytest.raises(Exception):
            db_session.commit()

    def test_ticket_project_relationship(self, db_session, org, project):
        t = Ticket(
            summary="Test relationship",
            organization_id=org.id,
            project_id=project.id,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)

        # Navigate the relationship
        db_session.refresh(project)
        assert any(ticket.id == t.id for ticket in project.tickets)

    def test_project_lists_its_tickets(self, db_session, org, project):
        other_project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            name="Other",
            description="Another project",
            alias="OTHER",
        )
        db_session.add(other_project)
        db_session.commit()

        t1 = Ticket(summary="A", organization_id=org.id, project_id=project.id)
        t2 = Ticket(summary="B", organization_id=org.id, project_id=project.id)
        t3 = Ticket(summary="C", organization_id=org.id, project_id=other_project.id)
        for t in (t1, t2, t3):
            db_session.add(t)
        db_session.commit()
        db_session.refresh(project)

        project_ticket_ids = {ticket.id for ticket in project.tickets}
        db_session.refresh(t1)
        db_session.refresh(t2)
        db_session.refresh(t3)
        assert t1.id in project_ticket_ids
        assert t2.id in project_ticket_ids
        assert t3.id not in project_ticket_ids


# ─── Project.alias ───────────────────────────────────────────────────────────


class TestProjectAlias:
    def test_project_stores_alias(self, db_session, org):
        p = Project(
            id=str(uuid4()),
            organization_id=org.id,
            name="Pixelfuel Core",
            description="Desc",
            alias="PF",
        )
        db_session.add(p)
        db_session.commit()
        db_session.refresh(p)

        assert p.alias == "PF"

    @pytest.mark.asyncio
    async def test_project_alias_required(self, db_session, org):
        """alias is now required (slug was retired; alias replaced it).

        Enforcement lives in ProjectService._normalize_alias (the DB column is
        not declared NOT NULL, so requiredness is a service-layer contract):
        creating a project with a blank alias must raise ValueError.
        """
        from src.services.project_service import ProjectService

        service = ProjectService(db_session)
        with pytest.raises(ValueError, match="required"):
            await service.create_project(
                organization_id=org.id,
                alias="",
                name="No Alias",
                description="Desc",
            )

    def test_project_alias_unique(self, db_session, org):
        p1 = Project(
            id=str(uuid4()),
            organization_id=org.id,
            name="Project A",
            description="Desc",
            alias="XX",
        )
        p2 = Project(
            id=str(uuid4()),
            organization_id=org.id,
            name="Project B",
            description="Desc",
            alias="XX",  # duplicate alias
        )
        db_session.add(p1)
        db_session.commit()
        db_session.add(p2)

        with pytest.raises(Exception):  # IntegrityError from unique constraint
            db_session.commit()


# ─── Ticket.project_ref_number ───────────────────────────────────────────────


class TestProjectRefNumber:
    def test_ticket_can_store_project_ref_number(self, db_session, org, project):
        t = Ticket(
            summary="Ticket with ref",
            organization_id=org.id,
            project_id=project.id,
            project_ref_number=42,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)

        assert t.project_ref_number == 42

    def test_project_ref_number_nullable(self, db_session, org, project):
        t = Ticket(
            summary="No ref number",
            organization_id=org.id,
            project_id=project.id,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)

        assert t.project_ref_number is None

    def test_display_ref_uses_alias_and_number(self, db_session, org, project):
        """Verify alias + project_ref_number compose the expected display format."""
        t = Ticket(
            summary="Auth refactor",
            organization_id=org.id,
            project_id=project.id,
            project_ref_number=7,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)
        db_session.refresh(project)

        display = f"{project.alias}-{t.project_ref_number}"
        assert display == "BP-7"


# ─── Per-project tickets endpoint ────────────────────────────────────────────


class TestGetProjectTicketsEndpoint:
    """Unit tests for GET /orgs/{org_id}/projects/{project_id}/tickets."""

    @pytest.mark.asyncio
    async def test_returns_tickets_for_project(self):
        from src.routers.tickets import get_project_tickets

        org_id = "org-abc"
        project_id = "proj-123"

        mock_session = MagicMock()
        mock_project = MagicMock()
        mock_project.organization_id = org_id
        mock_session.get.return_value = mock_project

        t1 = MagicMock()
        t1.id = 1
        t1.project_id = project_id
        t2 = MagicMock()
        t2.id = 2
        t2.project_id = project_id
        mock_session.exec.return_value.all.return_value = [t1, t2]

        mock_user = MagicMock()
        mock_user.id = "user-1"

        with patch("src.routers.tickets.require_org_role"):
            result = await get_project_tickets(
                organization_id=org_id,
                project_id=project_id,
                current_user=mock_user,
                session=mock_session,
            )

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_returns_404_when_project_not_found(self):
        from fastapi import HTTPException

        from src.routers.tickets import get_project_tickets

        mock_session = MagicMock()
        mock_session.get.return_value = None  # project not found

        mock_user = MagicMock()
        mock_user.id = "user-1"

        with patch("src.routers.tickets.require_org_role"):
            with pytest.raises(HTTPException) as exc_info:
                await get_project_tickets(
                    organization_id="org-abc",
                    project_id="nonexistent",
                    current_user=mock_user,
                    session=mock_session,
                )

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_returns_403_when_project_in_wrong_org(self):
        from fastapi import HTTPException

        from src.routers.tickets import get_project_tickets

        mock_session = MagicMock()
        mock_project = MagicMock()
        mock_project.organization_id = "other-org"  # different org
        mock_session.get.return_value = mock_project

        mock_user = MagicMock()
        mock_user.id = "user-1"

        with patch("src.routers.tickets.require_org_role"):
            with pytest.raises(HTTPException) as exc_info:
                await get_project_tickets(
                    organization_id="requesting-org",
                    project_id="proj-123",
                    current_user=mock_user,
                    session=mock_session,
                )

        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_filters_by_status(self):
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
            result = await get_project_tickets(
                organization_id=org_id,
                project_id=project_id,
                status=TicketStatus.DONE,
                current_user=mock_user,
                session=mock_session,
            )

        assert result == []
        # Verify exec was called (status filter applied)
        mock_session.exec.assert_called_once()

    @pytest.mark.asyncio
    async def test_org_level_tickets_span_all_projects(self):
        """Org-level query should return tickets regardless of project_id."""
        from src.routers.tickets import get_all_organization_tickets

        org_id = "org-abc"
        mock_session = MagicMock()
        mock_org = MagicMock()
        mock_session.get.return_value = mock_org

        t_with_project = MagicMock()
        t_with_project.organization_id = org_id
        t_with_project.project_id = "proj-1"

        t_without_project = MagicMock()
        t_without_project.organization_id = org_id
        t_without_project.project_id = None

        mock_session.exec.return_value.all.return_value = [
            t_with_project,
            t_without_project,
        ]

        mock_user = MagicMock()
        mock_user.id = "user-1"

        with patch("src.routers.tickets.require_org_role"):
            result = await get_all_organization_tickets(
                organization_id=org_id,
                current_user=mock_user,
                session=mock_session,
            )

        assert len(result) == 2


# ─── board_sync_service: project_id resolution ──────────────────────────────


class TestBoardSyncProjectId:
    """Tests for _get_project_id_for_board and project_id assignment at sync."""

    def test_get_project_id_for_board_found(self, db_session, org, board, project):
        pass

        from src.services.board_sync_service import BoardSyncService

        service = BoardSyncService()
        result = service._get_project_id_for_board(board, db_session)

        assert result == project.id

    def test_get_project_id_for_board_not_found(self, db_session, org):
        from src.services.board_sync_service import BoardSyncService

        # project_id is NOT NULL at the DB level now, so a board without one
        # can no longer be persisted -- construct it in-memory only, to
        # exercise the defense-in-depth raise in _get_project_id_for_board
        # (e.g. a raw-SQL row that bypassed the constraint).
        unlinked_board = BoardRegistration(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=None,
            board_name="Orphan Board",
            board_type=BoardType.TRELLO,
            board_url="https://trello.com/b/orphan",
            board_external_id="orphan-board",
        )

        service = BoardSyncService()

        with pytest.raises(ValueError, match="has no project_id"):
            service._get_project_id_for_board(unlinked_board, db_session)

    def test_create_ticket_assigns_project_id(self, db_session, org, board, project):
        from src.services.board_sync_service import BoardSyncService

        service = BoardSyncService()

        external = {
            "id": "ENG-001",
            "summary": "Test ticket",
            "description": None,
            "status": "backlog",
            "assignee": None,
            "url": None,
            "source_platform": "jira",
            "priority": None,
            "parent_external_id": None,
        }

        was_created, ticket = service._create_or_update_ticket(
            external, board, db_session, project_id=project.id
        )

        assert was_created is True
        assert ticket.project_id == project.id

    def test_create_ticket_assigns_project_ref_number(
        self, db_session, org, board, project
    ):
        from src.services.board_sync_service import BoardSyncService

        service = BoardSyncService()

        # First ticket in org
        t1_data = {
            "id": "ENG-001",
            "summary": "First",
            "description": None,
            "status": "backlog",
            "assignee": None,
            "url": None,
            "source_platform": "jira",
            "priority": None,
            "parent_external_id": None,
        }
        _, t1 = service._create_or_update_ticket(
            t1_data, board, db_session, project_id=project.id
        )
        assert t1.project_ref_number == 1

        # Second ticket in same org gets ref 2
        t2_data = {
            "id": "ENG-002",
            "summary": "Second",
            "description": None,
            "status": "todo",
            "assignee": None,
            "url": None,
            "source_platform": "jira",
            "priority": None,
            "parent_external_id": None,
        }
        _, t2 = service._create_or_update_ticket(
            t2_data, board, db_session, project_id=project.id
        )
        assert t2.project_ref_number == 2

    def test_update_ticket_does_not_change_project_ref_number(
        self, db_session, org, board, project
    ):
        from src.services.board_sync_service import BoardSyncService

        service = BoardSyncService()
        data = {
            "id": "ENG-003",
            "summary": "Original title",
            "description": None,
            "status": "backlog",
            "assignee": None,
            "url": None,
            "source_platform": "jira",
            "priority": None,
            "parent_external_id": None,
        }

        _, ticket = service._create_or_update_ticket(
            data, board, db_session, project_id=project.id
        )
        original_ref = ticket.project_ref_number
        assert original_ref is not None

        # Sync the same external ticket again (update path)
        data["summary"] = "Updated title"
        was_created, updated = service._create_or_update_ticket(
            data, board, db_session, project_id=project.id
        )

        assert was_created is False
        assert updated.project_ref_number == original_ref
        assert updated.summary == "Updated title"
