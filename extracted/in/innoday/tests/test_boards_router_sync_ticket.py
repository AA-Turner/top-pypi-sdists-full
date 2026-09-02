"""
Tests for the single-ticket sync endpoint:
POST /organizations/{organization_id}/boards/{board_id}/tickets/{external_key}/sync
"""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.adapters import BoardAdapterError
from src.api.app import app
from src.database import get_session
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
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
        alias=f"T{str(uuid4())[:6]}".upper(),
        name="Test Project",
        description="Test project",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def registration(db_session, org, project):
    reg = BoardRegistration(
        id=str(uuid4()),
        user_id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Test Linear Board",
        board_url="https://linear.app/testorg/team/PF",
        board_type=BoardType.LINEAR,
        board_external_id="team-123",
        is_active=True,
    )
    db_session.add(reg)
    db_session.commit()
    db_session.refresh(reg)
    return reg


@pytest.fixture
def inactive_registration(db_session, org, project):
    reg = BoardRegistration(
        id=str(uuid4()),
        user_id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Inactive Board",
        board_url="https://linear.app/testorg/team/OLD",
        board_type=BoardType.LINEAR,
        board_external_id="team-456",
        is_active=False,
    )
    db_session.add(reg)
    db_session.commit()
    db_session.refresh(reg)
    return reg


class TestSyncSingleTicket:
    def test_sync_ticket_creates_new_ticket(
        self, client, org, registration, auth_headers
    ):
        fake_ticket = Ticket(
            id=1,
            summary="New ticket",
            status=TicketStatus.TODO,
            url="https://linear.app/testorg/issue/PF-1",
            external_ticket_id="PF-1",
            organization_id=org.id,
            board_registration_id=registration.id,
            source_platform="linear",
        )

        with patch(
            "src.services.board_sync_service.board_sync_service.sync_single_ticket",
            new=AsyncMock(return_value=(True, fake_ticket)),
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/boards/{registration.id}/tickets/PF-1/sync",
                headers={**auth_headers, "X-Integration-Token": "fake-token"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["was_created"] is True
        assert data["ticket"]["summary"] == "New ticket"

    def test_sync_ticket_updates_existing_ticket(
        self, client, org, registration, auth_headers
    ):
        fake_ticket = Ticket(
            id=2,
            summary="Updated ticket",
            status=TicketStatus.IN_PROGRESS,
            external_ticket_id="PF-2",
            organization_id=org.id,
            board_registration_id=registration.id,
            source_platform="linear",
        )

        with patch(
            "src.services.board_sync_service.board_sync_service.sync_single_ticket",
            new=AsyncMock(return_value=(False, fake_ticket)),
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/boards/{registration.id}/tickets/PF-2/sync",
                headers={**auth_headers, "X-Integration-Token": "fake-token"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["was_created"] is False
        assert data["ticket"]["status"] == "in progress"

    def test_sync_ticket_not_found_on_board_returns_404(
        self, client, org, registration, auth_headers
    ):
        with patch(
            "src.services.board_sync_service.board_sync_service.sync_single_ticket",
            new=AsyncMock(side_effect=BoardAdapterError("Ticket 'PF-999' not found")),
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/boards/{registration.id}/tickets/PF-999/sync",
                headers={**auth_headers, "X-Integration-Token": "fake-token"},
            )

        assert resp.status_code == 404

    def test_sync_ticket_bad_board_returns_404(self, client, org, auth_headers):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/boards/nonexistent-board/tickets/PF-1/sync",
            headers={**auth_headers, "X-Integration-Token": "fake-token"},
        )

        assert resp.status_code == 404

    def test_sync_ticket_inactive_board_returns_400(
        self, client, org, inactive_registration, auth_headers
    ):
        resp = client.post(
            f"/api/v1/organizations/{org.id}/boards/{inactive_registration.id}/tickets/PF-1/sync",
            headers={**auth_headers, "X-Integration-Token": "fake-token"},
        )

        assert resp.status_code == 400


class TestTheCredentialResolvesFromVault:
    """#609: this endpoint declared `X-Integration-Token` as a REQUIRED header.

    A board whose credential is already in Vault -- the normal case, and the
    only case the platform actually supports -- could therefore not be synced
    at all without the caller supplying a credential from somewhere else. The
    CLI's answer was to read `~/.innoday/config.json` and post whatever it
    found there, which is the leak #609 exists to close. Removing that read
    is only safe because the header stopped being required here.

    `get_board_credential_payload` is patched throughout: it calls the
    `get_board_credential` Postgres function, which does not exist on the
    SQLite engine these tests run against.
    """

    def _fake_ticket(self, org, registration):
        return Ticket(
            id=3,
            summary="From Vault",
            status=TicketStatus.TODO,
            external_ticket_id="PF-1",
            organization_id=org.id,
            board_registration_id=registration.id,
            source_platform="linear",
        )

    def test_no_header_resolves_the_boards_own_vault_credential(
        self, client, org, registration, auth_headers
    ):
        sync = AsyncMock(return_value=(True, self._fake_ticket(org, registration)))

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"token": "token-from-vault"},
        ):
            with patch(
                "src.services.board_sync_service.board_sync_service.sync_single_ticket",
                new=sync,
            ):
                resp = client.post(
                    f"/api/v1/organizations/{org.id}/boards/{registration.id}/tickets/PF-1/sync",
                    headers=auth_headers,
                )

        assert resp.status_code == 200, resp.text
        # Not just "it worked" -- the Vault value is what reached the adapter.
        assert sync.await_args.kwargs["token"] == "token-from-vault"

    def test_an_explicit_header_still_overrides_the_stored_credential(
        self, client, org, registration, auth_headers
    ):
        """The header remains a legitimate one-off override; #609 removed the
        CLI's silent auto-population of it, not the header itself."""
        sync = AsyncMock(return_value=(True, self._fake_ticket(org, registration)))

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value={"token": "token-from-vault"},
        ):
            with patch(
                "src.services.board_sync_service.board_sync_service.sync_single_ticket",
                new=sync,
            ):
                resp = client.post(
                    f"/api/v1/organizations/{org.id}/boards/{registration.id}/tickets/PF-1/sync",
                    headers={**auth_headers, "X-Integration-Token": "caller-token"},
                )

        assert resp.status_code == 200, resp.text
        assert sync.await_args.kwargs["token"] == "caller-token"

    def test_no_header_and_no_stored_credential_is_a_400_naming_the_remedy(
        self, client, org, registration, auth_headers
    ):
        """Not a 422. A 422 says "you forgot a header"; the actual problem is
        that this board has no credential anywhere, and the fix is to store
        one -- so the response has to say that."""
        with patch(
            "src.routers.boards.get_board_credential_payload", return_value=None
        ):
            resp = client.post(
                f"/api/v1/organizations/{org.id}/boards/{registration.id}/tickets/PF-1/sync",
                headers=auth_headers,
            )

        assert resp.status_code == 400, resp.text
        assert "No credentials found for this board" in resp.json()["detail"]
