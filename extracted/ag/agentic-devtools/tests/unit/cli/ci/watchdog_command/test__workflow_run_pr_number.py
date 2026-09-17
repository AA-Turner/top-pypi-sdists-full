"""Tests for _workflow_run_pr_number()."""

from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.watchdog_command import _workflow_run_pr_number


class TestWorkflowRunPrNumber:
    """Tests for workflow run pull-request extraction."""

    def test_prefers_first_valid_pull_request_number(self) -> None:
        run = {"pull_requests": [{"number": "bad"}, {"number": 42}], "pr_number": 99}
        assert _workflow_run_pr_number(run) == 42

    def test_uses_dict_fallback_when_pull_requests_have_no_valid_number(self) -> None:
        assert _workflow_run_pr_number({"pull_requests": ["bad"], "pr_number": 43}) == 43
        assert _workflow_run_pr_number({"pull_requests": "bad", "pr_number": 44}) == 44

    def test_reads_object_pull_request_number(self) -> None:
        assert _workflow_run_pr_number(SimpleNamespace(pr_number=45)) == 45

    @pytest.mark.parametrize("run", [{}, {"pr_number": True}, {"pr_number": "46"}, SimpleNamespace()])
    def test_returns_zero_for_missing_or_invalid_numbers(self, run) -> None:
        assert _workflow_run_pr_number(run) == 0
