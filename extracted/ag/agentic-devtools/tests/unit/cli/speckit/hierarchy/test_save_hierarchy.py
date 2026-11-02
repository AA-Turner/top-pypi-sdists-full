"""Tests for save_hierarchy function."""

from datetime import UTC

import yaml

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyLevel,
    HierarchyNode,
    save_hierarchy,
)


class TestSaveHierarchy:
    """Tests for save_hierarchy function."""

    def test_creates_file(self, tmp_path):
        """Test that save_hierarchy creates a YAML file."""
        path = tmp_path / "hierarchy.yml"
        node = HierarchyNode(title="Epic", level=HierarchyLevel.EPIC)

        save_hierarchy(node, path)

        assert path.exists()

    def test_output_is_valid_yaml(self, tmp_path):
        """Test that saved file is valid YAML."""
        path = tmp_path / "hierarchy.yml"
        node = HierarchyNode(title="Feature", level=HierarchyLevel.FEATURE)
        save_hierarchy(node, path)

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_creates_parent_directories(self, tmp_path):
        """Test that parent directories are created."""
        path = tmp_path / "deep" / "nested" / "hierarchy.yml"
        node = HierarchyNode(title="Task", level=HierarchyLevel.TASK)

        save_hierarchy(node, path)

        assert path.exists()

    def test_canonical_key_order(self, tmp_path):
        """Test that output has canonical key order."""
        from datetime import datetime

        path = tmp_path / "hierarchy.yml"
        ts = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
        node = HierarchyNode(
            title="X",
            level=HierarchyLevel.EPIC,
            parent="5",
            children=[ChildEntry(key="10", title="C", order=1)],
            processed_at=ts,
        )
        save_hierarchy(node, path)

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert list(data.keys()) == [
            "title",
            "level",
            "parent",
            "children",
            "processed_at",
        ]

    def test_null_fields_explicit(self, tmp_path):
        """Test that None fields are serialized as null."""
        path = tmp_path / "hierarchy.yml"
        node = HierarchyNode(title="X", level=HierarchyLevel.TASK)
        save_hierarchy(node, path)

        content = path.read_text(encoding="utf-8")
        assert "parent: null" in content
        assert "processed_at: null" in content

    def test_children_serialized_correctly(self, tmp_path):
        """Test that children list is serialized with correct structure."""
        path = tmp_path / "hierarchy.yml"
        node = HierarchyNode(
            title="F",
            level=HierarchyLevel.FEATURE,
            children=[
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
            ],
        )
        save_hierarchy(node, path)

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert len(data["children"]) == 2
        assert data["children"][0] == {"key": "1", "title": "First", "order": 1}
        assert data["children"][1] == {"key": "2", "title": "Second", "order": 2}

    def test_processed_at_serialized_as_iso8601(self, tmp_path):
        """Test that processed_at is serialized as ISO-8601 string."""
        from datetime import datetime

        path = tmp_path / "hierarchy.yml"
        ts = datetime(2024, 6, 15, 14, 30, 0, tzinfo=UTC)
        node = HierarchyNode(title="X", level=HierarchyLevel.EPIC, processed_at=ts)
        save_hierarchy(node, path)

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["processed_at"] == "2024-06-15T14:30:00+00:00"
