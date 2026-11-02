"""Tests for the issue inventory provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderIssueInventoryMixin:
    """Tests for the issue inventory provider capability."""

    def test_list_no_change_candidate_prs_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_no_change_candidate_prs"):
            provider.list_no_change_candidate_prs()

    def test_get_pr_tree_state_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_pr_tree_state"):
            provider.get_pr_tree_state(1)

    def test_get_issue_facts_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_issue_facts"):
            provider.get_issue_facts(1)

    def test_get_file_line_count_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_file_line_count"):
            provider.get_file_line_count("abc123", "src/module.py")

    def test_list_linked_issue_labels_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_linked_issue_labels"):
            provider.list_linked_issue_labels(pr_number=11)

    def test_list_prs_with_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_prs_with_label"):
            provider.list_prs_with_label("in-progress")

    def test_get_label_applied_at_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_label_applied_at"):
            provider.get_label_applied_at(pr_number=1, label="in-progress")
