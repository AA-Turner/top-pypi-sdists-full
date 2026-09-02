"""
Tests for ticket creation endpoints:
POST /api/v1/organizations/{organization_id}/tickets
POST /api/v1/organizations/{organization_id}/boards/{board_id}/tickets

Two bugs fixed together here:
1. The board-scoped create_ticket endpoint called can_create_ticket(session,
   organization_id) — wrong argument order/count against the real signature
   can_create_ticket(organization_id, user_id, session) — causing a 500
   TypeError on every real request.
2. No non-board-scoped POST existed at all, so the MCP `create_ticket` tool
   (which posts to this URL shape) always 404'd, same class of gap as the
   update route fixed in PR #227.

Tests mock `can_create_ticket` to isolate these endpoint-level bugs from the
separate licensing subsystem it calls into.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.api.app import app
from src.database import get_session
from src.domain.board import BoardRegistration
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket
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
        id=str(uuid4()),
        organization_id=org.id,
        name="Test Project",
        alias="TEST",
        description="A project for tests",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def board(db_session, org, developer_user, project):
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
    db_session.refresh(b)
    return b


@pytest.fixture(autouse=True)
def allow_ticket_creation():
    """Isolate these endpoint tests from the licensing subsystem."""
    with patch("src.routers.tickets.can_create_ticket", return_value=True):
        yield


class TestCreateTicketByIdSuccess:
    def test_create_minimal_ticket(
        self, client, org, project, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={"summary": "A new ticket", "project_id": project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"] == "A new ticket"
        assert data["status"] == "backlog"
        assert data["project_id"] == project.id

    def test_create_draft_status_ticket(
        self, client, org, project, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={"summary": "Draft idea", "status": "draft", "project_id": project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "draft"

    def test_create_ticket_with_project_id(
        self, client, org, project, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={"summary": "Project-scoped ticket", "project_id": project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["project_id"] == project.id

    def test_create_ticket_with_all_fields(
        self, client, org, project, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Full ticket",
                "description": "Some description",
                "assignee": "alice",
                "status": "todo",
                "project_id": project.id,
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["description"] == "Some description"
        assert data["assignee"] == "alice"
        assert data["status"] == "todo"

    def test_no_board_id_required_in_path(
        self, client, org, project, developer_user, db_session
    ):
        """Regression test: this route must not require a board_id segment."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={"summary": "No board needed", "project_id": project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert "boards" not in str(resp.request.url)


