"""Tests for the ``HierarchyValidationProvider`` companion capability protocol.

Covers FR-016: the runtime-checkable protocol exposes exactly
``validate_issue_type`` and ``validate_hierarchy_pair`` and is satisfied by any
object structurally implementing both, without altering the eight-method
``IssueProvider`` contract.
"""

from __future__ import annotations

from agentic_devtools.adapters.issue_provider import (
    HierarchyValidationProvider,
    InMemoryIssueProvider,
)


class TestHierarchyValidationProtocol:
    def test_inmemory_provider_satisfies_protocol(self):
        assert isinstance(InMemoryIssueProvider("github"), HierarchyValidationProvider)

    def test_object_with_both_methods_satisfies_protocol(self):
        class _Stub:
            def validate_issue_type(self, issue_type):  # pragma: no cover - trivial
                return None

            def validate_hierarchy_pair(self, child_type, parent_type):  # pragma: no cover
                return None

        assert isinstance(_Stub(), HierarchyValidationProvider)

    def test_object_missing_a_method_fails_protocol(self):
        class _Partial:
            def validate_issue_type(self, issue_type):  # pragma: no cover - trivial
                return None

        assert not isinstance(_Partial(), HierarchyValidationProvider)

    def test_plain_object_fails_protocol(self):
        assert not isinstance(object(), HierarchyValidationProvider)
