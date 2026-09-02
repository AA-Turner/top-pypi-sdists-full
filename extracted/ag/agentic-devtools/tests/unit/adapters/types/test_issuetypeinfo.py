"""Tests for agentic_devtools.adapters.types.IssueTypeInfo."""

from __future__ import annotations

from agentic_devtools.adapters.base import IssueTypeInfo as IssueTypeInfoFromBase
from agentic_devtools.adapters.types import IssueTypeInfo


class TestIssueTypeInfo:
    """Tests for the IssueTypeInfo TypedDict."""

    def test_importable_from_types_module(self) -> None:
        """IssueTypeInfo can be imported from agentic_devtools.adapters.types."""
        assert IssueTypeInfo is not None

    def test_importable_from_base_module(self) -> None:
        """IssueTypeInfo can be imported from agentic_devtools.adapters.base."""
        assert IssueTypeInfoFromBase is IssueTypeInfo

    def test_importable_from_package(self) -> None:
        """IssueTypeInfo can be imported from agentic_devtools.adapters."""
        from agentic_devtools.adapters import IssueTypeInfo as IssueTypeInfoFromPkg

        assert IssueTypeInfoFromPkg is IssueTypeInfo

    def test_instantiation_with_required_fields(self) -> None:
        """IssueTypeInfo can be instantiated with name and description."""
        info: IssueTypeInfo = {"name": "Bug", "description": "A software defect"}
        assert info["name"] == "Bug"
        assert info["description"] == "A software defect"

    def test_instantiation_with_empty_description(self) -> None:
        """IssueTypeInfo accepts empty string for description."""
        info: IssueTypeInfo = {"name": "Task", "description": ""}
        assert info["name"] == "Task"
        assert info["description"] == ""
