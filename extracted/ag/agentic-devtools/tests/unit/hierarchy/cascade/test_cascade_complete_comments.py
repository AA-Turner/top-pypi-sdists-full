"""Tests for cascade completion comments (FR-006, FR-007)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestCascadeCompleteComments:
    """Tests for completion comment posting on cascade exhaustion."""

    def test_last_sibling_posts_completion_on_task(self, tmp_path: Path) -> None:
        """When last sibling completes, post completion comment on task."""
        parent_dir = tmp_path / "50"
        parent_dir.mkdir()
        yml_path = parent_dir / "hierarchy.yml"
        yml_path.write_text(
            "level: feature\nparent: 10\nchildren:\n"
            "  - number: 101\n    title: Task A\n    order: 1\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        with patch.object(processor, "_post_comment") as mock_comment:
            mock_comment.return_value = True
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.CASCADE_COMPLETE
        # Verify exact comment format (FR-006)
        assert "✅ **SpecKit cascade complete** — No further sub-issues to process." in result.comment

    def test_last_sibling_posts_parent_notification(self, tmp_path: Path) -> None:
        """When last sibling completes, also post notification on parent (FR-007)."""
        parent_dir = tmp_path / "50"
        parent_dir.mkdir()
        yml_path = parent_dir / "hierarchy.yml"
        yml_path.write_text(
            "level: feature\nparent: 10\nchildren:\n"
            "  - number: 101\n    title: Task A\n    order: 1\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        with patch.object(processor, "_post_comment") as mock_comment:
            mock_comment.return_value = True
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.CASCADE_COMPLETE
        # Should post two comments: one on completed_child (101), one on parent (50)
        comments_posted = [c[0] for c in mock_comment.call_args_list]
        # First call: (101, "✅ **SpecKit cascade complete** ...")
        assert comments_posted[0] == (101, "✅ **SpecKit cascade complete** — No further sub-issues to process.")
        # Second call: (50, "✅ All subtasks have completed SpecKit processing.")
        assert comments_posted[1] == (50, "✅ All subtasks have completed SpecKit processing.")

    def test_first_child_no_children_posts_cascade_complete(self, tmp_path: Path) -> None:
        """When parent has no children, post cascade complete (FR-006)."""
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: epic\nparent: null\nchildren: []\ninformational_children: []\n")

        processor = CascadeProcessor(owner="org", repo="repo")

        with patch.object(processor, "_post_comment") as mock_comment:
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.NO_CHILDREN
        comment_text = mock_comment.call_args[0][1]
        assert "✅ **SpecKit cascade complete** — No further sub-issues to process." == comment_text
