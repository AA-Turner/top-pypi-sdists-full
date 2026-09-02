"""Tests for all children being skipped (ineligible) in trigger_first_child."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


class TestAllChildrenSkipped:
    """Cover the path where _find_eligible_child returns None with skipped list."""

    def test_all_children_ineligible(self, tmp_path: Path):
        meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[ChildInfo(number=10, title="A"), ChildInfo(number=20, title="B")],
        )
        yml = tmp_path / "hierarchy.yml"

        with (
            patch("agentic_devtools.hierarchy.cascade.read_hierarchy_yml", return_value=meta),
            patch.object(CascadeProcessor, "_find_eligible_child", return_value=(None, [10, 20], None)),
            patch.object(CascadeProcessor, "_post_comment", return_value=True),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_first_child(42, yml)
            assert result.action == CascadeAction.CASCADE_COMPLETE
            assert result.skipped_issues == [10, 20]
