"""Tests confirming no hierarchy.yml generated for standalone issues."""

from pathlib import Path

from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class TestStandaloneNoYml:
    """Tests that standalone (non-hierarchical) issues get no hierarchy.yml."""

    def test_standalone_skips_write(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        result = write_hierarchy_yml(yml_path, meta)
        assert result is False
        assert not yml_path.exists()

    def test_standalone_with_no_parent_no_children(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        meta = HierarchyMetadata(
            level=HierarchyLevel.STANDALONE,
            parent=None,
            children=[],
        )
        result = write_hierarchy_yml(yml_path, meta)
        assert result is False
        assert not yml_path.exists()
