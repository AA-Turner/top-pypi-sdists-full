"""BoardSyncService._get_adapter previously always reconstructed Basic Auth
from an "email:api_token" colon-joined token, even for a Jira board whose
stored credential is OAuth 2.0 (auth_type == "oauth2") -- payload_to_legacy_token
would KeyError before this even got called, or (for the X-Integration-Token
override path) a bogus Basic Auth tuple would get built from garbage data.

The fix: payload_to_legacy_token returns OAUTH_TOKEN_SENTINEL for an OAuth
payload; _get_adapter recognizes that sentinel and resolves a real
(access_token, cloud_id) pair via ensure_fresh_jira_token instead, building
an OAuth-mode JiraAPI (self.auth is None) so the resulting JiraBoardAdapter's
own per-call refresh (_jira_request_context) takes over from there."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.domain.board import BoardType
from src.services.board_credential_service import OAUTH_TOKEN_SENTINEL
from src.services.board_sync_service import BoardSyncService


def _make_jira_registration(board_id="board-1"):
    registration = Mock()
    registration.id = board_id
    registration.board_type = BoardType.JIRA
    registration.board_url = (
        "https://example.atlassian.net/jira/software/c/projects/X/boards/1"
    )
    registration.organization = None
    return registration


@pytest.mark.asyncio
class TestGetAdapterOAuthJira:
    async def test_sentinel_token_resolves_oauth_credentials(self):
        service = BoardSyncService()
        registration = _make_jira_registration()
        session = Mock()

        with patch(
            # The OAuth resolution moved into the shared board-adapter factory,
            # so the patch target moves with it (mock at import location).
            "src.services.board_adapter_factory.ensure_fresh_jira_token",
            new=AsyncMock(return_value=("fresh-access-token", "cloud-abc")),
        ) as mock_refresh:
            adapter = await service._get_adapter(
                registration, OAUTH_TOKEN_SENTINEL, session
            )

        mock_refresh.assert_awaited_once_with(session, registration.id)
        # OAuth-mode JiraAPI has auth=None -- this is exactly what
        # JiraBoardAdapter._is_oauth_mode() checks to keep refreshing on
        # every subsequent call.
        assert adapter.api.auth is None
        assert adapter.api.base_url == "https://api.atlassian.com/ex/jira/cloud-abc"

    async def test_non_sentinel_token_still_builds_basic_auth(self):
        """Existing Basic Auth boards must be completely unaffected."""
        service = BoardSyncService()
        registration = _make_jira_registration()
        session = Mock()

        adapter = await service._get_adapter(
            registration, "dev@example.com:secret-token", session
        )

        assert adapter.api.auth == ("dev@example.com", "secret-token")

    async def test_oauth_adapters_are_never_cached(self):
        """OAuth-mode adapters must NOT be cached at all -- not just keyed
        differently from Basic Auth ones (that's already covered by
        test_board_sync_service_adapter_cache.py's TestGetAdapterCache).
        Caching one would mean every OAuth call on a board shares the same
        JiraBoardAdapter/JiraAPI object; _refresh_api_auth_if_oauth mutates
        that object's base_url/headers in place with no lock, and this
        service is a module-level singleton, so a cached instance would be
        racy under concurrent syncs. Two calls with the identical sentinel
        token must therefore return two DIFFERENT adapter instances."""
        service = BoardSyncService()
        registration = _make_jira_registration()
        session = Mock()

        with patch(
            # The OAuth resolution moved into the shared board-adapter factory,
            # so the patch target moves with it (mock at import location).
            "src.services.board_adapter_factory.ensure_fresh_jira_token",
            new=AsyncMock(return_value=("fresh-access-token", "cloud-abc")),
        ):
            first = await service._get_adapter(
                registration, OAUTH_TOKEN_SENTINEL, session
            )
            second = await service._get_adapter(
                registration, OAUTH_TOKEN_SENTINEL, session
            )

        assert first is not second
        assert service.adapters == {}
