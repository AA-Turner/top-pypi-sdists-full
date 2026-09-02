"""A rejected GitHub credential must surface as an actionable error, not a 500.

`get_organization_repositories` used to `raise Exception(...)` on any non-200,
which slipped past the onboarding router's `except WorkspaceOnboardError` and
became an opaque 500 — so an expired token looked like an InnoDay bug.

The credential in question is the org's Vault-stored one (#554 removed the
`GITHUB_TOKEN` env fallback), which is why the message names that rather than a
deployment env var.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.github_api import GitHubAPI, GitHubAPIError
from src.services.workspace_onboard import (
    WorkspaceOnboardError,
    WorkspaceOnboardService,
)


def _resp(status_code, text="Bad credentials"):
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    return resp


class TestGitHubAPIError:
    @pytest.mark.parametrize("status", [401, 403])
    def test_auth_statuses_flagged(self, status):
        assert GitHubAPIError("x", status_code=status).is_auth_error

    @pytest.mark.parametrize("status", [404, 422, 500, None])
    def test_non_auth_statuses_not_flagged(self, status):
        assert not GitHubAPIError("x", status_code=status).is_auth_error

    @pytest.mark.asyncio
    async def test_non_200_raises_typed_error_with_status(self):
        api = GitHubAPI(token="t")
        client = MagicMock()
        client.get = AsyncMock(return_value=_resp(401))
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=False)
        with patch("httpx.AsyncClient", return_value=client):
            with pytest.raises(GitHubAPIError) as ei:
                await api.get_organization_repositories("havilandsoftware")
        assert ei.value.status_code == 401
        assert ei.value.is_auth_error
        assert "havilandsoftware" in str(ei.value)


class TestDiscoverReposTranslatesError:
    @pytest.mark.asyncio
    async def test_expired_token_becomes_actionable_onboard_error(self):
        svc = WorkspaceOnboardService(session=MagicMock(), github_token="t")
        with patch.object(
            GitHubAPI,
            "get_organization_repositories",
            new=AsyncMock(side_effect=GitHubAPIError("Bad credentials", 401)),
        ):
            with pytest.raises(WorkspaceOnboardError) as ei:
                await svc.discover_repos(MagicMock(), "havilandsoftware", "pixelfuel")
        msg = str(ei.value)
        # Reworded by #554: the credential is the org's Vault-stored one, not the
        # process-wide GITHUB_TOKEN, so naming that variable sent the reader to
        # the wrong place to fix it. The remedy moved with it (reconnect GitHub
        # for the org, rather than rotate a deployment env var).
        assert "stored GitHub credential" in msg
        assert "401" in msg
        assert "reconnect" in msg.lower()

    @pytest.mark.asyncio
    async def test_non_auth_failure_still_becomes_onboard_error(self):
        svc = WorkspaceOnboardService(session=MagicMock(), github_token="t")
        with patch.object(
            GitHubAPI,
            "get_organization_repositories",
            new=AsyncMock(side_effect=GitHubAPIError("boom", 500)),
        ):
            with pytest.raises(WorkspaceOnboardError):
                await svc.discover_repos(MagicMock(), "havilandsoftware", "pixelfuel")
