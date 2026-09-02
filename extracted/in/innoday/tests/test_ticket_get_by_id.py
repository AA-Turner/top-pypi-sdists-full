"""
Tests for the non-board-scoped ticket GET-by-id endpoint:
GET /api/v1/organizations/{organization_id}/tickets/{ticket_id}

Regression: the CLI's `tickets show` (and the MCP server) call
GET /organizations/{org_id}/tickets/{ticket_id}, but the only registered
routes on that org-scoped path were PUT (update) and POST .../cancel — the
GET-by-id path existed solely in its board-scoped form
(/boards/{board_id}/tickets/{ticket_id}). So every `tickets show` 405'd
(Method Not Allowed). This is the same class of bug the cancel endpoint had
(see test_ticket_cancel_by_id.py's module docstring): a client-facing
org-scoped route missing while only the board-scoped variant existed.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus
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
    """Create a user and an active membership with the given role."""
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


class TestGetTicketByIdSuccess:
    def test_get_returns_the_ticket(self, client, org, ticket, member_user, db_session):
        resp = client.get(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            headers=bearer_for(db_session, member_user.id),
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == ticket.id
        assert body["summary"] == "Original summary"

    def test_no_board_id_required_in_path(
        self, client, org, ticket, member_user, db_session
    ):
        """Regression: this route must resolve without a board_id segment.

        Before the fix, GET on this org-scoped path returned 405 because only
        PUT/POST were registered there.
        """
        resp = client.get(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            headers=bearer_for(db_session, member_user.id),
        )
        assert resp.status_code == 200
        assert "boards" not in str(resp.request.url)

    def test_any_member_can_read(self, client, org, ticket, member_user, db_session):
        """Read is available to a plain MEMBER (no DEVELOPER/ADMIN needed),
        unlike update/cancel which require elevated roles."""
        resp = client.get(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            headers=bearer_for(db_session, member_user.id),
        )
        assert resp.status_code == 200


class TestGetTicketByIdErrors:
    def test_nonexistent_ticket_returns_404_not_405(
        self, client, org, member_user, db_session
    ):
        """A missing ticket must be 404 — proving the route matched and ran
        the handler, rather than 405 (route/method not registered)."""
        resp = client.get(
            f"/api/v1/organizations/{org.id}/tickets/999999",
            headers=bearer_for(db_session, member_user.id),
        )
        assert resp.status_code == 404

    def test_wrong_org_returns_404(self, client, other_org, ticket, db_session):
        reader = make_user_with_role(db_session, other_org, OrganizationRole.MEMBER)
        resp = client.get(
            f"/api/v1/organizations/{other_org.id}/tickets/{ticket.id}",
            headers=bearer_for(db_session, reader.id),
        )
        assert resp.status_code == 404
