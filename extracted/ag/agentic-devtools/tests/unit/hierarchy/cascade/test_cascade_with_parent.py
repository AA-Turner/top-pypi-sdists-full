"""Tests for cascade with parent_for_comment truthy path in trigger_next_sibling."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor, IssueStateError
from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


def _make_metadata(parent: int | None, children: list[ChildInfo]) -> HierarchyMetadata:
    return HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=parent, children=children)


def _track_post(posted_to: list[int]) -> object:
    """Create a side_effect callable that tracks posted issue numbers."""

    def _side_effect(n: int, _: str) -> bool:
        posted_to.append(n)
        return True

    return _side_effect


class TestCascadeWithParent:
    """Cover parent_for_comment truthy path (when metadata.parent is set)."""

    def test_halted_posts_to_parent(self, tmp_path: Path):
        """When pipeline_failed=True and parent is set, comment goes to parent."""
        meta = _make_metadata(parent=100, children=[ChildInfo(number=5, title="A")])
        yml = tmp_path / "hierarchy.yml"

        posted_to: list[int] = []

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(CascadeProcessor, "_post_comment", side_effect=_track_post(posted_to)),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml, pipeline_failed=True)
            assert result.action == CascadeAction.HALTED
            assert 100 in posted_to

    def test_cascade_complete_posts_to_parent(self, tmp_path: Path):
        """When no eligible sibling and parent is set, comment goes to parent."""
        meta = _make_metadata(parent=100, children=[ChildInfo(number=5, title="A")])
        yml = tmp_path / "hierarchy.yml"

        posted_to: list[int] = []

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(
                CascadeProcessor,
                "_find_eligible_child",
                return_value=(None, [], None),
            ),
            patch.object(CascadeProcessor, "_post_comment", side_effect=_track_post(posted_to)),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml)
            assert result.action == CascadeAction.CASCADE_COMPLETE
            assert 100 in posted_to

    def test_triggered_posts_to_parent(self, tmp_path: Path):
        """When eligible sibling found and parent is set, comment goes to parent."""
        child = ChildInfo(number=10, title="Sibling")
        meta = _make_metadata(parent=100, children=[ChildInfo(number=5, title="A"), child])
        yml = tmp_path / "hierarchy.yml"

        posted_to: list[int] = []

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(
                CascadeProcessor,
                "_find_eligible_child",
                return_value=(child, [], None),
            ),
            patch.object(CascadeProcessor, "_apply_label", return_value=True),
            patch.object(CascadeProcessor, "_post_comment", side_effect=_track_post(posted_to)),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml)
            assert result.action == CascadeAction.TRIGGERED
            assert 100 in posted_to

    def test_no_parent_does_not_post(self, tmp_path: Path):
        """When parent is None and yml path directory is not an issue number, no comment."""
        meta = _make_metadata(parent=None, children=[ChildInfo(number=5, title="A")])
        # tmp_path.name is not a plain integer, so path inference falls back to
        # metadata.parent (None) → parent_for_comment = 0 → no post.
        yml = tmp_path / "hierarchy.yml"

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(CascadeProcessor, "_post_comment") as mock_post,
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml, pipeline_failed=True)
            assert result.action == CascadeAction.HALTED
            mock_post.assert_not_called()

    def test_no_parent_api_error_does_not_post(self, tmp_path: Path):
        """IssueStateError with no parent_for_comment: halted but no comment posted."""
        meta = _make_metadata(parent=None, children=[ChildInfo(number=5, title="A")])
        # tmp_path.name is not a plain integer → parent_for_comment = 0 → no post.
        yml = tmp_path / "hierarchy.yml"

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(
                CascadeProcessor,
                "_find_eligible_child",
                side_effect=IssueStateError("transient error"),
            ),
            patch.object(CascadeProcessor, "_post_comment") as mock_post,
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml)
            assert result.action == CascadeAction.HALTED
            assert "transient error" in result.comment
            mock_post.assert_not_called()

    def test_epic_path_posts_to_directory_issue_number(self, tmp_path: Path):
        """When yml is in a numeric dir (e.g. specs/10/) and parent is None, post to #10."""
        epic_dir = tmp_path / "10"
        epic_dir.mkdir()
        yml = epic_dir / "hierarchy.yml"

        meta = _make_metadata(parent=None, children=[ChildInfo(number=5, title="A")])
        posted_to: list[int] = []

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(CascadeProcessor, "_post_comment", side_effect=_track_post(posted_to)),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml, pipeline_failed=True)
            assert result.action == CascadeAction.HALTED
            assert 10 in posted_to

    def test_failed_issue_halt_posts_to_child_and_parent(self, tmp_path: Path):
        """speckit:failed halt posts to both completed_child and parent_for_comment."""
        failed_child = ChildInfo(number=10, title="Failed")
        meta = _make_metadata(parent=100, children=[ChildInfo(number=5, title="A"), failed_child])
        yml = tmp_path / "hierarchy.yml"

        posted_to: list[int] = []

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(
                CascadeProcessor,
                "_find_eligible_child",
                return_value=(None, [], 10),
            ),
            patch.object(CascadeProcessor, "_post_comment", side_effect=_track_post(posted_to)),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml)
            assert result.action == CascadeAction.HALTED
            assert "speckit:failed" in result.comment
            # Halt comment must appear on both completed_child (5) and parent (100)
            assert posted_to.count(5) == 1
            assert posted_to.count(100) == 1

    def test_failed_issue_halt_no_parent_posts_only_to_child(self, tmp_path: Path):
        """speckit:failed halt with no parent only posts to completed_child (no parent post)."""
        failed_child = ChildInfo(number=10, title="Failed")
        meta = _make_metadata(parent=None, children=[ChildInfo(number=5, title="A"), failed_child])
        # Use tmp_path directly so directory name is not a plain integer → parent_for_comment = 0
        yml = tmp_path / "hierarchy.yml"

        posted_to: list[int] = []

        with (
            patch(
                "agentic_devtools.hierarchy.cascade.read_hierarchy_yml",
                return_value=meta,
            ),
            patch.object(
                CascadeProcessor,
                "_find_eligible_child",
                return_value=(None, [], 10),
            ),
            patch.object(CascadeProcessor, "_post_comment", side_effect=_track_post(posted_to)),
        ):
            proc = CascadeProcessor("o", "r")
            result = proc.trigger_next_sibling(5, yml)
            assert result.action == CascadeAction.HALTED
            assert posted_to == [5]
