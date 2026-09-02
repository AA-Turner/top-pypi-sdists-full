"""Tests for trigger_next_sibling (sibling progression)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.models import CascadeDirection


class TestTriggerNextSibling:
    """Tests for sibling-to-sibling cascade on child final-phase merge."""

    def test_triggers_next_sibling(self, tmp_path: Path) -> None:
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
            "  - number: 103\n"
            "    title: Feature C\n"
            "    order: 3\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        with (
            patch.object(processor, "_get_issue_state") as mock_state,
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_state.return_value = {"state": "open", "labels": []}
            mock_label.return_value = True
            mock_comment.return_value = True

            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 102
        assert result.event.direction == CascadeDirection.SIBLING_TO_SIBLING

    def test_cascade_complete_when_last_sibling(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\nparent: null\nchildren:\n"
            "  - number: 101\n    title: Feature A\n    order: 1\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")
        with patch.object(processor, "_post_comment") as mock_comment:
            mock_comment.return_value = True
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.CASCADE_COMPLETE

    def test_halts_when_label_application_fails(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: 100\n"
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

        with (
            patch.object(processor, "_get_issue_state", return_value={"state": "open", "labels": []}),
            patch.object(processor, "_apply_label", return_value=False),
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "Failed to apply the `speckit` label" in result.comment
        mock_comment.assert_called_once()

    def test_halts_without_parent_comment_when_label_application_fails(self, tmp_path: Path) -> None:
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

        with (
            patch.object(processor, "_get_issue_state", return_value={"state": "open", "labels": []}),
            patch.object(processor, "_apply_label", return_value=False),
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "Failed to apply the `speckit` label" in result.comment
        mock_comment.assert_not_called()

    def test_halts_with_error_when_completed_child_not_in_children(self, tmp_path: Path) -> None:
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
        with patch.object(processor, "_post_comment") as mock_comment:
            mock_comment.return_value = True
            result = processor.trigger_next_sibling(999, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "not listed as a child" in result.comment

    def test_halts_with_comment_when_completed_child_not_in_children_and_parent_known(self, tmp_path: Path) -> None:
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
            result = processor.trigger_next_sibling(999, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "not listed as a child" in result.comment
        mock_comment.assert_called_once_with(50, result.comment)

    def test_uses_slugged_directory_prefix_for_parent_comment(self, tmp_path: Path) -> None:
        parent_dir = tmp_path / "50-feature-core"
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
            "    title: Task B\n"
            "    order: 2\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")
        with (
            patch.object(processor, "_get_issue_state", return_value={"state": "open", "labels": []}),
            patch.object(processor, "_apply_label", return_value=False),
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.HALTED
        mock_comment.assert_called_once_with(50, result.comment)
