"""Tests for halt-on-failure (no next sibling triggered on pipeline failure)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestHaltOnFailure:
    """Tests FR-011: halt cascade when pipeline fails."""

    def test_halts_on_pipeline_failure(self, tmp_path: Path) -> None:
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
            result = processor.trigger_next_sibling(101, yml_path, pipeline_failed=True)

        assert result.action == CascadeAction.HALTED
        assert "halted" in result.comment.lower()

    def test_halts_on_speckit_failed_label(self, tmp_path: Path) -> None:
        """FR-004: halt when next candidate has speckit:failed label."""
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

        def mock_state(issue_number: int) -> dict:
            if issue_number == 102:
                return {"state": "open", "labels": [{"name": "speckit:failed"}]}
            return {"state": "open", "labels": []}

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "speckit:failed" in result.comment
        assert "#102" in result.comment
        assert "Manual intervention required" in result.comment
        mock_label.assert_not_called()
