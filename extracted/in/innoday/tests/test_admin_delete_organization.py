"""
Tests for the platform-admin organization delete endpoint (PF-149 / BUG-3).

Before the fix, `DELETE /api/v1/admin/organizations/{organization_id}` always
raised `AttributeError: 'ScalarResult' object has no attribute 'delete'` because
`session.exec(select(...)).delete()` is not a valid call — `Session.exec()` on a
`select()` returns a `ScalarResult`, which has no `.delete()` method. This test
asserts the endpoint now succeeds via the shared cascade helper instead.
"""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.ticket import Ticket
from src.domain.user import User, UserRole
from src.routers.platform import require_platform_access
from tests.db_helpers import build_test_engine


@pytest.fixture
def engine():
    engine = build_test_engine()
    return engine


@pytest.fixture
def client(engine):
    def get_test_session():
        with Session(engine) as session:
            yield session

    admin_user = User(
        id=str(uuid4()),
        email="admin@platform.com",
        full_name="Platform Administrator",
        role=UserRole.ADMIN,
    )

    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[require_platform_access] = lambda: admin_user

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def org_with_children(engine):
    with Session(engine) as session:
        org = Organization(
            id=str(uuid4()), name="Admin Delete Org", alias="admin-delete-org"
        )
        session.add(org)
        session.commit()

        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias=f"T{str(uuid4())[:6]}".upper(),
            name="Admin Delete Project",
            description="Test project",
        )
        session.add(project)
        session.commit()

        ticket = Ticket(
            organization_id=org.id, project_id=project.id, summary="Child ticket"
        )
        session.add(ticket)
        session.commit()

        return org.id


def test_delete_organization_requires_confirm(client, org_with_children):
    response = client.delete(f"/api/v1/admin/organizations/{org_with_children}")
    assert response.status_code == 400


def test_delete_organization_succeeds_with_confirm(client, org_with_children, engine):
    response = client.delete(
        f"/api/v1/admin/organizations/{org_with_children}", params={"confirm": "true"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"

    with Session(engine) as session:
        assert session.get(Organization, org_with_children) is None
        remaining_tickets = session.exec(
            select(Ticket).where(Ticket.organization_id == org_with_children)
        ).all()
        assert remaining_tickets == []


def test_delete_platform_organization_is_forbidden(client, engine):
    with Session(engine) as session:
        platform_org = Organization(
            id=str(uuid4()), name="Platform", alias="platform-admin"
        )
        session.add(platform_org)
        session.commit()
        platform_org_id = platform_org.id

    response = client.delete(
        f"/api/v1/admin/organizations/{platform_org_id}", params={"confirm": "true"}
    )

    assert response.status_code == 403


def test_update_status_platform_organization_is_forbidden(client, engine):
    """
    Before the fix, this endpoint checked `org.is_platform_org`, which does not
    exist on the Organization model and raised an AttributeError. It should use
    the same `org.slug == "platform-admin"` check as delete_organization.
    """
    with Session(engine) as session:
        platform_org = Organization(
            id=str(uuid4()), name="Platform", alias="platform-admin"
        )
        session.add(platform_org)
        session.commit()
        platform_org_id = platform_org.id

    response = client.put(
        f"/api/v1/admin/organizations/{platform_org_id}/status",
        params={"is_active": "false"},
    )

    assert response.status_code == 403
