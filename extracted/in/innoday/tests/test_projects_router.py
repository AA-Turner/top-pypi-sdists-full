"""Router-level tests for the projects API: ticket_creation_config round-trip and validation."""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project, ProjectPriority, ProjectStatus
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
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def user(db_session):
    u = User(
        id=str(uuid4()),
        email="test@example.com",
        full_name="Test User",
        role=UserRole.MEMBER,
        is_platform_member=True,  # bypass membership checks
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def auth_headers(user, db_session):
    return bearer_for(db_session, user.id)


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias="TEST",
        name="Test Project",
        description="A test project",
        status=ProjectStatus.ACTIVE,
        priority=ProjectPriority.MEDIUM,
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


class TestProjectTicketCreationConfig:
    def test_put_round_trips_ticket_creation_config(
        self, client, org, project, auth_headers
    ):
        config = {
            "board_id": "board-123",
            "labels": ["bug", "automated"],
            "issue_type": "Task",
            "parent_epic": "EPIC-1",
        }
        resp = client.put(
            f"/api/v1/organizations/{org.id}/projects/{project.id}",
            json={"ticket_creation_config": config},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["ticket_creation_config"] == config

        get_resp = client.get(
            f"/api/v1/organizations/{org.id}/projects/{project.id}",
            headers=auth_headers,
        )
        assert get_resp.status_code == 200
        assert get_resp.json()["ticket_creation_config"] == config

    def test_put_malformed_ticket_creation_config_returns_422(
        self, client, org, project, auth_headers
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/projects/{project.id}",
            json={
                "ticket_creation_config": {"labels": ["bug"]}
            },  # missing required board_id
            headers=auth_headers,
        )
        assert resp.status_code == 422


class TestProjectArchive:
    """DELETE .../projects/{id} -- archives, never removes.

    The route had no test coverage at all: the ADMIN guard, the cross-org 403,
    and the fact that the response says "archived" while the CLI said
    "deleted" were all unverified.
    """

    def test_delete_archives_and_reports_what_changed(
        self, client, org, project, auth_headers, db_session
    ):
        resp = client.delete(
            f"/api/v1/organizations/{org.id}/projects/{project.id}",
            headers=auth_headers,
        )

        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == project.id
        assert body["alias"] == "TEST"
        assert body["status"] == ProjectStatus.ARCHIVED.value
        # The prior status is what makes the outcome auditable.
        assert body["previous_status"] == ProjectStatus.ACTIVE.value

        db_session.expire_all()
        assert db_session.get(Project, project.id).status == ProjectStatus.ARCHIVED

    def test_archived_project_row_survives(
        self, client, org, project, auth_headers, db_session
    ):
        """Archive is soft -- the row and its alias must still be there."""
        client.delete(
            f"/api/v1/organizations/{org.id}/projects/{project.id}",
            headers=auth_headers,
        )

        resp = client.get(
            f"/api/v1/organizations/{org.id}/projects/{project.id}",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["alias"] == "TEST"

    def test_delete_accepts_an_alias(self, client, org, project, auth_headers):
        resp = client.delete(
            f"/api/v1/organizations/{org.id}/projects/TEST",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["id"] == project.id

    def test_delete_unknown_project_returns_404(self, client, org, auth_headers):
        resp = client.delete(
            f"/api/v1/organizations/{org.id}/projects/{uuid4()}",
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_delete_across_organizations_is_refused(
        self, client, org, project, auth_headers, db_session
    ):
        """A project may only be archived through its own organization."""
        other = Organization(id=str(uuid4()), name="Other Org")
        db_session.add(other)
        db_session.commit()

        resp = client.delete(
            f"/api/v1/organizations/{other.id}/projects/{project.id}",
            headers=auth_headers,
        )
        assert resp.status_code == 403

        db_session.expire_all()
        assert db_session.get(Project, project.id).status == ProjectStatus.ACTIVE
