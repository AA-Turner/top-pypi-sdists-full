"""Tests for IdempotencyQueryProvider protocol (FR-010)."""

from __future__ import annotations

from agentic_devtools.adapters.idempotency_query_provider import IdempotencyQueryProvider
from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult


class TestIdempotencyQueryProvider:
    """Verify IdempotencyQueryProvider protocol definition."""

    def test_protocol_is_runtime_checkable(self):
        """Protocol can be used with isinstance() checks."""

        class _Impl:
            def find_existing_issue(self, orchestration_key: str) -> ProviderIssueResult | None:
                return None

            def find_existing_link(self, parent_provider_id: str, child_provider_id: str) -> ProviderLinkResult | None:
                return None

            def find_existing_dependency(
                self, issue_provider_id: str, blocked_by_provider_id: str
            ) -> ProviderLinkResult | None:
                return None

        assert isinstance(_Impl(), IdempotencyQueryProvider)

    def test_class_without_methods_fails_isinstance(self):
        """A class missing any of the 3 methods does not satisfy the protocol."""

        class _Incomplete:
            def find_existing_issue(self, orchestration_key: str) -> ProviderIssueResult | None:
                return None

        assert not isinstance(_Incomplete(), IdempotencyQueryProvider)

    def test_protocol_has_exactly_three_methods(self):
        """Protocol defines exactly 3 public methods."""
        # Only count methods declared directly on this protocol.
        methods = [
            name
            for name, member in IdempotencyQueryProvider.__dict__.items()
            if not name.startswith("_") and callable(member)
        ]
        assert sorted(methods) == ["find_existing_dependency", "find_existing_issue", "find_existing_link"]
