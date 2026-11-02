"""Tests for resolve_pr_context_budget."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import (
    DEFAULT_PR_CONTEXT_BUDGET,
    resolve_pr_context_budget,
)

_ENV = "AGDT_PR_CONTEXT_BUDGET"


class TestResolvePrContextBudget:
    def test_default_when_unset(self, monkeypatch):
        monkeypatch.delenv(_ENV, raising=False)
        assert resolve_pr_context_budget() == DEFAULT_PR_CONTEXT_BUDGET

    def test_default_when_invalid(self, monkeypatch):
        monkeypatch.setenv(_ENV, "not-a-number")
        assert resolve_pr_context_budget() == DEFAULT_PR_CONTEXT_BUDGET

    def test_default_when_non_positive(self, monkeypatch):
        monkeypatch.setenv(_ENV, "0")
        assert resolve_pr_context_budget() == DEFAULT_PR_CONTEXT_BUDGET
        monkeypatch.setenv(_ENV, "-10")
        assert resolve_pr_context_budget() == DEFAULT_PR_CONTEXT_BUDGET

    def test_valid_value(self, monkeypatch):
        monkeypatch.setenv(_ENV, "5000")
        assert resolve_pr_context_budget() == 5000
