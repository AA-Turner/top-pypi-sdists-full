"""Regression tests for project scoping and archived-project visibility (#495).

Two failures that shared a shape -- the CLI showed organization-wide data
while looking project-scoped, and showed archived projects while claiming to
have deleted them:

  * `innoday --project <id> tickets list` accepted the flag and ignored it,
    returning every ticket in the organization. A pre-archive safety check
    read 781 org tickets as if they belonged to one project.
  * `innoday projects list` showed archived projects with no indication, so
    `projects delete` (which archives) looked like it had done nothing.
"""

import argparse
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.client import InnoDayAPIClient
from src.cli.commands.projects import ProjectCommands


def _response(status_code, json_body=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body if json_body is not None else {}
    resp.content = b"{}"
    return resp


def _client_config(project_id):
    config = MagicMock()
    config.get_current_organization.return_value = "acme"
    config._config = {"organizations": {"acme": {"id": "org-1"}}}
    config.get_current_project_id.return_value = project_id
    config.get_user_id.return_value = "user-1"
    config.get_cli_token.return_value = "token"
    config.get_team_secret.return_value = None
    config.get_api_timeout.return_value = 30
    config.get_api_url.return_value = "https://api.test"
    return config


class TestTicketsListScoping:
    async def _urls_for(self, project_id, **kwargs):
        """Return the URL list_tickets actually requested."""
        client = InnoDayAPIClient(_client_config(project_id))
        client.api_client = MagicMock()
        client.api_client.get = AsyncMock(return_value=_response(200, []))

        await client.list_tickets(**kwargs)
        return client.api_client.get.call_args[0][0]

    @pytest.mark.asyncio
    async def test_project_in_context_scopes_the_request(self):
        url = await self._urls_for("proj-1")

        # The project-scoped route already existed; the CLI just never used it.
        assert "/projects/proj-1/tickets" in url

    @pytest.mark.asyncio
    async def test_all_projects_flag_restores_org_wide_listing(self):
        url = await self._urls_for("proj-1", all_projects=True)

        assert "/projects/" not in url
        assert url.endswith("/organizations/org-1/tickets")

    @pytest.mark.asyncio
    async def test_no_project_context_lists_the_organization(self):
        url = await self._urls_for(None)

        assert url.endswith("/organizations/org-1/tickets")


class TestProjectsListHidesArchived:
    def _config(self):
        config = MagicMock()
        config.get_current_organization.return_value = "acme"
        config.get_organization_id.return_value = "org-1"
        return config

    def _args(self, **overrides):
        defaults = dict(
            project_command="list",
            status=None,
            priority=None,
            tags=None,
            all=False,
            format="table",
            no_color=True,
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    PROJECTS = [
        {"alias": "LIVE", "name": "Live One", "status": "active", "priority": "medium"},
        {
            "alias": "GONE",
            "name": "Archived One",
            "status": "archived",
            "priority": "medium",
        },
    ]

    def _patched_client(self):
        api_client = MagicMock()
        api_client.get = AsyncMock(return_value=_response(200, self.PROJECTS))
        api_client.close = AsyncMock()
        return api_client

    @pytest.mark.asyncio
    async def test_archived_hidden_by_default(self, capsys):
        with patch(
            "src.cli.commands.projects.InnoDayAPIClient",
            return_value=self._patched_client(),
        ):
            result = await ProjectCommands._handle_list(self._args(), self._config())

        assert result == 0
        out = capsys.readouterr().out
        assert "LIVE" in out
        assert "GONE" not in out
        # Hiding silently would be its own trap -- say the count.
        assert "1 archived project" in out

    @pytest.mark.asyncio
    async def test_all_flag_includes_archived(self, capsys):
        with patch(
            "src.cli.commands.projects.InnoDayAPIClient",
            return_value=self._patched_client(),
        ):
            result = await ProjectCommands._handle_list(
                self._args(all=True), self._config()
            )

        assert result == 0
        out = capsys.readouterr().out
        assert "LIVE" in out
        assert "GONE" in out

    @pytest.mark.asyncio
    async def test_explicit_status_filter_is_not_second_guessed(self, capsys):
        """`--status archived` must not be filtered back out."""
        with patch(
            "src.cli.commands.projects.InnoDayAPIClient",
            return_value=self._patched_client(),
        ):
            result = await ProjectCommands._handle_list(
                self._args(status="archived"), self._config()
            )

        assert result == 0
        assert "GONE" in capsys.readouterr().out


class TestArchiveImpactPreview:
    """The confirm prompt reads the overview envelope -- the same shape that
    crashed `projects show --overview` by being mistaken for a flat object.
    Anything consuming it needs a test that pins the nesting."""

    OVERVIEW = {
        "project": {"alias": "S4C", "name": "Soccer for Charities"},
        "repositories": {"total": 2, "by_layer": {}, "primary": None},
        "board": {
            "name": "S4C Board",
            "type": "linear",
            "tickets": {"total": 12, "open": 5, "in_progress": 2, "completed": 5},
        },
    }

    def _api_client(self, response):
        api_client = MagicMock()
        api_client.get = AsyncMock(return_value=response)
        return api_client

    @pytest.mark.asyncio
    async def test_preview_reports_attached_work(self, capsys):
        await ProjectCommands._print_archive_impact(
            self._api_client(_response(200, self.OVERVIEW)), "org-1", "S4C"
        )

        out = capsys.readouterr().out
        assert "Soccer for Charities" in out
        assert "2" in out  # repositories
        assert "S4C Board" in out
        assert "12" in out  # total tickets
        # The whole point is reassurance that archiving destroys nothing.
        assert "Nothing is deleted" in out

    @pytest.mark.asyncio
    async def test_preview_handles_a_project_with_no_board(self, capsys):
        bare = dict(self.OVERVIEW, board=None)

        await ProjectCommands._print_archive_impact(
            self._api_client(_response(200, bare)), "org-1", "S4C"
        )

        assert "none attached" in capsys.readouterr().out

    @pytest.mark.asyncio
    async def test_preview_failure_never_blocks_the_archive(self, capsys):
        """Decoration must not become a gate -- a 500 is silently skipped."""
        api_client = MagicMock()
        api_client.get = AsyncMock(side_effect=RuntimeError("network down"))

        await ProjectCommands._print_archive_impact(api_client, "org-1", "S4C")

        assert capsys.readouterr().out == ""


class TestReposListScoping:
    """`repos list` follows the project too -- the project-scoped route
    already existed at /organizations/{org}/projects/{id}/repositories."""

    def _repo_commands(self, project_id):
        from src.cli.commands.repositories import RepositoryCommands

        client = MagicMock()
        client.validate_organization_id.return_value = True
        client.organization_id = "org-1"
        client.project_id = project_id
        client.get = AsyncMock(
            return_value=_response(200, [{"id": 1, "name": "s4c-app"}])
        )
        return RepositoryCommands(MagicMock()), client

    @pytest.mark.asyncio
    async def test_scopes_to_the_project_in_context(self):
        commands, client = self._repo_commands("proj-1")

        with patch(
            "src.cli.commands.repositories.InnoDayAPIClient", return_value=client
        ):
            await commands.list_repositories(argparse.Namespace(all_projects=False))

        assert "/projects/proj-1/repositories" in client.get.call_args[0][0]

    @pytest.mark.asyncio
    async def test_all_projects_restores_the_org_wide_list(self):
        commands, client = self._repo_commands("proj-1")

        with patch(
            "src.cli.commands.repositories.InnoDayAPIClient", return_value=client
        ):
            await commands.list_repositories(argparse.Namespace(all_projects=True))

        assert client.get.call_args[0][0] == "repositories"


class TestBoardListScoping:
    """`board list` filters client-side: the project board route is POST-only,
    and BoardRegistrationResponse already carries project_id."""

    BOARDS = [
        {
            "id": "b1",
            "project_id": "proj-1",
            "board_name": "Mine",
            "board_type": "linear",
            "is_active": True,
        },
        {
            "id": "b2",
            "project_id": "proj-2",
            "board_name": "Theirs",
            "board_type": "jira",
            "is_active": True,
        },
    ]

    def _client(self, project_id):
        client = MagicMock()
        client.project_id = project_id
        client.get = AsyncMock(return_value=_response(200, self.BOARDS))
        return client

    def _config(self):
        config = MagicMock()
        config.get_current_organization.return_value = "acme"
        config.get_organization_id.return_value = "org-1"
        return config

    def _args(self, **overrides):
        defaults = dict(
            active_only=False, all_projects=False, format="table", no_color=True
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    @pytest.mark.asyncio
    async def test_shows_only_this_projects_board(self, capsys):
        from src.cli.commands.boards import BoardCommands

        result = await BoardCommands._handle_list(
            self._args(), self._client("proj-1"), self._config()
        )

        assert result == 0
        out = capsys.readouterr().out
        assert "Mine" in out
        assert "Theirs" not in out

    @pytest.mark.asyncio
    async def test_all_projects_shows_every_board(self, capsys):
        from src.cli.commands.boards import BoardCommands

        result = await BoardCommands._handle_list(
            self._args(all_projects=True), self._client("proj-1"), self._config()
        )

        assert result == 0
        out = capsys.readouterr().out
        assert "Mine" in out
        assert "Theirs" in out

    @pytest.mark.asyncio
    async def test_project_without_a_board_says_so(self, capsys):
        from src.cli.commands.boards import BoardCommands

        result = await BoardCommands._handle_list(
            self._args(), self._client("proj-unattached"), self._config()
        )

        assert result == 0
        out = capsys.readouterr().out
        assert "No board registered for this project" in out
        assert "--all-projects" in out
