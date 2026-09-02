"""
Regression tests for CLI<->API contract fixes (GitHub #336).

These target the CLI command handlers' own request/output logic -- they mock
InnoDayAPIClient rather than hitting a real API. Focus:

  * `orgs current --format json` must emit machine-readable JSON (item 1).
  * `projects update` must issue PUT, not POST -- the router only accepts PUT
    at that path (item 2).
"""

import argparse
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.commands.organizations import OrganizationCommands
from src.cli.commands.projects import ProjectCommands


def _response(status_code, json_body=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body if json_body is not None else {}
    return resp


class TestOrgsCurrentJson:
    """Item 1: `orgs current --format json` never emitted JSON before."""

    def _config(self):
        config = MagicMock()
        config.get_current_organization.return_value = "acme"
        config.get_organization_details.return_value = {
            "name": "Acme Corp",
            "id": "org-1",
        }
        return config

    def _args(self, **overrides):
        defaults = dict(
            org_command="current",
            format="table",
            no_color=True,
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    @pytest.mark.asyncio
    async def test_current_json_emits_parseable_json(self, capsys):
        config = self._config()
        result = await OrganizationCommands._handle_current(
            self._args(format="json"), config
        )

        assert result == 0
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["alias"] == "acme"
        assert parsed["name"] == "Acme Corp"
        assert parsed["id"] == "org-1"

    @pytest.mark.asyncio
    async def test_current_json_no_org_emits_empty_object(self, capsys):
        config = self._config()
        config.get_current_organization.return_value = None

        result = await OrganizationCommands._handle_current(
            self._args(format="json"), config
        )

        assert result == 0
        assert json.loads(capsys.readouterr().out) == {}

    @pytest.mark.asyncio
    async def test_current_table_still_prints_text(self, capsys):
        config = self._config()
        result = await OrganizationCommands._handle_current(
            self._args(format="table"), config
        )

        assert result == 0
        out = capsys.readouterr().out
        # Plain-text path -- not valid JSON, but human-readable fields present.
        assert "Acme Corp" in out
        assert "acme" in out


class TestProjectsUpdateUsesPut:
    """Item 2: `projects update` must PUT (router exposes only PUT here)."""

    def _config(self):
        config = MagicMock()
        config.get_current_organization.return_value = "acme"
        config.get_organization_id.return_value = "org-1"
        config.get_current_project_id.return_value = "proj-1"
        return config

    def _args(self, **overrides):
        defaults = dict(
            project_command="update",
            project_id="proj-1",
            org_id=None,
            name="New Name",
            description=None,
            goals=None,
            scope_limitations=None,
            priority=None,
            status=None,
            tags=None,
            format="table",
            no_color=True,
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    @pytest.mark.asyncio
    async def test_update_issues_put_not_post(self):
        config = self._config()
        with patch("src.cli.commands.projects.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.put = AsyncMock(return_value=_response(200, {"name": "New Name"}))
            client.post = AsyncMock()
            client.close = AsyncMock()

            result = await ProjectCommands._handle_update(self._args(), config)

        assert result == 0
        client.put.assert_called_once()
        client.post.assert_not_called()
        endpoint, kwargs = client.put.call_args
        assert endpoint[0] == "/organizations/org-1/projects/proj-1"
        assert kwargs["json"]["name"] == "New Name"


class TestApiUrlPrefixNotDoubled:
    """`_build_api_url` prepends `api/v1/` by string concatenation, so a caller
    passing a full path (`/api/v1/onboarding/resolve` — the convention used by
    workspace.py and the MCP server) produced `/api/v1/api/v1/...` and 404'd.
    A leading slash does NOT make it absolute here, because the prefix is
    joined before urljoin sees it."""

    def _client(self, org_id=None):
        from src.cli.client import InnoDayAPIClient

        config = MagicMock()
        config.get_api_url.return_value = "https://api.example.com"
        config.get_current_organization.return_value = None
        config.get_current_project_id.return_value = None
        config.get_user_id.return_value = "u1"
        config.get_cli_token.return_value = None
        config.get_team_secret.return_value = None
        config.get_api_timeout.return_value = 30.0
        client = InnoDayAPIClient(config)
        client.organization_id = org_id
        return client

    @pytest.mark.parametrize(
        "endpoint",
        [
            "/api/v1/onboarding/resolve",
            "api/v1/onboarding/resolve",
            "onboarding/resolve",
        ],
    )
    def test_full_and_bare_paths_resolve_identically(self, endpoint):
        url = self._client()._build_api_url(endpoint)
        assert url == "https://api.example.com/api/v1/onboarding/resolve"
        assert "api/v1/api/v1" not in url

    def test_org_scoping_still_applies_to_bare_tickets(self):
        url = self._client(org_id="ORG1")._build_api_url("tickets")
        assert url == "https://api.example.com/api/v1/organizations/ORG1/tickets"

    def test_org_scoped_full_path_is_not_double_scoped(self):
        url = self._client(org_id="ORG1")._build_api_url(
            "/api/v1/organizations/ORG1/releases"
        )
        assert url == "https://api.example.com/api/v1/organizations/ORG1/releases"
