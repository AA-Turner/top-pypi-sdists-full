"""Tests for read_hierarchy_yml."""

from pathlib import Path

import pytest

from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml
from agentic_devtools.hierarchy.models import HierarchyLevel


class TestReadHierarchyYml:
    """Tests for hierarchy.yml deserialization and validation."""

    def test_reads_valid_yaml(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\nparent: null\nchildren:\n"
            "  - number: 101\n    title: Feature A\n    order: 1\n"
            "informational_children: []\n"
        )
        meta = read_hierarchy_yml(yml_path)
        assert meta.level == HierarchyLevel.EPIC
        assert meta.parent is None
        assert len(meta.children) == 1
        assert meta.children[0].number == 101
        assert meta.children[0].title == "Feature A"

    def test_reads_feature_with_parent(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: feature\nparent: 100\nchildren:\n  - number: 110\n    title: Task A\n    order: 1\n"
        )
        meta = read_hierarchy_yml(yml_path)
        assert meta.level == HierarchyLevel.FEATURE
        assert meta.parent == 100

    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "nonexistent.yml"
        with pytest.raises(FileNotFoundError):
            read_hierarchy_yml(yml_path)

    def test_empty_file_raises(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("")
        with pytest.raises(ValueError, match="empty"):
            read_hierarchy_yml(yml_path)

    def test_invalid_level_raises(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: invalid\nchildren: []\n")
        with pytest.raises(ValueError, match="Invalid hierarchy level"):
            read_hierarchy_yml(yml_path)

    def test_missing_level_raises(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("parent: null\nchildren: []\n")
        with pytest.raises(ValueError, match="Missing or invalid"):
            read_hierarchy_yml(yml_path)

    def test_non_dict_raises(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("- item1\n- item2\n")
        with pytest.raises(ValueError, match="Expected YAML mapping"):
            read_hierarchy_yml(yml_path)

    def test_reads_informational_children(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: task\nparent: 101\nchildren: []\ninformational_children:\n  - number: 330\n    title: Deep child\n"
        )
        meta = read_hierarchy_yml(yml_path)
        assert len(meta.informational_children) == 1
        assert meta.informational_children[0].number == 330

    def test_default_empty_children(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: task\nparent: 100\n")
        meta = read_hierarchy_yml(yml_path)
        assert meta.children == []
        assert meta.informational_children == []
