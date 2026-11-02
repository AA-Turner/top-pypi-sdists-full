"""Tests for _condensed_log_budget()."""

from agentic_devtools.cli.ci.github_provider import _condensed_log_budget


class TestCondensedLogBudget:
    """Tests for selecting condensed-log budgets by repair type."""

    def test_ci_dispatch_uses_ci_only_budget(self) -> None:
        assert _condensed_log_budget("ci") == 40_000

    def test_non_ci_dispatch_uses_shared_budget(self) -> None:
        assert _condensed_log_budget("both") == 24_000
