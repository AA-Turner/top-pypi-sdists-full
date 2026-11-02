"""Tests for preserving dispatch actions while attaching inventory diagnostics."""

import pytest

from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import LiveEligibilityChecker, summarize_scan
from agentic_devtools.cli.ci.reconciliation.models import ReconciliationAction


@pytest.mark.parametrize("observed", [False, True])
def test_summarize_scan_keeps_action_and_unobserved_message(observed, monkeypatch):
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    checker = LiveEligibilityChecker(frozenset(), True, None) if observed else None
    action, message = summarize_scan((ReconciliationAction.NO_ACTION, "original"), checker)
    assert action is ReconciliationAction.NO_ACTION
    assert ("blocked" in message) if observed else message == "original"
