"""Tests verifying existing flat specs remain untouched."""

from pathlib import Path

from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata
from agentic_devtools.hierarchy.path_resolver import resolve_spec_path


class TestBackwardCompatibility:
    """Tests that standalone path resolution is backward compatible."""

    def test_standalone_does_not_create_nested(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        (specs_root / "200-existing-spec").mkdir(parents=True)

        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(200, meta, specs_root, short_name="existing-spec")
        assert path == specs_root / "200-existing-spec"
        # Existing dir should still be there
        assert (specs_root / "200-existing-spec").is_dir()

    def test_hierarchical_does_not_affect_standalone(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        # Pre-existing flat spec
        existing = specs_root / "200-old-spec"
        existing.mkdir(parents=True)
        (existing / "spec.md").write_text("old spec")

        # New hierarchical issue should get its own path
        meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            children=[],
        )
        path = resolve_spec_path(100, meta, specs_root)
        assert path != existing
        assert (existing / "spec.md").read_text() == "old spec"
