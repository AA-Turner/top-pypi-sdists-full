"""
Tests for `innoday sync`'s project-scoped cascade (board tickets, repos,
release status report). Mocks InnoDayAPIClient.get/post directly -- these
tests are about SyncCommands' own orchestration logic, not the routers
(which have their own test coverage).
"""

import argparse
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.cli.commands.sync import SyncCommands


def _config(project_id="proj-1"):
    """A config that raises if the cascade asks it for a board credential.

    The board leg of the cascade must reach no local credential store (#609);
    the server resolves the board's own credential from Vault. Making the
    attempt itself the failure is what keeps this honest -- returning None
    would pass whether or not the lookup happened.
    """
    config = MagicMock()
    config.get_current_organization.return_value = "acme"
    config.get_organization_id.return_value = "org-1"
    config.get_current_project_id.return_value = project_id
    config.get_organization_integration.side_effect = AssertionError(
        "the sync cascade read a board credential from local config"
    )
    config.get_credential.side_effect = AssertionError(
        "the sync cascade read a credential from the keyring"
    )
    return config


def _response(status_code, json_body=None, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body if json_body is not None else {}
    resp.text = text
    return resp


class TestCascadeGating:
    @pytest.mark.asyncio
    async def test_cascade_fails_without_org(self):
        config = _config()
        config.get_current_organization.return_value = None
        config.get_organization_id.return_value = None  # no org -> no id either

        result = await SyncCommands._handle_cascade(argparse.Namespace(), None, config)
        assert result == 1

    @pytest.mark.asyncio
    async def test_cascade_fails_without_project(self):
        config = _config(project_id=None)
        client = MagicMock()

        result = await SyncCommands._handle_cascade(
            argparse.Namespace(), client, config
        )
        assert result == 1


class TestSyncBoard:
    @pytest.mark.asyncio
    async def test_no_board_registered_skips_cleanly(self):
        client = MagicMock()
        client.get = AsyncMock(return_value=_response(200, []))
        config = _config()

        result = await SyncCommands._sync_board(client, "org-1", "proj-1", config)

        assert result == 0

    @pytest.mark.asyncio
    async def test_triggers_sync_with_no_locally_sourced_credential(self):
        """A board with no local credential syncs -- that used to be skipped.

        Before #609 this leg looked the board type up in
        ~/.innoday/config.json and returned early with "No jira credentials
        found" when it saw nothing, so the cascade quietly did not sync a
        board whose credential was sitting in Vault the whole time.
        """
        client = MagicMock()
        client.get = AsyncMock(
            return_value=_response(
                200, [{"id": "board-1", "board_type": "jira", "board_name": "Board"}]
            )
        )
        client.post = AsyncMock(
            return_value=_response(200, {"sync_id": "sync-1", "status": "PENDING"})
        )
        config = _config()

        result = await SyncCommands._sync_board(client, "org-1", "proj-1", config)

        assert result == 0
        client.post.assert_called_once()
        endpoint = client.post.call_args[0][0]
        assert endpoint == "/organizations/org-1/boards/board-1/sync"
        headers = client.post.call_args.kwargs.get("headers") or {}
        assert "X-Integration-Token" not in headers

    @pytest.mark.asyncio
    async def test_board_lookup_failure_returns_error(self):
        client = MagicMock()
        client.get = AsyncMock(return_value=_response(500))
        config = _config()

        result = await SyncCommands._sync_board(client, "org-1", "proj-1", config)

        assert result == 1


class TestSyncRepos:
    @pytest.mark.asyncio
    async def test_reports_synced_repos(self):
        client = MagicMock()
        client.post = AsyncMock(
            return_value=_response(
                200,
                {
                    "repositories_synced": 2,
                    "github_label": "my-project",
                    "new_repositories": [{"name": "repo-a", "layer": "api", "url": ""}],
                    "deactivated_repositories": 0,
                },
            )
        )

        result = await SyncCommands._sync_repos(client, "org-1", "proj-1")

        assert result == 0
        endpoint = client.post.call_args[0][0]
        assert endpoint == "/organizations/org-1/projects/proj-1/repositories/discover"

    @pytest.mark.asyncio
    async def test_failure_returns_error(self):
        client = MagicMock()
        client.post = AsyncMock(return_value=_response(400, text="bad request"))

        result = await SyncCommands._sync_repos(client, "org-1", "proj-1")

        assert result == 1


class TestReportReleases:
    @pytest.mark.asyncio
    async def test_reports_no_releases(self):
        client = MagicMock()
        client.get = AsyncMock(return_value=_response(200, []))

        # Should not raise
        await SyncCommands._report_releases(client, "org-1", "proj-1")

        params = client.get.call_args.kwargs["params"]
        assert params == {"project_id": "proj-1"}

    @pytest.mark.asyncio
    async def test_reports_existing_releases(self):
        client = MagicMock()
        client.get = AsyncMock(
            return_value=_response(
                200, [{"version": "v1.0.0", "status": "released", "released_at": None}]
            )
        )

        await SyncCommands._report_releases(client, "org-1", "proj-1")
