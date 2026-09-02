"""`scope generate` resolves the target board's credential from Vault (#609).

This endpoint declared ``X-Integration-Token`` as a **required** header, so a
board whose credential already lived in Vault could not be used at all unless
the caller supplied a credential from somewhere else. The CLI's answer was to
read ``~/.innoday/config.json`` and post whatever it found; removing that read
is only safe because the header stopped being required here.

It now shares ``resolve_board_sync_credential`` with both board-sync endpoints,
so all three resolve a credential the same way -- caller's header if given,
otherwise the board's own stored credential, otherwise a 400 naming the remedy.
That helper also enforces two things this route previously did not check at all:
the board must belong to the calling organization, and it must be active (which
this endpoint's own docstring already promised).

``get_board_credential_payload`` is patched throughout: it calls the
``get_board_credential`` Postgres function, which does not exist on the SQLite
engine these tests run against.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.database import get_session
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.scope_document import ScopeDocument, ScopeStatus
from src.domain.user import User, UserRole
from src.services.ticket_generation_service import (
    GenerationStatus,
    TicketGenerationResponse,
)
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_engine():
    return build_test_engine()


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
        email="scope@example.com",
        full_name="Scope User",
        role=UserRole.MEMBER,
        is_platform_member=True,
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
        alias=f"S{str(uuid4())[:6]}".upper(),
        name="Scope Project",
        description="Scope project",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def scope(db_session, project):
    s = ScopeDocument(
        id=str(uuid4()),
        project_id=project.id,
        version=1,
        status=ScopeStatus.FINAL,
        refined_scope="Build the thing",
        created_by="user",
    )
    db_session.add(s)
    db_session.commit()
    db_session.refresh(s)
    return s


def _registration(db_session, org, project, is_active=True):
    reg = BoardRegistration(
        id=str(uuid4()),
        user_id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Scope Board",
        board_url="https://linear.app/testorg/team/SC",
        board_type=BoardType.LINEAR,
        board_external_id="team-sc",
        is_active=is_active,
    )
    db_session.add(reg)
    db_session.commit()
    db_session.refresh(reg)
    return reg


@pytest.fixture
def registration(db_session, org, project):
    return _registration(db_session, org, project)


def _generation_response():
    return TicketGenerationResponse(
        generation_id=str(uuid4()),
        status=GenerationStatus.COMPLETED,
        tickets_generated=1,
        epics_created=0,
        stories_created=1,
        tasks_created=0,
        board_url="https://linear.app/testorg/team/SC",
    )


def _patched_service(generate):
    """Patch the service class the router constructs, keeping the awaited
    `generate_tickets_from_scope` mock reachable for assertions."""
    service = MagicMock()
    service.generate_tickets_from_scope = generate
    return patch("src.routers.scopes.TicketGenerationService", return_value=service)


def _post(client, org, project, scope, registration, auth_headers, token=None):
    headers = dict(auth_headers)
    if token is not None:
        headers["X-Integration-Token"] = token
    return client.post(
        f"/api/v1/organizations/{org.id}/projects/{project.id}"
        f"/scope/{scope.id}/generate",
        json={"board_id": registration.id},
        headers=headers,
    )


class TestScopeGenerateCredentialResolution:
    def test_no_header_resolves_the_boards_own_vault_credential(
        self, client, org, project, scope, registration, auth_headers
    ):
        generate = AsyncMock(return_value=_generation_response())

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"token": "token-from-vault"},
        ):
            with _patched_service(generate):
                resp = _post(client, org, project, scope, registration, auth_headers)

        assert resp.status_code == 200, resp.text
        # Not just "it worked" -- the Vault value is what reached the service.
        assert generate.await_args.kwargs["token"] == "token-from-vault"

    def test_an_explicit_header_still_overrides_the_stored_credential(
        self, client, org, project, scope, registration, auth_headers
    ):
        generate = AsyncMock(return_value=_generation_response())

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"token": "token-from-vault"},
        ):
            with _patched_service(generate):
                resp = _post(
                    client,
                    org,
                    project,
                    scope,
                    registration,
                    auth_headers,
                    token="caller-token",
                )

        assert resp.status_code == 200, resp.text
        assert generate.await_args.kwargs["token"] == "caller-token"

    def test_no_header_and_no_stored_credential_is_a_400_naming_the_remedy(
        self, client, org, project, scope, registration, auth_headers
    ):
        generate = AsyncMock(return_value=_generation_response())

        with patch(
            "src.routers.boards.get_board_credential_payload", return_value=None
        ):
            with _patched_service(generate):
                resp = _post(client, org, project, scope, registration, auth_headers)

        assert resp.status_code == 400, resp.text
        assert "No credentials found for this board" in resp.json()["detail"]
        generate.assert_not_awaited()

    def test_an_inactive_board_is_refused_before_any_generation_happens(
        self, client, db_session, org, project, scope, auth_headers
    ):
        """The check this route did not have. Its docstring promised "Board
        must be registered and active"; nothing enforced it here."""
        inactive = _registration(db_session, org, project, is_active=False)
        generate = AsyncMock(return_value=_generation_response())

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"token": "token-from-vault"},
        ):
            with _patched_service(generate):
                resp = _post(client, org, project, scope, inactive, auth_headers)

        assert resp.status_code == 400, resp.text
        assert "not active" in resp.json()["detail"]
        generate.assert_not_awaited()

    def test_a_board_in_another_organization_is_not_reachable(
        self, client, db_session, org, project, scope, auth_headers
    ):
        """Tenancy: `board_id` arrives in the request body, so without an
        org-scoped lookup one org could name another's board."""
        other_org = Organization(id=str(uuid4()), name="Other Org")
        db_session.add(other_org)
        db_session.commit()
        other_project = Project(
            id=str(uuid4()),
            organization_id=other_org.id,
            alias=f"O{str(uuid4())[:6]}".upper(),
            name="Other Project",
            description="Other",
        )
        db_session.add(other_project)
        db_session.commit()
        foreign = _registration(db_session, other_org, other_project)
        generate = AsyncMock(return_value=_generation_response())

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"token": "token-from-vault"},
        ):
            with _patched_service(generate):
                resp = _post(client, org, project, scope, foreign, auth_headers)

        assert resp.status_code == 404, resp.text
        generate.assert_not_awaited()
