"""Tests for grandchild enforcement (Task whose Feature parent is unspecked)."""

from pathlib import Path

from agentic_devtools.hierarchy.enforcement import EnforcementAction, enforce_parent_specked
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class TestGrandchildEnforcement:
    """Tests for grandchild (depth-2) enforcement."""

    def test_rejects_when_parent_feature_unspecked(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        # Epic dir exists but feature dir does not
        (specs_root / "100").mkdir()

        meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=101)
        result = enforce_parent_specked(110, meta, specs_root, ancestors=[100])
        assert result.action == EnforcementAction.REJECT

    def test_allows_when_parent_feature_specked(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        # Create epic and feature dirs
        (specs_root / "100" / "101").mkdir(parents=True)

        meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=101)
        result = enforce_parent_specked(110, meta, specs_root, ancestors=[100])
        assert result.action == EnforcementAction.ALLOW
