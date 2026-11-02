"""Tests for same-scan GitHub eligibility diagnostics."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import AgentTaskInventoryLoadResult
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import _build_live_eligibility_checker
from agentic_devtools.cli.ci.scheduler_inventory_scan import SchedulerInventoryScan


@pytest.mark.parametrize("inventory", [None, AgentTaskInventoryLoadResult(({},), complete=False)])
def test_unknown_snapshot_returns_none_even_with_eligible_members(inventory):
    provider = GitHubActionsProvider(repo="owner/repo")
    scan = SchedulerInventoryScan()
    if inventory is not None:
        scan.load(lambda: inventory)
    provider._scheduler_inventory_scan = scan
    provider.list_eligible_prs = MagicMock(return_value=[MagicMock(number=42)])
    checker = _build_live_eligibility_checker(provider)
    assert checker(MagicMock(pr_number=42)) is None
    assert checker(MagicMock(pr_number=99)) is None
    assert checker.diagnostics()["inventory_status"] == "unknown"


def test_complete_snapshot_uses_known_membership():
    provider = GitHubActionsProvider(repo="owner/repo")
    scan = SchedulerInventoryScan()
    scan.load(lambda: [])
    provider._scheduler_inventory_scan = scan
    provider.list_eligible_prs = MagicMock(return_value=[MagicMock(number=42)])
    checker = _build_live_eligibility_checker(provider)
    assert checker(MagicMock(pr_number=42)) is True
    assert checker(MagicMock(pr_number=99)) is False
    assert checker.diagnostics()["inventory_status"] == "complete"


@pytest.mark.parametrize("snapshot", [None, object()])
def test_missing_snapshot_is_not_complete_empty(snapshot):
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._scheduler_inventory_scan = snapshot
    provider.list_eligible_prs = MagicMock(return_value=[])
    checker = _build_live_eligibility_checker(provider)
    assert checker(MagicMock(pr_number=42)) is None
    assert checker.diagnostics()["inventory_availability"] is None


def test_non_github_provider_keeps_plain_eligibility_behavior():
    provider = MagicMock()
    provider.list_eligible_prs.return_value = [MagicMock(number=42)]
    checker = _build_live_eligibility_checker(provider)
    assert checker(MagicMock(pr_number=42)) is True
    assert checker(MagicMock(pr_number=99)) is False
    assert checker.diagnostics() == {}
    assert checker.summarize("existing message") == "existing message"
