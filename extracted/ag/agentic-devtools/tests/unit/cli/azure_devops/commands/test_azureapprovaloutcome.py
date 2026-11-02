"""Tests for the AzureApprovalOutcome dataclass."""

import pytest

from agentic_devtools.cli.azure_devops.commands import AzureApprovalOutcome


class TestAzureApprovalOutcome:
    """Tests for AzureApprovalOutcome's constructor/field contract."""

    def test_resolved_true_with_default_thread_id(self) -> None:
        """thread_id defaults to None when not provided."""
        outcome = AzureApprovalOutcome(resolved=True)

        assert outcome.resolved is True
        assert outcome.thread_id is None
        assert outcome.operation_kind is None

    def test_resolved_true_with_explicit_thread_id(self) -> None:
        """A resolved outcome may still carry the fallback thread ID."""
        outcome = AzureApprovalOutcome(resolved=True, thread_id=123, operation_kind="fallback_comment")

        assert outcome.resolved is True
        assert outcome.thread_id == 123
        assert outcome.operation_kind == "fallback_comment"

    def test_resolved_false_with_thread_id(self) -> None:
        """An unresolved outcome retains the thread ID for retry/dedup purposes."""
        outcome = AzureApprovalOutcome(resolved=False, thread_id=55, operation_kind="fallback_comment")

        assert outcome.resolved is False
        assert outcome.thread_id == 55
        assert outcome.operation_kind == "fallback_comment"

    def test_equality_between_equivalent_instances(self) -> None:
        """Instances with the same field values compare equal (dataclass semantics)."""
        assert AzureApprovalOutcome(resolved=True, thread_id=1) == AzureApprovalOutcome(resolved=True, thread_id=1)
        assert AzureApprovalOutcome(resolved=True) != AzureApprovalOutcome(resolved=False)

    def test_is_frozen(self) -> None:
        """The dataclass is immutable; attribute assignment raises."""
        outcome = AzureApprovalOutcome(resolved=True)

        with pytest.raises(AttributeError):
            outcome.resolved = False  # type: ignore[misc]
