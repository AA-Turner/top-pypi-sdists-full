"""
Tests for src.services.jira_oauth_service -- the Jira OAuth 2.0 (3LO) token
refresh helper and authorize/callback support functions.

Context (GitHub issue #296): Atlassian's edge rejects Basic Auth
(email:api_token) from Railway's shared egress IPs with a 401 demanding
OAuth. This module implements the durable fix -- OAuth 2.0 (3LO) -- as a
dual-mode addition alongside the existing Basic Auth path (see
src.services.board_credential_service, which keeps auth_type-less/"basic"
payloads working unmodified).

No real Atlassian OAuth app exists yet (requires human registration at
developer.atlassian.com) -- all Atlassian HTTP calls here are mocked.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.services.jira_oauth_service import (
    JiraOAuthError,
    build_authorize_url,
    ensure_fresh_jira_token,
    exchange_code_for_tokens,
    generate_state,
    parse_and_verify_state,
    resolve_cloud_id,
    verify_state,
)

ENV_VARS = {
    "BOARD_OAUTH_CLIENT_ID_JIRA": "test-client-id",
    "BOARD_OAUTH_CLIENT_SECRET_JIRA": "test-client-secret",
    "BOARD_OAUTH_REDIRECT_URI_JIRA": "https://www.inno.day/api/v1/organizations/org-1/boards/board-1/oauth/jira/callback",
}


@pytest.fixture(autouse=True)
def oauth_env(monkeypatch):
    for key, value in ENV_VARS.items():
        monkeypatch.setenv(key, value)


class TestGenerateAndVerifyState:
    def test_generate_state_is_tied_to_org_and_board_id(self):
        state = generate_state("org-1", "board-1")
        assert verify_state(state, "org-1", "board-1") is True

    def test_verify_state_rejects_wrong_board_id(self):
        state = generate_state("org-1", "board-1")
        assert verify_state(state, "org-1", "board-2") is False

    def test_verify_state_rejects_wrong_organization_id(self):
        state = generate_state("org-1", "board-1")
        assert verify_state(state, "org-2", "board-1") is False

    def test_verify_state_rejects_tampered_state(self):
        state = generate_state("org-1", "board-1")
        tampered = state[:-1] + ("a" if state[-1] != "a" else "b")
        assert verify_state(tampered, "org-1", "board-1") is False

    def test_verify_state_rejects_garbage_input(self):
        assert verify_state("not-a-valid-state-at-all", "org-1", "board-1") is False
        assert verify_state("", "org-1", "board-1") is False


class TestParseAndVerifyState:
    def test_round_trips_organization_id_and_board_id(self):
        state = generate_state("org-1", "board-1")
        assert parse_and_verify_state(state) == ("org-1", "board-1")

    def test_returns_none_for_tampered_state(self):
        state = generate_state("org-1", "board-1")
        tampered = state[:-1] + ("a" if state[-1] != "a" else "b")
        assert parse_and_verify_state(tampered) is None

    def test_returns_none_for_garbage_input(self):
        assert parse_and_verify_state("not-a-valid-state-at-all") is None
        assert parse_and_verify_state("") is None

    def test_real_uuid_ids_round_trip(self):
        """Mirrors production shape -- both IDs are UUIDs (no ':' char),
        so ':' is a safe delimiter for the state payload."""
        import uuid

        org_id = str(uuid.uuid4())
        board_id = str(uuid.uuid4())
        state = generate_state(org_id, board_id)
        assert parse_and_verify_state(state) == (org_id, board_id)
        assert verify_state(state, org_id, board_id) is True


class TestBuildAuthorizeUrl:
    def test_returns_atlassian_authorize_url_with_required_params(self):
        url, state = build_authorize_url(organization_id="org-1", board_id="board-1")

        assert url.startswith("https://auth.atlassian.com/authorize?")
        assert "audience=api.atlassian.com" in url
        assert "client_id=test-client-id" in url
        assert "response_type=code" in url
        assert "prompt=consent" in url
        assert f"state={state}" in url
        assert verify_state(state, "org-1", "board-1")
        # redirect_uri must be URL-encoded (not passed through raw)
        assert "redirect_uri=https%3A%2F%2F" in url
        # offline_access is required for Atlassian to issue a refresh token
        assert "offline_access" in url

    def test_authorize_url_requests_project_scope(self):
        """Regression: board endpoints (GET .../board/{id}/configuration,
        and even the baseline .../myself) 401 with "Unauthorized; scope
        does not match" unless read:project:jira is requested alongside
        read:board-scope:jira-software -- confirmed live 2026-07-15 with a
        freshly-consented token that otherwise had every other requested
        scope correctly granted. This is not documented up front by
        Atlassian; only reproducible by hitting the API directly."""
        url, _state = build_authorize_url(organization_id="org-1", board_id="board-1")
        # scope value is url-encoded with '+' for spaces (urlencode default)
        assert "read%3Aproject%3Ajira" in url

    def test_authorize_url_requests_board_scope(self):
        url, _state = build_authorize_url(organization_id="org-1", board_id="board-1")
        assert "read%3Aboard-scope%3Ajira-software" in url

    def test_authorize_url_requests_issue_meta_scope(self):
        url, _state = build_authorize_url(organization_id="org-1", board_id="board-1")
        assert "read%3Aissue-meta%3Ajira" in url
        assert "write%3Aboard-scope%3Ajira-software" in url


class TestExchangeCodeForTokens:
    @pytest.mark.asyncio
    async def test_posts_authorization_code_grant_and_returns_tokens(self):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            "access_token": "access-abc",
            "refresh_token": "refresh-xyz",
            "expires_in": 3600,
        }

        with patch.object(
            httpx.AsyncClient, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_post.return_value = mock_response

            result = await exchange_code_for_tokens("auth-code-123")

            assert result["access_token"] == "access-abc"
            assert result["refresh_token"] == "refresh-xyz"
            sent = mock_post.call_args.kwargs["json"]
            assert sent["grant_type"] == "authorization_code"
            assert sent["code"] == "auth-code-123"
            assert sent["client_id"] == "test-client-id"
            assert sent["client_secret"] == "test-client-secret"
            assert (
                mock_post.call_args.args[0] == "https://auth.atlassian.com/oauth/token"
            )

    @pytest.mark.asyncio
    async def test_raises_clear_error_on_failed_exchange(self):
        mock_response = MagicMock(status_code=400, text="invalid_grant")

        with patch.object(
            httpx.AsyncClient, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(JiraOAuthError):
                await exchange_code_for_tokens("bad-code")


class TestResolveCloudId:
    @pytest.mark.asyncio
    async def test_matches_accessible_resource_by_board_url(self):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = [
            {
                "id": "cloud-999",
                "url": "https://other.atlassian.net",
                "scopes": [],
            },
            {
                "id": "cloud-123",
                "url": "https://example.atlassian.net",
                "scopes": [],
            },
        ]

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            cloud_id, site_url = await resolve_cloud_id(
                access_token="access-abc",
                board_url="https://example.atlassian.net/jira/software/projects/ITPT",
            )

            assert cloud_id == "cloud-123"
            assert site_url == "https://example.atlassian.net"
            call_kwargs = mock_get.call_args.kwargs
            assert call_kwargs["headers"]["Authorization"] == "Bearer access-abc"

    @pytest.mark.asyncio
    async def test_raises_when_no_resource_matches_board_url(self):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = [
            {"id": "cloud-999", "url": "https://other.atlassian.net", "scopes": []}
        ]

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(JiraOAuthError):
                await resolve_cloud_id(
                    access_token="access-abc",
                    board_url="https://example.atlassian.net/jira/software/projects/ITPT",
                )


class TestEnsureFreshJiraToken:
    @pytest.mark.asyncio
    async def test_returns_existing_token_unchanged_when_not_expired(self):
        session = MagicMock()
        future_expiry = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        stored_payload = {
            "auth_type": "oauth2",
            "access_token": "still-good",
            "refresh_token": "refresh-xyz",
            "expires_at": future_expiry,
            "cloud_id": "cloud-123",
            "site_url": "https://example.atlassian.net",
        }

        with (
            patch(
                "src.services.jira_oauth_service.get_board_credential_payload",
                return_value=stored_payload,
            ),
            patch(
                "src.services.jira_oauth_service.set_board_credential"
            ) as mock_set_cred,
            patch.object(
                httpx.AsyncClient, "post", new_callable=AsyncMock
            ) as mock_post,
        ):
            access_token, cloud_id = await ensure_fresh_jira_token(session, "board-1")

        assert access_token == "still-good"
        assert cloud_id == "cloud-123"
        mock_post.assert_not_called()
        mock_set_cred.assert_not_called()

    @pytest.mark.asyncio
    async def test_refreshes_and_persists_new_token_when_expired(self):
        session = MagicMock()
        past_expiry = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        stored_payload = {
            "auth_type": "oauth2",
            "access_token": "stale-token",
            "refresh_token": "old-refresh",
            "expires_at": past_expiry,
            "cloud_id": "cloud-123",
            "site_url": "https://example.atlassian.net",
        }

        refresh_response = MagicMock(status_code=200)
        refresh_response.json.return_value = {
            "access_token": "new-access",
            "refresh_token": "new-refresh",
            "expires_in": 3600,
        }

        with (
            patch(
                "src.services.jira_oauth_service.get_board_credential_payload",
                return_value=stored_payload,
            ),
            patch(
                "src.services.jira_oauth_service.set_board_credential"
            ) as mock_set_cred,
            patch.object(
                httpx.AsyncClient, "post", new_callable=AsyncMock
            ) as mock_post,
        ):
            mock_post.return_value = refresh_response

            access_token, cloud_id = await ensure_fresh_jira_token(session, "board-1")

        assert access_token == "new-access"
        assert cloud_id == "cloud-123"

        sent = mock_post.call_args.kwargs["json"]
        assert sent["grant_type"] == "refresh_token"
        assert sent["refresh_token"] == "old-refresh"

        # Atlassian rotates refresh tokens on every use -- the NEW refresh
        # token must be the one persisted, not the old one silently kept.
        mock_set_cred.assert_called_once()
        persisted_payload = (
            mock_set_cred.call_args.kwargs.get("payload")
            or mock_set_cred.call_args.args[-1]
        )
        assert persisted_payload["access_token"] == "new-access"
        assert persisted_payload["refresh_token"] == "new-refresh"
        assert persisted_payload["auth_type"] == "oauth2"
        assert persisted_payload["cloud_id"] == "cloud-123"

    @pytest.mark.asyncio
    async def test_refreshes_when_within_safety_margin_of_expiry(self):
        """Refresh proactively when <5 min remain, not just when already
        expired -- avoids a request racing against expiry mid-flight."""
        session = MagicMock()
        near_expiry = (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat()
        stored_payload = {
            "auth_type": "oauth2",
            "access_token": "soon-to-expire",
            "refresh_token": "old-refresh",
            "expires_at": near_expiry,
            "cloud_id": "cloud-123",
            "site_url": "https://example.atlassian.net",
        }

        refresh_response = MagicMock(status_code=200)
        refresh_response.json.return_value = {
            "access_token": "new-access",
            "refresh_token": "new-refresh",
            "expires_in": 3600,
        }

        with (
            patch(
                "src.services.jira_oauth_service.get_board_credential_payload",
                return_value=stored_payload,
            ),
            patch("src.services.jira_oauth_service.set_board_credential"),
            patch.object(
                httpx.AsyncClient, "post", new_callable=AsyncMock
            ) as mock_post,
        ):
            mock_post.return_value = refresh_response
            access_token, _ = await ensure_fresh_jira_token(session, "board-1")

        assert access_token == "new-access"
        mock_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_clear_error_when_refresh_endpoint_fails(self):
        """Must not silently return a stale/invalid token if the refresh
        call itself fails."""
        session = MagicMock()
        past_expiry = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        stored_payload = {
            "auth_type": "oauth2",
            "access_token": "stale-token",
            "refresh_token": "old-refresh",
            "expires_at": past_expiry,
            "cloud_id": "cloud-123",
            "site_url": "https://example.atlassian.net",
        }

        failed_response = MagicMock(status_code=400, text="invalid_grant")

        with (
            patch(
                "src.services.jira_oauth_service.get_board_credential_payload",
                return_value=stored_payload,
            ),
            patch(
                "src.services.jira_oauth_service.set_board_credential"
            ) as mock_set_cred,
            patch.object(
                httpx.AsyncClient, "post", new_callable=AsyncMock
            ) as mock_post,
        ):
            mock_post.return_value = failed_response

            with pytest.raises(JiraOAuthError):
                await ensure_fresh_jira_token(session, "board-1")

        # Must not persist anything on failure.
        mock_set_cred.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_when_no_oauth_credential_stored(self):
        session = MagicMock()
        with patch(
            "src.services.jira_oauth_service.get_board_credential_payload",
            return_value=None,
        ):
            with pytest.raises(JiraOAuthError):
                await ensure_fresh_jira_token(session, "board-1")

    @pytest.mark.asyncio
    async def test_raises_when_stored_credential_is_basic_auth_not_oauth(self):
        session = MagicMock()
        with patch(
            "src.services.jira_oauth_service.get_board_credential_payload",
            return_value={"email": "a@b.com", "api_token": "tok"},
        ):
            with pytest.raises(JiraOAuthError):
                await ensure_fresh_jira_token(session, "board-1")


class TestParseExpiresAt:
    """An unreadable stored expiry must mean "refresh", never "raise".

    This was `datetime.fromisoformat(payload["expires_at"])` — an unguarded
    parse plus a bare index. A credential row written by an older version,
    hand-edited, or truncated raised `ValueError`/`KeyError` from inside token
    refresh, so a bad *field* surfaced as a board sync dying rather than as a
    token needing renewal.
    """

    def test_an_aware_value_keeps_its_instant(self):
        from datetime import datetime, timezone

        from src.services.jira_oauth_service import _parse_expires_at

        assert _parse_expires_at("2026-08-10T12:00:00+00:00") == datetime(
            2026, 8, 10, 12, 0, tzinfo=timezone.utc
        )

    def test_a_naive_value_is_read_as_utc(self):
        """The writer stores UTC; a value with no offset is not local time."""
        from datetime import datetime, timezone

        from src.services.jira_oauth_service import _parse_expires_at

        parsed = _parse_expires_at("2026-08-10T12:00:00")
        assert parsed == datetime(2026, 8, 10, 12, 0, tzinfo=timezone.utc)
        assert parsed.tzinfo is not None

    def test_an_offset_is_honoured_not_dropped(self):
        from datetime import datetime, timezone

        from src.services.jira_oauth_service import _parse_expires_at

        parsed = _parse_expires_at("2026-08-10T14:00:00+02:00")
        assert parsed.astimezone(timezone.utc) == datetime(
            2026, 8, 10, 12, 0, tzinfo=timezone.utc
        )

    @pytest.mark.parametrize("value", [None, "", "garbage", "2026-13-45T99:00:00"])
    def test_unusable_values_are_none_rather_than_an_exception(self, value):
        from src.services.jira_oauth_service import _parse_expires_at

        assert _parse_expires_at(value) is None

    def test_none_is_the_signal_the_caller_reads_as_expired(self):
        """Pinning the contract, since the safety of the whole change rests on it.

        Assuming a missing expiry means "still valid" would send a probably-dead
        token to Atlassian and turn one bad field into an unexplainable 401.
        Treating it as expired costs one refresh — the operation that fixes it.
        """
        import inspect

        from src.services import jira_oauth_service

        source = inspect.getsource(jira_oauth_service.ensure_fresh_jira_token)
        assert "if expires_at is not None else -1" in source, (
            "ensure_fresh_jira_token no longer treats an unreadable expiry as expired"
        )
        assert 'payload.get("expires_at")' in source, (
            "expires_at is being indexed again; a missing key is a KeyError"
        )
