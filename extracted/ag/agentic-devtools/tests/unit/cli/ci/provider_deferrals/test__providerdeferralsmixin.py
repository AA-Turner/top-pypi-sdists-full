"""Tests for the deferrals provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderDeferralsMixin:
    """Tests for the deferrals provider capability."""

    def test_find_deferral_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement find_deferral_issue"):
            provider.find_deferral_issue(pr_number=11, review_id=42)

    def test_create_deferral_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement create_deferral_issue"):
            provider.create_deferral_issue(
                pr_number=11,
                review_id=42,
                base_sha="abc1234",
                findings=[("specs/spec.md", "finding")],
                labels=["suppressed-comment-follow-up"],
            )

    def test_dispatch_suppressed_triage_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement dispatch_suppressed_triage"):
            provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

    def test_count_open_issues_with_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement count_open_issues_with_label"):
            provider.count_open_issues_with_label("suppressed-comment-follow-up")
