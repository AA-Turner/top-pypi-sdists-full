"""Tests for skip+exhaustion two-comment scenario (FR-005 + FR-006)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestSkipExhaustionTwoComments:
    """Tests that skip+exhaustion posts two separate comments."""

    def test_all_remaining_skipped_posts_two_comments(self, tmp_path: Path) -> None:
        """When all remaining siblings are skipped, post skip notice then completion."""
        parent_dir = tmp_path / "50"
        parent_dir.mkdir()
        yml_path = parent_dir / "hierarchy.yml"
        yml_path.write_text(
            "level: feature\n"
            "parent: 10\n"
            "children:\n"
            "  - number: 101\n"
            "    title: Task A\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Skip Me\n"
            "    order: 2\n"
            "  - number: 103\n"
            "    title: Skip Me Too\n"
            "    order: 3\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict:
            if issue_number in (102, 103):
                return {"state": "open", "labels": [{"name": "speckit:skip"}]}
            return {"state": "open", "labels": []}

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.CASCADE_COMPLETE
        mock_label.assert_not_called()

        # Should post at least 3 comments:
        # 1. Skip notice on completed_child (101)
        # 2. Completion comment on completed_child (101)
        # 3. Parent notification on parent (50)
        calls = mock_comment.call_args_list
        assert len(calls) >= 3

        # First comment: skip notice
        skip_comment = calls[0][0][1]
        assert "ℹ️ **Cascade Skip Notice**" in skip_comment
        assert "#102" in skip_comment
        assert "#103" in skip_comment
        assert "No further cascade target remains" in skip_comment

        # Second comment: cascade complete
        complete_comment = calls[1][0][1]
        assert "✅ **SpecKit cascade complete** — No further sub-issues to process." == complete_comment

        # Third comment: parent notification
        parent_comment = calls[2][0][1]
        assert "✅ All subtasks have completed SpecKit processing." == parent_comment

    def test_all_children_skipped_first_child(self, tmp_path: Path) -> None:
        """When all children of a parent are skipped, post skip notice then completion."""
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 201\n"
            "    title: Skip A\n"
            "    order: 1\n"
            "  - number: 202\n"
            "    title: Skip B\n"
            "    order: 2\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict:
            return {"state": "open", "labels": [{"name": "speckit:skip"}]}

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.CASCADE_COMPLETE
        mock_label.assert_not_called()

        calls = mock_comment.call_args_list
        # Should post 2 comments: skip notice + completion
        assert len(calls) == 2

        skip_comment = calls[0][0][1]
        assert "ℹ️ **Cascade Skip Notice**" in skip_comment
        assert "#201" in skip_comment
        assert "#202" in skip_comment

        complete_comment = calls[1][0][1]
        assert "✅ **SpecKit cascade complete**" in complete_comment
