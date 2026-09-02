"""Tests for write_hierarchy_yml."""

from pathlib import Path

import yaml

from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


class TestWriteHierarchyYml:
    """Tests for hierarchy.yml serialization."""

    def test_writes_epic_metadata(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[
                ChildInfo(number=101, title="User authentication feature"),
                ChildInfo(number=102, title="Payment processing feature"),
            ],
        )
        result = write_hierarchy_yml(yml_path, meta)
        assert result is True
        assert yml_path.exists()

        data = yaml.safe_load(yml_path.read_text())
        assert data["level"] == "epic"
        assert data["parent"] is None
        assert len(data["children"]) == 2
        assert data["children"][0]["number"] == 101

    def test_writes_feature_metadata(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        meta = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[ChildInfo(number=110, title="Task A")],
        )
        result = write_hierarchy_yml(yml_path, meta)
        assert result is True

        data = yaml.safe_load(yml_path.read_text())
        assert data["level"] == "feature"
        assert data["parent"] == 100

    def test_skips_standalone(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        result = write_hierarchy_yml(yml_path, meta)
        assert result is False
        assert not yml_path.exists()

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "specs" / "100" / "hierarchy.yml"
        meta = HierarchyMetadata(level=HierarchyLevel.EPIC)
        write_hierarchy_yml(yml_path, meta)
        assert yml_path.exists()

    def test_writes_informational_children(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        meta = HierarchyMetadata(
            level=HierarchyLevel.TASK,
            parent=101,
            informational_children=[ChildInfo(number=330, title="Deep child")],
        )
        write_hierarchy_yml(yml_path, meta)
        data = yaml.safe_load(yml_path.read_text())
        assert len(data["informational_children"]) == 1
        assert data["informational_children"][0]["number"] == 330
