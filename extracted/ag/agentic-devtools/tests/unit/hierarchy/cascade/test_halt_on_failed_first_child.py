"""Tests for cascade halt when first child has speckit:failed label (FR-004)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestHaltOnFailedFirstChild:
    """Tests that cascade halts when the first child has speckit:failed."""

    def test_halt_on_failed_first_child_epic(self, tmp_path: Path) -> None:
        """Epic→feature cascade halts when first feature has speckit:failed."""
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 101\n"
            "    title: Failed Feature\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Good Feature\n"
            "    order: 2\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict:
            if issue_number == 101:
                return {"state": "open", "labels": [{"name": "speckit:failed"}]}
            return {"state": "open", "labels": []}

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "speckit:failed" in result.comment
        assert "#101" in result.comment
        assert "Manual intervention required" in result.comment
        mock_label.assert_not_called()

    def test_halt_on_failed_feature_to_task(self, tmp_path: Path) -> None:
        """Feature→task cascade halts when first task has speckit:failed."""
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: feature\n"
            "parent: 50\n"
            "children:\n"
            "  - number: 201\n"
            "    title: Failed Task\n"
            "    order: 1\n"
            "  - number: 202\n"
            "    title: Good Task\n"
            "    order: 2\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict:
            if issue_number == 201:
                return {"state": "open", "labels": [{"name": "speckit:failed"}]}
            return {"state": "open", "labels": []}

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            result = processor.trigger_first_child(50, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "#201" in result.comment
        mock_label.assert_not_called()
