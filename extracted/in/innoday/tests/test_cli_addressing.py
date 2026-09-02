"""Two ways to address a command, and only two.

1. From the workspace — the cwd's `.innoday/project.yml` (`--dir` moves where
   that search starts; a variant, not a third mode).
2. Explicitly — `--org <alias|id> --project <alias|id>`, on a machine with
   nothing cloned.

Both were broken. `--project` was *silently discarded* on six modules — parsed,
then overwritten with `None`, because argparse copies a subparser's fresh
namespace over the parent's. And explicit addressing could not work at all,
because the org alias was resolved from a local map that `innoday login` never
populates.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.main import create_parser
from src.cli.utils.context import (
    ContextError,
    looks_like_uuid,
    resolve_context,
)

ORG_UUID = "2e2ffce7-ebd3-42d6-bdb7-9fd94f6759c4"
PROJ_UUID = "e52b7372-3537-49f5-91e9-6db52a2794e3"

#: Every subcommand that previously re-declared a global dest, plus a few that
#: never did — the point is that they now behave identically.
SUBCOMMANDS = [
    ["projects", "show"],
    ["projects", "update", "--name", "x"],
    ["projects", "delete"],
    ["scope", "show"],
    ["releases", "list"],
    ["git", "sync"],
    ["board", "register", "u", "n", "--type", "linear"],
    ["release"],
    ["hotfix"],
    ["summary"],
    ["timeline"],
    ["tickets", "list"],
    ["repos", "list"],
    ["sync"],
]


class TestGlobalFlagsReachEverySubcommand:
    """The regression that would have caught the clobbering."""

    @pytest.mark.parametrize("argv", SUBCOMMANDS, ids=lambda a: " ".join(a))
    def test_org_and_project_survive(self, argv):
        ns = create_parser().parse_args(["--org", "hs", "--project", "PF"] + argv)
        assert ns.organization == "hs"
        assert ns.project_id == "PF"

    def test_a_local_flag_still_overrides_the_global(self):
        """SUPPRESS removes the default, not the flag."""
        ns = create_parser().parse_args(
            ["--org", "hs", "projects", "show", "--project-id", "OTHER"]
        )
        assert ns.project_id == "OTHER"

    def test_the_old_spellings_still_parse(self):
        ns = create_parser().parse_args(
            ["--organization", "hs", "--project-id", "PF", "projects", "show"]
        )
        assert (ns.organization, ns.project_id) == ("hs", "PF")


class TestFlagsThatMeantTwoThings:
    def test_release_takes_github_org_not_org(self):
        """`--org` is the InnoDay org globally and was the GitHub org here —
        the same string meaning two different things in one CLI."""
        ns = create_parser().parse_args(
            ["--org", "hs", "release", "--github-org", "havilandsoftware"]
        )
        assert ns.organization == "hs"
        assert ns.github_org == "havilandsoftware"

    def test_platform_init_no_longer_forces_localhost(self):
        """It defaulted to http://localhost:8000, overriding the global --api-url
        — so `--api-url https://www.inno.day platform init` posted to localhost."""
        ns = create_parser().parse_args(
            ["--api-url", "https://www.inno.day", "platform", "init"]
        )
        assert getattr(ns, "api_url", None) == "https://www.inno.day"

    def test_projects_delete_accepts_the_cwd(self):
        """It required --project-id even inside a workspace — the one command
        that refused the cwd was the one you're most likely standing in."""
        ns = create_parser().parse_args(
            ["--org", "hs", "--project", "PF", "projects", "delete"]
        )
        assert ns.project_id == "PF"


class TestUuidDetection:
    def test_a_uuid_needs_no_lookup(self):
        assert looks_like_uuid(ORG_UUID)

    def test_an_alias_does(self):
        assert not looks_like_uuid("PF")
        assert not looks_like_uuid("bp")

    def test_empty_is_not_a_uuid(self):
        assert not looks_like_uuid("")


def _config(org=None, project=None, cached=None):
    c = MagicMock()
    c.get_current_organization.return_value = org
    c.get_current_project_id.return_value = project
    c.get_organization_id.return_value = cached
    c._config = {}
    return c


def _client(orgs=None, projects=None):
    c = MagicMock()

    async def get(endpoint, params=None):
        body = orgs if endpoint == "/organizations" else projects
        return SimpleNamespace(status_code=200, json=lambda: body or [])

    c.get = AsyncMock(side_effect=get)
    return c


