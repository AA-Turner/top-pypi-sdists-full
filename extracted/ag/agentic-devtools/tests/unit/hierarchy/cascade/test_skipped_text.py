"""Tests for skipped_text branch in trigger_first_child and trigger_next_sibling."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


class TestSkippedTextBranch:
    """Cover the `if skipped:` branches that generate skipped_text."""

    def test_trigger_first_child_with_skipped(self, tmp_path: Path):
        """When some children are skipped, a skip comment is posted."""
        meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[
                ChildInfo(number=5, title="Closed"),
                ChildInfo(number=10, title="Eligible"),
            ],
        )
        yml = tmp_path / "hierarchy.yml"

        eligible = ChildInfo(number=10, title="Eligible")

        with (
            patch("agentic_devtools.hierarchy.cascade.read_hierarchy_yml", return_value=meta),
            patch.object(CascadeProcessor, "_find_eligible_child", return_value=(eligible, [5], None)),
            patch.object(CascadeProcessor, "_apply_label", return_value=True),
            patch.object(CascadeProcessor, "_post_comment", return_value=True),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_first_child(42, yml)
            assert result.action == CascadeAction.TRIGGERED
            assert 5 in result.skipped_issues

    def test_trigger_next_sibling_with_skipped(self, tmp_path: Path):
        """When siblings are skipped, a skip comment is posted."""
        meta = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[
                ChildInfo(number=5, title="Done"),
                ChildInfo(number=7, title="Skipped"),
                ChildInfo(number=10, title="Target"),
            ],
        )
        yml = tmp_path / "hierarchy.yml"

        eligible = ChildInfo(number=10, title="Target")

        with (
            patch("agentic_devtools.hierarchy.cascade.read_hierarchy_yml", return_value=meta),
            patch.object(CascadeProcessor, "_find_eligible_child", return_value=(eligible, [7], None)),
            patch.object(CascadeProcessor, "_apply_label", return_value=True),
            patch.object(CascadeProcessor, "_post_comment", return_value=True),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml)
            assert result.action == CascadeAction.TRIGGERED
            assert 7 in result.skipped_issues
