"""Tests for _resolve_type helper (FR-006)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import IssueTypeMappingError
from agentic_devtools.adapters.issue_type_mapping import _resolve_type


class TestResolveType:
    def test_successful_lookup(self) -> None:
        mapping = {"epic": "Epic", "task": "Task"}
        assert _resolve_type("epic", mapping) == "Epic"

    def test_missing_key_raises(self) -> None:
        mapping = {"epic": "Epic"}
        with pytest.raises(IssueTypeMappingError, match="Cannot resolve issue type 'task'"):
            _resolve_type("task", mapping)

    def test_error_contains_available_mappings(self) -> None:
        mapping = {"bug": "Bug", "epic": "Epic"}
        with pytest.raises(IssueTypeMappingError, match=r"Available mappings: \['bug', 'epic'\]"):
            _resolve_type("task", mapping)

    def test_whitespace_only_value_raises(self) -> None:
        mapping = {"epic": "   "}
        with pytest.raises(
            IssueTypeMappingError,
            match=r"Resolved issue type 'epic' to an empty mapping value\..*Available mappings",
        ):
            _resolve_type("epic", mapping)

    def test_non_string_value_raises_mapping_error(self) -> None:
        mapping = {"epic": 42}  # type: ignore[dict-item]
        with pytest.raises(IssueTypeMappingError, match="must be a string"):
            _resolve_type("epic", mapping)  # type: ignore[arg-type]
