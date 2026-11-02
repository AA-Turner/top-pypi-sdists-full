"""Tests for the audit provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderAuditMixin:
    """Tests for the audit provider capability."""

    def test_list_closed_prs_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_closed_prs"):
            provider.list_closed_prs(exclude_labels=["audited"], limit=10)

    def test_claim_pr_for_audit_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement claim_pr_for_audit"):
            provider.claim_pr_for_audit(pr_number=1, label="in-progress")

    def test_add_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement add_label"):
            provider.add_label(pr_number=1, label="audited")

    def test_remove_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement remove_label"):
            provider.remove_label(pr_number=1, label="in-progress")

    def test_count_prs_without_labels_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement count_prs_without_labels"):
            provider.count_prs_without_labels(exclude_labels=["audited"])

    def test_list_all_review_comments_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_all_review_comments"):
            provider.list_all_review_comments(pr_number=1)
