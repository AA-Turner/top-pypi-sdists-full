"""The MCP `blastoff` tool has to turn ids into aliases before it can resolve.

`/api/v1/onboarding/resolve` -- the route that answers "which GitHub account and
which topics" -- matches on alias alone, while every reference the tool holds is
a UUID: an explicit `organization_id`/`project_id` is passed through verbatim,
and the fallback reads `innoday_id` out of `.innoday/project.yml`. So the tool
could not resolve a project at all, and the error it returned told the caller to
pass the two ids whose presence was the cause.

These tests pin the three shapes a caller actually arrives in -- ids, aliases,
nothing -- plus what is said when the project genuinely cannot be resolved.
"""

from __future__ import annotations

import io
import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from src.mcp import server

ORG_UUID = "5ec2cc85-55a8-431e-b8c5-c0178c9db00e"
PROJECT_UUID = "4f61ff9f-8138-471a-b321-4ff19eb7604d"


def _alias_lookup(org_alias="bp", project_alias="BPAI"):
    """Stand in for the org and project routes, which both accept either form.

    Keyed on the path rather than on call order so a test reads as "the org
    route answers this", not "the first call answers this".
    """

    async def _get(path, params=None):
        if "/projects/" in path:
            return {"id": PROJECT_UUID, "alias": project_alias, "name": "A project"}
        return {"id": ORG_UUID, "alias": org_alias, "name": "An organization"}

    return _get


def _run_blastoff(
    *, resolve_returns=None, org=None, project=None, alias_get=None, resolve_fn=None
):
    """Drive the tool far enough to see what `_resolve_release_target` was given.

    Everything past resolution -- the API client, the version store, the engine
    itself -- is replaced, because none of it is what is under test and all of
    it would reach the network.
    """
    from src.cli.commands import release_proxy

    seen: dict = {}

    async def fake_resolve(config, org_ref, project_ref):
        seen["org_ref"] = org_ref
        seen["project_ref"] = project_ref
        return resolve_returns

    api_client = MagicMock()
    api_client.close = AsyncMock()

    # Real strings, because the brief is serialised with `json.dumps` before it
    # reaches the engine and a MagicMock would not survive that.
    store = MagicMock()
    store.load_org_config.return_value = SimpleNamespace(
        next_version="v1.4.0",
        last_released_version="v1.3.0",
        last_released="2026-07-01T00:00:00Z",
    )

    with (
        patch.object(server._api, "resolve_org", return_value=org),
        patch.object(server._api, "resolve_project", return_value=project),
        patch.object(server._api, "get", side_effect=alias_get or _alias_lookup()),
        patch.object(server, "build_cli_config", return_value=MagicMock()),
        patch.object(
            release_proxy, "_resolve_release_target", resolve_fn or fake_resolve
        ),
        patch.object(release_proxy, "_build_store", return_value=store),
        patch("src.cli.client.InnoDayAPIClient", MagicMock(return_value=api_client)),
        patch.object(
            release_proxy.ReleaseProxyCommands,
            "_ticket_picture",
            staticmethod(lambda *a, **k: None),
        ),
        patch.object(
            release_proxy.ReleaseProxyCommands,
            "_invoke_blastoff",
            staticmethod(lambda *a, **k: 0),
        ),
    ):
        import asyncio

        result = asyncio.run(
            server.blastoff(
                release=False,
                hotfix=False,
                summary=None,
                topics=None,
                repo=None,
                commit=None,
                organization_id=None,
                project_id=None,
            )
        )
    return seen, result


TARGET = ("BPAI", "havilandsoftware", ["bpai"])


class TestWhicheverFormTheCallerHas:
    def test_uuids_are_looked_up_and_resolved_by_alias(self):
        seen, result = _run_blastoff(
            resolve_returns=TARGET, org=ORG_UUID, project=PROJECT_UUID
        )
        assert seen == {"org_ref": "bp", "project_ref": "BPAI"}
        assert "error" not in result

    def test_aliases_keep_working(self):
        """An alias round-trips: the routes accept one and hand back the
        canonical spelling, so a caller who already passed aliases is not
        broken by the lookup that was added for the ones who passed ids."""
        seen, result = _run_blastoff(
            resolve_returns=TARGET,
            org="bp",
            project="BPAI",
            alias_get=_alias_lookup(),
        )
        assert seen == {"org_ref": "bp", "project_ref": "BPAI"}
        assert "error" not in result

    def test_the_canonical_spelling_wins_over_the_one_passed(self):
        """`resolve_project` matches an alias case-insensitively, so a caller
        may pass `bpai` for project `BPAI`. `/onboarding/resolve` does not, and
        that mismatch is the case-sensitivity trap `_resolve_release_target`
        was written to escape -- so the alias InnoDay returns is the one used."""
        seen, _ = _run_blastoff(resolve_returns=TARGET, org="BP", project="bpai")
        assert seen == {"org_ref": "bp", "project_ref": "BPAI"}

    def test_a_failed_lookup_falls_back_to_the_reference_as_given(self):
        """A release must not be lost to the extra call. If the lookup cannot
        answer, the caller's own value is tried -- which is right whenever it
        was an alias already."""

        async def _explode(path, params=None):
            raise RuntimeError("the API is unreachable")

        seen, _ = _run_blastoff(
            resolve_returns=TARGET, org="bp", project="BPAI", alias_get=_explode
        )
        assert seen == {"org_ref": "bp", "project_ref": "BPAI"}


class TestWhatIsSaidWhenNothingResolves:
    def test_the_message_names_what_could_not_be_resolved(self):
        _, result = _run_blastoff(
            resolve_returns=None, org=ORG_UUID, project=PROJECT_UUID
        )
        assert "bp" in result["error"] and "BPAI" in result["error"]
        assert result["organization"] == "bp"
        assert result["project"] == "BPAI"

    def test_it_no_longer_advises_the_action_that_just_failed(self):
        """The old message asked for `organization_id` and `project_id`. A
        caller who passed both read it as "you did it wrong" and passed them
        again, which is the one thing that could not help."""
        _, result = _run_blastoff(
            resolve_returns=None, org=ORG_UUID, project=PROJECT_UUID
        )
        assert "organization_id" not in result["error"]
        assert "project_id" not in result["error"]

    def test_nothing_configured_is_still_reported_before_any_lookup(self):
        _, result = _run_blastoff(resolve_returns=None, org=None, project=None)
        assert "organization_id required" in result["error"]


class TestTheProtocolChannelStaysClean:
    def test_resolution_failure_prints_nothing_to_stdout(self):
        """`_resolve_release_target` reports its refusals with `console.print`.
        Under stdio transport stdout carries JSON-RPC, so a printed refusal
        corrupts the framing of every response after it."""

        async def printing_resolve(config, org_ref, project_ref):
            print("Could not resolve this project from InnoDay: not found")
            return None

        captured = io.StringIO()
        real_stdout = sys.stdout
        sys.stdout = captured
        try:
            _, result = _run_blastoff(
                org=ORG_UUID, project=PROJECT_UUID, resolve_fn=printing_resolve
            )
        finally:
            sys.stdout = real_stdout

        assert captured.getvalue() == ""
        assert "not found" in (result.get("details") or "")
