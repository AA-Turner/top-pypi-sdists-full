"""Tests for select_labels_to_propagate."""

from agentic_devtools.cli.ci.scheduler import (
    AUTO_MERGE_LABEL,
    PROPAGATED_ISSUE_LABELS,
    SUPPRESSED_FOLLOW_UP_LABEL,
    select_labels_to_propagate,
)


class TestSelectLabelsToPropagate:
    """Tests for the select_labels_to_propagate pure function."""

    def test_allowlist_contains_exactly_the_two_propagated_labels(self) -> None:
        assert PROPAGATED_ISSUE_LABELS == (AUTO_MERGE_LABEL, SUPPRESSED_FOLLOW_UP_LABEL)

    def test_allowlisted_issue_label_is_selected(self) -> None:
        assert select_labels_to_propagate([], [AUTO_MERGE_LABEL]) == [AUTO_MERGE_LABEL]

    def test_both_allowlisted_labels_selected_in_allowlist_order(self) -> None:
        result = select_labels_to_propagate([], [SUPPRESSED_FOLLOW_UP_LABEL, AUTO_MERGE_LABEL])
        assert result == [AUTO_MERGE_LABEL, SUPPRESSED_FOLLOW_UP_LABEL]

    def test_non_allowlisted_labels_are_never_copied(self) -> None:
        assert select_labels_to_propagate([], ["bug", "Subtask", "ai-pr-loop-ignore"]) == []

    def test_no_linked_issue_labels_returns_empty(self) -> None:
        assert select_labels_to_propagate(["some-label"], []) == []

    def test_label_already_on_pr_is_not_reselected(self) -> None:
        result = select_labels_to_propagate(
            [AUTO_MERGE_LABEL],
            [AUTO_MERGE_LABEL, SUPPRESSED_FOLLOW_UP_LABEL],
        )
        assert result == [SUPPRESSED_FOLLOW_UP_LABEL]

    def test_all_labels_already_present_returns_empty(self) -> None:
        assert select_labels_to_propagate(PROPAGATED_ISSUE_LABELS, PROPAGATED_ISSUE_LABELS) == []

    def test_duplicate_issue_labels_are_deduplicated(self) -> None:
        assert select_labels_to_propagate([], [AUTO_MERGE_LABEL, AUTO_MERGE_LABEL]) == [AUTO_MERGE_LABEL]

    def test_non_string_and_empty_entries_are_ignored(self) -> None:
        assert select_labels_to_propagate([None, 42, ""], [AUTO_MERGE_LABEL, None, "", 7]) == [AUTO_MERGE_LABEL]

    def test_non_string_pr_label_does_not_mask_propagation(self) -> None:
        assert select_labels_to_propagate([None], [AUTO_MERGE_LABEL]) == [AUTO_MERGE_LABEL]

    def test_custom_allowlist_is_honored(self) -> None:
        result = select_labels_to_propagate([], [AUTO_MERGE_LABEL, "needs-triage"], allowlist=("needs-triage",))
        assert result == ["needs-triage"]
