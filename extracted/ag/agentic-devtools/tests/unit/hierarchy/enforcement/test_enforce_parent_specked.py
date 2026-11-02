"""Tests for enforce_parent_specked with standalone/no-parent paths."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.hierarchy.enforcement import EnforcementAction, enforce_parent_specked
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class TestEnforceParentSpecked:
    """Cover standalone and no-parent branches."""

    def test_standalone_always_allowed(self, tmp_path: Path):
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE, parent=None)
        result = enforce_parent_specked(42, meta, tmp_path)
        assert result.action == EnforcementAction.ALLOW
        assert "Standalone" in result.reason

    def test_no_parent_allowed(self, tmp_path: Path):
        meta = HierarchyMetadata(level=HierarchyLevel.EPIC, parent=None)
        result = enforce_parent_specked(42, meta, tmp_path)
        assert result.action == EnforcementAction.ALLOW
        assert "Top-level" in result.reason

    def test_parent_specked_via_hierarchical_path(self, tmp_path: Path):
        """Parent has a spec directory at hierarchical path."""
        specs_root = tmp_path / "specs"
        (specs_root / "10").mkdir(parents=True)
        meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=10)
        result = enforce_parent_specked(42, meta, specs_root)
        assert result.action == EnforcementAction.ALLOW

    def test_parent_not_specked_rejected(self, tmp_path: Path):
        """Parent has no spec directory anywhere."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir(parents=True)
        meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=10)
        result = enforce_parent_specked(42, meta, specs_root)
        assert result.action == EnforcementAction.REJECT
        assert result.parent_issue == 10
