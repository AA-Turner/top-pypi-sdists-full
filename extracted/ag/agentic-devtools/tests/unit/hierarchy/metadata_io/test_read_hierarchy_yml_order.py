"""Tests for order field parsing in read_hierarchy_yml."""

from pathlib import Path

import pytest

from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml


class TestReadHierarchyYmlOrder:
    """Tests for order field parsing edge cases."""

    def test_order_missing_defaults_to_none(self, tmp_path: Path) -> None:
        """Missing order field defaults to None for backward compatibility with pre-order hierarchy.yml files."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\nparent: 1\nchildren:\n  - number: 10\n    title: Child\ninformational_children: []\n"
        )
        metadata = read_hierarchy_yml(yml)
        assert metadata.children[0].order is None

    def test_order_bool_raises_value_error(self, tmp_path: Path) -> None:
        """Boolean order value raises ValueError."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\n"
            "parent: 1\n"
            "children:\n"
            "  - number: 10\n"
            "    title: Child\n"
            "    order: true\n"
            "informational_children: []\n"
        )
        with pytest.raises(ValueError, match="Invalid child order"):
            read_hierarchy_yml(yml)

    def test_order_string_numeric_parses(self, tmp_path: Path) -> None:
        """String numeric order value is parsed to int."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\n"
            "parent: 1\n"
            "children:\n"
            "  - number: 10\n"
            "    title: Child\n"
            "    order: '3'\n"
            "informational_children: []\n"
        )
        metadata = read_hierarchy_yml(yml)
        assert metadata.children[0].order == 3

    def test_order_non_numeric_string_raises(self, tmp_path: Path) -> None:
        """Non-numeric string order value raises ValueError."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\n"
            "parent: 1\n"
            "children:\n"
            "  - number: 10\n"
            "    title: Child\n"
            "    order: abc\n"
            "informational_children: []\n"
        )
        with pytest.raises(ValueError, match="Invalid child order"):
            read_hierarchy_yml(yml)

    def test_order_false_bool_raises(self, tmp_path: Path) -> None:
        """False boolean order raises ValueError (not treated as 0)."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\n"
            "parent: 1\n"
            "children:\n"
            "  - number: 10\n"
            "    title: Child\n"
            "    order: false\n"
            "informational_children: []\n"
        )
        with pytest.raises(ValueError, match="Invalid child order"):
            read_hierarchy_yml(yml)

    def test_order_integer_value_parsed(self, tmp_path: Path) -> None:
        """Integer order value is stored directly."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\n"
            "parent: 1\n"
            "children:\n"
            "  - number: 10\n"
            "    title: Child A\n"
            "    order: 2\n"
            "  - number: 20\n"
            "    title: Child B\n"
            "    order: 1\n"
            "informational_children: []\n"
        )
        metadata = read_hierarchy_yml(yml)
        assert metadata.children[0].order == 2
        assert metadata.children[1].order == 1

    def test_order_list_value_raises(self, tmp_path: Path) -> None:
        """List value for order raises ValueError (read_hierarchy_yml normalises conversion errors)."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\n"
            "parent: 1\n"
            "children:\n"
            "  - number: 10\n"
            "    title: Child\n"
            "    order: [1, 2]\n"
            "informational_children: []\n"
        )
        with pytest.raises(ValueError, match="Invalid child order"):
            read_hierarchy_yml(yml)

    def test_order_float_raises_value_error(self, tmp_path: Path) -> None:
        """Float order value raises ValueError (no silent truncation)."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text(
            "level: feature\n"
            "parent: 1\n"
            "children:\n"
            "  - number: 10\n"
            "    title: Child\n"
            "    order: 1.5\n"
            "informational_children: []\n"
        )
        with pytest.raises(ValueError, match="Invalid child order"):
            read_hierarchy_yml(yml)
