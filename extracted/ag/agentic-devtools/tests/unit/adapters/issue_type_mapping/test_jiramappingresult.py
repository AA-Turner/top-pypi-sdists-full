"""Tests for JiraMappingResult frozen dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_type_mapping import JiraMappingResult


class TestJiraMappingResult:
    def test_construction_with_route(self) -> None:
        result = JiraMappingResult(type_name="Sub-task", labels=["backend"], route="parent")
        assert result.type_name == "Sub-task"
        assert result.labels == ["backend"]
        assert result.route == "parent"

    def test_construction_with_none_route(self) -> None:
        result = JiraMappingResult(type_name="Epic", labels=[], route=None)
        assert result.route is None

    def test_frozen(self) -> None:
        result = JiraMappingResult(type_name="Task", labels=[], route=None)
        with pytest.raises(AttributeError):
            result.type_name = "other"  # type: ignore[misc]
