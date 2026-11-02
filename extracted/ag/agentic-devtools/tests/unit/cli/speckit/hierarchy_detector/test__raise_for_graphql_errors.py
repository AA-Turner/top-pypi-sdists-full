"""Tests for _raise_for_graphql_errors helper."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.hierarchy import HierarchyValidationError
from agentic_devtools.cli.speckit.hierarchy_detector import _raise_for_graphql_errors


class TestRaiseForGraphQLErrors:
    """Tests for _raise_for_graphql_errors helper."""

    def test_non_dict_payload_is_ignored(self) -> None:
        """Non-dict payloads do not raise GraphQL errors."""
        _raise_for_graphql_errors(["not", "a", "dict"])

    def test_non_dict_error_entries_are_stringified(self) -> None:
        """Non-dict GraphQL error entries are stringified in the exception."""
        with pytest.raises(HierarchyValidationError, match="plain-error"):
            _raise_for_graphql_errors({"errors": ["plain-error"]})
