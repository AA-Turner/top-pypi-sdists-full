"""Tests for propagate_linked_issue_labels."""

import logging
from unittest.mock import MagicMock, call

import pytest

from agentic_devtools.cli.ci.scheduler import (
    AUTO_MERGE_LABEL,
    SUPPRESSED_FOLLOW_UP_LABEL,
    EligiblePR,
    propagate_linked_issue_labels,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestPropagateLinkedIssueLabels:
    """Tests for the propagate_linked_issue_labels orchestration function."""

    def test_applies_pending_labels(self) -> None:
        provider = MagicMock()
        prs = [EligiblePR(number=2020, created_at="", labels_to_propagate=(AUTO_MERGE_LABEL,))]

        result = propagate_linked_issue_labels(provider, prs)

        provider.add_label.assert_called_once_with(2020, AUTO_MERGE_LABEL)
        assert result == {2020: [AUTO_MERGE_LABEL]}

    def test_applies_multiple_labels_for_multiple_prs(self) -> None:
        provider = MagicMock()
        prs = [
            EligiblePR(
                number=2020,
                created_at="",
                labels_to_propagate=(AUTO_MERGE_LABEL, SUPPRESSED_FOLLOW_UP_LABEL),
            ),
            EligiblePR(number=2021, created_at="", labels_to_propagate=(SUPPRESSED_FOLLOW_UP_LABEL,)),
        ]

        result = propagate_linked_issue_labels(provider, prs)

        assert provider.add_label.call_args_list == [
            call(2020, AUTO_MERGE_LABEL),
            call(2020, SUPPRESSED_FOLLOW_UP_LABEL),
            call(2021, SUPPRESSED_FOLLOW_UP_LABEL),
        ]
        assert result == {
            2020: [AUTO_MERGE_LABEL, SUPPRESSED_FOLLOW_UP_LABEL],
            2021: [SUPPRESSED_FOLLOW_UP_LABEL],
        }

    def test_pr_without_pending_labels_makes_no_api_call(self) -> None:
        provider = MagicMock()
        prs = [EligiblePR(number=2020, created_at="")]

        result = propagate_linked_issue_labels(provider, prs)

        provider.add_label.assert_not_called()
        assert result == {}

    def test_empty_pr_list_makes_no_api_call(self) -> None:
        provider = MagicMock()

        assert propagate_linked_issue_labels(provider, []) == {}
        provider.add_label.assert_not_called()

    def test_dry_run_reports_without_calling_provider(self) -> None:
        provider = MagicMock()
        prs = [EligiblePR(number=2020, created_at="", labels_to_propagate=(AUTO_MERGE_LABEL,))]

        result = propagate_linked_issue_labels(provider, prs, dry_run=True)

        provider.add_label.assert_not_called()
        assert result == {2020: [AUTO_MERGE_LABEL]}

    def test_failure_is_non_fatal_and_other_labels_continue(self, caplog) -> None:
        provider = MagicMock()
        provider.add_label.side_effect = [RuntimeError("403 Forbidden"), None]
        prs = [
            EligiblePR(
                number=2020,
                created_at="",
                labels_to_propagate=(AUTO_MERGE_LABEL, SUPPRESSED_FOLLOW_UP_LABEL),
            )
        ]

        with caplog.at_level(logging.WARNING):
            result = propagate_linked_issue_labels(provider, prs)

        assert result == {2020: [SUPPRESSED_FOLLOW_UP_LABEL]}
        assert "403 Forbidden" in caplog.text

    def test_pr_omitted_when_every_label_fails(self) -> None:
        provider = MagicMock()
        provider.add_label.side_effect = RuntimeError("boom")
        prs = [
            EligiblePR(number=2020, created_at="", labels_to_propagate=(AUTO_MERGE_LABEL,)),
            EligiblePR(number=2021, created_at="", labels_to_propagate=(AUTO_MERGE_LABEL,)),
        ]

        result = propagate_linked_issue_labels(provider, prs)

        assert result == {}
        assert provider.add_label.call_count == 2

    def test_rate_limit_error_is_re_raised(self) -> None:
        provider = MagicMock()
        provider.add_label.side_effect = ProviderRateLimitError(is_rate_limit=True)
        prs = [EligiblePR(number=2020, created_at="", labels_to_propagate=(AUTO_MERGE_LABEL,))]

        with pytest.raises(ProviderRateLimitError):
            propagate_linked_issue_labels(provider, prs)

    def test_non_allowlisted_labels_are_silently_dropped_at_mutation_boundary(self) -> None:
        """Labels not in PROPAGATED_ISSUE_LABELS must never reach add_label."""
        provider = MagicMock()
        prs = [
            EligiblePR(
                number=2020,
                created_at="",
                labels_to_propagate=(AUTO_MERGE_LABEL, "arbitrary-label", "bug"),
            )
        ]

        result = propagate_linked_issue_labels(provider, prs)

        # Only the allowlisted label must be forwarded to the provider.
        provider.add_label.assert_called_once_with(2020, AUTO_MERGE_LABEL)
        assert result == {2020: [AUTO_MERGE_LABEL]}