class TestResolveContext:
    @pytest.mark.asyncio
    async def test_alias_resolves_over_the_api(self):
        """The case that could not work before: no cached org, no workspace."""
        ctx = await resolve_context(
            _config(org="bp", project="BPAI"),
            _client(
                orgs=[{"id": ORG_UUID, "alias": "bp"}],
                projects=[{"id": PROJ_UUID, "alias": "BPAI"}],
            ),
        )
        assert ctx.org_id == ORG_UUID
        assert ctx.project_id == PROJ_UUID

    @pytest.mark.asyncio
    async def test_a_uuid_is_passed_straight_through(self):
        client = _client()
        ctx = await resolve_context(_config(org=ORG_UUID, project=PROJ_UUID), client)
        assert (ctx.org_id, ctx.project_id) == (ORG_UUID, PROJ_UUID)
        client.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_a_cached_org_costs_no_call(self):
        client = _client(projects=[{"id": PROJ_UUID, "alias": "PF"}])
        await resolve_context(_config(org="hs", project="PF", cached=ORG_UUID), client)
        assert all(
            call.args[0] != "/organizations" for call in client.get.call_args_list
        )

    @pytest.mark.asyncio
    async def test_matching_is_case_insensitive(self):
        ctx = await resolve_context(
            _config(org="BP", project="bpai"),
            _client(
                orgs=[{"id": ORG_UUID, "alias": "bp"}],
                projects=[{"id": PROJ_UUID, "alias": "BPAI"}],
            ),
        )
        assert ctx.org_id == ORG_UUID and ctx.project_id == PROJ_UUID

    @pytest.mark.asyncio
    async def test_no_org_names_both_routes(self):
        """The error has to mention the flags — most messages named only the cwd."""
        with pytest.raises(ContextError) as e:
            await resolve_context(_config(), _client())
        assert "--org" in e.value.hint and "project.yml" in e.value.hint

    @pytest.mark.asyncio
    async def test_an_unknown_org_says_so(self):
        with pytest.raises(ContextError) as e:
            await resolve_context(
                _config(org="nope", project="x"),
                _client(orgs=[{"id": ORG_UUID, "alias": "bp"}]),
            )
        assert "nope" in e.value.message

    @pytest.mark.asyncio
    async def test_project_optional_when_not_required(self):
        ctx = await resolve_context(
            _config(org=ORG_UUID), _client(), require_project=False
        )
        assert ctx.project_id is None

    @pytest.mark.asyncio
    async def test_id_beats_alias_when_both_could_match(self):
        """Mirrors the server's resolve_project: id, then alias, then name."""
        ctx = await resolve_context(
            _config(org=ORG_UUID, project="shared"),
            _client(
                projects=[
                    {"id": "shared", "alias": "other"},
                    {"id": PROJ_UUID, "alias": "shared"},
                ]
            ),
        )
        assert ctx.project_id == "shared"


class TestClientResolvesLazily:
    """The client resolves the org itself, so ~40 handlers don't each need to."""

    @pytest.mark.asyncio
    async def test_it_resolves_before_a_request(self):
        from src.cli.client import InnoDayAPIClient

        config = MagicMock()
        config.get_api_url.return_value = "https://www.inno.day"
        config.get_api_timeout.return_value = 30.0
        config.get_current_organization.return_value = "bp"
        config.get_current_project_id.return_value = None
        config.get_user_id.return_value = None
        config.get_cli_token.return_value = None
        config.get_team_secret.return_value = None
        config._config = {"organizations": {}}

        client = InnoDayAPIClient(config)
        assert client.organization_id is None

        with patch(
            "src.cli.utils.context._resolve_org_id",
            new=AsyncMock(return_value=ORG_UUID),
        ):
            resolved = await client.ensure_org()
        assert resolved == ORG_UUID
        assert client.organization_id == ORG_UUID

    @pytest.mark.asyncio
    async def test_a_cached_id_is_left_alone(self):
        from src.cli.client import InnoDayAPIClient

        config = MagicMock()
        config.get_api_url.return_value = "https://www.inno.day"
        config.get_api_timeout.return_value = 30.0
        config.get_current_organization.return_value = "bp"
        config.get_current_project_id.return_value = None
        config.get_user_id.return_value = None
        config.get_cli_token.return_value = None
        config.get_team_secret.return_value = None
        config._config = {"organizations": {"bp": {"id": ORG_UUID}}}

        client = InnoDayAPIClient(config)
        with patch(
            "src.cli.utils.context._resolve_org_id",
            new=AsyncMock(side_effect=AssertionError("should not be called")),
        ):
            assert await client.ensure_org() == ORG_UUID
