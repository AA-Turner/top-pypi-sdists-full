"""Tests for suppressed_reaper.reap_no_change_prs()."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.suppressed_reaper import reap_no_change_prs
from tests.unit.cli.ci.suppressed_reaper._fixtures import ISSUE, brief, pr_body, provider


class TestReapNoChangePrs:
    """The run loop over every open candidate pull request."""

    def test_closes_an_eligible_pr_and_reports_it(self) -> None:
        """An eligible PR is closed and reported with its deferral issue."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = [brief()]
        result = reap_no_change_prs(mock)
        assert result["checked"] == 1
        assert result["closed"] == [{"pr": 99, "issue": ISSUE}]
        assert result["skipped"] == []
        assert result["dry_run"] is False
        mock.close_pr.assert_called_once()

    def test_skips_an_ineligible_pr_with_its_reason(self) -> None:
        """A rejected PR is reported with the condition that failed."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = [brief(body=pr_body(marker=False))]
        result = reap_no_change_prs(mock)
        assert result["closed"] == []
        assert result["skipped"] == [{"pr": 99, "reason": "no-marker"}]
        mock.close_pr.assert_not_called()

    def test_dry_run_reports_without_mutating(self) -> None:
        """A dry run names the PRs it would close but performs no mutation."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = [brief()]
        result = reap_no_change_prs(mock, dry_run=True)
        assert result == {"checked": 1, "closed": [{"pr": 99, "issue": ISSUE}], "skipped": [], "dry_run": True}
        mock.post_issue_comment.assert_not_called()
        mock.close_issue.assert_not_called()
        mock.close_pr.assert_not_called()

    def test_evaluation_failure_leaves_the_pr_open(self) -> None:
        """A provider error during evaluation never closes anything."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = [brief()]
        mock.get_issue_facts.side_effect = RuntimeError("boom")
        result = reap_no_change_prs(mock)
        assert result["skipped"] == [{"pr": 99, "reason": "evaluation-failed"}]
        mock.close_pr.assert_not_called()

    def test_close_failure_is_reported_and_does_not_abort_the_run(self) -> None:
        """One failed close is recorded; the next candidate is still evaluated."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = [brief(), brief(number=100)]
        mock.close_pr.side_effect = [RuntimeError("boom"), None]
        result = reap_no_change_prs(mock)
        assert result["skipped"] == [{"pr": 99, "reason": "close-failed"}]
        assert result["closed"] == [{"pr": 100, "issue": ISSUE}]

    def test_head_change_is_reported_with_a_stable_skip_reason(self) -> None:
        """A fresh push after evaluation leaves the PR open for the next run."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = [brief()]
        mock.get_pr_metadata.return_value = PRMetadata(
            number=99,
            title="No changes needed",
            head_branch="copilot/triage",
            head_sha="new-head",
            base_branch="main",
        )
        result = reap_no_change_prs(mock)
        assert result["closed"] == []
        assert result["skipped"] == [{"pr": 99, "reason": "head-changed"}]

    def test_max_prs_caps_the_number_of_closes(self) -> None:
        """Evaluation stops once the close budget for the run is spent."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = [brief(), brief(number=100)]
        result = reap_no_change_prs(mock, max_prs=1)
        assert result["checked"] == 1
        assert result["closed"] == [{"pr": 99, "issue": ISSUE}]

    @pytest.mark.parametrize("max_prs", [0, -1])
    def test_non_positive_max_prs_is_rejected(self, max_prs: int) -> None:
        """A non-positive budget is a caller error, not a silent no-op."""
        with pytest.raises(ValueError, match="max_prs must be a positive integer"):
            reap_no_change_prs(provider(), max_prs=max_prs)

    def test_no_candidates_is_a_clean_no_op(self) -> None:
        """An empty candidate list produces an empty summary."""
        mock = provider()
        mock.list_no_change_candidate_prs.return_value = []
        assert reap_no_change_prs(mock) == {"checked": 0, "closed": [], "skipped": [], "dry_run": False}
