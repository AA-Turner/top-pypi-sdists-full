"""Tests for cascade complete with no skips (eligible=None, skipped=[])."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


class TestCascadeCompleteNoSkips:
    """Cover the branch where eligible is None and skipped is empty."""

    def test_all_children_already_processed_no_skips(self, tmp_path: Path) -> None:
        """When all children are already processed (closed), no skip notice posted."""
        meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[ChildInfo(number=10, title="A"), ChildInfo(number=20, title="B")],
        )
        yml = tmp_path / "hierarchy.yml"

        posted_comments: list[str] = []

        def track_comment(issue: int, body: str) -> bool:
            posted_comments.append(body)
            return True

        with (
            patch("agentic_devtools.hierarchy.cascade.read_hierarchy_yml", return_value=meta),
            patch.object(CascadeProcessor, "_find_eligible_child", return_value=(None, [], None)),
            patch.object(CascadeProcessor, "_post_comment", side_effect=track_comment),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_first_child(42, yml)

        assert result.action == CascadeAction.CASCADE_COMPLETE
        assert result.skipped_issues == []
        # Only the completion comment, no skip notice
        assert len(posted_comments) == 1
        assert "cascade complete" in posted_comments[0].lower()