class TestCreateTicketByIdBoardPush:
    """
    A ticket created via the org-scoped endpoint should be pushed straight to
    the project's active external board (no separate sync needed). Best-effort:
    a board failure must fall back to an InnoDay-only create, not 500.
    """

    def test_pushes_to_board_when_project_has_active_board(
        self, client, db_session, org, project, board, developer_user
    ):
        from src.services.board_ticket_creation_service import TicketCreateResponse

        seen = {}

        async def fake_push(
            self, board_registration_id, ticket_data, user_id, token=None
        ):
            # Capture what the endpoint forwarded so we can assert the
            # requested status is threaded through to the board.
            seen["status"] = ticket_data.status
            # Mirror what the real service does: persist a board-linked row,
            # then return its response. Uses the fixture session, which shares
            # the engine the endpoint reads from. id is an auto-increment int,
            # so let the DB assign it rather than passing one in.
            row = Ticket(
                summary=ticket_data.summary,
                organization_id=org.id,
                project_id=project.id,
                board_registration_id=board_registration_id,
                external_ticket_id="PF-999",
                url="https://linear.app/x/issue/PF-999",
                source_platform="linear",
            )
            db_session.add(row)
            db_session.commit()
            db_session.refresh(row)
            return TicketCreateResponse(
                id=row.id,
                external_id="PF-999",
                external_url=row.url,
                summary=row.summary,
                description=row.description,
                status="todo",
                board_id=board_registration_id,
                board_name="Test Board",
                created_at=row.created_at,
                created_by=user_id,
            )

        with patch(
            "src.services.board_ticket_creation_service."
            "BoardTicketCreationService.create_ticket_on_board",
            new=fake_push,
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={
                    "summary": "Pushed ticket",
                    "status": "in progress",
                    "project_id": project.id,
                },
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["external_ticket_id"] == "PF-999"
        assert data["board_registration_id"] == board.id
        assert data["source_platform"] == "linear"
        # Requested status is forwarded to the board push (finding #3 fix).
        assert seen["status"] == "in progress"

    def test_board_push_failure_falls_back_to_innoday_only(
        self, client, org, project, board, developer_user, db_session
    ):
        async def boom(self, board_registration_id, ticket_data, user_id, token=None):
            raise RuntimeError("board unreachable")

        with patch(
            "src.services.board_ticket_creation_service."
            "BoardTicketCreationService.create_ticket_on_board",
            new=boom,
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={"summary": "Falls back", "project_id": project.id},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        data = resp.json()
        # Fell back to the InnoDay-only row: no external linkage.
        assert data["summary"] == "Falls back"
        assert data.get("external_ticket_id") is None
        assert data.get("board_registration_id") is None

    def test_no_board_still_creates_innoday_only(
        self, client, org, project, developer_user, db_session
    ):
        """Project without a board: unchanged InnoDay-only behaviour."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={"summary": "No board", "project_id": project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["board_registration_id"] is None

    def test_push_to_board_false_skips_board_even_when_one_exists(
        self, client, org, project, board, developer_user, db_session
    ):
        """push_to_board=false (used by bulk/parse flows) must NOT touch the
        board, even for a project that has an active one -- otherwise a bulk
        parse fires one synchronous external call per ticket."""
        called = {"n": 0}

        async def spy(self, board_registration_id, ticket_data, user_id, token=None):
            called["n"] += 1
            raise AssertionError("board push must not be attempted")

        with patch(
            "src.services.board_ticket_creation_service."
            "BoardTicketCreationService.create_ticket_on_board",
            new=spy,
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={
                    "summary": "Bulk item",
                    "project_id": project.id,
                    "push_to_board": False,
                },
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        assert called["n"] == 0
        assert resp.json()["board_registration_id"] is None


class TestCreateTicketByIdErrors:
    def test_wrong_org_project_id_returns_404(
        self, client, org, other_org, db_session, developer_user
    ):
        other_project = Project(
            id=str(uuid4()),
            organization_id=other_org.id,
            name="Other Project",
            alias="OTHER",
            description="Belongs to a different org",
        )
        db_session.add(other_project)
        db_session.commit()

        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={"summary": "Should fail", "project_id": other_project.id},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 404

    def test_insufficient_role_returns_403(self, client, org, member_user, db_session):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={"summary": "Should be forbidden"},
            headers=bearer_for(db_session, member_user.id),
        )
        assert resp.status_code == 403


class TestCreateTicketBoardScopedArgumentOrderRegression:
    """
    Regression test for the can_create_ticket(session, organization_id) bug —
    wrong argument order/count caused a 500 TypeError on every real request
    to the board-scoped create_ticket endpoint.

    NOTE: this endpoint moved from
    POST /{organization_id}/boards/{board_id}/tickets to
    POST /{organization_id}/boards/{board_id}/tickets/local-only (see
    src/routers/tickets.py) because the old shared path collided with
    src/routers/boards.py's create_board_ticket -- the endpoint that
    actually writes to the external board -- and FastAPI silently dispatched
    every request to this InnoDay-only handler instead, since tickets.router
    is registered before boards.router. Confirmed live: create_board_ticket
    never actually reached Linear/Jira until the paths were split.
    """

    def test_board_scoped_create_succeeds(
        self, client, org, board, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/boards/{board.id}/tickets/local-only",
            json={"summary": "Board ticket"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"] == "Board ticket"
        assert data["board_registration_id"] == board.id


class TestLicenseLimitExceededRegression:
    """
    Regression test for a second bug found alongside the argument-order one:
    both create_ticket endpoints raised LicenseLimitExceededError(tier_name=...,
    requested=...) — keyword arguments the real constructor
    (resource, limit, current) doesn't accept — so a license-exceeded org got
    a 500 TypeError instead of a clean error response.
    """

    def test_license_limit_returns_clean_error_not_500(
        self, client, org, project, developer_user, db_session
    ):
        with patch("src.routers.tickets.can_create_ticket", return_value=False):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={
                    "summary": "Should be blocked by license",
                    "project_id": project.id,
                },
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 402

    def test_board_scoped_license_limit_returns_clean_error_not_500(
        self, client, org, board, developer_user, db_session
    ):
        with patch("src.routers.tickets.can_create_ticket", return_value=False):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/boards/{board.id}/tickets/local-only",
                json={"summary": "Should be blocked by license"},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 402


# ---------------------------------------------------------------------------
# `release` on create -- validated against the project's outstanding releases
# ---------------------------------------------------------------------------


@pytest.fixture
def pipeline(db_session, org, project):
    """The two-slot pipeline a real project carries, plus closed history.

    `v1.10.0` is being cut, `v1.11.0` is being filled, `v1.9.0` has shipped and
    `v1.8.0` was archived -- so "outstanding" is a genuine subset rather than
    "every row".
    """
    rows = {}
    for version, status in (
        ("v1.10.0", ReleaseStatus.IN_PROGRESS),
        ("v1.11.0", ReleaseStatus.PLANNED),
        ("v1.9.0", ReleaseStatus.RELEASED),
        ("v1.8.0", ReleaseStatus.ARCHIVED),
    ):
        row = Release(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            version=version,
            status=status,
        )
        db_session.add(row)
        rows[version] = row
    db_session.commit()
    return rows


class TestCreateTicketByIdRelease:
    def test_an_outstanding_version_round_trips(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Fix the closer",
                "project_id": project.id,
                "release": "v1.11.0",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.11.0"

    def test_the_in_progress_version_is_outstanding_too(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Cutting now",
                "project_id": project.id,
                "release": "v1.10.0",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.10.0"

    def test_an_unknown_version_is_422_listing_the_real_options(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        """The negative control. A validator that is never wired up cannot make
        this pass -- the endpoint would answer 200."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Typo'd version",
                "project_id": project.id,
                "release": "v9.9.9",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        # A plain string, not a dict: the CLI f-strings `detail` and the MCP
        # server hands the raw body to an agent to read.
        assert isinstance(detail, str), detail
        assert "v9.9.9" in detail
        assert "v1.10.0" in detail and "v1.11.0" in detail

    def test_nothing_is_created_when_the_version_is_rejected(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Must not exist",
                "project_id": project.id,
                "release": "v9.9.9",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert (
            db_session.exec(
                select(Ticket).where(Ticket.summary == "Must not exist")
            ).first()
            is None
        )

    def test_current_resolves_to_the_version_being_cut(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        """Same sentinel and same helper as the `?release=current` filter, so the
        two cannot disagree about which version that is."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Into the current release",
                "project_id": project.id,
                "release": "current",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.10.0"

    def test_current_is_422_when_the_project_has_nothing_current(
        self, client, org, project, developer_user, db_session
    ):
        """422 rather than 404: it is a body field that cannot be satisfied, not a
        missing resource."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "No pipeline",
                "project_id": project.id,
                "release": "current",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

    def test_a_released_version_is_rejected_and_says_so(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Into the past",
                "project_id": project.id,
                "release": "v1.9.0",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        # Distinguishable from "unknown" -- the version exists, its status is the
        # problem, and a message that says "unknown" sends the user to create a
        # duplicate release row.
        assert "released" in detail
        assert "v1.9.0" in detail

    def test_an_archived_version_is_rejected(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Into the archive",
                "project_id": project.id,
                "release": "v1.8.0",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422
        assert "archived" in resp.json()["detail"]

    def test_matching_is_case_sensitive(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        """`V1.10.0` is not `v1.10.0`, and must not be silently corrected into it.

        `_bulk_close_tickets_for_release` matches `Ticket.release == version` with
        no normalisation, so admitting the wrong case would create exactly the
        orphaned ticket this validation exists to prevent.
        """
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Wrong case",
                "project_id": project.id,
                "release": "V1.10.0",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

    def test_surrounding_whitespace_is_stripped_not_rejected(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        """The one normalisation allowed, and the stored value is the release
        row's own string -- which is what the closer matches on."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/tickets",
            json={
                "summary": "Padded",
                "project_id": project.id,
                "release": "  v1.11.0  ",
            },
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.11.0"

    def test_omitting_release_leaves_it_unset_and_validates_nothing(
        self, client, org, project, developer_user, db_session
    ):
        """A project with no releases at all must still be able to take a ticket."""
        with patch("src.routers.tickets.resolve_ticket_release") as spy:
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={"summary": "No release", "project_id": project.id},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        assert resp.json()["release"] is None
        spy.assert_not_called()

    def test_the_validator_is_wired_to_this_route_with_the_bodys_project(
        self, client, org, project, pipeline, developer_user, db_session
    ):
        with patch(
            "src.routers.tickets.resolve_ticket_release", return_value="v1.11.0"
        ) as spy:
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={
                    "summary": "Wiring",
                    "project_id": project.id,
                    "release": "v1.11.0",
                },
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        spy.assert_called_once()
        assert spy.call_args.kwargs["project_id"] == project.id
        assert spy.call_args.kwargs["organization_id"] == org.id
        assert spy.call_args.kwargs["value"] == "v1.11.0"

    def test_the_board_push_path_does_not_drop_the_release(
        self, client, db_session, org, project, board, pipeline, developer_user
    ):
        """`BoardTicketCreationService.TicketCreateRequest` has no `release`
        field, so the row the push returns carries none -- a create that looked
        like it worked and silently did not. `push_to_board` is the *default*,
        so this is the common path.
        """
        from src.services.board_ticket_creation_service import TicketCreateResponse

        async def fake_push(
            self, board_registration_id, ticket_data, user_id, token=None
        ):
            row = Ticket(
                summary=ticket_data.summary,
                organization_id=org.id,
                project_id=project.id,
                board_registration_id=board_registration_id,
                external_ticket_id="PF-999",
                url="https://linear.app/x/issue/PF-999",
                source_platform="linear",
            )
            db_session.add(row)
            db_session.commit()
            db_session.refresh(row)
            return TicketCreateResponse(
                id=row.id,
                external_id="PF-999",
                external_url=row.url,
                summary=row.summary,
                description=row.description,
                status="todo",
                board_id=board_registration_id,
                board_name="Test Board",
                created_at=row.created_at,
                created_by=user_id,
            )

        with patch(
            "src.services.board_ticket_creation_service."
            "BoardTicketCreationService.create_ticket_on_board",
            new=fake_push,
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={
                    "summary": "Pushed with a release",
                    "project_id": project.id,
                    "release": "v1.11.0",
                },
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["external_ticket_id"] == "PF-999", "took the board-push path"
        assert data["release"] == "v1.11.0"

        # And it is persisted, not merely echoed.
        saved = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "PF-999")
        ).first()
        db_session.refresh(saved)
        assert saved.release == "v1.11.0"

    def test_a_bad_version_is_rejected_before_the_board_is_touched(
        self, client, db_session, org, project, board, pipeline, developer_user
    ):
        async def spy(self, board_registration_id, ticket_data, user_id, token=None):
            raise AssertionError("board must not be reached for an invalid release")

        with patch(
            "src.services.board_ticket_creation_service."
            "BoardTicketCreationService.create_ticket_on_board",
            new=spy,
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/tickets",
                json={
                    "summary": "Never pushed",
                    "project_id": project.id,
                    "release": "v9.9.9",
                },
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 422


class TestBoardScopedCreateRelease:
    """The board-scoped local-only create takes its project from the board, so
    that is the project its version must be validated against."""

    def test_an_outstanding_version_round_trips(
        self, client, org, board, pipeline, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/boards/{board.id}/tickets/local-only",
            json={"summary": "Board ticket", "release": "v1.11.0"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["release"] == "v1.11.0"

    def test_an_unknown_version_is_422(
        self, client, org, board, pipeline, developer_user, db_session
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/boards/{board.id}/tickets/local-only",
            json={"summary": "Board ticket", "release": "v9.9.9"},
            headers=bearer_for(db_session, developer_user.id),
        )
        assert resp.status_code == 422

    def test_the_validator_is_wired_with_the_boards_project(
        self, client, org, board, project, pipeline, developer_user, db_session
    ):
        with patch(
            "src.routers.tickets.resolve_ticket_release", return_value="v1.11.0"
        ) as spy:
            resp = client.post(
                f"/api/v1/organizations/{org.id}/boards/{board.id}/tickets/local-only",
                json={"summary": "Wiring", "release": "v1.11.0"},
                headers=bearer_for(db_session, developer_user.id),
            )
        assert resp.status_code == 200
        spy.assert_called_once()
        assert spy.call_args.kwargs["project_id"] == project.id
