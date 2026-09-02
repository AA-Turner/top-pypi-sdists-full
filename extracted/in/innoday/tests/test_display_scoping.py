"""Two commands that answered about one project while labelling it another.

Both are display bugs, and both are worse than they sound: the *data* was right
in each case, so nothing looked broken. They cost real time here —
`releases list` returning the whole organization put S4C's `v0.1.0 IN_PROGRESS`
and `v0.2.0 PLANNED` inside PF's listing, and those two rows were diagnosed
twice as genuine corruption of PF's release pipeline before anyone checked which
project owned them.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _releases():
    from src.cli.commands.releases import ReleasesCommands

    return ReleasesCommands


class TestReleasesListFollowsTheProjectInContext:
    """It read `args.project_id` directly while every sibling in the file goes
    through `_resolve_project_id`, which falls back to the cwd's project."""

    def test_resolver_prefers_an_explicit_flag(self):
        config = MagicMock()
        config.get_current_project_id.return_value = "from-cwd"
        args = SimpleNamespace(project_id="explicit")
        assert _releases()._resolve_project_id(args, config) == "explicit"

    def test_resolver_falls_back_to_the_cwd_project(self):
        config = MagicMock()
        config.get_current_project_id.return_value = "from-cwd"
        args = SimpleNamespace(project_id=None)
        assert _releases()._resolve_project_id(args, config) == "from-cwd"

    @pytest.mark.asyncio
    async def test_the_request_carries_the_cwd_project_as_a_filter(self):
        """The regression itself, asserted on the outgoing request: with no
        explicit flag the call used to carry no project_id at all, so the API
        answered org-wide while the output presented as one project's."""
        cmds = _releases()
        config = MagicMock()
        config.get_current_project_id.return_value = "pf-uuid"

        client = MagicMock()
        client.get = AsyncMock(
            return_value=SimpleNamespace(status_code=200, json=lambda: [], text="[]")
        )
        client.close = AsyncMock()

        with (
            patch("src.cli.commands.releases.InnoDayAPIClient", return_value=client),
            # The handler resolves the org through the async path now, because an
            # alias reaching the URL makes this route answer 200-with-empty-list
            # rather than erroring.
            patch.object(
                cmds, "_resolve_org_id_async", new=AsyncMock(return_value="org-1")
            ),
        ):
            await cmds._handle_list(SimpleNamespace(project_id=None, limit=10), config)

        assert client.get.call_args.kwargs["params"]["project_id"] == "pf-uuid"

    @pytest.mark.asyncio
    async def test_an_explicit_project_still_wins(self):
        cmds = _releases()
        config = MagicMock()
        config.get_current_project_id.return_value = "pf-uuid"

        client = MagicMock()
        client.get = AsyncMock(
            return_value=SimpleNamespace(status_code=200, json=lambda: [], text="[]")
        )
        client.close = AsyncMock()

        with (
            patch("src.cli.commands.releases.InnoDayAPIClient", return_value=client),
            # The handler resolves the org through the async path now, because an
            # alias reaching the URL makes this route answer 200-with-empty-list
            # rather than erroring.
            patch.object(
                cmds, "_resolve_org_id_async", new=AsyncMock(return_value="org-1")
            ),
        ):
            await cmds._handle_list(
                SimpleNamespace(project_id="other-uuid", limit=10), config
            )

        assert client.get.call_args.kwargs["params"]["project_id"] == "other-uuid"


class TestSummaryLabelsTheProjectItSummarised:
    """There are two `--project` flags — the global one on the entrypoint and
    the summary subcommand's — and the label logic knew only about the second.

        cd ~/workspaces/hs/pf
        innoday --organization bp --project BPCL summary --scrum
        -> "Team · last 1w · PF"

    The payload carried BPCL's project_id, so the numbers were BPCL's. Only the
    title said PF, which attributes one client's work to another client's
    project in the artefact whose whole purpose is to be read and acted on.
    """

    def label_for(self, project_ref, context):
        """The rule the command now applies: borrow the working directory's
        alias only when the ref *is* that project."""
        label = str(project_ref)
        if project_ref and project_ref == context.get("project_id"):
            label = context.get("project_alias") or context.get("project_name") or label
        return label

    def test_the_cwd_alias_is_used_when_the_ref_is_the_cwd_project(self):
        context = {"project_id": "pf-uuid", "project_alias": "PF"}
        assert self.label_for("pf-uuid", context) == "PF"

    def test_another_projects_ref_does_not_borrow_the_cwd_alias(self):
        """The bug: BPCL summarised from a PF workspace must not read 'PF'."""
        context = {"project_id": "pf-uuid", "project_alias": "PF"}
        assert self.label_for("BPCL", context) == "BPCL"

    def test_a_uuid_with_no_matching_context_labels_itself(self):
        """Better an unhelpful UUID than a confident wrong name."""
        assert self.label_for("4e1eac51", {"project_id": "pf-uuid"}) == "4e1eac51"

    def test_no_context_at_all_is_handled(self):
        assert self.label_for("BPCL", {}) == "BPCL"
