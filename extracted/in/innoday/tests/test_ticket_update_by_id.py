"""
Tests for the non-board-scoped ticket update endpoint:
PUT /api/v1/organizations/{organization_id}/tickets/{ticket_id}

Before this endpoint existed, the MCP `update_ticket` tool and the CLI's
`update_ticket` client method both called this URL shape, but `tickets.py`
only defined a board-scoped PUT (`/boards/{board_id}/tickets/{ticket_id}`),
so every MCP/CLI update request 404'd. This also covers the new `release`
field, which previously had no way to be set through the API.
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
from src.domain.release import Release, ReleaseStatus
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
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def other_org(db_session):
    o = Organization(id=str(uuid4()), name="Other Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


def make_user_with_role(db_session, org, role):
    """Create a user and an active membership with the given role (not platform staff)."""
    u = User(
        id=str(uuid4()),
        email=f"{role.value.lower()}@example.com",
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
def other_project(db_session, other_org):
    p = Project(
        organization_id=other_org.id,
        alias="OTHER",
        name="Other Project",
        description="A project in a different org",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def second_project(db_session, org):
    """A second project in the same org, used to test reassigning a ticket's project_id."""
    p = Project(
        organization_id=org.id,
        alias="SECOND",
        name="Second Project",
        description="A second project for testing project_id reassignment",
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


class TestUpdateTicketByIdFieldUpdates:
    def test_update_summary(self, client, org, ticket, developer_user, db_session):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"summary": "New summary"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["summary"] == "New summary"

    def test_update_description(self, client, org, ticket, developer_user, db_session):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"description": "New description"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["description"] == "New description"

    def test_update_assignee(self, client, org, ticket, developer_user, db_session):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"assignee": "bob"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["assignee"] == "bob"

    def test_update_status(self, client, org, ticket, developer_user, db_session):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"status": "in progress"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "in progress"

    def test_update_release(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        # A version the project is actually planning into -- since #522 the field
        # is validated against the project's outstanding releases, so the
        # `pipeline` fixture is what makes this a legal value rather than a
        # free-text string.
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": "v1.11.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.11.0"

        db_session.refresh(ticket)
        assert ticket.release == "v1.11.0"

    def test_update_project_id(
        self, client, org, ticket, developer_user, second_project, db_session
    ):
        # `ticket` already belongs to `project` (see fixture); reassign it to
        # `second_project` to prove the update actually changes the value.
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"project_id": second_project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["project_id"] == second_project.id

        db_session.refresh(ticket)
        assert ticket.project_id == second_project.id

    def test_omitting_project_id_preserves_existing_value(
        self, client, org, ticket, developer_user, second_project, db_session
    ):
        # First reassign project_id
        client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"project_id": second_project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        # Then update an unrelated field without project_id in the payload
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"summary": "Unrelated update"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["project_id"] == second_project.id

    def test_update_multiple_fields_at_once(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={
                "summary": "Combined update",
                "assignee": "carol",
                "status": "done",
                "release": "v1.11.0",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"] == "Combined update"
        assert data["assignee"] == "carol"
        assert data["status"] == "done"
        assert data["release"] == "v1.11.0"


class TestUpdateTicketByIdErrors:
    def test_wrong_org_returns_404(self, client, other_org, ticket, db_session):
        # Create a developer in other_org and try to update a ticket owned by `org`
        dev = make_user_with_role(db_session, other_org, OrganizationRole.DEVELOPER)
        resp = client.put(
            f"/api/v1/organizations/{other_org.id}/tickets/{ticket.id}",
            json={"summary": "Should not apply"},
            headers=bearer_for(db_session, dev.id),
        )
        assert resp.status_code == 404

    def test_nonexistent_ticket_returns_404(
        self, client, org, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/999999",
            json={"summary": "Nope"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 404

    def test_insufficient_role_returns_403(
        self, client, org, ticket, member_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"summary": "Should be forbidden"},
            headers=bearer_for(db_session, member_user.id),
        )
        assert resp.status_code == 403

    def test_project_id_from_different_org_returns_404(
        self, client, org, ticket, developer_user, other_project, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"project_id": other_project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 404

    def test_nonexistent_project_id_returns_404(
        self, client, org, ticket, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"project_id": str(uuid4())},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 404

    def test_no_board_id_required_in_path(
        self, client, org, ticket, developer_user, db_session
    ):
        """Regression test: this route must not require a board_id segment."""
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"summary": "No board needed"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert "boards" not in str(resp.request.url)


# ---------------------------------------------------------------------------
# `release` on update -- the same validation as create, plus the ordering rule
# ---------------------------------------------------------------------------


def _release(db_session, org, project, version, status):
    row = Release(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        version=version,
        status=status,
    )
    db_session.add(row)
    db_session.commit()
    return row


@pytest.fixture
def pipeline(db_session, org, project):
    """`project`'s two open slots, plus a shipped and an archived version."""
    return {
        version: _release(db_session, org, project, version, status)
        for version, status in (
            ("v1.10.0", ReleaseStatus.IN_PROGRESS),
            ("v1.11.0", ReleaseStatus.PLANNED),
            ("v1.9.0", ReleaseStatus.RELEASED),
            ("v1.8.0", ReleaseStatus.ARCHIVED),
        )
    }


@pytest.fixture
def second_project_pipeline(db_session, org, second_project):
    """A different project's open version. Version strings only mean something
    inside a project, so this one must not be accepted for `project`'s tickets."""
    return _release(
        db_session, org, second_project, "v4.0.0", ReleaseStatus.IN_PROGRESS
    )


class TestUpdateTicketByIdRelease:
    def test_an_outstanding_version_round_trips(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": "v1.11.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.11.0"

    def test_an_unknown_version_is_422_listing_the_real_options(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": "v9.9.9"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        assert isinstance(detail, str), detail
        assert "v1.10.0" in detail and "v1.11.0" in detail

        db_session.refresh(ticket)
        assert ticket.release is None, "a rejected update must write nothing"

    def test_current_resolves_to_the_version_being_cut(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": "current"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.10.0"

    def test_a_released_version_is_rejected_and_says_so(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": "v1.9.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422
        assert "released" in resp.json()["detail"]

    def test_matching_is_case_sensitive(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": "V1.10.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

    def test_an_empty_string_clears_the_field_without_validating(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        """Taking a ticket *out* of a release must not require naming a valid one."""
        client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": "v1.11.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"release": ""},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert not resp.json()["release"]

    def test_an_unmatched_stored_release_does_not_block_other_updates(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        """Validation keys off the *payload*, never off the row.

        Board sync writes arbitrary external versions (`2026.08-hotfix`); if the
        stored value were validated, every such ticket would become impossible to
        touch at all.
        """
        ticket.release = "2026.08-hotfix"
        db_session.add(ticket)
        db_session.commit()

        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"status": "done"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "done"
        assert resp.json()["release"] == "2026.08-hotfix", "left alone, not cleared"

    def test_the_validator_is_wired_to_this_route(
        self, client, org, ticket, project, pipeline, developer_user, db_session
    ):
        with patch(
            "src.routers.tickets.resolve_ticket_release", return_value="v1.11.0"
        ) as spy:
            resp = client.put(
                f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
                json={"release": "v1.11.0"},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        spy.assert_called_once()
        assert spy.call_args.kwargs["project_id"] == project.id

    def test_omitting_release_validates_nothing(
        self, client, org, ticket, pipeline, developer_user, db_session
    ):
        with patch("src.routers.tickets.resolve_ticket_release") as spy:
            resp = client.put(
                f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
                json={"summary": "Untouched release"},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        spy.assert_not_called()


class TestUpdateValidatesAgainstTheDestinationProject:
    """A single PUT can move a ticket *and* set its release. Validating against
    the project it arrived on would let it land on project B carrying project A's
    version -- the orphaned state this validation exists to prevent, created by
    the code meant to prevent it."""

    def test_moving_and_setting_the_destinations_version_succeeds(
        self,
        client,
        org,
        ticket,
        pipeline,
        second_project,
        second_project_pipeline,
        developer_user,
        db_session,
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"project_id": second_project.id, "release": "v4.0.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["project_id"] == second_project.id
        assert data["release"] == "v4.0.0"

    def test_moving_while_setting_the_origins_version_is_422(
        self,
        client,
        org,
        ticket,
        project,
        pipeline,
        second_project,
        second_project_pipeline,
        developer_user,
        db_session,
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
            json={"project_id": second_project.id, "release": "v1.11.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

        db_session.expire_all()
        moved = db_session.get(Ticket, ticket.id)
        assert moved.project_id == project.id, "the move was not committed either"
        assert moved.release is None, "nothing was written"

    def test_the_validator_receives_the_destination_project(
        self,
        client,
        org,
        ticket,
        second_project,
        second_project_pipeline,
        developer_user,
        db_session,
    ):
        with patch(
            "src.routers.tickets.resolve_ticket_release", return_value="v4.0.0"
        ) as spy:
            resp = client.put(
                f"/api/v1/organizations/{org.id}/tickets/{ticket.id}",
                json={"project_id": second_project.id, "release": "v4.0.0"},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        assert spy.call_args.kwargs["project_id"] == second_project.id


class TestBoardScopedUpdateRelease:
    """The board-scoped PUT shares `TicketUpdate`, so it must share the rule."""

    @pytest.fixture
    def board(self, db_session, org, project, developer_user):
        from src.domain.board import BoardRegistration

        b = BoardRegistration(
            id=str(uuid4()),
            user_id=developer_user.id,
            organization_id=org.id,
            project_id=project.id,
            board_name="Test Board",
            board_url="https://example.com/board",
            board_type="trello",
            board_external_id="ext-123",
            is_active=True,
        )
        db_session.add(b)
        db_session.commit()
        return b

    @pytest.fixture
    def board_ticket(self, db_session, org, project, board):
        t = Ticket(
            organization_id=org.id,
            project_id=project.id,
            board_registration_id=board.id,
            summary="Board-linked",
            status=TicketStatus.TODO,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)
        return t

    def test_an_outstanding_version_round_trips(
        self, client, org, board, board_ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/boards/{board.id}/tickets/{board_ticket.id}",
            json={"release": "v1.11.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.11.0"

    def test_an_unknown_version_is_422(
        self, client, org, board, board_ticket, pipeline, developer_user, db_session
    ):
        resp = client.put(
            f"/api/v1/organizations/{org.id}/boards/{board.id}/tickets/{board_ticket.id}",
            json={"release": "v9.9.9"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

    def test_the_validator_is_wired_to_this_route(
        self,
        client,
        org,
        board,
        board_ticket,
        project,
        pipeline,
        developer_user,
        db_session,
    ):
        with patch(
            "src.routers.tickets.resolve_ticket_release", return_value="v1.11.0"
        ) as spy:
            resp = client.put(
                f"/api/v1/organizations/{org.id}/boards/{board.id}"
                f"/tickets/{board_ticket.id}",
                json={"release": "v1.11.0"},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        spy.assert_called_once()
        assert spy.call_args.kwargs["project_id"] == project.id
