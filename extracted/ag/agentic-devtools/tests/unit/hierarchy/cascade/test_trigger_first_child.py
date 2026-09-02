"""Tests for trigger_first_child (parent-to-child cascade)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.models import CascadeDirection


class TestTriggerFirstChild:
    """Tests for parent-to-child cascade on final-phase merge."""

    def test_triggers_first_eligible_child(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 101\n"
            "    title: Feature A\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Feature B\n"
            "    order: 2\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        # Mock API calls
        with (
            patch.object(processor, "_get_issue_state") as mock_state,
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_state.return_value = {"state": "open", "labels": []}
            mock_label.return_value = True
            mock_comment.return_value = True

            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 101
        assert result.event.direction == CascadeDirection.PARENT_TO_CHILD
        mock_label.assert_called_once_with(101)

    def test_no_children_posts_comment(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: epic\nparent: null\nchildren: []\ninformational_children: []\n")

        processor = CascadeProcessor(owner="org", repo="repo")
        with patch.object(processor, "_post_comment") as mock_comment:
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.NO_CHILDREN
        assert "No further sub-issues" in result.comment
        mock_comment.assert_called_once()

    def test_halts_when_label_application_fails(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\nparent: null\nchildren:\n"
            "  - number: 101\n    title: Feature A\n    order: 1\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        with (
            patch.object(processor, "_get_issue_state", return_value={"state": "open", "labels": []}),
            patch.object(processor, "_apply_label", return_value=False),
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "Failed to apply the `speckit` label" in result.comment
        mock_comment.assert_called_once()
