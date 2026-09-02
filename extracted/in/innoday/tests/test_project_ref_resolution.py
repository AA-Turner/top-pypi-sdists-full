"""`--project ALIAS` must reach the API as a UUID.

The organization half of this was primed centrally and the project half was not,
which is not a symmetric omission: an org ref is only ever a URL prefix that the
generic verbs insert, but a project ref is baked into a query parameter or an
endpoint string by the command itself, before any verb runs. Measured against the
deployed API, with the alias:

    innoday --org hs --project PF releases list   ->  "No releases found"
    innoday --org hs --project PF tickets list    ->  "Project 'PF' not found"

and with the same project's UUID, three releases and 362 tickets. The releases
case is the one worth a test rather than a fix-and-move-on: `Release.project_id`
is a UUID column, so the alias matches no row and the route answers `HTTP 200`
with an empty list. A command that confidently reports nothing is indistinguishable
from a project that genuinely has nothing.
"""

from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.main import _prime_project_id

PF = "e52b7372-3537-49f5-91e9-6db52a2794e3"


def _config(project_ref, org_alias="hs"):
    config = MagicMock()
    config.get_current_project_id.return_value = project_ref
    config.get_current_organization.return_value = org_alias
    return config


@contextmanager
def _patched(projects=None, org_id="org-uuid", raise_on_project=None):
    """Patch the resolvers `_prime_project_id` imports at call time."""
    from src.cli.utils import context

    async def fake_project(client, org, ref):
        if raise_on_project:
            raise raise_on_project
        return (projects or {})[ref]

    client = MagicMock()
    client.close = AsyncMock()

    with (
        patch("src.cli.client.InnoDayAPIClient", return_value=client),
        patch.object(context, "_resolve_org_id", AsyncMock(return_value=org_id)),
        patch.object(context, "_resolve_project_id", side_effect=fake_project),
    ):
        yield


class TestAnAliasIsResolvedBeforeDispatch:
    @pytest.mark.asyncio
    async def test_the_alias_is_replaced_by_the_uuid(self):
        config = _config("PF")
        args = SimpleNamespace(command="releases", project_id="PF")

        with _patched(projects={"PF": PF}):
            error = await _prime_project_id(config, args)

        assert error is None
        config.set_project_override.assert_called_once_with(PF)

    @pytest.mark.asyncio
    async def test_the_namespace_is_rewritten_too(self):
        """`releases` and `tickets` read the flag off `args`, not through the
        config, so updating only the config would leave them holding the alias."""
        config = _config("PF")
        args = SimpleNamespace(command="releases", project_id="PF")

        with _patched(projects={"PF": PF}):
            await _prime_project_id(config, args)

        assert args.project_id == PF


class TestWhatIsSkipped:
    @pytest.mark.asyncio
    async def test_a_uuid_costs_no_request(self):
        """The workspace path: `.innoday/project.yml` already holds a UUID, so
        the common case must not pay for a lookup."""
        config = _config(PF)
        args = SimpleNamespace(command="releases", project_id=None)

        with patch("src.cli.client.InnoDayAPIClient") as client_cls:
            assert await _prime_project_id(config, args) is None

        client_cls.assert_not_called()
        config.set_project_override.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_project_at_all_is_not_an_error(self):
        config = _config(None)
        args = SimpleNamespace(command="orgs", project_id=None)
        assert await _prime_project_id(config, args) is None

    @pytest.mark.asyncio
    async def test_commands_that_never_need_an_org_are_skipped(self):
        """`login` runs before any org exists; resolving would fail and the
        failure would be reported instead of the command running."""
        config = _config("PF")
        args = SimpleNamespace(command="login", project_id="PF")

        with patch("src.cli.client.InnoDayAPIClient") as client_cls:
            assert await _prime_project_id(config, args) is None

        client_cls.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_organization_means_nothing_to_resolve_against(self):
        config = _config("PF", org_alias=None)
        args = SimpleNamespace(command="releases", project_id="PF")

        with patch("src.cli.client.InnoDayAPIClient") as client_cls:
            assert await _prime_project_id(config, args) is None

        client_cls.assert_not_called()


class TestHowFailureIsReported:
    """Deliberately unlike `_prime_org_id`, which is silent. The ref was typed on
    this command line; naming it beats a downstream 404 -- or an empty list."""

    @pytest.mark.asyncio
    async def test_an_unknown_project_is_named(self):
        from src.cli.utils.context import ContextError

        config = _config("NOPE")
        args = SimpleNamespace(command="releases", project_id="NOPE")
        err = ContextError(
            "No project 'NOPE' in this organization.",
            "Run `innoday projects list` to see them.",
        )

        with _patched(raise_on_project=err):
            message = await _prime_project_id(config, args)

        assert "NOPE" in message
        assert "projects list" in message
        config.set_project_override.assert_not_called()

    @pytest.mark.asyncio
    async def test_a_transport_failure_is_left_to_the_command(self):
        """A network hiccup raised out of context here reads as a bad --project.
        The command's own error handling says something truer."""
        config = _config("PF")
        args = SimpleNamespace(command="releases", project_id="PF")

        with _patched(raise_on_project=RuntimeError("connection reset")):
            assert await _prime_project_id(config, args) is None

        config.set_project_override.assert_not_called()


class TestTheOverrideWinsOverTheWorkspace:
    """`get_current_project_id` returns `_project_override or platform.project_id`,
    so writing the workspace slot would leave the alias still winning -- which is
    why this needs its own setter rather than `set_current_project_id`."""

    def test_setting_the_override_is_what_the_getter_returns(self):
        from src.cli.config import CLIConfig

        config = CLIConfig.__new__(CLIConfig)
        config._project_override = "PF"
        config._project_resolved_this_invocation = True
        config._config = {"platform": {"project_id": "some-workspace-uuid"}}

        assert config.get_current_project_id() == "PF"
        config.set_project_override(PF)
        assert config.get_current_project_id() == PF

    def test_the_resolved_value_is_not_persisted(self):
        """`~/.innoday/config.json` is shared by every terminal on the machine;
        a written-back project is the global mutable state cwd-resolution exists
        to avoid."""
        from src.cli.config import CLIConfig

        config = CLIConfig.__new__(CLIConfig)
        config._project_override = "PF"
        config._project_resolved_this_invocation = True
        config._config = {"platform": {"project_id": "workspace-uuid"}}

        config.set_project_override(PF)

        assert config._config["platform"]["project_id"] == "workspace-uuid"
