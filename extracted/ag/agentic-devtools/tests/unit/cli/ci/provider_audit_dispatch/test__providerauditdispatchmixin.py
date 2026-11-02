"""Tests for the audit dispatch provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderAuditDispatchMixin:
    """Tests for the audit dispatch provider capability."""

    def test_create_pull_request_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement create_pull_request"):
            provider.create_pull_request(title="My PR", body="Body")

    def test_create_audit_tracking_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement create_audit_tracking_issue"):
            provider.create_audit_tracking_issue(batch_id="abc123", pr_numbers=[1, 2])

    def test_dispatch_audit_evaluation_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement dispatch_audit_evaluation"):
            provider.dispatch_audit_evaluation(
                tracking_issue=2042,
                batch_id="abc123",
                batch_branch="audit/batch-abc123",
                batch_dir="audit-batches/abc123",
                pr_numbers=[1, 2],
            )
