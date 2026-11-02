"""Tests for hierarchical path resolution."""

from pathlib import Path

from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata
from agentic_devtools.hierarchy.path_resolver import resolve_spec_path


class TestResolveHierarchicalPath:
    """Tests for hierarchical nested path resolution (specs/{epic}/{feature}/{task}/)."""

    def test_epic_path(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            children=[ChildInfo(number=101, title="Feature A")],
        )
        path = resolve_spec_path(100, meta, specs_root)
        assert path == specs_root / "100"

    def test_feature_path_with_parent(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[ChildInfo(number=110, title="Task A")],
        )
        path = resolve_spec_path(101, meta, specs_root)
        assert path == specs_root / "100" / "101"

    def test_task_path_with_ancestors(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(
            level=HierarchyLevel.TASK,
            parent=101,
        )
        path = resolve_spec_path(110, meta, specs_root, ancestors=[100])
        assert path == specs_root / "100" / "101" / "110"

    def test_three_level_nesting(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(
            level=HierarchyLevel.TASK,
            parent=101,
        )
        path = resolve_spec_path(110, meta, specs_root, ancestors=[100, 101])
        assert path == specs_root / "100" / "101" / "110"

    def test_task_path_with_ancestors_and_short_name(self, tmp_path: Path) -> None:
        """short_name is ignored for hierarchical levels; path is strictly numeric."""
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=50)
        path = resolve_spec_path(101, meta, specs_root, short_name="auth-handler", ancestors=[10, 50])
        assert path == specs_root / "10" / "50" / "101"

    def test_feature_path_with_parent_and_short_name(self, tmp_path: Path) -> None:
        """Feature path is numeric only — short_name is ignored for hierarchical levels."""
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        path = resolve_spec_path(101, meta, specs_root, short_name="user-auth", ancestors=[100])
        assert path == specs_root / "100" / "101"

    def test_epic_path_with_short_name(self, tmp_path: Path) -> None:
        """Epic path is numeric only — short_name is ignored for hierarchical levels."""
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.EPIC, children=[ChildInfo(number=101, title="Feature A")])
        path = resolve_spec_path(100, meta, specs_root, short_name="core-platform")
        assert path == specs_root / "100"

    def test_no_slug_when_short_name_empty(self, tmp_path: Path) -> None:
        """Hierarchical leaf stays numeric when short_name is omitted."""
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=101)
        path = resolve_spec_path(110, meta, specs_root, ancestors=[100])
        assert path == specs_root / "100" / "101" / "110"
