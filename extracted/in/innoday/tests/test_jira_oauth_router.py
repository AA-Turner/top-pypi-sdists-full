"""
Tests for the Jira OAuth 2.0 (3LO) authorize/callback endpoints
(GitHub issue #296).

GET  /organizations/{organization_id}/boards/{board_id}/oauth/jira/authorize
GET  /organizations/{organization_id}/boards/{board_id}/oauth/jira/callback

No real Atlassian OAuth app exists yet -- all Atlassian HTTP calls are
mocked. These endpoints don't attempt a live OAuth flow.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from src.domain.board import BoardRegistration, BoardType

ENV_VARS = {
    "BOARD_OAUTH_CLIENT_ID_JIRA": "test-client-id",
    "BOARD_OAUTH_CLIENT_SECRET_JIRA": "test-client-secret",
    "BOARD_OAUTH_REDIRECT_URI_JIRA": "https://www.inno.day/api/v1/boards/oauth/jira/callback",
}


@pytest.fixture(autouse=True)
def oauth_env(monkeypatch):
    for key, value in ENV_VARS.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def board_registration(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        user_id="user-1",
        board_name="Test Jira Board",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net",
        board_external_id="80",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


@pytest.mark.asyncio
class TestAuthorizeEndpoint:
    async def test_returns_atlassian_authorize_url_with_required_params(
        self, db_session, org, board_registration
    ):
        from src.routers.boards import start_jira_oauth

        current_user = MagicMock()
        current_user.id = "test-user"

        with patch("src.routers.boards.require_org_role"):
            result = await start_jira_oauth(
                organization_id=org.id,
                board_id=board_registration.id,
                session=db_session,
                current_user=current_user,
            )

        url = (
            result["authorize_url"]
            if isinstance(result, dict)
            else result.authorize_url
        )
        assert url.startswith("https://auth.atlassian.com/authorize?")
        assert "client_id=test-client-id" in url
        assert "audience=api.atlassian.com" in url

    async def test_404_for_unknown_board(self, db_session, org):
        from src.routers.boards import start_jira_oauth

        current_user = MagicMock()
        current_user.id = "test-user"

        with pytest.raises(HTTPException) as exc_info:
            await start_jira_oauth(
                organization_id=org.id,
                board_id="does-not-exist",
                session=db_session,
                current_user=current_user,
            )

        assert exc_info.value.status_code == 404

    async def test_rejects_non_jira_board(self, db_session, org, project):
        from src.routers.boards import start_jira_oauth

        trello_board = BoardRegistration(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            user_id="user-1",
            board_name="Trello Board",
            board_type=BoardType.TRELLO,
            board_url="https://trello.com/b/abc123",
            board_external_id="abc123",
        )
        db_session.add(trello_board)
        db_session.commit()
        db_session.refresh(trello_board)

        current_user = MagicMock()
        current_user.id = "test-user"

        with patch("src.routers.boards.require_org_role"):
            with pytest.raises(HTTPException) as exc_info:
                await start_jira_oauth(
                    organization_id=org.id,
                    board_id=trello_board.id,
                    session=db_session,
                    current_user=current_user,
                )

        assert exc_info.value.status_code == 400


@pytest.mark.asyncio
class TestCallbackEndpoint:
    """
    The callback route is now the FIXED path registered with Atlassian
    (/api/v1/boards/oauth/jira/callback) -- no organization_id/board_id
    path params. jira_oauth_callback recovers both IDs from the signed
    `state` param instead, so these tests call it with only code/state.
    """

    async def test_exchanges_code_resolves_cloud_id_and_persists_credential(
        self, db_session, org, board_registration
    ):
        # `generate_state` belongs to the service; the router only ever
        # re-exported it by accident of an unused import.
        from src.routers.boards import jira_oauth_callback
        from src.services.jira_oauth_service import generate_state

        state = generate_state(org.id, board_registration.id)

        with (
            patch("src.routers.boards.require_org_role"),
            patch(
                "src.routers.boards.exchange_code_for_tokens",
                new=AsyncMock(
                    return_value={
                        "access_token": "access-abc",
                        "refresh_token": "refresh-xyz",
                        "expires_in": 3600,
                    }
                ),
            ),
            patch(
                "src.routers.boards.resolve_cloud_id",
                new=AsyncMock(
                    return_value=("cloud-123", "https://example.atlassian.net")
                ),
            ),
            patch("src.routers.boards.set_board_credential") as mock_set_cred,
        ):
            result = await jira_oauth_callback(
                code="auth-code-123",
                state=state,
                session=db_session,
            )

        assert result.board_id == board_registration.id
        assert result.cloud_id == "cloud-123"
        assert result.site_url == "https://example.atlassian.net"

        mock_set_cred.assert_called_once()
        call_args = mock_set_cred.call_args
        payload = call_args.kwargs.get("payload") or call_args.args[-1]
        assert payload["auth_type"] == "oauth2"
        assert payload["access_token"] == "access-abc"
        assert payload["refresh_token"] == "refresh-xyz"
        assert payload["cloud_id"] == "cloud-123"
        assert payload["site_url"] == "https://example.atlassian.net"
        assert "expires_at" in payload

    async def test_rejects_mismatched_state_as_csrf(
        self, db_session, org, board_registration
    ):
        from src.routers.boards import jira_oauth_callback

        with (
            patch("src.routers.boards.require_org_role"),
            patch("src.routers.boards.set_board_credential") as mock_set_cred,
        ):
            with pytest.raises(HTTPException) as exc_info:
                await jira_oauth_callback(
                    code="auth-code-123",
                    state="totally-bogus-state",
                    session=db_session,
                )

        assert exc_info.value.status_code == 400
        mock_set_cred.assert_not_called()

    async def test_404_for_unknown_board(self, db_session, org):
        """State is well-formed and signed (for a real org) but the
        board_id inside it doesn't correspond to a real board -- discovered
        only after state parsing succeeds, since board lookup now happens
        after IDs are recovered from state rather than from the URL."""
        # `generate_state` belongs to the service; the router only ever
        # re-exported it by accident of an unused import.
        from src.routers.boards import jira_oauth_callback
        from src.services.jira_oauth_service import generate_state

        state = generate_state(org.id, "does-not-exist")

        with pytest.raises(HTTPException) as exc_info:
            await jira_oauth_callback(
                code="auth-code-123",
                state=state,
                session=db_session,
            )

        assert exc_info.value.status_code == 404

    async def test_404_when_state_organization_id_does_not_match_any_org(
        self, db_session, board_registration
    ):
        """State is well-formed and signed, board_id is real, but the
        organization_id embedded in state doesn't match the board's actual
        organization -- the lookup is scoped by BOTH IDs from state, so
        this must still 404 rather than leaking the board across orgs."""
        # `generate_state` belongs to the service; the router only ever
        # re-exported it by accident of an unused import.
        from src.routers.boards import jira_oauth_callback
        from src.services.jira_oauth_service import generate_state

        state = generate_state("some-other-org-id", board_registration.id)

        with pytest.raises(HTTPException) as exc_info:
            await jira_oauth_callback(
                code="auth-code-123",
                state=state,
                session=db_session,
            )

        assert exc_info.value.status_code == 404


@pytest.mark.asyncio
class TestValidateBoardAccessOAuthMode:
    """
    validate_board_access's Jira branch has always assumed `token` is a
    Basic Auth "email:api_token" string. For a stored OAuth credential
    (not a raw incoming header value), it needs an OAuth-aware path: call
    /rest/api/3/myself through the OAuth base URL
    (https://api.atlassian.com/ex/jira/{cloud_id}) with a Bearer token
    instead of splitting on ":" and using Basic Auth.
    """

    async def test_validates_oauth_credential_via_bearer_and_cloud_id_url(self):
        from src.routers.boards import validate_board_access

        mock_response = MagicMock(status_code=200)

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await validate_board_access(
                "80",
                BoardType.JIRA,
                "access-abc",
                board_url="https://example.atlassian.net",
                auth_type="oauth2",
                cloud_id="cloud-123",
            )

        assert result is True
        call_args = mock_get.call_args
        called_url = call_args.args[0]
        assert (
            called_url
            == "https://api.atlassian.com/ex/jira/cloud-123/rest/api/3/myself"
        )
        assert call_args.kwargs["headers"]["Authorization"] == "Bearer access-abc"

    async def test_oauth_mode_returns_false_on_non_200(self):
        from src.routers.boards import validate_board_access

        mock_response = MagicMock(status_code=401)

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await validate_board_access(
                "80",
                BoardType.JIRA,
                "access-abc",
                board_url="https://example.atlassian.net",
                auth_type="oauth2",
                cloud_id="cloud-123",
            )

        assert result is False

    async def test_basic_auth_path_unaffected_by_oauth_param_default(self):
        """Default auth_type ('basic') must keep the existing email:token
        split behavior exactly as before -- zero regression."""
        from src.routers.boards import validate_board_access

        mock_response = MagicMock(status_code=200)

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await validate_board_access(
                "80",
                BoardType.JIRA,
                "me@example.com:tok123",
                board_url="https://example.atlassian.net",
            )

        assert result is True
        call_args = mock_get.call_args
        assert call_args.kwargs["auth"] == ("me@example.com", "tok123")
