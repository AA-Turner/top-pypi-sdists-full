"""Tests for no-children cascade comment."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestNoChildren:
    """Tests FR-010: comment posted when no children to cascade to."""

    def test_posts_comment_on_empty_children(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: epic\nparent: null\nchildren: []\ninformational_children: []\n")

        processor = CascadeProcessor(owner="org", repo="repo")

        with patch.object(processor, "_post_comment") as mock_comment:
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.NO_CHILDREN
        mock_comment.assert_called_once()
        # Comment should mention cascade complete
        comment_text = mock_comment.call_args[0][1]
        assert "No further sub-issues" in comment_text
