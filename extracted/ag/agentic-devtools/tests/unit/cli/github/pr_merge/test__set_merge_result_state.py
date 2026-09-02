"""Tests for _set_merge_result_state helper."""

from unittest.mock import call, patch

from agentic_devtools.cli.github import pr_merge


class TestSetMergeResultState:
    """Tests for _set_merge_result_state."""

    def test_sets_all_three_state_keys_on_success(self):
        """Writes merged=True, mergedAt, and strategy to state."""
        with patch.object(pr_merge, "set_value") as mock_set:
            pr_merge._set_merge_result_state(True, "2026-04-07T09:05:55Z", "squash")

        assert mock_set.call_count == 3
        mock_set.assert_any_call("github.pr_merged", True)
        mock_set.assert_any_call("github.pr_merged_at", "2026-04-07T09:05:55Z")
        mock_set.assert_any_call("github.pr_merge_strategy", "squash")

    def test_sets_all_three_state_keys_on_failure(self):
        """Writes merged=False, mergedAt=None, and strategy to state."""
        with patch.object(pr_merge, "set_value") as mock_set:
            pr_merge._set_merge_result_state(False, None, "rebase")

        assert mock_set.call_count == 3
        mock_set.assert_any_call("github.pr_merged", False)
        mock_set.assert_any_call("github.pr_merged_at", None)
        mock_set.assert_any_call("github.pr_merge_strategy", "rebase")

    def test_calls_set_value_in_order(self):
        """State keys are written in the declared order: merged, mergedAt, strategy."""
        with patch.object(pr_merge, "set_value") as mock_set:
            pr_merge._set_merge_result_state(True, "2026-01-01T00:00:00Z", "merge")

        assert mock_set.call_args_list == [
            call("github.pr_merged", True),
            call("github.pr_merged_at", "2026-01-01T00:00:00Z"),
            call("github.pr_merge_strategy", "merge"),
        ]

    def test_strategy_value_is_forwarded_verbatim(self):
        """The strategy string is passed through unchanged."""
        with patch.object(pr_merge, "set_value") as mock_set:
            pr_merge._set_merge_result_state(False, None, "squash")

        mock_set.assert_any_call("github.pr_merge_strategy", "squash")
