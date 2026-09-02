"""
Tests for the non-board-scoped ticket cancel endpoint:
POST /api/v1/organizations/{organization_id}/tickets/{ticket_id}/cancel

Tickets are never hard-deleted (see GH #291): the CLI's `tickets delete`
called DELETE /organizations/{org_id}/tickets/{ticket_id}, but the only
registered DELETE route was board-scoped
(/boards/{board_id}/tickets/{ticket_id}), so every CLI delete 405'd. This
replaces hard delete entirely with a soft cancel: status -> CANCELLED, plus a
mandatory note recorded as a TicketComment.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketComment, TicketStatus
from src.domain.user import User, UserRole
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_engine():
    engine = build_test_engine()
    return engine


@pytest.fixture
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def client(db_engine):
    def override_get_session():
        with Session(db_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Test Org", alias="testorg")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def other_org(db_session):
    o = Organization(id=str(uuid4()), name="Other Org", alias="otherorg")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


def make_user_with_role(db_session, org, role):
    """Create a user and an active membership with the given role (not platform staff)."""
    u = User(
        id=str(uuid4()),
        email=f"{role.value.lower()}@example.com",
        username=f"{role.value.lower()}user",
        full_name=f"{role.value} User",
        role=UserRole.MEMBER,
        is_platform_member=False,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)

    membership = OrganizationMembership(
        user_id=u.id,
        organization_id=org.id,
        role=role,
        is_active=True,
    )
    db_session.add(membership)
    db_session.commit()

    return u


@pytest.fixture
def developer_user(db_session, org):
    return make_user_with_role(db_session, org, OrganizationRole.DEVELOPER)


@pytest.fixture
def member_user(db_session, org):
    return make_user_with_role(db_session, org, OrganizationRole.MEMBER)


@pytest.fixture
def project(db_session, org):
    p = Project(
        organization_id=org.id,
        alias="TEST",
        name="Test Project",
        description="A project for testing",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def ticket(db_session, org, project):
    t = Ticket(
        organization_id=org.id,
        project_id=project.id,
        summary="Original summary",
        description="Original description",
        assignee="alice",
        status=TicketStatus.TODO,
    )
    db_session.add(t)
    db_session.commit()
    db_session.refresh(t)
    return t


class TestCancelTicketByIdSuccess:
    def test_cancel_sets_status_cancelled(
        self, client, org, ticket, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}/cancel",
            json={"note": "No longer needed"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "cancelled"

    def test_cancel_does_not_delete_row(
        self, client, org, ticket, developer_user, db_session
    ):
        client.post(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}/cancel",
            json={"note": "Duplicate of #123"},
            headers=bearer_for(db_session, developer_user.id),
        )
        db_session.expire_all()
        still_there = db_session.get(Ticket, ticket.id)
        assert still_there is not None
        assert still_there.status == TicketStatus.CANCELLED

    def test_cancel_records_note_as_comment(
        self, client, org, ticket, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}/cancel",
            json={"note": "Superseded by the new design"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200

        comments = db_session.exec(
            select(TicketComment).where(TicketComment.ticket_id == ticket.id)
        ).all()
        assert len(comments) == 1
        assert comments[0].comment == "Superseded by the new design"

    def test_no_board_id_required_in_path(
        self, client, org, ticket, developer_user, db_session
    ):
        """Regression test: this route must not require a board_id segment."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}/cancel",
            json={"note": "No board needed"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert "boards" not in str(resp.request.url)


class TestCancelTicketByIdErrors:
    def test_missing_note_returns_422(
        self, client, org, ticket, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}/cancel",
            json={},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

    def test_empty_note_returns_422(
        self, client, org, ticket, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}/cancel",
            json={"note": ""},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

    def test_wrong_org_returns_404(self, client, other_org, ticket, db_session):
        dev = make_user_with_role(db_session, other_org, OrganizationRole.DEVELOPER)
        resp = client.post(
            f"/api/v1/organizations/{other_org.id}/tickets/{ticket.id}/cancel",
            json={"note": "Should not apply"},
            headers=bearer_for(db_session, dev.id),
        )
        assert resp.status_code == 404

    def test_nonexistent_ticket_returns_404(
        self, client, org, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets/999999/cancel",
            json={"note": "Nope"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 404

    def test_insufficient_role_returns_403(
        self, client, org, ticket, member_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}/cancel",
            json={"note": "Should be forbidden"},
            headers=bearer_for(db_session, member_user.id),
        )
        assert resp.status_code == 403
