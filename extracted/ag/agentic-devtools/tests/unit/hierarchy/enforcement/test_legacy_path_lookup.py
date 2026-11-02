"""Tests for legacy flat path acceptance in enforcement."""

from pathlib import Path

from agentic_devtools.hierarchy.enforcement import EnforcementAction, enforce_parent_specked
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class TestLegacyPathLookup:
    """Tests that legacy flat paths (specs/{number}-*/) are accepted."""

    def test_accepts_legacy_flat_path(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        (specs_root / "100-user-auth").mkdir(parents=True)

        meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        result = enforce_parent_specked(101, meta, specs_root)
        assert result.action == EnforcementAction.ALLOW
        assert result.parent_path is not None

    def test_rejects_when_no_flat_path(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        specs_root.mkdir()

        meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        result = enforce_parent_specked(101, meta, specs_root)
        assert result.action == EnforcementAction.REJECT
